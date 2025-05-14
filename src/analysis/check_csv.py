# src\analysis\check_csv.py

import pandas as pd

df = pd.read_csv("data/raw/Izverts_pavadzimju_saraksts.csv")
print(f"Kolonnas: {df.columns.tolist()}")
print("\nPirmās 3 rindas:")
print(df[['DokumentaNosaukums', 'Klients', 'Dokumenta Numurs']].head(3))