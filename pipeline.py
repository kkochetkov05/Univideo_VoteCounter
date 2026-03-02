import traceback
import sys

import tkinter as tk
from tkinter import messagebox

from config import CONFIG_FILE
from source.data.input import load_config
from source.data.input import load_requied_files
from source.data.input import formate_tables
from source.data.output import export_ranked_list_to_excel

def start_():
    config = load_config(CONFIG_FILE)

    formToDBName = config["FormToDBName"]
    russianSTs_path = config["Workbooks"]["RussianWorkbook"]
    foreignerSTs_path = config["Workbooks"]["ForeignerWorkbook"]

    files = load_requied_files(
        russianSTs = russianSTs_path,
        foreignerSTs = foreignerSTs_path
    )

    russianSTs = files["russianSTs"]
    foreignerSTs = files["foreignerSTs"]

    russianSTs_table, foreignerSTs_table = formate_tables(russianSTs, foreignerSTs)

    try:
        export_ranked_list_to_excel(russianSTs_table, foreignerSTs_table)

        root = tk.Tk()
        root.withdraw()

        messagebox.showinfo(
            "Готово.",
            "Подсчет голосов прошел успешно.\n\n"
            "Результаты сохранены в файл"
        )
    except Exception as e:
        # Получаем детальную информацию об ошибке
        exc_type, exc_value, exc_traceback = sys.exc_info()

        # Формируем traceback
        tb_lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        tb_text = ''.join(tb_lines)

        # Более читаемый вариант traceback (последние 3 кадра)
        formatted_tb = traceback.format_tb(exc_traceback)
        last_frames = formatted_tb[-3:] if len(formatted_tb) >= 3 else formatted_tb

        # Извлекаем информацию о месте ошибки
        error_info = []
        for frame in last_frames:
            # Парсим строку traceback для получения файла и строки
            lines = frame.strip().split('\n')
            for line in lines:
                if 'File "' in line:
                    # Извлекаем путь к файлу и номер строки
                    parts = line.split('"')
                    if len(parts) >= 3:
                        file_path = parts[1]
                        line_info = parts[2].strip()
                        # Берем только имя файла, а не полный путь
                        file_name = file_path.split('/')[-1] if '/' in file_path else file_path.split('\\')[-1]
                        error_info.append(f"Файл: {file_name}")
                        error_info.append(f"Строка: {line_info}")

        # Формируем сообщение для пользователя
        error_message_parts = [
            f"Тип ошибки: {exc_type.__name__}",
            f"Сообщение: {str(exc_value)}",
        ]

        # Добавляем информацию о месте ошибки если удалось извлечь
        if error_info:
            error_message_parts.append("\nМесто ошибки:")
            error_message_parts.extend(error_info[-2:])  # Последний файл и строка

        error_message = '\n'.join(error_message_parts)

        print("=" * 50)
        print(f"ОШИБКА В ПАЙПЛАЙНЕ:")
        print(f"Тип: {exc_type.__name__}")
        print(f"Сообщение: {exc_value}")
        print(f"\nTraceback (последние вызовы):")
        print(''.join(last_frames))
        print("=" * 50)

        # Показываем окно с ошибкой
        root = tk.Tk()
        root.withdraw()

        messagebox.showerror(
            "Ошибка создания тэгов",
            f"Произошла ошибка при создании тэгов:\n\n"
            f"▸ Тип: {exc_type.__name__}\n"
            f"▸ Сообщение: {str(exc_value)[:150]}\n\n"
            f"Более подробная информация в консоли."
        )

        root.destroy()

        raise