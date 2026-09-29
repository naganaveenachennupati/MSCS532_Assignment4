# MSCS 532 Assignment 4
## Heap Data Structures: Implementation, Analysis, and Applications

**Student:** Naga Naveena Chennupati  
**Course:** MSCS 532 – Algorithms and Data Structures  
**University:** University of the Cumberlands  

## Overview

This project examines heap data structures through two practical applications: Heapsort and a heap-based priority queue for task scheduling.

The sorting portion implements Heapsort using an array-based max heap and evaluates its performance against Randomized Quicksort and Merge Sort. The empirical comparison uses multiple input sizes and four different input distributions: random, sorted, reverse-sorted, and repeated-element data.

The priority queue portion implements a binary max heap for `Task` objects. Each task contains a task ID, priority, arrival time, execution time, and deadline. The priority queue supports insertion, extraction of the highest-priority task, priority increases and decreases, and empty-queue checks.

The priority queue is then applied to a non-preemptive scheduling simulation. The simulation tracks task execution order, waiting time, turnaround time, deadline completion, tardiness, and processor idle time.

---

## Repository

GitHub Repository:

https://github.com/naganaveenachennupati/MSCS532_Assignment4

---

## Project Structure

```text
MSCS532_Assignment4/
│
├── heapsort.py
├── comparison_sorts.py
├── benchmark_sorts.py
├── generate_graphs.py
├── priority_queue.py
├── scheduler_simulation.py
├── test_heapsort.py
├── test_priority_queue.py
├── test_scheduler.py
├── requirements.txt
├── README.md
│
└── results/
    ├── sorting_results.csv
    ├── scheduling_results.csv
    ├── random_comparison.png
    ├── sorted_comparison.png
    ├── reverse_sorted_comparison.png
    └── repeated_comparison.png
```

---

# Part I: Heapsort Implementation

## Heapsort Design

Heapsort is implemented using a binary max heap stored directly in a Python list.

For a node stored at index `i`:

- Left child: `2i + 1`
- Right child: `2i + 2`
- Parent: `(i - 1) // 2`

The implementation consists of three main steps:

1. Convert the input list into a max heap using bottom-up heap construction.
2. Swap the maximum element at the root with the final element in the active heap.
3. Reduce the heap size and restore the max-heap property.

The process continues until the entire list is sorted in ascending order.

The `max_heapify` operation is implemented iteratively rather than recursively. This avoids recursive call-stack overhead while still restoring the heap property efficiently.

The sorting operation modifies the original list in place and also returns the sorted list.

---

## Heapsort Time Complexity

### Max-Heapify

`max_heapify` follows at most one path from a node toward the bottom of the heap.

Because the height of a binary heap is proportional to `log n`, the worst-case running time of one heapify operation is:

```text
O(log n)
```

### Building the Max Heap

Although an individual heapify operation can require `O(log n)` time, building an entire max heap using the bottom-up procedure requires:

```text
O(n)
```

The reason is that most nodes are located near the leaves of the heap and require little or no downward movement.

Only a small number of nodes occur near the top of the heap, where larger heapify costs are possible.

Therefore, the combined work is bounded by a linear-time summation rather than `O(n log n)`.

### Sorting Phase

After the max heap is constructed, Heapsort performs up to `n - 1` extractions.

Each extraction may require a heapify operation costing:

```text
O(log n)
```

Therefore, the extraction phase requires:

```text
O(n log n)
```

Combining heap construction and extraction gives:

```text
O(n) + O(n log n) = O(n log n)
```

### Overall Complexity

| Case | Time Complexity |
|---|---|
| Best Case | `O(n log n)` |
| Average Case | `O(n log n)` |
| Worst Case | `O(n log n)` |

Heapsort therefore provides the same asymptotic running-time guarantee regardless of whether the input is initially random, sorted, reverse-sorted, or contains repeated values.

---

## Heapsort Space Complexity

The implementation sorts the list in place.

Because `max_heapify` is iterative and does not allocate another array proportional to the input size, Heapsort requires:

```text
O(1)
```

auxiliary space, excluding the original input list.

