from typing import Optional, FrozenSet
from BaseClasses import Location, MultiWorld, Region
from .Data import get_region_data


class PokemonEmeraldLocation(Location):
    game: str = "Pokemon Emerald"
    id: Optional[int]
    default_item_id: Optional[int]
    is_event: bool
    tags: Optional[FrozenSet[str]]

    def __init__(self, player: int, name: str, id: Optional[int], parent: Optional[Region] = None, address: Optional[int] = None, default_item_id: Optional[int] = None, tags: Optional[FrozenSet[str]] = None):
        super().__init__(player, name, address, parent)
        self.id = id
        self.default_item_id = default_item_id
        self.is_event = id == None
        self.tags = tags


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
            map[location_data.label] = location_data.flag

    return map
