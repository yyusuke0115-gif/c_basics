import tkinter as tk
from tkinter import messagebox
import random
import math
import json
import os

# --- Neural Network Engine with Save/Load ---
class SimpleDeepMind:
    def __init__(self, input_size=64, hidden_size=32):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.w_input_hidden = [[random.uniform(-0.1, 0.1) for _ in range(hidden_size)] for _ in range(input_size)]
        self.w_hidden_output = [random.uniform(-0.1, 0.1) for _ in range(hidden_size)]
        self.learning_rate = 0.01

    def sigmoid(self, x):
        return 1 / (1 + math.exp(-max(min(x, 50), -50)))

    def sigmoid_derivative(self, x):
        return x * (1 - x)

    def predict(self, inputs):
        hidden = [0.0] * self.hidden_size
        for j in range(self.hidden_size):
            sum_val = sum(inputs[i] * self.w_input_hidden[i][j] for i in range(self.input_size))
            hidden[j] = self.sigmoid(sum_val)
        output = sum(hidden[k] * self.w_hidden_output[k] for k in range(self.hidden_size))
        return self.sigmoid(output), hidden

    def train(self, inputs, target):
        prediction, hidden = self.predict(inputs)
        output_error = target - prediction
        output_delta = output_error * self.sigmoid_derivative(prediction)
        
        hidden_deltas = [0.0] * self.hidden_size
        for j in range(self.hidden_size):
            error = output_delta * self.w_hidden_output[j]
            hidden_deltas[j] = error * self.sigmoid_derivative(hidden[j])
            
        for j in range(self.hidden_size):
            self.w_hidden_output[j] += self.learning_rate * output_delta * hidden[j]
            for i in range(self.input_size):
                self.w_input_hidden[i][j] += self.learning_rate * hidden_deltas[j] * inputs[i]

    # 重みデータを保存
    def save_brain(self, filename="brain_data.json"):
        data = {
            "w_ih": self.w_input_hidden,
            "w_ho": self.w_hidden_output
        }
        with open(filename, "w") as f:
            json.dump(data, f)
        print(f"Brain saved to {filename}")

    # 重みデータを読み込み
    def load_brain(self, filename="brain_data.json"):
        if os.path.exists(filename):
            with open(filename, "r") as f:
                data = json.load(f)
            self.w_input_hidden = data["w_ih"]
            self.w_hidden_output = data["w_ho"]
            print(f"Brain loaded from {filename}")
            return True
        return False

# --- Othello GUI with Control ---
class OthelloDeepMindGUI:
    def __init__(self, master):
        self.master = master
        self.nn = SimpleDeepMind()
        self.nn.load_brain() # 起動時に自動ロード
        self.setup_ui()
        self.reset_game()
        self.is_training = False
        self.match_count = 0

    def setup_ui(self):
        self.master.title("Othello DeepMind - Brain Saver")
        
        control = tk.Frame(self.master)
        control.pack(pady=10)
        
        self.train_btn = tk.Button(control, text="Start Learning", command=self.toggle_training)
        self.train_btn.pack(side=tk.LEFT, padx=5)
        
        self.save_btn = tk.Button(control, text="Save Brain", command=self.nn.save_brain)
        self.save_btn.pack(side=tk.LEFT, padx=5)

        self.info = tk.Label(self.master, text="Matches: 0")
        self.info.pack()

        self.canvas = tk.Canvas(self.master, width=400, height=400, bg="#1a3d1a")
        self.canvas.pack()

    def toggle_training(self):
        self.is_training = not self.is_training
        self.train_btn.config(text="Stop" if self.is_training else "Start Learning")
        if self.is_training: self.run_match()

    def reset_game(self):
        self.board = [0] * 64
        self.board[27], self.board[36], self.board[28], self.board[35] = -1, -1, 1, 1
        self.current_p = 1
        self.history = []

    def run_match(self):
        if not self.is_training: return
        
        moves = self.get_moves(self.current_p)
        if moves:
            best_move = self.choose_move(moves, self.current_p)
            self.history.append((self.board_to_input(self.current_p), best_move))
            self.make_move(best_move, self.current_p)
        
        self.current_p *= -1
        if not self.get_moves(1) and not self.get_moves(-1):
            self.learn()
            self.match_count += 1
            self.info.config(text=f"Matches: {self.match_count}")
            self.draw_board()
            self.reset_game()
            # 100試合ごとに自動保存（オプション）
            if self.match_count % 100 == 0: self.nn.save_brain()
            self.master.after(5, self.run_match)
        else:
            self.master.after(5, self.run_match)

    def choose_move(self, moves, player):
        if random.random() < 0.1: return random.choice(moves)
        best_val, best_m = -1.0, moves[0]
        for m in moves:
            # 簡易評価（本来は置いた後の盤面で評価すべきですが、学習の高速化のため現在の入力で予測）
            val, _ = self.nn.predict(self.board_to_input(player))
            if val > best_val:
                best_val, best_m = val, m
        return best_m

    def learn(self):
        b_c = self.board.count(1)
        w_c = self.board.count(-1)
        winner = 1 if b_c > w_c else (-1 if w_c > b_c else 0)
        for state, _ in self.history:
            target = 1.0 if winner != 0 else 0.5
            self.nn.train(state, target)

    def board_to_input(self, p): return [cell * p for cell in self.board]

    # --- Standard Logic (Same as before) ---
    def get_moves(self, p):
        return [i for i in range(64) if self.board[i] == 0 and self.can_flip(i, p)]

    def can_flip(self, pos, p):
        r, c = pos // 8, pos % 8
        for dr, dc in [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]:
            tr, tc, count = r+dr, c+dc, 0
            while 0 <= tr < 8 and 0 <= tc < 8 and self.board[tr*8+tc] == -p:
                tr, tc, count = tr+dr, tc+dc, count+1
            if count > 0 and 0 <= tr < 8 and 0 <= tc < 8 and self.board[tr*8+tc] == p: return True
        return False

    def make_move(self, pos, p):
        self.board[pos] = p
        r, c = pos // 8, pos % 8
        for dr, dc in [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]:
            tr, tc, temp = r+dr, c+dc, []
            while 0 <= tr < 8 and 0 <= tc < 8 and self.board[tr*8+tc] == -p:
                temp.append(tr*8+tc)
                tr, tc = tr+dr, tc+dc
            if temp and 0 <= tr < 8 and 0 <= tc < 8 and self.board[tr*8+tc] == p:
                for idx in temp: self.board[idx] = p

    def draw_board(self):
        self.canvas.delete("all")
        for i in range(64):
            x, y = (i % 8) * 50, (i // 8) * 50
            self.canvas.create_rectangle(x, y, x+50, y+50, outline="#333")
            if self.board[i] != 0:
                color = "black" if self.board[i] == 1 else "white"
                self.canvas.create_oval(x+5, y+5, x+45, y+45, fill=color)

if __name__ == "__main__":
    root = tk.Tk()
    app = OthelloDeepMindGUI(root)
    root.mainloop()