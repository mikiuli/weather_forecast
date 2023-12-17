import services
import database

from enum import StrEnum
import sys


class Text:
    start_text = ("Напишите '1', чтобы получить погоду в вашем городе\n"
                  "Напишите '2', чтобы получить погоду в любом другом городе\n"
                  "Напишите '3', чтобы посмотреть историю запросов\n"
                  "Напишите '4', чтобы выйти из приложения")
    wrong_text = "Вы написали что-то не то, попроуйте ещё раз"
    print_city_name_text = "Напишите название города"
    wrong_city_name_text = ("В названии была допущена ошибка\n"
                            "Введите правильное название города")
    app_cant_work_text = ("К сожалению, по неизвестным причинам "
                          "приложение не работает")


class Actions(StrEnum):
    WEATHER_IN_USER_LOCATION = "1"
    WEATHER_IN_CITY = "2"
    WEATHER_REQUESTS_HISTORY = "3"
    APP_EXIT = "4"


def get_local_weather() -> None:
    """
    Выводит к консоль информацию о погоде в текущем местоположении
    пользователя
    params: -
    returns: -
    """
    user_coordinates = services.get_user_coordinates()
    weather = services.get_weather(user_coordinates)
    database.save_weather_request(weather)
    print(services.format_weather(weather))


def get_city_weather() -> None:
    """
    Выводит в консоль информацию о погоде в заданном пользователем городе
    params: -
    returns: -
    """
    print(Text.print_city_name_text)
    city_name = input().strip()
    city_coordinates = services.get_city_coordinates(city_name)
    while city_coordinates == "error":
        print(Text.wrong_city_name_text)
        city_name = input()
        city_coordinates = services.get_city_coordinates(city_name)
    weather = services.get_weather(city_coordinates)
    database.save_weather_request(weather)
    print(services.format_weather(weather))


def get_weather_requests_history() -> None:
    """
    Выводит в консоль последние n запросов пользователя
    params: -
    returns: -
    """
    last_requests = database.get_last_requests()
    for request in last_requests:
        print(services.format_weather(request))
        print("\n")


def exit_app() -> None:
    sys.exit()


def main() -> None:
    database.create_database()
    actions = {
        Actions.WEATHER_IN_USER_LOCATION: get_local_weather,
        Actions.WEATHER_IN_CITY: get_city_weather,
        Actions.WEATHER_REQUESTS_HISTORY: get_weather_requests_history,
        Actions.APP_EXIT: exit_app
    }
    while True:
        print(Text.start_text)
        user_input = input().strip()
        if user_input in actions.keys():
            action = actions.get(user_input)
            action()
        else:
            print(Text.wrong_text)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        print(Text.app_cant_work_text)
