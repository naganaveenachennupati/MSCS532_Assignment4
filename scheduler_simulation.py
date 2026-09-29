"""
Non-preemptive priority scheduler simulation for MSCS 532 Assignment 4.

Tasks enter a max-priority queue according to their arrival times.
Among the tasks currently available, the task with the highest
numerical priority is executed next. Once execution begins, a task
runs to completion before another task is selected.
"""

import csv
from dataclasses import dataclass
from pathlib import Path

from priority_queue import MaxPriorityQueue, Task


RESULTS_PATH = Path("results") / "scheduling_results.csv"


@dataclass
class ScheduleResult:
    """Store the scheduling outcome for one completed task."""

    task_id: str
    priority: int
    arrival_time: int
    execution_time: int
    deadline: int
    start_time: int
    completion_time: int
    waiting_time: int
    turnaround_time: int
    tardiness: int
    deadline_met: bool


def schedule_tasks(tasks: list[Task]) -> list[ScheduleResult]:
    """
    Schedule tasks using non-preemptive max-priority scheduling.

    Only tasks whose arrival times are less than or equal to the
    current time are eligible for execution.

    Args:
        tasks: Tasks to schedule.

    Returns:
        Scheduling results in execution order.

    Raises:
        ValueError: If duplicate task IDs are supplied.
    """
    if not tasks:
        return []

    task_ids = [task.task_id for task in tasks]

    if len(task_ids) != len(set(task_ids)):
        raise ValueError("Task IDs must be unique")

    pending_tasks = sorted(
        tasks,
        key=lambda task: (
            task.arrival_time,
            task.task_id,
        ),
    )

    ready_queue = MaxPriorityQueue()
    results: list[ScheduleResult] = []

    current_time = 0
    next_task_index = 0

    while (
        next_task_index < len(pending_tasks)
        or not ready_queue.is_empty()
    ):
        if (
            ready_queue.is_empty()
            and next_task_index < len(pending_tasks)
            and pending_tasks[next_task_index].arrival_time
            > current_time
        ):
            current_time = (
                pending_tasks[next_task_index].arrival_time
            )

        while (
            next_task_index < len(pending_tasks)
            and pending_tasks[next_task_index].arrival_time
            <= current_time
        ):
            ready_queue.insert(
                pending_tasks[next_task_index]
            )
            next_task_index += 1

        task = ready_queue.extract_max()

        start_time = current_time
        completion_time = (
            start_time + task.execution_time
        )

        waiting_time = (
            start_time - task.arrival_time
        )

        turnaround_time = (
            completion_time - task.arrival_time
        )

        tardiness = max(
            0,
            completion_time - task.deadline,
        )

        deadline_met = (
            completion_time <= task.deadline
        )

        results.append(
            ScheduleResult(
                task_id=task.task_id,
                priority=task.priority,
                arrival_time=task.arrival_time,
                execution_time=task.execution_time,
                deadline=task.deadline,
                start_time=start_time,
                completion_time=completion_time,
                waiting_time=waiting_time,
                turnaround_time=turnaround_time,
                tardiness=tardiness,
                deadline_met=deadline_met,
            )
        )

        current_time = completion_time

    return results


def summarize_schedule(
    results: list[ScheduleResult],
) -> dict[str, float | int]:
    """Calculate summary statistics for a completed schedule."""
    if not results:
        return {
            "task_count": 0,
            "average_waiting_time": 0.0,
            "average_turnaround_time": 0.0,
            "deadlines_met": 0,
            "deadline_success_rate": 0.0,
            "idle_time": 0,
        }

    task_count = len(results)

    total_waiting_time = sum(
        result.waiting_time
        for result in results
    )

    total_turnaround_time = sum(
        result.turnaround_time
        for result in results
    )

    deadlines_met = sum(
        result.deadline_met
        for result in results
    )

    first_arrival = min(
        result.arrival_time
        for result in results
    )

    final_completion = max(
        result.completion_time
        for result in results
    )

    total_execution_time = sum(
        result.execution_time
        for result in results
    )

    schedule_span = (
        final_completion - first_arrival
    )

    idle_time = (
        schedule_span - total_execution_time
    )

    return {
        "task_count": task_count,
        "average_waiting_time": (
            total_waiting_time / task_count
        ),
        "average_turnaround_time": (
            total_turnaround_time / task_count
        ),
        "deadlines_met": deadlines_met,
        "deadline_success_rate": (
            deadlines_met / task_count * 100
        ),
        "idle_time": idle_time,
    }


