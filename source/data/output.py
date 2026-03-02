import pandas as pd
from dataclasses import fields

def export_ranked_list_to_excel(participants, filepath):
    column_order = [
        "Место",
        "Факультет",
        "Количество голосов"
    ]

    if not participants:
        pd.DataFrame(columns=column_order).to_excel(filepath, index=False)
        return

    data = []
    for participant in participants:
        row = {}
        for col in column_order:
            if col == "":
                row[col] == ""
            else:
                row[col] = getattr(participant, col, "")
        data.append(row)

    df = pd.DataFrame(data, columns=column_order)
    df.to_excel(filepath, index=False)