This is an important difference from the Merge Sort implementation used for comparison, which requires an auxiliary list proportional to the input size.

---

# Part II: Sorting Algorithm Comparison

## Comparison Algorithms

Heapsort was empirically compared with:

1. Randomized Quicksort
2. Merge Sort

### Randomized Quicksort

The Quicksort implementation selects a pivot randomly from the active subarray and uses Hoare partitioning.

The smaller partition is processed recursively while the larger partition is handled iteratively. This reduces recursive stack growth.

Randomized pivot selection helps prevent the input-order sensitivity associated with deterministic pivot choices such as always selecting the first or last element.

### Merge Sort

Merge Sort recursively divides the list into smaller portions and merges sorted ranges using an auxiliary list.

Its theoretical running time is:

```text
O(n log n)
```

for best, average, and worst cases.

Its main tradeoff compared with Heapsort is additional memory usage.

---

# Benchmark Methodology

The benchmark compares the three algorithms using the following input sizes:

```text
100
500
1,000
2,000
5,000
```

Four input distributions were tested:

- Random
- Sorted
- Reverse Sorted
- Repeated Values

Each algorithm was executed five times for every size and distribution.

The complete experiment therefore consisted of:

```text
5 input sizes
× 4 distributions
× 3 algorithms
× 5 trials
= 300 timed sorting executions
```

Reproducible random-number seeds were used to make the generated datasets consistent.

For the random, sorted, and reverse-sorted cases, the same underlying distinct values were used so that the main difference was input ordering.

The repeated-value datasets were generated from a smaller range of values to intentionally introduce duplicates.

---

## Timing Method

Python's:

```python
time.perf_counter_ns()
```

was used for high-resolution performance measurements.

To avoid including unrelated work in the timing measurement:

- the source dataset was copied before timing started;
- the expected result was generated before timing started;
- only the sorting operation itself was timed.

After every timed execution, the algorithm's output was compared with Python's built-in `sorted()` result.

If an algorithm produced an incorrect result, the benchmark would raise an error rather than record the timing.

For each configuration, the benchmark stores:

- Trial 1 runtime
- Trial 2 runtime
- Trial 3 runtime
- Trial 4 runtime
- Trial 5 runtime
- Mean runtime
- Sample standard deviation

The results are stored in:

```text
results/sorting_results.csv
```

---

# Sorting Results

At an input size of `n = 5000`, the final benchmark produced the following mean runtimes:

| Input Distribution | Heapsort | Randomized Quicksort | Merge Sort |
|---|---:|---:|---:|
| Random | 7.2376 ms | 4.9627 ms | 5.6812 ms |
| Sorted | 7.6021 ms | 3.9975 ms | 4.8285 ms |
| Reverse Sorted | 6.7596 ms | 4.0168 ms | 4.6984 ms |
| Repeated | 7.1007 ms | 4.4317 ms | 5.4142 ms |

---

## Analysis of Sorting Results

Randomized Quicksort produced the lowest mean runtime at `n = 5000` for all four tested input distributions.

Merge Sort generally produced the second-lowest runtime, while Heapsort required more time in this Python implementation.

This does not contradict the theoretical complexity analysis. All three algorithms have `O(n log n)` expected or guaranteed behavior under the implementations used here, but asymptotic notation does not account for constant factors, memory-access behavior, interpreter overhead, or the number and type of operations performed internally.

### Heapsort

Heapsort remained comparatively consistent across the different input arrangements.

At `n = 5000`, its mean runtime ranged from approximately:

```text
6.76 ms to 7.60 ms
```

The input order did not cause a major asymptotic performance change.

This behavior is consistent with Heapsort's:

```text
O(n log n)
```

best-, average-, and worst-case time complexity.

### Randomized Quicksort

Randomized Quicksort was the fastest algorithm for all four tested distributions at `n = 5000`.

Its mean runtime ranged from approximately:

```text
4.00 ms to 4.96 ms
```

The sorted and reverse-sorted datasets did not produce the severe degradation often associated with poorly chosen deterministic Quicksort pivots.

