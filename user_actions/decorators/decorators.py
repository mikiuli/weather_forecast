"""Декораторы для функций из weather_forecast для отлова предполагаемых
ошибок"""

import sys
from typing import Callable
from functools import wraps

from user_actions.errors.errors import MyBaseError


def errors_manager(custom_exception: MyBaseError) -> Callable:
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
                return func(*args, **kwargs)
            except custom_exception as e:
                print(e)
                sys.exit()
        return wrapper
    return decorator
