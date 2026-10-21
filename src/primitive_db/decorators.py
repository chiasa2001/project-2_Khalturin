# src/primitive_db/decorators.py
import functools
import time
from collections.abc import Callable
from typing import Any


def handle_db_errors(func: Callable) -> Callable:
    """Перехватывает ошибки БД и выводит сообщение вместо падения программы."""
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except (ValueError, KeyError, FileNotFoundError) as e:
            print(f"Ошибка: {e}")
            return None
    return wrapper


def confirm_action(description: str) -> Callable:
    """Фабрика декораторов: перед выполнением просит подтвердить действие."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            answer = input(f"Вы уверены, что хотите '{description}'? [y/n]: ")
            if answer.strip().lower() != "y":
                print("Операция отменена.")
                return None
            return func(*args, **kwargs)
        return wrapper
    return decorator


def log_time(func: Callable) -> Callable:
    """Замеряет время выполнения функции и выводит его в консоль."""
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time.monotonic()
        result = func(*args, **kwargs)
        elapsed = time.monotonic() - start
        print(f"Функция '{func.__name__}' выполнялась за {elapsed:.2f} сек.")
        return result
    return wrapper

def create_cache() -> Callable:
    """Возвращает функцию-кэш: результаты запоминаются по аргументам."""
    cache: dict = {}

    def cache_result(value_func: Callable) -> Callable:
        @functools.wraps(value_func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            key = (args, tuple(sorted(kwargs.items())))
            if key in cache:
                return cache[key]
            result = value_func(*args, **kwargs)
            cache[key] = result
            return result
        return wrapper

    def clear() -> None:
        cache.clear()

    cache_result.clear = clear
    return cache_result
