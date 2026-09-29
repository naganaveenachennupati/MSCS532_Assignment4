"""
Comparison sorting algorithms for MSCS 532 Assignment 4.

Randomized Quicksort and Merge Sort are used as comparison algorithms
for the empirical evaluation of Heapsort.
"""

import random


def randomized_quicksort(
    values: list[int],
    rng: random.Random | None = None,
) -> list[int]:
    """
    Sort a list in ascending order using randomized Quicksort.

    The algorithm modifies the input list in place and also returns it.
    A random pivot is selected from each active subarray.

    Args:
        values: List of integers to sort.
        rng: Optional random-number generator for reproducible testing.

    Returns:
        The same list sorted in ascending order.
    """
    if rng is None:
        rng = random.Random()

    _randomized_quicksort(values, 0, len(values) - 1, rng)
    return values


def _randomized_quicksort(
    values: list[int],
    low: int,
    high: int,
    rng: random.Random,
) -> None:
    """
    Sort the subarray values[low:high + 1] using randomized Quicksort.

    The smaller partition is processed recursively and the larger one
    iteratively to reduce recursive stack depth.
    """
    while low < high:
        split_index = _randomized_partition(values, low, high, rng)

        left_size = split_index - low + 1
        right_size = high - split_index

        if left_size < right_size:
            _randomized_quicksort(
                values,
                low,
                split_index,
                rng,
            )
            low = split_index + 1
        else:
            _randomized_quicksort(
                values,
                split_index + 1,
                high,
                rng,
            )
            high = split_index


def _randomized_partition(
    values: list[int],
    low: int,
    high: int,
    rng: random.Random,
) -> int:
    """Choose a random pivot and partition using Hoare's method."""
    pivot_index = rng.randint(low, high)

    values[low], values[pivot_index] = (
        values[pivot_index],
        values[low],
    )

    return _hoare_partition(values, low, high)


def _hoare_partition(
    values: list[int],
    low: int,
    high: int,
) -> int:
    """Partition a subarray using Hoare's partitioning scheme."""
    pivot_value = values[low]

    left = low - 1
    right = high + 1

    while True:
        left += 1
        while values[left] < pivot_value:
            left += 1

        right -= 1
        while values[right] > pivot_value:
            right -= 1

        if left >= right:
            return right

        values[left], values[right] = (
            values[right],
            values[left],
        )


def merge_sort(values: list[int]) -> list[int]:
    """
    Sort a list in ascending order using Merge Sort.

    The input list is modified in place and also returned.

    Args:
        values: List of integers to sort.

    Returns:
        The same list sorted in ascending order.
    """
    if len(values) <= 1:
        return values

    auxiliary = values.copy()
    _merge_sort(values, auxiliary, 0, len(values))
    return values


def _merge_sort(
    values: list[int],
    auxiliary: list[int],
    start: int,
    end: int,
) -> None:
    """Recursively sort values[start:end]."""
    if end - start <= 1:
        return

    middle = (start + end) // 2

    _merge_sort(values, auxiliary, start, middle)
    _merge_sort(values, auxiliary, middle, end)

    _merge(values, auxiliary, start, middle, end)


def _merge(
    values: list[int],
    auxiliary: list[int],
    start: int,
    middle: int,
    end: int,
) -> None:
    """Merge two sorted adjacent ranges."""
    auxiliary[start:end] = values[start:end]

    left = start
    right = middle
    destination = start

    while left < middle and right < end:
        if auxiliary[left] <= auxiliary[right]:
            values[destination] = auxiliary[left]
            left += 1
        else:
            values[destination] = auxiliary[right]
            right += 1

        destination += 1

    while left < middle:
        values[destination] = auxiliary[left]
        left += 1
        destination += 1

    while right < end:
        values[destination] = auxiliary[right]
        right += 1
        destination += 1


if __name__ == "__main__":
    sample_values = [12, 11, 13, 5, 6, 7]

    quicksort_values = sample_values.copy()
    mergesort_values = sample_values.copy()

    randomized_quicksort(
        quicksort_values,
        random.Random(532),
    )
    merge_sort(mergesort_values)

    print("Original:             ", sample_values)
    print("Randomized Quicksort: ", quicksort_values)
    print("Merge Sort:           ", mergesort_values)