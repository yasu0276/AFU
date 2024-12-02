import tkinter as tk
import simpleaudio as sa
from tkinterdnd2 import DND_FILES, TkinterDnD
from dataclasses import dataclass

def get_window_size():
    root = tk.Tk()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.destroy()
    return (width, height)

@dataclass(slots=True)
class FrameUtils():
    max_width: int = get_window_size()[0]
    max_height: int = get_window_size()[1]
    width: int = max_width // 2
    height: int = max_height // 2
    title: str = "AFU"
    button_frame: tk.Frame = None
    button_start: tk.Button = None
    button_stop: tk.Button = None

class AFU(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()

        # ESC キーをバインド
        self.bind('<Escape>', lambda evnet: self.on_escape())

        # Window クラスをインスタンス
        self.window_utils = FrameUtils()

        # ウィンドウサイズ
        self.geometry(f'{self.window_utils.width}x{self.window_utils.height}')
        self.minsize(self.window_utils.width, self.window_utils.height)
        self.maxsize(self.window_utils.max_width, self.window_utils.max_height)
        self.title(self.window_utils.title)

        # 列要素の拡張対応
        self.columnconfigure(index=0, weight=0) # ボタンのフレームは固定
        self.columnconfigure(index=1, weight=1)

        ## Drag & Drop フレーム
        self.drag_and_drop_frame = DragAndDropUtil(self)
        self.drag_and_drop_frame.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        # ボタンフレーム
        self.window_utils.button_frame = tk.Frame(self)
        self.window_utils.button_frame.grid(row=0, column=0, padx=0, pady=5)

        self.window_utils.button_start = tk.Button(self.window_utils.button_frame, text="start", command=lambda: self.execute_start(self.drag_and_drop_frame.get_file_path()), width=20)
        self.window_utils.button_start.pack(side=tk.TOP, padx=10)

        self.window_utils.button_stop = tk.Button(self.window_utils.button_frame, text="stop", command=self.execute_stop, width=20)
        self.window_utils.button_stop.pack(side=tk.TOP, padx=10)

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

    def execute_start(self, file_path_):
        file_path = file_path_
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

