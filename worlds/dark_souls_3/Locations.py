import sys

from BaseClasses import Location
from worlds.dark_souls_3.data.locations_data import location_tables, painted_world_table, dreg_heap_table, \
    ringed_city_table


class DarkSouls3Location(Location):
    game: str = "Dark Souls III"

    @staticmethod
    def get_name_to_id() -> dict:
        base_id = 100000
        table_offset = 100

        output = {}
        for i, table in enumerate(location_tables):
            if len(table) > table_offset:
                raise Exception("A location table has {} entries, that is more than {} entries (table #{})".format(len(table), table_offset, i))
            output.update({name: id for id, name in enumerate(table, base_id + (table_offset * i))})

        return output
