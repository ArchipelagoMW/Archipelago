import typing

from BaseClasses import Location
from .Names import LocationNames


class OSRSLocation(Location):
    game: str = "Old School Runescape"


class LocationData(typing.NamedTuple):
    id: int
    name: str
    skill_reqs: typing.Dict[str, int] = {}