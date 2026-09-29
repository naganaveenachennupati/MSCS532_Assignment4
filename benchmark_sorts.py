"""
Empirical sorting benchmark for MSCS 532 Assignment 4.

The benchmark compares Heapsort, Randomized Quicksort, and Merge Sort
across multiple input sizes and input distributions. Each configuration
is executed five times, and the mean and sample standard deviation are
saved to a CSV file.
"""

import csv
import random
import statistics
import time
from pathlib import Path

from comparison_sorts import merge_sort, randomized_quicksort
from heapsort import heapsort


SIZES = [100, 500, 1000, 2000, 5000]
TRIALS = 5

DATASET_SEED = 532
QUICKSORT_SEED = 1532

DISTRIBUTIONS = [
    "Random",
    "Sorted",
    "Reverse Sorted",
    "Repeated",
]

ALGORITHMS = [
    "Heapsort",
    "Randomized Quicksort",
    "Merge Sort",
]

RESULTS_PATH = Path("results") / "sorting_results.csv"


def create_datasets(size: int, trial: int) -> dict[str, list[int]]:
    """
    Create reproducible datasets for one size and trial.

    Random, sorted, and reverse-sorted datasets use the same distinct
    values so that only their ordering changes. The repeated-value
    dataset is generated separately with a small value range.
    """
    rng = random.Random(DATASET_SEED + size * 100 + trial)

    random_values = rng.sample(
        range(-size * 10, size * 10 + 1),
        size,
    )

    repeated_values = [
        rng.randint(-10, 10)
        for _ in range(size)
    ]

    return {
        "Random": random_values,
        "Sorted": sorted(random_values),
        "Reverse Sorted": sorted(
            random_values,
            reverse=True,
        ),
        "Repeated": repeated_values,
    }


def time_algorithm(
    algorithm_name: str,
    source_values: list[int],
    quicksort_seed: int,
) -> float:
    """
    Time one sorting algorithm and verify that its output is correct.

    Dataset copying and construction of the expected result occur
    outside the measured interval.
    """
    values = source_values.copy()
    expected = sorted(source_values)

    if algorithm_name == "Randomized Quicksort":
        rng = random.Random(quicksort_seed)

        start_time = time.perf_counter_ns()
        randomized_quicksort(values, rng)
        end_time = time.perf_counter_ns()

    elif algorithm_name == "Heapsort":
        start_time = time.perf_counter_ns()
        heapsort(values)
        end_time = time.perf_counter_ns()

    elif algorithm_name == "Merge Sort":
        start_time = time.perf_counter_ns()
        merge_sort(values)
        end_time = time.perf_counter_ns()

    else:
        raise ValueError(
            f"Unknown algorithm: {algorithm_name}"
        )

    if values != expected:
        raise AssertionError(
            f"{algorithm_name} produced an incorrect result."
        )

    elapsed_ms = (end_time - start_time) / 1_000_000
    return elapsed_ms


def run_benchmark() -> list[dict[str, object]]:
    """
    Execute all benchmark configurations and return aggregated results.
    """
    rows = []

    for distribution in DISTRIBUTIONS:
        for size in SIZES:
            timings = {
                algorithm: []
                for algorithm in ALGORITHMS
            }

            for trial in range(TRIALS):
                datasets = create_datasets(size, trial)
                source_values = datasets[distribution]

                for algorithm_index, algorithm in enumerate(
                    ALGORITHMS
                ):
                    quicksort_seed = (
                        QUICKSORT_SEED
                        + size * 100
                        + trial * 10
                        + algorithm_index
                    )

                    elapsed_ms = time_algorithm(
                        algorithm,
                        source_values,
                        quicksort_seed,
                    )

                    timings[algorithm].append(elapsed_ms)

            for algorithm in ALGORITHMS:
                trial_times = timings[algorithm]

                mean_ms = statistics.mean(trial_times)
                stddev_ms = statistics.stdev(trial_times)

                row = {
                    "distribution": distribution,
                    "size": size,
                    "algorithm": algorithm,
                    "trial_1_ms": trial_times[0],
                    "trial_2_ms": trial_times[1],
                    "trial_3_ms": trial_times[2],
                    "trial_4_ms": trial_times[3],
                    "trial_5_ms": trial_times[4],
                    "mean_ms": mean_ms,
                    "stddev_ms": stddev_ms,
                }

                rows.append(row)

                print(
                    f"{distribution:<15} "
                    f"n={size:<5} "
                    f"{algorithm:<21} "
                    f"mean={mean_ms:>9.4f} ms "
                    f"sd={stddev_ms:>8.4f} ms"
                )

    return rows


def save_results(rows: list[dict[str, object]]) -> None:
    """Write benchmark results to the results directory."""
    RESULTS_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    fieldnames = [
        "distribution",
        "size",
        "algorithm",
        "trial_1_ms",
        "trial_2_ms",
        "trial_3_ms",
        "trial_4_ms",
        "trial_5_ms",
        "mean_ms",
        "stddev_ms",
    ]

    with RESULTS_PATH.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    """Run the benchmark and save its results."""
    print(
        "Sorting benchmark: "
        "Heapsort vs. Randomized Quicksort vs. Merge Sort"
    )
    print(
        f"Sizes: {SIZES} | Trials per configuration: {TRIALS}"
    )
    print("-" * 90)

    rows = run_benchmark()
    save_results(rows)

    print("-" * 90)
    print(
        f"Benchmark complete. Results saved to: "
        f"{RESULTS_PATH}"
    )


if __name__ == "__main__":
    main()