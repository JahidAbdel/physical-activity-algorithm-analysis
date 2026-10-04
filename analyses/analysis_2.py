import pandas as pd
import os
import time

def average_daily_steps(df):
    total = 0
    count = 0
    
    for value in df["ACTIVITY_steps"]:
        if pd.notna(value):
            total += value
            count += 1
    
    if count == 0:
        return 0
    
    return int(total / count)


def anomaly_detection(df, average_steps):
    anomaly_count = 0
    
    for value in df["ACTIVITY_steps"]:
        if pd.notna(value):
            if value <= average_steps * 0.5:
                anomaly_count += 1
    
    return anomaly_count


def sort_by_average(data):
    n = len(data)
    
    for i in range(n):
        maximum = i
    
        for j in range(i + 1, n):
            if data[j][1] > data[maximum][1]:
                maximum = j
    
        data[i], data[maximum] = data[maximum], data[i]
    
    return data


def sort_by_anomalies(data):
    n = len(data)
    
    for i in range(n):
        minimum = i
        
        for j in range(i + 1, n):
            if data[j][2] < data[minimum][2]:
                minimum = j
        
        data[i], data[minimum] = data[minimum], data[i]
    
    return data



directory_path = os.path.join(os.path.dirname(__file__), '..', 'researchdata')


results = []

start = time.time() #timing evidence

for file in os.listdir(directory_path):
    if file.endswith(".csv"):
        file_full_path = os.path.join(directory_path, file)
        df = pd.read_csv(file_full_path)
        participant = file.replace(".csv", "")
        average_steps = average_daily_steps(df)
        anomaly_count = anomaly_detection(df, average_steps)
        results.append((participant, average_steps, anomaly_count))


if not results:

    print("No participant data found in:", directory_path)

else:
   
    # Ranking from highest to lowest average daily steps per participant
    rank = 1
    ranked_by_average = sort_by_average(list(results))
    print("Ranking by average daily steps (highest to lowest):\n")
    for participant, average, _ in ranked_by_average:
        print(f"{rank}) Participant no.{participant} had an average of {average:,} steps/day")
        rank += 1

    print("\n\n-------------------------------------------------------------\n")

    # Ranking from lowest to highest anomalies detected per participant
    rank = 1
    ranked_by_anomalies = sort_by_anomalies(list(results))
    print("\nRanking by anomalous days (lowest to highest):\n")
    for participant, _, anomaly_count in ranked_by_anomalies:
        print(f"{rank}) Participant no.{participant} had {anomaly_count} anomalous day(s)")
        rank += 1
    end = time.time() #timing evidence
    print(f"\nTotal execution time : {end - start:.5f} seconds.")


    
# --- TESTS ---

# --- Comparing average_daily_steps() with Pandas .mean() ---

df_test = pd.DataFrame({"ACTIVITY_steps": [4000, 6000, float("nan"), 2000]})

assert average_daily_steps(df_test) == int(df_test["ACTIVITY_steps"].mean()), "Erreur: Le calcul manuel ne correspond pas à la fonction intégrée."

print("La fonction manuelle et la fonction intégrée donnent le même résultat !")

# --- average_daily_steps() ---

# Passing test: average is computed correctly, NaN values are skipped
df_test = pd.DataFrame({"ACTIVITY_steps": [4000, 6000, float("nan"), 2000]})
result = average_daily_steps(df_test)
assert result == 4000, f"Test failed: expected 4000 but got {result}"
print("average_daily_steps() — Passing test succeeded")
 
# Failing test: NaN is (incorrectly) expected to lower the average by counting as a 0
df_test2 = pd.DataFrame({"ACTIVITY_steps": [4000, 6000, float("nan"), 2000]})
result2 = average_daily_steps(df_test2)
assert result2 == 3000, f"Test failed: expected 3000 but got {result2}"  # Wrong: NaN is not counted
print("This line will NOT be reached")
 
# --- anomaly_detection() ---
 
# Passing test: only days at or below 50% of average are flagged
df_test3 = pd.DataFrame({"ACTIVITY_steps": [1000, 500, 200, 800]})  # average = 500 → threshold = 250
result3 = anomaly_detection(df_test3, 500)
assert result3 == 1, f"Test failed: expected 1 anomaly but got {result3}"  # Only 200 qualifies
print("anomaly_detection() — Passing test succeeded")
 
# Failing test: all days are (incorrectly) expected to be anomalies
df_test4 = pd.DataFrame({"ACTIVITY_steps": [1000, 500, 200, 800]})
result4 = anomaly_detection(df_test4, 500)
assert result4 == 4, f"Test failed: expected 4 anomalies but got {result4}"  # Wrong: only 1 qualifies
print("This line will NOT be reached")
 
# --- sort_by_average() ---
 
# Passing test: unsorted list is correctly sorted from highest to lowest average
unsorted_avg = [("A", 3000, 0), ("B", 9000, 0), ("C", 6000, 0)]
result5 = sort_by_average(list(unsorted_avg))
assert result5 == [("B", 9000, 0), ("C", 6000, 0), ("A", 3000, 0)], f"Test failed: got {result5}"
print("sort_by_average() — Passing test succeeded")
 
# Failing test: sorted list is (incorrectly) expected to remain in its original unsorted order
result6 = sort_by_average([("A", 3000, 0), ("B", 9000, 0), ("C", 6000, 0)])
assert result6 == [("A", 3000, 0), ("B", 9000, 0), ("C", 6000, 0)], f"Test failed: got {result6}"  # Wrong: sort changes order
print("This line will NOT be reached")
 
# --- sort_by_anomalies() ---
 
# Passing test: list is correctly sorted from fewest to most anomalies
unsorted_anom = [("A", 0, 5), ("B", 0, 1), ("C", 0, 3)]
result7 = sort_by_anomalies(list(unsorted_anom))
assert result7 == [("B", 0, 1), ("C", 0, 3), ("A", 0, 5)], f"Test failed: got {result7}"
print("sort_by_anomalies() — Passing test succeeded")
 
# Failing test: the already-lowest anomaly count is (incorrectly) expected to end up last
result8 = sort_by_anomalies([("A", 0, 5), ("B", 0, 1), ("C", 0, 3)])
assert result8[2] == ("B", 0, 1), f"Test failed: got {result8}"  # Wrong: B should be first, not last
print("This line will NOT be reached")
