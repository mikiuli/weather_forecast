"""Возвращает текущие координаты пользователя, используя библиотеку geocoder"""

import geocoder

from services.exceptions import CantGetUserCityError


def get_user_city_name() -> str:
    """
    Получает название города пользователя с помощью geocoder
    params: -
    returns: Название города в виде строки
    """
    try:
        coordinates = geocoder.ip("me")
        return coordinates.city
    except AttributeError:
        raise CantGetUserCityError()
