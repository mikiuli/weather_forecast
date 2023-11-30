import services
import database


class Process:
    start = True
    stop = False


class Text:
    start_text = ("Print '1' to get your local weather\n"
                  "Print '2' to get weather of any city you want\n"
                  "Print '3' to get access to your requests story")
    restart_text = "Do you want to restart? y/n"
    wrong_text = "You printed stuff out of offered options, try again"
    print_city_name_text = "Print city name"
    wrong_city_name = ("В названии была допущена ошибка\n"
                       "Введите правильное название города")


def get_save_print_weather(coordinates) -> None:
    weather = services.get_weather(coordinates)
    database.save_weather_request(weather)
    print(services.format_weather(weather))


def get_local_weather() -> None:
    user_coordinates = services.get_user_coordinates()
    get_save_print_weather(user_coordinates)


def get_city_weather() -> None:
    print(Text.print_city_name_text)
    city_name = input()
    city_coordinates = services.get_city_coordinates(city_name)
    while city_coordinates == "error":
        print(Text.wrong_city_name)
        city_name = input()
        city_coordinates = services.get_city_coordinates(city_name)
    get_save_print_weather(city_coordinates)


def get_weather_requests_history() -> None:
    last_requests = database.get_last_requests()
    for request in last_requests:
        print(services.format_weather(request))


def choose_options(user_input: str) -> None:
    if user_input == '1':
        get_local_weather()
    elif user_input == '2':
        get_city_weather()
    else:
        get_weather_requests_history()


def main() -> None:
    process = Process.start
    database.create_database()
    while process:
        print(Text.start_text)
        user_input = input()
        if user_input in {'1', '2', '3'}:
            choose_options(user_input)
            print(Text.restart_text)
            restart = input()
            while restart.lower() not in {'y', 'n'}:
                print(Text.wrong_text)
                print(Text.restart_text)
                restart = input()
            if restart.lower() == "y":
                continue
            else:
                process = Process.stop
        else:
            print(Text.wrong_text)
            continue


if __name__ == "__main__":
    main()
