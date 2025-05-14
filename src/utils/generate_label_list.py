# src/utils/generate_label_list.py

import json
from pathlib import Path

def extract_labels(annotations_file: str) -> list:
    """Iegūst unikālos labelus no annotations.json."""
    with open(annotations_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    labels = set()
    for item in data:
        for label in item.get("labels", []):
            labels.add(label)  # Pievieno visus labelus, ieskaitot "O"
    return sorted(labels)

def save_label_list(labels: list, output_path: str):
    """Saglabā labelu sarakstu."""
    Path(output_path).parent.mkdir(exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(labels, f, indent=4)
    print(f"Labelu saraksts saglabāts: {output_path}")

if __name__ == "__main__":
    # Izmantojiet jūsu annotations failu (piem., pavadzimes.json)
    annotations_file = "data/annotations/merged_annotations.json"
    output_path = "data/train_dataset/label_list.json"  # Vai "data/hf_train_dataset/label_list.json"
    
    labels = extract_labels(annotations_file)
    save_label_list(labels, output_path)