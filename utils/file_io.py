import json
from pathlib import Path
from typing import Any


def save_json(data: Any, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_json(input_path: Path) -> Any:
    with open(input_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_text(text: str, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)


def load_text(input_path: Path) -> str:
    with open(input_path, "r", encoding="utf-8") as f:
        return f.read()