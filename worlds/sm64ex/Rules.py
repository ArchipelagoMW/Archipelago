import typing
from ..generic.Rules import add_rule
from .Regions import connect_regions

def set_rules(world,player):
    connect_regions(world, player, "Menu", "Bob-omb Battlefield", lambda state: True)
    connect_regions(world, player, "Menu", "Whomp's Fortress", lambda state: state.has("Star", player, 1))
    connect_regions(world, player, "Menu", "Jolly Roger Bay", lambda state: state.has("Star", player, 3))
    connect_regions(world, player, "Menu", "Cool, Cool Mountain", lambda state: state.has("Star", player, 3))
    connect_regions(world, player, "Menu", "Big Boo's Haunt", lambda state: state.has("Star", player, 12))

    connect_regions(world, player, "Menu", "Cellar", lambda state: state.has("Cellar Key", player))
    connect_regions(world, player, "Cellar", "Menu", lambda state: True)

    connect_regions(world, player, "Cellar", "Hazy Maze Cave", lambda state: True)
    connect_regions(world, player, "Cellar", "Lethal Lava Land", lambda state: True)
    connect_regions(world, player, "Cellar", "Shifting Sand Land", lambda state: True)
    connect_regions(world, player, "Cellar", "Dire, Dire Docks", lambda state: state.has("Star", player, 30))

    connect_regions(world, player, "Menu", "Second Floor", lambda state: state.has("Second Floor Key", player))
    connect_regions(world, player, "Second Floor", "Menu", lambda state: True)

    connect_regions(world, player, "Second Floor", "Snowman's Land", lambda state: True)
    connect_regions(world, player, "Second Floor", "Wet-Dry World", lambda state: True)
    connect_regions(world, player, "Second Floor", "Tall, Tall Mountain", lambda state: True)
    connect_regions(world, player, "Second Floor", "Tiny-Huge Island", lambda state: True)

    connect_regions(world, player, "Second Floor", "Third Floor", lambda state: state.has("Star", player, 50))
    connect_regions(world, player, "Third Floor", "Second Floor", lambda state: True)

    connect_regions(world, player, "Third Floor", "Tick Tock Clock", lambda state: True)
    connect_regions(world, player, "Third Floor", "Rainbow Ride", lambda state: True)

    connect_regions(world, player, "Bob-omb Battlefield", "Menu", lambda state: True)
    connect_regions(world, player, "Whomp's Fortress", "Menu", lambda state: True)
    connect_regions(world, player, "Jolly Roger Bay", "Menu", lambda state: True)
    connect_regions(world, player, "Cool, Cool Mountain", "Menu", lambda state: True)
    connect_regions(world, player, "Big Boo's Haunt", "Menu", lambda state: True)
    connect_regions(world, player, "Hazy Maze Cave", "Cellar", lambda state: True)
    connect_regions(world, player, "Lethal Lava Land", "Cellar", lambda state: True)
    connect_regions(world, player, "Shifting Sand Land", "Cellar", lambda state: True)
    connect_regions(world, player, "Dire, Dire Docks", "Cellar", lambda state: True)
    connect_regions(world, player, "Snowman's Land", "Second Floor", lambda state: True)
    connect_regions(world, player, "Wet-Dry World", "Second Floor", lambda state: True)
    connect_regions(world, player, "Tall, Tall Mountain", "Second Floor", lambda state: True)
    connect_regions(world, player, "Tiny-Huge Island", "Second Floor", lambda state: True)
    connect_regions(world, player, "Tick Tock Clock", "Second Floor", lambda state: True)
    connect_regions(world, player, "Rainbow Ride", "Second Floor", lambda state: True)

    #Special Rules for some Locations
    add_rule(world.get_location("Eye to Eye in the Secret Room", player), lambda state: state.can_reach("Vanish Cap Under the Moat Red Coins", 'Location', player))
    add_rule(world.get_location("Collect the Caps...", player), lambda state: state.can_reach("Cavern of the Metal Cap Red Coins", 'Location', player) and
                                                                              state.can_reach("Vanish Cap Under the Moat Red Coins", 'Location', player))
    add_rule(world.get_location("Into the Igloo", player), lambda state: state.can_reach("Vanish Cap Under the Moat Red Coins", 'Location', player))
    add_rule(world.get_location("Quick Race Through Downtown!", player), lambda state: state.can_reach("Vanish Cap Under the Moat Red Coins", 'Location', player))
    if (world.StrictCapRequirements[player].value):
        add_rule(world.get_location("Mario Wings to the Sky", player), lambda state: state.can_reach("Tower of the Wing Cap Red Coins", 'Location', player))
        add_rule(world.get_location("Metal-Head Mario Can Move!", player), lambda state: state.can_reach("Cavern of the Metal Cap Red Coins", 'Location', player))
        add_rule(world.get_location("JRB: Through the Jet Stream", player), lambda state: state.can_reach("Cavern of the Metal Cap Red Coins", 'Location', player))
        add_rule(world.get_location("Free Flying for 8 Red Coins", player), lambda state: state.can_reach("Tower of the Wing Cap Red Coins", 'Location', player))
        add_rule(world.get_location("DDD: Through the Jet Stream", player), lambda state: state.can_reach("Cavern of the Metal Cap Red Coins", 'Location', player))

    #Rules for Secret Stars
    add_rule(world.get_location("Bowser in the Dark World Red Coins", player), lambda state: state.has("Star", player, 8))
    add_rule(world.get_location("Bowser in the Fire Sea Red Coins", player), lambda state: state.can_reach("Cellar",'Region',player) and state.has("Star", player, 30))
    add_rule(world.get_location("Bowser in the Sky Red Coins", player), lambda state: state.can_reach("Second Floor",'Region',player) and state.has("Star", player, 70))
    add_rule(world.get_location("The Princess's Secret Slide Box", player), lambda state: state.has("Star", player, 1))
    add_rule(world.get_location("The Princess's Secret Slide Fast", player), lambda state: state.has("Star", player, 1))
    add_rule(world.get_location("Cavern of the Metal Cap Red Coins", player), lambda state: state.can_reach("Cellar", 'Region', player))
    add_rule(world.get_location("Tower of the Wing Cap Red Coins", player), lambda state: state.has("Star", player, 10))
    add_rule(world.get_location("Vanish Cap Under the Moat Red Coins", player), lambda state: state.can_reach("Cellar", 'Region', player))
    add_rule(world.get_location("Wing Mario Over the Rainbow Red Coins", player), lambda state: state.can_reach("Third Floor", 'Region', player) and state.can_reach("Tower of the Wing Cap Red Coins", 'Location', player))
    add_rule(world.get_location("The Secret Aquarium", player), lambda state: state.can_reach("Jolly Roger Bay", 'Region', player))
    add_rule(world.get_location("Toad (Cellar)", player), lambda state: state.can_reach("Cellar",'Region',player))
    add_rule(world.get_location("Toad (Second Floor)", player), lambda state: state.can_reach("Second Floor",'Region',player))
    add_rule(world.get_location("Toad (Third Floor)", player), lambda state: state.can_reach("Third Floor",'Region',player))
    add_rule(world.get_location("MIPS 1", player), lambda state: state.can_reach("Cellar",'Region',player) and state.has("Star", player, 15))
    add_rule(world.get_location("MIPS 2", player), lambda state: state.can_reach("Cellar",'Region',player) and state.has("Star", player, 50))

    #Rules for Keys
    add_rule(world.get_location("Cellar Key", player), lambda state: state.has("Star", player, 8))
    add_rule(world.get_location("Second Floor Key", player), lambda state: state.can_reach("Cellar", 'Region', player) and state.has("Star", player, 30))

    world.completion_condition[player] = lambda state: state.can_reach(world.get_region("Second Floor", player),'Region',player) and state.has("Star", player, 70)