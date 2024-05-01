import typing

from BaseClasses import Region, Entrance
from .Locations import MLSSLocation, mainArea, chucklehuck, castleTown, startingFlag, chuckolatorFlag, piranhaFlag, \
    kidnappedFlag, beanstarFlag, birdoFlag, surfable, hooniversity, gwarharEntrance, gwarharMain, \
    fungitown, fungitownBeanstar, fungitownBirdo, teeheeValley, winkle, sewers, airport, \
    bowsers, bowsersMini, jokesEntrance, jokesMain, theater, booStatue, oasis, postJokes, baseUltraRocks, coins
from . import StateLogic

if typing.TYPE_CHECKING:
    from . import MLSSWorld


def create_regions(world: "MLSSWorld", excluded: typing.List[str]):
    menu_region = Region("Menu", world.player, world.multiworld)
    world.multiworld.regions.append(menu_region)

    create_region(world, "Main Area", mainArea, excluded)
    create_region(world, "Chucklehuck Woods", chucklehuck, excluded)
    create_region(world, "Beanbean Castle Town", castleTown, excluded)
    create_region(world, "Shop Starting Flag", startingFlag, excluded)
    create_region(world, "Shop Chuckolator Flag", chuckolatorFlag, excluded)
    create_region(world, "Shop Mom Piranha Flag", piranhaFlag, excluded)
    create_region(world, "Shop Enter Fungitown Flag", kidnappedFlag, excluded)
    create_region(world, "Shop Beanstar Complete Flag", beanstarFlag, excluded)
    create_region(world, "Shop Birdo Flag", birdoFlag, excluded)
    create_region(world, "Surfable", surfable, excluded)
    create_region(world, "Hooniversity", hooniversity, excluded)
    create_region(world, "GwarharEntrance", gwarharEntrance, excluded)
    create_region(world, "GwarharMain", gwarharMain, excluded)
    create_region(world, "TeeheeValley", teeheeValley, excluded)
    create_region(world, "Winkle", winkle, excluded)
    create_region(world, "Sewers", sewers, excluded)
    create_region(world, "Airport", airport, excluded)
    create_region(world, "JokesEntrance", jokesEntrance, excluded)
    create_region(world, "JokesMain", jokesMain, excluded)
    create_region(world, "PostJokes", postJokes, excluded)
    create_region(world, "Theater", theater, excluded)
    create_region(world, "Fungitown", fungitown, excluded)
    create_region(world, "Fungitown Shop Beanstar Complete Flag", fungitownBeanstar, excluded)
    create_region(world, "Fungitown Shop Birdo Flag", fungitownBirdo, excluded)
    create_region(world, "BooStatue", booStatue, excluded)
    create_region(world, "Oasis", oasis, excluded)
    create_region(world, "BaseUltraRocks", baseUltraRocks, excluded)

    if world.options.coins:
        create_region(world, "Coins", coins, excluded)

    if not world.options.castle_skip:
        create_region(world, "Bowser's Castle", bowsers, excluded)
        create_region(world, "Bowser's Castle Mini", bowsersMini, excluded)


