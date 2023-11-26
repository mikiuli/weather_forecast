"""Returns current coordinates of user's device using IPInfo module"""

import ipinfo

from dataclasses import dataclass

from services.exceptions import CantGetCoordinates
import services.config


@dataclass(slots=True, frozen=True)
class Coordinates:
    latitude: float
    longitude: float


def get_user_coordinates() -> Coordinates:

    """Returns current user coordinates using IPinfo"""

    coordinates = _get_IPinfo()
    return _round_gps_coordinates(coordinates)


def _get_IPinfo() -> Coordinates:
    access_token = services.config.IPINFO_ACCESS_TOKEN

    try:
        handler = ipinfo.getHandler(access_token)
        details = handler.getDetails()
        latitude = float(details.latitude)
        longitude = float(details.longitude)

        return Coordinates(latitude=latitude, longitude=longitude)

    except Exception:
        raise CantGetCoordinates


def _round_gps_coordinates(coordinates: Coordinates) -> Coordinates:
    if not services.config.USE_ROUND_COORDS:
        return coordinates
    return Coordinates(*map(lambda c: round(c, 1), [coordinates.latitude,
                                                    coordinates.longitude]))
