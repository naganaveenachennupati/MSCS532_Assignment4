"""
Generate performance graphs for the Assignment 4 sorting benchmark.

Each graph compares Heapsort, Randomized Quicksort, and Merge Sort
using the benchmark mean runtime and sample standard deviation.
"""

import csv
from pathlib import Path

import matplotlib.pyplot as plt


RESULTS_PATH = Path("results") / "sorting_results.csv"

OUTPUT_FILES = {
    "Random": "random_comparison.png",
    "Sorted": "sorted_comparison.png",
    "Reverse Sorted": "reverse_sorted_comparison.png",
    "Repeated": "repeated_comparison.png",
}

ALGORITHMS = [
    "Heapsort",
    "Randomized Quicksort",
    "Merge Sort",
]


def load_results() -> list[dict[str, object]]:
    """Load and convert benchmark results from the CSV file."""
    rows = []

    with RESULTS_PATH.open(
        "r",
        newline="",
        encoding="utf-8",
    ) as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            rows.append(
                {
                    "distribution": row["distribution"],
                    "size": int(row["size"]),
                    "algorithm": row["algorithm"],
                    "mean_ms": float(row["mean_ms"]),
                    "stddev_ms": float(row["stddev_ms"]),
                }
            )

    return rows


def create_graph(
    rows: list[dict[str, object]],
    distribution: str,
    output_filename: str,
) -> None:
    """Create one comparison graph for a dataset distribution."""
    plt.figure(figsize=(9, 6))

    for algorithm in ALGORITHMS:
        algorithm_rows = [
            row
            for row in rows
            if (
                row["distribution"] == distribution
                and row["algorithm"] == algorithm
            )
        ]

        algorithm_rows.sort(
            key=lambda row: row["size"]
        )

        sizes = [
            row["size"]
            for row in algorithm_rows
        ]

        means = [
            row["mean_ms"]
            for row in algorithm_rows
        ]

        standard_deviations = [
            row["stddev_ms"]
            for row in algorithm_rows
        ]

        plt.errorbar(
            sizes,
            means,
            yerr=standard_deviations,
            marker="o",
            capsize=4,
            linewidth=1.8,
            label=algorithm,
        )

    plt.title(
        f"Sorting Performance on {distribution} Input"
    )
    plt.xlabel("Input Size (n)")
    plt.ylabel("Mean Runtime (ms)")
    plt.xticks([100, 500, 1000, 2000, 5000])
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()

    output_path = Path("results") / output_filename

    plt.savefig(
        output_path,
        dpi=200,
        bbox_inches="tight",
    )

    plt.close()

    print(f"Created: {output_path}")


def main() -> None:
    """Generate one graph for each input distribution."""
    rows = load_results()

    for distribution, filename in OUTPUT_FILES.items():
        create_graph(
            rows,
            distribution,
            filename,
        )

    print("All performance graphs generated successfully.")


if __name__ == "__main__":
    main()