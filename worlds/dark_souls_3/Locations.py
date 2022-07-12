import typing
from BaseClasses import Location, Region, RegionType
from worlds.dark_souls_3.data.locations_data import dictionary_table


class LocationData(int):
    code: int


class DarkSouls3Location(Location):

    @staticmethod
    def get_location_name_to_id() -> typing.Dict[str, int]:
        return dictionary_table
