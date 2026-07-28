from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import ItemClassification, Location

from . import items

if TYPE_CHECKING:
    from .world import BATIMWorld


LOCATION_NAME_TO_ID = {
    "CH1 Bacon Soup 0": 100,
    "CH1 Bacon Soup 1": 101,
    "CH1 Bacon Soup 2": 102,
    "CH1 Bacon Soup 3": 103,
    "CH1 Bacon Soup 4": 104,
    "CH1 Bacon Soup 5": 105,
    "CH1 Bacon Soup 6": 106,
    "CH1 Bacon Soup 7": 107,
    "CH1 Bacon Soup 8": 108,
    "CH1 Bacon Soup 9": 109,
    "CH1 Bacon Soup 10": 110,
    "CH1 Bacon Soup 11": 111,
    "CH1 Bacon Soup 12": 112,
    "CH1 Bacon Soup 13": 113,
    "CH1 Bacon Soup 14": 114,
    "CH1 Bacon Soup 15": 115,
    "CH1 Bacon Soup 16": 116,
    "CH1 Bacon Soup 17": 117,
    "CH1 Bacon Soup 18": 118,
    "CH1 Bacon Soup 19": 119,
    "CH1 Bacon Soup 20": 120,
    "CH1 Book": 121,
    "CH1 Doll": 122,
    "CH1 Gear": 123,
    "CH1 Inkwell": 124,
    "CH1 Record": 125,
    "CH1 Wrench": 126,
    "CH1 Audio Log Dark and Cold": 127,
    "CH1 Audio Log This Machine": 128,
    "CH1 Radio": 129,
    "CH1 theMeatly": 130,
    "CH1 Complete": 199,
    "CH2 Bacon Soup 0": 200,
    "CH2 Bacon Soup 1": 201,
    "CH2 Bacon Soup 2": 202,
    "CH2 Bacon Soup 3": 203,
    "CH2 Bacon Soup 4": 204,
    "CH2 Bacon Soup 5": 205,
    "CH2 Bacon Soup 6": 206,
    "CH2 Bacon Soup 7": 207,
    "CH2 Bacon Soup 8": 208,
    "CH2 Bacon Soup 9": 209,
    "CH2 Bacon Soup 10": 210,
    "CH2 Bacon Soup 11": 211,
    "CH2 Bacon Soup 12": 212,
    "CH2 Bacon Soup 13": 213,
    "CH2 Bacon Soup 14": 214,
    "CH2 Bacon Soup 15": 215,
    "CH2 Bacon Soup 16": 216,
    "CH2 Bacon Soup 17": 217,
    "CH2 Bacon Soup 18": 218,
    "CH2 Bacon Soup 19": 219,
    "CH2 Bacon Soup 20": 220,
    "CH2 Bacon Soup 21": 221,
    "CH2 Bacon Soup 22": 222,
    "CH2 Bacon Soup 23": 223,
    "CH2 Bacon Soup 24": 224,
    "CH2 Bacon Soup 25": 225,
    "CH2 Bacon Soup 26": 226,
    "CH2 Bacon Soup 27": 227,
    "CH2 Bacon Soup 28": 228,
    "CH2 Bacon Soup 29": 229,
    "CH2 Bacon Soup 30": 230,
    "CH2 Keys": 231,
    "CH2 Valve": 232,
    "CH2 Audio Log Can I Get an Amen?": 233,
    "CH2 Audio Log The Pump Switch": 234,
    "CH2 Audio Log New Actress": 235,
    "CH2 Audio Log Crazy Sammy": 236,
    "CH2 Audio Log Stupid Keys": 237,
    "CH2 Audio Log Sanctuary Puzzle": 238,
    "CH2 Audio Log Quiet and Smelly Sewers": 239,
    "CH2 Radio": 240,
    "CH2 theMeatly": 241,
    "CH2 Complete": 299,
    "CH3 Bacon Soup 0": 300,
    "CH3 Bacon Soup 1": 301,
    "CH3 Bacon Soup 2": 302,
    "CH3 Bacon Soup 3": 303,
    "CH3 Bacon Soup 4": 304,
    "CH3 Bacon Soup 5": 305,
    "CH3 Bacon Soup 6": 306,
    "CH3 Bacon Soup 7": 307,
    "CH3 Bacon Soup 8": 308,
    "CH3 Bacon Soup 9": 309,
    "CH3 Bacon Soup 10": 310,
    "CH3 Bacon Soup 11": 311,
    "CH3 Bacon Soup 12": 312,
    "CH3 Bacon Soup 13": 313,
    "CH3 Bacon Soup 14": 314,
    "CH3 Bacon Soup 15": 315,
    "CH3 Bacon Soup 16": 316,
    "CH3 Bacon Soup 17": 317,
    "CH3 Bacon Soup 18": 318,
    "CH3 Bacon Soup 19": 319,
    "CH3 Bacon Soup 20": 320,
    "CH3 Bacon Soup 21": 321,
    "CH3 Bacon Soup 22": 322,
    "CH3 Bacon Soup 23": 323,
    "CH3 Bacon Soup 24": 324,
    "CH3 Bacon Soup 25": 325,
    "CH3 Bacon Soup 26": 326,
    "CH3 Bacon Soup 27": 327,
    "CH3 Bacon Soup 28": 328,
    "CH3 Bacon Soup 29": 329,
    "CH3 Bacon Soup 30": 330,
    "CH3 Bacon Soup 31": 331,
    "CH3 Bacon Soup 32": 332,
    "CH3 Bacon Soup 33": 333,
    "CH3 Bacon Soup 34": 334,
    "CH3 Bacon Soup 35": 335,
    "CH3 Bacon Soup 36": 336,
    "CH3 Bacon Soup 37": 337,
    "CH3 Bacon Soup 38": 338,
    "CH3 Audio Log Crooked Smile": 350,
    "CH3 Audio Log Time to Believe": 351,
    "CH3 Audio Log Everything is Coming Apart": 352,
    "CH3 Audio Log Ink Pressure": 353,
    "CH3 Audio Log Cutting Corners": 354,
    "CH3 Audio Log Lunch with Joey": 355,
    "CH3 Audio Log Crack a Smile": 356,
    "CH3 Audio Log The Genius Upstairs": 357,
    "CH3 Audio Log Looking for Trouble": 358,
    "CH3 Audio Log Man of Ideas": 359,
    "CH3 Radio": 360,
    "CH3 theMeatly": 361,
    "CH3 Complete": 399,
    "CH4 Bacon Soup 0": 400,
    "CH4 Bacon Soup 1": 401,
    "CH4 Bacon Soup 2": 402,
    "CH4 Bacon Soup 3": 403,
    "CH4 Bacon Soup 4": 404,
    "CH4 Bacon Soup 5": 405,
    "CH4 Bacon Soup 6": 406,
    "CH4 Bacon Soup 7": 407,
    "CH4 Bacon Soup 8": 408,
    "CH4 Bacon Soup 9": 409,
    "CH4 Bacon Soup 10": 410,
    "CH4 Bacon Soup 11": 411,
    "CH4 Bacon Soup 12": 412,
    "CH4 Bacon Soup 13": 413,
    "CH4 Bacon Soup 14": 414,
    "CH4 Bacon Soup 15": 415,
    "CH4 Bacon Soup 16": 416,
    "CH4 Bacon Soup 17": 417,
    "CH4 Bacon Soup 18": 418,
    "CH4 Bulls Eye": 419,
    "CH4 Call the Milk Man": 420,
    "CH4 Wasting Time": 421,
    "CH4 Bertrum Boss": 422,
    "CH4 Brute Boris Boss": 423,
    "CH4 Audio Log Indiscernible": 430,
    "CH4 Audio Log Behind Closed Doors": 431,
    "CH4 Audio Log Colossal Wonders": 432,
    "CH4 Audio Log Playing Games": 433,
    "CH4 Audio Log Mechanical Demon": 434,
    "CH4 Audio Log Bertrum's Reveal": 435,
    "CH4 Audio Log Turn it Off": 436,
    "CH4 Radio": 437,
    "CH4 theMeatly": 438,
    "CH4 Complete": 499,
    "CH5 Bacon Soup 0": 500,
    "CH5 Bacon Soup 1": 501,
    "CH5 Bacon Soup 2": 502,
    "CH5 Bacon Soup 3": 503,
    "CH5 Bacon Soup 4": 504,
    "CH5 Bacon Soup 5": 505,
    "CH5 Bacon Soup 6": 506,
    "CH5 Sammy Lawrence Boss": 507,
    "CH5 Audio Log Office Report": 520,
    "CH5 Audio Log Chocolate Cake": 521,
    "CH5 Audio Log The Big Picture": 522,
    "CH5 Audio Log Thousands of Souls": 523,
    "CH5 Audio Log Bringing Alice to Life": 524,
    "CH5 Audio Log Bendy's End": 525,
    "CH5 Radio": 526,
    "CH5 theMeatly": 527,
}


