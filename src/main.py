import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD

def get_window_size():
    root = tk.Tk()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.destroy()
    return (width, height)


class MyApp(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()


        # ESC キーをバインド
        self.bind('<Escape>', lambda evnet: self.on_escape())

        # ウィンドウサイズ
        (max_width, max_height) = get_window_size()
        width = max_width // 2
        height = max_height // 2
        self.geometry(f'{width}x{height}')
        self.minsize(width, height)
        self.maxsize(max_width, max_height)
        self.title(f'AFU')

        # 列要素の拡張対応
        self.columnconfigure(index=0, weight=1)

        # 行要素の拡張対応
        self.rowconfigure(index=0, weight=1)
        self.rowconfigure(index=1, weight=1)
        self.rowconfigure(index=2, weight=0) # ボタン用のフレームを固定する

        ## Drag & Drop フレーム
        self.drag_and_drop_frames_f = frameDragAndDrop(self)
        self.drag_and_drop_frames_f.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

        self.drag_and_drop_frames_s = frameDragAndDrop(self)
        self.drag_and_drop_frames_s.grid(row=1, column=0, padx=5, pady=5, sticky='ew')

        # ボタンフレーム
        self.button_frame = tk.Frame(self)
        self.button_frame.grid(row=2, column=0, padx=0, pady=5)

        self.button_frame_left = tk.Button(self.button_frame, text="start", command=self.execute_start, width=20)
        self.button_frame_left.pack(side=tk.LEFT, padx=10)

        self.button_frame_right = tk.Button(self.button_frame, text="stop", command=self.execute_stop, width=20)
        self.button_frame_right.pack(side=tk.LEFT, padx=10)

    def execute_start(self):
        print("start")

    def execute_stop(self):
        print("stop")

    def on_escape(self):
        self.quit()

class frameDragAndDrop(tk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.textbox = tk.Text(self)
        self.textbox.insert(0.0, "Drag and Drop File.")
        self.textbox.configure(state='disabled')

        ## ドラッグアンドドロップ
        self.textbox.drop_target_register(DND_FILES)
        self.textbox.dnd_bind('<<Drop>>', self.funcDragAndDrop)

        ## スクロールバー設定
        self.scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.textbox.yview)
        self.textbox['yscrollcommand'] = self.scrollbar.set

        ## 配置
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.textbox.grid(row=0, column=0, sticky='ewns')
        self.scrollbar.grid(row=0, column=1, sticky='ewns')

    def funcDragAndDrop(self, e):
        ## ここを編集してください
        self.textbox.config(state="normal")
        self.textbox.delete("1.0", tk.END)
        self.textbox.insert(tk.END, e.data)
        self.textbox.configure(state="disabled")

if __name__ == "__main__":
    app = MyApp()
    app.mainloop()

