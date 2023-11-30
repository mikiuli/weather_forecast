from datetime import datetime

from services.weather_api_service import Weather, Celsius, Unix_time


def format_weather(weather: Weather) -> str:
    return (f"Текущее время: {_format_time(weather.current_time)}\n"
            f"Название города: {weather.city}\n"
            f"Погодные условия: {weather.weather_type}\n"
            f"Текущая температура: {weather.temperature} "
            f"градус{_format_gradus_ending(weather.temperature)} по цельсию\n"
            f"Ощущается как: {weather.temperature_feels_like} "
            f"градус{_format_gradus_ending(weather.temperature_feels_like)}"
            " по цельсию\n"
            f"Скорость ветра: {weather.wind_speed} м/с")


def _format_gradus_ending(temp: Celsius) -> str:
    if str(temp)[-1] == "1" and abs(temp) != 11:
        return ""
    elif (str(temp)[-1] in
          ["2", "3", "4"]) and (abs(temp) not in
                                [12, 13, 14]):
        return "a"
    else:
        return "ов"


def _format_time(time: Unix_time) -> datetime:
    date = datetime.utcfromtimestamp(time)
    return date.astimezone()
