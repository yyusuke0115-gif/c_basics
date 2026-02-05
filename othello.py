import tkinter as tk
from tkinter import messagebox, ttk
import random

# Constants
BOARD_SIZE = 8
SQUARE_SIZE = 60
EMPTY, BLACK, WHITE = 0, 1, 2
DEPTH = 4  # Default depth
SOLVE_LIMIT = 10 # Number of empty squares to start perfect endgame solving

POSITION_VALUES = [
    [100, -20,  10,   5,   5,  10, -20, 100],
    [-20, -50,  -2,  -2,  -2,  -2, -50, -20],
    [ 10,  -2,   5,   1,   1,   5,  -2,  10],
    [  5,  -2,   1,   1,   1,   1,  -2,   5],
    [  5,  -2,   1,   1,   1,   1,  -2,   5],
    [ 10,  -2,   5,   1,   1,   5,  -2,  10],
    [-20, -50,  -2,  -2,  -2,  -2, -50, -20],
    [100, -20,  10,   5,   5,  10, -20, 100],
]

class OthelloLab:
    def __init__(self, master):
        self.master = master
        self.master.title("Othello AI Laboratory")
        self.board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.current_player = BLACK
        
        # UI Setup
        self.setup_control_panel()
        self.setup_canvas()
        self.reset_game()

    def setup_control_panel(self):
        panel = tk.Frame(self.master)
        panel.pack(pady=10)

        tk.Label(panel, text="Black (P1):").grid(row=0, column=0)
        self.p1_type = ttk.Combobox(panel, values=["Minimax", "Alpha-Beta", "Alpha-Beta + Solver"])
        self.p1_type.current(0)
        self.p1_type.grid(row=0, column=1, padx=5)

        tk.Label(panel, text="White (P2):").grid(row=0, column=2)
        self.p2_type = ttk.Combobox(panel, values=["Minimax", "Alpha-Beta", "Alpha-Beta + Solver"])
        self.p2_type.current(2)
        self.p2_type.grid(row=0, column=3, padx=5)

        self.start_btn = tk.Button(panel, text="Start Match", command=self.start_match)
        self.start_btn.grid(row=0, column=4, padx=10)

    def setup_canvas(self):
        self.status_label = tk.Label(self.master, text="Select AIs and Start", font=("Arial", 12))
        self.status_label.pack()
        self.canvas = tk.Canvas(self.master, width=480, height=480, bg="dark green")
        self.canvas.pack()

    def reset_game(self):
        self.board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.board[3][3], self.board[4][4] = WHITE, WHITE
        self.board[3][4], self.board[4][3] = BLACK, BLACK
        self.current_player = BLACK
        self.is_running = False
        self.draw_board()

    def start_match(self):
        self.reset_game()
        self.is_running = True
        self.play_next_move()

    def draw_board(self):
        self.canvas.delete("all")
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                x, y = c*SQUARE_SIZE, r*SQUARE_SIZE
                self.canvas.create_rectangle(x, y, x+SQUARE_SIZE, y+SQUARE_SIZE, outline="black")
                if self.board[r][c] != EMPTY:
                    color = "black" if self.board[r][c] == BLACK else "white"
                    self.canvas.create_oval(x+5, y+5, x+SQUARE_SIZE-5, y+SQUARE_SIZE-5, fill=color)

    def play_next_move(self):
        if not self.is_running: return
        
        strategy = self.p1_type.get() if self.current_player == BLACK else self.p2_type.get()
        self.status_label.config(text=f"Turn: {'BLACK' if self.current_player==BLACK else 'WHITE'} ({strategy})")
        
        best_move = self.think(self.current_player, strategy)
        
        if best_move:
            self.apply_move(self.board, best_move[0], best_move[1], self.current_player)
            self.draw_board()

        self.current_player = 3 - self.current_player # Switch 1<->2
        
        if not self.get_legal_moves(self.board, self.current_player):
            self.current_player = 3 - self.current_player
            if not self.get_legal_moves(self.board, self.current_player):
                self.end_game()
                return
        
        self.master.after(500, self.play_next_move)

    def think(self, player, strategy):
        moves = self.get_legal_moves(self.board, player)
        if not moves: return None
        
        empty_count = sum(row.count(EMPTY) for row in self.board)
        use_solver = "Solver" in strategy and empty_count <= SOLVE_LIMIT
        
        best_moves = []
        best_score = -float('inf')
        
        for r, c in moves:
            temp = [row[:] for row in self.board]
            self.apply_move(temp, r, c, player)
            
            if use_solver:
                # Perfect play: maximize stone count difference
                score = -self.minimax_alpha_beta(temp, empty_count, -float('inf'), float('inf'), False, player, True)
            elif "Alpha-Beta" in strategy:
                score = -self.minimax_alpha_beta(temp, DEPTH-1, -float('inf'), float('inf'), False, player, False)
            else:
                score = -self.minimax_basic(temp, DEPTH-1, False, player)
            
            if score > best_score:
                best_score = score
                best_moves = [(r, c)]
            elif score == best_score:
                best_moves.append((r, c))
        
        return random.choice(best_moves)

    def minimax_alpha_beta(self, board, depth, alpha, beta, is_max, ai_player, is_solving):
        if depth == 0:
            return self.evaluate(board, ai_player, is_solving)
        
        current = ai_player if is_max else (3 - ai_player)
        moves = self.get_legal_moves(board, current)
        
        if not moves:
            return self.minimax_alpha_beta(board, depth-1, alpha, beta, not is_max, ai_player, is_solving)

        if is_max:
            v = -float('inf')
            for r, c in moves:
                t = [row[:] for row in board]
                self.apply_move(t, r, c, current)
                v = max(v, self.minimax_alpha_beta(t, depth-1, alpha, beta, False, ai_player, is_solving))
                alpha = max(alpha, v)
                if beta <= alpha: break
            return v
        else:
            v = float('inf')
            for r, c in moves:
                t = [row[:] for row in board]
                self.apply_move(t, r, c, current)
                v = min(v, self.minimax_alpha_beta(t, depth-1, alpha, beta, True, ai_player, is_solving))
                beta = min(beta, v)
                if beta <= alpha: break
            return v

    def minimax_basic(self, board, depth, is_max, ai_player):
        if depth == 0: return self.evaluate(board, ai_player, False)
        current = ai_player if is_max else (3 - ai_player)
        moves = self.get_legal_moves(board, current)
        if not moves: return self.minimax_basic(board, depth-1, not is_max, ai_player)
        
        scores = []
        for r, c in moves:
            t = [row[:] for row in board]
            self.apply_move(t, r, c, current)
            scores.append(self.minimax_basic(t, depth-1, not is_max, ai_player))
        return max(scores) if is_max else min(scores)

    def evaluate(self, board, player, is_solving):
        if is_solving:
            # Return stone difference
            return sum(row.count(player) for row in board) - sum(row.count(3-player) for row in board)
        # Positional evaluation
        score = 0
        for r in range(8):
            for c in range(8):
                if board[r][c] == player: score += POSITION_VALUES[r][c]
                elif board[r][c] == 3-player: score -= POSITION_VALUES[r][c]
        return score

    def apply_move(self, board, r, c, p):
        flippable = self.get_flippable(board, r, c, p)
        board[r][c] = p
        for fr, fc in flippable: board[fr][fc] = p

    def get_flippable(self, board, row, col, player):
        if board[row][col] != EMPTY: return []
        opp, stones = 3 - player, []
        for dr, dc in [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]:
            r, c, temp = row + dr, col + dc, []
            while 0 <= r < 8 and 0 <= c < 8 and board[r][c] == opp:
                temp.append((r, c))
                r, c = r + dr, c + dc
            if 0 <= r < 8 and 0 <= c < 8 and board[r][c] == player: stones.extend(temp)
        return stones

    def get_legal_moves(self, board, player):
        return [(r, c) for r in range(8) for c in range(8) if self.get_flippable(board, r, c, player)]

    def end_game(self):
        self.is_running = False
        b = sum(row.count(BLACK) for row in self.board)
        w = sum(row.count(WHITE) for row in self.board)
        msg = f"Black: {b}, White: {w}\n" + ("Black Wins!" if b > w else "White Wins!" if w > b else "Draw!")
        messagebox.showinfo("Result", msg)

if __name__ == "__main__":
    root = tk.Tk()
    app = OthelloLab(root)
    root.mainloop()