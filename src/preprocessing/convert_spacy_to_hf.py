# src\preprocessing\convert_spacy_to_hf.py

import spacy
from spacy.tokens import DocBin
from datasets import Dataset, Features, Value, ClassLabel, Sequence
from pathlib import Path
import json

def convert_spacy_to_hf(spacy_path, output_path):
    nlp = spacy.blank("lv")
    doc_bin = DocBin().from_disk(spacy_path)
    docs = list(doc_bin.get_docs(nlp.vocab))
    
    # Vispirms iegūstam visus unikālos labelus
    all_labels = set()
    for doc in docs:
        for token in doc:
            if token.ent_iob_ != "O":
                all_labels.add(f"{token.ent_iob_}-{token.ent_type_}")
    all_labels.add("O")
    label_list = sorted(list(all_labels))
    
    # Sagatavojam datus
    data = []
    for doc in docs:
        tokens = [token.text for token in doc]
        labels = []
        for token in doc:
            if token.ent_iob_ == "O":
                labels.append("O")
            else:
                labels.append(f"{token.ent_iob_}-{token.ent_type_}")
        
        data.append({
            "id": str(len(data)),
            "tokens": tokens,
            "labels": labels,
            "text": doc.text
        })
    
    # Definējam features struktūru
    features = Features({
        'id': Value('string'),
        'tokens': Sequence(Value('string')),
        'labels': Sequence(ClassLabel(names=label_list)),
        'text': Value('string')
    })
    
    hf_dataset = Dataset.from_list(data, features=features)
    
    # Saglabājam
    Path(output_path).mkdir(parents=True, exist_ok=True)
    hf_dataset.save_to_disk(output_path)
    
    # Saglabājam arī labelu sarakstu
    with open(f"{output_path}/label_list.json", "w") as f:
        json.dump(label_list, f)
    
    print(f"Dati veiksmīgi konvertēti. Atrasti {len(label_list)} entītiju tipi:")
    print(label_list)

if __name__ == "__main__":
    convert_spacy_to_hf(
        spacy_path="data/train_dataset/ner_training.spacy",
        output_path="data/hf_train_dataset"
    )