import typing
from ..generic.Rules import add_rule
from .Regions import connect_regions

area_connections = {}

def set_rules(world,player):
    sm64courses = ["Bob-omb Battlefield", "Whomp's Fortress", "Jolly Roger Bay", "Cool, Cool Mountain", "Big Boo's Haunt",
                   "Hazy Maze Cave", "Lethal Lava Land", "Shifting Sand Land", "Dire, Dire Docks", "Snowman's Land", "Wet-Dry World",
                   "Tall, Tall Mountain", "Tiny-Huge Island", "Tick Tock Clock", "Rainbow Ride"]
    sm64courses_o = sm64courses.copy()
    if (world.AreaRandomizer[player].value):
        world.random.shuffle(sm64courses)
    connect_regions(world, player, "Menu", sm64courses[0], lambda state: True)
    connect_regions(world, player, "Menu", sm64courses[1], lambda state: state.has("Power Star", player, 1))
    connect_regions(world, player, "Menu", sm64courses[2], lambda state: state.has("Power Star", player, 3))
    connect_regions(world, player, "Menu", sm64courses[3], lambda state: state.has("Power Star", player, 3))
    connect_regions(world, player, "Menu", sm64courses[4], lambda state: state.has("Power Star", player, 12))

    connect_regions(world, player, "Menu", "Basement", lambda state: state.has("Basement Key", player))
    connect_regions(world, player, "Basement", "Menu", lambda state: True)

    connect_regions(world, player, "Basement", sm64courses[5], lambda state: True)
    connect_regions(world, player, "Basement", sm64courses[6], lambda state: True)
    connect_regions(world, player, "Basement", sm64courses[7], lambda state: True)
    connect_regions(world, player, "Basement", sm64courses[8], lambda state: state.has("Power Star", player, 30))

    connect_regions(world, player, "Menu", "Second Floor", lambda state: state.has("Second Floor Key", player))
    connect_regions(world, player, "Second Floor", "Menu", lambda state: True)

    connect_regions(world, player, "Second Floor", sm64courses[9], lambda state: True)
    connect_regions(world, player, "Second Floor", sm64courses[10], lambda state: True)
    connect_regions(world, player, "Second Floor", sm64courses[11], lambda state: True)
    connect_regions(world, player, "Second Floor", sm64courses[12], lambda state: True)

    connect_regions(world, player, "Second Floor", "Third Floor", lambda state: state.has("Power Star", player, 50))
    connect_regions(world, player, "Third Floor", "Second Floor", lambda state: True)

    connect_regions(world, player, "Third Floor", sm64courses[13], lambda state: True)
    connect_regions(world, player, "Third Floor", sm64courses[14], lambda state: True)

    for i in range(0, len(sm64courses)):
        connect_regions(world, player, sm64courses[i], "Menu", lambda state: True)
        area_connections[i] = sm64courses.index(sm64courses_o[i])

    #Special Rules for some Locations
    add_rule(world.get_location("Tower of the Wing Cap Switch", player), lambda state: state.has("Power Star", player, 10))
    add_rule(world.get_location("Cavern of the Metal Cap Switch", player), lambda state: state.can_reach("Hazy Maze Cave",'Region',player))
    add_rule(world.get_location("Vanish Cap Under the Moat Switch", player), lambda state: state.can_reach("Basement", 'Region', player))

    add_rule(world.get_location("BBH: Eye to Eye in the Secret Room", player), lambda state: state.has("Vanish Cap", player))
    add_rule(world.get_location("DDD: Collect the Caps...", player), lambda state: state.has("Metal Cap", player) and
                                                                              state.has("Vanish Cap", player))
    add_rule(world.get_location("SL: Into the Igloo", player), lambda state: state.has("Vanish Cap", player))
    add_rule(world.get_location("WDW: Quick Race Through Downtown!", player), lambda state: state.has("Vanish Cap", player))
    if (world.StrictCapRequirements[player].value):
        add_rule(world.get_location("BoB: Mario Wings to the Sky", player), lambda state: state.has("Wing Cap", player))
        add_rule(world.get_location("HMC: Metal-Head Mario Can Move!", player), lambda state: state.has("Metal Cap", player))
        add_rule(world.get_location("JRB: Through the Jet Stream", player), lambda state: state.has("Metal Cap", player))
        add_rule(world.get_location("SSL: Free Flying for 8 Red Coins", player), lambda state: state.has("Wing Cap", player))
        add_rule(world.get_location("DDD: Through the Jet Stream", player), lambda state: state.has("Metal Cap", player))
        add_rule(world.get_location("Vanish Cap Under the Moat Red Coins", player), lambda state: state.has("Vanish Cap", player))

    #Rules for Secret Stars
    add_rule(world.get_location("Bowser in the Dark World Red Coins", player), lambda state: state.has("Power Star", player, 8))
    add_rule(world.get_location("Bowser in the Fire Sea Red Coins", player), lambda state: state.can_reach("Basement",'Region',player) and state.has("Power Star", player, 30))
    add_rule(world.get_location("Bowser in the Sky Red Coins", player), lambda state: state.can_reach("Third Floor",'Region',player) and state.has("Power Star", player, world.StarsToFinish[player].value))
    add_rule(world.get_location("The Princess's Secret Slide Block", player), lambda state: state.has("Power Star", player, 1))
    add_rule(world.get_location("The Princess's Secret Slide Fast", player), lambda state: state.has("Power Star", player, 1))
    add_rule(world.get_location("Cavern of the Metal Cap Red Coins", player), lambda state: state.can_reach("Cavern of the Metal Cap Switch", 'Location', player) and state.has("Metal Cap", player))
    add_rule(world.get_location("Tower of the Wing Cap Red Coins", player), lambda state: state.can_reach("Tower of the Wing Cap Switch", 'Location', player))
    add_rule(world.get_location("Vanish Cap Under the Moat Red Coins", player), lambda state: state.can_reach("Vanish Cap Under the Moat Switch", 'Location', player))
    add_rule(world.get_location("Wing Mario Over the Rainbow", player), lambda state: state.can_reach("Third Floor", 'Region', player) and state.has("Wing Cap", player))
    add_rule(world.get_location("The Secret Aquarium", player), lambda state: state.has("Power Star", player, 3))
    add_rule(world.get_location("Toad (Basement)", player), lambda state: state.can_reach("Basement",'Region',player))
    add_rule(world.get_location("Toad (Second Floor)", player), lambda state: state.can_reach("Second Floor",'Region',player))
    add_rule(world.get_location("Toad (Third Floor)", player), lambda state: state.can_reach("Third Floor",'Region',player))
    add_rule(world.get_location("MIPS 1", player), lambda state: state.can_reach("Basement",'Region',player) and state.has("Power Star", player, 15))
    add_rule(world.get_location("MIPS 2", player), lambda state: state.can_reach("Basement",'Region',player) and state.has("Power Star", player, 50))

    #Rules for Keys
    add_rule(world.get_location("Bowser in the Dark World Key", player), lambda state: state.has("Power Star", player, 8))
    add_rule(world.get_location("Bowser in the Fire Sea Key", player), lambda state: state.can_reach("Basement", 'Region', player) and state.has("Power Star", player, 30))

    world.completion_condition[player] = lambda state: state.can_reach("Third Floor",'Region',player) and state.has("Power Star", player, world.StarsToFinish[player].value)
