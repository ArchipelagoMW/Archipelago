from typing import TYPE_CHECKING, Dict, NamedTuple, Set
from enum import IntEnum
from BaseClasses import Region, Location, Item, ItemClassification
from worlds.generic.Rules import add_rule

from ...constants import get_game_base_id

if TYPE_CHECKING:
    from ... import UFO50World


class Hidden(IntEnum):
    not_hidden = 0
    has_tell = 1
    no_tell = 2


class LocationInfo(NamedTuple):
    id_offset: int
    region_name: str
    fuel_touch: int = 0  # how many tanks it took to get to the check
    fuel_get: int = 0  # how many tanks it took to get to the check and back to a base
    concealed: int = Hidden.not_hidden


# for breaking variuos rocks mostly
class EventInfo(NamedTuple):
    region_name: str
    item_name: str


location_table: Dict[str, LocationInfo] = {
    # Shallows
    "Shallows Upper Left - Ceiling Torpedo Upgrade": LocationInfo(20, "Shallows", 1, 2, Hidden.no_tell),  # no missile
    "Shallows Upper Left - Fuel Tank next to Coral": LocationInfo(1, "Shallows", 2, 3),
    "Shallows Lower Left - Fuel Tank between some Coral": LocationInfo(10, "Shallows", 1, 2),
    "Shallows Lower Left - Fuel Tank above Breakable Rocks": LocationInfo(8, "Shallows - Missile", 1, 2),  # missile
    "Shallows Upper Mid - Torpedo Upgrade at Surface": LocationInfo(27, "Shallows - Buster", 2, 4),  # buster
    "Shallows Upper Mid - Fuel Tank on Coral": LocationInfo(9, "Shallows", 1, 1),
    "Shallows Uppper Mid - Fuel Tank behind ! Blocks": LocationInfo(6, "Shallows - Buster", 2, 3),  # buster
    "Shallows Upper Mid - Egg at Surface": LocationInfo(52, "Shallows - Buster", 1, 2),  # buster
    "Shallows Upper Mid - Fuel Tank in Floor at Surface": LocationInfo(11, "Shallows - Buster", 1, 2, Hidden.has_tell),  # buster, depth
    "Shallows Mid - Torpedo Upgrade above Breakable Rocks": LocationInfo(24, "Shallows - Missile", 3, 5),  # missile
    # ship requires explosives to enter
    # using missiles, it requires 6 fuel tanks to open it and get back to base
    "Shallows Sunken Ship - Cargo Hold Egg": LocationInfo(55, "Sunken Ship", 2, 4),
    "Shallows Sunken Ship - Bow Egg": LocationInfo(51, "Sunken Ship - Buster", 2, 4),  # buster
    "Shallows Sunken Ship - Bow Torpedo Upgrade in Wall": LocationInfo(26, "Sunken Ship - Buster", 2, 4, Hidden.has_tell),  # buster
    "Shallows Sunken Ship - Depth Charge Module": LocationInfo(92, "Sunken Ship", 2, 4),
    "Shallows Lower Mid - Super Booster Module": LocationInfo(93, "Shallows", 3, 5),  # assumes light damage
    "Shallows Lower Mid - Fuel Tank on Coral": LocationInfo(2, "Shallows", 2, 4),
    "Shallows Lower Mid - Egg on Coral": LocationInfo(53, "Shallows", 3, 4),
    "Shallows Lower Mid - Lower Ceiling Torpedo Upgrade": LocationInfo(22, "Shallows - Missile", 2, 3, Hidden.no_tell),  # missile
    "Shallows Lower Mid - Upper Ceiling Torpedo Upgrade": LocationInfo(21, "Shallows", 1, 2, Hidden.no_tell),
    "Shallows Lower Mid - Fuel Tank in Floor": LocationInfo(7, "Shallows - Depth", 1, 2, Hidden.has_tell),  # depth
    "Shallows Lower Mid - Torpedo Upgrade on Coral": LocationInfo(23, "Shallows", 2, 3),
    "Shallows Upper Right - Fuel Tank under Breakable Rocks": LocationInfo(5, "Shallows - Depth", 2, 3),  # depth
    # 5.5 tanks to get from base to first maze block w/o drill, 2 tanks w/ drill
    # fuel tank: 6.5 to touch, 13 or 3 to touch w/ drill (tested), 6 w/ drill
    # torpedo: 8.5 to touch, 15 or 5 to touch w/ drill (tested), 8 w/ drill
    # egg: 10.5 to touch, 16 or 7 to touch w/ drill (tested), 9 to base w/ drill
    "Shallows Upper Right - Fuel Tank in Coral Maze": LocationInfo(4, "Shallows - Buster", Hidden.no_tell),
    "Shallows Upper Right - Torpedo Upgrade in Coral Maze": LocationInfo(25, "Shallows - Buster"),
    "Shallows Upper Right - Egg in Coral Maze": LocationInfo(50, "Shallows - Buster"),

    "Shallows Lower Right - Fuel Tank under Breakable Rocks": LocationInfo(3, "Shallows - Depth", 3, 7),  # depth
    "Shallows Lower Right - Buster Torpedoes Module": LocationInfo(90, "Shallows", 2, 3),
    "Shallows Lower Right - Egg behind ! Blocks": LocationInfo(54, "Shallows - Buster", 2, 3),  # buster
    "Shallows Lower Right - Egg in Coral": LocationInfo(56, "Shallows - Buster", 3, 5, Hidden.no_tell),  # buster
    "Shallows Lower Right - Drill Module": LocationInfo(91, "Shallows - Buster", 3, 6),  # buster

    # Deeper
    # 1.75 from left base to non-boat deeper entrance
    # 1 from right base to deep entrance
    # from left base to boat depths entrance
    "Deeper Upper Left - Torpedo Upgrade in Wall": LocationInfo(121, "Deeper", Hidden.has_tell),
    "Deeper Upper Left - Egg by Urchins": LocationInfo(150, "Deeper", 4, 7),
    "Deeper Upper Left - Fuel Tank on Coral": LocationInfo(100, "Deeper", 4, 7),
    "Deeper Upper Left - Fuel Tank behind ! Blocks": LocationInfo(103, "Deeper", 4, 6),
    "Deeper Upper Mid - Torpedo Upgrade in Coral": LocationInfo(124, "Deeper", 3, 5, Hidden.no_tell),
    "Deeper Upper Mid - Torpedo Upgrade in Ceiling": LocationInfo(125, "Deeper", 3, 6, Hidden.has_tell),  # depth or missile
    "Deeper Upper Mid - Egg in Dirt": LocationInfo(154, "Deeper", Hidden.no_tell),  # drill, 3/5
    "Deeper Upper Mid - Spotlight Module": LocationInfo(192, "Deeper", 3, 5),  # depth
    "Deeper Upper Mid - Fuel Tank in Collapsed Structure": LocationInfo(102, "Deeper", 2, 5),
    "Deeper Upper Right - Fuel Tank in Collapsed Structure": LocationInfo(104, "Deeper", 3, 5),
    "Deeper Upper Right - Egg on Coral": LocationInfo(155, "Deeper", 4, 7),  # about the same speed with drill
    "Deeper Upper Right - Torpedo Upgrade in Wall": LocationInfo(122, "Deeper", 3, 5, Hidden.has_tell),
    "Deeper Right - Torpedo Upgrade on Coral": LocationInfo(123, "Deeper", 5, 8),  # same speed to blow up rocks
    "Deeper Upper Right - Targeting System Module": LocationInfo(190, "Deeper", 5, 9),
    "Deeper Lower Right - Egg behind Urchins": LocationInfo(152, "Deeper", 3, 5, Hidden.no_tell),
    "Deeper Lower Right - Fuel Tank in Ceiling": LocationInfo(105, "Deeper", 4, 7, Hidden.no_tell),  # depth or missile
    "Deeper Lower Right - Egg on Coral": LocationInfo(151, "Deeper", 5, 8),
    "Deeper Lower Mid - Missile System Module": LocationInfo(191, "Deeper", 4, 7),
    "Deeper Lower Mid - Torpedo Upgrade on Coral": LocationInfo(120, "Deeper", 4, 7),
    "Deeper Lower Mid - Fuel Tank in Floor": LocationInfo(101, "Deeper", Hidden.has_tell),  # depth, 4/7
    "Deeper Lower Left - Egg in Wall": LocationInfo(153, "Deeper", 4, 7, Hidden.no_tell),

    # Abyss
    # there's a paint net file with Abyss routes on them, with the fuel taken for them
    "Abyss Upper Left - Egg on Seaweed near Urchins": LocationInfo(251, "Abyss"),
    "Abyss Upper Left - Fuel Tank on Seaweed": LocationInfo(201, "Abyss", 4, 9),  # put in a rule if combat logic changes
    "Abyss Upper Left - Egg on Seaweed above Torpedo Upgrade": LocationInfo(252, "Abyss"),
    "Abyss Upper Left - Torpedo Upgrade in Seaweed": LocationInfo(220, "Abyss", Hidden.no_tell),
    "Abyss Lower Left - Egg in Facility": LocationInfo(256, "Abyss"),
    "Abyss Lower Left - Torpedo Upgrade in Facility": LocationInfo(223, "Abyss"),
    "Abyss Lower Left - Fuel Tank in Facility Floor": LocationInfo(200, "Abyss", Hidden.has_tell),
    "Abyss Upper Mid - Torpedo Upgrade in Wall": LocationInfo(221, "Abyss", Hidden.has_tell),
    "Abyss Upper Mid - Torpedo Upgrade in Cave": LocationInfo(222, "Abyss"),
    "Abyss Upper Mid - Egg on Seaweed": LocationInfo(253, "Abyss"),
    "Abyss Upper Mid - Efficient Fuel Module": LocationInfo(290, "Abyss"),
    "Abyss Upper Mid - Egg in Seaweed": LocationInfo(255, "Abyss", Hidden.no_tell),  # 4 to touch, 9 to base w/ bomb,
    "Abyss Upper Mid - Torpedo Upgrade behind Seaweed": LocationInfo(225, "Abyss"),
    "Abyss Upper Right - Egg by Seaweed": LocationInfo(254, "Abyss"),
    "Abyss Upper Right - Torpedo Upgrade in Wall": LocationInfo(224, "Abyss", 4, 8, Hidden.has_tell),
    "Abyss Lower Right - Fuel Tank in Floor": LocationInfo(202, "Abyss", Hidden.no_tell),  # technically has a tell but eh
    "Abyss Lower Right - Egg by Skull": LocationInfo(250, "Abyss"),
    "Abyss Lower Right - Radar System Module": LocationInfo(291, "Abyss"),
    "Abyss Lower Right - Armor Plating Module": LocationInfo(292, "Abyss"),

    # Bosses
    # combat logic is weird cause you can save damage done to a boss
    # my gut says 7 fuel, 5 torpedo upgrades OR 5 fuel and depth charges for the first two bosses
    "Lamia": LocationInfo(300, "Shallows"),  # shark
    "Iku Turso": LocationInfo(301, "Shallows"),  # octopus
    # 10 fuel, 8 torpedo upgrades, missile module or burst OR 8 fuel and depth charges for the second two bosses
    "Bakunawa": LocationInfo(302, "Deeper"),  # moray eel
    "Neptune": LocationInfo(303, "Deeper"),  # nautilus

    # 13 fuel, 12 torpedo upgrades, missile module, burst OR 13 fuel and depth charges
    "Dracula": LocationInfo(304, "Abyss"),  # squid-thing

    "Garden": LocationInfo(997, "Menu"),
    "Gold": LocationInfo(998, "Abyss"),
    "Cherry": LocationInfo(999, "Abyss")
}


