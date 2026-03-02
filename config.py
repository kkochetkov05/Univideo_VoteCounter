import os
import sys

def get_project_root():
    """определяет корневую папку проекта"""
    if getattr(sys, 'frozen', False):
        # если собрано в exe
        return os.path.dirname(sys.executable)
    else:
        # в разработке
        return os.path.dirname(os.path.abspath(__file__))

PROJECT_ROOT = get_project_root()
CONFIG_FILE = os.path.join(PROJECT_ROOT, "config.json")

APP_NAME = "Счетчик голосов"
VERSION = "1.0.0"