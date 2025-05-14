# src\utils\analyze_data.py

from collections import Counter
import json

# Ielādē anotācijas
with open("c:\\Code\\Invoice_extractor\\data\\annotations.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Apkopo klases
all_labels = [label for example in data for label in example["labels"]]
label_counts = Counter(all_labels)

# Izdrukā statistiku
print("Klases sadalījums:")
for label, count in label_counts.items():
    print(f"{label}: {count}")
