import tkinter as tk
from tkinter import messagebox
import random
import time

# --- 資料格式 (依圖片需求設定) ---
WORD_BANKS = {
    "Normal": ["apple", "banana", "keyboard", "window", "happy", "cherry", "python"],
    "Hard": ["binary search", "linked list", "cloud storage", "artificial intelligence"],
    "Nightmare": [
        "Practice makes perfect.",
        "Accuracy is more important than speed.",
        "Keep calm and carry on typing."
    ]
}

TIME_LIMITS = {
    "Normal": 10,
    "Hard": 10,
    "Nightmare": 15
}

class TypingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Speed Typing Challenge")
        self.root.geometry("600x500")
        self.root.configure(bg="#2c3e50")

        # 遊戲變數
        self.difficulty = tk.StringVar(value="Normal")
        self.total_rounds = tk.IntVar(value=5)
        self.current_round = 0
        self.score = 0
        self.start_time = 0
        self.total_chars_typed = 0
        self.timer_running = False
        self.remaining_time = 0

        self.setup_ui()

    def setup_ui(self):
        # 標題
        tk.Label(self.root, text="Speed Typing Challenge", font=("Arial", 24, "bold"), 
                 fg="white", bg="#2c3e50").pack(pady=20)

        # 設定區 (回合數與難度)
        setting_frame = tk.Frame(self.root, bg="#2c3e50")
        setting_frame.pack()

        tk.Label(setting_frame, text="Rounds:", fg="white", bg="#2c3e50").grid(row=0, column=0)
        self.round_entry = tk.Entry(setting_frame, textvariable=self.total_rounds, width=5)
        self.round_entry.grid(row=0, column=1, padx=10)

        diff_frame = tk.Frame(self.root, bg="#2c3e50")
        diff_frame.pack(pady=10)
        for diff in WORD_BANKS.keys():
            tk.Radiobutton(diff_frame, text=diff, variable=self.difficulty, value=diff,
                           indicatoron=0, width=10, selectcolor="#34495e").pack(side=tk.LEFT, padx=5)

        # 開始按鈕
        self.start_btn = tk.Button(self.root, text="Start Game", command=self.start_game,
                                   font=("Arial", 12), bg="#ecf0f1")
        self.start_btn.pack(pady=10)

        # 題目顯示區
        self.target_label = tk.Label(self.root, text="---", font=("Courier", 20, "bold"), 
                                     fg="#2ecc71", bg="#2c3e50")
        self.target_label.pack(pady=20)

        # 剩餘時間顯示
        self.time_label = tk.Label(self.root, text="Time: 0.0s", fg="white", bg="#2c3e50")
        self.time_label.pack()

        # 輸入框
        self.input_entry = tk.Entry(self.root, font=("Arial", 14), width=30, justify='center')
        self.input_entry.pack(pady=10)
        self.input_entry.bind("<KeyRelease>", self.check_realtime_color)
        self.input_entry.bind("<Return>", self.submit_answer)
        self.input_entry.config(state=tk.DISABLED)

        # 成績與 WPM 顯示區 (隱藏)
        self.result_label = tk.Label(self.root, text="", fg="#f1c40f", bg="#2c3e50", font=("Arial", 12))
        self.result_label.pack(pady=10)

    def start_game(self):
        self.current_round = 0
        self.score = 0
        self.total_chars_typed = 0
        self.start_time = time.time()
        self.result_label.config(text="")
        self.start_btn.config(state=tk.DISABLED)
        self.round_entry.config(state=tk.DISABLED)
        self.input_entry.config(state=tk.NORMAL)
        self.next_round()

    def next_round(self):
        if self.current_round < self.total_rounds.get():
            self.current_round += 1
            self.current_word = random.choice(WORD_BANKS[self.difficulty.get()])
            self.target_label.config(text=self.current_word, fg="#2ecc71")
            self.input_entry.delete(0, tk.END)
            self.input_entry.focus()
            
            # 設定倒數計時
            self.remaining_time = TIME_LIMITS[self.difficulty.get()]
            self.update_timer()
        else:
            self.end_game()

    def update_timer(self):
        if self.remaining_time > 0:
            self.time_label.config(text=f"Time: {round(self.remaining_time, 1)}s")
            self.remaining_time -= 0.1
            self.timer_job = self.root.after(100, self.update_timer)
        else:
            self.submit_answer(None) # 時間到自動提交

    def check_realtime_color(self, event):
        # 逐字顏色回饋
        typed = self.input_entry.get()
        if self.current_word.startswith(typed):
            self.input_entry.config(fg="black") # 正確時保持原色或綠色
        else:
            self.input_entry.config(fg="red") # 錯誤時變紅

    def submit_answer(self, event):
        # 取消計時器
        if hasattr(self, 'timer_job'):
            self.root.after_cancel(self.timer_job)

        typed = self.input_entry.get().strip()
        if typed == self.current_word:
            self.score += 1
            self.total_chars_typed += len(typed)
        
        self.next_round()

    def end_game(self):
        self.target_label.config(text="Game Over", fg="white")
        self.input_entry.config(state=tk.DISABLED)
        self.start_btn.config(state=tk.NORMAL)
        self.round_entry.config(state=tk.NORMAL)

        # 計算 WPM (Words Per Minute)
        # 邏輯：(總打字字數 / 5) / 分鐘數
        total_time_minutes = (time.time() - self.start_time) / 60
        wpm = round((self.total_chars_typed / 5) / total_time_minutes) if total_time_minutes > 0 else 0
        
        accuracy = int((self.score / self.total_rounds.get()) * 100)
        
        result_text = f"Final Score: {self.score}/{self.total_rounds.get()} ({accuracy}%)\nWPM: {wpm}"
        self.result_label.config(text=result_text)

if __name__ == "__main__":
    root = tk.Tk()
    game = TypingGame(root)
    root.mainloop()
