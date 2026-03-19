import heapq
from typing import List, Tuple, Dict, Set, FrozenSet


class TaskGraph:
    """Represents the environment: Tasks, Durations, and Dependencies."""

    def __init__(self, durations: Dict[str, int], dependencies: Dict[str, List[str]]):
        self.durations = durations
        self.dependencies = dependencies
        self.all_tasks = set(durations.keys())

    def get_available_tasks(self, completed_tasks: Set[str]) -> List[str]:
        """Returns tasks whose dependencies are fully met and aren't completed yet."""
        available = []
        for task in self.all_tasks:
            if task not in completed_tasks:
                # Check if ALL dependencies are in the completed set
                deps = self.dependencies.get(task, [])
                if all(d in completed_tasks for d in deps):
                    available.append(task)
        return available

    def calculate_critical_path(self, task: str) -> int:
        """
        Recursively calculates the longest path from this task to the end.
        (This will be used for our A* Heuristic)
        """
        # Find all tasks that depend on THIS task
        successors = [t for t, deps in self.dependencies.items() if task in deps]

        if not successors:
            return self.durations[task]

        max_future_time = max(self.calculate_critical_path(s) for s in successors)
        return self.durations[task] + max_future_time


class SchedulerAI:
    def __init__(self, graph: TaskGraph, num_workers: int = 2):
        self.graph = graph
        self.num_workers = num_workers

    def heuristic(self, remaining_tasks: Set[str]) -> int:
        """
        Admissible Heuristic: The max critical path of any remaining task.
        We cannot finish faster than the longest dependency chain.
        """
        if not remaining_tasks:
            return 0
        return max(self.graph.calculate_critical_path(t) for t in remaining_tasks)

    def greedy_solve(self) -> Tuple[int, List[Tuple[str, int]]]:  # type: ignore
        """
        Greedy Approach:
        Always assign the first available task to the earliest available worker.
        Does NOT look ahead to see if delaying a task is smarter.
        """
        # (This is where you will implement a simple loop that assigns
        # tasks without using a Priority Queue or evaluating future states)
        pass

    def a_star_solve(self) -> Tuple[int, Dict[str, int]]:
        """
        A* Search:
        Explores different task-ordering permutations to find the lowest makespan.
        """

        # State representation for Priority Queue:
        # (f_score, tie_breaker, current_time, scheduled_tasks_tuple, worker_finish_times_tuple, task_finish_times_dict)

        # Start state: Time 0, no tasks scheduled, all workers free at time 0
        start_workers = tuple([0] * self.num_workers)
        start_task_times = {}  # Maps task -> finish_time
        scheduled = frozenset()

        pq = []
        heapq.heappush(pq, (0, 0, 0, scheduled, start_workers, start_task_times))

        # Keep track of the best time we've seen for a specific set of scheduled tasks
        visited: Dict[FrozenSet[str], int] = {scheduled: 0}
        tie_breaker = 0

        while pq:
            f, _, current_time, completed, workers, task_times = heapq.heappop(pq)

            # 1. Goal Check: Are all tasks scheduled?
            if len(completed) == len(self.graph.all_tasks):
                # The total time is whenever the last worker finishes
                total_time = max(workers)
                return total_time, task_times

            # 2. Get available tasks
            available = self.graph.get_available_tasks(set(completed))

            # 3. Expansion: Try scheduling each available task
            for task in available:
                # Find the earliest time this task can actually start
                # It must be AFTER all its dependencies finish
                deps = self.graph.dependencies.get(task, [])
                deps_finish_time = max([task_times[d] for d in deps] + [0])

                # Find the earliest available worker who can take it
                # The worker can start either when they are free, OR when dependencies finish
                earliest_worker_idx = min(
                    range(self.num_workers), key=lambda i: max(workers[i], deps_finish_time)
                )
                start_time = max(workers[earliest_worker_idx], deps_finish_time)

                # Calculate finish time
                finish_time = start_time + self.graph.durations[task]

                # Create the NEW state
                new_completed = frozenset(list(completed) + [task])
                new_workers = list(workers)
                new_workers[earliest_worker_idx] = finish_time
                new_workers = tuple(sorted(new_workers))  # Sort to group equivalent worker states

                new_task_times = task_times.copy()
                new_task_times[task] = finish_time

                # The "Cost" (g) is the maximum time any worker is currently busy
                g = max(new_workers)

                if new_completed not in visited or g < visited[new_completed]:
                    visited[new_completed] = g

                    remaining = self.graph.all_tasks - set(new_completed)
                    h = self.heuristic(remaining)
                    f_score = g + h

                    tie_breaker += 1
                    heapq.heappush(
                        pq, (f_score, tie_breaker, g, new_completed, new_workers, new_task_times)
                    )

        return -1, {}


# --- Example Usage ---
if __name__ == "__main__":
    # Task Durations
    durations = {"A": 3, "B": 2, "C": 4, "D": 1, "E": 2}

    # Dependencies (Task depends on list of tasks)
    # A -> B -> D
    # A -> C -> E
    dependencies = {"A": [], "B": ["A"], "C": ["A"], "D": ["B"], "E": ["C"]}

    graph = TaskGraph(durations, dependencies)
    ai = SchedulerAI(graph, num_workers=2)

    total_time, schedule = ai.a_star_solve()
    print(f"Optimal A* Total Time: {total_time}")
    print("Task Finish Times:")
    for task, t in sorted(schedule.items(), key=lambda x: x[1]):
        print(f"  Task {task} finishes at time {t}")
