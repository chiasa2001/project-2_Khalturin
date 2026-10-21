# src/primitive_db/core.py
from typing import Any

from prettytable import PrettyTable

from primitive_db.decorators import confirm_action, handle_db_errors
from primitive_db.parser import make_predicate, parse_condition

VALID_TYPES = {"int", "str", "bool"}


def create_table(metadata: dict[str, Any], table_name: str,
                 columns: list[str]) -> dict[str, Any]:
    """Создаёт таблицу с заданными столбцами."""
    if table_name in metadata:
        raise ValueError(f"Таблица '{table_name}' уже существует.")

    final_columns = ["ID:int"] + columns
    for col in final_columns:
        if ":" not in col:
            raise ValueError(f"Некорректный формат столбца '{col}'.")
        name, dtype = col.split(":", 1)
        if dtype not in VALID_TYPES:
            raise ValueError(
                f"Недопустимый тип данных '{dtype}' для столбца '{name}'."
            )

    metadata[table_name] = final_columns
    print(f"Таблица '{table_name}' успешно создана.")
    return metadata


@confirm_action("удаление таблицы")
@handle_db_errors
def drop_table(metadata: dict[str, Any], table_name: str) -> dict[str, Any]:
    """Удаляет таблицу после подтверждения пользователя."""
    if table_name not in metadata:
        raise ValueError(f"Таблица '{table_name}' не найдена.")
    del metadata[table_name]
    print(f"Таблица '{table_name}' успешно удалена.")
    return metadata


@handle_db_errors
def list_tables(metadata: dict[str, Any]) -> None:
    """Печатает список таблиц с их столбцами."""
    if not metadata:
        print("Таблиц не найдено.")
        return
    print("Список таблиц:")
    for table_name, cols in metadata.items():
        print(f"- {table_name}: {', '.join(cols)}")


def _get_columns_dict(metadata: dict[str, Any], table_name: str) -> dict[str, str]:
    """{'name': 'str', 'age': 'int', 'ID': 'int'} — для удобного доступа к типам."""
    return dict(col.split(":", 1) for col in metadata[table_name])


def _coerce(value: Any, dtype: str) -> Any:
    """Приводит строковое значение к типу согласно метаданным."""
    if dtype == "int":
        return int(value)
    if dtype == "bool":
        if str(value).lower() in ("true", "1", "да"):
            return True
        if str(value).lower() in ("false", "0", "нет"):
            return False
        raise ValueError(f"Значение '{value}' не является bool.")
    return str(value)


@handle_db_errors
def insert_row(metadata: dict[str, Any], table_data: list[dict[str, Any]],
               table_name: str, values: dict[str, Any]) -> list[dict[str, Any]]:
    """Добавляет запись в таблицу. Возвращает обновлённый список данных."""
    if table_name not in metadata:
        raise ValueError(f"Таблица '{table_name}' не найдена.")

    columns = _get_columns_dict(metadata, table_name)

    unknown = set(values) - set(columns)
    missing = set(columns) - {"ID"} - set(values)
    if unknown or missing:
        raise ValueError(
            f"Лишние столбцы {sorted(unknown)}, не заданы {sorted(missing)}."
        )

    row = {col: _coerce(values[col], columns[col]) for col in values}

    new_id = max((r.get("ID", 0) for r in table_data), default=0) + 1
    row = {"ID": new_id, **row}

    table_data.append(row)
    print(f"Добавлена запись: {row}")
    return table_data


@handle_db_errors
def select_rows(table_data: list[dict[str, Any]], columns: dict[str, str],
                where_clause: str | None = None) -> PrettyTable:
    """Выбирает записи. Без условия — все, с условием — только подходящие."""
    if where_clause:
        predicate = make_predicate(*parse_condition(where_clause), columns)
        rows = [r for r in table_data if predicate(r)]
    else:
        rows = table_data

    table = PrettyTable()
    table.field_names = list(columns.keys())
    for r in rows:
        table.add_row([r.get(c, "") for c in columns])
    return table


@handle_db_errors
def update_rows(table_data: list[dict[str, Any]], columns: dict[str, str],
                set_clause: str, where_clause: str) -> list[dict[str, Any]]:
    """Обновляет найденные записи. Возвращает обновлённый список данных."""
    set_field, _, set_value = parse_condition(set_clause)
    if set_field == "ID":
        raise ValueError("Столбец ID изменять нельзя.")
    if set_field not in columns:
        raise ValueError(f"Столбца '{set_field}' нет в таблице.")
    typed_value = _coerce(set_value, columns[set_field])
    predicate = make_predicate(*parse_condition(where_clause), columns)

    count = 0
    for row in table_data:
        if predicate(row):
            row[set_field] = typed_value
            count += 1
    print(f"Обновлено записей: {count}")
    return table_data


@handle_db_errors
def delete_rows(table_data: list[dict[str, Any]], columns: dict[str, str],
                where_clause: str) -> list[dict[str, Any]]:
    """Удаляет записи по условию. Возвращает обновлённый список данных."""
    predicate = make_predicate(*parse_condition(where_clause), columns)
    kept = [r for r in table_data if not predicate(r)]
    print(f"Удалено записей: {len(table_data) - len(kept)}")
    return kept
