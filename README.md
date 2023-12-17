weather_forecast

Прогроз погоды - учебное консольное приложение для получения информации о прогнозе погоды.

Пользователь может:
1. Получить данные о прогнозе погоды в его текущем местоположении
2. Сделать запрос на прогноз погоды в любом городе мира
3. Получить историю своих запросов

Запрос приходит в формате строки:
"Текущее время: 2023-10-03 09:48:47+03:00
Название города: Санкт-Петербург
Погодные условия: облачно
Текущая температура: 12 градусов по цельсию
Ощущается как: 11 градусов по цельсию
Скорость ветра: 5 м/c"

Установка:


Необходимо создать виртуальное окружение, активировать его
и загрузить в него файл requirements.txt.

Использование:

Запуск программы осуществляется с корневого файла weather_forecast.py.
Программа предлагает четыре варианта запроса каждый под своим номером
и место для ввода номера пользователем. После ввода номера и нажатия Enter
пользователю предоставляются данные по его запросу.

В случае некорректного ввода приложение уведомляет об этом и требует ввести
запрос заново.

В случае невозможности получить координаты пользователя появляется ошибка и
программу требуется перезапустить.

В случае отсутствия соединения с сервером погоды появляется ошибка и
программу требуется перезапустить.

Использованные библиотеки:

ipinfo - получение текущих координат пользователя
requests - создание http запроса для получения погоды по координатам