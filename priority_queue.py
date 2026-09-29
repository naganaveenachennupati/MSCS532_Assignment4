"""
Priority Queue implementation using a max-heap.

This module provides a max-priority queue with the following operations:
- insert
- maximum
- extract_max
- increase_key
- is_empty
"""

from __future__ import annotations


class MaxPriorityQueue:
    """A max-priority queue implemented with a binary max-heap."""

    def __init__(self) -> None:
        """Create an empty priority queue."""
        self.heap: list[int] = []

    def __len__(self) -> int:
        """Return the number of elements in the queue."""
        return len(self.heap)

    def is_empty(self) -> bool:
        """Return True if the queue is empty, otherwise False."""
        return len(self.heap) == 0

    def parent(self, index: int) -> int:
        """Return the parent index of a node."""
        return (index - 1) // 2

    def left(self, index: int) -> int:
        """Return the left child index."""
        return 2 * index + 1

    def right(self, index: int) -> int:
        """Return the right child index."""
        return 2 * index + 2

    def maximum(self) -> int:
        """Return the maximum element without removing it."""
        if self.is_empty():
            raise IndexError("Priority queue is empty")
        return self.heap[0]

    def insert(self, key: int) -> None:
        """Insert a new key into the priority queue."""
        if not isinstance(key, int):
            raise TypeError("Priority queue only supports integer keys")

        self.heap.append(float("-inf"))
        self.increase_key(len(self.heap) - 1, key)

    def increase_key(self, index: int, new_key: int) -> None:
        """Increase the value of the key at the given index."""
        if not isinstance(new_key, int):
            raise TypeError("Priority queue only supports integer keys")

        if index < 0 or index >= len(self.heap):
            raise IndexError("Index out of range")

        if new_key < self.heap[index]:
            raise ValueError(
                "New key must be greater than or equal to the current key"
            )

        self.heap[index] = new_key

        while index > 0 and self.heap[self.parent(index)] < self.heap[index]:
            parent_index = self.parent(index)
            self.heap[index], self.heap[parent_index] = (
                self.heap[parent_index],
                self.heap[index],
            )
            index = parent_index

    def extract_max(self) -> int:
        """Remove and return the maximum element."""
        if self.is_empty():
            raise IndexError("Priority queue is empty")

        maximum_value = self.heap[0]
        last_value = self.heap.pop()

        if not self.is_empty():
            self.heap[0] = last_value
            self.max_heapify(0)

        return maximum_value

    def max_heapify(self, index: int) -> None:
        """Restore the max-heap property from a given index downward."""
        size = len(self.heap)

        while True:
            left_index = self.left(index)
            right_index = self.right(index)
            largest = index

            if (
                left_index < size
                and self.heap[left_index] > self.heap[largest]
            ):
                largest = left_index

            if (
                right_index < size
                and self.heap[right_index] > self.heap[largest]
            ):
                largest = right_index

            if largest == index:
                break

            self.heap[index], self.heap[largest] = (
                self.heap[largest],
                self.heap[index],
            )
            index = largest


if __name__ == "__main__":
    pq = MaxPriorityQueue()

    for value in [15, 6, 20, 3, 17]:
        pq.insert(value)

    print("Initial heap:", pq.heap)
    print("Maximum:", pq.maximum())
    print("Extract max:", pq.extract_max())
    print("Heap after extraction:", pq.heap)

    pq.increase_key(2, 25)
    print("Heap after increase_key:", pq.heap)