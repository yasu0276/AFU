from __future__ import annotations
import tkinter as tk
import simpleaudio as sa
from dataclasses import dataclass
from collections import deque
from .ui_component import *

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
