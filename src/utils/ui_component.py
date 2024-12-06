from __future__ import annotations
import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD

class DragAndDropUtil(tk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.textbox = tk.Text(self)
        self.textbox.insert(0.0, "Drag and Drop File.")
        self.textbox.configure(state='disabled')

        ## ドラッグアンドドロップ
        self.textbox.drop_target_register(DND_FILES)
        self.textbox.dnd_bind('<<Drop>>', self.execute_drag_and_drop)

        ## スクロールバー設定
        self.scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.textbox.yview)
        self.textbox['yscrollcommand'] = self.scrollbar.set

        ## 配置
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.textbox.grid(row=0, column=0, sticky='ewns')
        self.scrollbar.grid(row=0, column=1, sticky='ewns')

        # ファイルパス記憶変数
        self.file_path = None

    def execute_drag_and_drop(self, e) -> None:
        ## ここを編集してください
        self.textbox.config(state="normal")
        self.textbox.delete("1.0", tk.END)
        self.textbox.insert(tk.END, e.data)
        self.textbox.configure(state="disabled")
        self.file_path = e.data
        # ドラッグ＆ドロップした後にフォーカスが外れるので強制フォーカス
        self.focus_force()

    def get_file_path(self) -> str :
        return (self.file_path)
