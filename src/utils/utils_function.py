from .common_import import *
import tkinter as tk
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .format_data import AudioObj

def write_csv(file_path: str, audio_obj: 'AudioObj') -> None:
    with open(file_path, "w") as file_ptr:
        file_ptr.write(f"Number of Channels, {audio_obj.num_channels}\n")
        file_ptr.write(f"Bytes per Sample, {audio_obj.bytes_to_sample}\n")
        file_ptr.write(f"Sample Rate, {audio_obj.sample_rate}\n")

        audio_data = audio_obj.audio_buffer

        # 各チャンネルのバッファーを書き出し
        [file_ptr.write(f"{ch}ch, " + ",".join(map(str, audio_data[:, ch])) + "\n") for ch in range(0, audio_obj.num_channels)]

def get_window_size() -> tuple:
    root = tk.Tk()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.destroy()
    return (width, height)
