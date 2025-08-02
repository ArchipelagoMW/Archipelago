from BaseClasses import MultiWorld
from ..generic.Rules import set_rule
from .Options import CCCharlesOptions

# Go mode : egg_green + egg_blue + egg_red + temple_key + bug_spray (+ remote_explosive x8 but the base game ignores it)

def set_rules(world: MultiWorld, options: CCCharlesOptions, player: int) -> None:
    # Tony
    set_rule(world.get_location("barn_scraps_1", player),
        lambda state: state.has("Barn Key", player))
    set_rule(world.get_location("barn_scraps_2", player),
        lambda state: state.has("Barn Key", player))
    set_rule(world.get_location("barn_scraps_3", player),
        lambda state: state.has("Barn Key", player))
    set_rule(world.get_location("barn_scraps_4", player),
        lambda state: state.has("Barn Key", player))
    set_rule(world.get_location("barn_scraps_5", player),
        lambda state: state.has("Barn Key", player))
    set_rule(world.get_location("barn_scraps_6", player),
        lambda state: state.has("Barn Key", player))
    set_rule(world.get_location("barn_scraps_7", player),
        lambda state: state.has("Barn Key", player))
    set_rule(world.get_location("barn_scraps_8", player),
        lambda state: state.has("Barn Key", player))
    set_rule(world.get_location("barn_scraps_9", player),
        lambda state: state.has("Barn Key", player))

    # Candice
    set_rule(world.get_location("tutorial_scraps_1", player),
        lambda state: state.has("Candice's Key", player))
    set_rule(world.get_location("tutorial_scraps_2", player),
        lambda state: state.has("Candice's Key", player))
    set_rule(world.get_location("tutorial_scraps_3", player),
        lambda state: state.has("Candice's Key", player))
    set_rule(world.get_location("tutorial_scraps_4", player),
        lambda state: state.has("Candice's Key", player))
    set_rule(world.get_location("tutorial_scraps_5", player),
        lambda state: state.has("Candice's Key", player))
    set_rule(world.get_location("tutorial_scraps_6", player),
        lambda state: state.has("Candice's Key", player))
    set_rule(world.get_location("tutorial_scraps_7", player),
        lambda state: state.has("Candice's Key", player))
    set_rule(world.get_location("tutorial_scraps_8", player),
        lambda state: state.has("Candice's Key", player))
    set_rule(world.get_location("tutorial_scraps_9", player),
        lambda state: state.has("Candice's Key", player))

    # Lizbeth
    set_rule(world.get_location("swamp_lizbeth_murkwater_mission_end", player),
        lambda state: state.has("Dead Fish", player))

    # Daryl
    set_rule(world.get_location("junkyard_daryl_ancient_tablet", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("junkyard_daryl_mission_end", player),
        lambda state: state.has("Ancient Tablet", player))

    # South House
    set_rule(world.get_location("south_house_chest_scraps_1", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("south_house_chest_scraps_2", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("south_house_chest_scraps_3", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("south_house_chest_scraps_4", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("south_house_chest_scraps_5", player),
         lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("south_house_chest_scraps_6", player),
         lambda state: state.has("Lockpicks", player))

    # South Mine
    set_rule(world.get_location("south_mine_inside_scraps_1", player),
        lambda state: state.has("South Mine Key", player))
    set_rule(world.get_location("south_mine_inside_scraps_2", player),
        lambda state: state.has("South Mine Key", player))
    set_rule(world.get_location("south_mine_inside_scraps_3", player),
        lambda state: state.has("South Mine Key", player))
    set_rule(world.get_location("south_mine_inside_scraps_4", player),
        lambda state: state.has("South Mine Key", player))
    set_rule(world.get_location("south_mine_inside_scraps_5", player),
        lambda state: state.has("South Mine Key", player))
    set_rule(world.get_location("south_mine_inside_scraps_6", player),
        lambda state: state.has("South Mine Key", player))
    set_rule(world.get_location("south_mine_inside_scraps_7", player),
        lambda state: state.has("South Mine Key", player))
    set_rule(world.get_location("south_mine_inside_scraps_8", player),
        lambda state: state.has("South Mine Key", player))
    set_rule(world.get_location("south_mine_inside_scraps_9", player),
        lambda state: state.has("South Mine Key", player))
    set_rule(world.get_location("south_mine_inside_paint_can_green", player),
        lambda state: state.has("South Mine Key", player) and
            state.has("Lockpicks", player))

    # Theodore
    set_rule(world.get_location("station_theodore_mission_end", player),
        lambda state: state.has("Blue Box", player))

    # Watchtower
    set_rule(world.get_location("watchtower_paint_can_pink", player),
        lambda state: state.has("Lockpicks", player))

    # Sasha
    set_rule(world.get_location("house_sasha_mission_end", player),
            lambda state: state.has("Page Drawing", player, 8))

    # Santiago
    set_rule(world.get_location("port_santiago_mission_end", player),
        lambda state: state.has("Journal", player))

    # Trench House
    set_rule(world.get_location("trench_house_chest_scraps_1", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("trench_house_chest_scraps_2", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("trench_house_chest_scraps_3", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("trench_house_chest_scraps_4", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("trench_house_chest_scraps_5", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("trench_house_chest_scraps_6", player),
        lambda state: state.has("Lockpicks", player))

    # East House
    set_rule(world.get_location("east_house_chest_scraps_1", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("east_house_chest_scraps_2", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("east_house_chest_scraps_3", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("east_house_chest_scraps_4", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("east_house_chest_scraps_5", player),
        lambda state: state.has("Lockpicks", player))

    # Explosive Training
    set_rule(world.get_location("explosive_training_scraps_11", player),
        lambda state: state.has("Timed Dynamite", player))
    set_rule(world.get_location("explosive_training_scraps_12", player),
        lambda state: state.has("Timed Dynamite", player))
    set_rule(world.get_location("explosive_training_box_of_rocket", player),
        lambda state: state.has("Timed Dynamite", player))

    # John
    set_rule(world.get_location("workshop_john_smith_mission_end", player),
         lambda state: state.has("Box of Rocket", player))

    # Claire
    set_rule(world.get_location("lighthouse_claire_mission_end", player),
        lambda state: state.has("Breaker", player, 4))

    # North Mine
    set_rule(world.get_location("north_mine_inside_scraps_1", player),
        lambda state: state.has("North Mine Key", player))
    set_rule(world.get_location("north_mine_inside_scraps_2", player),
        lambda state: state.has("North Mine Key", player))
    set_rule(world.get_location("north_mine_inside_scraps_3", player),
        lambda state: state.has("North Mine Key", player))
    set_rule(world.get_location("north_mine_inside_scraps_4", player),
        lambda state: state.has("North Mine Key", player))
    set_rule(world.get_location("north_mine_inside_scraps_5", player),
        lambda state: state.has("North Mine Key", player))
    set_rule(world.get_location("north_mine_inside_scraps_6", player),
        lambda state: state.has("North Mine Key", player))
    set_rule(world.get_location("north_mine_inside_scraps_7", player),
        lambda state: state.has("North Mine Key", player))
    set_rule(world.get_location("north_mine_inside_scraps_8", player),
        lambda state: state.has("North Mine Key", player))
    set_rule(world.get_location("north_mine_inside_scraps_9", player),
        lambda state: state.has("North Mine Key", player))
    set_rule(world.get_location("north_mine_inside_scraps_10", player),
        lambda state: state.has("North Mine Key", player))
    set_rule(world.get_location("north_mine_inside_scraps_11", player),
        lambda state: state.has("North Mine Key", player))
    set_rule(world.get_location("north_mine_inside_scraps_12", player),
        lambda state: state.has("North Mine Key", player))
    set_rule(world.get_location("north_mine_inside_scraps_13", player),
        lambda state: state.has("North Mine Key", player))
    set_rule(world.get_location("north_mine_inside_blue_egg", player),
        lambda state: state.has("North Mine Key", player))
    set_rule(world.get_location("north_mine_inside_paint_can_blue", player),
        lambda state: state.has("North Mine Key", player) and
            state.has("Lockpicks", player))

    # Paul
    set_rule(world.get_location("museum_paul_mission_end", player),
        lambda state: state.has("Remote Explosive x8", player))
        # lambda state: state.has("Remote Explosive", player, 8)) # TODO : Add an option to split remote explosives

    # West Beach
    set_rule(world.get_location("west_beach_chest_scraps_1", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("west_beach_chest_scraps_2", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("west_beach_chest_scraps_3", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("west_beach_chest_scraps_4", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("west_beach_chest_scraps_5", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("west_beach_chest_scraps_6", player),
        lambda state: state.has("Lockpicks", player))

    # Caravan
    set_rule(world.get_location("caravan_chest_scraps_1", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("caravan_chest_scraps_2", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("caravan_chest_scraps_3", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("caravan_chest_scraps_4", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("caravan_chest_scraps_5", player),
        lambda state: state.has("Lockpicks", player))

    # Ronny
    set_rule(world.get_location("towers_ronny_mission_end", player),
        lambda state: state.has("Employment Contracts", player))

    # North Beach
    set_rule(world.get_location("north_beach_chest_scraps_1", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("north_beach_chest_scraps_2", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("north_beach_chest_scraps_3", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("north_beach_chest_scraps_4", player),
        lambda state: state.has("Lockpicks", player))

    # Mine Shaft
    set_rule(world.get_location("mine_shaft_chest_scraps_1", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("mine_shaft_chest_scraps_2", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("mine_shaft_chest_scraps_3", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("mine_shaft_chest_scraps_4", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("mine_shaft_chest_scraps_5", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("mine_shaft_chest_scraps_6", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("mine_shaft_chest_scraps_7", player),
        lambda state: state.has("Lockpicks", player))

    # Mob Camp
    set_rule(world.get_location("mob_camp_scraps_17", player),
        lambda state: state.has("Mob Camp Key", player))
    set_rule(world.get_location("mob_camp_scraps_18", player),
        lambda state: state.has("Mob Camp Key", player))
    set_rule(world.get_location("mob_camp_stolen_bob", player),
        lambda state: state.has("Mob Camp Key", player) and
            state.has("Broken Bob", player))

    # Mountain Ruin
    set_rule(world.get_location("mountain_ruin_inside_scraps_1", player),
        lambda state: state.has("Mountain Ruin Key", player))
    set_rule(world.get_location("mountain_ruin_inside_scraps_2", player),
        lambda state: state.has("Mountain Ruin Key", player))
    set_rule(world.get_location("mountain_ruin_inside_scraps_3", player),
        lambda state: state.has("Mountain Ruin Key", player))
    set_rule(world.get_location("mountain_ruin_inside_scraps_4", player),
        lambda state: state.has("Mountain Ruin Key", player))
    set_rule(world.get_location("mountain_ruin_inside_scraps_5", player),
        lambda state: state.has("Mountain Ruin Key", player))
    set_rule(world.get_location("mountain_ruin_inside_scraps_6", player),
        lambda state: state.has("Mountain Ruin Key", player))
    set_rule(world.get_location("mountain_ruin_inside_scraps_7", player),
        lambda state: state.has("Mountain Ruin Key", player))
    set_rule(world.get_location("mountain_ruin_inside_scraps_8", player),
        lambda state: state.has("Mountain Ruin Key", player))
    set_rule(world.get_location("mountain_ruin_inside_scraps_9", player),
        lambda state: state.has("Mountain Ruin Key", player))
    set_rule(world.get_location("mountain_ruin_inside_scraps_10", player),
        lambda state: state.has("Mountain Ruin Key", player))
    set_rule(world.get_location("mountain_ruin_inside_scraps_11", player),
        lambda state: state.has("Mountain Ruin Key", player))
    set_rule(world.get_location("mountain_ruin_inside_scraps_12", player),
        lambda state: state.has("Mountain Ruin Key", player))
    set_rule(world.get_location("mountain_ruin_inside_scraps_13", player),
        lambda state: state.has("Mountain Ruin Key", player))
    set_rule(world.get_location("mountain_ruin_inside_scraps_14", player),
        lambda state: state.has("Mountain Ruin Key", player))
    set_rule(world.get_location("mountain_ruin_inside_scraps_15", player),
        lambda state: state.has("Mountain Ruin Key", player))
    set_rule(world.get_location("mountain_ruin_inside_scraps_16", player),
        lambda state: state.has("Mountain Ruin Key", player))
    set_rule(world.get_location("mountain_ruin_inside_scraps_17", player),
        lambda state: state.has("Mountain Ruin Key", player))
    set_rule(world.get_location("mountain_ruin_inside_red_egg", player),
        lambda state: state.has("Mountain Ruin Key", player))
    set_rule(world.get_location("mountain_ruin_inside_paint_can_red", player),
        lambda state: state.has("Mountain Ruin Key", player) and
            state.has("Lockpicks", player))

    # Prism Temple
    set_rule(world.get_location("prism_temple_chest_scraps_1", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("prism_temple_chest_scraps_2", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("prism_temple_chest_scraps_3", player),
        lambda state: state.has("Lockpicks", player))

    # Pickle
    set_rule(world.get_location("field_pickle_lady_jar_of_pickles", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("field_pickle_lady_mission_end", player),
         lambda state: state.has("Jar of Pickles", player))

    # Morse Bunker
    set_rule(world.get_location("morse_bunker_chest_scraps_1", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("morse_bunker_chest_scraps_2", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("morse_bunker_chest_scraps_3", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("morse_bunker_chest_scraps_4", player),
        lambda state: state.has("Lockpicks", player))
    set_rule(world.get_location("morse_bunker_chest_scraps_5", player),
        lambda state: state.has("Lockpicks", player))

    # Place "Victory" at "Final Boss" and set collection as win condition
    world.completion_condition[player] = lambda state: state.has("Victory", player)
