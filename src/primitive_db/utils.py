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

def save_metadata(data: dict | None = None) -> None:
    """Сохраняет метаданные в JSON-файл."""
    if data is None:
        data = {}
    path = Path(METADATA_FILE)
    # Создаем родительскую папку, если её нет (на случай переноса)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# Папка для хранения данных таблиц: data/<имя_таблицы>.json
DATA_DIR = BASE_DIR / "data"

def load_table_data(table_name: str) -> list:
    """Загружает данные таблицы из data/<table_name>.json.
    Если файла нет, возвращает пустой список."""
    path = DATA_DIR / f"{table_name}.json"
    try:
        if path.exists():
            with path.open("r", encoding="utf-8") as f:
                return json.load(f)
        return []
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_table_data(table_name: str, data: list) -> None:
    """Сохраняет данные таблицы в data/<table_name>.json."""
    path = DATA_DIR / f"{table_name}.json"
    # Создаем папку data, если её ещё нет
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
