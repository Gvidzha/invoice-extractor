# src\preprocessing\csv_to_json.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


import pandas as pd
import json
from pathlib import Path
from typing import Dict, List
from configs.config_pdb_pvn_maksataji_odata import (  # Importē konfigu atbilstoši failam
    COLUMN_MAPPING,
    TEXT_TEMPLATE,
    ENTITY_TYPES,
)

def csv_to_json(csv_path: str, output_path: str) -> None:
    # 1. Ielasīt CSV
    df = pd.read_csv(csv_path, sep='\t')
    df = df.fillna("")

    # 2. Pārveidot katru ierakstu
    annotations = []
    for _, row in df.iterrows():
        # 2a. Izveidot tekstu no veidnes
        text = TEXT_TEMPLATE.format(**{
            key: row[csv_col] for key, csv_col in COLUMN_MAPPING.items()
        })

        # 2b. Identificēt entītijas
        entities = []
        for entity_label, col_key in ENTITY_TYPES.items():
            value = str(row[COLUMN_MAPPING[col_key]])
            if value:
                start = text.find(value)
                if start != -1:
                    entities.append({
                        "text": value,
                        "label": entity_label,
                        "start": start,
                        "end": start + len(value),
                    })

        # 2c. Tokenizēt un marķēt BIO/IOB
        tokens = text.split()  # Vienkāršota tokenizācija
        labels = ["O"] * len(tokens)
        
        for ent in entities:
            # Atrod tokenus, kas pārklājas ar entītiju
            for i, token in enumerate(tokens):
                token_start = text.find(token)
                token_end = token_start + len(token)
                if (ent["start"] <= token_start < ent["end"]) or (ent["start"] < token_end <= ent["end"]):
                    prefix = "B-" if labels[i] == "O" else "I-"
                    labels[i] = f"{prefix}{ent['label']}"

        # 2d. Pievienot JSON
        annotations.append({
            "text": text,
            "tokens": tokens,
            "labels": labels,
            "entities": entities,
        })

    # 3. Saglabāt JSON
    Path(output_path).parent.mkdir(exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(annotations, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    csv_to_json(
        csv_path="data/raw/pdb_pvnmaksataji_odata.csv",
        output_path="data/annotations/annotations_1.json",
    )