# **weather_forecast**
____

Прогроз погоды - учебное консольное приложение для получения информации о прогнозе погоды.
____

Пользователь может:
1. Получить данные о прогнозе погоды в его текущем местоположении
2. Сделать запрос на прогноз погоды в любом городе мира
3. Получить историю своих запросов, количество запросов задаёт пользователь
4. Удалить историю запросов
5. Выйти из приложения
____

Запрос приходит в формате строки:
```
Текущее время: 2023-10-03 09:48:47+03:00
Название города: Санкт-Петербург
Погодные условия: облачно
Текущая температура: 12 градусов по цельсию
Ощущается как: 11 градусов по цельсию
Скорость ветра: 5 м/c
```

## **_Установка_**

1. Установить интерпретатор [Python 3.11.6](https://www.python.org/downloads/release/python-3116/) и выше
2. Установить среду разработки, например, [VSCode](https://code.visualstudio.com/) или [Pycharm](https://www.jetbrains.com/pycharm/)
3. Клонировать репозиторий на локальный компьютер [как клонировать](https://docs.github.com/ru/repositories/creating-and-managing-repositories/cloning-a-repository)
4. Открыть в среде разработки, и, находясь в корневом файле weather_forecast.py,
создать виртуальное окружение:
```python3 -m venv venv```
активировать его:
для Windows:
```venv\Scripts\activate.ps1```
для macOS и Linux:
```source venv/bin/activate```
5. Загрузить файл requirements.txt:
```pip install -r requirements.txt```
6. Запустить программу из корневого файла weather_forecast.py

## **_Использование_**

Запуск программы осуществляется с корневого файла weather_forecast.py.
Программа предлагает пять вариантов запроса каждый под своим номером
и место для ввода номера пользователем. Необходимо ввести цифру
и нажать Enter.\
![1](https://github.com/mikiuli/weather_forecast/assets/141579432/e2fbce85-af61-4dcb-9cbb-dc3f6c56ddf6) \
 \
В случае некорректного ввода приложение уведомляет об этом и требует ввести
запрос заново.\
![2](https://github.com/mikiuli/weather_forecast/assets/141579432/a1c6ebcc-cd41-44c8-85a9-bdac54c9f2f5) \
 \
Когда запрос выполнен, снова появляется стартовый текст.\
![3](https://github.com/mikiuli/weather_forecast/assets/141579432/135da9ab-029e-4769-95f5-3a9350bdf5f5) \
 \
Если пользователь хочет получить прогноз погоды определённого города(2),
будет предложена строка, куда необходимо ввести название города на русском языке.\
![4](https://github.com/mikiuli/weather_forecast/assets/141579432/174c3cda-a389-428a-b6b9-e9599f1cb3a4) \
 \
Если в названии допущена грамматическая ошибка или введены некорректные данные,
программа будет продолжать просить ввести название города до тех пор,
пока от внешнего сервера не придёт ответ с кодом 200.\
![5](https://github.com/mikiuli/weather_forecast/assets/141579432/9ae6180e-8fa4-41a8-ac0a-46c0b0f6179b) \
 \
При получении истории запросов(3) необходимо ввести число запросов. Ожидается введение
целого положительного числа, остальные числа обрабатываться не будут и программа
будет продолжать просить ввести число.\
![6](https://github.com/mikiuli/weather_forecast/assets/141579432/3b4c59e6-912f-40ad-ac26-eec947a50a40) \
 \
Получение прогноза погоды(1), удаление истории запросов(4) и выход из приложения(5)
происходят сразу после ввода номера.

## **_Структура проекта_**

Корневой файл weather_forecast.py\
services - обработка запросов, работа с API, вывод данных в консоль\
database - работа с базой данных: создание соединения, создание базы данных,
сохранение запроса, удаление запросов\
decorators - проверка наличия интернет-соединения и отлов пользовательских исключений для корректного завершения работы программы\
errors - пользовательские исключения\
lexicon - тексты для общения с пользователем

## **_Использованные библиотеки_**

requests - создание http запроса для получения погоды по названию города
с сервера openweathermap.org с API ключом\
geocoder - получение названия города, в котором сейчас находится пользователь\
sqlite3 - создание базы данных для хранения истории запросов
