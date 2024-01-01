import services
import database

from enum import StrEnum
import sys
from functools import wraps


class Text:
    start_text = ("Напишите '1', чтобы получить погоду в вашем городе\n"
                  "Напишите '2', чтобы получить погоду в любом другом городе\n"
                  "Напишите '3', чтобы посмотреть историю запросов\n"
                  "Напишите '4', чтобы удалить историю запросов\n"
                  "Напишите '5', чтобы выйти из приложения")
    wrong_text = "Вы написали что-то не то, попробуйте ещё раз"
    print_city_name_text = "Напишите название города"
    wrong_city_name_text = ("В названии была допущена ошибка\n"
                            "Введите правильное название города")
    requests_number_text = ("Введите количество запросов, "
                            "которое Вы хотите получить")
    delete_history_text = ("Вся история запросов удалена")
    app_cant_work_text = ("К сожалению, приложение не может продолжать "
                          "свою работу.\n"
                          "Перезапустите его и выполните запрос заново")


CUSTOM_EXCEPTIONS = (services.exceptions.CantGetUserCityError,
                     services.exceptions.APIServiceError,
                     services.exceptions.WrongAPIError,
                     services.exceptions.UnspecifiedError,
                     database.exceptions.NoConnectionWithDBError)


def errors_manager(custom_exceptions):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except custom_exceptions as e:
                print(e)
                exit_app()
        return wrapper
    return decorator


@errors_manager(CUSTOM_EXCEPTIONS)
def get_local_weather() -> None:
    """
    Выводит к консоль информацию о погоде в текущем местоположении
    пользователя
    params: -
    returns: -
    """
    user_city_name = services.get_user_city_name()
    weather = services.get_weather(user_city_name)
    database.save_weather_request(weather)
    print(services.format_weather(weather))


@errors_manager(CUSTOM_EXCEPTIONS)
def get_city_weather() -> None:
    """
    Выводит в консоль информацию о погоде в заданном пользователем городе
    params: -
    returns: -
    """
    print(Text.print_city_name_text)
    city_name = input().strip().lower()
    weather = services.get_weather(city_name)
    while weather == 404:
        print(Text.wrong_city_name_text)
        city_name = input().strip()
        weather = services.get_weather(city_name)
    database.save_weather_request(weather)
    print(services.format_weather(weather))


@errors_manager(CUSTOM_EXCEPTIONS)
def get_weather_requests_history() -> None:
    """
    Выводит в консоль последние n запросов пользователя
    params: -
    returns: -
    """
    print(Text.requests_number_text)
    requests_number = input().strip()
    while True:
        try:
            requests_number = abs(int(requests_number))
            break
        except TypeError:
            print(Text.wrong_text)
            requests_number = input().strip()
    last_requests = database.get_last_requests(int(requests_number))
    for number, request in enumerate(last_requests, 1):
        print("------------"+str(number)+"------------")
        print(services.format_weather(request))


@errors_manager(CUSTOM_EXCEPTIONS)
def delete_requests_history() -> None:
    """
    Удаляет все сохранённые запросы из базы данных
    params: -
    returns: -
    """
    database.delete_history()
    print(Text.delete_history_text)


def exit_app() -> None:
    """
    Осуществляет выход из приложения
    params: -
    returns: -
    """
    sys.exit()


class Actions(StrEnum):
    WEATHER_IN_USER_LOCATION = "1"
    WEATHER_IN_CITY = "2"
    WEATHER_REQUESTS_HISTORY = "3"
    DELETE_HISTORY = "4"
    APP_EXIT = "5"


@errors_manager(CUSTOM_EXCEPTIONS)
def main() -> None:
    database.create_database()
    actions = {
        Actions.WEATHER_IN_USER_LOCATION: get_local_weather,
        Actions.WEATHER_IN_CITY: get_city_weather,
        Actions.WEATHER_REQUESTS_HISTORY: get_weather_requests_history,
        Actions.DELETE_HISTORY: delete_requests_history,
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
