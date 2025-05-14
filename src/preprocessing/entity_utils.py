# src\preprocessing\entity_utils.py

from typing import List, Dict

def validate_entities(text: str, entities: List[Dict]) -> bool:
    """Pārbauda, vai entītiju pozīcijas atbilst tekstam."""
    for ent in entities:
        if text[ent["start"]:ent["end"]] != ent["text"]:
            return False
    return True


def improve_tokenization(text: str) -> List[str]:
    """Uzlabota tokenizācija (var pielāgot)."""
    return text.split()  # Var aizstāt ar spaCy tokenizeru