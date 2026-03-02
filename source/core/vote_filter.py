"""
Модуль фильтрации и подсчёта голосов
Здесь реализуется логика отбора строк и определения победителей
"""

import pandas as pd
from typing import Union, List, Tuple


def process_vote_row(row: pd.Series) -> Union[bool, Tuple[str, ...], List[str]]:
    """
    Обрабатывает одну строку голосования и определяет, засчитывается ли голос

    Args:
        row: Строка DataFrame с данными голосования

    Returns:
        - False: если голос не засчитывается
        - tuple/list из 1-3 названий факультетов: если голос засчитывается

    Пример:
        >>> process_vote_row(row)
        False  # голос не подходит

        >>> process_vote_row(row)
        ("Факультет информатики",)  # 1 голос

        >>> process_vote_row(row)
        ("ФИТ", "ГФ", "ЭФ")  # 3 голоса
    """

    # ========================================
    # ЗДЕСЬ ПИШИ СВОЮ ЛОГИКУ ОТБОРА
    # ========================================

    # Пример 1: Простейшая проверка (замени на свою)
    # Проверяем, что есть имя и email
    name = row.get('ФИО', '') or row.get('Имя', '')
    email = row.get('email', '')

    if not name or not email:
        return False  # Пропускаем строку

    # Пример 2: Определение факультетов по ответам
    # Предположим, в колонках есть выборы факультетов
    faculty_choice_1 = row.get('Факультет 1', '')
    faculty_choice_2 = row.get('Факультет 2', '')
    faculty_choice_3 = row.get('Факультет 3', '')

    # Собираем список непустых факультетов (до 3)
    faculties = []
    for choice in [faculty_choice_1, faculty_choice_2, faculty_choice_3]:
        if choice and isinstance(choice, str) and choice.strip():
            faculties.append(choice.strip())

    # Если нет ни одного факультета - пропускаем
    if not faculties:
        return False

    # Возвращаем от 1 до 3 факультетов
    return tuple(faculties[:3])  # Ограничиваем до 3

    # ========================================
    # Другие примеры логики:
    # ========================================

    # Пример 3: Проверка типа студента
    # is_russian = row.get('Тип', '') == 'Русский'
    # if not is_russian:
    #     return False

    # Пример 4: Проверка заполненности определённых полей
    # required_fields = ['ФИО', 'email', 'Факультет']
    # if not all(row.get(field, '') for field in required_fields):
    #     return False

    # Пример 5: Фильтрация по дате
    # vote_date = row.get('Дата голосования')
    # if pd.isna(vote_date) or vote_date < some_deadline:
    #     return False

    # Пример 6: Возврат одного факультета
    # faculty = row.get('Выбранный факультет', '')
    # if faculty:
    #     return (faculty,)
    # else:
    #     return False


def calculate_rankings(df: pd.DataFrame) -> pd.DataFrame:
    """
    Обрабатывает весь DataFrame и формирует ранжированный список

    Args:
        df: DataFrame со всеми данными голосования

    Returns:
        DataFrame с колонками: ['Факультет', 'Голосов', 'Место']
    """

    # Словарь для подсчёта голосов
    vote_counts = {}

    # Проходим по каждой строке
    for index, row in df.iterrows():
        result = process_vote_row(row)

        # Если False - пропускаем
        if result is False:
            continue

        # Если вернулись факультеты - засчитываем голоса
        if isinstance(result, (tuple, list)):
            for faculty in result:
                vote_counts[faculty] = vote_counts.get(faculty, 0) + 1

    # Создаём DataFrame с результатами
    if not vote_counts:
        # Если нет ни одного голоса
        return pd.DataFrame(columns=['Факультет', 'Голосов', 'Место'])

    results_df = pd.DataFrame([
        {'Факультет': faculty, 'Голосов': count}
        for faculty, count in vote_counts.items()
    ])

    # Сортируем по количеству голосов (по убыванию)
    results_df = results_df.sort_values('Голосов', ascending=False).reset_index(drop=True)

    # Добавляем колонку с местом
    results_df['Место'] = range(1, len(results_df) + 1)

    # Переупорядочиваем колонки
    results_df = results_df[['Место', 'Факультет', 'Голосов']]

    return results_df
