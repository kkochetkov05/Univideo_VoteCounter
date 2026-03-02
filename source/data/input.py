import pandas as pd
from pathlib import Path
import json

def load_config(CONFIG_FILE):
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"{CONFIG_FILE} не найден")
        return {}
    except json.JSONDecodeError:
        print(f"Ошибка чтения {CONFIG_FILE}")
        return {}

def load_requied_files(**file_paths):
    result = {}
    for name, path in file_paths.items():
        if not Path(path).exists():
            raise FileNotFoundError(f"Файл не найден: {Path(path).name}")
    df = pd.read_excel(path, sheet_name=None)
    result[name] = df
    return result

def formate_tables(russianSTs, foreignerSTs):
    russianSTsTable = russianSTs[0].iloc[1:, 1:3]
    foreignerSTsTable = foreignerSTs[0].iloc[1:, 1:3]

    headers_rename_dict = {
        "Unnamed: 1": "Направление",
        "Unnamed: 2": "ФИО",
        "Unnamed: 3": "Корпоративный email"
    }

    russianSTsTable = russianSTsTable.rename(columns=headers_rename_dict)
    foreignerSTsTable = foreignerSTsTable.rename(columns=headers_rename_dict)

    STs = pd.concat([russianSTsTable, foreignerSTsTable], ignore_index=True)

    return STs