import tkinter as tk
from tkinter import messagebox
from typing import List, Tuple, Set, Optional, Dict
from queue import PriorityQueue
import random

Board = Tuple[str, ...]

class GameModel:
    def __init__(self):
        # 3x3 Tuple of empty spaces
        self.initial_state: Board = (' ',) * 9
        self.lines = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8), # Rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8), # Cols
            (0, 4, 8), (2, 4, 6)             # Diags
        ]

    def get_current_player(self, state: Board) -> str:
        """Determines turn based on piece count. X goes first."""
        x_count = state.count('X')
        o_count = state.count('O')
        return 'X' if x_count == o_count else 'O'

    def get_legal_moves(self, state: Board) -> List[Board]:
        """Returns all possible next board states."""
        if self.is_terminal(state):
            return []
            
        player = self.get_current_player(state)
        moves = []
        state_list = list(state)
        
        for i in range(9):
            if state_list[i] == ' ':
                state_list[i] = player
                moves.append(tuple(state_list))
                state_list[i] = ' ' # Backtrack
        
        random.shuffle(moves) # Shuffle to add variety in simple searches
        return moves

    def get_winner(self, state: Board) -> Optional[str]:
        for line in self.lines:
            a, b, c = line
            if state[a] == state[b] == state[c] and state[a] != ' ':
                return state[a]
        return None

    def is_terminal(self, state: Board) -> bool:
        return self.get_winner(state) is not None or ' ' not in state

