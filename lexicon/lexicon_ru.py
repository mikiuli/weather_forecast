"""Тексты для вывода пользователю"""


from enum import StrEnum

START_TEXT = ("Напишите '1', чтобы получить погоду в вашем городе\n"
              "Напишите '2', чтобы получить погоду в любом другом "
              "городе\n""Напишите '3', чтобы посмотреть историю запросов\n"
              "Напишите '4', чтобы удалить историю запросов\n"
              "Напишите '5', чтобы выйти из приложения")
WRONG_TEXT = "Вы написали что-то не то, попробуйте ещё раз"
PRINT_CITY_NAME_TEXT = "Напишите название города"
WRONG_CITY_NAME_TEXT = ("В названии была допущена ошибка\n"
                        "Введите правильное название города")
REQUESTS_NUMBER_TEXT = ("Введите количество запросов, "
                        "которое Вы хотите получить")
DELETE_HISTORY_TEXT = "Вся история запросов удалена"
APP_CANT_WORK_TEXT = ("К сожалению, приложение не может продолжать "
                      "свою работу.\n"
                      "Перезапустите его и выполните запрос заново")


class Text(StrEnum):
    start_text = START_TEXT
    wrong_text = WRONG_TEXT
    print_city_name_text = PRINT_CITY_NAME_TEXT
    wrong_city_name_text = WRONG_CITY_NAME_TEXT
    requests_number_text = REQUESTS_NUMBER_TEXT
    delete_history_text = DELETE_HISTORY_TEXT
    app_cant_work_text = APP_CANT_WORK_TEXT
