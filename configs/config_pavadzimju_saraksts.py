# configs\config_pavadzimju_saraksts.py

# Kolonnas, kas satur entītijas
COLUMN_MAPPING = {
    "document_type": "DokumentaNosaukums",  # JSON lauks → CSV kolonna
    "document_number": "Dokumenta Numurs",
    "client": "Klients",
    "amount": "Summa",
    "currency": "Valutaskods",
    "date": "Datums",
}

# Teksta veidošanas veidne (kā apvienot kolonnas)
TEXT_TEMPLATE = (
    "Dokuments: {document_type} | Numurs: {document_number} | "
    "Klients: {client} | Summa: {amount} {currency} | Datums: {date}"
)

# Entītiju tipi un to CSV kolonnas
ENTITY_TYPES = {
    "DOCUMENT_TYPE": "document_type",
    "DOCUMENT_NUMBER": "document_number",
    "CLIENT": "client",
    "AMOUNT": "amount",
    "CURRENCY": "currency",
    "DATE": "date",
}