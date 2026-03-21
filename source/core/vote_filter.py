import pandas as pd
from typing import Union, List, Tuple
from source.core.name_mapping import is_name_in_db
import re


def _normalize_fio(name: str) -> str:
    if not isinstance(name, str):
        return ""
    return name.replace("ё", "е").replace("Ё", "Е").strip()


def _extract_st_from_email(email: str) -> str:
    if not isinstance(email, str):
        return ""
    return email.split("@", 1)[0].strip().lower()

def _get_student_record(STsdf: pd.DataFrame, st_code: str):
    st_code = str(st_code).strip().lower()
    mask = STsdf["Корпоративный email"].apply(_extract_st_from_email) == st_code
    matches = STsdf[mask]
    if matches.empty:
        return None
    return matches.iloc[0]



def _get_faculty_choices(row: pd.Series) -> List[str]:
    faculty_columns = [
        "Филология",
        "Медицина",
        "Прикладная математика - процессы управления (ПМ-ПУ)",
        "Биология",
        "Клуб иностранных обучающихся (КИО)",
        "Экономика",
        "Математика и механика (МатМех)",
        "Искусства",
        "Физическая культура и спорт",
        "Журналистика и массовые коммуникации (ВШЖиМК)",
        "Математика и компьютерные науки (МКН)",
        "Философия",
        "Студенческие отряды",
        "Психология",
        "Востоковедение",
        "Социология",
        "Свободные искусства и науки",
        "Политология",
        "Химия",
        "Международные отношения (ФМО)",
        "Теология",
        "Менеджмент (ВШМ)",
        "Институт наук о Земле (ИНоЗ)",
        "История",
        "Юриспруденция",
    ]

    selected = []
    for col in faculty_columns:
        value = row.get(col, "")
        if isinstance(value, (int, float)):
            if pd.isna(value):
                continue
            if value > 0:
                selected.append(col)
        elif isinstance(value, str):
            if value.strip():
                selected.append(col)
    return selected


# def _remove_own_faculty(selected: List[str], student_record: pd.Series) -> List[str]:
#     direction = student_record.get("Направление", "")
#     if not isinstance(direction, str) or not direction.strip():
#         return selected
#
#     result = []
#     for form_name in selected:
#         db_names = is_name_in_db(form_name)
#         if not db_names:
#             result.append(form_name)
#             continue
#
#         mapped = False
#         for db_name in db_names:
#             if db_name in direction:
#                 mapped = True
#                 break
#
#         if not mapped:
#             result.append(form_name)
#
#     return result

def build_result_row(student_record: pd.Series, selected_faculties: List[str], row: pd.Series) -> dict:
    """
    Формирует одну строку результата в формате result_1:
    chat_id, От кого, 1, 2, 3, mail
    """
    chat_id = row.get("ID", "")

    status = row.get("Статус", "")  # колонка статуса в votesTable
    if isinstance(status, str) and status.strip() == "Сотрудник":
        from_faculty = "Сотрудник"
    else:
        # для студентов берем направление из STs
        from_faculty = student_record.get("Направление", "")

    first = selected_faculties[0] if len(selected_faculties) > 0 else ""
    second = selected_faculties[1] if len(selected_faculties) > 1 else ""
    third = selected_faculties[2] if len(selected_faculties) > 2 else ""

    mail = row.get("st", "")

    return {
        "chat_id": chat_id,
        "От кого": from_faculty,
        "1": first,
        "2": second,
        "3": third,
        "mail": mail.lower(),
    }


def process_vote_row(STsdf: pd.DataFrame, row: pd.Series) -> Union[bool, Tuple[str, ...], List[str]]:
    # берем поля из уже отформатированной таблицы голосов
    name = row.get("ФИО", "")
    st = row.get("st", "")
    st = st.replace('S', 's')
    status = row.get("Статус", "")  # колонка статуса

    if not st:
        return False

    # --- ВЕТКА ДЛЯ СОТРУДНИКОВ ---
    if isinstance(status, str) and status.strip() == "Сотрудник":
        # формат st + 6 цифр
        if not re.fullmatch(r"st\d{6}", st):
            return False

        selected_faculties = _get_faculty_choices(row)
        if not selected_faculties or len(selected_faculties) > 3:
            return False

        return tuple(selected_faculties)

    # --- ДАЛЬШЕ ЛОГИКА ДЛЯ СТУДЕНТОВ ---

    # приводим st к нижнему регистру
    student_record = _get_student_record(STsdf, str(st).strip().lower())
    if student_record is None:
        return False

    fio_db_raw = student_record.get("ФИО", None)

    # если ФИО в STs = NaN, проверку совпадения пропускаем
    if not pd.isna(fio_db_raw):
        fio_form = _normalize_fio(str(name))
        fio_db = _normalize_fio(str(fio_db_raw))
        if fio_form != fio_db:
            return False

    selected_faculties = _get_faculty_choices(row)
    if not selected_faculties:
        return False

    # если человек выбрал свой факультет, голос сразу не считаем
    direction = student_record.get("Направление", "")
    if isinstance(direction, str) and direction.strip():
        for form_name in selected_faculties:
            db_names = is_name_in_db(form_name)
            if not db_names:
                continue
            for db_name in db_names:
                if db_name in direction:
                    return False

    if len(selected_faculties) > 3:
        return False

    return tuple(selected_faculties)





def build_result_table(STsdf: pd.DataFrame, votesdf: pd.DataFrame) -> pd.DataFrame:
    result_rows = []
    seen_st = set()

    for _, row in votesdf.iterrows():
        st = row.get("st", "")
        if isinstance(st, str):
            st_key = st.strip().lower().replace("S", "s")
        else:
            st_key = str(st).strip().lower()

        if st_key:
            if st_key in seen_st:
                continue

        selected_faculties = process_vote_row(STsdf, row)
        if selected_faculties is False:
            continue

        status = row.get("Статус", "")
        if isinstance(status, str) and status.strip() == "Сотрудник":
            student_record = None
        else:
            student_record = _get_student_record(STsdf, st_key)
            if student_record is None:
                continue

        row_dict = build_result_row(
            student_record if student_record is not None else pd.Series(),
            list(selected_faculties),
            row
        )
        result_rows.append(row_dict)

        if st_key:
            seen_st.add(st_key)

    if not result_rows:
        return pd.DataFrame(columns=["chat_id", "От кого", "1", "2", "3", "mail"])

    return pd.DataFrame(result_rows)

