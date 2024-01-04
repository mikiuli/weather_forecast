import sqlite3

import services
import database
import lexicon
import decorators

from enum import StrEnum
import sys
from http import HTTPStatus

CUSTOM_EXCEPTIONS = (services.exceptions.CantGetUserCityError,
                     services.exceptions.APIServiceError,
                     services.exceptions.WrongAPIError,
                     services.exceptions.UnspecifiedError,
                     services.exceptions.InternetIsNotAvailable,
                     database.exceptions.NoConnectionWithDBError)
INTERNET_CONNECTION_ERROR = services.exceptions.InternetIsNotAvailable


@decorators.errors_manager(CUSTOM_EXCEPTIONS)
@decorators.internet_manager(INTERNET_CONNECTION_ERROR)
def get_local_weather(connection: sqlite3.Connection) -> None:
    """
    Выводит к консоль информацию о погоде в текущем местоположении
    пользователя
    params: -
    returns: -
    """
    user_city_name = services.get_user_city_name()
    weather = services.get_weather(user_city_name)
    database.save_weather_request(connection, weather)
    print(services.format_weather(weather))


@decorators.errors_manager(CUSTOM_EXCEPTIONS)
@decorators.internet_manager(INTERNET_CONNECTION_ERROR)
def get_city_weather(connection: sqlite3.Connection) -> None:
    """
    Выводит в консоль информацию о погоде в заданном пользователем городе
    params: -
    returns: -
    """
    print(lexicon.Text.print_city_name_text)
    city_name = input().strip().lower()
    weather = services.get_weather(city_name)
    while weather == HTTPStatus.NOT_FOUND:
        print(lexicon.Text.wrong_city_name_text)
        city_name = input().strip().lower()
        weather = services.get_weather(city_name)
    database.save_weather_request(connection, weather)
    print(services.format_weather(weather))


@decorators.errors_manager(CUSTOM_EXCEPTIONS)
def get_weather_requests_history(connection: sqlite3.Connection) -> None:
    """
    Выводит в консоль последние n запросов пользователя
    params: -
    returns: -
    """
    print(lexicon.Text.requests_number_text)
    requests_number = input().strip()
    while True:
        try:
            requests_number = abs(int(requests_number))
            break
        except ValueError:
            print(lexicon.Text.wrong_text)
            requests_number = input().strip()
    last_requests = database.get_last_requests(connection,
                                               int(requests_number))
    for number, request in enumerate(last_requests, 1):
        print("--------------"+str(number)+"--------------")
        print(services.format_weather(request))


@decorators.errors_manager(CUSTOM_EXCEPTIONS)
def delete_requests_history(connection: sqlite3.Connection) -> None:
    """
    Удаляет все сохранённые запросы из базы данных
    params: -
    returns: -
    """
    database.delete_history(connection)
    print(lexicon.Text.delete_history_text)


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


@decorators.errors_manager(CUSTOM_EXCEPTIONS)
def main() -> None:
    actions = {
        Actions.WEATHER_IN_USER_LOCATION: get_local_weather,
        Actions.WEATHER_IN_CITY: get_city_weather,
        Actions.WEATHER_REQUESTS_HISTORY: get_weather_requests_history,
        Actions.DELETE_HISTORY: delete_requests_history,
        Actions.APP_EXIT: exit_app
    }
    with database.create_connection() as connection:
        database.create_database(connection)
        while True:
            print(lexicon.Text.start_text)
            user_input = input().strip()
            if user_input in actions.keys():
                action = actions.get(user_input)
                try:
                    action(connection)
                except TypeError:
                    action()
            else:
                print(lexicon.Text.wrong_text)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        print(lexicon.Text.app_cant_work_text)
