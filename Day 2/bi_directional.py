import networkx as nx
import matplotlib.pyplot as plt
from collections import deque


class Navigator:
    def __init__(self, graph_matrix) -> None:
        self.graph_matrix = graph_matrix
        self.n = len(graph_matrix)
        self.nodes_explored = 0

        # Convert adjacency matrix to NetworkX graph for visualization
        self.G = nx.Graph()
        for r in range(self.n):
            for c in range(r, self.n):  # Undirected, check upper triangle
                if self.graph_matrix[r][c] == 1:
                    self.G.add_edge(r, c)

    def reset_counter(self):
        self.nodes_explored = 0

    # --- Task 1: Bi-directional BFS (Optimal Shortest Path) ---
    def solve_bidirectional_bfs(self, start, end):
        self.reset_counter()
        if start == end:
            return [start]

        q_up = deque([start])
        q_down = deque([end])

        parent_up = {start: None}
        parent_down = {end: None}

        while q_up and q_down:
            # 1. Expand from Start
            if q_up:
                self.nodes_explored += 1
                u = q_up.popleft()
                for v, has_edge in enumerate(self.graph_matrix[u]):
                    if has_edge == 1:
                        if v not in parent_up:
                            parent_up[v] = u
                            q_up.append(v)
                            # Collision Check
                            if v in parent_down:
                                return self._merge_paths(parent_up, parent_down, v)

            # 2. Expand from End
            if q_down:
                self.nodes_explored += 1
                u = q_down.popleft()
                for v, has_edge in enumerate(self.graph_matrix[u]):
                    if has_edge == 1:
                        if v not in parent_down:
                            parent_down[v] = u
                            q_down.append(v)
                            # Collision Check
                            if v in parent_up:
                                return self._merge_paths(parent_up, parent_down, v)
        return []

    # --- Task 1 (Extra): Bi-directional DFS (Non-Optimal Path) ---
    def solve_bidirectional_dfs(self, start, end):
        self.reset_counter()
        if start == end:
            return [start]

        # Use Stacks for DFS (Last-In-First-Out)
        stack_up = [start]
        stack_down = [end]

        parent_up = {start: None}
        parent_down = {end: None}

        while stack_up and stack_down:
            # 1. Step from Start
            if stack_up:
                self.nodes_explored += 1
                u = stack_up.pop()

                # Check if we bumped into the other search's path
                if u in parent_down:
                    return self._merge_paths(parent_up, parent_down, u)

                for v, has_edge in enumerate(self.graph_matrix[u]):
                    if has_edge == 1 and v not in parent_up:
                        parent_up[v] = u
                        stack_up.append(v)

            # 2. Step from End
            if stack_down:
                self.nodes_explored += 1
                u = stack_down.pop()

                # Check if we bumped into the other search's path
                if u in parent_up:
                    return self._merge_paths(parent_up, parent_down, u)

                for v, has_edge in enumerate(self.graph_matrix[u]):
                    if has_edge == 1 and v not in parent_down:
                        parent_down[v] = u
                        stack_down.append(v)
        return []

    def _merge_paths(self, parent_up, parent_down, meeting_node):
        # Reconstruct path from Start -> Meeting
        path_start = []
        curr = meeting_node
        while curr is not None:
            path_start.append(curr)
            curr = parent_up.get(curr)  # .get() avoids errors if key missing
        path_start.reverse()

        # Reconstruct path from Meeting -> End
        path_end = []
        # Start from parent of meeting node to avoid duplicates
        curr = parent_down.get(meeting_node)
        while curr is not None:
            path_end.append(curr)
            curr = parent_down.get(curr)

        return path_start + path_end

    # --- Standard BFS (For Comparison) ---
    def solve_standard_bfs(self, start, end):
        self.reset_counter()
        q = deque([start])
        visited = {start: None}

        while q:
            self.nodes_explored += 1
            u = q.popleft()
            if u == end:
                return self._reconstruct_path(visited, end)

            for v, has_edge in enumerate(self.graph_matrix[u]):
                if has_edge == 1 and v not in visited:
                    visited[v] = u
                    q.append(v)
        return []

    # --- Standard DFS (For Comparison) ---
    def solve_standard_dfs(self, start, end):
        self.reset_counter()
        stack = [start]
        visited = {start: None}

        while stack:
            self.nodes_explored += 1
            u = stack.pop()
            if u == end:
                return self._reconstruct_path(visited, end)

            for v, has_edge in enumerate(self.graph_matrix[u]):
                if has_edge == 1 and v not in visited:
                    visited[v] = u
                    stack.append(v)
        return []

    def _reconstruct_path(self, parents, end_node):
        path = []
        curr = end_node
        while curr is not None:
            path.append(curr)
            curr = parents[curr]
        return path[::-1]

    # --- Visualization ---
    def visualize_path(self, path, title="Path Visualization"):
        # Use spring_layout for better positioning, seed ensures it looks same every time
        pos = nx.spring_layout(self.G, seed=42)
        plt.figure(figsize=(8, 6))

        # Draw background graph
        nx.draw(
            self.G,
            pos,
            with_labels=True,
            node_color="lightblue",
            node_size=500,
            font_weight="bold",
            edge_color="gray",
        )

        # Draw solution path
        if path:
            path_edges = list(zip(path, path[1:]))
            nx.draw_networkx_nodes(self.G, pos, nodelist=path, node_color="orange", node_size=300)
            nx.draw_networkx_edges(self.G, pos, edgelist=path_edges, edge_color="red", width=2.5)

        plt.title(title)
        print(f"Displaying: {title} (Close window to continue)")
        plt.show()


def create_city_grid(rows, cols):
    """
    Generates an adjacency matrix for a grid-like city map.
    Nodes are numbered 0 to (rows*cols - 1).
    Each node connects to its neighbors (Up, Down, Left, Right).
    """
    n = rows * cols
    matrix = [[0] * n for _ in range(n)]

    for r in range(rows):
        for c in range(cols):
            u = r * cols + c

            # Connect to the Right Neighbor
            if c + 1 < cols:
                v = r * cols + (c + 1)
                matrix[u][v] = 1
                matrix[v][u] = 1

            # Connect to the Bottom Neighbor
            if r + 1 < rows:
                v = (r + 1) * cols + c
                matrix[u][v] = 1
                matrix[v][u] = 1

    return matrix


def main():
    ROWS, COLS = 6, 6
    mat = create_city_grid(ROWS, COLS)
    start_node = 0
    end_node = 7

    nav = Navigator(mat)

    print(f"--- COMPARISON: 6x6 Grid City (Node {start_node} to {end_node}) ---\n")

    # Bi-Directional BFS
    bi_bfs_path = nav.solve_bidirectional_bfs(start_node, end_node)
    print(
        f"[Bi-Directional BFS]\t Nodes Explored: {nav.nodes_explored} \t(Path Length: {len(bi_bfs_path)})"
    )

    # Bi-Directional DFS
    bi_dfs_path = nav.solve_bidirectional_dfs(start_node, end_node)
    print(
        f"[Bi-Directional DFS]\t Nodes Explored: {nav.nodes_explored} \t(Path Length: {len(bi_dfs_path)})"
    )

    # Visualize
    nav.visualize_path(bi_bfs_path, f"6x6 City Grid: {start_node} to {end_node}")


if __name__ == "__main__":
    main()
