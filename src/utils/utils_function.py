from .common_import import *
from typing import TYPE_CHECKING
import tkinter as tk
import soundfile as sf
import numpy as np
import logging
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

def get_bytes_per_sample(subtype: str) -> int:
    # サンプルフォーマットからバイト数を決定
    bit_depth_map = {
        "PCM_U8"         : 1, # 8-bit unsigned PCM
        "PCM_16"         : 2, # 16-bit signed PCM
        "PCM_24"         : 3, # 24-bit signed PCM
        "PCM_32"         : 4, # 32-bit signed PCM
        "FLOAT"          : 4, # 32-bit float
        "DOUBLE"         : 8, # 64-bit float
        "MPEG_LAYER_III" : 8  # mp3 も Numpy 形式で読み込んだ際は 64 bit となるためビット深度を 8 とする
    }

    return bit_depth_map.get(subtype)

def convert_audio_buffer(audio_buffer: np.array, subtype: str) -> np.array:
    # サンプルフォーマットからバイト数を決定
    match subtype:
        case "PCM_U8": # 8-bit unsigned PCM
            audio_buffer = audio_buffer.astype(np.int16)
            audio_buffer = np.int16((audio_buffer - 128) * 256)  # 8-bit PCM は符号なしのため変換
        case "PCM_16": # 16-bit signed PCM
            audio_buffer = audio_buffer.astype(np.int16)
        case "PCM_24": # 24-bit signed PCM
            audio_buffer = np.int16(audio_buffer / (2**23) * 32767)  # 24-bit PCM を 16-bit にスケール
        case "PCM_32": # 32-bit signed PCM
            audio_buffer = np.int16(audio_buffer / (2**31) * 32767)  # 32-bit PCM を 16-bit にスケール
        case "FLOAT" | "DOUBLE" | "MPEG_LAYER_III" | "VORBIS" : # 32-bit float, 64-bit float, mp3 は同じ変換形式かつ、クリッピング対策を行う
            audio_buffer = np.int16(np.clip(audio_buffer * 32767, -32768, 32767))
        case _: # どの形式でもない場合
            logging.warning(f"Unexpected subtype encountered: {subtype}")

    return audio_buffer

def analyze_audio_file(audio_obj: 'AudioObj', file_path: str) -> None:
    # オーディオファイルの取得
    audio_obj.audio_file = sf.SoundFile(file_path)

    # メタデータの取得
    audio_obj.num_channels = audio_obj.audio_file.channels
    audio_obj.subtype = audio_obj.audio_file.subtype
    audio_obj.bytes_to_sample = get_bytes_per_sample(audio_obj.audio_file.subtype)
    audio_obj.sample_rate = audio_obj.audio_file.samplerate

    # オーディオファイル、オーディオバッファの取得
    audio_buffer = audio_obj.audio_file.read()

    # 再生側がビット深度 2 までしか対応していないので合わせる変換をする
    audio_buffer = convert_audio_buffer(audio_buffer, audio_obj.subtype)
    audio_obj.bytes_to_sample = 2

    # 変換済みのバッファを登録
    audio_obj.audio_buffer = audio_buffer