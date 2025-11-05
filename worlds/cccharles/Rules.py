from BaseClasses import MultiWorld
from ..generic.Rules import set_rule
from .Options import CCCharlesOptions

# Go mode: Green Egg + Blue Egg + Red Egg + Temple Key + Bug Spray (+ Remote Explosive x8 but the base game ignores it)

def set_rules(world: MultiWorld, options: CCCharlesOptions, player: int) -> None:
    # Tony Tiddle
    set_rule(world.get_entrance("Barn Door", player),
        lambda state: state.has("Barn Key", player))

    # Candice
    set_rule(world.get_entrance("Tutorial House Door", player),
        lambda state: state.has("Candice's Key", player))

    # Lizbeth Murkwater
    set_rule(world.get_location("Swamp Lizbeth Murkwater Mission End", player),
        lambda state: state.has("Dead Fish", player))

    # Daryl
    set_rule(world.get_location("Junkyard Area Chest Ancient Tablet", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("Junkyard Area Daryl Mission End", player),
        lambda state: state.has("Ancient Tablet", player))

    # South House
    set_rule(world.get_location("South House Chest Scraps 1", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("South House Chest Scraps 2", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("South House Chest Scraps 3", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("South House Chest Scraps 4", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("South House Chest Scraps 5", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("South House Chest Scraps 6", player),
        lambda state: state.has("Lockpicks", player))

    # South Mine
    set_rule(world.get_entrance("South Mine Gate", player),
        lambda state: state.has("South Mine Key", player))

    set_rule(world.get_location("South Mine Inside Green Paint Can", player),
        lambda state: state.has("Lockpicks", player))

    # Theodore
    set_rule(world.get_location("Middle Station Theodore Mission End", player),
        lambda state: state.has("Blue Box", player))

    # Watchtower
    set_rule(world.get_location("Watchtower Pink Paint Can", player),
        lambda state: state.has("Lockpicks", player))

    # Sasha
    set_rule(world.get_location("Haunted House Sasha Mission End", player),
        lambda state: state.has("Page Drawing", player, 8))

    # Santiago
    set_rule(world.get_location("Port Santiago Mission End", player),
        lambda state: state.has("Journal", player))

    # Trench House
    set_rule(world.get_location("Trench House Chest Scraps 1", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("Trench House Chest Scraps 2", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("Trench House Chest Scraps 3", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("Trench House Chest Scraps 4", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("Trench House Chest Scraps 5", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("Trench House Chest Scraps 6", player),
        lambda state: state.has("Lockpicks", player))

    # East House
    set_rule(world.get_location("East House Chest Scraps 1", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("East House Chest Scraps 2", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("East House Chest Scraps 3", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("East House Chest Scraps 4", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("East House Chest Scraps 5", player),
        lambda state: state.has("Lockpicks", player))

    # Rocket Testing Bunker
    set_rule(world.get_entrance("Stuck Bunker Door", player),
        lambda state: state.has("Timed Dynamite", player))

    # John Smith
    set_rule(world.get_location("Workshop John Smith Mission End", player),
        lambda state: state.has("Box of Rockets", player))

    # Claire
    set_rule(world.get_location("Lighthouse Claire Mission End", player),
        lambda state: state.has("Breaker", player, 4))

    # North Mine
    set_rule(world.get_entrance("North Mine Gate", player),
        lambda state: state.has("North Mine Key", player))

    set_rule(world.get_location("North Mine Inside Blue Paint Can", player),
        lambda state: state.has("Lockpicks", player))

    # Paul
    set_rule(world.get_location("Museum Paul Mission End", player),
        lambda state: state.has("Remote Explosive x8", player))
        # lambda state: state.has("Remote Explosive", player, 8)) # TODO: Add an option to split remote explosives

    # West Beach
    set_rule(world.get_location("West Beach Chest Scraps 1", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("West Beach Chest Scraps 2", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("West Beach Chest Scraps 3", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("West Beach Chest Scraps 4", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("West Beach Chest Scraps 5", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("West Beach Chest Scraps 6", player),
        lambda state: state.has("Lockpicks", player))

    # Caravan
    set_rule(world.get_location("Caravan Chest Scraps 1", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("Caravan Chest Scraps 2", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("Caravan Chest Scraps 3", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("Caravan Chest Scraps 4", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("Caravan Chest Scraps 5", player),
        lambda state: state.has("Lockpicks", player))

    # Ronny
    set_rule(world.get_location("Towers Ronny Mission End", player),
        lambda state: state.has("Employment Contracts", player))

    # North Beach
    set_rule(world.get_location("North Beach Chest Scraps 1", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("North Beach Chest Scraps 2", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("North Beach Chest Scraps 3", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("North Beach Chest Scraps 4", player),
        lambda state: state.has("Lockpicks", player))

    # Mine Shaft
    set_rule(world.get_location("Mine Shaft Chest Scraps 1", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("Mine Shaft Chest Scraps 2", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("Mine Shaft Chest Scraps 3", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("Mine Shaft Chest Scraps 4", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("Mine Shaft Chest Scraps 5", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("Mine Shaft Chest Scraps 6", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("Mine Shaft Chest Scraps 7", player),
        lambda state: state.has("Lockpicks", player))

    # Mob Camp
    set_rule(world.get_entrance("Mob Camp Locked Door", player),
        lambda state: state.has("Mob Camp Key", player))

    set_rule(world.get_location("Mob Camp Locked Room Stolen Bob", player),
        lambda state: state.has("Broken Bob", player))

    # Mountain Ruin
    set_rule(world.get_entrance("Mountain Ruin Gate", player),
        lambda state: state.has("Mountain Ruin Key", player))

    set_rule(world.get_location("Mountain Ruin Inside Red Paint Can", player),
        lambda state: state.has("Lockpicks", player))

    # Prism Temple
    set_rule(world.get_location("Prism Temple Chest Scraps 1", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("Prism Temple Chest Scraps 2", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("Prism Temple Chest Scraps 3", player),
        lambda state: state.has("Lockpicks", player))

    # Pickle Lady
    set_rule(world.get_location("Pickle Val Jar of Pickles", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("Pickle Val Pickle Lady Mission End", player),
        lambda state: state.has("Jar of Pickles", player))

    # Morse Bunker
    set_rule(world.get_location("Morse Bunker Chest Scraps 1", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("Morse Bunker Chest Scraps 2", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("Morse Bunker Chest Scraps 3", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("Morse Bunker Chest Scraps 4", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("Morse Bunker Chest Scraps 5", player),
        lambda state: state.has("Lockpicks", player))

    # Add rules to reach the "Go mode"
    set_rule(world.get_location("Final Boss", player),
        lambda state: state.has("Temple Key", player)
            and state.has("Green Egg", player)
            and state.has("Blue Egg", player)
            and state.has("Red Egg", player))
    world.completion_condition[player] = lambda state: state.has("Victory", player)
