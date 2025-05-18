# src/training/train_ner.py

from transformers import (
    AutoTokenizer,
    AutoModelForTokenClassification,
    Trainer,
    TrainingArguments,
    DataCollatorForTokenClassification
)
from datasets import load_from_disk, DatasetDict
import json
import argparse
from pathlib import Path
import numpy as np
from src.config.ner_config import NERConfig

def load_data(data_path: str):
    try:
        train_dataset = load_from_disk(f"{data_path}/train_dataset")
        val_dataset = load_from_disk(f"{data_path}/val_dataset")
        dataset = DatasetDict({
            "train": train_dataset,
            "validation": val_dataset
        })

        if "labels" not in dataset["train"].features:
            raise ValueError("Dataset nesatur 'labels' lauku")
            
        print(f"Ielādēti {len(dataset['train'])} treniņa piemēri")
        return dataset
        
    except Exception as e:
        raise ValueError(f"Datu ielādes kļūda: {str(e)}") from e

def tokenize_and_align_labels(examples, tokenizer, label_map, max_length):
    tokenized_inputs = tokenizer(
        examples["tokens"],
        truncation=True,
        padding="max_length",
        max_length=max_length,
        is_split_into_words=True,
        return_tensors="np"
    )
    
    labels = []
    for i, label_seq in enumerate(examples["labels"]):
        word_ids = tokenized_inputs.word_ids(batch_index=i)
        previous_word_idx = None
        label_ids = []
        
        for word_idx in word_ids:
            if word_idx is None:
                label_ids.append(-100)
            elif word_idx != previous_word_idx:
                label_ids.append(label_map[label_seq[word_idx]])
            else:
                label_ids.append(label_map[label_seq[word_idx]] if label_seq[word_idx].startswith("I") else -100)
            previous_word_idx = word_idx
            
        labels.append(label_ids)
    
    tokenized_inputs["labels"] = labels
    return tokenized_inputs

def load_label_map(label_path: str):
    with open(f"{label_path}/label_list.json", "r") as f:
        label_list = json.load(f)
    return {label: i for i, label in enumerate(label_list)}

def print_label_info(label_map):
    print("\nLietotie entītiju tipi:")
    for label, idx in label_map.items():
        print(f"{idx}: {label}")

def setup_training(config: NERConfig, data_path: str = "data", label_path: str = "data/train_dataset"):
    # 1. Ielādēt datus
    dataset = load_data(data_path)
    
    # 2. Ielādēt labelu sarakstu
    label_map = load_label_map(label_path)
    id2label = {i: label for label, i in label_map.items()}
    print_label_info(label_map)

    # 3. Inicializēt tokenizētāju
    tokenizer = AutoTokenizer.from_pretrained(config.model_name)

    # 4. Tokenizēt datus
    tokenized_dataset = dataset.map(
        lambda examples: tokenize_and_align_labels(
            examples, tokenizer, label_map, config.max_length
        ),
        batched=True,
        remove_columns=['text', 'tokens', 'entities']
    )

    # 5. Inicializēt modeli
    model = AutoModelForTokenClassification.from_pretrained(
        config.model_name,
        num_labels=len(label_map),
        id2label=id2label,
        label2id=label_map
    )

    # 6. Datu apstrādes parametri
    data_collator = DataCollatorForTokenClassification(tokenizer)

    # 7. Treniņa parametri
    training_args = TrainingArguments(
        output_dir=config.output_dir,
        eval_strategy="epoch",
        eval_steps=config.eval_steps,
        save_strategy="steps",
        save_steps=config.save_steps,
        learning_rate=config.learning_rate,
        per_device_train_batch_size=config.per_device_train_batch_size,
        num_train_epochs=config.num_train_epochs,
        weight_decay=config.weight_decay,
        logging_dir=config.logging_dir,
        report_to="none"
    )

    # 8. Inicializēt treneri
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset["train"],
        eval_dataset=tokenized_dataset["validation"],
        data_collator=data_collator,
        tokenizer=tokenizer,
    )

    return trainer

def main():
    parser = argparse.ArgumentParser(description='Train NER model')
    parser.add_argument('--config', type=str, default=None, help='Path to config file')
    parser.add_argument('--data_path', type=str, default='data', help='Path to training data')
    parser.add_argument('--label_path', type=str, default='data/train_dataset', help='Path to label files')
    args = parser.parse_args()

    # Load config (use default if not specified)
    config = NERConfig()
    if args.config:
        import yaml
        with open(args.config) as f:
            config_data = yaml.safe_load(f)
            config = NERConfig(**config_data)

    trainer = setup_training(config, args.data_path, args.label_path)

    # 9. Trenēt modeli
    print("\nSākam apmācību...")
    trainer.train()
    trainer.save_model("saved_model")
    print("Apmācība pabeigta! Modelis saglabāts: saved_model/")

if __name__ == "__main__":
    main()