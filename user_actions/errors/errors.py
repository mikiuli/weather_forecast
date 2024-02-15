"""Пользовательские исключения"""


class MyBaseError(Exception):
    pass


class NoConnectionWithDBError(MyBaseError):
    """Нет связи с базой данных"""
    def __init__(self) -> None:
        message = "Проблемы с подключением к базе данных"
        super().__init__(message)


class CantGetUserCityError(MyBaseError):
    """Программа не может получить название города пользователя"""
    def __init__(self) -> None:
        message = "Программа не может определить Ваше местоположение"
        super().__init__(message)


class APIServiceError(MyBaseError):
    """На сервере произошла ошибка, запрос не может быть обработан"""
    def __init__(self) -> None:
        message = "На сервере произошла ошибка, запрос не может быть обработан"
        super().__init__(message)


class WrongAPIError(MyBaseError):
    """Некорректный API ключ"""
    def __init__(self) -> None:
        message = "Неверный API ключ, программа не может работать"
        super().__init__(message)


class TimeoutServiceError(MyBaseError):
    """Слишком долгое время ожидания ответа сервера"""
    def __init__(self) -> None:
        message = "Слишком долгое время ожидания ответа сервера"
        super().__init__(message)


class UnspecifiedError(MyBaseError):
    """Ошибка при попытке связаться с сервером"""
    def __init__(self) -> None:
        message = ("Произошла ошибка при попытке связаться с сервером, "
                   "попробуйте перезапустить программу")
        super().__init__(message)


class InternetIsNotAvailable(MyBaseError):
    """Нет доступа к интернету"""
    def __init__(self) -> None:
        message = "Для работы программы необходимо подключиться к интернету"
        super().__init__(message)


class WrongCityName(MyBaseError):
    """Пользователь ввёл название города неправильно"""
    pass
