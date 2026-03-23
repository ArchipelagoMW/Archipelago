import typing

from BaseClasses import Region, Entrance
from .Locations import (
    MLSSLocation,
    mainArea,
    chucklehuck,
    castleTown,
    startingFlag,
    chuckolatorFlag,
    piranhaFlag,
    kidnappedFlag,
    beanstarFlag,
    birdoFlag,
    surfable,
    hooniversity,
    gwarharEntrance,
    gwarharMain,
    fungitown,
    fungitownBeanstar,
    fungitownBirdo,
    teeheeValley,
    winkle,
    sewers,
    airport,
    bowsers,
    bowsersMini,
    jokesEntrance,
    jokesMain,
    theater,
    booStatue,
    oasis,
    postJokes,
    baseUltraRocks,
    coins,
    cacklettas_soul,
)
from . import StateLogic

if typing.TYPE_CHECKING:
    from . import MLSSWorld


def create_regions(world: "MLSSWorld"):
    menu_region = Region("Menu", world.player, world.multiworld)
    world.multiworld.regions.append(menu_region)

    create_region(world, "Main Area", mainArea)
    create_region(world, "Chucklehuck Woods", chucklehuck)
    create_region(world, "Beanbean Castle Town", castleTown)
    create_region(world, "Shop Starting Flag", startingFlag)
    create_region(world, "Shop Chuckolator Flag", chuckolatorFlag)
    create_region(world, "Shop Mom Piranha Flag", piranhaFlag)
    create_region(world, "Shop Enter Fungitown Flag", kidnappedFlag)
    create_region(world, "Shop Beanstar Complete Flag", beanstarFlag)
    create_region(world, "Shop Birdo Flag", birdoFlag)
    create_region(world, "Surfable", surfable)
    create_region(world, "Hooniversity", hooniversity)
    create_region(world, "GwarharEntrance", gwarharEntrance)
    create_region(world, "GwarharMain", gwarharMain)
    create_region(world, "TeeheeValley", teeheeValley)
    create_region(world, "Winkle", winkle)
    create_region(world, "Sewers", sewers)
    create_region(world, "Airport", airport)
    create_region(world, "JokesEntrance", jokesEntrance)
    create_region(world, "JokesMain", jokesMain)
    create_region(world, "PostJokes", postJokes)
    create_region(world, "Theater", theater)
    create_region(world, "Fungitown", fungitown)
    create_region(world, "Fungitown Shop Beanstar Complete Flag", fungitownBeanstar)
    create_region(world, "Fungitown Shop Birdo Flag", fungitownBirdo)
    create_region(world, "BooStatue", booStatue)
    create_region(world, "Oasis", oasis)
    create_region(world, "BaseUltraRocks", baseUltraRocks)
    create_region(world, "Cackletta's Soul", cacklettas_soul)

    if world.options.coins:
        create_region(world, "Coins", coins)

    if not world.options.castle_skip:
        create_region(world, "Bowser's Castle", bowsers)
        create_region(world, "Bowser's Castle Mini", bowsersMini)


