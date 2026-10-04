# Physical Activity Algorithm Analysis

Academic project completed as part of the Applied Algorithms course at the University of Geneva.

This Python project analyses participant step-count data through aggregation, anomaly detection, selection sort, consecutive-streak analysis, and graph-based similarity grouping with breadth-first search (BFS).

## Prerequisites
- Python 3.10+
- `pip` to install Python dependencies
- A `researchdata/` folder containing the `.csv` files at the root of the project
---

## Installation via Terminal

### 1. Clone the Repository

```bash
git clone git@github.com:JahidAbdel/physical-activity-algorithm-analysis.git
cd physical-activity-algorithm-analysis
```

### 2. Create a virtual environment

***MacOS / Linux:***

```bash
python3 -m venv .venv
source .venv/bin/activate
```

***Windows (Powershell):***

```bash
python3 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the analyses

***Beginner analysis:***

```bash
python3 analyses/analysis_1.py
```

***Intermediate analysis:***

```bash
python3 analyses/analysis_2.py
```

***Advanced analysis:***

```bash
python3 analyses/analysis_3.py
```


## Beginner Analysis - Ranking participants by total steps

### 1. Problem

Which participant walked the most steps across the entire study period?
We rank all the participants from highest to lowest total steps count.

### 2. Algorithm

It will be done in two steps:

- **a) Aggregation**: (`overall_steps`): iterate over every daily row for a participant
  and sum the `ACTIVITY_steps` values, skipping missing entries to avoid errors.
- **b) Sorting**: (`sort_participants`): rank the (participant, total) pairs using
  **selection sort** on each pass, find the participant with the highest remaining
  total and move them to the front.

### 3. Why

Aggregation requires reading every row once, so a single loop is both necessary
and sufficient. Sorting is applied to only the number of participants, so
even an O(p²) algorithm like selection sort is instantaneous at that scale since we only have 12 participants.
Selection sort is chosen deliberately as a learning baseline: every comparison
and every swap is explicit and easy to trace.

### 4. Complexity

**`overall_steps(df)`**

- Time O(n) — we loop once over every row in the participant's CSV to sum the steps.
- Space O(1) — we only keep one running total, no matter how many rows there are.

**`sort_participants(data)`**

- Time O(p²) — selection sort compares every remaining element on each pass.
- Space O(1) — the list is sorted in-place, no extra list is created.

**Overall (across all participants)**

- Time O(p · n) — we call overall_steps once per participant, so p times.
- Space O(p) — the results list holds one (id, total) tuple per participant.

Where:
- n = number of daily rows per participant CSV
- p = number of participants


## Intermediate Analysis - Flagging unusual activity days for each participant 

### 1. Problem

For each participant, which days can be considered unusually low in terms of steps?
Instead of using a fixed threshold, we compare each participant's daily steps against
their own personal daily average, making the detection personalized.
A day is flagged as anomalous when the step count is 50% or less of the participant's average.
Finally we rank participants from highest to lowest average daily steps, then from lowest
to highest number of anomalous days.

### 2. Algorithm

It will be done in three steps:

- **a) Aggregation** (`average_daily_steps`): iterate over every daily row for a participant
  and compute their average daily step count, skipping missing entries.
- **b) Anomaly detection** (`anomaly_detection`): iterate over the daily rows again and count
  the days where steps are at or below 50% of the participant's average.
- **c) Sorting** (`sort_by_average`, `sort_by_anomalies`): rank the participants using
  **selection sort** once by average daily steps (highest to lowest), once by anomalous
  day count (lowest to highest).

### 3. Why

Computing the average requires reading every row once, so a single loop is both necessary
and sufficient. The same applies to anomaly detection — one pass is enough to count
the flagged days. Using a personal average instead of a fixed global threshold makes
the detection fairer.

### 4. Complexity

**`average_daily_steps(df)`**

- Time O(n) — we loop once over every row in the participant's CSV to compute the average.
- Space O(1) — only a running total and a counter are kept.

**`anomaly_detection(df, average_steps)`**

- Time O(n) — one pass through the daily rows to count anomalous days.
- Space O(1) — only a counter is kept.

**`sort_by_average(data)` and `sort_by_anomalies(data)`**

- Time O(p²) — selection sort compares every remaining element on each pass.
- Space O(1) — the list is sorted in-place, no extra list is created.

**Overall (across all participants)**

- Time O(p · n) — we call both functions once per participant, so p times.
- Space O(p) — the results list holds one (id, average, anomaly_count) tuple per participant.

Where:
- n = number of daily rows per participant CSV
- p = number of participants


## (BONUS) Advanced Analysis - Pattern similarity between participants 
### 1. Problem

For each participant, what is the longest consecutive streak of days where they met
or exceeded their own personal daily average in steps?
Additionally, which participants have similar activity levels to each other?
We model this as a graph where participants are nodes and edges connect participants
whose average daily steps are within 1,000 steps of each other, then use BFS to
find groups of similarly active participants.

### 2. Algorithm

It will be done in three steps:

- **a) Aggregation** (`average_daily_steps`): reused directly from the intermediate
  analysis to compute each participant's personal daily average.
- **b) Longest streak** (`longest_streak`): walk through the days in chronological
  order maintaining two counters `current_streak` and `best_streak`. If today's
  steps meet or exceed the participant's average, increment `current_streak`;
  otherwise reset it to 0. Update `best_streak` whenever `current_streak` exceeds it.
- **c) Similarity graph** (`build_graph`, `bfs`, `find_components`): build an adjacency
  list where two participants are connected if their average daily steps are within 1,000
  of each other. Then run BFS from every unvisited node to find all connected components —
  groups of participants with similar activity levels.

### 3. Why

The streak algorithm uses two running counters to carry the state forward day by day.
Because current_streak already encodes how many consecutive good days have occurred
up to the previous row, each new day only needs to check one condition and update
one value so that no past data needs to be read again. This makes the approach efficient (O(n))
and easy to follow step by step.
The graph models participant similarity represent closeness in activity
level, and BFS finds all reachable participants from a starting node level by level,
guaranteeing every connection is found without revisiting nodes.

### 4. Complexity

**`longest_streak(df, average_steps)`**

- Time O(n) — one pass through the daily rows.
- Space O(1) — only two counters are kept.

**`build_graph(data, threshold)`**

- Time O(p²) — every pair of participants is compared once.
- Space O(p + e) — p nodes and e edges in the adjacency list.

**`bfs(graph, start)`**

- Time O(p + e) — each node and each edge is visited at most once.
- Space O(p) — the visited set and queue hold at most p nodes.

**`find_components(graph)`**

- Time O(p + e) — BFS is called across all nodes exactly once in total.
- Space O(p) — the visited set holds at most p nodes.

**Overall (across all participants)**

- Time O(p · n + p²) — O(p · n) for streaks across all participants, O(p²) to build the graph.
- Space O(p) — results list and graph structures.

Where:
- n = number of daily rows per participant CSV
- p = number of participants
- e = number of edges in the graph

## Acknowledgements

This project was written and developed by me as part of the course work.
I used Claude as an assistant to help improve the structure, clarity, and English wording of the README documentation.

Claude also helped me better understand certain algorithmic approaches and problem-solving methodologies during development. However, the implementation and code logic were written by me, and the assistant was not used to directly generate the project’s source code.
