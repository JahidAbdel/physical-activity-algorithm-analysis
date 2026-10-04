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


def longest_streak(df, average_steps):
    best_streak = 0
    current_streak = 0

    for value in df["ACTIVITY_steps"]:
        if pd.notna(value):
            if value >= average_steps:
                current_streak += 1
                if current_streak > best_streak:
                    best_streak = current_streak
            else:
                current_streak = 0
        else:
            current_streak = 0

    return best_streak


def build_graph(data, threshold):
    n = len(data)
    graph = {}

    for participant, _, _ in data:
        graph[participant] = []

    for i in range(n):
        for j in range(i + 1, n):
            participant_a, average_a, _ = data[i]
            participant_b, average_b, _ = data[j]

            if abs(average_a - average_b) <= threshold:
                graph[participant_a].append(participant_b)
                graph[participant_b].append(participant_a)

    return graph


def bfs(graph, start):
    visited = set()
    queue = [start]
    visited.add(start)

    while queue:
        current = queue.pop(0)

        for neighbor in graph[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return visited


def find_components(graph):
    visited = set()
    components = []

    for participant in graph:
        if participant not in visited:
            component = bfs(graph, participant)
            components.append(component)
            visited.update(component)

    return components


directory_path = os.path.join(os.path.dirname(__file__), '..', 'researchdata')
results = []

start = time.time()

for file in os.listdir(directory_path):
    if file.endswith(".csv"):
        file_full_path = os.path.join(directory_path, file)
        df = pd.read_csv(file_full_path)
        participant = file.replace(".csv", "")
        average_steps = average_daily_steps(df)
        personal_best_streak = longest_streak(df, average_steps)
        results.append((participant, average_steps, personal_best_streak))

print("\nPersonal longest streak per participant:\n")
enumeration = 1
for participant, _, personal_best_streak in results:
    print(f"   {enumeration}) Participant no.{participant} best streak was of {personal_best_streak} day(s)")
    enumeration += 1

graph = build_graph(results, 1000)
components = find_components(graph)

print("\nGroups of participants with similar activity levels (within 1,000 steps/day):\n")
for i, component in enumerate(components, start=1):
    print(f"   Group {i}: {', '.join(sorted(component))}")

end = time.time()
print(f"\nTotal execution time: {end - start:.5f} seconds.")
