from utils import *

def write_csv(file_path: str, audio_obj: AudioObj):
    with open(file_path, "w") as file_ptr:
        file_ptr.write(f"Number of Channels, {audio_obj.num_channels}\n")
        file_ptr.write(f"Bytes per Sample, {audio_obj.bytes_to_sample}\n")
        file_ptr.write(f"Sample Rate, {audio_obj.sample_rate}\n")

        audio_data = audio_obj.audio_buffer

        # 各チャンネルのバッファーを書き出し
        [file_ptr.write(f"{ch}ch, " + ",".join(map(str, audio_data[:, ch])) + "\n") for ch in range(0, audio_obj.num_channels)]

class AFU(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()

        # メニューバー
        self.menubar = tk.Menu(self)
        self.config(menu=self.menubar)

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
        self.frame_top.drag_and_drop = DragAndDropUtil(self, width=50, height=100)
        self.frame_top.drag_and_drop.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        self.frame_bottom.drag_and_drop = DragAndDropUtil(self, width=50, height=100)
        self.frame_bottom.drag_and_drop.grid(row=1, column=1, padx=5, pady=5, sticky='ew')

        # ボタンフレーム Top
        self.frame_top.button = tk.Frame(self)
        self.frame_top.button.grid(row=0, column=0, padx=0, pady=5)

        self.frame_top.button_start = tk.Button(self.frame_top.button, text="start", command=lambda: self.execute_start(self.frame_top, self.audio_top), width=20)
        self.frame_top.button_start.pack(side=tk.TOP, padx=10)

        self.frame_top.button_stop = tk.Button(self.frame_top.button, text="stop", command=lambda: self.execute_stop(self.audio_top), width=20)
        self.frame_top.button_stop.pack(side=tk.TOP, padx=10)

        self.frame_top.button_stop.pack(side=tk.TOP, padx=10)
        self.frame_bottom.button = tk.Frame(self)
        self.frame_bottom.button.grid(row=1, column=0, padx=0, pady=5)

        # ボタンフレーム Bottom
        self.frame_bottom.button_start = tk.Button(self.frame_bottom.button, text="start", command=lambda: self.execute_start(self.frame_bottom, self.audio_bottom), width=20)
        self.frame_bottom.button_start.pack(side=tk.TOP, padx=10)

        self.frame_bottom.button_stop = tk.Button(self.frame_bottom.button, text="stop", command=lambda: self.execute_stop(self.audio_bottom), width=20)
        self.frame_bottom.button_stop.pack(side=tk.TOP, padx=10)

        # ファイルメニュー
        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="ファイル", menu=self.file_menu)
        # サブメニューを作成
        self.save_menu = tk.Menu(self.file_menu, tearoff=0)
        self.file_menu.add_cascade(label="保存", menu=self.save_menu)
        self.save_menu.add_command(label="画像", command=self.save_image)
        self.save_menu.add_command(label="CSV", command=self.save_csv)
        # メインに追加し直し
        self.file_menu.add_command(label="終了 (ESC) ", command=self.quit)

        # 編集メニュー
        self.edit_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="編集", menu=self.edit_menu)

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

    def save_csv(self):
        file_types = [("CSV", "*.csv")]
        audio_objects = [self.audio_top, self.audio_bottom]

        for audio_object in audio_objects:
            # ファイルパスとオーディオバッファが取得できなければ何もしない
            if audio_object:
                save_path = filedialog.asksaveasfilename(
                    defaultextension = ".csv",
                    filetypes = file_types,
                    title = "CSVを保存"
                )

            if save_path:
                write_csv(save_path, audio_object)

    def save_image(self):
        file_types = [("PNG", "*.png"), ("JPEG", "*.jpg")]
        pil_images = [self.frame_top.pil_image, self.frame_bottom.pil_image]

        for pil_image in pil_images:
            if pil_image:
                save_path = filedialog.asksaveasfilename(
                    defaultextension = ".png",
                    filetypes = file_types,
                    title = "画像を保存"
                )

            if save_path:
                pil_image.save(save_path)

    def notify(self, child, file_path):
        # 子クラス（ドラッグ＆ドロップフレーム）からの通知でオーディオファイルを解析
        if file_path is not None:
            # 子クラスの生成 ID からどのフレームか特定
            if (child == self.frame_top.drag_and_drop):
                audio_obj = self.audio_top
                frame_obj = self.frame_top
                drag_and_drop_obj = self.frame_top.drag_and_drop
            if (child == self.frame_bottom.drag_and_drop):
                audio_obj = self.audio_bottom
                frame_obj = self.frame_bottom
                drag_and_drop_obj = self.frame_bottom.drag_and_drop
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

            # 各チャンネルを分離
            audio_obj.audio_buffer = audio_obj.audio_buffer.reshape(-1, audio_obj.num_channels)

            # メタデータの書き出し
            content =  f"File Path, {file_path}\n"
            content +=  f"Number of Channels, {audio_obj.num_channels}\n"
            content +=  f"Bytes per Sample, {audio_obj.bytes_to_sample}\n"
            content +=  f"Sample Rate, {audio_obj.sample_rate}\n"
            drag_and_drop_obj.write_content(content)

            # 音声波形をプロット
            audio_data = audio_obj.audio_buffer
            title = file_path.replace(".wav", "")
            duration = len(audio_data) / audio_obj.sample_rate
            times = np.linspace(0, duration, len(audio_data))
            buf = io.BytesIO()
            # 画像サイズ、dpi 設定
            fig_size = (10, 5)
            dpi = 100
            # 余白を最小限に設定
            plt.tight_layout(pad=0)
            # カラーマップから色を取得
            colors = plt.cm.viridis(np.linspace(0, 1, audio_obj.num_channels))
            plt.figure(figsize=fig_size)
            [plt.plot(times, audio_data[:, i], color=colors[i], label=f"{i} ch") for i in range(0, audio_obj.num_channels, 1)]
            plt.title(f"{title}")
            plt.xlabel("Times [s]")
            plt.ylabel("Amplitude")
            plt.grid()
            plt.legend()
            # プロットをバイト列として保存
            plt.savefig(buf, dpi=dpi)
            plt.close()

            # バッファーの先頭にシークして画像を読み込み
            buf.seek(0)
            frame_obj.pil_image = Image.open(buf)
            # テキストエリアに表示できるように形式を変更
            frame_obj.photo_image = ImageTk.PhotoImage(frame_obj.pil_image.resize((fig_size[0] * dpi, fig_size[1] * dpi)))
            drag_and_drop_obj.write_image(frame_obj.photo_image)

if __name__ == "__main__":
    app = AFU()
    app.mainloop()

