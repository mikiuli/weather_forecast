"""Получает погоду с сервиса openweathermap с помощью библиотеки requests,
отправляет в формате Weather"""

from dataclasses import dataclass
import json
from json.decoder import JSONDecodeError
from typing import TypeAlias
from http import HTTPStatus
from datetime import datetime, timezone, timedelta

import requests

from user_actions.errors.errors import (WrongCityName,
                                        InternetIsNotAvailable,
                                        UnspecifiedError,
                                        WrongAPIError,
                                        APIServiceError)

Celsius: TypeAlias = int
MetresPerSec: TypeAlias = int


@dataclass(slots=True, frozen=True)
class Weather:
    current_time: datetime
    city: str
    weather_type: str
    temperature: Celsius
    temperature_feels_like: Celsius
    wind_speed: MetresPerSec

    def __repr__(self) -> str:
        """
        Форматирует экземпляр класса для вывода в консоль
        params: -
        returns: строка с информацией о погоде
        """
        return (f"Текущее время: {self.current_time}\n"
                f"Название города: {self.city}\n"
                f"Погодные условия: {self.weather_type}\n"
                f"Текущая температура: {self.temperature} "
                f"градус{Weather._format_gradus_ending(self.temperature)} по цельсию\n"
                f"Ощущается как: {self.temperature_feels_like} "
                f"градус{Weather._format_gradus_ending(self.temperature_feels_like)}"
                " по цельсию\n"
                f"Скорость ветра: {self.wind_speed} м/с\n")

    @staticmethod
    def _format_gradus_ending(temp: Celsius) -> str:
        """
        Изменяет окончание слова "градус" в зависимости от числительного
        перед ним
        params: temp: температура в цельсиях
        returns: окончание для слова "градус"
        """
        if str(temp)[-1] == "1" and abs(temp) != 11:
            return ""
        elif (str(temp)[-1] in
              ["2", "3", "4"]) and (abs(temp) not in
                                    [12, 13, 14]):
            return "a"
        else:
            return "ов"


def get_weather_from_openweatherAPI(openweatherAPI: str,
                                    city_name: str) -> Weather:
    """
    Получает прогноз погоды от вебсервиса OpenWeather и
    возвращает в виде класса Weather
    params: city_name: имя города, погоду в котором
    хочет получить пользователь,
    openweatherAPI: API-ключ от openweathermap.org
    returns: погоду в виде класса Weather
    """
    openweather_response = _get_openweather_response(
        openweatherAPI=openweatherAPI,
        city_name=city_name
    )
    if isinstance(openweather_response, int):
        return openweather_response
    weather = _parse_openweather_response(openweather_response)
    return weather


def _check_status_code_OK(status_code: requests.status_codes) -> bool:
    if status_code == HTTPStatus.OK:
        return True
    if status_code == HTTPStatus.NOT_FOUND:
        raise WrongCityName()
    if status_code == HTTPStatus.UNAUTHORIZED:
        raise WrongAPIError()
    if status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        raise APIServiceError()
    raise UnspecifiedError()


def _get_openweather_response(openweatherAPI: str, city_name: str) -> dict:
    """
    Получает ответ от сервера, райзит ошибку, если проблемы с соединением
    params: openweatherAPI: API-ключ от openweathermap.org,
    city_name: имя города, погоду в котором хочет получить пользователь
    returns: Возвращает тело полученного ответа в виде текса
    """
    url = ("https://api.openweathermap.org/data/2.5/weather?"
           f"appid={openweatherAPI}&"
           "units=metric&lang=ru")
    try:
        response = requests.get(url=url, timeout=3, params={"q": city_name})
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
        raise InternetIsNotAvailable()
    if _check_status_code_OK(response.status_code):
        try:
            openweather_dict = json.loads(response.text)
        except JSONDecodeError:
            raise APIServiceError()
        return openweather_dict


def _parse_openweather_response(openweather_dict: dict) -> Weather:
    """
    Превращает словарь в класс Weather
    params: openweather_response: тело полученного ответа в виде текса
    returns: погоду в виде класса Weather
    """
    try:
        return Weather(
            current_time=_fetch_current_time(openweather_dict),
            city=_fetch_city_name(openweather_dict),
            weather_type=_fetch_weather_type(openweather_dict),
            temperature=_fetch_temperature(openweather_dict),
            temperature_feels_like=_fetch_temp_feels_like(openweather_dict),
            wind_speed=_fetch_wind_speed(openweather_dict)
        )
    except (KeyError, IndexError):
        raise APIServiceError


def _fetch_current_time(openweather_dict: dict) -> datetime:
    """
    Получает текущее время из словаря
    params: openweather_dict: словарь
    returns: время в datetime формате
    """
    date = openweather_dict["dt"]
    tzinfo = openweather_dict["timezone"]
    tz = timezone(timedelta(seconds=tzinfo))
    formatted_time = datetime.fromtimestamp(date, tz=tz)
    return formatted_time


def _fetch_city_name(openweather_dict: dict) -> str:
    """
    Получает имя города
    params: openweather_dict: словарь
    returns: имя города
    """
    return openweather_dict["name"]


def _fetch_temperature(openweather_dict: dict) -> Celsius:
    """
    Получает температуру
    params: openweather_dict: словарь
    returns: температуру в цельсиях
    """
    return round(openweather_dict["main"]["temp"])


def _fetch_temp_feels_like(openweather_dict) -> Celsius:
    """
    Получает температуру "ощущается как"
    params: openweather_dict: словарь
    returns: температуру "ощущается как"
    """
    return round(openweather_dict["main"]["feels_like"])


def _fetch_wind_speed(openweather_dict: dict) -> MetresPerSec:
    """
    Получает скорость ветра
    params: openweather_dict: словарь
    returns: скорость ветра
    """
    return round(openweather_dict["wind"]["speed"])


def _fetch_weather_type(openweather_dict: dict) -> str:
    """
    Получает описание погоды
    params: openweather_dict: словарь
    returns: один из объектов класса WatherType
    """
    return str(openweather_dict["weather"][0]["description"])
