# src/config/ner_config.py

from dataclasses import dataclass

@dataclass
class NERConfig:
    model_name: str = "bert-base-multilingual-cased"
    learning_rate: float = 2e-5
    per_device_train_batch_size: int = 8
    num_train_epochs: int = 3
    weight_decay: float = 0.01
    max_length: int = 128
    output_dir: str = "./results"
    logging_dir: str = "./logs"
    eval_steps: int = 500
    save_steps: int = 500