This is because the implementation selects pivots randomly rather than always selecting a fixed array position.

### Merge Sort

Merge Sort also showed relatively stable performance across the different input distributions.

Its `n = 5000` results ranged from approximately:

```text
4.70 ms to 5.68 ms
```

Its predictable divide-and-conquer structure provides `O(n log n)` running time regardless of initial input ordering.

However, this implementation uses additional auxiliary storage for merging.

### Measurement Variation

Some benchmark configurations produced larger standard deviations than others.

This is expected when measuring very short execution times because individual runs can be affected by factors such as:

- operating-system scheduling;
- Python interpreter activity;
- background applications;
- processor scheduling and caching effects.

Using five trials and reporting both the mean and sample standard deviation provides more useful information than relying on a single timing measurement.

---

# Performance Graphs

Four graphs were generated from the benchmark results:

```text
results/random_comparison.png
results/sorted_comparison.png
results/reverse_sorted_comparison.png
results/repeated_comparison.png
```

Each graph displays:

- input size on the x-axis;
- mean runtime in milliseconds on the y-axis;
- one line for each sorting algorithm;
- error bars representing sample standard deviation.

The graphs provide a visual comparison of algorithm scalability and performance variability.

---

# Part III: Priority Queue Implementation

## Data Structure Choice

The priority queue is implemented using a binary max heap stored in a Python list.

A list is well suited to binary heaps because parent and child locations can be calculated directly from array indices without storing explicit node references.

For a node at index `i`:

```text
Parent      = (i - 1) // 2
Left child  = 2i + 1
Right child = 2i + 2
```

A max heap was selected because the scheduling policy treats higher numerical priority values as more important.

Therefore, the highest-priority task is kept at the root of the heap.

---

# Task Representation

Each task is represented by a `Task` dataclass containing:

```text
task_id
priority
arrival_time
execution_time
deadline
```

The implementation validates task information when a task is created.

Examples of invalid values that are rejected include:

- empty task IDs;
- negative arrival times;
- non-positive execution times;
- deadlines earlier than arrival times;
- invalid data types.

---

# Priority Ordering

Tasks are primarily ordered according to numerical priority.

A larger priority value represents greater scheduling priority.

When two tasks have equal priority:

1. the task with the earlier arrival time is preferred;
2. if arrival times also match, task ID is used as a deterministic final tie-break.

This ensures that the priority queue produces repeatable behavior.

---

# Position Map

In addition to the heap list, the priority queue maintains a dictionary that maps:

```text
task_id -> heap index
```

This allows the implementation to locate a task directly when its priority changes.

Without this map, changing the priority of a known task could require scanning the heap, which would require `O(n)` time before the heap-adjustment operation even begins.

The position map allows the task to be found in expected `O(1)` dictionary lookup time, after which heap restoration requires at most `O(log n)` time.

The position map requires:

```text
O(n)
```

additional storage.

---

# Priority Queue Operations

## `insert(task)`

A new task is appended to the end of the heap and moved upward until the max-heap property is restored.

Time complexity:

```text
O(log n)
```

---

## `extract_max()`

The task at the heap root is removed.

The final task in the heap is moved to the root and then moved downward until the heap property is restored.

Time complexity:

```text
O(log n)
```

---

## `increase_key(task_id, new_priority)`

The position map is used to locate the task.

After its priority is increased, the task may move upward in the heap.

Time complexity:

```text
O(log n)
```

---

## `decrease_key(task_id, new_priority)`

The position map is used to locate the task.

After its priority is decreased, the task may move downward in the heap.

Time complexity:

```text
O(log n)
```

---

## `peek_max()`

Returns the task stored at the root without removing it.

Time complexity:

```text
O(1)
```

---

## `is_empty()`

Checks whether the heap contains any tasks.

Time complexity:

```text
O(1)
```

---

## Priority Queue Complexity Summary

| Operation | Time Complexity |
|---|---:|
| Insert | `O(log n)` |
| Extract Maximum | `O(log n)` |
| Increase Priority | `O(log n)` |
| Decrease Priority | `O(log n)` |
| Peek Maximum | `O(1)` |
| Check Empty | `O(1)` |

