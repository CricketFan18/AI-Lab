import tkinter as tk
import time
from collections import deque

class MazeVisualizer:
    def __init__(self, root, maze):
        self.root = root
        self.maze = maze
        self.rows = len(maze)
        self.cols = len(maze[0])
        self.cell_size = 40
        self.rects = {}
        self.canvas = tk.Canvas(root, width=self.cols * self.cell_size, 
                                height=self.rows * self.cell_size)
        self.canvas.pack()
        self.draw_maze()
        self.btn = tk.Button(root, text="Start BFS Visualization", command=self.run_bfs)
        self.btn.pack()

    def draw_maze(self):
        """Draws the initial grid"""
        for r in range(self.rows):
            for c in range(self.cols):
                x1 = c * self.cell_size
                y1 = r * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                
                color = "white"
                if self.maze[r][c] == 0: color = "black"    # Wall
                if r == 0 and c == 0: color = "green"       # Start
                if r == self.rows-1 and c == self.cols-1: color = "red" # End
                rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")
                self.rects[(r, c)] = rect

    def update_cell(self, r, c, color):
        """Updates a specific cell's color instantly"""
        # Don't overwrite Start/End colors unnecessarily
        if (r, c) == (0, 0) or (r, c) == (self.rows-1, self.cols-1):
            return
            
        rect_id = self.rects[(r, c)]
        self.canvas.itemconfig(rect_id, fill=color)
        self.root.update() # Force Tkinter to refresh the screen

    def run_bfs(self):
        """Runs BFS with animation"""
        queue = deque()
        queue.append((0, 0, [])) # r, c, path
        visited = set()
        visited.add((0, 0))
        
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        
        found = False
        final_path = []

        while queue:
            r, c, path = queue.popleft()
            
            # If we reached the end
            if r == self.rows - 1 and c == self.cols - 1:
                final_path = path + [(r, c)]
                found = True
                break

            # Animation: Color the node currently being processed
            self.update_cell(r, c, "lightblue")
            time.sleep(0.05) # Slow down so we can see it

            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                
                if (0 <= nr < self.rows and 
                    0 <= nc < self.cols and 
                    self.maze[nr][nc] == 1 and 
                    (nr, nc) not in visited):
                    
                    visited.add((nr, nc))
                    queue.append((nr, nc, path + [(r, c)]))

        if found:
            print("Path Found! Drawing path...")
            self.draw_path(final_path)
        else:
            print("No Path Found")

    def draw_path(self, path):
        """Highlights the final path in yellow"""
        for r, c in path:
            self.update_cell(r, c, "gold")
            time.sleep(0.05)

# --- CONFIGURATION ---
if __name__ == "__main__":
    # 0 = Wall, 1 = Path
    maze_layout = [
        [1, 1, 1, 0, 1, 1, 1],
        [1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1]
    ]

    root = tk.Tk()
    root.title("Maze Solver Visualization")
    
    app = MazeVisualizer(root, maze_layout)
    
    root.mainloop()