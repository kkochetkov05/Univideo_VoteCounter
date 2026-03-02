import pandas as pd
import os


def export_ranked_list_to_excel(ranked_df: pd.DataFrame, output_path: str = "output/ranked_list.xlsx"):
    """
    Экспортирует ранжированный список в Excel

    Args:
        ranked_df: DataFrame с колонками ['Место', 'Факультет', 'Голосов']
        output_path: Путь для сохранения файла
    """

    # Создаём директорию, если не существует
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Экспорт в Excel
    ranked_df.to_excel(output_path, index=False, sheet_name='Рейтинг')

    print(f"Результаты сохранены: {output_path}")
