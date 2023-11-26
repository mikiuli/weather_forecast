import services


class Process:
    start = True
    stop = False


class Text:
    start_text = """Print '1' to get your local weather\n
              Print '2' to get weather of any city you want\n
              Print '3' to get access to your requests story"""
    restart_text = "Do you want to restart? y/n"
    wrong_text = "You printed stuff out of offered options, try again"


def main() -> None:
    process = Process.start
    while process:
        print(Text.start_text)
        user_input = input()
        if user_input in {'1', '2', '3'}:
            if user_input == '1':
                coordinates = services.get_user_coordinates()
                weather = services.get_weather(coordinates)
                print(services.format_weather(weather))
                # print(format_weather(weather))
            elif user_input == '2':
                coordinates = services.get_user_coordinates()
                weather = services.get_weather(coordinates)
                print(weather)
                # print(format_weather(weather))
            else:
                pass
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
