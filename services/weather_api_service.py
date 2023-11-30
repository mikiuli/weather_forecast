import requests

from dataclasses import dataclass
from enum import Enum
import json
from json.decoder import JSONDecodeError

from typing import TypeAlias

from services.user_coordinates import Coordinates
import services.config
from services.exceptions import APIServiseError

Celsius: TypeAlias = int
metres_per_sec: TypeAlias = int
Unix_time: TypeAlias = int


class WeatherType(str, Enum):
    THUNDERSTORM = "Гроза"
    DRIZZLE = "Изморозь"
    RAIN = "Дождь"
    SNOW = "Снег"
    CLEAR = "Ясно"
    FOG = "Туман"
    CLOUDS = "Облачно"


@dataclass(slots=True, frozen=True)
class Weather:
    current_time: Unix_time
    city: str

    weather_type: WeatherType
    temperature: Celsius
    temperature_feels_like: Celsius
    wind_speed: metres_per_sec


def get_weather(coordinates: Coordinates) -> Weather:
    """Requests weather in OpenWeather API and returns it"""
    openweather_response = _get_openweather_response(
        longitude=coordinates.longitude, latitude=coordinates.latitude
    )
    weather = _parse_openweather_response(openweather_response)
    return weather


def _get_openweather_response(latitude: float, longitude: float) -> str:
    url = services.config.OPENWEATHER_URL.format(latitude=latitude,
                                                 longitude=longitude)
    response = requests.get(url=url)
    try:
        return response.text
    except requests.exceptions.HTTPError:
        raise APIServiseError


def _parse_openweather_response(openweather_response: str) -> Weather:
    try:
        openweather_dict = json.loads(openweather_response)
    except JSONDecodeError:
        raise APIServiseError
    return Weather(
        current_time=_parse_current_time(openweather_dict),
        city=_parse_city_name(openweather_dict),
        weather_type=_parse_weather_type(openweather_dict),
        temperature=_parse_temperature(openweather_dict),
        temperature_feels_like=_parse_temp_feels_like(openweather_dict),
        wind_speed=_parse_wind_speed(openweather_dict)
    )


def _parse_current_time(openweather_dict: dict) -> Unix_time:
    return openweather_dict["dt"]


def _parse_city_name(openweather_dict: dict) -> str:
    return openweather_dict["name"]


def _parse_temperature(openweather_dict: dict) -> Celsius:
    return round(openweather_dict["main"]["temp"])


def _parse_temp_feels_like(openweather_dict) -> Celsius:
    return round(openweather_dict["main"]["feels_like"])


def _parse_wind_speed(openweather_dict: dict) -> metres_per_sec:
    return round(openweather_dict["wind"]["speed"])


def _parse_weather_type(openweather_dict: dict) -> WeatherType:
    try:
        weather_type_id = (str(openweather_dict["weather"][0]["id"]))
    except (IndexError, KeyError):
        raise APIServiseError
    weather_types = {
        "1": WeatherType.THUNDERSTORM,
        "3": WeatherType.DRIZZLE,
        "5": WeatherType.RAIN,
        "6": WeatherType.SNOW,
        "7": WeatherType.FOG,
        "800": WeatherType.CLEAR,
        "80": WeatherType.CLOUDS
    }
    for _id, _weather_type in weather_types.items():
        if weather_type_id.startswith(_id):
            return _weather_type
    raise APIServiseError
