"""Выполняет действие по номеру запроса пользователя"""

import sqlite3
from enum import StrEnum
import sys

from user_actions import services
from user_actions import database
from user_actions import lexicon
from user_actions import decorators
from user_actions import errors


@decorators.errors_manager(errors.MyBaseError)
def _get_local_weather(connection: sqlite3.Connection,
                       openweatherAPI: str,
                       ipinfo_access_token: str) -> None:
    """
    Выводит к консоль информацию о погоде в текущем местоположении
    пользователя
    params: connection: подключение к базе данных,
    openweatherAPI: API-ключ от openweathermap.org,
    access_token: токен для использования библиотеки ipinfo
    returns: -
    """
    user_city_name = services.get_user_city_name(ipinfo_access_token)
    weather = services.get_weather_from_openweatherAPI(openweatherAPI,
                                                       user_city_name)
    database.save_weather_data(connection, weather)
    print(weather)


@decorators.errors_manager(errors.MyBaseError)
def _get_city_weather(connection: sqlite3.Connection,
                      openweatherAPI: str) -> None:
    """
    Выводит в консоль информацию о погоде в заданном пользователем городе
    params: connection: подключение к базе данных,
    openweatherAPI: API-ключ от openweathermap.org
    returns: -
    """
    print(lexicon.Text.print_city_name_text)
    city_name = input().strip().lower()
    while True:
        try:
            weather = services.get_weather_from_openweatherAPI(openweatherAPI,
                                                               city_name)
            break
        except errors.WrongCityName:
            print(lexicon.Text.wrong_city_name_text)
            city_name = input().strip().lower()
            weather = services.get_weather_from_openweatherAPI(openweatherAPI,
                                                               city_name)
    database.save_weather_data(connection, weather)
    print(weather)


@decorators.errors_manager(errors.MyBaseError)
def _get_weather_history(connection: sqlite3.Connection) -> None:
    """
    Выводит в консоль последние n запросов пользователя
    params: connection: подключение к базе данных
    returns: -
    """
    print(lexicon.Text.requests_number_text)
    weather_data_number = input().strip()
    while True:
        try:
            if "." in weather_data_number:
                raise ValueError
            weather_data_number = int(weather_data_number)
            if weather_data_number < 0:
                raise ValueError
            else:
                break
        except ValueError:
            print(lexicon.Text.wrong_text)
            weather_data_number = input().strip()
    weather_datas_list = database.get_weather_data(connection,
                                                   int(weather_data_number))
    for number, weather_data in enumerate(weather_datas_list, 1):
        print("--------------"+str(number)+"--------------")
        print(weather_data)


@decorators.errors_manager(errors.MyBaseError)
def _delete_weather_history(connection: sqlite3.Connection) -> None:
    """
    Удаляет все сохранённые запросы из базы данных
    params: connection: подключение к базе данных
    returns: -
    """
    database.delete_weather_data(connection)
    print(lexicon.Text.delete_history_text)


def _exit_app() -> None:
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


def _execute_action_by_name(ipinfo_access_token: str,
                            openweatherAPI: str,
                            connection: sqlite3.Connection) -> None:
    """
    Осуществляет выполнение действий по номеру
    params: connection: подключение к базе данных,
    openweatherAPI: API-ключ от openweathermap.org,
    ipinfo_access_token: токен для использования библиотеки ipinfo
    returns: -
    """
    actions = {
        Actions.WEATHER_IN_USER_LOCATION: _get_local_weather,
        Actions.WEATHER_IN_CITY: _get_city_weather,
        Actions.WEATHER_REQUESTS_HISTORY: _get_weather_history,
        Actions.DELETE_HISTORY: _delete_weather_history,
        Actions.APP_EXIT: _exit_app
    }
    arguments = {
        _get_local_weather: (connection, openweatherAPI, ipinfo_access_token),
        _get_city_weather: (connection, openweatherAPI),
        _get_weather_history: (connection, ),
        _delete_weather_history: (connection, ),
        _exit_app: ()
    }
    while True:
        print(lexicon.Text.start_text)
        user_input = input().strip()
        if user_input in actions.keys():
            action = actions.get(user_input)
            action(*arguments[action])
        else:
            print(lexicon.Text.wrong_text)


@decorators.errors_manager(errors.MyBaseError)
def process_app(ipinfo_access_token: str,
                openweatherAPI: str) -> None:
    """
    Выполняет действия для старта приложения: создаёт соединение с базой данных,
    создаёт таблицу, если она отсутствует, запускает цикл приложения,
    закрывает соединение после выхода из приложения
    params: openweatherAPI: API-ключ от openweathermap.org,
    ipinfo_access_token: токен для использования библиотеки ipinfo
    returns: -
    """
    with database.connect_with_database() as connection:
        database.init_table(connection)
        _execute_action_by_name(ipinfo_access_token,
                                openweatherAPI,
                                connection)
