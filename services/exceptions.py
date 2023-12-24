class CantGetCity(Exception):
    """Программа не может получить название Вашего города"""
    pass


class APIServiceError(Exception):
    """На сервере произошла ошибка, запрос не может быть обработан"""
    pass


class OverloadServiseError(Exception):
    """Сервер перегружен или находится на техническом обслуживании"""
    pass


class TimeoutServiceError(Exception):
    """Слишком долгое время ожидания ответа сервера"""
    pass


class BaseError(Exception):
    """По неизвестным причинам прогноз погоды получить невозможно,
    попробуйте повторить запрос через некоторое время"""
    pass
