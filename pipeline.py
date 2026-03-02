import traceback
import sys
import tkinter as tk
from tkinter import messagebox
from config import CONFIG_FILE
from source.data.input import load_config, load_requied_files, formate_tables
from source.core.vote_filter import calculate_rankings
from source.data.output import export_ranked_list_to_excel


def start():
    """Главная функция запуска обработки"""

    # Загрузка конфигурации
    config = load_config(CONFIG_FILE)
    russian_STs_path = config['RussianWorkbook']
    foreigner_STs_path = config['ForeignerWorkbook']
    output_path = config.get('OutputPath', 'output/ranked_list.xlsx')

    # Загрузка файлов
    files = load_requied_files({
        'russianSTs': russian_STs_path,
        'foreignerSTs': foreigner_STs_path
    })

    russian_STs = files['russianSTs']
    foreigner_STs = files['foreignerSTs']

    # Форматирование таблиц
    STs = formate_tables(russian_STs, foreigner_STs)

    # Обработка голосов и формирование рейтинга
    try:
        ranked_df = calculate_rankings(STs)

        # Экспорт результатов
        export_ranked_list_to_excel(ranked_df, output_path)

        # Успешное завершение
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo(
            "Готово",
            f"Обработка завершена!\n\nРанжированный список сохранён:\n{output_path}"
        )
        root.destroy()

    except Exception as e:
        # Обработка ошибок
        exc_type, exc_value, exc_traceback = sys.exc_info()

        tb_lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        tb_text = ''.join(tb_lines)

        formatted_tb = traceback.format_tb(exc_traceback)
        last_frames = formatted_tb[-3:] if len(formatted_tb) > 3 else formatted_tb

        error_info = []
        for frame in last_frames:
            lines = frame.strip().split('\n')
            for line in lines:
                if 'File' in line:
                    parts = line.split('"')
                    if len(parts) >= 3:
                        filepath = parts[1]
                        lineinfo = parts[2].strip()
                        filename = filepath.split('/')[-1] if '/' in filepath else filepath.split('\\')[-1]
                        error_info.append(f"{filename}")
                        error_info.append(f"{lineinfo}")

        error_message_parts = [
            f"{exc_type.__name__}:",
            f"{str(exc_value)}",
        ]

        if error_info:
            error_message_parts.append("")
            error_message_parts.extend(error_info[-2:])

        error_message = '\n'.join(error_message_parts)

        print("=" * 50)
        print(f"Ошибка: {exc_type.__name__}")
        print(f"Сообщение: {exc_value}")
        print('\n'.join(last_frames))
        print("=" * 50)

        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(
            "Ошибка",
            f"Произошла ошибка:\n\n{exc_type.__name__}\n{str(exc_value)[:150]}\n\nПодробности в консоли."
        )
        root.destroy()
        raise
