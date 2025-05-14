# src\training\split_dataset.py

from datasets import Dataset
from sklearn.model_selection import train_test_split

# Ceļš uz anotāciju JSON failu
annotations_file = "data/annotations/merged_annotations.json"

# Ielādē anotācijas no JSON faila
dataset = Dataset.from_json(annotations_file)

# Sadaliet datus treniņa un validācijas kopās (80% treniņam, 20% validācijai)
train_test_split = dataset.train_test_split(test_size=0.2, seed=42)
train_dataset = train_test_split["train"]
val_dataset = train_test_split["test"]

# Saglabā sadalītās datu kopas
train_dataset.save_to_disk("data/train_dataset")
val_dataset.save_to_disk("data/val_dataset")

print(f"Treniņa datu skaits: {len(train_dataset)}")
print(f"Validācijas datu skaits: {len(val_dataset)}")