The heap itself requires `O(n)` storage, and the task-position dictionary also requires `O(n)` storage.

Therefore, the total asymptotic storage requirement remains:

```text
O(n)
```

---

# Part IV: Scheduler Simulation

## Scheduling Policy

The project applies the max-priority queue to a non-preemptive priority scheduler.

Only tasks whose arrival times are less than or equal to the current simulation time are eligible to enter the ready queue.

The highest-priority available task is selected from the max heap.

Once a task begins execution, it continues until completion.

A higher-priority task that arrives while another task is already running does not interrupt the running task.

---

## Scheduling Metrics

For every completed task, the simulation records:

- Task ID
- Priority
- Arrival time
- Execution time
- Deadline
- Start time
- Completion time
- Waiting time
- Turnaround time
- Tardiness
- Deadline status

Waiting time is calculated as:

```text
Waiting Time = Start Time - Arrival Time
```

Turnaround time is calculated as:

```text
Turnaround Time = Completion Time - Arrival Time
```

Tardiness is calculated as:

```text
max(0, Completion Time - Deadline)
```

A deadline is considered met when:

```text
Completion Time <= Deadline
```

---

# Sample Scheduling Results

The sample scheduling workload produced the following execution order:

```text
T1 -> T2 -> T5 -> T4 -> T3 -> T6
```

The detailed execution was:

| Task | Priority | Arrival | Execution | Start | Completion | Waiting | Turnaround | Deadline | Met |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| T1 | 3 | 0 | 4 | 0 | 4 | 0 | 4 | 8 | Yes |
| T2 | 5 | 1 | 3 | 4 | 7 | 3 | 6 | 9 | Yes |
| T5 | 5 | 6 | 2 | 7 | 9 | 1 | 3 | 13 | Yes |
| T4 | 4 | 3 | 5 | 9 | 14 | 6 | 11 | 16 | Yes |
| T3 | 2 | 2 | 2 | 14 | 16 | 12 | 14 | 14 | No |
| T6 | 4 | 20 | 3 | 20 | 23 | 0 | 3 | 25 | Yes |

The scheduling results are stored in:

```text
results/scheduling_results.csv
```

---

# Scheduler Analysis

The scheduler processed six tasks.

The measured summary was:

```text
Tasks scheduled:             6
Average waiting time:        3.67 time units
Average turnaround time:     6.83 time units
Deadlines met:               5 of 6
Deadline success rate:       83.33%
Processor idle time:         4 time units
```

T1 begins first even though T2 has a higher numerical priority.

At time `0`, T1 is the only available task. T2 does not arrive until time `1`.

Because the scheduler is non-preemptive, T1 continues running until time `4`, after which the highest-priority waiting task is selected.

T5 later executes before T4 because T5 has a higher priority and is available when the previous task completes.

T3 experiences the longest waiting time and misses its deadline because several higher-priority tasks are selected before it.

The processor becomes idle between the completion of T3 at time `16` and the arrival of T6 at time `20`, producing four units of processor idle time.

This example demonstrates that priority scheduling can favor high-priority work while increasing waiting time for lower-priority tasks.

---

# Testing and Validation

The project includes automated unit tests covering the sorting algorithms, heap behavior, priority queue, and scheduler.

The complete test suite contains:

```text
43 automated tests
```

All 43 tests passed successfully.

---

## Sorting Tests

The sorting tests include:

- empty input;
- single-element input;
- two-element input;
- already sorted input;
- reverse-sorted input;
- repeated values;
- all-equal values;
- negative values;
- mixed positive and negative values;
- large randomized input;
- in-place sorting verification;
- max-heap property validation;
- Randomized Quicksort correctness;
- Merge Sort correctness;
- large comparison-algorithm inputs.

---

## Priority Queue Tests

Priority queue tests include:

- empty queue behavior;
- insertion;
- maximum-priority access;
- extraction order;
- priority increases;
- priority decreases;
- equal-priority tie handling;
- duplicate task IDs;
- extraction from an empty queue;
- invalid priority-change direction;
- invalid task attributes;
- negative priorities;
- unknown task IDs;
- large queues containing 500 tasks.

