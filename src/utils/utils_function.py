from .common_import import *
from typing import TYPE_CHECKING
import tkinter as tk
import soundfile as sf
import numpy as np
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

def get_bytes_per_sample(sub_type: str) -> int:
    # サンプルフォーマットからバイト数を決定
    bit_depth_map = {
        "PCM_U8": 1,   # 8-bit unsigned PCM
        "PCM_16": 2,   # 16-bit signed PCM
        "PCM_24": 3,   # 24-bit signed PCM
        "PCM_32": 4,   # 32-bit signed PCM
        "FLOAT" : 4,   # 32-bit float
        "DOUBLE": 8,   # 64-bit float
    }

    return bit_depth_map.get(sub_type)

def analyze_audio_file(audio_obj: 'AudioObj', file_path: str) -> None:
    # オーディオファイルの取得
    audio_obj.audio_file = sf.SoundFile(file_path)

    # メタデータの取得
    audio_obj.num_channels = audio_obj.audio_file.channels
    audio_obj.bytes_to_sample = get_bytes_per_sample(audio_obj.audio_file.subtype)
    audio_obj.sample_rate = audio_obj.audio_file.samplerate

    # オーディオファイル、オーディオバッファの取得
    audio_buffer, _ = sf.read(file_path)

    # ビット深度に合わせた変換を行う
    match audio_obj.bytes_to_sample:
        case 2:
            audio_buffer = (audio_buffer * 32767).astype(np.int16)
        case 3:
            audio_buffer = (audio_buffer * 8388607).astype(np.int32)
        case 4:
            audio_buffer = (audio_buffer * 2147483647).astype(np.int32)

    # 変換済みのバッファを登録
    audio_obj.audio_buffer = audio_buffer