from __future__ import annotations
from .ui_component import DragAndDropUtil
from .utils_function import get_window_size
from .format_data import AudioObj
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image, ImageTk
from tkinter import PhotoImage
from tkinter import filedialog
from dataclasses import dataclass, field
from collections import deque
from PIL import Image
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from typing import TYPE_CHECKING
import tkinter as tk
import matplotlib.pyplot as plt
import simpleaudio as sa
import soundfile as sf
import numpy as np
import io