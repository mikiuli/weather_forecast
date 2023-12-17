import sqlite3

from services.weather_api_service import Weather
from database.exceptions import NoConnectionWithDB

REQUESTS_NUMBER = 5

CREATE_TABLE_QUERY = """CREATE TABLE IF NOT EXISTS Weather_requests (
    id INTEGER PRIMARY KEY,
    time INTEGER NOT NULL,
    city_name TEXT NOT NULL,
    weather_type TEXT NOT NULL,
    temperature INTEGER NOT NULL,
    temp_feels_like INTEGER NOT NULL,
    wind_speed INTEGER NOT NULL
)"""
COUNT_REQUESTS_QUERY = """SELECT COUNT(*) FROM Weather_requests"""
INSERT_QUERY = """INSERT INTO Weather_requests (time, city_name, weather_type,
temperature, temp_feels_like, wind_speed) VALUES (?, ?, ?, ?, ?, ?)"""
DELETE_FIRST_REQUEST_QUERY = """DELETE FROM Weather_requests
WHERE id = (SELECT MIN(id) FROM Weather_requests)"""
SELECT_ALL_QUERY = """SELECT * FROM Weather_requests"""


def create_database() -> None:
    """
    Создает базу данных
    params: -
    returns: -
    """
    try:
        with sqlite3.connect("weather_forecast.db") as connection:
            cursor = connection.cursor()
            cursor.execute(CREATE_TABLE_QUERY)
    except Exception:
        raise NoConnectionWithDB


def save_weather_request(weather: Weather) -> None:
    """
    Сохраняет запрос пользователя о погоде в базе данных
    params: weather:  информация о погоде в виде класса Weather
    returns: -
    """
    try:
        with sqlite3.connect("weather_forecast.db") as connection:
            cursor = connection.cursor()
            cursor.execute(COUNT_REQUESTS_QUERY)
            total_requests = cursor.fetchone()[0]

            if total_requests == REQUESTS_NUMBER:
                cursor.execute(DELETE_FIRST_REQUEST_QUERY)
            cursor.execute(INSERT_QUERY, (weather.current_time,
                                          weather.city,
                                          weather.weather_type,
                                          weather.temperature,
                                          weather.temperature_feels_like,
                                          weather.wind_speed))

            connection.commit()
    except Exception:
        raise NoConnectionWithDB


def get_last_requests() -> list[Weather]:
    """
    Даёт информацию о последних n запросах пользователя
    params: -
    returns: список запросов, структурно организованных в класс Weather
    """
    try:
        with sqlite3.connect("weather_forecast.db") as connection:
            cursor = connection.cursor()
            cursor.execute(SELECT_ALL_QUERY)
            weather_requests = cursor.fetchall()

            requests_list = []
            for request in weather_requests:
                weather = Weather(current_time=request[1],
                                  city=request[2],
                                  weather_type=request[3],
                                  temperature=request[4],
                                  temperature_feels_like=request[5],
                                  wind_speed=request[6])
                requests_list.append(weather)
            requests_list.reverse()
        return requests_list
    except Exception:
        raise NoConnectionWithDB
