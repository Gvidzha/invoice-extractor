# configs\config_pdb_pvn_maksataji_odata.py

# Kolonnas, kas satur entītijas
COLUMN_MAPPING = {
    "document_type": "Reģistrācijas Numurs",
    "client": "Uzņēmuma nosaukums",
    "date": "Datums Ieslēgšana",
    "end_date": "Datums Izslēgšana",  # Ja nepieciešams
}



# Teksta veidošanas veidne (kā apvienot kolonnas)
TEXT_TEMPLATE = (
    "Reģ. Nr.: {document_type} | Nosaukums: {client} | Ieslēgts: {date} | Izslēgts: {end_date}"
)


# Entītiju tipi un to CSV kolonnas
ENTITY_TYPES = {
    "DOCUMENT_TYPE": "document_type",
    "CLIENT": "client",
    "DATE": "date",
    "END_DATE": "end_date",
}
