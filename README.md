## Управление таблицами

### Команды

- `create_table <name> <col1:type1> [col2:type2] ...` — создать таблицу (типы: int, str, bool).
- `drop_table <name>` — удалить таблицу.
- `list_tables` — показать список таблиц.
- `exit` — выход.

### Пример использования

```text
db> create_table users name:str age:int
Таблица 'users' успешно создана.

db> list_tables
Список таблиц:
- users: ID:int, name:str, age:int

db> drop_table users
Таблица 'users' успешно удалена.
## Декораторы

Проект использует декораторы для упрощения кода:

- `handle_db_errors` — перехватывает ошибки (KeyError, ValueError, FileNotFoundError)
  и выводит сообщение вместо падения программы.
- `confirm_action("описание")` — запрашивает подтверждение перед опасными операциями.
- `log_time` — замеряет и выводит время выполнения функции.
- `create_cache()` — кэширует результаты одинаковых запросов `select`.

Пример подтверждения удаления:

```text
db> drop_table users
Вы уверены, что хотите 'удаление таблицы'? [y/n]: y
Таблица 'users' успешно удалена.
