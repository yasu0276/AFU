from __future__ import annotations
import tkinter as tk
import simpleaudio as sa
from tkinterdnd2 import DND_FILES, TkinterDnD
from dataclasses import dataclass
from collections import deque

def get_window_size():
    root = tk.Tk()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.destroy()
    return (width, height)

@dataclass(slots=True)
class FrameObj():
    max_width: int = get_window_size()[0]
    max_height: int = get_window_size()[1]
    width: int = max_width // 2
    height: int = max_height // 2
    title: str = "AFU"
    button: tk.Frame = None
    button_start: tk.Button = None
    button_stop: tk.Button = None
    drag_and_drop: DragAndDropUtil = None

@dataclass(slots=True)
class AudioObj():
    wave_obj: sa.WaveObject = None
    play_obj_que: deque = deque()

class AFU(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()

        # ESC キーをバインド
        self.bind('<Escape>', lambda evnet: self.on_escape())

        # クラスをインスタンス
        self.frame_top = FrameObj()
        self.wave_top = AudioObj()
        self.frame_bottom = FrameObj()
        self.wave_bottom = AudioObj()

        # ウィンドウサイズ
        self.geometry(f'{self.frame_top.width}x{self.frame_top.height}')
        self.minsize(self.frame_top.width, self.frame_top.height)
        self.maxsize(self.frame_top.max_width, self.frame_top.max_height)
        self.title(self.frame_top.title)

        # 列要素の拡張対応
        self.columnconfigure(index=0, weight=0) # ボタンのフレームは固定
        self.columnconfigure(index=1, weight=1)

        # 行要素の拡張対応
        self.rowconfigure(index=0, weight=1)
        self.rowconfigure(index=1, weight=1)

        # Drag & Drop フレーム
        self.frame_top.drag_and_drop = DragAndDropUtil(self)
        self.frame_top.drag_and_drop.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        self.frame_bottom.drag_and_drop = DragAndDropUtil(self)
        self.frame_bottom.drag_and_drop.grid(row=1, column=1, padx=5, pady=5, sticky='ew')

        # ボタンフレーム
        self.frame_top.button = tk.Frame(self)
        self.frame_top.button.grid(row=0, column=0, padx=0, pady=5)

        self.frame_top.button_start = tk.Button(self.frame_top.button, text="start", command=lambda: self.execute_start(self.frame_top, self.wave_top), width=20)
        self.frame_top.button_start.pack(side=tk.TOP, padx=10)

        self.frame_top.button_stop = tk.Button(self.frame_top.button, text="stop", command=lambda: self.execute_stop(self.wave_top), width=20)
        self.frame_top.button_stop.pack(side=tk.TOP, padx=10)

        self.frame_bottom.button = tk.Frame(self)
        self.frame_bottom.button.grid(row=1, column=0, padx=0, pady=5)

        self.frame_bottom.button_start = tk.Button(self.frame_bottom.button, text="start", command=lambda: self.execute_start(self.frame_bottom, self.wave_bottom), width=20)
        self.frame_bottom.button_start.pack(side=tk.TOP, padx=10)

        self.frame_bottom.button_stop = tk.Button(self.frame_bottom.button, text="stop", command=lambda: self.execute_stop(self.wave_bottom), width=20)
        self.frame_bottom.button_stop.pack(side=tk.TOP, padx=10)

    def execute_start(self, frame_obj: FrameObj, audio_obj: AudioObj):
        file_path = frame_obj.drag_and_drop.get_file_path()
        if file_path is not None:
            audio_obj.wave_obj = sa.WaveObject.from_wave_file(file_path)
            play_obj = audio_obj.wave_obj.play()
            audio_obj.play_obj_que.append(play_obj)

    def execute_stop(self, audio_obj: AudioObj):
        play_obj = audio_obj.play_obj_que.popleft()
        if play_obj.is_playing():
            play_obj.stop()

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

