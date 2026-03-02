import pandas as pd
import os
import tkinter as tk
from tkinter import messagebox
import json
import sys

from config import CONFIG_FILE


def main():
    if os.path.exists(CONFIG_FILE) and os.path.getsize(CONFIG_FILE) > 0:
        root = tk.Tk()
#        app = SecondPhaseApp(root)
    else:
        root = tk.Tk()
#        app = FirstPhaseApp(root)

    root.mainloop()

if __name__ == "__main__":
    main()