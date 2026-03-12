from typing import List, Tuple, Dict, Optional
from queue import PriorityQueue


class TreasureHunt:
    def __init__(self, grid: List[List[str]]) -> None:
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0]) if self.rows else 0
        self.result: List[Tuple[int, int]] = []
        self.stats = {"expanded": 0, "discovered": 0}

    def manhattan(self, a: Tuple[int, int], b: Tuple[int, int]) -> int:
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def is_walkable(self, x: int, y: int) -> bool:
        return self.grid[x][y] in ("W", "S", "X")

    def search(self, start: List[int], goal: List[int]) -> None:
        start_t = (start[0], start[1])
        goal_t = (goal[0], goal[1])

        explored = set([start_t])  # visited/discovered
        parent: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {start_t: None}

        pq = PriorityQueue()
        pq.put((self.manhattan(start_t, goal_t), start_t))  # (heuristic, node)

        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        while not pq.empty():
            h, (x, y) = pq.get()
            self.stats["expanded"] += 1

            # If we reached the treasure
            if (x, y) == goal_t or self.grid[x][y] == "X":
                self.result = self.construct_path(parent, (x, y))
                return

            for dx, dy in directions:
                nx, ny = x + dx, y + dy

                if 0 <= nx < self.rows and 0 <= ny < self.cols:
                    if (nx, ny) in explored:
                        continue
                    if not self.is_walkable(nx, ny):
                        continue  # blocked

                    explored.add((nx, ny))
                    parent[(nx, ny)] = (x, y)
                    self.stats["discovered"] += 1

                    nh = self.manhattan((nx, ny), goal_t)
                    pq.put((nh, (nx, ny)))

        # If we exit the loop, no path found
        self.result = []

    def construct_path(
        self, parent: Dict[Tuple[int, int], Optional[Tuple[int, int]]], end: Tuple[int, int]
    ) -> List[Tuple[int, int]]:
        path = []
        cur: Optional[Tuple[int, int]] = end
        while cur is not None:
            path.append(cur)
            cur = parent.get(cur)
        return path[::-1]

    def showResult(self) -> None:
        if not self.result:
            print("No Path Available")
            print("Stats:", self.stats)
            return

        print("Found the path by Best-First Search (Greedy BFS)")
        print(f"Path length: {len(self.result)}")
        print(f"Path: {self.result}")
        print("Stats:", self.stats)


def main():
    grid = [
        ["S", "B", "W", "W", "W"],
        ["W", "B", "W", "B", "W"],
        ["W", "B", "W", "B", "W"],
        ["W", "B", "W", "B", "W"],
        ["W", "W", "W", "B", "X"],
    ]

    hunter = TreasureHunt(grid)
    hunter.search([0, 0], [4, 4])
    hunter.showResult()


if __name__ == "__main__":
    main()
