import tkinter as tk
from tkinter import ttk

class MainView:
    def __init__(self, master):
        self.master = master
        self.main_frame = ttk.Frame(self.master)
        self.main_frame.pack(fill=tk.BOTH, expand=1)