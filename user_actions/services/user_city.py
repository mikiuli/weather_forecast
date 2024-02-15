"""Возвращает текущие координаты пользователя, используя библиотеку ipinfo"""

import ipinfo

from user_actions.errors import errors


def get_user_city_name(ipinfo_access_token: str) -> str:
    """
    Получает название города пользователя с помощью geocoder
    params: ipinfo_access_token: токен для использования библиотеки ipinfo
    returns: Название города в виде строки
    """
    try:
        handler = ipinfo.getHandler(access_token=ipinfo_access_token)
        details = handler.getDetails()
        return details.city
    except Exception:
        raise errors.CantGetUserCityError()
