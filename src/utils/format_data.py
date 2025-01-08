from __future__ import annotations
from dataclasses import dataclass, field
from collections import deque
from .ui_component import *
import tkinter as tk
import simpleaudio as sa
import numpy as np
import wave

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
    _num_channels: int = 0
    _bytes_to_sample: int = 0
    _sample_rate: int = 0
    wave_obj: wave.Wave_read = None
    audio_buffer: np.array = None
    play_obj_que: deque = field(default_factory=deque)

    @property
    def num_channels(self):
        return self._num_channels

    @num_channels.setter
    def num_channels(self, value):
        self._num_channels = value

    @property
    def bytes_to_sample(self):
        return self._bytes_to_sample

    @bytes_to_sample.setter
    def bytes_to_sample(self, value):
        self._bytes_to_sample = value

    @property
    def sample_rate(self):
        return self._sample_rate

    @sample_rate.setter
    def sample_rate(self, value):
        self._sample_rate = value