class BATIMLocation(Location):
    game = "Bendy and the Ink Machine"


def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: LOCATION_NAME_TO_ID[location_name] for location_name in location_names}


def create_all_locations(world: BATIMWorld) -> None:
    create_regular_locations(world)
    create_events(world)


def create_regular_locations(world: BATIMWorld) -> None:
    ch1_intro = world.get_region("CH1 Intro")
    ch1_basement = world.get_region("CH1 Basement")
    ch2_intro = world.get_region("CH2 Intro")
    ch2_after_keys = world.get_region("CH2 After Keys")
    ch2_after_valve = world.get_region("CH2 After Valve")
    ch3_intro = world.get_region("CH3 Intro")
    ch3_alice_objectives = world.get_region("CH3 Alice Objectives")
    ch4_intro = world.get_region("CH4 Intro")
    ch4_after_book_puzzle = world.get_region("CH4 After Book Puzzle")
    ch4_after_bertrum = world.get_region("CH4 After Bertrum")
    ch5 = world.get_region("CH5")

    ch1_intro_locations = get_location_names_with_ids([
        "CH1 Doll",
        "CH1 Gear",
        "CH1 Wrench",
        "CH1 Record",
        "CH1 Inkwell",
        "CH1 Book",
        "CH1 Bacon Soup 1",
        "CH1 Bacon Soup 2",
        "CH1 Bacon Soup 3",
        "CH1 Bacon Soup 4",
        "CH1 Bacon Soup 5",
        "CH1 Bacon Soup 6",
        "CH1 Bacon Soup 7",
        "CH1 Bacon Soup 8",
        "CH1 Bacon Soup 9",
        "CH1 Bacon Soup 10",
        "CH1 Bacon Soup 11",
        "CH1 Bacon Soup 12",
        "CH1 Bacon Soup 13",
        "CH1 Bacon Soup 14",
        "CH1 Bacon Soup 15",
        "CH1 Bacon Soup 16",
        "CH1 Bacon Soup 17",
        "CH1 Bacon Soup 18",
        "CH1 Bacon Soup 19",
        "CH1 Audio Log This Machine",
        "CH1 Radio",
    ])
    ch1_intro.add_locations(ch1_intro_locations, BATIMLocation)

    ch1_basement_locations = get_location_names_with_ids(["CH1 Bacon Soup 20", "CH1 Bacon Soup 0", "CH1 Audio Log Dark and Cold", "CH1 Complete"])
    ch1_basement.add_locations(ch1_basement_locations, BATIMLocation)

    ch2_intro_locations = get_location_names_with_ids([
        "CH2 Bacon Soup 0",
        "CH2 Bacon Soup 3",
        "CH2 Bacon Soup 4",
        "CH2 Bacon Soup 5",
        "CH2 Bacon Soup 6",
        "CH2 Bacon Soup 7",
        "CH2 Bacon Soup 8",
        "CH2 Bacon Soup 9",
        "CH2 Bacon Soup 10",
        "CH2 Bacon Soup 11",
        "CH2 Bacon Soup 12",
        "CH2 Bacon Soup 13",
        "CH2 Bacon Soup 14",
        "CH2 Bacon Soup 15",
        "CH2 Bacon Soup 16",
        "CH2 Bacon Soup 17",
        "CH2 Bacon Soup 18",
        "CH2 Bacon Soup 19",
        "CH2 Bacon Soup 20",
        "CH2 Bacon Soup 25",
        "CH2 Bacon Soup 26",
        "CH2 Bacon Soup 27",
        "CH2 Bacon Soup 28",
        "CH2 Bacon Soup 29",
        "CH2 Audio Log Can I Get an Amen?",
        "CH2 Audio Log The Pump Switch",
        "CH2 Audio Log New Actress",
        "CH2 Audio Log Crazy Sammy",
        "CH2 Audio Log Stupid Keys",
        "CH2 Keys",
    ])
    ch2_intro.add_locations(ch2_intro_locations, BATIMLocation)

    ch2_after_keys_locations = get_location_names_with_ids([
        "CH2 Bacon Soup 1",
        "CH2 Bacon Soup 2",
        "CH2 Bacon Soup 23",
        "CH2 Bacon Soup 24",
        "CH2 Bacon Soup 30",
        "CH2 Audio Log Sanctuary Puzzle",
        "CH2 Audio Log Quiet and Smelly Sewers",
        "CH2 Valve",
    ])
    ch2_after_keys.add_locations(ch2_after_keys_locations, BATIMLocation)

    ch2_after_valve_locations = get_location_names_with_ids([
        "CH2 Bacon Soup 21",
        "CH2 Bacon Soup 22",
        "CH2 Radio",
        "CH2 Complete",
    ])
    ch2_after_valve.add_locations(ch2_after_valve_locations, BATIMLocation)

    ch3_intro_locations = get_location_names_with_ids([
        "CH3 Bacon Soup 0",
        "CH3 Bacon Soup 1",
        "CH3 Bacon Soup 2",
        "CH3 Bacon Soup 3",
        "CH3 Bacon Soup 4",
        "CH3 Bacon Soup 22",
        "CH3 Bacon Soup 24",
        "CH3 Bacon Soup 25",
        "CH3 Bacon Soup 29",
        "CH3 Bacon Soup 30",
        "CH3 Bacon Soup 33",
        "CH3 Bacon Soup 36",
        "CH3 Bacon Soup 38",
        "CH3 Audio Log Crooked Smile",
        "CH3 Audio Log Everything is Coming Apart",
        "CH3 Audio Log Time to Believe",
        "CH3 Audio Log Ink Pressure",
        "CH3 Audio Log Cutting Corners",
        "CH3 Audio Log Lunch with Joey",
    ])
    ch3_intro.add_locations(ch3_intro_locations, BATIMLocation)

    ch3_alice_objectives_locations = get_location_names_with_ids([
        "CH3 Bacon Soup 5",
        "CH3 Bacon Soup 6",
        "CH3 Bacon Soup 7",
        "CH3 Bacon Soup 8",
        "CH3 Bacon Soup 9",
        "CH3 Bacon Soup 10",
        "CH3 Bacon Soup 11",
        "CH3 Bacon Soup 12",
        "CH3 Bacon Soup 13",
        "CH3 Bacon Soup 14",
        "CH3 Bacon Soup 15",
        "CH3 Bacon Soup 16",
        "CH3 Bacon Soup 17",
        "CH3 Bacon Soup 18",
        "CH3 Bacon Soup 19",
        "CH3 Bacon Soup 20",
        "CH3 Bacon Soup 21",
        "CH3 Bacon Soup 23",
        "CH3 Bacon Soup 26",
        "CH3 Bacon Soup 27",
        "CH3 Bacon Soup 28",
        "CH3 Bacon Soup 31",
        "CH3 Bacon Soup 32",
        "CH3 Bacon Soup 34",
        "CH3 Bacon Soup 35",
        "CH3 Bacon Soup 37",
        "CH3 Audio Log Crack a Smile",
        "CH3 Audio Log The Genius Upstairs",
        "CH3 Audio Log Looking for Trouble",
        "CH3 Audio Log Man of Ideas",
        "CH3 Radio",
        "CH3 Complete",
    ])
    ch3_alice_objectives.add_locations(ch3_alice_objectives_locations, BATIMLocation)

    ch4_intro_locations = get_location_names_with_ids([
        "CH4 Bacon Soup 1",
        "CH4 Bacon Soup 6",
        "CH4 Bacon Soup 14",
        "CH4 Audio Log Indiscernible",
        "CH4 Audio Log Behind Closed Doors",
    ])
    ch4_intro.add_locations(ch4_intro_locations, BATIMLocation)

    ch4_after_book_puzzle_locations = get_location_names_with_ids([
        "CH4 Bacon Soup 0",
        "CH4 Bacon Soup 2",
        "CH4 Bacon Soup 3",
        "CH4 Bacon Soup 4",
        "CH4 Bacon Soup 7",
        "CH4 Bacon Soup 8",
        "CH4 Bacon Soup 9",
        "CH4 Bacon Soup 10",
        "CH4 Bacon Soup 15",
        "CH4 Bacon Soup 16",
        "CH4 Bacon Soup 17",
        "CH4 Bacon Soup 18",
        "CH4 Audio Log Colossal Wonders",
        "CH4 Audio Log Playing Games",
        "CH4 Audio Log Mechanical Demon",
        "CH4 Radio",
    ])
    ch4_after_book_puzzle.add_locations(ch4_after_book_puzzle_locations, BATIMLocation)

    ch4_after_bertrum_locations = get_location_names_with_ids([
        "CH4 Bacon Soup 5",
        "CH4 Bacon Soup 11",
        "CH4 Bacon Soup 12",
        "CH4 Bacon Soup 13",
        "CH4 Bertrum Boss",
        "CH4 Brute Boris Boss",
        "CH4 Audio Log Bertrum's Reveal",
        "CH4 Audio Log Turn it Off",
        "CH4 Complete",
    ])
    ch4_after_bertrum.add_locations(ch4_after_bertrum_locations, BATIMLocation)

    ch5_locations = get_location_names_with_ids([
        "CH5 Bacon Soup 0",
        "CH5 Bacon Soup 1",
        "CH5 Bacon Soup 2",
        "CH5 Bacon Soup 3",
        "CH5 Bacon Soup 4",
        "CH5 Bacon Soup 5",
        "CH5 Bacon Soup 6",
        "CH5 Sammy Lawrence Boss",
        "CH5 Audio Log Office Report",
        "CH5 Audio Log The Big Picture",
        "CH5 Audio Log Chocolate Cake",
        "CH5 Audio Log Thousands of Souls",
        "CH5 Audio Log Bringing Alice to Life",
        "CH5 Audio Log Bendy's End",
        "CH5 Radio",
    ])
    ch5.add_locations(ch5_locations, BATIMLocation)

    # Minigame Sanity
    if world.options.minigame_sanity:
        ch4_minigame_locations = get_location_names_with_ids(["CH4 Bulls Eye", "CH4 Call the Milk Man", "CH4 Wasting Time"])
        ch4_after_book_puzzle.add_locations(ch4_minigame_locations, BATIMLocation)

    # theMeatly Sanity
    if world.options.the_meatly_sanity:
        ch1_basement.add_locations(get_location_names_with_ids(["CH1 theMeatly"]), BATIMLocation)
        ch2_after_valve.add_locations(get_location_names_with_ids(["CH2 theMeatly"]), BATIMLocation)
        ch3_alice_objectives.add_locations(get_location_names_with_ids(["CH3 theMeatly"]), BATIMLocation)
        ch4_intro.add_locations(get_location_names_with_ids(["CH4 theMeatly"]), BATIMLocation)
        ch5.add_locations(get_location_names_with_ids(["CH5 theMeatly"]), BATIMLocation)

    # FIXME Special Options
    # # Locations may be in different regions depending on the player's options.
    # # In our case, the hammer option puts the Top Middle Chest into its own room called Top Middle Room.
    # top_middle_room_locations = get_location_names_with_ids(["Top Middle Chest"])
    # if world.options.hammer:
    #     top_middle_room = world.get_region("Top Middle Room")
    #     top_middle_room.add_locations(top_middle_room_locations, APQuestLocation)
    # else:
    #     overworld.add_locations(top_middle_room_locations, APQuestLocation)
    #
    # # Locations may exist only if the player enables certain options.
    # # In our case, the extra_starting_chest option adds the Bottom Left Extra Chest location.
    # if world.options.extra_starting_chest:
    #     # Once again, it is important to stress that even though the Bottom Left Extra Chest location doesn't always
    #     # exist, it must still always be present in the world's location_name_to_id.
    #     # Whether the location actually exists in the seed is purely determined by whether we create and add it here.
    #     bottom_left_extra_chest = get_location_names_with_ids(["Bottom Left Extra Chest"])
    #     overworld.add_locations(bottom_left_extra_chest, APQuestLocation)


def create_events(world: BATIMWorld) -> None:
    ch5 = world.get_region("CH5")
    ch5.add_event("Beast Bendy Defeated", "Victory", location_type=BATIMLocation, item_type=items.BATIMItem)
