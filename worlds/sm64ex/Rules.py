from ..generic.Rules import add_rule
from .Regions import connect_regions, sm64courses


def set_rules(world, player: int, area_connections):
    courseshuffle = list(range(len(sm64courses)))
    if world.AreaRandomizer[player]:
        world.random.shuffle(courseshuffle)
    area_connections.update({index: value for index, value in enumerate(courseshuffle)})

    connect_regions(world, player, "Menu", sm64courses[area_connections[0]])
    connect_regions(world, player, "Menu", sm64courses[area_connections[1]], lambda state: state.has("Power Star", player, 1))
    connect_regions(world, player, "Menu", sm64courses[area_connections[2]], lambda state: state.has("Power Star", player, 3))
    connect_regions(world, player, "Menu", sm64courses[area_connections[3]], lambda state: state.has("Power Star", player, 3))
    connect_regions(world, player, "Menu", "Bowser in the Dark World", lambda state: state.has("Power Star", player, 8))
    connect_regions(world, player, "Menu", sm64courses[area_connections[4]], lambda state: state.has("Power Star", player, 12))

    connect_regions(world, player, "Menu", "Basement", lambda state: state.has("Basement Key", player) or state.has("Progressive Key", player, 1))

    connect_regions(world, player, "Basement", sm64courses[area_connections[5]])
    connect_regions(world, player, "Basement", sm64courses[area_connections[6]])
    connect_regions(world, player, "Basement", sm64courses[area_connections[7]])
    connect_regions(world, player, "Basement", sm64courses[area_connections[8]], lambda state: state.has("Power Star", player, 30))
    connect_regions(world, player, "Basement", "Bowser in the Fire Sea", lambda state: state.has("Power Star", player, 30) and
                                                                                       state.can_reach("DDD: Board Bowser's Sub", 'Location', player))

    connect_regions(world, player, "Menu", "Second Floor", lambda state: state.has("Second Floor Key", player) or state.has("Progressive Key", player, 2))

    connect_regions(world, player, "Second Floor", sm64courses[area_connections[9]])
    connect_regions(world, player, "Second Floor", sm64courses[area_connections[10]])
    connect_regions(world, player, "Second Floor", sm64courses[area_connections[11]])
    connect_regions(world, player, "Second Floor", sm64courses[area_connections[12]])

    connect_regions(world, player, "Second Floor", "Third Floor", lambda state: state.has("Power Star", player, 50))

    connect_regions(world, player, "Third Floor", sm64courses[area_connections[13]])
    connect_regions(world, player, "Third Floor", sm64courses[area_connections[14]])

    #Special Rules for some Locations
    add_rule(world.get_location("Tower of the Wing Cap Switch", player), lambda state: state.has("Power Star", player, 10))
    add_rule(world.get_location("Cavern of the Metal Cap Switch", player), lambda state: state.can_reach("Hazy Maze Cave", 'Region', player))
    add_rule(world.get_location("Vanish Cap Under the Moat Switch", player), lambda state: state.can_reach("Basement", 'Region', player))

    add_rule(world.get_location("BoB: Mario Wings to the Sky", player), lambda state: state.has("Cannon Unlock BoB", player))
    add_rule(world.get_location("BBH: Eye to Eye in the Secret Room", player), lambda state: state.has("Vanish Cap", player))
    add_rule(world.get_location("DDD: Collect the Caps...", player), lambda state: state.has("Vanish Cap", player))
    add_rule(world.get_location("DDD: Pole-Jumping for Red Coins", player), lambda state: state.can_reach("Bowser in the Fire Sea", 'Region', player))
    add_rule(world.get_location("SL: Into the Igloo", player), lambda state: state.has("Vanish Cap", player))
    add_rule(world.get_location("WDW: Quick Race Through Downtown!", player), lambda state: state.has("Vanish Cap", player))
    add_rule(world.get_location("RR: Somewhere Over the Rainbow", player), lambda state: state.has("Cannon Unlock RR", player))

    if world.AreaRandomizer[player]:
        # If area rando is on, it may not be possible to modify WDW's starting water level,
        # which would make it impossible to reach downtown area without the cannon.
        add_rule(world.get_location("WDW: Quick Race Through Downtown!", player), lambda state: state.has("Cannon Unlock WDW", player))
        add_rule(world.get_location("WDW: Go to Town for Red Coins", player), lambda state: state.has("Cannon Unlock WDW", player))

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
        add_rule(world.get_location("WDW: Quick Race Through Downtown!", player), lambda state: state.has("Cannon Unlock WDW", player))
        add_rule(world.get_location("WDW: Go to Town for Red Coins", player), lambda state: state.has("Cannon Unlock WDW", player))
    if world.StrictCapRequirements[player] and world.StrictCannonRequirements[player]:
        # Ability to reach the floating island. Need some of those coins to get 100 coin star as well.
        add_rule(world.get_location("BoB: Find the 8 Red Coins", player), lambda state: state.has("Cannon Unlock BoB", player) or state.has("Wing Cap", player))
        add_rule(world.get_location("BoB: Shoot to the Island in the Sky", player), lambda state: state.has("Cannon Unlock BoB", player) or state.has("Wing Cap", player))
        if world.EnableCoinStars[player]:
            add_rule(world.get_location("BoB: 100 Coins", player), lambda state: state.has("Cannon Unlock BoB", player) or state.has("Wing Cap", player))

    #Rules for Secret Stars
    add_rule(world.get_location("Bowser in the Sky Red Coins", player), lambda state: state.can_reach("Third Floor", 'Region',player) and state.has("Power Star", player, world.StarsToFinish[player].value))
    add_rule(world.get_location("The Princess's Secret Slide Block", player), lambda state: state.has("Power Star", player, 1))
    add_rule(world.get_location("The Princess's Secret Slide Fast", player), lambda state: state.has("Power Star", player, 1))
    add_rule(world.get_location("Cavern of the Metal Cap Red Coins", player), lambda state: state.can_reach("Cavern of the Metal Cap Switch", 'Location', player))
    add_rule(world.get_location("Tower of the Wing Cap Red Coins", player), lambda state: state.can_reach("Tower of the Wing Cap Switch", 'Location', player))
    add_rule(world.get_location("Vanish Cap Under the Moat Red Coins", player), lambda state: state.can_reach("Vanish Cap Under the Moat Switch", 'Location', player))
    add_rule(world.get_location("Wing Mario Over the Rainbow", player), lambda state: state.can_reach("Third Floor", 'Region', player) and state.has("Wing Cap", player))
    add_rule(world.get_location("The Secret Aquarium", player), lambda state: state.has("Power Star", player, 3))
    add_rule(world.get_location("Toad (Basement)", player), lambda state: state.can_reach("Basement", 'Region', player) and state.has("Power Star", player, 12))
    add_rule(world.get_location("Toad (Second Floor)", player), lambda state: state.can_reach("Second Floor", 'Region', player) and state.has("Power Star", player, 25))
    add_rule(world.get_location("Toad (Third Floor)", player), lambda state: state.can_reach("Third Floor", 'Region', player) and state.has("Power Star", player, 35))
    add_rule(world.get_location("MIPS 1", player), lambda state: state.can_reach("Basement", 'Region', player) and state.has("Power Star", player, 15))
    add_rule(world.get_location("MIPS 2", player), lambda state: state.can_reach("Basement", 'Region', player) and state.has("Power Star", player, 50))

    world.completion_condition[player] = lambda state: state.can_reach("Third Floor", 'Region', player) and state.has("Power Star", player, world.StarsToFinish[player].value)
