"""Осуществляет работу с базой данных sqlite3"""
from contextlib import contextmanager

import sqlite3

from user_actions.services.weather_api_service import Weather
from user_actions.errors import errors

CREATE_TABLE_QUERY = """CREATE TABLE IF NOT EXISTS weather_data (
    id INTEGER PRIMARY KEY,
    time TEXT NOT NULL,
    city_name TEXT NOT NULL,
    weather_type TEXT NOT NULL,
    temperature INTEGER NOT NULL,
    temp_feels_like INTEGER NOT NULL,
    wind_speed INTEGER NOT NULL
)"""
CREATE_INDEX_QUERY = """CREATE INDEX idx_id ON weather_data (id)"""
COUNT_REQUESTS_QUERY = """SELECT COUNT(*) FROM weather_data"""
INSERT_QUERY = """INSERT INTO weather_data (time, city_name, weather_type,
temperature, temp_feels_like, wind_speed) VALUES (?, ?, ?, ?, ?, ?)"""
DELETE_ALL_REQUESTS_QUERY = """DELETE FROM weather_data"""
SELECT_LAST_N_REQUESTS_QUERY = """SELECT time, city_name, weather_type,
temperature, temp_feels_like, wind_speed FROM weather_data
ORDER BY id DESC
LIMIT {number}"""


@contextmanager
def connect_with_database() -> sqlite3.Connection:
    """
    Создаёт соединение с базой данных и закрывает его
    после выхода из приложения
    params: -
    returns: connection: соединение с базой данных
    """
    try:
        connection = sqlite3.connect("weather_forecast.db")
        print("e)")
        yield connection
    except sqlite3.OperationalError:
        raise errors.NoConnectionWithDBError()
    finally:
        connection.close()


def init_table(connection: sqlite3.Connection) -> None:
    """
    Создает таблицу в базе данных
    params: connection: соединение с базой данных, открытое
    в функции connect_with_database
    returns: -
    """
    try:
        cursor = connection.cursor()
        cursor.execute(CREATE_TABLE_QUERY)
        try:
            cursor.execute(CREATE_INDEX_QUERY)
        except sqlite3.OperationalError:
            pass
        connection.commit()
    except sqlite3.OperationalError:
        raise errors.NoConnectionWithDBError()


def save_weather_data(connection: sqlite3.Connection,
                      weather: Weather) -> None:
    """
    Сохраняет запрос пользователя о погоде в базе данных
    params: weather:  информация о погоде в виде класса Weather
    connection: соединение с базой данных, открытое в функции
    connect_with_database
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
        raise errors.NoConnectionWithDBError()


def get_weather_data(connection: sqlite3.Connection,
                     number: int) -> list[Weather]:
    """
    Даёт информацию о последних number запросах пользователя
    params: connection: соединение с базой данных, открытое в функции
    connect_with_database, number: количество запросов, которое
    хочет получить пользователь
    returns: список запросов в виде списка, каждый элемент которого
    является объектом класса Weather
    """
    try:
        cursor = connection.cursor()
        cursor.execute(SELECT_LAST_N_REQUESTS_QUERY.format(number=number))
        weather_datas = cursor.fetchall()

        weather_datas_list = []
        for data in weather_datas:
            weather = Weather(current_time=data[0],
                              city=data[1],
                              weather_type=data[2],
                              temperature=data[3],
                              temperature_feels_like=data[4],
                              wind_speed=data[5])
            weather_datas_list.append(weather)
        return weather_datas_list
    except sqlite3.OperationalError:
        raise errors.NoConnectionWithDBError()


def delete_weather_data(connection: sqlite3.Connection) -> None:
    """
    Очищает базу данных
    params: connection: соединение с базой данных, открытое в функции
    connect_with_database
    returns: -
    """
    try:
        cursor = connection.cursor()
        cursor.execute(DELETE_ALL_REQUESTS_QUERY)
        connection.commit()
    except sqlite3.OperationalError:
        raise errors.NoConnectionWithDBError()
