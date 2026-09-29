"""
Task-based max-priority queue for MSCS 532 Assignment 4.

The priority queue uses a binary max-heap stored in a Python list.
Tasks with higher numerical priority values are processed first.
An index map provides direct access to a task's heap position when
its priority must be changed.
"""

from dataclasses import dataclass


@dataclass
class Task:
    """Represent a task handled by the priority scheduler."""

    task_id: str
    priority: int
    arrival_time: int
    execution_time: int
    deadline: int

    def __post_init__(self) -> None:
        """Validate task attributes."""
        if not isinstance(self.task_id, str) or not self.task_id.strip():
            raise ValueError("task_id must be a non-empty string")

        if not isinstance(self.priority, int):
            raise TypeError("priority must be an integer")

        if not isinstance(self.arrival_time, int):
            raise TypeError("arrival_time must be an integer")

        if not isinstance(self.execution_time, int):
            raise TypeError("execution_time must be an integer")

        if not isinstance(self.deadline, int):
            raise TypeError("deadline must be an integer")

        if self.arrival_time < 0:
            raise ValueError("arrival_time cannot be negative")

        if self.execution_time <= 0:
            raise ValueError("execution_time must be positive")

        if self.deadline < self.arrival_time:
            raise ValueError(
                "deadline cannot be earlier than arrival_time"
            )


class MaxPriorityQueue:
    """
    Binary max-heap priority queue for Task objects.

    Higher numerical priority values are served first. When priorities
    are equal, the task with the earlier arrival time is preferred.
    Task ID provides a deterministic final tie-break.
    """

    def __init__(self) -> None:
        """Create an empty priority queue."""
        self.heap: list[Task] = []
        self._positions: dict[str, int] = {}

    def __len__(self) -> int:
        """Return the number of tasks in the queue."""
        return len(self.heap)

    def is_empty(self) -> bool:
        """Return True when no tasks are waiting."""
        return len(self.heap) == 0

    def peek_max(self) -> Task:
        """Return the highest-priority task without removing it."""
        if self.is_empty():
            raise IndexError("Priority queue is empty")

        return self.heap[0]

    def insert(self, task: Task) -> None:
        """
        Insert a task while preserving the max-heap property.

        Time complexity: O(log n).
        """
        if not isinstance(task, Task):
            raise TypeError("Only Task objects can be inserted")

        if task.task_id in self._positions:
            raise ValueError(
                f"Task ID already exists: {task.task_id}"
            )

        self.heap.append(task)
        index = len(self.heap) - 1
        self._positions[task.task_id] = index

        self._sift_up(index)

    def extract_max(self) -> Task:
        """
        Remove and return the highest-priority task.

        Time complexity: O(log n).
        """
        if self.is_empty():
            raise IndexError("Priority queue is empty")

        highest_priority_task = self.heap[0]
        last_task = self.heap.pop()

        del self._positions[highest_priority_task.task_id]

        if self.heap:
            self.heap[0] = last_task
            self._positions[last_task.task_id] = 0
            self._sift_down(0)

        return highest_priority_task

    def increase_key(
        self,
        task_id: str,
        new_priority: int,
    ) -> None:
        """
        Increase an existing task's priority.

        Time complexity: O(log n).
        """
        index = self._get_task_index(task_id)
        task = self.heap[index]

        if new_priority < task.priority:
            raise ValueError(
                "New priority must be greater than or equal "
                "to the current priority"
            )

        task.priority = new_priority
        self._sift_up(index)

    def decrease_key(
        self,
        task_id: str,
        new_priority: int,
    ) -> None:
        """
        Decrease an existing task's priority.

        Time complexity: O(log n).
        """
        index = self._get_task_index(task_id)
        task = self.heap[index]

        if new_priority > task.priority:
            raise ValueError(
                "New priority must be less than or equal "
                "to the current priority"
            )

        task.priority = new_priority
        self._sift_down(index)

    def _get_task_index(self, task_id: str) -> int:
        """Return a task's heap index using the position map."""
        if task_id not in self._positions:
            raise KeyError(f"Unknown task ID: {task_id}")

        return self._positions[task_id]

    def _higher_priority(
        self,
        first: Task,
        second: Task,
    ) -> bool:
        """Return True when first should appear above second."""
        if first.priority != second.priority:
            return first.priority > second.priority

        if first.arrival_time != second.arrival_time:
            return first.arrival_time < second.arrival_time

        return first.task_id < second.task_id

    def _swap(self, first_index: int, second_index: int) -> None:
        """Swap two heap entries and update their recorded positions."""
        self.heap[first_index], self.heap[second_index] = (
            self.heap[second_index],
            self.heap[first_index],
        )

        self._positions[self.heap[first_index].task_id] = first_index
        self._positions[self.heap[second_index].task_id] = second_index

    def _sift_up(self, index: int) -> None:
        """Move a task upward until the max-heap property holds."""
        while index > 0:
            parent_index = (index - 1) // 2

            if not self._higher_priority(
                self.heap[index],
                self.heap[parent_index],
            ):
                break

            self._swap(index, parent_index)
            index = parent_index

    def _sift_down(self, index: int) -> None:
        """Move a task downward until the max-heap property holds."""
        size = len(self.heap)

        while True:
            left_index = 2 * index + 1
            right_index = 2 * index + 2
            largest = index

            if (
                left_index < size
                and self._higher_priority(
                    self.heap[left_index],
                    self.heap[largest],
                )
            ):
                largest = left_index

            if (
                right_index < size
                and self._higher_priority(
                    self.heap[right_index],
                    self.heap[largest],
                )
            ):
                largest = right_index

            if largest == index:
                return

            self._swap(index, largest)
            index = largest


if __name__ == "__main__":
    queue = MaxPriorityQueue()

    tasks = [
        Task("T1", 3, 0, 4, 12),
        Task("T2", 5, 1, 3, 10),
        Task("T3", 2, 2, 2, 15),
        Task("T4", 4, 3, 5, 18),
    ]

    for task in tasks:
        queue.insert(task)

    print("Highest-priority task:", queue.peek_max())

    queue.increase_key("T3", 6)
    print("After increasing T3:", queue.peek_max())

    queue.decrease_key("T3", 1)
    print("After decreasing T3:", queue.peek_max())

    print("\nExtraction order:")
    while not queue.is_empty():
        print(queue.extract_max())