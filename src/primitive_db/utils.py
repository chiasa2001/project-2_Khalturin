import json
from pathlib import Path

# Вычисляем путь относительно расположения этого файла (src/primitive_db/utils.py)
BASE_DIR = Path(__file__).resolve().parent
METADATA_FILE = BASE_DIR / "db_meta.json"

def load_metadata(filepath: Path | str = METADATA_FILE) -> dict:
    """Загружает метаданные из JSON-файла. Если файл не найден, возвращает пустой словарь."""
    path = Path(filepath)
    try:
        if path.exists():
            with path.open("r", encoding="utf-8") as f:
                return json.load(f)
        return {}
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_metadata(filepath: Path | str = METADATA_FILE, data: dict | None = None) -> None:
    """Сохраняет метаданные в JSON-файл."""
    if data is None:
        data = {}
    path = Path(filepath)
    # Создаем родительскую папку, если её нет (на случай переноса)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
