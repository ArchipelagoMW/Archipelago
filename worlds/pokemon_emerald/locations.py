"""
Classes and functions related to AP locations for Pokemon Emerald
"""
from typing import Dict, Optional, FrozenSet, Iterable

from BaseClasses import Location, MultiWorld, Region

from .data import config, data
from .items import offset_item_value


class PokemonEmeraldLocation(Location):
    game: str = "Pokemon Emerald"
    flag: Optional[int]
    rom_address: Optional[int]
    default_item_code: Optional[int]
    is_event: bool
    tags: FrozenSet[str]

    def __init__(
            self,
            player: int,
            name: str,
            flag: Optional[int],
            parent: Optional[Region] = None,
            rom_address: Optional[int] = None,
            default_item_value: Optional[int] = None,
            tags: FrozenSet[str] = frozenset()) -> None:
        super().__init__(player, name, None if flag is None else offset_flag(flag), parent)
        self.flag = flag
        self.default_item_code = None if default_item_value is None else offset_item_value(default_item_value)
        self.rom_address = rom_address
        self.is_event = flag is None
        self.tags = tags


def offset_flag(flag: int) -> int:
    """
    Returns the AP location id (address) for a given flag
    """
    if flag is None:
        return None
    return flag + config["ap_offset"]


def reverse_offset_flag(location_id: int) -> int:
    """
    Returns the flag id for a given AP location id (address)
    """
    if location_id is None:
        return None
    return location_id - config["ap_offset"]


def create_locations_with_tags(multiworld: MultiWorld, player: int, tags: Iterable[str]) -> None:
    """
    Iterates through region data and adds locations to the multiworld if
    those locations include any of the provided tags.
    """
    tags = set(tags)

    for region_name, region_data in data.regions.items():
        region = multiworld.get_region(region_name, player)
        filtered_locations = [loc for loc in region_data.locations if len(tags & data.locations[loc].tags) > 0]

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
    """
    Creates a map from location labels to their AP location id (address)
    """
    label_to_id_map: Dict[str, int] = {}
    for region_data in data.regions.values():
        for location_name in region_data.locations:
            location_data = data.locations[location_name]
            label_to_id_map[location_data.label] = offset_flag(location_data.flag)

    return label_to_id_map
