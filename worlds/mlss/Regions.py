import typing

from BaseClasses import MultiWorld, Region, Entrance, LocationProgressType
from worlds.generic.Rules import add_rule, set_rule
from .Locations import MLSSLocation, mainArea, chucklehuck, castleTown, startingFlag, chuckolatorFlag, piranhaFlag, \
    kidnappedFlag, beanstarFlag, birdoFlag, surfable, hooniversity, gwarharEntrance, gwarharMain, \
    fungitown, fungitownBeanstar, fungitownBirdo, teeheeValley, winkle, sewers, airport, \
    bowsers, bowsersMini, jokesEntrance, jokesMain, theater, booStatue, oasis, postJokes, baseUltraRocks, event, coins
from . import StateLogic
from .Names.LocationName import LocationName


def create_regions(world: MultiWorld, player: int, excluded: typing.List[str]):
    menu_region = Region("Menu", player, world)
    world.regions.append(menu_region)

    main_region = create_region(world, player, "Main Area", mainArea, excluded)
    world.regions.append(main_region)

    chucklehuck_region = create_region(world, player, "Chucklehuck Woods", chucklehuck, excluded)
    world.regions.append(chucklehuck_region)

    castleTown_region = create_region(world, player, "Beanbean Castle Town", castleTown, excluded)
    world.regions.append(castleTown_region)

    startingFlag_region = create_region(world, player, "Shop Starting Flag", startingFlag, excluded)
    world.regions.append(startingFlag_region)

    chuckolatorFlag_region = create_region(world, player, "Shop Chuckolator Flag", chuckolatorFlag, excluded)
    world.regions.append(chuckolatorFlag_region)

    piranhaFlag_region = create_region(world, player, "Shop Piranha Flag", piranhaFlag, excluded)
    world.regions.append(piranhaFlag_region)

    kidnappedFlag_region = create_region(world, player, "Shop Peach Kidnapped Flag", kidnappedFlag, excluded)
    world.regions.append(kidnappedFlag_region)

    beanstarFlag_region = create_region(world, player, "Shop Beanstar Complete Flag", beanstarFlag, excluded)
    world.regions.append(beanstarFlag_region)

    birdoFlag_region = create_region(world, player, "Shop Birdo Flag", birdoFlag, excluded)
    world.regions.append(birdoFlag_region)

    surfable_region = create_region(world, player, "Surfable", surfable, excluded)
    world.regions.append(surfable_region)

    hooniversity_region = create_region(world, player, "Hooniversity", hooniversity, excluded)
    world.regions.append(hooniversity_region)

    gwarharEntrance_region = create_region(world, player, "GwarharEntrance", gwarharEntrance, excluded)
    world.regions.append(gwarharEntrance_region)

    gwarharMain_region = create_region(world, player, "GwarharMain", gwarharMain, excluded)
    world.regions.append(gwarharMain_region)

    teehee_valley_region = create_region(world, player, "TeeheeValley", teeheeValley, excluded)
    world.regions.append(teehee_valley_region)

    winkle_region = create_region(world, player, "Winkle", winkle, excluded)
    world.regions.append(winkle_region)

    sewers_region = create_region(world, player, "Sewers", sewers, excluded)
    world.regions.append(sewers_region)

    airport_region = create_region(world, player, "Airport", airport, excluded)
    world.regions.append(airport_region)

    jokesEntrance_region = create_region(world, player, "JokesEntrance", jokesEntrance, excluded)
    world.regions.append(jokesEntrance_region)

    jokesMain_region = create_region(world, player, "JokesMain", jokesMain, excluded)
    world.regions.append(jokesMain_region)

    postJokes_region = create_region(world, player, "PostJokes", postJokes, excluded)
    world.regions.append(postJokes_region)

    theater_region = create_region(world, player, "Theater", theater, excluded)
    world.regions.append(theater_region)

    fungitown_region = create_region(world, player, "Fungitown", fungitown, excluded)
    world.regions.append(fungitown_region)

    fungitownBeanstar_region = create_region(world, player, "FungitownBeanstar", fungitownBeanstar, excluded)
    world.regions.append(fungitownBeanstar_region)

    fungitownBirdo_region = create_region(world, player, "FungitownBirdo", fungitownBirdo, excluded)
    world.regions.append(fungitownBirdo_region)

    booStatue_region = create_region(world, player, "BooStatue", booStatue, excluded)
    world.regions.append(booStatue_region)

    oasis_region = create_region(world, player, "Oasis", oasis, excluded)
    world.regions.append(oasis_region)

    event_region = create_region(world, player, "Event", event, excluded)
    world.regions.append(event_region)

    if world.coins[player]:
        print("CREATING REGION")
        coins_region = create_region(world, player, "Coins", coins, excluded)
        world.regions.append(coins_region)

    if not world.castle_skip[player]:
        bowsers_region = create_region(world, player, "Bowser's Castle", bowsers, excluded)
        world.regions.append(bowsers_region)
        bowsersMini_region = create_region(world, player, "Bowser's Castle Mini", bowsersMini, excluded)
        world.regions.append(bowsersMini_region)

    baseUltraRocks_region = create_region(world, player, "BaseUltraRocks", baseUltraRocks, excluded)
    world.regions.append(baseUltraRocks_region)


