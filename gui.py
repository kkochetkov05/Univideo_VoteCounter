import os
import json
import traceback
from tkcalendar import DateEntry
from tkinter import (
    Tk, Frame, Label, Entry, Button,
    filedialog, messagebox, StringVar
)
from tkinter import ttk

from config import CONFIG_FILE
from pipeline import start


class VoteCounterGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Univideo Vote Counter")
        self.master.geometry("1280x720")
        self.master.resizable(True, True)

        # Общая сетка: 2 строки (конфиг + запуск), 1 колонка
        self.master.rowconfigure(0, weight=4)   # верх — больше
        self.master.rowconfigure(1, weight=1)   # низ — меньше
        self.master.columnconfigure(0, weight=1)

        # Переменные для путей
        self.russian_path = StringVar()
        self.kio_path = StringVar()
        self.study_path = StringVar()
        self.ag_path = StringVar()
        self.votes_path = StringVar()
        self.output_path = StringVar(value="output/ranked_list.xlsx")
        self.date_var = StringVar()

        # Загрузка существующей конфигурации
        self.load_existing_config()

        # Создание интерфейса
        self.create_config_window()
        self.create_main_window()

    def load_existing_config(self):
        """Загрузка существующего config.json"""
        if os.path.exists(CONFIG_FILE) and os.path.getsize(CONFIG_FILE) > 0:
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                self.russian_path.set(config.get('RussianWorkbook', ''))
                self.kio_path.set(config.get('KIOWorkbook', ''))
                self.study_path.set(config.get('studyWorkbook', ''))
                self.ag_path.set(config.get('AGWorkbook', ''))
                self.votes_path.set(config.get('VotesWorkbook', ''))
                self.output_path.set(config.get('OutputPath', 'output/ranked_list.xlsx'))
                self.date_var.set(config.get('date', ''))
            except Exception:
                pass

    def create_config_window(self):
        # Фрейм конфигурации занимает верхнюю часть окна
        self.config_frame = Frame(self.master, bg='#fffffe')
        self.config_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=10)

        # Сетка внутри config_frame:
        # 0: заголовок
        # 1: подзаголовок
        # 2-7: поля для файлов (6 строк)
        # 8: дата
        # 9: кнопки
        for r in range(10):
            # небольшие веса, чтобы всё масштабировалось равномерно
            self.config_frame.rowconfigure(r, weight=1)
        self.config_frame.columnconfigure(0, weight=1)
        self.config_frame.columnconfigure(1, weight=3)  # колонка с Entry больше
        self.config_frame.columnconfigure(2, weight=0)  # колонка с кнопкой "Обзор"

        # Заголовок
        title = Label(
            self.config_frame,
            text="Конфигурация проекта",
            font=("Arial", 16, "bold"),
            bg='#fffffe',
            fg='#13343b'
        )
        title.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 2))

        subtitle = Label(
            self.config_frame,
            text="Укажите пути к файлам Excel",
            font=("Arial", 9),
            bg='#fffffe',
            fg='#626c71'
        )
        subtitle.grid(row=1, column=0, columnspan=3, sticky="w", pady=(0, 5))

        row_idx = 2  # начинаем поля со строки 2

        # Поля: метка | Entry | кнопка "Обзор"
        self._create_file_row(
            row_idx,
            "Excel-файл с русскими студентами:",
            self.russian_path,
            self.browse_russian
        )
        row_idx += 1

        self._create_file_row(
            row_idx,
            "Excel-файл с КИО:",
            self.kio_path,
            self.browse_kio
        )
        row_idx += 1

        self._create_file_row(
            row_idx,
            "Excel-файл с study:",
            self.study_path,
            self.browse_study
        )
        row_idx += 1

        self._create_file_row(
            row_idx,
            "Excel-файл с Академической гимназией:",
            self.ag_path,
            self.browse_ag
        )
        row_idx += 1

        self._create_file_row(
            row_idx,
            "Excel-файл с данными голосования:",
            self.votes_path,
            self.browse_votes
        )
        row_idx += 1

        self._create_file_row(
            row_idx,
            "Путь для сохранения результатов:",
            self.output_path,
            self.browse_output,
            note_text="Файл будет создан автоматически, если не существует"
        )
        row_idx += 1

        # Поле даты — отдельной строкой, без кнопки
        date_container = Frame(self.config_frame, bg='#fffffe')
        date_container.grid(row=row_idx, column=0, columnspan=3, sticky="w", pady=(2, 0))

        date_label = Label(
            date_container,
            text="Дата (для фильтра старых голосов):",
            font=("Arial", 10, "bold"),
            bg='#fffffe',
            fg='#13343b'
        )
        date_label.grid(row=0, column=0, sticky="w", padx=(10, 5))

        self.date_entry = DateEntry(
            date_container,
            textvariable=self.date_var,
            date_pattern="yyyy-mm-dd",
            font=("Arial", 10),
            relief='solid',
            bd=1,
            width=12  # ключевой параметр ширины
        )
        self.date_entry.grid(row=0, column=1, sticky="w")  # без nsew, чтобы не растягивалось

        # колонке с датой вес не даём
        date_container.columnconfigure(0, weight=0)
        date_container.columnconfigure(1, weight=0)

        row_idx += 1

        # Кнопки сохранения/загрузки конфигурации — последняя строка
        btn_frame = Frame(self.config_frame, bg='#fffffe')
        btn_frame.grid(row=row_idx, column=0, columnspan=3, sticky="e", pady=(4, 0))

        save_btn = Button(
            btn_frame,
            text="Сохранить конфигурацию",
            command=self.save_config,
            bg='#21808d',
            fg='white',
            font=("Arial", 10, "bold"),
            padx=12,
            pady=6,
            relief='flat',
            cursor='hand2'
        )
        save_btn.pack(side='left', padx=3)

        load_btn = Button(
            btn_frame,
            text="Загрузить существующую",
            command=self.load_config,
            bg='#f5f5f5',
            fg='#13343b',
            font=("Arial", 10),
            padx=12,
            pady=6,
            relief='flat',
            cursor='hand2'
        )
        load_btn.pack(side='left', padx=3)

    def _create_file_row(self, row, label_text, var, browse_cmd, note_text=None):
        """Одна строка: метка, поле ввода, кнопка 'Обзор' (+ опциональная подпись)"""
        label = Label(
            self.config_frame,
            text=label_text,
            font=("Arial", 10, "bold"),
            bg='#fffffe',
            fg='#13343b'
        )
        label.grid(row=row, column=0, sticky="w", padx=(10, 5))

        entry = Entry(
            self.config_frame,
            textvariable=var,
            font=("Arial", 10),
            relief='solid',
            bd=1
        )
        entry.grid(row=row, column=1, sticky="nsew", pady=2)

        browse_btn = Button(
            self.config_frame,
            text="Обзор",
            command=browse_cmd,
            bg='#f5f5f5',
            fg='#13343b',
            font=("Arial", 9),
            padx=10,
            pady=3,
            relief='flat',
            cursor='hand2'
        )
        browse_btn.grid(row=row, column=2, sticky="e", padx=(5, 0), pady=2)

        if note_text:
            note = Label(
                self.config_frame,
                text=note_text,
                font=("Arial", 8),
                bg='#fffffe',
                fg='#999'
            )
            # маленькая подпись под строкой (в той же колонке, что и entry)
            note.grid(row=row + 1, column=1, columnspan=2, sticky="w", pady=(0, 2))

    def create_main_window(self):
        # Нижняя часть — запуск обработки
        self.main_frame = Frame(self.master, bg='#fffffe')
        self.main_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 10))

        self.main_frame.rowconfigure(0, weight=0)
        self.main_frame.rowconfigure(1, weight=1)
        self.main_frame.rowconfigure(2, weight=0)
        self.main_frame.rowconfigure(3, weight=1)
        self.main_frame.columnconfigure(0, weight=1)

        ttk.Separator(self.main_frame, orient='horizontal').grid(
            row=0, column=0, sticky="ew", pady=(0, 5)
        )

        title = Label(
            self.main_frame,
            text="Подсчёт голосов",
            font=("Arial", 16, "bold"),
            bg='#fffffe',
            fg='#13343b'
        )
        title.grid(row=1, column=0, sticky="n", pady=(2, 2))

        subtitle = Label(
            self.main_frame,
            text="Запустите обработку данных и формирование рейтинга победителей",
            font=("Arial", 9),
            bg='#fffffe',
            fg='#626c71'
        )
        subtitle.grid(row=2, column=0, sticky="n", pady=(0, 5))

        run_btn = Button(
            self.main_frame,
            text="Запустить обработку",
            command=self.run_processing,
            bg='#21808d',
            fg='white',
            font=("Arial", 13, "bold"),
            padx=20,
            pady=8,
            relief='flat',
            cursor='hand2'
        )
        run_btn.grid(row=3, column=0, sticky="n", pady=(5, 10))

    # -------- browse функции --------

    def browse_russian(self):
        path = filedialog.askopenfilename(
            title="Выберите файл с русскими студентами",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
        )
        if path:
            self.russian_path.set(path)

    def browse_kio(self):
        path = filedialog.askopenfilename(
            title="Выберите файл с КИО",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
        )
        if path:
            self.kio_path.set(path)

    def browse_study(self):
        path = filedialog.askopenfilename(
            title="Выберите файл study",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
        )
        if path:
            self.study_path.set(path)

    def browse_ag(self):
        path = filedialog.askopenfilename(
            title="Выберите файл с Академической гимназией",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
        )
        if path:
            self.ag_path.set(path)

    def browse_votes(self):
        path = filedialog.askopenfilename(
            title="Выберите файл с данными голосования",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
        )
        if path:
            self.votes_path.set(path)

    def browse_output(self):
        path = filedialog.asksaveasfilename(
            title="Укажите путь для сохранения результатов",
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        if path:
            self.output_path.set(path)

    # -------- сохранение/загрузка конфигурации --------

    def save_config(self):
        """Сохранение конфигурации в config.json"""
        russian = self.russian_path.get().strip()
        kio = self.kio_path.get().strip()
        study = self.study_path.get().strip()
        ag = self.ag_path.get().strip()
        votes = self.votes_path.get().strip()
        output = self.output_path.get().strip()
        date_val = self.date_var.get().strip()

        if not (russian and kio and study and ag and votes):
            messagebox.showerror("Ошибка", "Заполните все обязательные поля!")
            return

        config = {
            "RussianWorkbook": russian,
            "KIOWorkbook": kio,
            "studyWorkbook": study,
            "AGWorkbook": ag,
            "VotesWorkbook": votes,
            "OutputPath": output,
            "date": date_val
        }

        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            messagebox.showinfo("Успех", "Конфигурация успешно сохранена!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить конфигурацию:\n{e}")

    def load_config(self):
        """Загрузка конфигурации из config.json"""
        if not os.path.exists(CONFIG_FILE):
            messagebox.showerror("Ошибка", "Файл config.json не найден!")
            return

        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
            self.russian_path.set(config.get('RussianWorkbook', ''))
            self.kio_path.set(config.get('KIOWorkbook', ''))
            self.study_path.set(config.get('studyWorkbook', ''))
            self.ag_path.set(config.get('AGWorkbook', ''))
            self.votes_path.set(config.get('VotesWorkbook', ''))
            self.output_path.set(config.get('OutputPath', 'output/ranked_list.xlsx'))
            self.date_var.set(config.get('date', ''))
            messagebox.showinfo("Успех", "Конфигурация загружена!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить конфигурацию:\n{e}")

    def run_processing(self):
        """Запуск обработки данных"""
        if not os.path.exists(CONFIG_FILE) or os.path.getsize(CONFIG_FILE) == 0:
            messagebox.showerror("Ошибка", "Сначала сохраните конфигурацию!")
            return

        try:
            messagebox.showinfo(
                "Обработка",
                "Обработка данных запущена...\nЭто может занять некоторое время"
            )
            start()
            messagebox.showinfo(
                "Успех",
                "Обработка завершена!\nРезультаты сохранены в Excel-файл"
            )
        except Exception as e:
            traceback.print_exc()
            messagebox.showerror("Ошибка", f"Ошибка при обработке:\n{e}")


def main():
    root = Tk()
    root.state('zoomed')
    app = VoteCounterGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
