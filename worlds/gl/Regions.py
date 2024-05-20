import typing

from BaseClasses import Region, Entrance
from .Locations import GLLocation, valleyOfFire, daggerPeak, cliffsOfDesolation, lostCave, volcanicCavern \
    , dragonsLair, castleCourtyard, dungeonOfTorment, towerArmory \
    , castleTreasury, chimerasKeep, poisonedFields, hauntedCemetery \
    , venomousSpire, toxicAirShip, arcticDocks, frozenCamp \
    , crystalMine, eruptingFissure, desecratedTemple \
    , battleTrenches, battleTowers, infernalFortress \
    , gatesOfTheUnderworld, plagueFiend, yeti

if typing.TYPE_CHECKING:
    from . import GauntletLegendsWorld


def create_regions(world: "GauntletLegendsWorld"):
    world.multiworld.regions.append(Region("Menu", world.player, world.multiworld))

    create_region(world, "Valley of Fire", valleyOfFire)

    create_region(world, "Dagger Peak", daggerPeak)

    create_region(world, "Cliffs of Desolation", cliffsOfDesolation)

    create_region(world, "Lost Cave", lostCave)

    create_region(world, "Volcanic Caverns", volcanicCavern)

    create_region(world, "Dragon's Lair", dragonsLair)

    create_region(world, "Castle Courtyard", castleCourtyard)

    create_region(world, "Dungeon of Torment", dungeonOfTorment)

    create_region(world, "Tower Armory", towerArmory)

    create_region(world, "Castle Treasury", castleTreasury)

    create_region(world, "Chimera's Keep", chimerasKeep)

    create_region(world, "Poisonous Fields", poisonedFields)

    create_region(world, "Haunted Cemetery", hauntedCemetery)

    create_region(world, "Venomous Spire", venomousSpire)

    create_region(world, "Toxic Air Ship", toxicAirShip)

    create_region(world, "Vat of the Plague Fiend", plagueFiend)

    create_region(world, "Arctic Docks", arcticDocks)

    create_region(world, "Frozen Camp", frozenCamp)

    create_region(world, "Crystal Mine", crystalMine)

    create_region(world, "Erupting Fissure", eruptingFissure)

    create_region(world, "Yeti", yeti)

    create_region(world, "Desecrated Temple", desecratedTemple)

    create_region(world, "Battle Trenches", battleTrenches)

    create_region(world, "Battle Towers", battleTowers)

    create_region(world, "Infernal Fortress", infernalFortress)

    create_region(world, "Gates of the Underworld", gatesOfTheUnderworld)


def connect_regions(world: "GauntletLegendsWorld"):
    names: typing.Dict[str, int] = {}

    connect(world, names, "Menu", "Valley of Fire")
    connect(world, names, "Menu", "Dagger Peak")
    connect(world, names, "Menu", "Cliffs of Desolation")
    connect(world, names, "Menu", "Lost Cave")
    connect(world, names, "Menu", "Volcanic Caverns")
    connect(world, names, "Menu", "Dragon's Lair")
    connect(world, names, "Valley of Fire", "Castle Courtyard", lambda state: state.has("Valley of Fire Obelisk", world.player) and state.has("Dagger Peak Obelisk", world.player) and state.has("Cliffs of Desolation Obelisk", world.player))
    connect(world, names, "Castle Courtyard", "Dungeon of Torment")
    connect(world, names, "Castle Courtyard", "Tower Armory")
    connect(world, names, "Castle Courtyard", "Castle Treasury")
    connect(world, names, "Castle Courtyard", "Chimera's Keep")
    connect(world, names, "Valley of Fire", "Poisonous Fields", lambda state: state.has("Castle Courtyard Obelisk", world.player) and state.has("Dungeon of Torment Obelisk", world.player))
    connect(world, names, "Poisonous Fields", "Haunted Cemetery")
    connect(world, names, "Poisonous Fields", "Venomous Spire")
    connect(world, names, "Poisonous Fields", "Toxic Air Ship")
    connect(world, names, "Toxic Air Ship", "Vat of the Plague Fiend")
    connect(world, names, "Valley of Fire", "Arctic Docks", lambda state: state.has("Poisoned Fields Obelisk", world.player) and state.has("Haunted Cemetery Obelisk", world.player))
    connect(world, names, "Arctic Docks", "Frozen Camp")
    connect(world, names, "Arctic Docks", "Crystal Mine")
    connect(world, names, "Arctic Docks", "Erupting Fissure")
    connect(world, names, "Erupting Fissure", "Yeti")
    connect(world, names, "Valley of Fire", "Desecrated Temple", lambda state: state.has("Dragon Mirror Shard", world.player) and state.has("Chimera Mirror Shard", world.player) and state.has("Plague Fiend Mirror Shard", world.player) and state.has("Yeti Mirror Shard", world.player))
    connect(world, names, "Desecrated Temple", "Battle Trenches")
    connect(world, names, "Desecrated Temple", "Battle Towers")
    connect(world, names, "Desecrated Temple", "Infernal Fortress")
    connect(world, names, "Valley of Fire", "Gates of the Underworld",
            lambda state: state.has("Runestone 1", world.player) and state.has("Runestone 2", world.player)
            and state.has("Runestone 3", world.player) and state.has("Runestone 4", world.player)
            and state.has("Runestone 5", world.player) and state.has("Runestone 6", world.player)
            and state.has("Runestone 7", world.player) and state.has("Runestone 8", world.player)
            and state.has("Runestone 9", world.player) and state.has("Runestone 10", world.player)
            and state.has("Runestone 11", world.player) and state.has("Runestone 12", world.player)
            and state.has("Runestone 13", world.player))


def create_region(world: "GauntletLegendsWorld", name, locations):
    reg = Region(name, world.player, world.multiworld)
    for location in locations:
        if location.name not in world.disabled_locations:
            loc = GLLocation(world.player, location.name, location.id, reg)
            reg.locations.append(loc)
    world.multiworld.regions.append(reg)


def connect(world: "GauntletLegendsWorld", used_names: typing.Dict[str, int], source: str, target: str,
            rule: typing.Optional[typing.Callable] = None):
    source_region = world.multiworld.get_region(source, world.player)
    target_region = world.multiworld.get_region(target, world.player)

    if target not in used_names:
        used_names[target] = 1
        name = target
    else:
        used_names[target] += 1
        name = target + (' ' * used_names[target])

    connection = Entrance(world.player, name, source_region)

    if rule:
        connection.access_rule = rule

    source_region.exits.append(connection)
    connection.connect(target_region)
