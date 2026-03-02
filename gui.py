import os
import sys
import json
from tkinter import Tk, Frame, Label, Entry, Button, filedialog, messagebox, StringVar
from tkinter import ttk
from config import CONFIG_FILE
from pipeline import start


class VoteCounterGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Univideo Vote Counter")
        self.master.geometry("800x600")
        self.master.resizable(True, True)

        # Переменные для путей
        self.russian_path = StringVar()
        self.foreigner_path = StringVar()
        self.output_path = StringVar(value="output/ranked_list.xlsx")

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
                    self.foreigner_path.set(config.get('ForeignerWorkbook', ''))
                    self.output_path.set(config.get('OutputPath', 'output/ranked_list.xlsx'))
            except:
                pass

    def create_config_window(self):
        """Окно конфигурации"""
        config_frame = Frame(self.master, bg='#fffffe', padx=30, pady=20)
        config_frame.pack(fill='both', expand=True, padx=20, pady=(20, 10))

        # Заголовок
        title = Label(config_frame, text="Конфигурация проекта",
                      font=("Arial", 18, "bold"), bg='#fffffe', fg='#13343b')
        title.pack(pady=(0, 5))

        subtitle = Label(config_frame, text="Укажите пути к файлам Excel с данными голосования",
                         font=("Arial", 10), bg='#fffffe', fg='#626c71')
        subtitle.pack(pady=(0, 20))

        # Поля ввода
        self._create_file_field(config_frame, "Excel-файл с русскими студентами:",
                                self.russian_path, self.browse_russian)
        self._create_file_field(config_frame, "Excel-файл с иностранными студентами:",
                                self.foreigner_path, self.browse_foreigner)
        self._create_file_field(config_frame, "Путь для сохранения результатов:",
                                self.output_path, self.browse_output, is_output=True)

        # Кнопки действий
        btn_frame = Frame(config_frame, bg='#fffffe')
        btn_frame.pack(pady=20)

        save_btn = Button(btn_frame, text="Сохранить конфигурацию",
                          command=self.save_config, bg='#21808d', fg='white',
                          font=("Arial", 11, "bold"), padx=20, pady=10,
                          relief='flat', cursor='hand2')
        save_btn.pack(side='left', padx=5)

        load_btn = Button(btn_frame, text="Загрузить существующую",
                          command=self.load_config, bg='#f5f5f5', fg='#13343b',
                          font=("Arial", 11), padx=20, pady=10,
                          relief='flat', cursor='hand2')
        load_btn.pack(side='left', padx=5)

    def create_main_window(self):
        """Главное окно запуска"""
        main_frame = Frame(self.master, bg='#fffffe', padx=30, pady=20)
        main_frame.pack(fill='both', expand=True, padx=20, pady=(10, 20))

        # Разделитель
        ttk.Separator(self.master, orient='horizontal').pack(fill='x', padx=20)

        # Заголовок
        title = Label(main_frame, text="Подсчёт голосов",
                      font=("Arial", 18, "bold"), bg='#fffffe', fg='#13343b')
        title.pack(pady=(10, 5))

        subtitle = Label(main_frame, text="Запустите обработку данных и формирование рейтинга победителей",
                         font=("Arial", 10), bg='#fffffe', fg='#626c71')
        subtitle.pack(pady=(0, 20))

        # Кнопка запуска
        run_btn = Button(main_frame, text="Запустить обработку",
                         command=self.run_processing, bg='#21808d', fg='white',
                         font=("Arial", 14, "bold"), padx=40, pady=15,
                         relief='flat', cursor='hand2')
        run_btn.pack(pady=30)

    def _create_file_field(self, parent, label_text, var, browse_cmd, is_output=False):
        """Создание поля для файла с кнопкой обзора"""
        container = Frame(parent, bg='#fffffe')
        container.pack(fill='x', pady=8)

        label = Label(container, text=label_text, font=("Arial", 10, "bold"),
                      bg='#fffffe', fg='#13343b')
        label.pack(anchor='w')

        input_frame = Frame(container, bg='#fffffe')
        input_frame.pack(fill='x', pady=(5, 0))

        entry = Entry(input_frame, textvariable=var, font=("Arial", 10),
                      relief='solid', bd=1)
        entry.pack(side='left', fill='x', expand=True, ipady=5)

        browse_btn = Button(input_frame, text="Обзор", command=browse_cmd,
                            bg='#f5f5f5', fg='#13343b', font=("Arial", 9),
                            padx=15, pady=5, relief='flat', cursor='hand2')
        browse_btn.pack(side='left', padx=(8, 0))

        if is_output:
            note = Label(container, text="Файл будет создан автоматически, если не существует",
                         font=("Arial", 8), bg='#fffffe', fg='#999')
            note.pack(anchor='w', pady=(2, 0))

    def browse_russian(self):
        path = filedialog.askopenfilename(
            title="Выберите файл с русскими студентами",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
        )
        if path:
            self.russian_path.set(path)

    def browse_foreigner(self):
        path = filedialog.askopenfilename(
            title="Выберите файл с иностранными студентами",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
        )
        if path:
            self.foreigner_path.set(path)

    def browse_output(self):
        path = filedialog.asksaveasfilename(
            title="Укажите путь для сохранения результатов",
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        if path:
            self.output_path.set(path)

    def save_config(self):
        """Сохранение конфигурации в config.json"""
        russian = self.russian_path.get().strip()
        foreigner = self.foreigner_path.get().strip()
        output = self.output_path.get().strip()

        if not russian or not foreigner:
            messagebox.showerror("Ошибка", "Заполните все обязательные поля!")
            return

        config = {
            "RussianWorkbook": russian,
            "ForeignerWorkbook": foreigner,
            "OutputPath": output
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
                self.foreigner_path.set(config.get('ForeignerWorkbook', ''))
                self.output_path.set(config.get('OutputPath', 'output/ranked_list.xlsx'))
            messagebox.showinfo("Успех", "Конфигурация загружена!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить конфигурацию:\n{e}")

    def run_processing(self):
        """Запуск обработки данных"""
        if not os.path.exists(CONFIG_FILE) or os.path.getsize(CONFIG_FILE) == 0:
            messagebox.showerror("Ошибка", "Сначала сохраните конфигурацию!")
            return

        try:
            messagebox.showinfo("Обработка", "Обработка данных запущена...\nЭто может занять некоторое время")
            start()  # Вызов вашего pipeline
            messagebox.showinfo("Успех", "Обработка завершена!\nРезультаты сохранены в Excel-файл")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при обработке:\n{e}")


def main():
    root = Tk()
    app = VoteCounterGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
