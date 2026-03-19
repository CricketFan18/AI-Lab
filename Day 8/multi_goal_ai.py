import heapq
from typing import List, Tuple, Dict, Set, FrozenSet

# Type Aliases for readability
# State: (row, col, collected_goal_ids)
State = Tuple[int, int, FrozenSet[int]]


class MultiGoalGrid:
    def __init__(self, grid: List[List[str]], goals: Dict[Tuple[int, int], int]):
        """
        grid: 2D array ('S'=start, 'E'=exit, '.'=open, '#'=wall)
        goals: Dictionary mapping (row, col) to priority/reward score
        """
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])
        self.goals = goals

        # Locate Start and Exit
        self.start_pos = self.find_char("S")
        self.exit_pos = self.find_char("E")

    def find_char(self, char: str) -> Tuple[int, int]:
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == char:
                    return (r, c)
        return (-1, -1)

    def get_neighbors(self, r: int, c: int) -> List[Tuple[int, int]]:
        valid = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols and self.grid[nr][nc] != "#":
                valid.append((nr, nc))
        return valid


class MultiGoalAI:
    def __init__(self, environment: MultiGoalGrid):
        self.env = environment

    def heuristic(self, current_pos: Tuple[int, int], collected: FrozenSet[int]) -> float:
        """
        A basic heuristic for multi-goal.
        For true A*, this needs to be admissible (never overestimate).
        A simple valid heuristic: Distance to the Exit.
        A better one: Distance to nearest uncollected goal + distance to exit.
        """
        # Simple Manhattan distance to exit
        return abs(current_pos[0] - self.env.exit_pos[0]) + abs(
            current_pos[1] - self.env.exit_pos[1]
        )

    def solve_a_star(self) -> Tuple[int, List[Tuple[int, int]]]:
        """Finds the optimal path balancing step cost and goal rewards."""

        # Initial State: Start pos, empty set of collected goals
        start_state: State = (self.env.start_pos[0], self.env.start_pos[1], frozenset())

        # Priority Queue: (f_score, tie_breaker, g_score, state, path)
        pq = []
        heapq.heappush(pq, (0, 0, 0, start_state, [self.env.start_pos]))

        # g_score dictionary now tracks the exact STATE, not just the coordinate
        g_scores: Dict[State, int] = {start_state: 0}

        tie_breaker = 0
        best_final_score = float("inf")
        best_path = []

        while pq:
            f, _, g, current_state, path = heapq.heappop(pq)
            r, c, collected = current_state

            # 1. Check if we reached the exit
            if (r, c) == self.env.exit_pos:
                # We reached the end. Did we get a good score?
                if g < best_final_score:
                    best_final_score = g
                    best_path = path
                continue  # Keep searching to see if there's a better path

            # 2. Explore Neighbors
            for nr, nc in self.env.get_neighbors(r, c):
                new_collected = set(collected)
                step_cost = 1

                # Check if this neighbor is a new goal we haven't collected yet
                if (nr, nc) in self.env.goals and (nr, nc) not in collected:
                    new_collected.add((nr, nc))
                    # Subtract priority from the cost (Reward!)
                    step_cost -= self.env.goals[(nr, nc)]

                new_state = (nr, nc, frozenset(new_collected))
                tentative_g = g + step_cost

                # 3. State update
                if new_state not in g_scores or tentative_g < g_scores[new_state]:
                    g_scores[new_state] = tentative_g

                    h = self.heuristic((nr, nc), frozenset(new_collected))
                    f_score = tentative_g + h

                    tie_breaker += 1
                    heapq.heappush(
                        pq, (f_score, tie_breaker, tentative_g, new_state, path + [(nr, nc)])
                    )

        return best_final_score, best_path  # type: ignore


# --- Quick Test ---
if __name__ == "__main__":
    # S = Start, E = Exit, * = Goals
    maze = [["S", ".", ".", "#", "*"], ["#", "#", ".", "#", "."], ["*", ".", ".", ".", "E"]]

    # Map coordinates to their priority reward
    goal_priorities = {(0, 4): 15, (2, 0): 5}  # High priority goal  # Low priority goal

    env = MultiGoalGrid(maze, goal_priorities)
    ai = MultiGoalAI(env)

    score, final_path = ai.solve_a_star()
    print(f"Final Path Score (Cost - Reward): {score}")
    print(f"Path Length: {len(final_path)} steps")
    print(f"Path taken: {final_path}")
