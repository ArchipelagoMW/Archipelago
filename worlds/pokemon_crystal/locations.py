from typing import TYPE_CHECKING, Optional, Dict, FrozenSet

from BaseClasses import Location, Region
from .data import data

if TYPE_CHECKING:
    from . import PokemonCrystalWorld


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
        super().__init__(player, name, flag, parent)
        self.default_item_code = default_item_value
        self.rom_address = rom_address
        self.tags = tags


def create_locations(world: "PokemonCrystalWorld", regions: Dict[str, Region]) -> None:
    exclude = set()
    if not world.options.randomize_hidden_items:
        exclude.add("Hidden")
    if not world.options.randomize_pokegear:
        exclude.add("Pokegear")
    if not world.options.trainersanity:
        exclude.add("Trainersanity")
    if not world.options.randomize_badges:
        exclude.add("Badge")
    if not world.options.randomize_berry_trees:
        exclude.add("BerryTree")

    for region_name, region_data in data.regions.items():
        if region_name in regions:
            region = regions[region_name]
            filtered_locations = [loc for loc in region_data.locations if
                                  not exclude.intersection(set(data.locations[loc].tags))]
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
            label_to_id_map[location_data.label] = location_data.flag

    return label_to_id_map
