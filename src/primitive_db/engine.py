# src/primitive_db/engine.py
import shlex

from primitive_db.core import (
    _get_columns_dict,
    create_table,
    delete_rows,
    drop_table,
    insert_row,
    list_tables,
    select_rows,
    update_rows,
)
from primitive_db.decorators import log_time
from primitive_db.utils import (
    load_metadata,
    load_table_data,
    save_metadata,
    save_table_data,
)

HELP = """Доступные команды:
create_table <имя> <столбец:тип> [столбец:тип ...] - создать таблицу (типы: int, str, bool)
drop_table <имя>                                  - удалить таблицу
list_tables                                       - показать все таблицы
insert <таблица> <столбец=значение> [...]         - добавить запись
select <таблица> [where <условие>]                - показать записи
update <таблица> set <столбец=значение> where <условие> - обновить записи
delete <таблица> where <условие>                  - удалить записи
help                                              - показать эту справку
exit                                              - выйти"""

# "Медленные" операции оборачиваем в декоратор замера времени
timed_select = log_time(select_rows)
timed_insert = log_time(insert_row)


def run() -> None:
    print("Creative DB. Введите 'help' для справки, 'exit' для выхода.")
    metadata = load_metadata()
    while True:
        try:
            user_input = input("db> ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nВыход.")
            break

        if not user_input:
            continue

        args = shlex.split(user_input)
        command = args[0].lower()

        if command in ("exit", "quit"):
            print("Выход.")
            break

        if command == "help":
            print(HELP)
            continue

        if command == "create_table":
            if len(args) < 3:
                print("Использование: create_table <имя> <столбец:тип> [столбец:тип ...]")
            else:
                metadata = create_table(metadata, args[1], args[2:])
                if metadata is None:
                    metadata = load_metadata()

        elif command == "drop_table":
            if len(args) < 2:
                print("Использование: drop_table <имя>")
            else:
                new_metadata = drop_table(metadata, args[1])
                if new_metadata is not None:
                    metadata = new_metadata

        elif command == "list_tables":
            list_tables(metadata)

        elif command == "insert":
            # insert users name=Ilya age=25
            if len(args) < 3:
                print("Использование: insert <таблица> <столбец=значение> [...]")
            else:
                table_name = args[1]
                values = {}
                ok = True
                for pair in args[2:]:
                    if "=" not in pair:
                        print(f"Ошибка: неверный формат '{pair}', ожидается столбец=значение.")
                        ok = False
                        break
                    key, value = pair.split("=", 1)
                    values[key] = value
                if ok:
                    table_data = load_table_data(table_name)
                    result = timed_insert(metadata, table_data, table_name, values)
                    if result is not None:
                        table_data = result
                        save_table_data(table_name, table_data)

        elif command == "select":
            # select users [where age > 18]
            if len(args) < 2:
                print("Использование: select <таблица> [where <условие>]")
            else:
                table_name = args[1]
                where = None
                if len(args) >= 4 and args[2].lower() == "where":
                    where = " ".join(args[3:])
                if table_name not in metadata:
                    print(f"Ошибка: таблица '{table_name}' не найдена.")
                else:
                    table_data = load_table_data(table_name)
                    result = timed_select(
                        table_data,
                        _get_columns_dict(metadata, table_name),
                        where,
                    )
                    if result is not None:
                        print(result)

        elif command == "update":
            # update users set age=26 where name = Ilya
            if len(args) < 6 or args[2].lower() != "set" or "where" not in [a.lower() for a in args]:
                print("Использование: update <таблица> set <столбец=значение> where <условие>")
            else:
                table_name = args[1]
                where_idx = next(i for i, a in enumerate(args) if a.lower() == "where")
                set_clause = args[3]
                where_clause = " ".join(args[where_idx + 1:])
                if table_name not in metadata:
                    print(f"Ошибка: таблица '{table_name}' не найдена.")
                else:
                    table_data = load_table_data(table_name)
                    result = update_rows(
                        table_data,
                        _get_columns_dict(metadata, table_name),
                        set_clause, where_clause,
                    )
                    if result is not None:
                        save_table_data(table_name, result)

        elif command == "delete":
            # delete users where ID = 1
            if len(args) < 4 or args[2].lower() != "where":
                print("Использование: delete <таблица> where <условие>")
            else:
                table_name = args[1]
                where_clause = " ".join(args[3:])
                if table_name not in metadata:
                    print(f"Ошибка: таблица '{table_name}' не найдена.")
                else:
                    table_data = load_table_data(table_name)
                    result = delete_rows(
                        table_data,
                        _get_columns_dict(metadata, table_name),
                        where_clause,
                    )
                    if result is not None:
                        save_table_data(table_name, result)

        else:
            print(f"Неизвестная команда: {command}. Введите 'help'.")

    save_metadata(metadata)
