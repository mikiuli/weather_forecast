import user_actions
from user_actions import lexicon

from environs import Env


def main() -> None:
    """
    Запуск приложения
    params: -
    returns: -
    """
    env = Env()
    env.read_env()
    openweatherAPI = env("OPENWEATHER_API")
    ipinfo_access_token = env("IPINFO_ACCESS_TOKEN")
    user_actions.process_app(ipinfo_access_token=ipinfo_access_token,
                             openweatherAPI=openweatherAPI)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        print(lexicon.Text.app_cant_work_text)
