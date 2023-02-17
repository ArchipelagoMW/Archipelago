from BaseClasses import Location
import typing


class AdvData(typing.NamedTuple):
    id: typing.Optional[int]
    rom_address: int
    region: str


class PokemonEmeraldLocation(Location):
    game: str = "Pokemon Emerald"

    # def __init__(self, player: int, name: str, address: typing.Optional[int], parent):
    #     super().__init__(player, name, address, parent)


advancement_table = {
    "Route 104: Potion": AdvData(1135, 2690726, 'Game'),
    "Route 104: Hidden Poke Ball": AdvData(562, 5408816, 'Game'),
}

exclusion_table = {
}

events_table = {
}

lookup_id_to_name: typing.Dict[int, str] = {data.id: item_name for item_name, data in advancement_table.items() if data.id}
