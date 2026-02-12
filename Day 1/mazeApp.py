import tkinter as tk
import MazeProblem

class MazeApp:
    def __init__(self, root, maze, solver):
        self.root = root
        self.maze = maze
        self.solver = solver
        self.rows = len(maze)
        self.cols = len(maze[0])
        self.cell_size = 40
        self.rects = {}
        self.canvas = tk.Canvas(root, width=self.cols * self.cell_size, 
                                height=self.rows * self.cell_size)
        self.canvas.pack()
        self.draw_grid()
        self.algorithm_step = self.solver.bfs_generator()
        self.btn = tk.Button(root, text="Start", command=self.animate_step)
        self.btn.pack()

    def draw_grid(self):
        for r in range(self.rows):
            for c in range(self.cols):
                x1, y1 = c * self.cell_size, r * self.cell_size
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size
                color = "white"
                if self.maze[r][c] == 0: color = "black"
                if (r, c) == (0, 0): color = "green"
                if (r, c) == (self.rows-1, self.cols-1): color = "red"
                self.rects[(r, c)] = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

    def animate_step(self):
        """
        Asks the solver for the NEXT step and updates the UI.
        Uses root.after() to schedule the next frame.
        """
        try:
            action, data = next(self.algorithm_step)
            if action == "VISIT":
                r, c = data
                # Don't color over start/end
                if (r, c) != (0, 0) and (r, c) != (self.rows-1, self.cols-1):
                    self.update_color(r, c, "lightblue")
                self.root.after(50, self.animate_step)
                
            elif action == "PATH":
                self.draw_path(data)
                
        except StopIteration:
            print("Algorithm Finished")

    def draw_path(self, path):
        for r, c in path:
            if (r, c) != (0, 0) and (r, c) != (self.rows-1, self.cols-1):
                self.update_color(r, c, "gold")
    
    def update_color(self, r, c, color):
        self.canvas.itemconfig(self.rects[(r, c)], fill=color)

if __name__ == "__main__":
    maze_layout = [
        [1, 1, 1, 0, 1, 1, 1],
        [1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1]
    ]

    root = tk.Tk()
    root.title("Modular Maze Solver")
    solver = MazeProblem(maze_layout)
    app = MazeApp(root, maze_layout, solver)
    
    root.mainloop()