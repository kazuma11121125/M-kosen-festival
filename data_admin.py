import tkinter as tk
import json


with open("data.json" ,"r") as f:
    ranking_data = json.load(f)
large_font = ("Helvetica", 20)  # 大きなフォントを定義


def delete_by_name():
    name_to_delete = delete_entry.get()
    for i, (_, _, text) in enumerate(ranking_data):
        if text == name_to_delete:
            del ranking_data[i]
            break
    with open("data.json", "w") as f:
        json.dump(ranking_data, f, indent=2)
    delete_entry.delete(0, 'end')

# ランキングを更新する関数
def update_ranking(event=None):  # エンターキーを受け付けるために event=None を追加
    # スコアとテキストを取得
    new_score = int(score_entry.get())
    new_text = text_entry.get()

    # 同じテキストがすでに存在するかチェック
    for i, (_, score, text) in enumerate(ranking_data):
        if text == new_text:
            # 同じテキストが見つかった場合、スコアを更新
            ranking_data[i] = (i + 1, new_score, new_text)
            break
    else:
        # 同じテキストが見つからなかった場合、新しいエントリを追加
        ranking_data.append((len(ranking_data) + 1, new_score, new_text))

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

root.mainloop()