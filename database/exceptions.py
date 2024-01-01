"""Пользовательские исключения для пакета database"""


class NoConnectionWithDBError(Exception):
    """Нет связи с базой данных"""
    def __init__(self) -> None:
        message = "Проблемы с подключением к базе данных"
        super().__init__(message)
