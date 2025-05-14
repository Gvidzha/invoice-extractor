# src/training/load_annotations.py

from datasets import load_from_disk

def load_train_val():
    return {
        "train": load_from_disk("data/hf_train_dataset"),
        "validation": load_from_disk("data/val_dataset")
    }

if __name__ == "__main__":
    datasets = load_train_val()
    print("Treniņu ieraksts:")
    print(datasets["train"][0])
    print(f"Train kopā: {len(datasets['train'])}, Val kopā: {len(datasets['validation'])}")
