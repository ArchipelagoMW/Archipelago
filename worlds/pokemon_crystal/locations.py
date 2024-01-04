from typing import TYPE_CHECKING, Optional, Dict, FrozenSet
from BaseClasses import Location, Region

from .items import offset_item_value
from .data import data, BASE_OFFSET

if TYPE_CHECKING:
    from . import PokemonCrystalWorld
else:
    PokemonCrystalWorld = object


class PokemonCrystalLocation(Location):
    game: str = "Pokemon Crystal"
    rom_address: Optional[int]
    default_item_code: Optional[int]
    flag: Optional[int]
    tags: FrozenSet[str]

    def __init__(
            self,
            player: int,
            name: str,
            parent: Optional[Region] = None,
            flag: Optional[int] = None,
            rom_address: Optional[int] = None,
            default_item_value: Optional[int] = None,
            tags: FrozenSet[str] = frozenset()
    ) -> None:
        super().__init__(player, name, None if flag is None else offset_flag(flag), parent)
        self.default_item_code = None if default_item_value is None else offset_item_value(default_item_value)
        self.rom_address = rom_address
        self.tags = tags


def offset_flag(flag: int) -> int:
    """
    Returns the AP location id (address) for a given flag
    """
    if flag is None:
        return None
    return flag + BASE_OFFSET


def reverse_offset_flag(location_id: int) -> int:
    """
    Returns the flag id for a given AP location id (address)
    """
    if location_id is None:
        return None
    return location_id - BASE_OFFSET


def create_locations(world: PokemonCrystalWorld, regions: Dict[str, Region], randomize_hidden_items: bool) -> None:
    for region_name, region_data in data.regions.items():
        region = regions[region_name]
        filtered_locations = {}
        if not randomize_hidden_items:
            filtered_locations = [loc for loc in region_data.locations if not "Hidden" in data.locations[loc].tags]
        else:
            filtered_locations = region_data.locations
        for location_name in filtered_locations:
            location_data = data.locations[location_name]
            location = PokemonCrystalLocation(
                world.player,
                location_data.label,
                region,
                location_data.flag,
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
