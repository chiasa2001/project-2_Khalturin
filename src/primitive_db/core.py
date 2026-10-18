# src/primitive_db/core.py
from typing import List, Dict, Any

VALID_TYPES = {"int", "str", "bool"}

def create_table(metadata: Dict[str, Any], table_name: str, columns: List[str]) -> Dict[str, Any]:
    if table_name in metadata:
        print(f"Ошибка: таблица '{table_name}' уже существует.")
        return metadata
    final_columns = ["ID:int"] + columns
    for col in final_columns:
        if ":" not in col:
            print(f"Ошибка: некорректный формат столбца '{col}'.")
            return metadata
        name, dtype = col.split(":", 1)
        if dtype not in VALID_TYPES:
            print(f"Ошибка: недопустимый тип данных '{dtype}' для столбца '{name}'.")
            return metadata
    metadata[table_name] = final_columns
    print(f"Таблица '{table_name}' успешно создана.")
    return metadata

def drop_table(metadata: Dict[str, Any], table_name: str) -> Dict[str, Any]:
    if table_name not in metadata:
        print(f"Ошибка: таблица '{table_name}' не найдена.")
        return metadata
    del metadata[table_name]
    print(f"Таблица '{table_name}' успешно удалена.")
    return metadata

def list_tables(metadata: Dict[str, Any]) -> None:
    if not metadata:
        print("Таблиц не найдено.")
        return
    print("Список таблиц:")
    for table_name in metadata.keys():
        print(f"- {table_name}")