def connect_regions(world: MultiWorld, player: int):
    names: typing.Dict[str, int] = {}

    connect(world, player, names, "Menu", "Main Area")
    connect(world, player, names, "Main Area", "Event")
    if world.coins[player]:
        connect(world, player, names, "Main Area", "Coins")
    connect(world, player, names, "Main Area", "BaseUltraRocks", lambda state: StateLogic.ultra(state, player))
    connect(world, player, names, "Main Area", "Chucklehuck Woods", lambda state: StateLogic.brooch(state, player))
    connect(world, player, names, "Main Area", "BooStatue", lambda state: StateLogic.canCrash(state, player))
    connect(world, player, names, "Main Area", "Hooniversity", lambda state: StateLogic.canDig(state, player) and StateLogic.canMini(state, player))
    connect(world, player, names, "Hooniversity", "Oasis")
    connect(world, player, names, "Main Area", "TeeheeValley", lambda state: StateLogic.super(state, player) or StateLogic.canDash(state, player))
    connect(world, player, names, "TeeheeValley", "GwarharEntrance", lambda state: StateLogic.membership(state, player) and StateLogic.fire(state, player))
    connect(world, player, names, "TeeheeValley", "Oasis", lambda state: StateLogic.membership(state, player) and StateLogic.fire(state, player))
    connect(world, player, names, "TeeheeValley", "Fungitown", lambda state: StateLogic.thunder(state, player) and StateLogic.castleTown(state, player) and StateLogic.rose(state, player))
    connect(world, player, names, "Fungitown", "FungitownBeanstar", lambda state: StateLogic.pieces(state, player) or state.can_reach("FungitownBirdo", "Region", player))
    connect(world, player, names, "Fungitown", "FungitownBirdo", lambda state: StateLogic.postJokes(state, player))
    connect(world, player, names, "Main Area", "Shop Starting Flag", lambda state: StateLogic.brooch(state, player) or StateLogic.rose(state, player))
    connect(world, player, names, "Shop Starting Flag", "Shop Chuckolator Flag", lambda state: (StateLogic.brooch(state, player) and StateLogic.fruits(state, player)) or state.can_reach("Shop Piranha Flag", "Region", player))
    connect(world, player, names, "Shop Starting Flag", "Shop Piranha Flag", lambda state: StateLogic.thunder(state, player) or state.can_reach("Shop Peach Kidnapped Flag", "Region", player))
    connect(world, player, names, "Shop Starting Flag", "Shop Peach Kidnapped Flag", lambda state: (StateLogic.thunder(state, player) and StateLogic.fungitown(state, player)) or state.can_reach("Shop Beanstar Complete Flag", "Region", player))
    connect(world, player, names, "Shop Starting Flag", "Shop Beanstar Complete Flag", lambda state: (StateLogic.castleTown(state, player) and StateLogic.pieces(state, player) and StateLogic.rose(state, player)) or state.can_reach("Shop Birdo Flag", "Region", player))
    connect(world, player, names, "Shop Starting Flag", "Shop Birdo Flag", lambda state: StateLogic.postJokes(state, player))
    connect(world, player, names, "Main Area", "Sewers", lambda state: StateLogic.rose(state, player))
    connect(world, player, names, "Main Area", "Airport", lambda state: StateLogic.thunder(state, player))
    connect(world, player, names, "Main Area", "Theater", lambda state: StateLogic.canDash(state, player))
    connect(world, player, names, "Main Area", "Surfable", lambda state: StateLogic.surfable(state, player))
    connect(world, player, names, "Surfable", "GwarharEntrance")
    connect(world, player, names, "Surfable", "Oasis")
    connect(world, player, names, "Surfable", "JokesEntrance", lambda state: StateLogic.fire(state, player))
    connect(world, player, names, "JokesMain", "PostJokes", lambda state: StateLogic.postJokes(state, player))
    if not world.castle_skip[player]:
        connect(world, player, names, "PostJokes", "Bowser's Castle")
        connect(world, player, names, "Bowser's Castle", "Bowser's Castle Mini", lambda state: StateLogic.canMini(state, player) and StateLogic.thunder(state, player))
    connect(world, player, names, "Chucklehuck Woods", "Winkle", lambda state: StateLogic.canDash(state, player))
    connect(world, player, names, "Chucklehuck Woods", "Beanbean Castle Town", lambda state: StateLogic.fruits(state, player))
    if world.difficult_logic[player]:
        connect(world, player, names, "GwarharEntrance", "GwarharMain", lambda state: StateLogic.canDash(state, player))
        connect(world, player, names, "JokesEntrance", "JokesMain", lambda state: StateLogic.canDig(state, player))
    else:
        connect(world, player, names, "GwarharEntrance", "GwarharMain", lambda state: StateLogic.canDash(state, player) and StateLogic.canCrash(state, player))
        connect(world, player, names, "JokesEntrance", "JokesMain", lambda state: StateLogic.canCrash(state, player) and StateLogic.canDig(state, player))


def create_region(world, player, name, locations, excluded):
    ret = Region(name, player, world)
    for location in locations:
        loc = MLSSLocation(player, location.name, location.id, ret)
        if location.name in excluded:
            continue
        ret.locations.append(loc)
    return ret


def connect(world: MultiWorld, player: int, used_names: typing.Dict[str, int], source: str, target: str,
            rule: typing.Optional[typing.Callable] = None):
    source_region = world.get_region(source, player)
    target_region = world.get_region(target, player)

    if target not in used_names:
        used_names[target] = 1
        name = target
    else:
        used_names[target] += 1
        name = target + (' ' * used_names[target])

    connection = Entrance(player, name, source_region)

    if rule:
        connection.access_rule = rule

    source_region.exits.append(connection)
    connection.connect(target_region)
