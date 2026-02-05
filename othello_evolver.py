import tkinter as tk
from tkinter import messagebox
import random
import json
import os

BOARD_SIZE = 8
SQUARE_SIZE = 50
EMPTY, BLACK, WHITE = 0, 1, 2
KNOWLEDGE_FILE = "knowledge.json"

class OthelloEvolver:
    def __init__(self, master):
        self.master = master
        self.master.title("Othello Evolver - Autonomous Learning")
        
        # Initialize or Load Knowledge (Weight Table)
        self.load_knowledge()
        
        self.reset_game()
        self.setup_gui()
        
        # Training stats
        self.match_count = 0
        self.is_training = False

    def load_knowledge(self):
        if os.path.exists(KNOWLEDGE_FILE):
            with open(KNOWLEDGE_FILE, "r") as f:
                self.position_values = json.load(f)
            print("Knowledge loaded from file.")
        else:
            # Start with a flat (neutral) table if no knowledge exists
            self.position_values = [[0.0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
            print("New knowledge initialized.")

    def save_knowledge(self):
        with open(KNOWLEDGE_FILE, "w") as f:
            json.dump(self.position_values, f)

    def setup_gui(self):
        control_panel = tk.Frame(self.master)
        control_panel.pack(pady=10)

        self.train_btn = tk.Button(control_panel, text="Start Auto-Learning", command=self.toggle_training)
        self.train_btn.pack(side=tk.LEFT, padx=5)

        self.save_btn = tk.Button(control_panel, text="Save Knowledge", command=self.save_knowledge)
        self.save_btn.pack(side=tk.LEFT, padx=5)

        self.info_label = tk.Label(self.master, text="Matches Played: 0", font=("Arial", 12))
        self.info_label.pack()

        self.canvas = tk.Canvas(self.master, width=400, height=400, bg="dark green")
        self.canvas.pack()

    def reset_game(self):
        self.board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.board[3][3], self.board[4][4] = WHITE, WHITE
        self.board[3][4], self.board[4][3] = BLACK, BLACK
        self.current_player = BLACK
        self.history = {BLACK: [], WHITE: []} # Tracks where each player placed stones

    def toggle_training(self):
        self.is_training = not self.is_training
        self.train_btn.config(text="Stop Learning" if self.is_training else "Start Auto-Learning")
        if self.is_training:
            self.run_match()

    def run_match(self):
        if not self.is_training: return
        
        moves = self.get_legal_moves(self.board, self.current_player)
        if moves:
            # AI chooses move based on current position_values
            row, col = self.choose_best_move(moves)
            self.history[self.current_player].append((row, col))
            self.apply_move(self.board, row, col, self.current_player)
            self.draw_board()
        
        # Switch player
        self.current_player = 3 - self.current_player
        
        # Check if next player can move
        if not self.get_legal_moves(self.board, self.current_player):
            self.current_player = 3 - self.current_player
            # If neither can move, game over
            if not self.get_legal_moves(self.board, self.current_player):
                self.learn_from_result()
                self.match_count += 1
                self.info_label.config(text=f"Matches Played: {self.match_count}")
                self.reset_game()
                # Fast forward to next match
                self.master.after(10, self.run_match)
                return

        # Speed of visualization (set to 1 for super fast training)
        self.master.after(50, self.run_match)

    def choose_best_move(self, moves):
        # Epsilon-greedy: 10% chance to explore randomly to find new strategies
        if random.random() < 0.1:
            return random.choice(moves)
        
        best_score = -float('inf')
        best_moves = []
        for r, c in moves:
            score = self.position_values[r][c]
            if score > best_score:
                best_score = score
                best_moves = [(r, c)]
            elif score == best_score:
                best_moves.append((r, c))
        return random.choice(best_moves)

    def learn_from_result(self):
        b_count = sum(row.count(BLACK) for row in self.board)
        w_count = sum(row.count(WHITE) for row in self.board)
        
        if b_count > w_count:
            winner, loser = BLACK, WHITE
        elif w_count > b_count:
            winner, loser = WHITE, BLACK
        else:
            return # Draw - no learning today

        # Reward the winner's moves
        for r, c in self.history[winner]:
            self.position_values[r][c] += 0.1
        
        # Penalize the loser's moves
        for r, c in self.history[loser]:
            self.position_values[r][c] -= 0.1

    def draw_board(self):
        self.canvas.delete("all")
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                x, y = c*SQUARE_SIZE, r*SQUARE_SIZE
                self.canvas.create_rectangle(x, y, x+SQUARE_SIZE, y+SQUARE_SIZE, outline="black")
                if self.board[r][c] != EMPTY:
                    color = "black" if self.board[r][c] == BLACK else "white"
                    self.canvas.create_oval(x+2, y+2, x+SQUARE_SIZE-2, y+SQUARE_SIZE-2, fill=color)

    def apply_move(self, board, r, c, p):
        opp = 3 - p
        board[r][c] = p
        for dr, dc in [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]:
            tr, tc, temp = r + dr, c + dc, []
            while 0 <= tr < 8 and 0 <= tc < 8 and board[tr][tc] == opp:
                temp.append((tr, tc))
                tr, tc = tr + dr, tc + dc
            if 0 <= tr < 8 and 0 <= tc < 8 and board[tr][tc] == p:
                for fr, fc in temp: board[fr][fc] = p

    def get_legal_moves(self, board, p):
        moves = []
        for r in range(8):
            for c in range(8):
                if board[r][c] == EMPTY:
                    if self.is_legal(board, r, c, p): moves.append((r, c))
        return moves

    def is_legal(self, board, row, col, p):
        opp = 3 - p
        for dr, dc in [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]:
            r, c = row + dr, col + dc
            found_opp = False
            while 0 <= r < 8 and 0 <= c < 8 and board[r][c] == opp:
                r, c = r + dr, c + dc
                found_opp = True
            if found_opp and 0 <= r < 8 and 0 <= c < 8 and board[r][c] == p:
                return True
        return False

if __name__ == "__main__":
    root = tk.Tk()
    app = OthelloEvolver(root)
    root.mainloop()