---

## Scheduler Tests

Scheduler tests include:

- empty schedules;
- highest-priority task selection;
- task arrival-time handling;
- non-preemptive execution;
- processor idle periods;
- equal-priority tie handling;
- deterministic task-ID tie breaking;
- waiting-time calculations;
- turnaround-time calculations;
- missed deadlines and tardiness;
- duplicate task-ID rejection;
- expected execution order for the sample workload.

---

## Run All Tests

Run:

```bash
python -m unittest -v
```

The verified final result is:

```text
Ran 43 tests
OK
```

---

# How to Run the Project

## Requirements

Python 3.x is required.

The project uses Matplotlib for graph generation.

Install dependencies with:

```bash
python -m pip install -r requirements.txt
```

---

## Run Heapsort

```bash
python heapsort.py
```

---

## Run Randomized Quicksort and Merge Sort

```bash
python comparison_sorts.py
```

---

## Run the Sorting Benchmark

```bash
python benchmark_sorts.py
```

This creates or updates:

```text
results/sorting_results.csv
```

The benchmark performs 300 timed executions across the defined algorithms, sizes, and input distributions.

---

## Generate Performance Graphs

```bash
python generate_graphs.py
```

This creates:

```text
results/random_comparison.png
results/sorted_comparison.png
results/reverse_sorted_comparison.png
results/repeated_comparison.png
```

---

## Run the Priority Queue Demonstration

```bash
python priority_queue.py
```

---

## Run the Scheduler Simulation

```bash
python scheduler_simulation.py
```

This creates:

```text
results/scheduling_results.csv
```

---

## Run Only the Sorting Tests

```bash
python -m unittest test_heapsort.py -v
```

---

## Run Only the Priority Queue Tests

```bash
python -m unittest test_priority_queue.py -v
```

---

## Run Only the Scheduler Tests

```bash
python -m unittest test_scheduler.py -v
```

---

## Run the Complete Test Suite

```bash
python -m unittest -v
```

Expected verified result:

```text
Ran 43 tests
OK
```

---

# Key Findings

The project produced several important observations.

First, Heapsort maintained predictable performance across random, sorted, reverse-sorted, and repeated-element inputs. This is consistent with its `O(n log n)` best-, average-, and worst-case complexity.

Second, Randomized Quicksort produced the lowest measured mean runtime at `n = 5000` for all four tested distributions. Random pivot selection helped it avoid the ordered-input degradation associated with poor deterministic pivot choices.

Third, Merge Sort also showed predictable performance across different input arrangements but required an additional auxiliary list for merging.

Fourth, the binary max heap provided efficient priority queue operations. Insertions, extractions, and priority modifications require at most `O(log n)` heap adjustment, while accessing the maximum task and checking whether the queue is empty require `O(1)` time.

Finally, the scheduling simulation demonstrated how priority, task arrival time, execution duration, and deadlines interact in a realistic non-preemptive scheduler. Higher-priority tasks were favored when multiple tasks were available, while a lower-priority task experienced a longer wait and missed its deadline.

---

# Conclusion

This assignment demonstrates how binary heaps support both sorting and priority-based applications.

Heapsort provides predictable `O(n log n)` running time in the best, average, and worst cases while requiring only `O(1)` auxiliary sorting space in this iterative implementation.

The empirical comparison showed that Randomized Quicksort and Merge Sort were faster than Heapsort for the tested Python workloads, although all three algorithms scaled consistently with their expected asymptotic behavior.

The max-heap priority queue demonstrated efficient insertion, extraction, and priority-modification operations. The addition of a task-position map allowed priority changes to locate tasks directly rather than scanning the heap.

The scheduler simulation extended the heap implementation into a practical application by modeling task arrivals, execution times, priorities, deadlines, waiting times, turnaround times, deadline misses, and processor idle periods.

Together, the implementations, empirical measurements, automated tests, and scheduler simulation demonstrate both the theoretical properties and practical applications of heap data structures.