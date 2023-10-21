import tkinter as tk
import json
import tkinter.messagebox as messagebox 
with open("data.json" ,"r") as f:
    ranking_data = json.load(f)
large_font = ("Helvetica", 20)  # 大きなフォントを定義

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

def delete_by_name():
    name_to_delete = delete_entry.get()
    check = False
    ret = messagebox.askyesno('確認', '削除を実行しますか？')
    if ret:
        for i, (_, _, text) in enumerate(ranking_data):
            if text == name_to_delete:
                del ranking_data[i]
                check = True
                break
        if check:
            with open("data.json", "w") as f:
                json.dump(ranking_data, f, indent=2)
                delete_entry.delete(0, 'end')
                messagebox.showinfo('情報', f'名前: {name_to_delete}\n削除しました。')
        else:
            messagebox.showerror('エラー',f"名前: {name_to_delete}\n見つかりませんでした。")

# ランキングを更新する関数
def update_ranking(event=None):  # エンターキーを受け付けるために event=None を追加
    checkmessage = ""
    # スコアとテキストを取得
    check = True
    if score_entry.get() and text_entry.get():
        try:
            new_score = int(score_entry.get())
        except:
            checkmessage = "スコアは自然数を入力してください。"
            check = False
        new_text = text_entry.get()
        # 同じテキストがすでに存在するかチェック
        if check:
            for i, (_, score, text) in enumerate(ranking_data):
                if text == new_text:
                    # 同じテキストが見つかった場合、スコアを更新
                    ranking_data[i] = (i + 1, new_score, new_text)
                    checkmessage = f"スコア: {new_score} 名前: {new_text} 値を更新しました。"
                    break
            else:
                # 同じテキストが見つからなかった場合、新しいエントリを追加
                ranking_data.append((len(ranking_data) + 1, new_score, new_text))
                checkmessage = f"スコア: {new_score} 名前: {new_text} 値を追加しました。"

            sorted_list = sorted(ranking_data, key=lambda x: x[1], reverse=True)

                # 1番目の要素（index 0）を再度振り直す
            reordered_list = [[i+1, item[1], item[2]] for i, item in enumerate(sorted_list)]    
            with open("data.json", "w") as f:
                json.dump(reordered_list,f,indent=2)

                # スコアでソート
            ranking_data.sort(key=lambda x: x[1], reverse=True)

                # ランキング表示をクリア
            for widget in ranking_frame.winfo_children():
                widget.destroy()
            score_entry.delete(0, 'end')
            text_entry.delete(0, 'end')            
    else:
        checkmessage = "入力されていません"
    if check:
        messagebox.showinfo('情報', checkmessage)
    else:
        messagebox.showerror('エラー', checkmessage)
# Tkinterウィンドウを作成
root = tk.Tk()
root.title("ランキング編集 管理者専用")

# 入力フレーム
input_frame = tk.Frame(root)
input_frame.pack(pady=10)
label_score = tk.Label(input_frame, text="スコア:", font=large_font)  # 大きなフォントを適用
score_entry = tk.Entry(input_frame, font=large_font)  # 大きなフォントを適用
label_text = tk.Label(input_frame, text="名前:", font=large_font)  # 大きなフォントを適用
text_entry = tk.Entry(input_frame, font=large_font)  # 大きなフォントを適用

# Enterキーでランキングを更新するイベントを設定
score_entry.bind('<Return>', update_ranking)
text_entry.bind('<Return>', update_ranking)

update_button = tk.Button(input_frame, text="ランキング更新", command=update_ranking, font=large_font)  # 大きなフォントを適用
label_score.grid(row=0, column=0)
score_entry.grid(row=0, column=1)
label_text.grid(row=0, column=2)
text_entry.grid(row=0, column=3)
update_button.grid(row=0, column=4)

# 削除フレーム
delete_frame = tk.Frame(root)
delete_frame.pack(pady=10)
label_delete = tk.Label(delete_frame, text="削除する名前:", font=large_font)  # 大きなフォントを適用
delete_entry = tk.Entry(delete_frame, font=large_font)  # 大きなフォントを適用
delete_button = tk.Button(delete_frame, text="名前削除", command=delete_by_name, font=large_font)  # 大きなフォントを適用
label_delete.grid(row=0, column=0)
delete_entry.grid(row=0, column=1)
delete_button.grid(row=0, column=2)

# ランキングフレーム
ranking_frame = tk.Frame(root)
ranking_frame.pack(pady=30)

root.protocol("WM_DELETE_WINDOW", close_window)  # ウィンドウの閉じるボタンが押されたときにclose_windowを呼び出す

root.mainloop()