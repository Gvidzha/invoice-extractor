# src/inference/ner_extractor.py

import os
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

# Ceļš uz OCR teksta failu
ocr_text_file = "data/ocr_texts/pavadzime_cheks.txt"

# Ielasa OCR tekstu
with open(ocr_text_file, "r", encoding="utf-8") as f:
    text = f.read()

# Ielādē modeli un tokenizatoru
model_dir = "models/saved_model"
tokenizer = AutoTokenizer.from_pretrained(model_dir)
model = AutoModelForTokenClassification.from_pretrained(model_dir)

# Izveido NER pipeline
ner_pipeline = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")

# Palaid ekstrakciju
entities = ner_pipeline(text)

# Izdrukā atrastos elementus
for entity in entities:
    print(f"{entity['word']} ({entity['entity_group']}) - score: {entity['score']:.2f}")
