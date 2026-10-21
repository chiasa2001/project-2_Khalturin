# src/primitive_db/parser.py
from collections.abc import Callable
from typing import Any

_OPERATORS = ["==", "!=", ">=", "<=", ">", "<", "="]


def parse_condition(clause: str) -> tuple[str, str, Any]:
    """Разбирает условие вида 'age > 25' или "name = 'Anna'".
    Возвращает (поле, оператор, значение-строкой)."""
    for op in _OPERATORS:
        if op in clause:
            field, value = clause.split(op, 1)
            field = field.strip()
            value = value.strip().strip("'\"")
            if not field:
                raise ValueError(f"Не указано поле в условии: '{clause}'")
            return field, ("==" if op == "=" else op), value
    raise ValueError(
        f"Некорректное условие: '{clause}'. Ожидается 'поле оператор значение'."
    )

def make_predicate(field: str, op: str, value: Any, columns: dict) -> Callable:
    """Строит функцию-предикат для фильтрации строк."""
    if field not in columns:
        raise ValueError(f"Столбца '{field}' нет в таблице.")

    dtype = columns[field]

    def to_typed(v):
        if dtype == "int":
            return int(v)
        if dtype == "bool":
            if str(v).lower() in ("true", "1", "да"):
                return True
            if str(v).lower() in ("false", "0", "нет"):
                return False
            raise ValueError(f"Значение '{v}' не является bool.")
        return str(v)

    value = to_typed(value)
    ops = {
        "==": lambda a, b: a == b,
        "!=": lambda a, b: a != b,
        ">": lambda a, b: a > b,
        "<": lambda a, b: a < b,
        ">=": lambda a, b: a >= b,
        "<=": lambda a, b: a <= b,
    }

    def predicate(row: dict) -> bool:
        if field not in row or row[field] is None:
            return False
        return ops[op](row[field], value)

    return predicate
