# src\ner\generate_annotations.py

import pandas as pd
import json
import os
from collections import defaultdict

# Iestatījumi
input_csv = "data/raw/Izverts_pavadzimju_saraksts.csv"
output_json = "data/annotations.json"

# Nolasām CSV failu
try:
    df = pd.read_csv(input_csv, sep=';', encoding='utf-8', dtype=str)
except:
    df = pd.read_csv(input_csv, sep=',', encoding='utf-8', dtype=str)

# Aizvietojam NaN vērtības
df = df.fillna('')

# Entītiju tipu kartēšana
entity_mapping = {
    'DokumentaNosaukums': 'DOCUMENT_TYPE',
    'Dokumenta Numurs': 'DOCUMENT_NUMBER',
    'Klients': 'CLIENT',
    'Pakalpojumu nosaukums': 'SERVICE',
    'Summa': 'AMOUNT',
    'Valutaskods': 'CURRENCY',
    'Datums': 'DATE',
    'DatumsTermiņš': 'DUE_DATE'
}

# Sagatavojam anotācijas
annotations = []

for _, row in df.iterrows():
    # Izveidojam tekstu no atbilstošajiem laukiem
    text_parts = []
    
    # Obligātie lauki
    if 'Dokumenta Numurs' in df.columns and row['Dokumenta Numurs'].strip():
        text_parts.append(f"Nr.{row['Dokumenta Numurs'].strip()}")
    
    if 'Klients' in df.columns and row['Klients'].strip():
        text_parts.append(f"Klientam: {row['Klients'].strip()}")
    
    # Datumu lauki
    if 'Datums' in df.columns and row['Datums'].strip():
        text_parts.append(f"Izsniegts: {row['Datums'].strip()}")
    
    if 'DatumsTermiņš' in df.columns and row['DatumsTermiņš'].strip():
        text_parts.append(f"Termiņš: {row['DatumsTermiņš'].strip()}")
    
    # Finanšu lauki
    if 'Summa' in df.columns and row['Summa'].strip():
        amount = row['Summa'].strip()
        currency = row['Valutaskods'].strip() if 'Valutaskods' in df.columns else ''
        text_parts.append(f"Summa: {amount} {currency}")
    
    if 'Pakalpojumu nosaukums' in df.columns and row['Pakalpojumu nosaukums'].strip():
        text_parts.append(f"Pakalpojums: {row['Pakalpojumu nosaukums'].strip()}")
    
    full_text = " | ".join(text_parts)
    
    # Sagatavojam BIO anotācijas
    tokens = full_text.split()
    labels = ["O"] * len(tokens)
    entities = []

    # Atrodam entītijas tekstā
    for col, label in entity_mapping.items():
        if col in df.columns:
            value = str(row[col]).strip()
            if value:
                start_pos = full_text.find(value)
                if start_pos != -1:
                    end_pos = start_pos + len(value)
                    entities.append({
                        'start': start_pos,
                        'end': end_pos,
                        'label': label
                    })

    # Pārveidojam par BIO anotācijām
    for entity in entities:
        entity_text = full_text[entity['start']:entity['end']]
        entity_tokens = entity_text.split()
        
        # Atrodam tokenu pozīcijas
        for i, token in enumerate(tokens):
            token_start = full_text.find(token)
            token_end = token_start + len(token)
            
            if token_start >= entity['start'] and token_end <= entity['end']:
                if i > 0 and labels[i-1].endswith(entity['label']):
                    labels[i] = f"I-{entity['label']}"
                else:
                    labels[i] = f"B-{entity['label']}"

    annotations.append({
        'text': full_text,
        'tokens': tokens,
        'labels': labels,
        'entities': entities,
        'metadata': {
            'HronoID': row.get('HronoID', ''),
            'GadaID': row.get('GadaID', ''),
            'OrigDoc': row.to_dict()
        }
    })

# Saglabājam anotācijas
os.makedirs(os.path.dirname(output_json), exist_ok=True)
with open(output_json, 'w', encoding='utf-8') as f:
    json.dump(annotations, f, ensure_ascii=False, indent=4, default=str)

print(f"Veiksmīgi saglabāts {len(annotations)} anotētu ierakstu")
print(f"Anotācijas failā: {output_json}")