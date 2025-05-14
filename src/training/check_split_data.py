# src\training\check_split_data.py

from datasets import load_from_disk

# Ielādē treniņa un validācijas kopas
train_dataset = load_from_disk("data/train_dataset")
val_dataset = load_from_disk("data/val_dataset")

# Izdrukā treniņa un validācijas datu piemērus
print("Treniņa datu piemērs:")
print(train_dataset[0])  # Izdrukā pirmo ierakstu no treniņa datiem

print("\nValidācijas datu piemērs:")
print(val_dataset[0])  # Izdrukā pirmo ierakstu no validācijas datiem

# Izdrukā kopējo ierakstu skaitu
print(f"\nTreniņa datu skaits: {len(train_dataset)}")
print(f"Validācijas datu skaits: {len(val_dataset)}")