# src\training\train_ner.py

from transformers import (
    AutoTokenizer,
    AutoModelForTokenClassification,
    Trainer,
    TrainingArguments,
    DataCollatorForTokenClassification
)
from datasets import load_from_disk, DatasetDict
import json
from pathlib import Path
import numpy as np

# 1. Datu ielāde un pārbaude
def load_data():
    try:
        train_dataset = load_from_disk("data/train_dataset")
        val_dataset = load_from_disk("data/val_dataset")
        dataset = DatasetDict({
            "train": train_dataset,
            "validation": val_dataset
        })

        if "labels" not in dataset["train"].features:
            raise ValueError("Dataset nesatur 'labels' lauku")
            
        print(f"Ielādēti {len(dataset['train'])} treniņa piemēri")
        return dataset
        
    except Exception as e:
        raise ValueError(f"Datu ielādes kļūda: {str(e)}")

# 2. Tokenizācijas funkcija
def tokenize_and_align(examples):
    tokenized_inputs = tokenizer(
        examples["tokens"],
        truncation=True,
        padding="max_length",
        max_length=128,
        is_split_into_words=True,
        return_tensors="pt"
    )
    
    # Pārveidot labels par skaitļiem
    aligned_labels = []
    for i, labels in enumerate(examples["labels"]):
        word_ids = tokenized_inputs.word_ids(batch_index=i)
        previous_word_idx = None
        label_ids = []
        
        for word_idx in word_ids:
            if word_idx is None:
                label_ids.append(-100)
            elif word_idx != previous_word_idx:
                label_ids.append(label_map[labels[word_idx]])
            else:
                label_ids.append(label_map[labels[word_idx]] if labels[word_idx].startswith("I") else -100)
            previous_word_idx = word_idx
            
        aligned_labels.append(label_ids)
    
    tokenized_inputs["labels"] = aligned_labels
    return tokenized_inputs

def main():
    # 1. Ielādēt datus
    dataset = load_data()
    
    # 2. Ielādēt labelu sarakstu
    with open("data/train_dataset/label_list.json", "r") as f:
        label_list = json.load(f)
    
    # 3. Inicializēt tokenizētāju
    global tokenizer, label_map
    model_name = "bert-base-multilingual-cased"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    label_map = {label: i for i, label in enumerate(label_list)}
    id2label = {i: label for i, label in enumerate(label_list)}
    
    print("\nLietotie entītiju tipi:")
    for label, idx in label_map.items():
        print(f"{idx}: {label}")

    # 4. Tokenizēt datus
    def tokenize_and_align_labels(examples):
        tokenized_inputs = tokenizer(
            examples["tokens"],
            truncation=True,
            padding="max_length",
            max_length=128,
            is_split_into_words=True,
            return_tensors="pt"
        )
        
        # Iegūstam labelus no examples
        labels = []
        for i, label_seq in enumerate(examples["labels"]):
            word_ids = tokenized_inputs.word_ids(batch_index=i)
            label_ids = []
            for word_idx in word_ids:
                if word_idx is None:
                    label_ids.append(-100)
                else:
                    label_ids.append(label_map[label_seq[word_idx]])
            labels.append(label_ids)
        
        tokenized_inputs["labels"] = labels
        return tokenized_inputs
    
    tokenized_dataset = dataset.map(
        tokenize_and_align_labels,
        batched=True,
        remove_columns=['text', 'tokens', 'entities']  # Noņem tikai konkrētās kolonnas
    )

    # 5. Inicializēt modeli
    model = AutoModelForTokenClassification.from_pretrained(
        model_name,
        num_labels=len(label_map),
        id2label=id2label,
        label2id=label_map
    )

    # 6. Datu apstrādes parametri
    data_collator = DataCollatorForTokenClassification(tokenizer)

    # 7. Treniņa parametri
    training_args = TrainingArguments(
        output_dir="./results",
        eval_strategy="epoch",
        eval_steps=500,
        save_strategy="steps",
        save_steps=500,
        learning_rate=2e-5,
        per_device_train_batch_size=8,
        num_train_epochs=3,
        weight_decay=0.01,
        logging_dir="./logs",
        report_to="none"
    )

    # 8. Inicializēt treneri
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset["train"],  # ja dataset ir sadalīts
        eval_dataset=tokenized_dataset["validation"],  # pievienojiet evaluācijas datus
        data_collator=data_collator,
        tokenizer=tokenizer,
    )

    # 9. Trenēt modeli
    print("\nSākam apmācību...")
    trainer.train()
    trainer.save_model("saved_model")
    print("Apmācība pabeigta! Modelis saglabāts: saved_model/")

if __name__ == "__main__":
    main()