import unittest

from priority_queue import MaxPriorityQueue, Task


class TestMaxPriorityQueue(unittest.TestCase):
    """Tests for the task-based max-priority queue."""

    def create_task(
        self,
        task_id: str,
        priority: int,
        arrival_time: int = 0,
        execution_time: int = 1,
        deadline: int = 10,
    ) -> Task:
        return Task(
            task_id,
            priority,
            arrival_time,
            execution_time,
            deadline,
        )

    def test_empty_queue(self):
        queue = MaxPriorityQueue()

        self.assertTrue(queue.is_empty())
        self.assertEqual(len(queue), 0)

    def test_insert_and_peek_max(self):
        queue = MaxPriorityQueue()

        queue.insert(self.create_task("T1", 3))
        queue.insert(self.create_task("T2", 8))
        queue.insert(self.create_task("T3", 5))

        self.assertEqual(queue.peek_max().task_id, "T2")
        self.assertEqual(len(queue), 3)

    def test_extract_max_order(self):
        queue = MaxPriorityQueue()

        queue.insert(self.create_task("T1", 3))
        queue.insert(self.create_task("T2", 8))
        queue.insert(self.create_task("T3", 5))
        queue.insert(self.create_task("T4", 1))

        extracted = [
            queue.extract_max().task_id
            for _ in range(4)
        ]

        self.assertEqual(
            extracted,
            ["T2", "T3", "T1", "T4"],
        )

    def test_increase_key(self):
        queue = MaxPriorityQueue()

        queue.insert(self.create_task("T1", 4))
        queue.insert(self.create_task("T2", 6))
        queue.insert(self.create_task("T3", 2))

        queue.increase_key("T3", 10)

        self.assertEqual(queue.peek_max().task_id, "T3")
        self.assertEqual(queue.peek_max().priority, 10)

    def test_decrease_key(self):
        queue = MaxPriorityQueue()

        queue.insert(self.create_task("T1", 10))
        queue.insert(self.create_task("T2", 7))
        queue.insert(self.create_task("T3", 5))

        queue.decrease_key("T1", 1)

        self.assertEqual(queue.peek_max().task_id, "T2")

    def test_equal_priority_uses_arrival_time(self):
        queue = MaxPriorityQueue()

        queue.insert(
            self.create_task(
                "Later",
                5,
                arrival_time=4,
                deadline=15,
            )
        )
        queue.insert(
            self.create_task(
                "Earlier",
                5,
                arrival_time=1,
                deadline=15,
            )
        )

        self.assertEqual(
            queue.extract_max().task_id,
            "Earlier",
        )

    def test_duplicate_task_id(self):
        queue = MaxPriorityQueue()

        queue.insert(self.create_task("T1", 5))

        with self.assertRaises(ValueError):
            queue.insert(self.create_task("T1", 9))

    def test_extract_from_empty_queue(self):
        queue = MaxPriorityQueue()

        with self.assertRaises(IndexError):
            queue.extract_max()

    def test_peek_from_empty_queue(self):
        queue = MaxPriorityQueue()

        with self.assertRaises(IndexError):
            queue.peek_max()

    def test_unknown_task_increase(self):
        queue = MaxPriorityQueue()

        with self.assertRaises(KeyError):
            queue.increase_key("Missing", 10)

    def test_unknown_task_decrease(self):
        queue = MaxPriorityQueue()

        with self.assertRaises(KeyError):
            queue.decrease_key("Missing", 1)

    def test_invalid_increase_direction(self):
        queue = MaxPriorityQueue()
        queue.insert(self.create_task("T1", 8))

        with self.assertRaises(ValueError):
            queue.increase_key("T1", 4)

    def test_invalid_decrease_direction(self):
        queue = MaxPriorityQueue()
        queue.insert(self.create_task("T1", 4))

        with self.assertRaises(ValueError):
            queue.decrease_key("T1", 8)

    def test_negative_priorities(self):
        queue = MaxPriorityQueue()

        queue.insert(self.create_task("T1", -10))
        queue.insert(self.create_task("T2", -2))
        queue.insert(self.create_task("T3", -7))

        self.assertEqual(
            queue.extract_max().task_id,
            "T2",
        )

    def test_invalid_task_values(self):
        with self.assertRaises(ValueError):
            Task("", 5, 0, 2, 10)

        with self.assertRaises(ValueError):
            Task("T1", 5, -1, 2, 10)

        with self.assertRaises(ValueError):
            Task("T1", 5, 0, 0, 10)

        with self.assertRaises(ValueError):
            Task("T1", 5, 5, 2, 4)

    def test_large_queue(self):
        queue = MaxPriorityQueue()

        for number in range(500):
            queue.insert(
                Task(
                    task_id=f"T{number}",
                    priority=number,
                    arrival_time=0,
                    execution_time=1,
                    deadline=1000,
                )
            )

        extracted_priorities = []

        while not queue.is_empty():
            extracted_priorities.append(
                queue.extract_max().priority
            )

        self.assertEqual(
            extracted_priorities,
            list(range(499, -1, -1)),
        )


if __name__ == "__main__":
    unittest.main()