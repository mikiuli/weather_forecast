"""Осуществляет работу с базой данных sqlite3"""

import sqlite3

from services.weather_api_service import Weather
from errors.errors import custom_exceptions

CREATE_TABLE_QUERY = """CREATE TABLE IF NOT EXISTS Weather_requests (
    id INTEGER PRIMARY KEY,
    time TEXT NOT NULL,
    city_name TEXT NOT NULL,
    weather_type TEXT NOT NULL,
    temperature INTEGER NOT NULL,
    temp_feels_like INTEGER NOT NULL,
    wind_speed INTEGER NOT NULL
)"""
COUNT_REQUESTS_QUERY = """SELECT COUNT(*) FROM Weather_requests"""
INSERT_QUERY = """INSERT INTO Weather_requests (time, city_name, weather_type,
temperature, temp_feels_like, wind_speed) VALUES (?, ?, ?, ?, ?, ?)"""
DELETE_ALL_REQUESTS_QUERY = """DELETE FROM Weather_requests"""
SELECT_LAST_N_REQUESTS_QUERY = """SELECT time, city_name, weather_type,
temperature, temp_feels_like, wind_speed FROM Weather_requests
ORDER BY id DESC
LIMIT {number}"""


def create_connection() -> sqlite3.Connection:
    """
    Создаёт соединение с базой данных
    params: -
    returns: -
    """
    try:
        connection = sqlite3.connect("weather_forecast.db")
    except sqlite3.OperationalError:
        raise custom_exceptions.NoConnectionWithDBError()
    return connection


def create_database(connection: sqlite3.Connection) -> None:
    """
    Создает базу данных
    params: connection: соединение с базой данных, открытое
    в функции create_connection
    returns: -
    """
    try:
        cursor = connection.cursor()
        cursor.execute(CREATE_TABLE_QUERY)
    except sqlite3.OperationalError:
        raise custom_exceptions.NoConnectionWithDBError()


def save_weather_request(connection: sqlite3.Connection,
                         weather: Weather) -> None:
    """
    Сохраняет запрос пользователя о погоде в базе данных
    params: weather:  информация о погоде в виде класса Weather
    connection: соединение с базой данных, открытое в функции
    create_connection
    returns: -
    """
    try:
        cursor = connection.cursor()
        cursor.execute(INSERT_QUERY, (weather.current_time,
                                      weather.city,
                                      weather.weather_type,
                                      weather.temperature,
                                      weather.temperature_feels_like,
                                      weather.wind_speed))

        connection.commit()
    except sqlite3.OperationalError:
        raise custom_exceptions.NoConnectionWithDBError()


def get_last_requests(connection: sqlite3.Connection,
                      number: int) -> list[Weather]:
    """
    Даёт информацию о последних number запросах пользователя
    params: number: количество запросов, которое хочет получить пользователь
    returns: список запросов в виде списка, каждый элемент которого
    является объектом класса Weather
    """
    try:
        cursor = connection.cursor()
        cursor.execute(SELECT_LAST_N_REQUESTS_QUERY.format(number=number))
        weather_requests = cursor.fetchall()

        requests_list = []
        for request in weather_requests:
            weather = Weather(current_time=request[0],
                              city=request[1],
                              weather_type=request[2],
                              temperature=request[3],
                              temperature_feels_like=request[4],
                              wind_speed=request[5])
            requests_list.append(weather)
        return requests_list
    except sqlite3.OperationalError:
        raise custom_exceptions.NoConnectionWithDBError()


def delete_history(connection: sqlite3.Connection) -> None:
    """
    Очищает базу данных
    params: -
    returns: -
    """
    try:
        cursor = connection.cursor()
        cursor.execute(DELETE_ALL_REQUESTS_QUERY)
        connection.commit()
    except sqlite3.OperationalError:
        raise custom_exceptions.NoConnectionWithDBError()
