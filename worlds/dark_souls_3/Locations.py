from BaseClasses import Location
from worlds.dark_souls_3.data.locations_data import location_tables


class DarkSouls3Location(Location):
    game: str = "Dark Souls III"

    @staticmethod
    def get_name_to_id() -> dict:
        base_id = 100000
        table_offset = 100

        output = {}
        i = 0
        for table in location_tables:
            output |= {name: id for id, name in enumerate(table, base_id + (table_offset * i))}
            i += 1

        return output
