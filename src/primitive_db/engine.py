# src/primitive_db/engine.py
import shlex
from primitive_db.core import create_table, drop_table, list_tables
from primitive_db.utils import load_metadata, save_metadata

HELP = """Доступные команды:
create_table <имя> <столбец:тип> [столбец:тип …] - создать таблицу (типы: int, str, bool)
drop_table <имя>                               - удалить таблицу
list_tables                                    - показать все таблицы
help                                           - показать эту справку
exit                                           - выйти"""

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
        if user_input.lower() in {"exit", "quit"}:
            print("Выход.")
            break
        args = shlex.split(user_input)
        if not args:
            continue
        command = args.lower()
        if command == "create_table":
            if len(args) < 3:
                print("Использование: create_table <имя> <столбец:тип> [столбец:тип …]")
            else:
                metadata = create_table(metadata, args, args[2:])
        elif command == "drop_table":
            if len(args) < 2:
                print("Использование: drop_table <имя>")
            else:
                metadata = drop_table(metadata, args)
        elif command == "list_tables":
            list_tables(metadata)
        elif command == "help":
            print(HELP)
        else:
            print(f"Неизвестная команда: {command}. Введите 'help' для справки.")
    save_metadata(metadata)
