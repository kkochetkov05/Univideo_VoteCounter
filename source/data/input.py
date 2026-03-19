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

def formate_tables(russianSTs, foreignerSTs, votes):
    russian_sheet = next(iter(russianSTs.values()))
    foreigner_sheet = next(iter(foreignerSTs.values()))
    votes_sheet = next(iter(votes.values()))

    russianSTsTable = russian_sheet.iloc[1:, 1:3]
    foreignerSTsTable = foreigner_sheet.iloc[1:, 1:3]

    headers_rename_dict = {
        "Unnamed: 1": "Направление",
        "Unnamed: 2": "ФИО",
        "Unnamed: 3": "Корпоративный email"
    }

    russianSTsTable = russianSTsTable.rename(columns=headers_rename_dict)
    foreignerSTsTable = foreignerSTsTable.rename(columns=headers_rename_dict)

    STsTable = pd.concat([russianSTsTable, foreignerSTsTable], ignore_index=True)

    votesTable = votes_sheet.iloc[1:, 1:29]

    votes_headers_rename_dict = {
        "Unnamed: 1": "ID",
        "Unnamed: 2": "Статус",
        "Unnamed: 3": "st",
        "Unnamed: 4": "ФИО",
        "Unnamed: 5": "Филология",
        "Unnamed: 6": "Медицина",
        "Unnamed: 7": "Прикладная математика - процессы управления (ПМ-ПУ)",
        "Unnamed: 8": "Биология",
        "Unnamed: 9": "Клуб иностранных обучающихся (КИО)",
        "Unnamed: 10": "Экономика",
        "Unnamed: 11": "Математика и механика (МатМех)",
        "Unnamed: 12": "Искусства",
        "Unnamed: 13": "Физическая культура и спорт",
        "Unnamed: 14": "Журналистика и массовые коммуникации (ВШЖиМК)",
        "Unnamed: 15": "Математика и компьютерные науки (МКН)",
        "Unnamed: 16": "Философия",
        "Unnamed: 17": "Студенческие отряды",
        "Unnamed: 18": "Психология",
        "Unnamed: 19": "Востоковедение",
        "Unnamed: 20": "Социология",
        "Unnamed: 21": "Свободные искусства и науки",
        "Unnamed: 22": "Политология",
        "Unnamed: 23": "Химия",
        "Unnamed: 24": "Международные отношения (ФМО)",
        "Unnamed: 25": "Теология",
        "Unnamed: 26": "Менеджмент (ВШМ)",
        "Unnamed: 27": "Институт наук о Земле (ИНоЗ)",
        "Unnamed: 28": "История",
        "Unnamed: 29": "Юриспруденция"
    }

    votesTable = votesTable.rename(columns=votes_headers_rename_dict)

    return STsTable, votesTable