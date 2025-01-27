from __future__ import annotations
import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image, ImageTk
from tkinter import PhotoImage
from tkinter import filedialog

class DragAndDropUtil(tk.LabelFrame):
    def __init__(self, parent, width=50, height=50):
        super().__init__(parent)
        self.textbox = tk.Text(self, width=width, height=height)
        self.__width = width
        self.__height = height
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

        # 親クラスにドラッグ＆ドロップされたファイルを通知するために記録しておく
        self.parent = parent

        # ファイルパス記憶変数
        self.file_path = None
        self.__file_path = None

    def execute_drag_and_drop(self, e) -> None:
        # ファイルパスを記録
        self.file_path = e.data
        # ドラッグ＆ドロップした後にフォーカスが外れるので強制フォーカス
        self.focus_force()

    def write_content(self, content: str) -> None:
        self.textbox.config(state="normal")
        self.textbox.delete("1.0", tk.END)
        self.textbox.insert(tk.END, content)
        self.textbox.configure(state="disabled")

    def write_image(self, image: PhotoImage) -> None:
        self.textbox.config(state="normal")
        self.textbox.delete("1.0", tk.END)
        self.textbox.insert("1.0", "\n")
        self.textbox.image_create("1.0", image=image)
        self.textbox.configure(state="disabled")

    @property
    def file_path(self) -> str:
        return self.__file_path

    @file_path.setter
    def file_path(self, file_path):
        self.__file_path = file_path
        if self.parent:
            self.parent.notify(self, self.__file_path)

    @property
    def width(self) -> int:
        return self.__width

    @property
    def height(self) -> int:
        return self.__height