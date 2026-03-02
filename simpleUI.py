import os
import sys
import json
from config import CONFIG_FILE
from pipeline import start_
from source.data.input import load_config
import tkinter as tk
from tkinter import messagebox, ttk

current_file = os.path.abspath(__file__)
project_root = os.path.dirname(current_file)

if project_root not in sys.path:
    sys.path.insert(0, project_root)

def normalize_path(path):
    if not path or path == "":
        return path
    normalized = path.replace("\\", "/").replace('"', "").strip()
    return normalized

def Configuration:


