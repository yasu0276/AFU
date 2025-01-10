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

        self.frame_top.button_to_txt = tk.Button(self.frame_top.button, text="to txt", command=lambda: self.to_txt(self.frame_top, self.audio_top), width=20)
        self.frame_top.button_to_txt.pack(side=tk.TOP, padx=10)

        self.frame_top.button_stop.pack(side=tk.TOP, padx=10)
        self.frame_bottom.button = tk.Frame(self)
        self.frame_bottom.button.grid(row=1, column=0, padx=0, pady=5)

        self.frame_bottom.button_start = tk.Button(self.frame_bottom.button, text="start", command=lambda: self.execute_start(self.frame_bottom, self.audio_bottom), width=20)
        self.frame_bottom.button_start.pack(side=tk.TOP, padx=10)

        self.frame_bottom.button_stop = tk.Button(self.frame_bottom.button, text="stop", command=lambda: self.execute_stop(self.audio_bottom), width=20)
        self.frame_bottom.button_stop.pack(side=tk.TOP, padx=10)

        self.frame_bottom.button_to_txt = tk.Button(self.frame_bottom.button, text="to txt", command=lambda: self.to_txt(self.frame_bottom, self.audio_bottom), width=20)
        self.frame_bottom.button_to_txt.pack(side=tk.TOP, padx=10)

    def execute_start(self, frame_obj: FrameObj, audio_obj: AudioObj):
        play_obj = sa.play_buffer(
            audio_obj.audio_buffer.tobytes(),
            audio_obj.num_channels,
            audio_obj.bytes_to_sample,
            audio_obj.sample_rate
        )
        audio_obj.play_obj_que.append(play_obj)

    def execute_stop(self, audio_obj: AudioObj):
        try:
            play_obj = audio_obj.play_obj_que.popleft()
            if play_obj.is_playing(): play_obj.stop()
        except IndexError:
            pass

    def on_escape(self):
        self.quit()

    def on_all_start(self):
        self.execute_start(self.frame_top, self.audio_top)
        self.execute_start(self.frame_bottom, self.audio_bottom)

    def on_all_stop(self):
        self.execute_stop(self.audio_top)
        self.execute_stop(self.audio_bottom)

    def to_txt(self, frame_obj: FrameObj, audio_obj: AudioObj):
        # ファイルパスとオーディオバッファが取得できなければ何もしない
        if frame_obj.file_path is None:
            return
        if audio_obj.audio_buffer is None:
            return

        save_file_path = frame_obj.file_path.replace(".wav", ".csv")
        with open(save_file_path, "w") as file_ptr:
            file_ptr.write(f"Number of Channels, {audio_obj.num_channels}\n")
            file_ptr.write(f"Bytes per Sample, {audio_obj.bytes_to_sample}\n")
            file_ptr.write(f"Sample Rate, {audio_obj.sample_rate}\n")

            # ステレオの場合、各チャンネルを分離
            audio_data = audio_obj.audio_buffer
            if audio_obj.num_channels > 1:
                audio_data = audio_data.reshape(-1, audio_obj.num_channels)
            else:
                audio_data = audio_data.reshape(-1, 1)

            # 各チャンネルのバッファーを書き出し
            [file_ptr.write(f"{ch}ch, " + ",".join(map(str, audio_data[:, ch])) + "\n") for ch in range(0, audio_obj.num_channels)]

    def notify(self, child, file_path):
        # 子クラス（ドラッグ＆ドロップフレーム）からの通知でオーディオファイルを解析
        if file_path is not None:
            # 子クラスの生成 ID からどのフレームか特定
            if (child == self.frame_top.drag_and_drop):
                audio_obj = self.audio_top
                frame_obj = self.frame_top
            if (child == self.frame_bottom.drag_and_drop):
                audio_obj = self.audio_bottom
                frame_obj = self.frame_bottom
            # ファイルパスの記録
            frame_obj.file_path = file_path
            # 波形データの読み込み
            audio_obj.wave_obj = wave.open(file_path, 'rb')
            audio_frame = audio_obj.wave_obj.readframes(audio_obj.wave_obj.getnframes())
            # メタデータの取得
            audio_obj.num_channels = audio_obj.wave_obj.getnchannels()
            audio_obj.bytes_to_sample = audio_obj.wave_obj.getsampwidth()
            audio_obj.sample_rate = audio_obj.wave_obj.getframerate()
            # サンプル幅からデータ型を特定
            audio_dtype = np.int16 if audio_obj.bytes_to_sample == 2 else np.uint8
            audio_obj.audio_buffer = np.frombuffer(audio_frame, dtype=audio_dtype)

if __name__ == "__main__":
    app = AFU()
    app.mainloop()