def connect_regions(world: "MLSSWorld"):
    names: typing.Dict[str, int] = {}

    connect(world, names, "Menu", "Main Area")
    if world.options.coins:
        connect(world, names, "Main Area", "Coins")
    connect(world, names, "Main Area", "BaseUltraRocks", lambda state: StateLogic.ultra(state, world.player))
    connect(world, names, "Main Area", "Chucklehuck Woods", lambda state: StateLogic.brooch(state, world.player))
    connect(world, names, "Main Area", "BooStatue", lambda state: StateLogic.canCrash(state, world.player))
    if world.options.goal == "emblem_hunt":
        if world.options.castle_skip:
            connect(world, names, "Main Area", "Cackletta's Soul",
                    lambda state: state.has("Beanstar Emblem", world.player, world.options.emblems_required.value))
        else:
            connect(world, names, "Main Area", "Bowser's Castle", lambda state: state.has("Beanstar Emblem", world.player, world.options.emblems_required.value))
            connect(world, names, "Bowser's Castle", "Bowser's Castle Mini", lambda state:
                                  StateLogic.canMini(state, world.player)
                                  and StateLogic.thunder(state,world.player))
            connect(world, names, "Bowser's Castle Mini", "Cackletta's Soul", lambda state: StateLogic.soul(state, world.player))
    connect(
        world,
        names,
        "Main Area",
        "Hooniversity",
        lambda state: StateLogic.canDig(state, world.player) and StateLogic.canMini(state, world.player),
    )
    connect(world, names, "Hooniversity", "Oasis")
    connect(
        world,
        names,
        "Main Area",
        "TeeheeValley",
        lambda state: StateLogic.super(state, world.player) or StateLogic.canDash(state, world.player),
    )
    connect(
        world,
        names,
        "TeeheeValley",
        "GwarharEntrance",
        lambda state: StateLogic.membership(state, world.player) and StateLogic.fire(state, world.player),
    )
    connect(
        world,
        names,
        "TeeheeValley",
        "Oasis",
        lambda state: StateLogic.membership(state, world.player) and StateLogic.fire(state, world.player),
    )
    connect(
        world,
        names,
        "TeeheeValley",
        "Fungitown",
        lambda state: StateLogic.thunder(state, world.player)
        and StateLogic.castleTown(state, world.player)
        and StateLogic.rose(state, world.player),
    )
    connection = connect(
        world,
        names,
        "Fungitown",
        "Fungitown Shop Beanstar Complete Flag",
        lambda state: StateLogic.pieces(state, world.player) or StateLogic.fungitown_birdo_shop(state, world.player),
        True,
    )
    world.multiworld.register_indirect_condition(world.get_region("Fungitown Shop Birdo Flag"), connection)
    connect(world, names, "Main Area", "Shop Starting Flag")
    connection = connect(
        world,
        names,
        "Shop Starting Flag",
        "Shop Chuckolator Flag",
        lambda state: (
            StateLogic.brooch(state, world.player)
            and StateLogic.fruits(state, world.player)
            and (
                StateLogic.thunder(state, world.player)
                or StateLogic.fire(state, world.player)
                or StateLogic.hammers(state, world.player)
            )
        )
        or (
            StateLogic.piranha_shop(state, world.player)
            or StateLogic.fungitown_shop(state, world.player)
            or StateLogic.star_shop(state, world.player)
            or StateLogic.birdo_shop(state, world.player)
        ),
        True,
    )
    world.multiworld.register_indirect_condition(world.get_region("Shop Mom Piranha Flag"), connection)
    world.multiworld.register_indirect_condition(world.get_region("Shop Enter Fungitown Flag"), connection)
    world.multiworld.register_indirect_condition(world.get_region("Shop Beanstar Complete Flag"), connection)
    world.multiworld.register_indirect_condition(world.get_region("Shop Birdo Flag"), connection)
    connection = connect(
        world,
        names,
        "Shop Starting Flag",
        "Shop Mom Piranha Flag",
        lambda state: StateLogic.thunder(state, world.player)
        or (
            StateLogic.fungitown_shop(state, world.player)
            or StateLogic.star_shop(state, world.player)
            or StateLogic.birdo_shop(state, world.player)
        ),
        True,
    )
    world.multiworld.register_indirect_condition(world.get_region("Shop Enter Fungitown Flag"), connection)
    world.multiworld.register_indirect_condition(world.get_region("Shop Beanstar Complete Flag"), connection)
    world.multiworld.register_indirect_condition(world.get_region("Shop Birdo Flag"), connection)
    connection = connect(
        world,
        names,
        "Shop Starting Flag",
        "Shop Enter Fungitown Flag",
        lambda state: StateLogic.fungitown(state, world.player)
        or (StateLogic.star_shop(state, world.player) or StateLogic.birdo_shop(state, world.player)),
        True,
    )
    world.multiworld.register_indirect_condition(world.get_region("Shop Beanstar Complete Flag"), connection)
    world.multiworld.register_indirect_condition(world.get_region("Shop Birdo Flag"), connection)
    connection = connect(
        world,
        names,
        "Shop Starting Flag",
        "Shop Beanstar Complete Flag",
        lambda state: (
            StateLogic.castleTown(state, world.player)
            and StateLogic.pieces(state, world.player)
            and StateLogic.rose(state, world.player)
        )
        or StateLogic.birdo_shop(state, world.player),
        True,
    )
    world.multiworld.register_indirect_condition(world.get_region("Shop Birdo Flag"), connection)
    connect(world, names, "Main Area", "Sewers", lambda state: StateLogic.rose(state, world.player))
    connect(world, names, "Main Area", "Airport", lambda state: StateLogic.thunder(state, world.player))
    connect(world, names, "Main Area", "Theater", lambda state: StateLogic.canDash(state, world.player))
    connect(world, names, "Main Area", "Surfable", lambda state: StateLogic.surfable(state, world.player))
    connect(world, names, "Surfable", "GwarharEntrance")
    connect(world, names, "Surfable", "Oasis")
    connect(world, names, "Surfable", "JokesEntrance", lambda state: StateLogic.fire(state, world.player))
    connect(world, names, "JokesMain", "PostJokes", lambda state: StateLogic.postJokes(state, world.player, world.options.goal.value))
    if not world.options.castle_skip and world.options.goal != "emblem_hunt":
        connect(world, names, "PostJokes", "Bowser's Castle")
        connect(
            world,
            names,
            "Bowser's Castle",
            "Bowser's Castle Mini",
            lambda state: StateLogic.canMini(state, world.player) and StateLogic.thunder(state, world.player),
        )
        connect(world, names, "Bowser's Castle Mini", "Cackletta's Soul")
    elif world.options.goal != "emblem_hunt":
        connect(world, names, "PostJokes", "Cackletta's Soul")
    connect(world, names, "Chucklehuck Woods", "Winkle", lambda state: StateLogic.canDash(state, world.player))
    connect(
        world,
        names,
        "Chucklehuck Woods",
        "Beanbean Castle Town",
        lambda state: StateLogic.fruits(state, world.player)
        and (
            StateLogic.hammers(state, world.player)
            or StateLogic.fire(state, world.player)
            or StateLogic.thunder(state, world.player)
        ),
    )
    if world.options.difficult_logic:
        connect(world, names, "GwarharEntrance", "GwarharMain", lambda state: StateLogic.canDash(state, world.player))
        connect(world, names, "JokesEntrance", "JokesMain", lambda state: StateLogic.canDig(state, world.player))
        connect(
            world,
            names,
            "Shop Starting Flag",
            "Shop Birdo Flag",
            lambda state: StateLogic.postJokes(state, world.player, world.options.goal.value),
        )
        connect(
            world,
            names,
            "Fungitown",
            "Fungitown Shop Birdo Flag",
            lambda state: StateLogic.postJokes(state, world.player, world.options.goal.value),
        )
    else:
        connect(
            world,
            names,
            "GwarharEntrance",
            "GwarharMain",
            lambda state: StateLogic.canDash(state, world.player) and StateLogic.canCrash(state, world.player),
        )
        connect(
            world,
            names,
            "JokesEntrance",
            "JokesMain",
            lambda state: StateLogic.canCrash(state, world.player) and StateLogic.canDig(state, world.player),
        )
        connect(
            world,
            names,
            "Shop Starting Flag",
            "Shop Birdo Flag",
            lambda state: StateLogic.canCrash(state, world.player) and StateLogic.postJokes(state, world.player, world.options.goal.value),
        )
        connect(
            world,
            names,
            "Fungitown",
            "Fungitown Shop Birdo Flag",
            lambda state: StateLogic.canCrash(state, world.player) and StateLogic.postJokes(state, world.player, world.options.goal.value),
        )


def create_region(world: "MLSSWorld", name, locations):
    ret = Region(name, world.player, world.multiworld)
    for location in locations:
        loc = MLSSLocation(world.player, location.name, location.id, ret)
        if location.name in world.disabled_locations:
            continue
        ret.locations.append(loc)
    world.multiworld.regions.append(ret)


def connect(
    world: "MLSSWorld",
    used_names: typing.Dict[str, int],
    source: str,
    target: str,
    rule: typing.Optional[typing.Callable] = None,
    reach: typing.Optional[bool] = False,
) -> typing.Optional[Entrance]:
    source_region = world.multiworld.get_region(source, world.player)
    target_region = world.multiworld.get_region(target, world.player)

    if target not in used_names:
        used_names[target] = 1
        name = target
    else:
        used_names[target] += 1
        name = target + (" " * used_names[target])

    connection = Entrance(world.player, name, source_region)

    if rule:
        connection.access_rule = rule

    source_region.exits.append(connection)
    connection.connect(target_region)
    return connection if reach else None
