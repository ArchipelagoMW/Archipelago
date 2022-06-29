import typing
from BaseClasses import Location, Region, RegionType
from worlds.dark_souls_3.data.locations_data import dictionary_table


class LocationData(int):
    code: int


class DarkSouls3Location(Location):
    game: str = "Dark Souls III"

    # override constructor to automatically mark event locations as such
    def __init__(self, player: int, name='', code=None, parent=None):
        super(DarkSouls3Location, self).__init__(player, name, code, parent)
        self.event = code is None

    @staticmethod
    def get_location_name_to_id() -> typing.Dict[str, int]:
        return dictionary_table
