from ..generic.Rules import add_rule
from .Regions import connect_regions, sm64courses, sm64paintings, sm64secrets, sm64entrances

def fix_reg(entrance_ids, reg, invalidspot, swaplist, world):
    if entrance_ids.index(reg) == invalidspot: # Unlucky :C
            swaplist.remove(invalidspot)
            rand = world.random.choice(swaplist)
            entrance_ids[invalidspot], entrance_ids[rand] = entrance_ids[rand], entrance_ids[invalidspot]
            swaplist.append(invalidspot)
            swaplist.remove(rand)

def set_rules(world, player: int, area_connections):
    destination_regions = list(range(13)) + [12,13,14] + list(range(15,15+len(sm64secrets))) # Two instances of Destination Course THI. Past normal course idx are secret regions
    secret_entrance_ids = list(range(len(sm64paintings), len(sm64paintings) + len(sm64secrets)))
    course_entrance_ids = list(range(len(sm64paintings)))
    if world.AreaRandomizer[player].value >= 1:  # Some randomization is happening, randomize Courses
        world.random.shuffle(course_entrance_ids)
    if world.AreaRandomizer[player].value == 2:  # Randomize Secrets as well
        world.random.shuffle(secret_entrance_ids)
    entrance_ids = course_entrance_ids + secret_entrance_ids
    if world.AreaRandomizer[player].value == 3:  # Randomize Courses and Secrets in one pool
        world.random.shuffle(entrance_ids)
        # Guarantee first entrance is a course
        swaplist = list(range(len(entrance_ids)))
        if entrance_ids.index(0) > 15: # Unlucky :C
            rand = world.random.randint(0,15)
            entrance_ids[entrance_ids.index(0)], entrance_ids[rand] = entrance_ids[rand], entrance_ids[entrance_ids.index(0)]
            swaplist.remove(entrance_ids.index(0))
        # Guarantee COTMC is not mapped to HMC, cuz thats impossible
        fix_reg(entrance_ids, 20, 5, swaplist, world)
        # Guarantee BITFS is not mapped to DDD
        fix_reg(entrance_ids, 22, 8, swaplist, world)
        if entrance_ids.index(22) == 5: # If BITFS is mapped to HMC...
            fix_reg(entrance_ids, 20, 8, swaplist, world) # ... then dont allow COTMC to be mapped to DDD
    temp_assign = dict(zip(entrance_ids,destination_regions)) # Used for Rules only

    # Destination Format: LVL | AREA with LVL = LEVEL_x, AREA = Area as used in sm64 code
    area_connections.update({sm64entrances[entrance]: destination for entrance, destination in zip(entrance_ids,sm64entrances)})
    
    connect_regions(world, player, "Menu", sm64courses[temp_assign[0]]) # BOB
    connect_regions(world, player, "Menu", sm64courses[temp_assign[1]], lambda state: state.has("Power Star", player, 1)) # WF
    connect_regions(world, player, "Menu", sm64courses[temp_assign[2]], lambda state: state.has("Power Star", player, 3)) # JRB
    connect_regions(world, player, "Menu", sm64courses[temp_assign[3]], lambda state: state.has("Power Star", player, 3)) # CCM
    connect_regions(world, player, "Menu", sm64courses[temp_assign[4]], lambda state: state.has("Power Star", player, 12)) # BBH
    connect_regions(world, player, "Menu", sm64courses[temp_assign[16]], lambda state: state.has("Power Star", player, 1)) # PSS
    connect_regions(world, player, "Menu", sm64courses[temp_assign[17]], lambda state: state.has("Power Star", player, 3)) # SA
    connect_regions(world, player, "Menu", sm64courses[temp_assign[19]], lambda state: state.has("Power Star", player, 10)) # TOTWC
    connect_regions(world, player, "Menu", sm64courses[temp_assign[18]], lambda state: state.has("Power Star", player, world.FirstBowserStarDoorCost[player].value)) # BITDW

    connect_regions(world, player, "Menu", "Basement", lambda state: state.has("Basement Key", player) or state.has("Progressive Key", player, 1))

    connect_regions(world, player, "Basement", sm64courses[temp_assign[5]]) # HMC
    connect_regions(world, player, "Basement", sm64courses[temp_assign[6]]) # LLL
    connect_regions(world, player, "Basement", sm64courses[temp_assign[7]]) # SSL
    connect_regions(world, player, "Basement", sm64courses[temp_assign[8]], lambda state: state.has("Power Star", player, world.BasementStarDoorCost[player].value)) # DDD
    connect_regions(world, player, "Hazy Maze Cave", sm64courses[temp_assign[20]]) # COTMC
    connect_regions(world, player, "Basement", sm64courses[temp_assign[21]]) # VCUTM
    connect_regions(world, player, "Basement", sm64courses[temp_assign[22]], lambda state: state.has("Power Star", player, world.BasementStarDoorCost[player].value) and
                                                                                       state.can_reach("DDD: Board Bowser's Sub", 'Location', player)) # BITFS

    connect_regions(world, player, "Menu", "Second Floor", lambda state: state.has("Second Floor Key", player) or state.has("Progressive Key", player, 2))

    connect_regions(world, player, "Second Floor", sm64courses[temp_assign[9]]) # SL
    connect_regions(world, player, "Second Floor", sm64courses[temp_assign[10]]) # WDW
    connect_regions(world, player, "Second Floor", sm64courses[temp_assign[11]]) # TTM
    connect_regions(world, player, "Second Floor", sm64courses[temp_assign[12]]) # THI Tiny
    connect_regions(world, player, "Second Floor", sm64courses[temp_assign[13]]) # THI Huge

    connect_regions(world, player, "Second Floor", "Third Floor", lambda state: state.has("Power Star", player, world.SecondFloorStarDoorCost[player].value))

    connect_regions(world, player, "Third Floor", sm64courses[temp_assign[14]]) # TTC
    connect_regions(world, player, "Third Floor", sm64courses[temp_assign[15]]) # RR
    connect_regions(world, player, "Third Floor", sm64courses[temp_assign[23]]) # WMOTR
    connect_regions(world, player, "Third Floor", "Bowser in the Sky", lambda state: state.has("Power Star", player, world.StarsToFinish[player].value)) # BITS

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

    world.completion_condition[player] = lambda state: state.can_reach("Bowser in the Sky", 'Region', player)