def connect_regions(world: "MLSSWorld"):
    names: typing.Dict[str, int] = {}

    connect(world, names, "Menu", "Main Area")
    if world.options.coins:
        connect(world, names, "Main Area", "Coins")
    connect(world, names, "Main Area", "BaseUltraRocks", StateLogic.ultra(world.player))
    connect(world, names, "Main Area", "Chucklehuck Woods", StateLogic.brooch(world.player))
    connect(world, names, "Main Area", "BooStatue", StateLogic.canCrash(world.player))
    connect(world, names, "Main Area", "Hooniversity", StateLogic.canDig(world.player) and StateLogic.canMini(world.player))
    connect(world, names, "Hooniversity", "Oasis")
    connect(world, names, "Main Area", "TeeheeValley", StateLogic.super(world.player) or StateLogic.canDash(world.player))
    connect(world, names, "TeeheeValley", "GwarharEntrance", StateLogic.membership(world.player) and StateLogic.fire(world.player))
    connect(world, names, "TeeheeValley", "Oasis", StateLogic.membership(world.player) and StateLogic.fire(world.player))
    connect(world, names, "TeeheeValley", "Fungitown", StateLogic.thunder(world.player) and StateLogic.castleTown(world.player) and StateLogic.rose(world.player))
    connection = connect(world, names, "Fungitown", "Fungitown Shop Beanstar Complete Flag", StateLogic.pieces(world.player) or StateLogic.fungitown_birdo_shop(world.player), True)
    world.multiworld.register_indirect_condition(world.get_region("Fungitown Shop Birdo Flag"), connection)
    connect(world, names, "Main Area", "Shop Starting Flag", StateLogic.brooch(world.player) or StateLogic.rose(world.player))
    connection = connect(world, names, "Shop Starting Flag", "Shop Chuckolator Flag", (StateLogic.brooch(world.player) and StateLogic.fruits(world.player) and (StateLogic.thunder(world.player) or StateLogic.fire(world.player) or StateLogic.hammers(world.player))) or StateLogic.piranha_shop(world.player), True)
    world.multiworld.register_indirect_condition(world.get_region("Shop Mom Piranha Flag"), connection)
    connection = connect(world, names, "Shop Starting Flag", "Shop Mom Piranha Flag", StateLogic.thunder(world.player) or StateLogic.fungitown_shop(world.player), True)
    world.multiworld.register_indirect_condition(world.get_region("Shop Enter Fungitown Flag"), connection)
    connect(world, names, "Shop Starting Flag", "Shop Enter Fungitown Flag", StateLogic.fungitown(world.player) or StateLogic.star_shop(world.player), True)
    world.multiworld.register_indirect_condition(world.get_region("Shop Beanstar Complete Flag"), connection)
    connect(world, names, "Shop Starting Flag", "Shop Beanstar Complete Flag", (StateLogic.castleTown(world.player) and StateLogic.pieces(world.player) and StateLogic.rose(world.player)) or StateLogic.birdo_shop(world.player), True)
    world.multiworld.register_indirect_condition(world.get_region("Shop Birdo Flag"), connection)
    connect(world, names, "Main Area", "Sewers", StateLogic.rose(world.player))
    connect(world, names, "Main Area", "Airport", StateLogic.thunder(world.player))
    connect(world, names, "Main Area", "Theater", StateLogic.canDash(world.player))
    connect(world, names, "Main Area", "Surfable", StateLogic.surfable(world.player))
    connect(world, names, "Surfable", "GwarharEntrance")
    connect(world, names, "Surfable", "Oasis")
    connect(world, names, "Surfable", "JokesEntrance", StateLogic.fire(world.player))
    connect(world, names, "JokesMain", "PostJokes", StateLogic.postJokes(world.player))
    if not world.options.castle_skip:
        connect(world, names, "PostJokes", "Bowser's Castle")
        connect(world, names, "Bowser's Castle", "Bowser's Castle Mini", StateLogic.canMini(world.player) and StateLogic.thunder(world.player))
    connect(world, names, "Chucklehuck Woods", "Winkle", StateLogic.canDash(world.player))
    connect(world, names, "Chucklehuck Woods", "Beanbean Castle Town", StateLogic.fruits(world.player) and (StateLogic.hammers(world.player) or StateLogic.fire(world.player) or StateLogic.thunder(world.player)))
    if world.options.difficult_logic:
        connect(world, names, "GwarharEntrance", "GwarharMain", StateLogic.canDash(world.player))
        connect(world, names, "JokesEntrance", "JokesMain", StateLogic.canDig(world.player))
        connect(world, names, "Shop Starting Flag", "Shop Birdo Flag", StateLogic.postJokes(world.player))
        connect(world, names, "Fungitown", "Fungitown Shop Birdo Flag", StateLogic.postJokes(world.player))
    else:
        connect(world, names, "GwarharEntrance", "GwarharMain", StateLogic.canDash(world.player) and StateLogic.canCrash(world.player))
        connect(world, names, "JokesEntrance", "JokesMain", StateLogic.canCrash(world.player) and StateLogic.canDig(world.player))
        connect(world, names, "Shop Starting Flag", "Shop Birdo Flag", StateLogic.canCrash(world.player) and StateLogic.postJokes(world.player))
        connect(world, names, "Fungitown", "Fungitown Shop Birdo Flag", StateLogic.canCrash(world.player) and StateLogic.postJokes(world.player))


def create_region(world: "MLSSWorld", name, locations, excluded):
    ret = Region(name, world.player, world.multiworld)
    for location in locations:
        loc = MLSSLocation(world.player, location.name, location.id, ret)
        if location.name in excluded:
            continue
        ret.locations.append(loc)
    world.multiworld.regions.append(ret)


def connect(world: "MLSSWorld", used_names: typing.Dict[str, int], source: str, target: str,
            rule: typing.Optional[typing.Callable] = None, reach: typing.Optional[bool] = False) -> Entrance | None:
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
    if reach:
        return connection
    else:
        return None
