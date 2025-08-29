from typing import Dict, Optional, TYPE_CHECKING, Set

from BaseClasses import Location, Region
from worlds.clair_obscur.Const import BASE_OFFSET, LOCATION_OFFSET
from worlds.clair_obscur.Data import data, ClairObscurLocationData
from ..generic.Rules import add_rule

if TYPE_CHECKING:
    from . import ClairObscurWorld

class ClairObscurLocation(Location):
    game: str = "Clair Obscur Expedition 33"
    default_item: Optional[str]

    def __init__(
            self,
            player: int,
            name: str,
            code: int,
            parent: Optional[Region] = None,
            default_item_value: Optional[str] = None) -> None:
        super().__init__(player, name, code, parent)
        self.default_item = default_item_value


def create_locations(world: "ClairObscurWorld", regions: Dict[str, Region]) -> None:
    code = 0

    excluded_types = []
    if not world.options.gestral_shuffle:
        excluded_types.append("Lost Gestral")

    for region_name, region in regions.items():
        if region_name == "Menu": continue

        region_data = data.regions[region_name]

        for location_name in region_data.locations:

            location_data = data.locations[location_name]
            if location_data.type in excluded_types:
                continue

            location = ClairObscurLocation(
                world.player,
                location_data.name,
                offset_location_value(code),
                region,
                location_data.default_item
            )
            conditions = location_data.condition
            if conditions:
                for cond in conditions:
                    amount = conditions[cond]
                    add_rule(location, lambda state, con=cond, pl=world.player, am=amount: state.has(con, pl, am))

            pictos = location_data.pictos_level
            if pictos > 1:
                pictos = world.convert_pictos(pictos)
                add_rule(location, lambda state, pl=world.player, pic=pictos: state.has_group("Picto", pl, pic))

            region.locations.append(location)
            code += 1


def offset_location_value(location_id: int) -> int:
    """
    Returns the AP location id for a given location value
    """
    return BASE_OFFSET + LOCATION_OFFSET + location_id

def reverse_offset_location_value(location_id: int) -> int:
    """
    Returns the location value for a given AP location id
    """
    return location_id - BASE_OFFSET - LOCATION_OFFSET


def create_location_name_to_ap_id() -> Dict[str, int]:
    """
    Creates a map from item name to their AP item id
    """
    name_to_ap_id = {}
    index = 1
    for location in data.locations.values():
        name_to_ap_id[location.name] = offset_location_value(index)
        index += 1

    return name_to_ap_id

def create_location_groups(locations: Dict[int, ClairObscurLocationData]):
    location_groups: Dict[str, Set[str]] = {
        "Chest": set(),
        "Boss": set(),
        "Tower": set(),
        "Lost Gestral": set(),
        "Lost Gestral reward": set(),
        "Quest reward": set()
    }

    for loc in locations.keys():
        location_groups[locations[loc].type].add(locations[loc].name)

    return location_groups
