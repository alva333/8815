import tkinter as tk
from controllers.main_controller import MainController
import pywinstyles

if __name__ == '__main__':
    root = tk.Tk()
    app = MainController(root)
    pywinstyles.apply_style(window=root, style="win7") 
    root.mainloop()