import copy
from queue import PriorityQueue
from typing import List, Tuple, Dict, Optional, Set

# Type alias for the board state (immutable tuple of tuples)
BoardState = Tuple[Tuple[int, ...], ...]


class EightPuzzleSolver:
    def __init__(self, start_grid: List[List[int]], goal_grid: List[List[int]]) -> None:
        # Convert lists to tuples for immutability (needed for sets/dicts)
        self.start_state: BoardState = tuple(tuple(row) for row in start_grid)
        self.goal_state: BoardState = tuple(tuple(row) for row in goal_grid)

        self.rows = len(start_grid)
        self.cols = len(start_grid[0])

        # Pre-compute goal coordinates for O(1) lookup during H2 calculation
        # Map: tile_value -> (row, col)
        self.goal_coords = {}
        for r in range(self.rows):
            for c in range(self.cols):
                val = self.goal_state[r][c]
                self.goal_coords[val] = (r, c)

    def find_zero(self, state: BoardState) -> Tuple[int, int]:
        """Helper to find the coordinates of the empty tile (0)."""
        for r in range(self.rows):
            for c in range(self.cols):
                if state[r][c] == 0:
                    return r, c
        return -1, -1

    def get_neighbors(self, state: BoardState) -> List[BoardState]:
        """Generates valid next states by sliding tiles into the empty space."""
        neighbors = []
        z_row, z_col = self.find_zero(state)

        # Directions: Up, Down, Left, Right
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dr, dc in directions:
            new_r, new_c = z_row + dr, z_col + dc

            if 0 <= new_r < self.rows and 0 <= new_c < self.cols:
                # Convert tuple to list to modify, then back to tuple
                new_state_list = [list(row) for row in state]
                # Swap 0 with the neighbor
                new_state_list[z_row][z_col], new_state_list[new_r][new_c] = (
                    new_state_list[new_r][new_c],
                    new_state_list[z_row][z_col],
                )

                neighbors.append(tuple(tuple(row) for row in new_state_list))

        return neighbors

    # --- Heuristics ---

    def h1_misplaced_tiles(self, state: BoardState) -> int:
        """H1: Count number of tiles in the wrong position (excluding 0)."""
        count = 0
        for r in range(self.rows):
            for c in range(self.cols):
                val = state[r][c]
                if val != 0 and val != self.goal_state[r][c]:
                    count += 1
        return count

    def h2_manhattan_distance(self, state: BoardState) -> int:
        """H2: Sum of Manhattan distances for all tiles to their goal positions."""
        distance = 0
        for r in range(self.rows):
            for c in range(self.cols):
                val = state[r][c]
                if val != 0:
                    target_r, target_c = self.goal_coords[val]
                    distance += abs(r - target_r) + abs(c - target_c)
        return distance

    # --- A* Search ---

    def search(self, heuristic_type: str = "H2") -> None:
        """
        Executes A* Search.
        heuristic_type: 'H1' for Misplaced Tiles, 'H2' for Manhattan Distance
        """
        # Choose the heuristic function
        if heuristic_type == "H1":
            heuristic_func = self.h1_misplaced_tiles
        else:
            heuristic_func = self.h2_manhattan_distance

        # Priority Queue stores: (f_score, state)
        pq = PriorityQueue()

        # g_score: cost from start to current node
        g_score: Dict[BoardState, int] = {self.start_state: 0}

        # Calculate initial f_score (g=0 + h)
        start_h = heuristic_func(self.start_state)
        pq.put((start_h, self.start_state))

        parent: Dict[BoardState, Optional[BoardState]] = {self.start_state: None}
        expanded_nodes = 0

        print(f"\n--- Starting A* Search using {heuristic_type} ---")

        while not pq.empty():
            current_f, current_state = pq.get()

            # If we reached the goal
            if current_state == self.goal_state:
                self.reconstruct_path(parent, current_state, expanded_nodes)
                return

            # Explore neighbors
            expanded_nodes += 1
            current_g = g_score[current_state]

            for neighbor in self.get_neighbors(current_state):
                # Tentative g_score is current cost + 1 (1 move)
                tentative_g = current_g + 1

                # If this path to neighbor is better, or we haven't seen it yet
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + heuristic_func(neighbor)

                    pq.put((f_score, neighbor))
                    parent[neighbor] = current_state

        print("No solution found.")

    def reconstruct_path(self, parent: Dict, end_state: BoardState, expanded: int) -> None:
        path = []
        curr = end_state
        while curr is not None:
            path.append(curr)
            curr = parent[curr]
        path.reverse()

        print(f"Goal Reached!")
        print(f"Nodes Explored: {expanded}")
        print(f"Solution Depth: {len(path) - 1}")
        for i, step in enumerate(path):
            print(f"Step {i}:")
            for row in step:
                print("  " + " ".join(str(val) for val in row))
            print()


def main():
    start_grid = [[2, 4, 3], [1, 6, 8], [7, 0, 5]]

    goal_grid = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    solver = EightPuzzleSolver(start_grid, goal_grid)
    solver.search(heuristic_type="H1")  # Misplaced Tiles
    solver.search(heuristic_type="H2")  # Manhattan Distance


if __name__ == "__main__":
    main()
