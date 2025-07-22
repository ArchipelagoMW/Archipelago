import typing

from BaseClasses import Entrance, Region
from .Items import item_list

from .Locations import (
    GLLocation,
    arctic_docks,
    battle_towers,
    battle_trenches,
    castle_courtyard,
    castle_treasury,
    chimeras_keep,
    cliffs_of_desolation,
    crystal_mine,
    dagger_peak,
    desecrated_temple,
    dragons_lair,
    dungeon_of_torment,
    erupting_fissure,
    frozen_camp,
    gates_of_the_underworld,
    haunted_cemetery,
    infernal_fortress,
    lost_cave,
    plague_fiend,
    poisoned_fields,
    tower_armory,
    toxic_air_ship,
    valley_of_fire,
    venomous_spire,
    volcanic_cavern,
    yeti,
    LocationData
)

if typing.TYPE_CHECKING:
    from . import GauntletLegendsWorld


def create_regions(world: "GauntletLegendsWorld"):
    world.multiworld.regions.append(Region("Menu", world.player, world.multiworld))

    create_region(world, "Valley of Fire", valley_of_fire)

    create_region(world, "Dagger Peak", dagger_peak)

    create_region(world, "Cliffs of Desolation", cliffs_of_desolation)

    create_region(world, "Lost Cave", lost_cave)

    create_region(world, "Volcanic Caverns", volcanic_cavern)

    create_region(world, "Dragon's Lair", dragons_lair)

    create_region(world, "Castle Courtyard", castle_courtyard)

    create_region(world, "Dungeon of Torment", dungeon_of_torment)

    create_region(world, "Tower Armory", tower_armory)

    create_region(world, "Castle Treasury", castle_treasury)

    create_region(world, "Chimera's Keep", chimeras_keep)

    create_region(world, "Poisonous Fields", poisoned_fields)

    create_region(world, "Haunted Cemetery", haunted_cemetery)

    create_region(world, "Venomous Spire", venomous_spire)

    create_region(world, "Toxic Air Ship", toxic_air_ship)

    create_region(world, "Vat of the Plague Fiend", plague_fiend)

    create_region(world, "Arctic Docks", arctic_docks)

    create_region(world, "Frozen Camp", frozen_camp)

    create_region(world, "Crystal Mine", crystal_mine)

    create_region(world, "Erupting Fissure", erupting_fissure)

    create_region(world, "Yeti", yeti)

    create_region(world, "Desecrated Temple", desecrated_temple)

    create_region(world, "Battle Trenches", battle_trenches)

    create_region(world, "Battle Towers", battle_towers)

    create_region(world, "Infernal Fortress", infernal_fortress)

    create_region(world, "Gates of the Underworld", gates_of_the_underworld)


def connect_regions(world: "GauntletLegendsWorld"):
    names: typing.Dict[str, int] = {}

    connect(world, names, "Menu", "Valley of Fire")
    connect(world, names, "Menu", "Dagger Peak")
    connect(world, names, "Menu", "Cliffs of Desolation")
    connect(world, names, "Menu", "Lost Cave")
    connect(world, names, "Menu", "Volcanic Caverns")
    connect(world, names, "Menu", "Dragon's Lair")
    connect(world, names, "Menu", "Castle Courtyard",
            lambda state: state.has("Mountain Obelisk 1", world.player)
            and state.has("Mountain Obelisk 2", world.player)
            and state.has("Mountain Obelisk 3", world.player)
    )
    connect(world, names, "Castle Courtyard", "Dungeon of Torment")
    connect(world, names, "Castle Courtyard", "Tower Armory")
    connect(world, names, "Castle Courtyard", "Castle Treasury")
    connect(world, names, "Castle Courtyard", "Chimera's Keep")
    connect(world, names, "Menu", "Poisonous Fields",
            lambda state: state.has("Castle Obelisk 1", world.player)
            and state.has("Castle Obelisk 2", world.player)
    )
    connect(world, names, "Poisonous Fields", "Haunted Cemetery")
    connect(world, names, "Poisonous Fields", "Venomous Spire")
    connect(world, names, "Poisonous Fields", "Toxic Air Ship")
    connect(world, names, "Toxic Air Ship", "Vat of the Plague Fiend")
    connect(world, names, "Menu", "Arctic Docks",
            lambda state: state.has("Town Obelisk 1", world.player)
            and state.has("Town Obelisk 2", world.player)
    )
    connect(world, names, "Arctic Docks", "Frozen Camp")
    connect(world, names, "Arctic Docks", "Crystal Mine")
    connect(world, names, "Arctic Docks", "Erupting Fissure")
    connect(world, names, "Erupting Fissure", "Yeti")
    connect(world, names, "Menu", "Desecrated Temple",
            lambda state: state.has("Dragon Mirror Shard", world.player)
            and state.has("Chimera Mirror Shard", world.player)
            and state.has("Plague Fiend Mirror Shard", world.player)
            and state.has("Yeti Mirror Shard", world.player)
    )
    connect(world, names, "Desecrated Temple", "Battle Trenches")
    connect(world, names, "Desecrated Temple", "Battle Towers")
    connect(world, names, "Desecrated Temple", "Infernal Fortress")
    connect(world, names, "Menu", "Gates of the Underworld",
            lambda state: state.has("stones", world.player, 13)
    )


def create_region(world: "GauntletLegendsWorld", name: str, locations: list[LocationData]):
    reg = Region(name, world.player, world.multiworld)
    reg.add_locations({loc.name: loc.id for loc in locations if loc.name not in world.disabled_locations}, GLLocation)
    world.multiworld.regions.append(reg)


def connect(world: "GauntletLegendsWorld",
            used_names: typing.Dict[str, int],
            source: str,
            target: str,
            rule: typing.Optional[typing.Callable] = None,
):
    source_region = world.multiworld.get_region(source, world.player)
    target_region = world.multiworld.get_region(target, world.player)

    if target not in used_names:
        used_names[target] = 1
        name = target
    else:
        used_names[target] += 1
        name = target + (" " * used_names[target])

    source_region.connect(target_region, name, rule)
