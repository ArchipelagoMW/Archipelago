from typing import Dict, Optional, FrozenSet
from BaseClasses import Location, MultiWorld, Region
from .Data import data, config
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
        self.is_event = flag is None
        self.tags = tags


def offset_flag(flag: Optional[int]) -> Optional[int]:
    if flag is None:
        return None
    return flag + config["ap_offset"]


def reverse_offset_flag(location_id: Optional[int]) -> Optional[int]:
    if location_id is None:
        return None
    return location_id - config["ap_offset"]


def create_locations_with_tags(multiworld: MultiWorld, player: int, tags):
    tags = set(tags)

    for region_name, region_data in data.regions.items():
        region = multiworld.get_region(region_name, player)
        filtered_locations = [l for l in region_data.locations if len(tags & data.locations[l].tags) > 0]

        for location_name in filtered_locations:
            location_data = data.locations[location_name]
            location = PokemonEmeraldLocation(
                player,
                location_data.label,
                location_data.flag,
                region,
                location_data.rom_address,
                location_data.default_item,
                location_data.tags
            )
            region.locations.append(location)


def create_location_label_to_id_map() -> Dict[str, int]:
    label_to_id_map: Dict[str, int] = {}
    for region_data in data.regions.values():
        for location_name in region_data.locations:
            location_data = data.locations[location_name]
            label_to_id_map[location_data.label] = offset_flag(location_data.flag)

    return label_to_id_map