event_table: Dict[str, EventInfo] = {
    "Sunken Ship": EventInfo("Shallows", "Bombed Open the Ship"),
    "Rock at Buster Urchin Path": EventInfo("Deeper", "Bombed the Buster Urchin Path Exit Rock"),
    "Rock at Leftmost Abyss Entrance": EventInfo("Deeper", "Bombed the Leftmost Abyss Entrance Rock"),
    "Rock at Second from Left Abyss Entrance": EventInfo("Deeper", "Bombed the Second from Left Abyss Entrance Rock"),
    "Rightmost Abyss Rock": EventInfo("Abyss", "Bombed the Rightmost Abyss Rock"),
}


# this is for filling out location_name_to_id, it should be static regardless of yaml options
def get_locations() -> Dict[str, int]:
    return {f"Porgy - {name}": data.id_offset + get_game_base_id("Porgy") for name, data in location_table.items()}


# this should return the location groups for this game, independent of yaml options
# you should include a group that contains all location for this game that is called the same thing as the game
def get_location_groups() -> Dict[str, Set[str]]:
    location_groups: Dict[str, Set[str]] = {"Porgy": {f"Porgy - {loc_name}" for loc_name in location_table.keys()}}
    return location_groups


# this is not a required function, but a recommended one -- the world class does not call this function
def create_locations(world: "UFO50World", regions: Dict[str, Region]) -> None:
    for loc_name, loc_data in location_table.items():
        if loc_name == "Cherry" and "Porgy" not in world.options.cherry_allowed_games:
            break
        if loc_name in ["Gold", "Cherry"] and "Porgy" in world.goal_games:
            if (loc_name == "Gold" and "Porgy" not in world.options.cherry_allowed_games) or loc_name == "Cherry":
                loc = Location(world.player, f"Porgy - {loc_name}", None, regions[loc_data.region_name])
                loc.place_locked_item(Item("Completed Porgy", ItemClassification.progression, None, world.player))
                add_rule(world.get_location("Completed All Games"), lambda state: state.has("Completed Porgy", world.player))
                regions[loc_data.region_name].locations.append(loc)
                break

        loc = Location(world.player, f"Porgy - {loc_name}", get_game_base_id("Porgy") + loc_data.id_offset,
                       regions[loc_data.region_name])
        regions[loc_data.region_name].locations.append(loc)

    for event_name, event_data in event_table.items():
        event_loc = Location(world.player, f"Porgy - {event_name}", None, regions[event_data.region_name])
        event_item = Item(f"Porgy - {event_data.item_name}", ItemClassification.progression, None, world.player)
        event_loc.place_locked_item(event_item)
        regions[event_data.region_name].locations.append(event_loc)
