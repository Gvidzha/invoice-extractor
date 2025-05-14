# src\preprocessing\merge_annotations.py

import json

# Ceļi uz failiem
file1 = "data/annotations/annotations_1.json"
file2 = "data/annotations/pavadzimes.json"
output_file = "data/annotations/merged_annotations.json"

# Ielādē abus failus
with open(file1, "r", encoding="utf-8") as f1, open(file2, "r", encoding="utf-8") as f2:
    data1 = json.load(f1)
    data2 = json.load(f2)

# Apvieno datus
merged_data = data1 + data2

# Saglabā apvienoto failu
with open(output_file, "w", encoding="utf-8") as f_out:
    json.dump(merged_data, f_out, ensure_ascii=False, indent=2)

print(f"Saglabāts: {output_file} ({len(merged_data)} ieraksti)")
