"""
Heapsort implementation for MSCS 532 Assignment 4.

The algorithm uses an array-based max heap and sorts the input list
in ascending order in place.
"""


def max_heapify(values: list[int], heap_size: int, root_index: int) -> None:
    """
    Restore the max-heap property for the subtree rooted at root_index.

    The implementation is iterative, which avoids recursive call-stack
    overhead while moving the current value downward through the heap.

    Args:
        values: List containing the heap.
        heap_size: Number of elements currently considered part of the heap.
        root_index: Index of the subtree root.
    """
    while True:
        largest = root_index
        left_child = 2 * root_index + 1
        right_child = 2 * root_index + 2

        if (
            left_child < heap_size
            and values[left_child] > values[largest]
        ):
            largest = left_child

        if (
            right_child < heap_size
            and values[right_child] > values[largest]
        ):
            largest = right_child

        if largest == root_index:
            return

        values[root_index], values[largest] = (
            values[largest],
            values[root_index],
        )

        root_index = largest


def build_max_heap(values: list[int]) -> None:
    """
    Convert the input list into a max heap in place.

    Leaf nodes already satisfy the heap property, so heap construction
    begins with the last non-leaf node and proceeds toward the root.
    """
    heap_size = len(values)

    for index in range(heap_size // 2 - 1, -1, -1):
        max_heapify(values, heap_size, index)


def heapsort(values: list[int]) -> list[int]:
    """
    Sort the input list in ascending order using Heapsort.

    The function modifies the original list and also returns it.

    Args:
        values: List of integers to sort.

    Returns:
        The same list sorted in ascending order.
    """
    build_max_heap(values)

    for end_index in range(len(values) - 1, 0, -1):
        values[0], values[end_index] = (
            values[end_index],
            values[0],
        )

        max_heapify(values, end_index, 0)

    return values


if __name__ == "__main__":
    sample_values = [12, 11, 13, 5, 6, 7]

    print("Original:", sample_values)
    heapsort(sample_values)
    print("Sorted:  ", sample_values)