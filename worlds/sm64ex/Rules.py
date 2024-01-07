from ..generic.Rules import add_rule
from .Regions import connect_regions, SM64Levels, sm64_level_to_paintings, sm64_paintings_to_level, sm64_level_to_secrets, sm64_secrets_to_level, sm64_entrances_to_level, sm64_level_to_entrances

def shuffle_dict_keys(world, obj: dict) -> dict:
    keys = list(obj.keys())
    values = list(obj.values())
    world.random.shuffle(keys)
    return dict(zip(keys,values))

def fix_reg(entrance_map: dict, entrance: SM64Levels, invalid_regions: set,
            swapdict: dict, world):
    if entrance_map[entrance] in invalid_regions: # Unlucky :C
        replacement_regions = [(rand_region, rand_entrance) for rand_region, rand_entrance in swapdict.items()
                               if rand_region not in invalid_regions]
        rand_region, rand_entrance = world.random.choice(replacement_regions)
        old_dest = entrance_map[entrance]
        entrance_map[entrance], entrance_map[rand_entrance] = rand_region, old_dest
        swapdict[rand_region] = entrance
    swapdict.pop(entrance_map[entrance]) # Entrance now fixed to rand_region

def set_rules(world, player: int, area_connections: dict):
    randomized_level_to_paintings = sm64_level_to_paintings.copy()
    randomized_level_to_secrets = sm64_level_to_secrets.copy()
    if world.AreaRandomizer[player].value >= 1:  # Some randomization is happening, randomize Courses
        randomized_level_to_paintings = shuffle_dict_keys(world,sm64_level_to_paintings)
    if world.AreaRandomizer[player].value == 2:  # Randomize Secrets as well
        randomized_level_to_secrets = shuffle_dict_keys(world,sm64_level_to_secrets)
    randomized_entrances = { **randomized_level_to_paintings, **randomized_level_to_secrets }
    if world.AreaRandomizer[player].value == 3:  # Randomize Courses and Secrets in one pool
        randomized_entrances = shuffle_dict_keys(world,randomized_entrances)
        swapdict = { entrance: level for (level,entrance) in randomized_entrances.items() }
        # Guarantee first entrance is a course
        fix_reg(randomized_entrances, SM64Levels.BOB_OMB_BATTLEFIELD, sm64_secrets_to_level.keys(), swapdict, world)
        # Guarantee BITFS is not mapped to DDD
        fix_reg(randomized_entrances, SM64Levels.BOWSER_IN_THE_FIRE_SEA, {"Dire, Dire Docks"}, swapdict, world)
        # Guarantee COTMC is not mapped to HMC, cuz thats impossible. If BitFS -> HMC, also no COTMC -> DDD.
        if randomized_entrances[SM64Levels.BOWSER_IN_THE_FIRE_SEA] == "Hazy Maze Cave":
            fix_reg(randomized_entrances, SM64Levels.CAVERN_OF_THE_METAL_CAP, {"Hazy Maze Cave", "Dire, Dire Docks"}, swapdict, world)
        else:
            fix_reg(randomized_entrances, SM64Levels.CAVERN_OF_THE_METAL_CAP, {"Hazy Maze Cave"}, swapdict, world)

    # Destination Format: LVL | AREA with LVL = LEVEL_x, AREA = Area as used in sm64 code
    # Cast to int to not rely on availability of SM64Levels enum. Will cause crash in MultiServer otherwise
    area_connections.update({int(entrance_lvl): int(sm64_entrances_to_level[destination]) for (entrance_lvl,destination) in randomized_entrances.items()})
    randomized_entrances_s = {sm64_level_to_entrances[entrance_lvl]: destination for (entrance_lvl,destination) in randomized_entrances.items()}
    
    connect_regions(world, player, "Menu", randomized_entrances_s["Bob-omb Battlefield"])
    connect_regions(world, player, "Menu", randomized_entrances_s["Whomp's Fortress"], lambda state: state.has("Power Star", player, 1))
    connect_regions(world, player, "Menu", randomized_entrances_s["Jolly Roger Bay"], lambda state: state.has("Power Star", player, 3))
    connect_regions(world, player, "Menu", randomized_entrances_s["Cool, Cool Mountain"], lambda state: state.has("Power Star", player, 3))
    connect_regions(world, player, "Menu", randomized_entrances_s["Big Boo's Haunt"], lambda state: state.has("Power Star", player, 12))
    connect_regions(world, player, "Menu", randomized_entrances_s["The Princess's Secret Slide"], lambda state: state.has("Power Star", player, 1))
    connect_regions(world, player, "Menu", randomized_entrances_s["The Secret Aquarium"], lambda state: state.has("Power Star", player, 3))
    connect_regions(world, player, "Menu", randomized_entrances_s["Tower of the Wing Cap"], lambda state: state.has("Power Star", player, 10))
    connect_regions(world, player, "Menu", randomized_entrances_s["Bowser in the Dark World"], lambda state: state.has("Power Star", player, world.FirstBowserStarDoorCost[player].value))

    connect_regions(world, player, "Menu", "Basement", lambda state: state.has("Basement Key", player) or state.has("Progressive Key", player, 1))

    connect_regions(world, player, "Basement", randomized_entrances_s["Hazy Maze Cave"])
    connect_regions(world, player, "Basement", randomized_entrances_s["Lethal Lava Land"])
    connect_regions(world, player, "Basement", randomized_entrances_s["Shifting Sand Land"])
    connect_regions(world, player, "Basement", randomized_entrances_s["Dire, Dire Docks"], lambda state: state.has("Power Star", player, world.BasementStarDoorCost[player].value))
    connect_regions(world, player, "Hazy Maze Cave", randomized_entrances_s["Cavern of the Metal Cap"])
    connect_regions(world, player, "Basement", randomized_entrances_s["Vanish Cap under the Moat"])
    connect_regions(world, player, "Basement", randomized_entrances_s["Bowser in the Fire Sea"], lambda state: state.has("Power Star", player, world.BasementStarDoorCost[player].value) and
                                                                                       state.can_reach("DDD: Board Bowser's Sub", 'Location', player))

    connect_regions(world, player, "Menu", "Second Floor", lambda state: state.has("Second Floor Key", player) or state.has("Progressive Key", player, 2))

    connect_regions(world, player, "Second Floor", randomized_entrances_s["Snowman's Land"])
    connect_regions(world, player, "Second Floor", randomized_entrances_s["Wet-Dry World"])
    connect_regions(world, player, "Second Floor", randomized_entrances_s["Tall, Tall Mountain"])
    connect_regions(world, player, "Second Floor", randomized_entrances_s["Tiny-Huge Island (Tiny)"])
    connect_regions(world, player, "Second Floor", randomized_entrances_s["Tiny-Huge Island (Huge)"])
    connect_regions(world, player, "Tiny-Huge Island (Tiny)", "Tiny-Huge Island (Huge)")
    connect_regions(world, player, "Tiny-Huge Island (Huge)", "Tiny-Huge Island (Tiny)")

    connect_regions(world, player, "Second Floor", "Third Floor", lambda state: state.has("Power Star", player, world.SecondFloorStarDoorCost[player].value))

    connect_regions(world, player, "Third Floor", randomized_entrances_s["Tick Tock Clock"])
    connect_regions(world, player, "Third Floor", randomized_entrances_s["Rainbow Ride"])
    connect_regions(world, player, "Third Floor", randomized_entrances_s["Wing Mario over the Rainbow"])
    connect_regions(world, player, "Third Floor", "Bowser in the Sky", lambda state: state.has("Power Star", player, world.StarsToFinish[player].value))

    #Special Rules for some Locations
    add_rule(world.get_location("BoB: Mario Wings to the Sky", player), lambda state: state.has("Cannon Unlock BoB", player))
    add_rule(world.get_location("BBH: Eye to Eye in the Secret Room", player), lambda state: state.has("Vanish Cap", player))
    add_rule(world.get_location("DDD: Collect the Caps...", player), lambda state: state.has("Vanish Cap", player))
    add_rule(world.get_location("DDD: Pole-Jumping for Red Coins", player), lambda state: state.can_reach("Bowser in the Fire Sea", 'Region', player))
    if world.EnableCoinStars[player]:
        add_rule(world.get_location("DDD: 100 Coins", player), lambda state: state.can_reach("Bowser in the Fire Sea", 'Region', player))
    add_rule(world.get_location("SL: Into the Igloo", player), lambda state: state.has("Vanish Cap", player))
    add_rule(world.get_location("WDW: Quick Race Through Downtown!", player), lambda state: state.has("Vanish Cap", player))
    add_rule(world.get_location("RR: Somewhere Over the Rainbow", player), lambda state: state.has("Cannon Unlock RR", player))

    if world.AreaRandomizer[player] or world.StrictCannonRequirements[player]:
        # If area rando is on, it may not be possible to modify WDW's starting water level,
        # which would make it impossible to reach downtown area without the cannon.
        add_rule(world.get_location("WDW: Quick Race Through Downtown!", player), lambda state: state.has("Cannon Unlock WDW", player))
        add_rule(world.get_location("WDW: Go to Town for Red Coins", player), lambda state: state.has("Cannon Unlock WDW", player))
        add_rule(world.get_location("WDW: 1Up Block in Downtown", player), lambda state: state.has("Cannon Unlock WDW", player))

    if world.StrictCapRequirements[player]:
        add_rule(world.get_location("BoB: Mario Wings to the Sky", player), lambda state: state.has("Wing Cap", player))
        add_rule(world.get_location("HMC: Metal-Head Mario Can Move!", player), lambda state: state.has("Metal Cap", player))
        add_rule(world.get_location("JRB: Through the Jet Stream", player), lambda state: state.has("Metal Cap", player))
        add_rule(world.get_location("SSL: Free Flying for 8 Red Coins", player), lambda state: state.has("Wing Cap", player))
        add_rule(world.get_location("DDD: Through the Jet Stream", player), lambda state: state.has("Metal Cap", player))
        add_rule(world.get_location("DDD: Collect the Caps...", player), lambda state: state.has("Metal Cap", player))
        add_rule(world.get_location("Vanish Cap Under the Moat Red Coins", player), lambda state: state.has("Vanish Cap", player))
        add_rule(world.get_location("Cavern of the Metal Cap Red Coins", player), lambda state: state.has("Metal Cap", player))
    if world.StrictCannonRequirements[player]:
        add_rule(world.get_location("WF: Blast Away the Wall", player), lambda state: state.has("Cannon Unlock WF", player))
        add_rule(world.get_location("JRB: Blast to the Stone Pillar", player), lambda state: state.has("Cannon Unlock JRB", player))
        add_rule(world.get_location("CCM: Wall Kicks Will Work", player), lambda state: state.has("Cannon Unlock CCM", player))
        add_rule(world.get_location("TTM: Blast to the Lonely Mushroom", player), lambda state: state.has("Cannon Unlock TTM", player))
    if world.StrictCapRequirements[player] and world.StrictCannonRequirements[player]:
        # Ability to reach the floating island. Need some of those coins to get 100 coin star as well.
        add_rule(world.get_location("BoB: Find the 8 Red Coins", player), lambda state: state.has("Cannon Unlock BoB", player) or state.has("Wing Cap", player))
        add_rule(world.get_location("BoB: Shoot to the Island in the Sky", player), lambda state: state.has("Cannon Unlock BoB", player) or state.has("Wing Cap", player))
        if world.EnableCoinStars[player]:
            add_rule(world.get_location("BoB: 100 Coins", player), lambda state: state.has("Cannon Unlock BoB", player) or state.has("Wing Cap", player))

    #Rules for Secret Stars
    add_rule(world.get_location("Wing Mario Over the Rainbow Red Coins", player), lambda state: state.has("Wing Cap", player))
    add_rule(world.get_location("Wing Mario Over the Rainbow 1Up Block", player), lambda state: state.has("Wing Cap", player))
    add_rule(world.get_location("Toad (Basement)", player), lambda state: state.can_reach("Basement", 'Region', player) and state.has("Power Star", player, 12))
    add_rule(world.get_location("Toad (Second Floor)", player), lambda state: state.can_reach("Second Floor", 'Region', player) and state.has("Power Star", player, 25))
    add_rule(world.get_location("Toad (Third Floor)", player), lambda state: state.can_reach("Third Floor", 'Region', player) and state.has("Power Star", player, 35))

    if world.MIPS1Cost[player].value > world.MIPS2Cost[player].value:
        (world.MIPS2Cost[player].value, world.MIPS1Cost[player].value) = (world.MIPS1Cost[player].value, world.MIPS2Cost[player].value)
    add_rule(world.get_location("MIPS 1", player), lambda state: state.can_reach("Basement", 'Region', player) and state.has("Power Star", player, world.MIPS1Cost[player].value))
    add_rule(world.get_location("MIPS 2", player), lambda state: state.can_reach("Basement", 'Region', player) and state.has("Power Star", player, world.MIPS2Cost[player].value))

    if world.CompletionType[player] == "last_bowser_stage":
        world.completion_condition[player] = lambda state: state.can_reach("Bowser in the Sky", 'Region', player)
    elif world.CompletionType[player] == "all_bowser_stages":
        world.completion_condition[player] = lambda state: state.can_reach("Bowser in the Dark World", 'Region', player) and \
                                                           state.can_reach("Bowser in the Fire Sea", 'Region', player) and \
                                                           state.can_reach("Bowser in the Sky", 'Region', player)