class GameAI:
    def __init__(self, model: GameModel):
        self.model = model

    def get_move_diff(self, old_state: Board, new_state: Board) -> int:
        """Helper to find which index changed between two states."""
        for i in range(9):
            if old_state[i] != new_state[i]:
                return i
        return -1

    def bfs_solve(self, start_node: Board, ai_player: str) -> Optional[Board]:
        """
        Breadth-First Search.
        Finds the path to the closest winning state.
        Note: This is 'optimistic'—it looks for a path where AI wins, 
        but doesn't guarantee the opponent plays optimally.
        """
        queue = [(start_node, [])] # (current_state, path_of_moves)
        visited = {start_node}

        while queue:
            current, path = queue.pop(0)

            # If this state is a win for AI, return the FIRST move that led here
            winner = self.model.get_winner(current)
            if winner == ai_player:
                return path[0] if path else None
            
            # Don't expand if game over (loss or draw)
            if winner is not None or ' ' not in current:
                continue

            # Expand
            for neighbor in self.model.get_legal_moves(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    # Append this state to the path history
                    new_path = path + [neighbor]
                    queue.append((neighbor, new_path))
        
        # If no forced win found, pick a random legal move
        moves = self.model.get_legal_moves(start_node)
        return moves[0] if moves else None

    def dfs_solve(self, start_node: Board, ai_player: str) -> Optional[Board]:
        """Depth-First Search. Dives deep into one variation."""
        stack = [(start_node, [])]
        visited = {start_node}

        while stack:
            current, path = stack.pop()
            
            winner = self.model.get_winner(current)
            if winner == ai_player:
                return path[0] if path else None
            
            if winner is not None or ' ' not in current:
                continue
                
            for neighbor in self.model.get_legal_moves(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    new_path = path + [neighbor]
                    stack.append((neighbor, new_path))
                    
        moves = self.model.get_legal_moves(start_node)
        return moves[0] if moves else None

    def heuristic(self, state: Board, ai_player: str) -> int:
        """
        Heuristic: 
        (Number of possible winning lines for AI) - (Number of possible winning lines for Opponent)
        """
        score = 0
        opponent = 'X' if ai_player == 'O' else 'O'
        
        for line in self.model.lines:
            line_vals = [state[i] for i in line]
            
            # Positive score if line is open for AI
            if opponent not in line_vals:
                score += 1
                if line_vals.count(ai_player) == 2: score += 10 # Close to win
            
            # Negative score if line is open for Opponent
            if ai_player not in line_vals:
                score -= 1
                if line_vals.count(opponent) == 2: score -= 10 # Block danger

        return score

    def a_star_solve(self, start_node: Board, ai_player: str) -> Optional[Board]:
        """
        A* Search adapted for Game State.
        Uses Priority Queue based on Cost (Depth) - Heuristic (Potential).
        """
        pq = PriorityQueue()
        # Priority: (f_score, tie_breaker, state, path)
        # We want to MINIMIZE cost, so we use negative heuristic for "Max" Logic
        pq.put((0, 0, start_node, []))
        
        visited = {start_node}
        tie_breaker = 0

        best_move_if_no_win = None
        max_heuristic_seen = -float('inf')

        while not pq.empty():
            _, _, current, path = pq.get()
            
            winner = self.model.get_winner(current)
            if winner == ai_player:
                return path[0] if path else None

            if winner is not None or ' ' not in current:
                continue

            # Limit depth to keep it responsive
            if len(path) > 4: 
                continue

            for neighbor in self.model.get_legal_moves(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    
                    # Calculate Score
                    h = self.heuristic(neighbor, ai_player)
                    g = len(path) + 1 # Cost is depth
                    
                    # Since PriorityQueue is Min-Heap, we invert logic for "Good" states
                    # Lower f_score should be better. 
                    # If h is high (good for AI), -h is low (good for PQ)
                    f_score = g - (h * 2) 
                    
                    # Track best intermediate move in case we don't find a forced win
                    if h > max_heuristic_seen:
                        max_heuristic_seen = h
                        if not path: # Immediate neighbor
                            best_move_if_no_win = neighbor
                        elif path: # Deep neighbor
                            best_move_if_no_win = path[0]

                    tie_breaker += 1
                    pq.put((f_score, tie_breaker, neighbor, path + [neighbor]))
        
        # Fallback
        moves = self.model.get_legal_moves(start_node)
        return best_move_if_no_win if best_move_if_no_win else (moves[0] if moves else None)

class TicTacToeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Assignment 7: Game AI")
        
        self.model = GameModel()
        self.ai = GameAI(self.model)
        self.current_state = self.model.initial_state
        self.ai_player = 'O'
        self.human_player = 'X'
        
        # UI Setup
        self.main_frame = tk.Frame(root, padx=20, pady=20)
        self.main_frame.pack()

        # Algorithm Selection
        self.algo_var = tk.StringVar(value="A*")
        control_frame = tk.Frame(self.main_frame)
        
        # FIX: 'mb' replaced with 'pady=(top, bottom)'
        control_frame.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        tk.Label(control_frame, text="AI Strategy: ").pack(side=tk.LEFT)
        modes = ["BFS", "DFS", "A*"]
        for mode in modes:
            tk.Radiobutton(control_frame, text=mode, variable=self.algo_var, value=mode).pack(side=tk.LEFT)

        # Buttons Grid
        self.buttons = []
        self.btn_frame = tk.Frame(self.main_frame)
        self.btn_frame.grid(row=1, column=0, columnspan=3)
        
        for i in range(9):
            btn = tk.Button(self.btn_frame, text=' ', font=('Arial', 24), width=4, height=2,
                            command=lambda idx=i: self.on_click(idx))
            btn.grid(row=i//3, column=i%3)
            self.buttons.append(btn)
            
        # Status
        self.status_lbl = tk.Label(self.main_frame, text="Your Turn (X)", font=('Arial', 12))
        
        # FIX: 'mt' replaced with 'pady'
        self.status_lbl.grid(row=2, column=0, columnspan=3, pady=(10, 0))

        # Reset
        # FIX: 'mt' replaced with 'pady'
        tk.Button(self.main_frame, text="Reset Game", command=self.reset_game).grid(row=3, column=0, columnspan=3, pady=(5, 0))

    def on_click(self, index):
        # 1. Human Move
        if self.current_state[index] != ' ' or self.model.is_terminal(self.current_state):
            return

        state_list = list(self.current_state)
        state_list[index] = self.human_player
        self.current_state = tuple(state_list)
        self.update_gui()

        if self.check_game_over(): return

        # 2. AI Move
        self.status_lbl.config(text="AI is thinking...")
        self.root.update() # Force refresh
        
        algo = self.algo_var.get()
        new_state = None
        
        if algo == "BFS":
            new_state = self.ai.bfs_solve(self.current_state, self.ai_player)
        elif algo == "DFS":
            new_state = self.ai.dfs_solve(self.current_state, self.ai_player)
        else:
            new_state = self.ai.a_star_solve(self.current_state, self.ai_player)
            
        if new_state:
            self.current_state = new_state
            self.update_gui()
            self.check_game_over()

    def update_gui(self):
        for i, val in enumerate(self.current_state):
            self.buttons[i].config(text=val, state=tk.NORMAL if val == ' ' else tk.DISABLED)
            # Color logic
            if val == 'X': self.buttons[i].config(disabledforeground="blue")
            if val == 'O': self.buttons[i].config(disabledforeground="red")

    def check_game_over(self):
        winner = self.model.get_winner(self.current_state)
        if winner:
            self.status_lbl.config(text=f"Winner: {winner}!")
            messagebox.showinfo("Game Over", f"{winner} wins!")
            return True
        elif ' ' not in self.current_state:
            self.status_lbl.config(text="It's a Draw!")
            messagebox.showinfo("Game Over", "Draw!")
            return True
        
        self.status_lbl.config(text="Your Turn (X)")
        return False

    def reset_game(self):
        self.current_state = self.model.initial_state
        self.update_gui()
        self.status_lbl.config(text="Your Turn (X)")
        
if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeApp(root)
    root.mainloop()