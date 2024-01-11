"""Декораторы для функций из weather_forecast для отлова предполагаемых
ошибок"""

import sys
from typing import Callable
from functools import wraps

import requests

from errors.errors import CustomExceptionTuple


def internet_manager(internet_connection_error) -> Callable:
    """
    Декоратор
    Проверяет подключение пользователя к интернету,
    возвращает ошибку при его отсутствии
    params: func: функция, чувствительная к наличию интернета
    returns: декоратор"""
    def decorator(func) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> None:
            try:
                requests.get("https://github.com", timeout=3)
            except Exception:
                raise internet_connection_error()
            func(*args, **kwargs)
        return wrapper
    return decorator


def errors_manager(custom_exceptions:
                   CustomExceptionTuple) -> Callable:
    """
    Декоратор
    Отлавливает пользовательские ошибки и завершает работу программы
    при наличии ошибок
    params: custom_exceptions: кортеж пользовательских ошибок
    из errors.errors
    returns: декоратор
    """
    def decorator(func) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> None:
            try:
                func(*args, **kwargs)
            except custom_exceptions as e:
                print(e)
                sys.exit()
        return wrapper
    return decorator
