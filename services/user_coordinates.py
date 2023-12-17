"""Возвращает текущие координаты пользователя, используя библиотеку geocoder"""

import geocoder

from dataclasses import dataclass

from services.exceptions import CantGetCoordinates
import services.config


@dataclass(slots=True, frozen=True)
class Coordinates:
    latitude: float
    longitude: float


def get_user_coordinates() -> Coordinates:
    """
    Получает округленные или нет координаты пользователя
    params: -
    returns: Координаты пользователя в виде класса Coordinates
    """
    coordinates = _get_coordinates()
    return _round_gps_coordinates(coordinates)


def _get_coordinates() -> Coordinates:
    """
    Получает координаты пользователя с помощью geocoder
    params: -
    returns: Координаты пользователя в виде класса Coordinates
    """
    try:
        coordinates = geocoder.ip("me")
        return Coordinates(latitude=coordinates.lat, longitude=coordinates.lng)
    except Exception:
        raise CantGetCoordinates


def _round_gps_coordinates(coordinates: Coordinates) -> Coordinates:
    """
    Округляет координаты, если это задано в config.py
    params: Координаты пользователя в виде класса Coordinates
    returns: Округленные координаты пользователя в виде класса Coordinates
    """
    if not services.config.USE_ROUND_COORDS:
        return coordinates
    return Coordinates(*map(lambda c: round(c, 1), [coordinates.latitude,
                                                    coordinates.longitude]))
