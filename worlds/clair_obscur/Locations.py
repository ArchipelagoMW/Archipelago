from typing import Dict, Optional, TYPE_CHECKING, Set

from BaseClasses import Location, Region, LocationProgressType
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

# def set_weapons_to_normal(world: "ClairObscurWorld") -> None:
#     """
#     Sets all weapon item classifications to normal rather than useful. Necessary if Exclude Endgame Locations is on,
#     otherwise there aren't enough filler items to fill the excluded locations.
#     """
#     for item in world.item_name_groups["Weapon"]:
#         world.multiworld.get_items()

def create_locations(world: "ClairObscurWorld", regions: Dict[str, Region]) -> None:

    #These locations were in data dumps but not confirmed to be either accessible or inaccessible.
    #These will be left in the pool in case they're found in testing, but will contain filler to avoid softlocks.
    unconfirmed_location_names = ["Monolith: Tower Peak - Left before Expedition Flag (This might be in the void)",
        "World Map: Unknown 2",
        "World Map: Unknown 1",
        "Lumiere (Act 3): Lumina 5",
        "Lumiere (Act 3): Upgrade 6",
        "Red Woods: Lumina 1",
        "Sea Cliff: Chroma 1"]

    excluded_types = []
    excluded_conditions = []
    if not world.options.shuffle_free_aim: excluded_conditions.append("Free Aim")
    if not world.options.gestral_shuffle: excluded_conditions.append("Lost Gestral")

    exclusion_level = 99
    if world.options.exclude_endgame_locations < 2 and world.options.goal < 2:
        exclusion_level = 16 + world.options.goal
        #Conveniently, the Monolith and Lumiere are 1 pictos_level apart.

    if not world.options.gestral_shuffle:
        excluded_types.append("Lost Gestral")

    for region_name, region in regions.items():
        if region_name == "Menu": continue
        if world.options.exclude_endless_tower == 0 and region_name.startswith("Endless Tower"): continue
        region_data = data.regions[region_name]
        region_level = region_data.pictos_level
        if world.options.exclude_endgame_locations == 0 and region_level >= exclusion_level: continue

        for location_name in region_data.locations:

            location_data = data.locations[location_name]
            location_level = max(location_data.pictos_level, region_level)
            if (location_data.type in excluded_types or
                    (world.options.exclude_endgame_locations == 0 and location_level >= exclusion_level)):
                continue

            loc_id = world.location_name_to_id[location_data.name]
            location = ClairObscurLocation(
                world.player,
                location_data.name,
                loc_id,
                region,
                location_data.default_item
            )
            conditions = location_data.condition
            if conditions:
                for cond in conditions:
                    if cond in excluded_conditions: continue
                    amount = conditions[cond]
                    add_rule(location, lambda state, con=cond, pl=world.player, am=amount: state.has(con, pl, am))

            if location_data.type == "Boss":
                location.progress_type = LocationProgressType.PRIORITY

            if location_data.pictos_level > 1:
                #Checks location_data rather than location_level here as this doesn't need to run if there's already
                #a region access rule for pictos level.
                converted_pictos = world.convert_pictos(location_level)
                add_rule(location, lambda state, pl=world.player, pic=converted_pictos:
                    state.has_group("Picto", pl, pic))

            if world.options.exclude_endgame_locations == 1 and location_level >= exclusion_level:
                location.progress_type = LocationProgressType.EXCLUDED

            if world.options.exclude_endless_tower == 1 and region_name.startswith("Endless Tower"):
                location.progress_type = LocationProgressType.EXCLUDED

            if location_name in unconfirmed_location_names:
                location.progress_type = LocationProgressType.EXCLUDED

            region.locations.append(location)


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
    index = 0
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
