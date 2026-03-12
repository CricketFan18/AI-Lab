from typing import Dict, List, Tuple, Optional
from queue import PriorityQueue
from collections import deque


class UniformCostSearch:
    def __init__(self, graph: Dict[str, List[Tuple[str, int]]]) -> None:
        """
        graph adjacency list format:
        {
            'A': [('B', 2), ('C', 5)],
            'B': [('D', 4)],
            ...
        }
        """
        self.graph = graph
        self.path: List[str] = []
        self.min_cost: Optional[int] = None
        self.stats = {"expanded": 0, "relaxed": 0}

    def search(self, start: str, goal: str) -> None:
        # parent[node] = previous_node on best path
        parent: Dict[str, Optional[str]] = {start: None}

        # best_cost[node] = best known cost to reach node
        best_cost: Dict[str, int] = {start: 0}

        pq = PriorityQueue()
        pq.put((0, start))  # (total_cost_so_far, node)

        while not pq.empty():
            cost_so_far, node = pq.get()
            self.stats["expanded"] += 1

            # Important: skip if this is an outdated (worse) entry
            if cost_so_far != best_cost.get(node, float("inf")):
                continue

            if node == goal:
                self.min_cost = cost_so_far
                self.path = self.construct_path(parent, goal)
                return

            for neighbor, edge_cost in self.graph.get(node, []):
                new_cost = cost_so_far + edge_cost

                if new_cost < best_cost.get(neighbor, float("inf")):
                    best_cost[neighbor] = new_cost
                    parent[neighbor] = node
                    pq.put((new_cost, neighbor))
                    self.stats["relaxed"] += 1

        # no path
        self.path = []
        self.min_cost = None

    def construct_path(self, parent: Dict[str, Optional[str]], end: str) -> List[str]:
        path = []
        cur: Optional[str] = end
        while cur is not None:
            path.append(cur)
            cur = parent.get(cur)
        return path[::-1]

    def showResult(self) -> None:
        if not self.path:
            print("No Path Available (UCS)")
            print("Stats:", self.stats)
            return

        print("Found the optimal path by Uniform Cost Search (UCS)")
        print("Path:", " -> ".join(self.path))
        print("Minimum Cost:", self.min_cost)
        print("Stats:", self.stats)


def main():
    # Example transportation network (weighted graph)
    graph = {
        "A": [("B", 2), ("C", 5)],
        "B": [("C", 1), ("D", 4)],
        "C": [("D", 1), ("E", 7)],
        "D": [("E", 3)],
        "E": [],
    }

    ucs = UniformCostSearch(graph)
    ucs.search("A", "E")
    ucs.showResult()


if __name__ == "__main__":
    main()
