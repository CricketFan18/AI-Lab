import heapq
import math
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Dict, Optional


class RobotPlanner:
    def __init__(self, grid: np.ndarray):
        """
        grid: 2D numpy array where 0 is walkable and 1 is an obstacle.
        """
        self.grid = grid
        self.rows, self.cols = grid.shape

    def heuristic(self, a: Tuple[int, int], b: Tuple[int, int], method: str) -> float:
        """Calculates distance between a and b."""
        if method == "manhattan":
            return abs(a[0] - b[0]) + abs(a[1] - b[1])
        elif method == "euclidean":
            return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)
        else:
            return 0.0  # Zero heuristic makes A* behave like Dijkstra (UCS)

    def get_neighbors(self, node: Tuple[int, int], allow_diagonal: bool) -> List[Tuple[int, int]]:
        """Returns valid neighbors."""
        r, c = node
        # Standard: Up, Down, Left, Right
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        if allow_diagonal:
            # Add diagonals: NE, NW, SE, SW
            directions += [(-1, 1), (-1, -1), (1, 1), (1, -1)]

        neighbors = []
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            # Check bounds and obstacles
            if 0 <= nr < self.rows and 0 <= nc < self.cols and self.grid[nr][nc] == 0:
                neighbors.append((nr, nc))
        return neighbors

    def search(
        self,
        start: Tuple[int, int],
        goal: Tuple[int, int],
        algo_type: str = "A*",
        movement_type: str = "4-way",
    ) -> Tuple[List, int]:
        """
        Unified Search Function.
        algo_type: 'A*', 'UCS', 'BFS'
        movement_type: '4-way' (Manhattan), '8-way' (Euclidean)
        Returns: (path, nodes_explored_count)
        """

        # Setup Priority Queue: (priority, sort_index, node)
        # sort_index is a tie-breaker to avoid comparing coordinate tuples directly
        pq = []
        heapq.heappush(pq, (0, 0, start))

        # Costs
        g_score: Dict[Tuple[int, int], float] = {start: 0.0}
        # Values can be a Tuple OR None
        parents: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {start: None}
        explored_count = 0
        # Determine heuristic method based on movement
        h_method = "manhattan" if movement_type == "4-way" else "euclidean"
        allow_diag = movement_type == "8-way"

        # Special case: BFS uses a Queue, not a Priority Queue based on cost
        # But we can simulate BFS in a PQ by using depth as priority (or just a simple list)
        if algo_type == "BFS":
            queue = [start]
            visited = {start}
            while queue:
                current = queue.pop(0)
                explored_count += 1

                if current == goal:
                    return self.reconstruct_path(parents, current), explored_count

                for neighbor in self.get_neighbors(current, allow_diag):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        parents[neighbor] = current
                        queue.append(neighbor)
            return [], explored_count

        # Logic for A* and UCS
        tie_breaker = 0
        while pq:
            _, _, current = heapq.heappop(pq)
            explored_count += 1

            if current == goal:
                return self.reconstruct_path(parents, current), explored_count

            for neighbor in self.get_neighbors(current, allow_diag):
                # Calculate movement cost
                # 1.0 for orthogonal, 1.414 (sqrt(2)) for diagonal
                move_cost = 1.0
                if abs(current[0] - neighbor[0]) == 1 and abs(current[1] - neighbor[1]) == 1:
                    move_cost = 1.414

                tentative_g = g_score[current] + move_cost

                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    g_score[neighbor] = tentative_g
                    parents[neighbor] = current

                    # Calculate Priority (f_score)
                    if algo_type == "UCS":
                        f_score = tentative_g  # Only cost matters
                    else:  # A*
                        f_score = tentative_g + self.heuristic(neighbor, goal, h_method)

                    tie_breaker += 1
                    heapq.heappush(pq, (f_score, tie_breaker, neighbor))

        return [], explored_count

    def reconstruct_path(self, parents, current):
        path = []
        while current:
            path.append(current)
            current = parents[current]
        return path[::-1]

    def visualize(self, path, title="Path"):
        """Visualizes the grid and the path."""
        # Create a display map: 0=free, 1=obstacle, 2=path, 3=start, 4=goal
        display_map = np.copy(self.grid)

        for r, c in path:
            display_map[r][c] = 0.5  # Mark path with a distinct value for color

        fig, ax = plt.subplots(figsize=(6, 6))
        # Use a colormap: white for free, black for obstacles, blue for path
        ax.imshow(display_map, cmap="magma")

        # Mark start and goal specifically
        if path:
            start, goal = path[0], path[-1]
            ax.text(start[1], start[0], "S", color="green", ha="center", va="center", weight="bold")
            ax.text(goal[1], goal[0], "G", color="red", ha="center", va="center", weight="bold")

        ax.set_title(title)
        plt.show()


# --- Driver Code ---
def main():
    # 0 = Free, 1 = Obstacle
    grid_size = 20
    grid = np.zeros((grid_size, grid_size))

    # Add some random obstacles
    np.random.seed(42)  # Fixed seed for reproducibility
    obstacles = np.random.rand(grid_size, grid_size) < 0.2
    grid[obstacles] = 1

    # Ensure start and goal are free
    start, goal = (0, 0), (19, 19)
    grid[start] = 0
    grid[goal] = 0

    planner = RobotPlanner(grid)

    print(f"Start: {start}, Goal: {goal}")
    print("\n--- 4-Way Movement (Manhattan) ---")
    path_a, nodes_a = planner.search(start, goal, "A*", "4-way")
    path_ucs, nodes_ucs = planner.search(start, goal, "UCS", "4-way")
    path_bfs, nodes_bfs = planner.search(start, goal, "BFS", "4-way")

    print(f"A* | Path Len: {len(path_a)} | Explored: {nodes_a}")
    print(f"UCS | Path Len: {len(path_ucs)} | Explored: {nodes_ucs}")
    print(f"BFS | Path Len: {len(path_bfs)} | Explored: {nodes_bfs}")

    planner.visualize(path_a, "A* Path (Manhattan)")
    print("\n--- 8-Way Movement (Euclidean) ---")
    path_diag, nodes_diag = planner.search(start, goal, "A*", "8-way")
    print(f"A* (Diag) | Path Len: {len(path_diag)} | Explored: {nodes_diag}")

    planner.visualize(path_diag, "A* Path (Euclidean)")


if __name__ == "__main__":
    main()
