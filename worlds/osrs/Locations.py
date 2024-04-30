import typing

from BaseClasses import Location


class SkillRequirement(typing.NamedTuple):
    skill: str
    level: int


class LocationRow(typing.NamedTuple):
    name: str
    category: str
    regions: typing.List[str]
    skills: typing.List[SkillRequirement]
    items: typing.List[str]
    qp: int


class OSRSLocation(Location):
    game: str = "Old School Runescape"
