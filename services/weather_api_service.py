"""Получает погоду с сервиса openweathermap с помощью библиотеки requests,
отправляет в формате Weather"""

import requests

from dataclasses import dataclass
import json
from json.decoder import JSONDecodeError

from typing import TypeAlias

from http import HTTPStatus

import services.config
from services import exceptions

Celsius: TypeAlias = int
metres_per_sec: TypeAlias = int
Unix_time: TypeAlias = int


@dataclass(slots=True, frozen=True)
class Weather:
    current_time: Unix_time
    city: str

    weather_type: str
    temperature: Celsius
    temperature_feels_like: Celsius
    wind_speed: metres_per_sec


def get_weather(city_name: str) -> Weather:
    """
    Получает прогноз погоды от вебсервиса OpenWeather и
    возвращает в виде класса Weather
    params: city_name: имя города, погоду в котором хочет получить пользователь
    returns: погоду в виде класса Weather
    """
    openweather_response = _get_openweather_response(
        city_name=city_name
    )
    if isinstance(openweather_response, int):
        return openweather_response
    else:
        weather = _parse_openweather_response(openweather_response)
        return weather


def _get_openweather_response(city_name: str) -> str:
    """
    Получает ответ от сервера, райзит ошибку, если проблемы с соединением
    params: city_name: имя города, погоду в котором хочет получить пользователь
    returns: Возвращает тело полученного ответа в виде текса
    """
    url = services.config.OPENWEATHER_URL.format(city_name=city_name)
    try:
        response = requests.get(url=url, timeout=3)
    except requests.exceptions.Timeout:
        raise exceptions.TimeoutServiceError()
    if response.status_code == HTTPStatus.OK:
        return response.text
    elif response.status_code == HTTPStatus.NOT_FOUND:
        return response.status_code
    elif response.status_code == HTTPStatus.UNAUTHORIZED:
        raise exceptions.WrongAPIError()
    elif response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        raise exceptions.APIServiceError()
    else:
        raise exceptions.UnspecifiedError()


def _parse_openweather_response(openweather_response: str) -> Weather:
    """
    Превращает текстовый ответ сервера в словарь и парсит его
    params: openweather_response: тело полученного ответа в виде текса
    returns: погоду в виде класса Weather
    """
    try:
        openweather_dict = json.loads(openweather_response)
    except JSONDecodeError:
        print("""По неизвестным причинам прогноз погоды получить невозможно,
              попробуйте повторить запрос через некоторое время""")
        raise exceptions.APIServiceError()
    return Weather(
        current_time=_parse_current_time(openweather_dict),
        city=_parse_city_name(openweather_dict),
        weather_type=_parse_weather_type(openweather_dict),
        temperature=_parse_temperature(openweather_dict),
        temperature_feels_like=_parse_temp_feels_like(openweather_dict),
        wind_speed=_parse_wind_speed(openweather_dict)
    )


def _parse_current_time(openweather_dict: dict) -> Unix_time:
    """
    Получает текущее время из словаря
    params: openweather_dict: словарь
    returns: время в юникс формате
    """
    try:
        return openweather_dict["dt"]
    except KeyError:
        raise exceptions.BaseError()


def _parse_city_name(openweather_dict: dict) -> str:
    """
    Получает имя города
    params: openweather_dict: словарь
    returns: имя города
    """
    try:
        return openweather_dict["name"]
    except KeyError:
        raise exceptions.BaseError()


def _parse_temperature(openweather_dict: dict) -> Celsius:
    """
    Получает температуру
    params: openweather_dict: словарь
    returns: температуру в цельсиях
    """
    try:
        return round(openweather_dict["main"]["temp"])
    except KeyError:
        raise exceptions.BaseError()


def _parse_temp_feels_like(openweather_dict) -> Celsius:
    """
    Получает температуру "ощущается как"
    params: openweather_dict: словарь
    returns: температуру "ощущается как"
    """
    try:
        return round(openweather_dict["main"]["feels_like"])
    except KeyError:
        raise exceptions.BaseError()


def _parse_wind_speed(openweather_dict: dict) -> metres_per_sec:
    """
    Получает скорость ветра
    params: openweather_dict: словарь
    returns: скорость ветра
    """
    try:
        return round(openweather_dict["wind"]["speed"])
    except KeyError:
        raise exceptions.BaseError()


def _parse_weather_type(openweather_dict: dict) -> str:
    """
    Получает описание погоды
    params: openweather_dict: словарь
    returns: один из объектов класса WatherType
    """
    try:
        return str(openweather_dict["weather"][0]["description"])
    except (KeyError, IndexError):
        raise exceptions.BaseError()
