from datetime import datetime
from pathlib import Path
import csv
import tkinter as tk
from tkinter import StringVar, ttk
import numpy as np


class MainFrame(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._vars = {
            'Name': StringVar(),
            'Audio': []
        }

        ttk.LabelFrame(self, text="Data").grid()
        lbl_name = ttk.Label(self, text="Label1")
        lbl_name.grid(row=0, column=0)

class Application(tk.Tk):
    """Application root window
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Classes Test Application")

        self.main_frame = MainFrame(self)
        self.main_frame.grid(row=1, padx=10, sticky='ew')

if __name__ == "__main__":
    app = Application()
    app.mainloop()

