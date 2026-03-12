from typing import List
import copy
from collections import deque


class MazeProblem:
    def __init__(self, maze: List[List[int]]):
        self.maze = maze
        self.row = len(maze)
        self.column = len(maze[0])

        self.result_dfs = []
        self.result_bfs = []

        self.dfs_nodes_explored = 0
        self.bfs_nodes_explored = 0

    # ---------------- DFS ----------------
    def solve_dfs(self):
        temp_maze = copy.deepcopy(self.maze)
        self.result_dfs = []
        self.dfs_nodes_explored = 0
        found = False  # stop after one valid path

        def dfs(path, x, y):
            nonlocal found
            if found:
                return

            if not (0 <= x < self.row and 0 <= y < self.column):
                return
            if temp_maze[x][y] == 0:
                return

            self.dfs_nodes_explored += 1
            path.append([x, y])

            if x == self.row - 1 and y == self.column - 1:
                self.result_dfs = path[:]
                found = True
                return

            temp_maze[x][y] = 0
            dfs(path, x + 1, y)
            dfs(path, x - 1, y)
            dfs(path, x, y + 1)
            dfs(path, x, y - 1)
            temp_maze[x][y] = 1

            path.pop()

        if self.maze[0][0] == 1:
            dfs([], 0, 0)

    # ---------------- BFS ----------------
    def solve_bfs(self):
        self.result_bfs = []
        self.bfs_nodes_explored = 0

        if self.maze[0][0] == 0 or self.maze[self.row - 1][self.column - 1] == 0:
            return

        queue = deque()
        queue.append((0, 0, [[0, 0]]))
        visited = set()
        visited.add((0, 0))

        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        while queue:
            x, y, path = queue.popleft()
            self.bfs_nodes_explored += 1

            if x == self.row - 1 and y == self.column - 1:
                self.result_bfs = path
                return

            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if (
                    0 <= nx < self.row
                    and 0 <= ny < self.column
                    and self.maze[nx][ny] == 1
                    and (nx, ny) not in visited
                ):
                    visited.add((nx, ny))
                    queue.append((nx, ny, path + [[nx, ny]]))

    # ---------------- OUTPUT ----------------
    def printMaze(self):
        print("--- Maze Layout ---")
        for row in self.maze:
            print(row)

    def show_results(self):
        print("\n--- DFS Result (One Valid Path) ---")
        if not self.result_dfs:
            print("No path found via DFS.")
        else:
            print(f"Path Length: {len(self.result_dfs)}")
            print(f"Path: {self.result_dfs}")
            print(f"Nodes Explored (DFS): {self.dfs_nodes_explored}")

        print("\n--- BFS Result (Shortest Path) ---")
        if not self.result_bfs:
            print("No path found via BFS.")
        else:
            print(f"Shortest Path Length: {len(self.result_bfs)}")
            print(f"Path: {self.result_bfs}")
            print(f"Nodes Explored (BFS): {self.bfs_nodes_explored}")

        print("\n--- Comparison ---")
        print(f"DFS explored {self.dfs_nodes_explored} nodes.")
        print(f"BFS explored {self.bfs_nodes_explored} nodes.")


# ---------------- MAIN ----------------
def main():
    maze = [[1, 1, 1, 1, 1], [1, 0, 0, 0, 1], [1, 1, 1, 0, 1], [1, 0, 1, 1, 1], [1, 1, 0, 1, 1]]

    solver = MazeProblem(maze)
    solver.printMaze()
    solver.solve_dfs()
    solver.solve_bfs()
    solver.show_results()


if __name__ == "__main__":
    main()
