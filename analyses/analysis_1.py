import pandas as pd 
import os 

# First step: Get the total steps done by each participant
def overall_steps(df):
    total = 0
    for value in df["ACTIVITY_steps"]:
        if pd.notna(value): # In case we don't have the data of the number of steps done in a day by a partcipant 
            total += int(value)
    return total

# Second step: Ranking the partcipants from highest to lowest based on the overall steps done
def sort_participants(data):
    n = len(data)

    for i in range(n):
        maximum = i

        for j in range(i+1, n):
            if data[j][1] > data[maximum][1]: # Compares the 2 to see if its higher of lower 
                maximum = j

        data[i], data[maximum] = data[maximum], data[i] # Swapping the 2 

    return data


directory_path = os.path.join(os.path.dirname(__file__), '..', 'researchdata')  
results = []

for file in os.listdir(directory_path):
    if file.endswith(".csv"):
        file_full_path = os.path.join(directory_path, file)  
        df = pd.read_csv(file_full_path)
        total_steps = overall_steps(df)
        participant = file.replace(".csv", "")
        results.append((participant, total_steps))  # Adds the number of steps to the array for every partcipant 


if not results:
    print("No participant data found in:", directory_path)
else:
    sorted_results = sort_participants(results)


rank = int(1)
print("\nRanking by most steps walked across the entire study pediod (highest to lowest):\n")
for participant, steps in sorted_results:
    print(f"{rank}) Participant no.{participant} walked a total of {steps:,} steps.")
    rank += 1



# --- TESTS ---

# --- overall_steps() ---

# Passing test: total steps are summed correctly, NaN values are ignored
df_test = pd.DataFrame({"ACTIVITY_steps": [1000, 2000, float("nan"), 3000]})
result = overall_steps(df_test)
assert result == 6000, f"Test failed: expected 6000 but got {result}"
print("overall_steps() — Passing test succeeded")
 
# Failing test: NaN is (incorrectly) expected to be counted as 0 toward the total
df_test2 = pd.DataFrame({"ACTIVITY_steps": [1000, float("nan"), 500]})
result2 = overall_steps(df_test2)
assert result2 == 1501, f"Test failed: expected 1501 but got {result2}"  # Wrong expected value
print("This line will NOT be reached")
 
# --- sort_participants() ---
already_sorted = [("A", 9000), ("B", 6000), ("C", 3000)]
result3 = sort_participants(list(already_sorted))
assert result3 == [("A", 9000), ("B", 6000), ("C", 3000)], f"Test failed: got {result3}"
print("sort_participants() — Passing test succeeded")
 

unsorted = [("A", 3000), ("B", 9000), ("C", 6000)]
result4 = sort_participants(list(unsorted))
assert result4 == [("A", 3000), ("B", 9000), ("C", 6000)], f"Test failed: got {result4}"  # Wrong: sort changes the order
print("This line will NOT be reached")
