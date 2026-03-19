import pandas as pd
from typing import Union, List, Tuple
from source.core.name_mapping import is_name_in_db


def _normalize_fio(name: str) -> str:
    if not isinstance(name, str):
        return ""
    return name.replace("ё", "е").replace("Ё", "Е").strip()


def _extract_st_from_email(email: str) -> str:
    if not isinstance(email, str) or "@" not in email:
        return ""
    return email.split("@", 1)[0].strip()


def _get_student_record(STsdf: pd.DataFrame, st_code: str):
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


def _remove_own_faculty(selected: List[str], student_record: pd.Series) -> List[str]:
    direction = student_record.get("Направление", "")
    if not isinstance(direction, str) or not direction.strip():
        return selected

    result = []
    for form_name in selected:
        db_names = is_name_in_db(form_name)
        if not db_names:
            result.append(form_name)
            continue

        mapped = False
        for db_name in db_names:
            if db_name in direction:
                mapped = True
                break

        if not mapped:
            result.append(form_name)

    return result


def process_vote_row(
    STsdf: pd.DataFrame, row: pd.Series
) -> Union[bool, Tuple[str, ...], List[str]]:
    name = row.get("ФИО", "")
    st = row.get("st", "")

    if not name or not st:
        return False

    student_record = _get_student_record(STsdf, str(st).strip())
    if student_record is None:
        return False

    fio_form = _normalize_fio(str(name))
    fio_db = _normalize_fio(str(student_record.get("ФИО", "")))
    if fio_form != fio_db:
        return False

    selected_faculties = _get_faculty_choices(row)
    if not selected_faculties:
        return False

    filtered_faculties = _remove_own_faculty(selected_faculties, student_record)
    if not filtered_faculties or len(filtered_faculties) > 3:
        return False

    return tuple(filtered_faculties)


def calculate_rankings(STsdf: pd.DataFrame, votesdf: pd.DataFrame) -> pd.DataFrame:
    vote_counts = {}

    for _, row in votesdf.iterrows():
        result = process_vote_row(STsdf, row)
        if result is False:
            continue

        if isinstance(result, (tuple, list)):
            for faculty in result:
                vote_counts[faculty] = vote_counts.get(faculty, 0) + 1

    if not vote_counts:
        return pd.DataFrame(columns=["Факультет", "Голосов", "Место"])

    results_df = pd.DataFrame(
        [{"Факультет": f, "Голосов": c} for f, c in vote_counts.items()]
    )
    results_df = results_df.sort_values("Голосов", ascending=False).reset_index(
        drop=True
    )
    results_df["Место"] = range(1, len(results_df) + 1)
    results_df = results_df[["Место", "Факультет", "Голосов"]]

    return results_df
