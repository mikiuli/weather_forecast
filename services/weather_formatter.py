"""Выводит данные в консоль из объекта класса Weather"""

from services.weather_api_service import Weather, Celsius


def format_weather(weather: Weather) -> str:
    """
    Преобразует данные из класса Weather в строку заданного формата
    params: weather: информация о погоде в виде класса Weather
    returns: строку заданного формата
    """
    return (f"Текущее время: {weather.current_time}\n"
            f"Название города: {weather.city}\n"
            f"Погодные условия: {weather.weather_type}\n"
            f"Текущая температура: {weather.temperature} "
            f"градус{_format_gradus_ending(weather.temperature)} по цельсию\n"
            f"Ощущается как: {weather.temperature_feels_like} "
            f"градус{_format_gradus_ending(weather.temperature_feels_like)}"
            " по цельсию\n"
            f"Скорость ветра: {weather.wind_speed} м/с\n")


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
