from typing import Dict, List, Tuple, Optional
from collections import deque


class BFSUnweighted:
    def __init__(self, graph: Dict[str, List[Tuple[str, int]]]) -> None:
        self.graph = graph
        self.path: List[str] = []
        self.stats = {"expanded": 0}

    def search(self, start: str, goal: str) -> None:
        parent: Dict[str, Optional[str]] = {start: None}
        visited = set([start])

        q = deque([start])

        while q:
            node = q.popleft()
            self.stats["expanded"] += 1

            if node == goal:
                self.path = self.construct_path(parent, goal)
                return

            for neighbor, _cost in self.graph.get(node, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = node
                    q.append(neighbor)

        self.path = []

    def construct_path(self, parent: Dict[str, Optional[str]], end: str) -> List[str]:
        path = []
        cur: Optional[str] = end
        while cur is not None:
            path.append(cur)
            cur = parent.get(cur)
        return path[::-1]

    def showResult(self) -> None:
        if not self.path:
            print("No Path Available (BFS)")
            print("Stats:", self.stats)
            return

        print("Found a path by BFS (fewest edges, not minimum cost)")
        print("Path:", " -> ".join(self.path))
        print("Stats:", self.stats)
