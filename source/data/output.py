import pandas as pd
import os


def export_results_to_excel(result_df: pd.DataFrame, output_path: str = "output/result.xlsx"):
    """
    Экспортирует таблицу результатов (формат result_1) в Excel.
    Ожидаются колонки: ['chat_id', 'От кого', '1', '2', '3', 'mail'].
    """
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    result_df.to_excel(output_path, index=False, sheet_name="Результаты")
    print(f"Результаты сохранены: {output_path}")

