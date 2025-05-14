# src\analysis\check_entities.py

import spacy
from spacy.tokens import DocBin

def check_spacy_entities(spacy_path):
    nlp = spacy.blank("lv")  # Izmantojam to pašu valodu
    doc_bin = DocBin().from_disk(spacy_path)
    docs = list(doc_bin.get_docs(nlp.vocab))
    
    print(f"\nKopējais dokumentu skaits: {len(docs)}")
    
    entity_counts = {}
    for i, doc in enumerate(docs[:3]):  # Pārbaudam pirmos 3 dokumentus
        print(f"\n--- Dokuments {i+1} ---")
        print("Teksts:", doc.text)
        
        if not doc.ents:
            print("Nav atrastas entītītes!")
        else:
            for ent in doc.ents:
                print(f"Entītija: '{ent.text}' ({ent.label_})")
                entity_counts[ent.label_] = entity_counts.get(ent.label_, 0) + 1
    
    print("\nAtrastie entītiju tipi un to skaits:")
    for label, count in entity_counts.items():
        print(f"{label}: {count}")

if __name__ == "__main__":
    check_spacy_entities("data/train_dataset/ner_training.spacy")