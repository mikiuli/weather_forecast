from geopy.geocoders import Nominatim

from services.user_coordinates import Coordinates


def get_city_coordinates(city_name: str) -> Coordinates:
    try:
        geolocator = Nominatim(user_agent="weather_forecast")
        location = geolocator.geocode(city_name)
        return Coordinates(latitude=location.latitude,
                           longitude=location.longitude)
    except AttributeError:
        return "error"
