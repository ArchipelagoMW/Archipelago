from BaseClasses import Location
import typing


class AdvData(typing.NamedTuple):
    id: int
    region: str = "Board"


class ChecksFinderLocation(Location):
    game: str = "ChecksFinder"


base_id = 81000
advancement_table = {f"Tile {i+1}": AdvData(base_id+i) for i in range(25)}
lookup_id_to_name: typing.Dict[int, str] = {data.id: item_name for item_name, data in advancement_table.items()}
