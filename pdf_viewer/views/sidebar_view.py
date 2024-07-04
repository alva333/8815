import tkinter as tk
from tkinter import ttk

class SidebarView:
    def __init__(self, master):
        self.sidebar_frame = ttk.Frame(master, width=200)
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.sidebar_canvas = tk.Canvas(self.sidebar_frame)
        self.sidebar_canvas.pack(side=tk.LEFT, fill=tk.Y, expand=1)

        self.sidebar_scrollbar = ttk.Scrollbar(self.sidebar_frame, orient=tk.VERTICAL, command=self.sidebar_canvas.yview)
        self.sidebar_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.sidebar_canvas.config(yscrollcommand=self.sidebar_scrollbar.set)
        self.sidebar_canvas.bind('<Configure>', lambda e: self.sidebar_canvas.config(scrollregion=self.sidebar_canvas.bbox('all')))

        self.thumbnails_frame = ttk.Frame(self.sidebar_canvas)
        self.sidebar_canvas.create_window((0, 0), window=self.thumbnails_frame, anchor='nw')