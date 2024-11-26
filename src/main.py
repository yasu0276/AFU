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

        # Main フレーム
        self.main_frame = tk.Frame()
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.main_frame.columnconfigure(index=0, weight=1)
        self.main_frame.columnconfigure(index=1, weight=1)
        self.main_frame.rowconfigure(index=0, weight=1)
        self.main_frame.rowconfigure(index=1, weight=1)
        self.main_frame.rowconfigure(index=2, weight=1)

        # ウィンドウサイズ
        (max_width, max_height) = get_window_size()
        width = max_width // 2
        height = max_height // 2
        self.geometry(f'{width}x{height}')
        self.minsize(width, height)
        self.maxsize(max_width, max_height)
        self.title(f'AFU')

        ## Drag & Drop フレーム
        self.drag_and_drop_frames_f = frameDragAndDrop(self.main_frame)
        self.drag_and_drop_frames_f.grid(row=0, column=0, padx=5, pady=5, sticky=(tk.E, tk.W))
        self.rowconfigure(index=0, weight=1)
        self.columnconfigure(index=0, weight=1)

        self.drag_and_drop_frames_s = frameDragAndDrop(self.main_frame)
        self.drag_and_drop_frames_s.grid(row=1, column=0, padx=5, pady=5, sticky=(tk.E, tk.W))
        self.rowconfigure(index=1, weight=1)
        self.columnconfigure(index=0, weight=1)

        # ボタン用フレーム
        self.button_frame = tk.Frame(self.main_frame)
        self.button_frame.grid(row=2, column=0, padx=5, pady=5, sticky=(tk.E, tk.W))
        self.button_frame.columnconfigure(index=0, weight=1)
        self.button_frame.columnconfigure(index=1, weight=1)

        # ボタン作成
        self.button_start = tk.Button(self.button_frame, text="start", command=self.execute_start)
        self.button_stop = tk.Button(self.button_frame, text="stop", command=self.execute_stop)

        # 配置
        self.button_start.grid(row=0, column=0, padx=5, pady=5)
        self.button_stop.grid(row=0, column=1, padx=5, pady=5)

    def execute_start(self):
        print("start")

    def execute_stop(self):
        print("stop")

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
        self.textbox.grid(column=0, row=0, sticky=(tk.E, tk.W))
        self.scrollbar.grid(row=0, column=1, sticky=(tk.E, tk.W))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

    def funcDragAndDrop(self, e):
        ## ここを編集してください
        self.textbox.config(state="normal")
        self.textbox.delete("1.0", tk.END)
        self.textbox.insert(tk.END, e.data)
        self.textbox.configure(state="disabled")

if __name__ == "__main__":
    app = MyApp()
    app.mainloop()