def save_results(
    results: list[ScheduleResult],
    output_path: Path = RESULTS_PATH,
) -> None:
    """Save detailed scheduling results to a CSV file."""
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    fieldnames = [
        "task_id",
        "priority",
        "arrival_time",
        "execution_time",
        "deadline",
        "start_time",
        "completion_time",
        "waiting_time",
        "turnaround_time",
        "tardiness",
        "deadline_met",
    ]

    with output_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=fieldnames,
        )

        writer.writeheader()

        for result in results:
            writer.writerow(
                {
                    "task_id": result.task_id,
                    "priority": result.priority,
                    "arrival_time": result.arrival_time,
                    "execution_time": result.execution_time,
                    "deadline": result.deadline,
                    "start_time": result.start_time,
                    "completion_time": result.completion_time,
                    "waiting_time": result.waiting_time,
                    "turnaround_time": result.turnaround_time,
                    "tardiness": result.tardiness,
                    "deadline_met": result.deadline_met,
                }
            )


def print_results(
    results: list[ScheduleResult],
) -> None:
    """Print scheduling results in a readable table."""
    print(
        f"{'Task':<6}"
        f"{'Pri':>5}"
        f"{'Arr':>6}"
        f"{'Exec':>6}"
        f"{'Start':>7}"
        f"{'End':>6}"
        f"{'Wait':>7}"
        f"{'Turn':>7}"
        f"{'Deadline':>10}"
        f"{'Met':>6}"
    )

    print("-" * 66)

    for result in results:
        print(
            f"{result.task_id:<6}"
            f"{result.priority:>5}"
            f"{result.arrival_time:>6}"
            f"{result.execution_time:>6}"
            f"{result.start_time:>7}"
            f"{result.completion_time:>6}"
            f"{result.waiting_time:>7}"
            f"{result.turnaround_time:>7}"
            f"{result.deadline:>10}"
            f"{str(result.deadline_met):>6}"
        )


def main() -> None:
    """Run a sample priority-scheduling simulation."""
    tasks = [
        Task("T1", 3, 0, 4, 8),
        Task("T2", 5, 1, 3, 9),
        Task("T3", 2, 2, 2, 14),
        Task("T4", 4, 3, 5, 16),
        Task("T5", 5, 6, 2, 13),
        Task("T6", 4, 20, 3, 25),
    ]

    results = schedule_tasks(tasks)
    summary = summarize_schedule(results)

    print("Non-Preemptive Priority Scheduling Simulation")
    print("=" * 66)

    print_results(results)

    print("\nSummary")
    print("-" * 40)
    print(f"Tasks scheduled: {summary['task_count']}")
    print(
        "Average waiting time: "
        f"{summary['average_waiting_time']:.2f}"
    )
    print(
        "Average turnaround time: "
        f"{summary['average_turnaround_time']:.2f}"
    )
    print(
        "Deadlines met: "
        f"{summary['deadlines_met']}/"
        f"{summary['task_count']}"
    )
    print(
        "Deadline success rate: "
        f"{summary['deadline_success_rate']:.2f}%"
    )
    print(
        f"Processor idle time: "
        f"{summary['idle_time']}"
    )

    save_results(results)

    print(
        f"\nScheduling results saved to: "
        f"{RESULTS_PATH}"
    )


if __name__ == "__main__":
    main()