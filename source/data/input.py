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

def formate_tables(russianSTs, KIOSTs, AGSTs, studySTs, votes):
    russian_sheet = next(iter(russianSTs.values()))
    KIO_sheet = next(iter(KIOSTs.values()))
    AG_sheet = next(iter(AGSTs.values()))
    study_sheet = next(iter(studySTs.values()))
    votes_sheet = next(iter(votes.values()))

    russianSTsTable = russian_sheet.iloc[0:]
    KIOSTsTable = KIO_sheet.iloc[0:]
    studySTsTable = study_sheet[0:]
    AGSTsTable = AG_sheet.iloc[0:, 2]
    temp = ['Студенческие отряды'] * len(AGSTsTable)
    temp = pd.Series(temp, name='Направление')
    AGSTsTable = pd.concat([AGSTsTable, temp], axis=1)


    # headers_rename_dict = {
    #     "Unnamed: 1": "ФИО",
    #     "Unnamed: 2": "Направление",
    #     "Unnamed: 3": "Гражданство",
    #     "Unnamed: 4": "Корпоративный email"
    # }
    #
    # russianSTsTable = russianSTsTable.rename(columns=headers_rename_dict)
    # KIOSTsTable = KIOSTsTable.rename(columns=headers_rename_dict)
    # studySTsTable = studySTsTable.rename(columns=headers_rename_dict)

    AGSTsTable.columns = ['Корпоративный email', 'Направление']

    STsTable = pd.concat([russianSTsTable, KIOSTsTable, studySTsTable, AGSTsTable], ignore_index=True)
    pd.set_option('display.max_columns', None)
    print(STsTable.columns)
    print(STsTable)

    votesTable = votes_sheet.iloc[0:, 1:17]
    votesTable.columns = ['Время создания', 'Статус',
       'st',
       'ФИО',
       'Студенческие отряды',
       'Психология',
       'Востоковедение',
       'Социология',
       'Свободные искусства и науки',
       'Политология',
       'Химия',
       'Международные отношения (ФМО)',
       'Теология',
       'Менеджмент (ВШМ)',
       'Институт наук о Земле (ИНоЗ)',
       'История']

    # votes_headers_rename_dict = {
    #     "Unnamed: 1": "ID",
    #     "Unnamed: 2": "Статус",
    #     "Unnamed: 3": "st",
    #     "Unnamed: 4": "ФИО",
    #     "Unnamed: 5": "Филология",
    #     "Unnamed: 6": "Медицина",
    #     "Unnamed: 7": "Прикладная математика - процессы управления (ПМ-ПУ)",
    #     "Unnamed: 8": "Биология",
    #     "Unnamed: 9": "Клуб иностранных обучающихся (КИО)",
    #     "Unnamed: 10": "Экономика",
    #     "Unnamed: 11": "Математика и механика (МатМех)",
    #     "Unnamed: 12": "Искусства",
    #     "Unnamed: 13": "Физическая культура и спорт",
    #     "Unnamed: 14": "Журналистика и массовые коммуникации (ВШЖиМК)",
    #     "Unnamed: 15": "Математика и компьютерные науки (МКН)",
    #     "Unnamed: 16": "Философия",
    #     "Unnamed: 17": "Студенческие отряды",
    #     "Unnamed: 18": "Психология",
    #     "Unnamed: 19": "Востоковедение",
    #     "Unnamed: 20": "Социология",
    #     "Unnamed: 21": "Свободные искусства и науки",
    #     "Unnamed: 22": "Политология",
    #     "Unnamed: 23": "Химия",
    #     "Unnamed: 24": "Международные отношения (ФМО)",
    #     "Unnamed: 25": "Теология",
    #     "Unnamed: 26": "Менеджмент (ВШМ)",
    #     "Unnamed: 27": "Институт наук о Земле (ИНоЗ)",
    #     "Unnamed: 28": "История",
    #     "Unnamed: 29": "Юриспруденция"
    # }
    #
    # votesTable = votesTable.rename(columns=votes_headers_rename_dict)

    return STsTable, AGSTsTable, votesTable

