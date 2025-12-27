import typing
from typing import Optional, Callable

from BaseClasses import Region
from .Data import excluded_levels

from .Locations import GLLocation, LocationData, get_locations_by_tags

if typing.TYPE_CHECKING:
    from . import GauntletLegendsWorld


def create_regions(world: "GauntletLegendsWorld"):
    world.multiworld.regions.append(Region("Menu", world.player, world.multiworld))

    regions_dict = get_regions_dict()
    for name, locations in regions_dict.items():
        if name not in [level for region, levels in excluded_levels.items() if region in world.excluded_regions for level in levels]:
            create_region(world, name, locations)
        else:
            world.disabled_locations.update([loc.name for loc in locations if loc.name not in world.disabled_locations])

def get_regions_dict() -> dict[str, list[LocationData]]:
    """
    Returns a dictionary mapping region names to their corresponding location data lists.
    """
    return {
        "Valley of Fire": get_locations_by_tags("valley_of_fire"),
        "Dagger Peak": get_locations_by_tags("dagger_peak"),
        "Cliffs of Desolation": get_locations_by_tags("cliffs_of_desolation"),
        "Lost Cave": get_locations_by_tags("lost_cave"),
        "Volcanic Caverns": get_locations_by_tags("volcanic_cavern"),
        "Dragon's Lair": get_locations_by_tags("dragons_lair"),
        "Castle Courtyard": get_locations_by_tags("castle_courtyard"),
        "Dungeon of Torment": get_locations_by_tags("dungeon_of_torment"),
        "Tower Armory": get_locations_by_tags("tower_armory"),
        "Castle Treasury": get_locations_by_tags("castle_treasury"),
        "Chimera's Keep": get_locations_by_tags("chimeras_keep"),
        "Poisoned Fields": get_locations_by_tags("poisoned_fields"),
        "Haunted Cemetery": get_locations_by_tags("haunted_cemetery"),
        "Venomous Spire": get_locations_by_tags("venomous_spire"),
        "Toxic Air Ship": get_locations_by_tags("toxic_air_ship"),
        "Vat of the Plague Fiend": get_locations_by_tags("plague_fiend"),
        "Arctic Docks": get_locations_by_tags("arctic_docks"),
        "Frozen Camp": get_locations_by_tags("frozen_camp"),
        "Crystal Mine": get_locations_by_tags("crystal_mine"),
        "Erupting Fissure": get_locations_by_tags("erupting_fissure"),
        "Yeti's Cavern": get_locations_by_tags("yeti"),
        "Desecrated Temple": get_locations_by_tags("desecrated_temple"),
        "Altar of Skorne": get_locations_by_tags("altar_of_skorne"),
        "Battle Trenches": get_locations_by_tags("battle_trenches"),
        "Fortified Towers": get_locations_by_tags("fortified_towers"),
        "Infernal Fortress": get_locations_by_tags("infernal_fortress"),
        "Gates of the Underworld": get_locations_by_tags("gates_of_the_underworld")
    }


