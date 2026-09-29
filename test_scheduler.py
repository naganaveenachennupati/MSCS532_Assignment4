import unittest

from priority_queue import Task
from scheduler_simulation import (
    schedule_tasks,
    summarize_schedule,
)


class TestScheduler(unittest.TestCase):
    """Tests for the non-preemptive priority scheduler."""

    def test_empty_schedule(self):
        results = schedule_tasks([])

        self.assertEqual(results, [])

    def test_highest_available_priority_runs_first(self):
        tasks = [
            Task("T1", 2, 0, 1, 10),
            Task("T2", 8, 0, 1, 10),
            Task("T3", 5, 0, 1, 10),
        ]

        results = schedule_tasks(tasks)

        self.assertEqual(
            [result.task_id for result in results],
            ["T2", "T3", "T1"],
        )

    def test_task_does_not_start_before_arrival(self):
        tasks = [
            Task("T1", 5, 3, 2, 10),
        ]

        results = schedule_tasks(tasks)

        self.assertEqual(
            results[0].start_time,
            3,
        )

    def test_scheduler_is_non_preemptive(self):
        tasks = [
            Task("Low", 1, 0, 5, 20),
            Task("High", 10, 1, 1, 20),
        ]

        results = schedule_tasks(tasks)

        self.assertEqual(
            [result.task_id for result in results],
            ["Low", "High"],
        )

        self.assertEqual(
            results[0].completion_time,
            5,
        )

        self.assertEqual(
            results[1].start_time,
            5,
        )

    def test_idle_gap_is_handled(self):
        tasks = [
            Task("T1", 5, 0, 2, 10),
            Task("T2", 4, 7, 1, 12),
        ]

        results = schedule_tasks(tasks)

        self.assertEqual(
            results[1].start_time,
            7,
        )

        summary = summarize_schedule(results)

        self.assertEqual(
            summary["idle_time"],
            5,
        )

    def test_equal_priority_uses_arrival_time(self):
        tasks = [
            Task("Later", 5, 2, 1, 10),
            Task("Earlier", 5, 0, 3, 10),
        ]

        results = schedule_tasks(tasks)

        self.assertEqual(
            results[0].task_id,
            "Earlier",
        )

    def test_equal_priority_and_arrival_uses_task_id(self):
        tasks = [
            Task("T2", 5, 0, 1, 10),
            Task("T1", 5, 0, 1, 10),
        ]

        results = schedule_tasks(tasks)

        self.assertEqual(
            [result.task_id for result in results],
            ["T1", "T2"],
        )

    def test_waiting_and_turnaround_times(self):
        tasks = [
            Task("T1", 5, 0, 3, 10),
            Task("T2", 4, 0, 2, 10),
        ]

        results = schedule_tasks(tasks)

        self.assertEqual(
            results[0].waiting_time,
            0,
        )

        self.assertEqual(
            results[0].turnaround_time,
            3,
        )

        self.assertEqual(
            results[1].waiting_time,
            3,
        )

        self.assertEqual(
            results[1].turnaround_time,
            5,
        )

    def test_deadline_miss_and_tardiness(self):
        tasks = [
            Task("T1", 5, 0, 5, 3),
        ]

        results = schedule_tasks(tasks)

        self.assertFalse(
            results[0].deadline_met
        )

        self.assertEqual(
            results[0].tardiness,
            2,
        )

    def test_duplicate_task_ids_rejected(self):
        tasks = [
            Task("T1", 5, 0, 1, 10),
            Task("T1", 3, 2, 1, 10),
        ]

        with self.assertRaises(ValueError):
            schedule_tasks(tasks)

    def test_sample_schedule_order(self):
        tasks = [
            Task("T1", 3, 0, 4, 8),
            Task("T2", 5, 1, 3, 9),
            Task("T3", 2, 2, 2, 14),
            Task("T4", 4, 3, 5, 16),
            Task("T5", 5, 6, 2, 13),
            Task("T6", 4, 20, 3, 25),
        ]

        results = schedule_tasks(tasks)

        self.assertEqual(
            [result.task_id for result in results],
            ["T1", "T2", "T5", "T4", "T3", "T6"],
        )


if __name__ == "__main__":
    unittest.main()