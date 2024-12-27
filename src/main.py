from utils import *

class AFU(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()

        # ウインドウに強制フォーカス
        self.focus_force()

        # ESC キーをバインド
        self.bind('<Escape>', lambda evnet: self.on_escape())

        # space キーをバインド
        self.bind('<space>', lambda evnet: self.on_all_start())

        # Shift + space キーをバインド
        self.bind('<Shift-space>', lambda evnet: self.on_all_stop())

        # クラスをインスタンス
        self.frame_top = FrameObj()
        self.audio_top = AudioObj()
        self.frame_bottom = FrameObj()
        self.audio_bottom = AudioObj()

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

        self.frame_top.button_start = tk.Button(self.frame_top.button, text="start", command=lambda: self.execute_start(self.frame_top, self.audio_top), width=20)
        self.frame_top.button_start.pack(side=tk.TOP, padx=10)

        self.frame_top.button_stop = tk.Button(self.frame_top.button, text="stop", command=lambda: self.execute_stop(self.audio_top), width=20)
        self.frame_top.button_stop.pack(side=tk.TOP, padx=10)

        self.frame_bottom.button = tk.Frame(self)
        self.frame_bottom.button.grid(row=1, column=0, padx=0, pady=5)

        self.frame_bottom.button_start = tk.Button(self.frame_bottom.button, text="start", command=lambda: self.execute_start(self.frame_bottom, self.audio_bottom), width=20)
        self.frame_bottom.button_start.pack(side=tk.TOP, padx=10)

        self.frame_bottom.button_stop = tk.Button(self.frame_bottom.button, text="stop", command=lambda: self.execute_stop(self.audio_bottom), width=20)
        self.frame_bottom.button_stop.pack(side=tk.TOP, padx=10)

    def execute_start(self, frame_obj: FrameObj, audio_obj: AudioObj):
        file_path = frame_obj.drag_and_drop.get_file_path()
        if file_path is not None:
            audio_obj.wave_obj = wave.open(file_path, 'rb')
            audio_frame = audio_obj.wave_obj.readframes(audio_obj.wave_obj.getnframes())
            audio_data = np.frombuffer(audio_frame, dtype=np.int16)
            play_obj = sa.play_buffer(
                audio_data.tobytes(),
                num_channels=audio_obj.wave_obj.getnchannels(),
                bytes_per_sample=audio_obj.wave_obj.getsampwidth(),
                sample_rate=audio_obj.wave_obj.getframerate()
            )
            audio_obj.play_obj_que.append(play_obj)

    def execute_stop(self, audio_obj: AudioObj):
        play_obj = audio_obj.play_obj_que.popleft()
        if play_obj.is_playing():
            play_obj.stop()

    def on_escape(self):
        self.quit()

    def on_all_start(self):
        self.execute_start(self.frame_top, self.audio_top)
        self.execute_start(self.frame_bottom, self.audio_bottom)

    def on_all_stop(self):
        self.execute_stop(self.audio_top)
        self.execute_stop(self.audio_bottom)

if __name__ == "__main__":
    app = AFU()
    app.mainloop()