def connect_regions(world: "GauntletLegendsWorld"):
    names: dict[str, int] = {}

    connect(world, names, "Menu", "Valley of Fire")
    connect(world, names, "Menu", "Dagger Peak", _portal_helper("Portal to Dagger Peak", world))
    connect(world, names, "Menu", "Cliffs of Desolation", _portal_helper("Portal to Cliffs of Desolation", world))
    connect(world, names, "Menu", "Lost Cave", _portal_helper("Portal to Lost Cave", world))
    connect(world, names, "Menu", "Volcanic Caverns", _portal_helper("Portal to Volcanic Caverns", world))
    connect(world, names, "Menu", "Dragon's Lair", _portal_helper("Portal to Dragon's Lair", world))
    connect(world, names, "Menu", "Castle Courtyard",
            lambda state: state.has("Valley of Fire Obelisk", world.player)
            and state.has("Dagger Peak Obelisk", world.player)
            and state.has("Cliffs of Desolation Obelisk", world.player)
    )
    connect(world, names, "Castle Courtyard", "Dungeon of Torment", _portal_helper("Portal to Dungeon of Torment", world))
    connect(world, names, "Castle Courtyard", "Tower Armory", _portal_helper("Portal to Tower Armory", world))
    connect(world, names, "Castle Courtyard", "Castle Treasury", _portal_helper("Portal to Castle Treasury", world))
    connect(world, names, "Castle Courtyard", "Chimera's Keep", _portal_helper("Portal to Chimera's Keep", world))
    connect(world, names, "Menu", "Poisoned Fields",
            lambda state: state.has("Castle Courtyard Obelisk", world.player)
            and state.has("Dungeon of Torment Obelisk", world.player)
    )
    connect(world, names, "Poisoned Fields", "Haunted Cemetery", _portal_helper("Portal to Haunted Cemetery", world))
    connect(world, names, "Poisoned Fields", "Venomous Spire", _portal_helper("Portal to Venomous Spire", world))
    connect(world, names, "Poisoned Fields", "Toxic Air Ship", _portal_helper("Portal to Toxic Air Ship", world))
    connect(world, names, "Toxic Air Ship", "Vat of the Plague Fiend", _portal_helper("Portal to Vat of the Plague Fiend", world))
    connect(world, names, "Menu", "Arctic Docks",
            lambda state: state.has("Poisoned Fields Obelisk", world.player)
            and state.has("Haunted Cemetery Obelisk", world.player)
    )
    connect(world, names, "Arctic Docks", "Frozen Camp", _portal_helper("Portal to Frozen Camp", world))
    connect(world, names, "Arctic Docks", "Crystal Mine", _portal_helper("Portal to Crystal Mine", world))
    connect(world, names, "Arctic Docks", "Erupting Fissure", _portal_helper("Portal to Erupting Fissure", world))
    connect(world, names, "Erupting Fissure", "Yeti's Cavern", _portal_helper("Portal to Yeti's Cavern", world))
    connect(world, names, "Menu", "Desecrated Temple",
            lambda state: state.has("Dragon Mirror Shard", world.player)
            and state.has("Chimera Mirror Shard", world.player)
            and state.has("Plague Fiend Mirror Shard", world.player)
            and state.has("Yeti Mirror Shard", world.player)
    )
    connect(world, names, "Desecrated Temple", "Altar of Skorne")
    connect(world, names, "Desecrated Temple", "Battle Trenches")
    connect(world, names, "Desecrated Temple", "Fortified Towers", _portal_helper("Portal to Fortified Towers", world))
    connect(world, names, "Desecrated Temple", "Infernal Fortress", _portal_helper("Portal to Infernal Fortress", world))
    connect(world, names, "Menu", "Gates of the Underworld",
            lambda state: state.has("stones", world.player, 13)
    )

def _portal_helper(item: str, world: "GauntletLegendsWorld") -> Callable:
    return lambda state, portals=bool(world.options.portals.value): (state.has(item, world.player) if portals else True)


def create_region(world: "GauntletLegendsWorld", name: str, locations: list[LocationData]):
    reg = Region(name, world.player, world.multiworld)
    reg.add_locations({loc.name: loc.id for loc in locations if loc.name not in world.disabled_locations}, GLLocation)
    world.multiworld.regions.append(reg)


def connect(world: "GauntletLegendsWorld",
            used_names: dict[str, int],
            source: str,
            target: str,
            rule: Optional[Callable] = None,
):
    excluded_levels_ = [level for region, levels in excluded_levels.items() if region in world.excluded_regions for level in levels]
    if source in excluded_levels_ or target in excluded_levels_:
        return
    source_region = world.multiworld.get_region(source, world.player)
    target_region = world.multiworld.get_region(target, world.player)

    if target not in used_names:
        used_names[target] = 1
        name = target
    else:
        used_names[target] += 1
        name = target + (" " * used_names[target])

    source_region.connect(target_region, name, rule)
