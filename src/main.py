import tkinter as tk
import simpleaudio as sa
from tkinterdnd2 import DND_FILES, TkinterDnD

def get_window_size():
    root = tk.Tk()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.destroy()
    return (width, height)

class AFU(TkinterDnD.Tk):
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
        self.columnconfigure(index=0, weight=0) # ボタンのフレームは固定
        self.columnconfigure(index=1, weight=1)

        # ボタンフレーム
        self.button_frame_top = tk.Frame(self)
        self.button_frame_top.grid(row=0, column=0, padx=0, pady=5)

        self.button_frame_top_start = tk.Button(self.button_frame_top, text="start", command=self.execute_start, width=20)
        self.button_frame_top_start.pack(side=tk.TOP, padx=10)

        self.button_frame_top_stop = tk.Button(self.button_frame_top, text="stop", command=self.execute_stop, width=20)
        self.button_frame_top_stop.pack(side=tk.TOP, padx=10)

        ## Drag & Drop フレーム
        self.drag_and_drop_frames_top = DragAndDropUtil(self)
        self.drag_and_drop_frames_top.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        # ボタンフレーム
#        self.button_frame_bottom = tk.Frame(self)
#        self.button_frame_bottom.grid(row=1, column=0, padx=0, pady=5)
#
#        self.button_frame_left = tk.Button(self.button_frame_bottom, text="start", command=self.execute_start, width=20)
#        self.button_frame_left.pack(side=tk.TOP, padx=10)
#
#        self.button_frame_right = tk.Button(self.button_frame_bottom, text="stop", command=self.execute_stop, width=20)
#        self.button_frame_right.pack(side=tk.TOP, padx=10)
#
#        ## Drag & Drop フレーム
#        self.drag_and_drop_frames_bottom = DragAndDropUtil(self)
#        self.drag_and_drop_frames_bottom.grid(row=1, column=1, padx=5, pady=5, sticky='ew')

    def execute_start(self):
        file_path = self.drag_and_drop_frames_top.get_file_path()
        if file_path is not None:
            self.wave_obj = sa.WaveObject.from_wave_file(file_path)
            self.play_obj = self.wave_obj.play()

    def execute_stop(self):
        if self.play_obj.is_playing():
            self.play_obj.stop()

    def on_escape(self):
        self.quit()

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

    def get_file_path(self) -> str :
        return (self.file_path)

if __name__ == "__main__":
    app = AFU()
    app.mainloop()

