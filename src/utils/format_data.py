from .common_import import *
from .utils_function import get_window_size
from dataclasses import dataclass, field
from collections import deque
from tkinter import PhotoImage
from PIL import Image
import numpy as np
import tkinter as tk
import soundfile as sf

max_width, max_height = get_window_size()
@dataclass(slots=True)
class FrameObj():
    max_width: int = max_width
    max_height: int = max_height
    width: int = max_width
    height: int = max_height
    title: str = "AFU"
    _file_path: str = None
    button: tk.Frame = None
    button_start: tk.Button = None
    button_stop: tk.Button = None
    drag_and_drop: DragAndDropUtil = None
    pil_image:Image = None
    photo_image: PhotoImage = None

    @property
    def file_path(self) -> str:
        return self._file_path

    @file_path.setter
    def file_path(self, value):
        self._file_path = value

@dataclass(slots=True)
class AudioObj():
    _num_channels: int = 0
    _bytes_to_sample: int = 0
    _sample_rate: int = 0
    _subtype: str = None
    audio_file: sf.SoundFile = None
    audio_buffer: np.array = None
    play_obj_que: deque = field(default_factory=deque)

    @property
    def num_channels(self) -> int:
        return self._num_channels

    @num_channels.setter
    def num_channels(self, value):
        self._num_channels = value

    @property
    def bytes_to_sample(self) -> int:
        return self._bytes_to_sample

    @bytes_to_sample.setter
    def bytes_to_sample(self, value):
        self._bytes_to_sample = value

    @property
    def sample_rate(self) -> int:
        return self._sample_rate

    @sample_rate.setter
    def sample_rate(self, value):
        self._sample_rate = value

    @property
    def subtype(self) -> str:
        return self._subtype

    @sample_rate.setter
    def subtype(self, value):
        self._subtype = value