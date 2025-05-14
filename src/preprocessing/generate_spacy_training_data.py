# src\preprocessing\generate_spacy_training_data.py

import pandas as pd
import spacy
from spacy.tokens import DocBin
import csv

def generate_training_data(csv_path: str, output_path: str):
    # Nolasīt CSV failu
    try:
        df = pd.read_csv(
            csv_path,
            sep='\t',  # Ja dati ir atdalīti ar tabulāciju
            dtype=str,
            quoting=csv.QUOTE_MINIMAL,
            encoding='utf-8'
        )
    except:
        # Ja tabulācija nedarbojas, mēģinām ar komatu
        df = pd.read_csv(
            csv_path,
            sep=',',
            dtype=str,
            quotechar='"',
            encoding='utf-8'
        )

    # Pārbaudām, vai nepieciešamās kolonnas eksistē
    required_columns = [
        'DokumentaNosaukums', 
        'Dokumenta Numurs', 
        'Klients',
        'Pakalpojumu nosaukums',
        'Summa',
        'Valutaskods'
    ]
    
    # Pārveidojam kolonnu nosaukumus, ja tie neatbilst
    df.columns = df.columns.str.strip()
    available_columns = df.columns.tolist()
    
    # Atlasām tikai kolonnas, kas pieejamas
    selected_columns = [col for col in required_columns if col in available_columns]
    df = df[selected_columns].dropna()
    
    # Inicializējam Spacy modeli
    nlp = spacy.blank("lv")
    doc_bin = DocBin()

    for _, row in df.iterrows():
        # Izveidojam tekstu aprakstu
        text_parts = []
        if 'DokumentaNosaukums' in selected_columns:
            text_parts.append(f"Dokuments: {row['DokumentaNosaukums'].strip()}")
        if 'Dokumenta Numurs' in selected_columns:
            text_parts.append(f"Numurs: {row['Dokumenta Numurs'].strip()}")
        if 'Klients' in selected_columns:
            text_parts.append(f"Klients: {row['Klients'].strip()}")
        if 'Pakalpojumu nosaukums' in selected_columns:
            text_parts.append(f"Pakalpojums: {row['Pakalpojumu nosaukums'].strip()}")
        if 'Summa' in selected_columns and 'Valutaskods' in selected_columns:
            text_parts.append(f"Summa: {row['Summa'].strip()} {row['Valutaskods'].strip()}")
        
        text = " ".join(text_parts)
        doc = nlp.make_doc(text)

        # Definējam entītijas
        ents = []
        
        # Pievienojam entītijas katram laukam
        if 'DokumentaNosaukums' in selected_columns:
            doc_name = row['DokumentaNosaukums'].strip()
            start = text.find(doc_name)
            if start != -1:
                ents.append((start, start + len(doc_name), "DOCUMENT_NAME"))
        
        if 'Dokumenta Numurs' in selected_columns:
            doc_num = row['Dokumenta Numurs'].strip()
            start = text.find(doc_num)
            if start != -1:
                ents.append((start, start + len(doc_num), "DOCUMENT_NUMBER"))
        
        # ... (līdzīgi citām kolonnām)

        # Pārveidojam par Spacy entītijām
        spans = [doc.char_span(start, end, label=label) for start, end, label in ents]
        spans = [span for span in spans if span is not None]
        doc.ents = spans
        
        doc_bin.add(doc)

    # Saglabājam treniņu datus
    doc_bin.to_disk(output_path)
    print(f"Saglabāti {len(doc_bin)} treniņu piemēri failā {output_path}")

if __name__ == "__main__":
    generate_training_data(
        csv_path="data/raw/Izverts_pavadzimju_saraksts.csv",
        output_path="data/train_dataset/ner_training.spacy"
    )
