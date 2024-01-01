"""Пользовательские исключения для пакета services"""


class CantGetUserCityError(Exception):
    """Программа не может получить название Вашего города"""
    def __init__(self) -> None:
        message = "Программа не может определить Ваше местоположение"
        super().__init__(message)


class APIServiceError(Exception):
    """На сервере произошла ошибка, запрос не может быть обработан"""
    def __init__(self) -> None:
        message = "На сервере произошла ошибка, запрос не может быть обработан"
        super().__init__(message)


class WrongAPIError(Exception):
    """Некорректный API ключ"""
    def __init__(self) -> None:
        message = "Неверный API ключ, программа не может работать"
        super().__init__(message)


class TimeoutServiceError(Exception):
    """Слишком долгое время ожидания ответа сервера"""
    def __init__(self) -> None:
        message = "Слишком долгое время ожидания ответа сервера"
        super().__init__(message)


class UnspecifiedError(Exception):
    """Ошибка при попытке связаться с сервером"""
    def __init__(self) -> None:
        message = ("Произошла ошибка при попытке связаться с сервером, "
                   "попробуйте перезапустить программу")
        super().__init__(message)
