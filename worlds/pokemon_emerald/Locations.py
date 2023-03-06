from typing import Optional, FrozenSet, Union
from BaseClasses import Location, MultiWorld, Region
from .Data import get_region_data
from .Items import offset_item_value


class PokemonEmeraldLocation(Location):
    game: str = "Pokemon Emerald"
    flag: Optional[int]
    rom_address: Optional[int]
    default_item_code: Optional[int]
    is_event: bool
    tags: Optional[FrozenSet[str]]

    def __init__(self, player: int, name: str, flag: Optional[int], parent: Optional[Region] = None, rom_address: Optional[int] = None, default_item_value: Optional[int] = None, tags: Optional[FrozenSet[str]] = None):
        super().__init__(player, name, offset_flag(flag), parent)
        self.flag = flag
        self.default_item_code = offset_item_value(default_item_value)
        self.rom_address = rom_address
        self.is_event = flag == None
        self.tags = tags


def offset_flag(flag: Union[int, None]) -> Union[int, None]:
    if (flag == None): return None
    return flag + 3860000


def reverse_offset_flag(id: Union[int, None]) -> Union[int, None]:
    if (id == None): return None
    return id - 3860000


def create_locations_with_tags(multiworld: MultiWorld, player: int, tags):
    region_data = get_region_data()
    tags = set(tags)

    for region_name, region_data in region_data.items():
        region = multiworld.get_region(region_name, player)
        for location_data in [location for location in region_data.locations if len(tags & location.tags) > 0]:
            location = PokemonEmeraldLocation(player, location_data.label, location_data.flag, region, location_data.rom_address, location_data.default_item, location_data.tags)
            region.locations.append(location)


def create_location_label_to_id_map():
    region_data = get_region_data()

    map = {}
    for region_data in region_data.values():
        for location_data in region_data.locations:
            map[location_data.label] = offset_flag(location_data.flag)

    return map
