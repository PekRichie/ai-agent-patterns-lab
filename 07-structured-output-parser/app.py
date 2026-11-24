"""Strukturált LLM JSON-kimenet kinyerő, séma-validátor és javító retry-hurok."""
import json
import re
from typing import Callable


def extract_json_block(text: str) -> str:
    fenced = re.search(r"```(?:json)?\s*(\{.*?\}|\[.*?\])\s*```", text, re.S)
    if fenced:
        return fenced.group(1)
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end > start:
        return text[start : end + 1]
    raise ValueError("Nem található JSON objektum az LLM kimenetében.")


def validate_schema(obj: dict, required_types: dict[str, type]) -> list[str]:
    errors = []
    for key, expected_type in required_types.items():
        if key not in obj:
            errors.append(f"Hiányzó mező: {key}")
        elif not isinstance(obj[key], expected_type):
            errors.append(f"Hibás típus ({key}): várt {expected_type.__name__}, kapott {type(obj[key]).__name__}")
    return errors


def parse_with_repair(
    llm_call: Callable[[str | None], str],
    required_types: dict[str, type],
    max_retries: int = 2,
) -> dict:
    feedback: str | None = None
    for _ in range(max_retries + 1):
        raw = llm_call(feedback)
        try:
            obj = json.loads(extract_json_block(raw))
            if not isinstance(obj, dict):
                raise ValueError("A gyökérelemnek JSON objektumnak kell lennie.")
            errs = validate_schema(obj, required_types)
            if not errs:
                return obj
            feedback = "; ".join(errs)
        except Exception as exc:
            feedback = str(exc)
    raise ValueError(f"Séma-validáció sikertelen {max_retries} javítás után: {feedback}")
