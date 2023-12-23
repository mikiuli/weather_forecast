"""Возвращает текущие координаты пользователя, используя библиотеку geocoder"""

import geocoder

from services.exceptions import CantGetCity


def get_user_city_name() -> str:
    """
    Получает название города пользователя с помощью geocoder
    params: -
    returns: Название города в виде строки
    """
    try:
        coordinates = geocoder.ip("me")
        return coordinates.city
    except Exception:
        raise CantGetCity
