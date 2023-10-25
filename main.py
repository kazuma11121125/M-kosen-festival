import tkinter as tk
import json
import threading
global ranking_data_1
import time
import tkinter.messagebox as messagebox 

ranking_data_1 = ""
# フォント設定
large_font = ("Helvetica", 20)  # 大きなフォントを定義
score_font = ("Helvetica", 40)  # スコア表示のフォントサイズを2倍に定義

def close_window():
    # 最初の確認を表示
    ret = messagebox.askyesno('確認', 'ウィンドウを閉じますか？')
    if ret:
        # ユーザーがはいを選択した場合、もう一度確認
        ret = messagebox.askyesno('確認', '本当にウィンドウを閉じますか？')
        if ret:
            # ユーザーが再度はいを選択した場合、ウィンドウを閉じる
            ret = messagebox.askyesno('確認', '本当の本当にウィンドウを閉じますか？')
            if ret:
                root.destroy()
#当日閉じられにくいようにする。kazumaの仕事削減(ここ重要)

def show():
    global ranking_data_1
    ch = True
    try:
        with open("data.json", "r") as f:
            ranking_data = json.load(f)
    except json.decoder.JSONDecodeError:
        ch = False
        ranking_data = ranking_data_1
    if ch:
        if ranking_data != ranking_data_1:
            for widget in ranking_frame.winfo_children():
                widget.destroy()
            label_ranking = tk.Label(ranking_frame, text="〜Ranking〜", font=score_font)  # 大きなフォントを適用
            label_ranking.grid(row=0, column=0, columnspan=3, pady=(15, 20), padx=40)  # 横方向と縦方向のスペースを確保
            label_rank = tk.Label(ranking_frame, text="Rank", font=score_font)  # 大きなフォントを適用
            label_rank.grid(row=1, column=0, pady=(15, 10), padx=30)  # 横方向と縦方向のスペースを確保
            label_score = tk.Label(ranking_frame, text="Score", font=score_font)  # 大きなフォントを適用
            label_score.grid(row=1, column=1, pady=(15, 10), padx=30)  # 横方向と縦方向のスペースを確保
            label_text = tk.Label(ranking_frame, text="Name", font=score_font)  # 大きなフォントを適用
            label_text.grid(row=1, column=2, pady=(15, 10), padx=30)  # 横方向と縦方向のスペースを確保
            # 初期ランキングを表示（上位6位まで）
            for i, (rank, score, text) in enumerate(ranking_data[:6]):
                label_rank = tk.Label(ranking_frame, text=f"{i + 1}位", font=score_font)  # 大きなフォントを適用
                label_rank.grid(row=i + 2, column=0, pady=10, padx=40)  # 横方向と縦方向のスペースを確保
                label_score = tk.Label(ranking_frame, text=score, font=score_font)  # スコア表示のフォントサイズを2倍に適用
                label_score.grid(row=i + 2, column=1, pady=10, padx=40)  # 横方向と縦方向のスペースを確保
                label_text = tk.Label(ranking_frame, text=text, font=score_font)  # 大きなフォントを適用
                label_text.grid(row=i + 2, column=2, pady=10, padx=40)  # 横方向と縦方向のスペースを確保
            ranking_data_1 = ranking_data
    
# Tkinterウィンドウを作成
root = tk.Tk()
root.title("ランキング")

# ウィンドウを最大化（全画面表示）
root.attributes('-zoomed', True)

# ランキングフレーム
ranking_frame = tk.Frame(root)
ranking_frame.pack(pady=30)

def kousin():
    while True:
        show()
        time.sleep(1)
thread1 = threading.Thread(target=kousin, daemon=True)
thread1.start()

def on_closing():
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.protocol("WM_DELETE_WINDOW", close_window)  # ウィンドウの閉じるボタンが押されたときにclose_windowを呼び出す

root.mainloop()
