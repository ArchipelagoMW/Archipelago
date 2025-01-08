from copy import deepcopy

from BaseClasses import CollectionState
from worlds.AutoWorld import World


def has_bombs(state: CollectionState, player: int):
    return state.has_group("weapons", player)

def has_candle(state: CollectionState, player: int):
    return state.has_group("candles", player)

def has_power_bracelet(state: CollectionState, player: int):
    return state.has("Power Bracelet", player)

def has_raft(state: CollectionState, player: int):
    return state.has("Raft", player)

def has_recorder(state: CollectionState, player: int):
    return state.has("Recorder", player)

def has_anything(state: CollectionState, player: int):
    return True


overworld_entrances_data = {
    "Screen 01": (has_bombs, "Door Repair"),
    "Screen 03": (has_bombs, "Door Repair"),
    "Screen 04": (has_anything, "Potion Shop"),
    "Screen 05": (has_bombs, "Level 9"),
    "Screen 07": (has_bombs, "Door Repair"),
    "Screen 0A": (has_anything, "White Sword Pond"),
    "Screen 0B": (has_anything, "Level 5"),
    "Screen 0C": (has_anything, "Candle Shop"),
    "Screen 0D": (has_bombs, "Potion Shop"),
    "Screen 0E": (has_anything, "Letter Cave"),
    "Screen 0F": (has_anything, "Secret Money Large"),
    "Screen 10": (has_bombs, "Money Making Game"),
    "Screen 12": (has_bombs, "Shield Shop"),
    "Screen 13": (has_bombs, "Secret Money Medium"),
    "Screen 14": (has_bombs, "Door Repair"),
    "Screen 16": (has_bombs, "Money Making Game"),
    "Screen 1A": (has_anything, "Go Up The Mountain Hint"),
    "Screen 1C": (has_anything, "Secret Is In Tree Hint"),
    "Screen 1D": (has_power_bracelet, "Warp Cave"),
    "Screen 1E": (has_bombs, "Door Repair"),
    "Screen 1F": (has_anything, "Money Making Game"),
    "Screen 21": (has_anything, "Magical Sword Grave"),
    "Screen 22": (has_anything, "Level 6"),
    "Screen 23": (has_power_bracelet, "Warp Cave"),
    "Screen 25": (has_anything, "Arrow Shop"),
    "Screen 26": (has_bombs, "Shield Shop"),
    "Screen 27": (has_bombs, "Potion Shop"),
    "Screen 28": (has_candle, "Secret Money Medium"),
    "Screen 2C": (has_bombs, "Take Any Item"),
    "Screen 2D": (has_bombs, "Secret Money Medium"),
    "Screen 2F": (has_raft, "Take Any Item"),
    "Screen 33": (has_bombs, "Potion Shop"),
    "Screen 34": (has_anything, "Blue Ring Shop"),
    "Screen 37": (has_anything, "Level 1"),
    "Screen 3C": (has_anything, "Level 2"),
    "Screen 3D": (has_anything, "Secret Money Medium"),
    "Screen 42": (has_recorder, "Level 7"),
    "Screen 44": (has_anything, "Arrow Shop"),
    "Screen 45": (has_raft, "Level 4"),
    "Screen 46": (has_candle, "Shield Shop"),
    "Screen 47": (has_candle, "Take Any Item"),
    "Screen 48": (has_candle, "Secret Money Medium"),
    "Screen 49": (has_power_bracelet, "Warp Cave"),
    "Screen 4A": (has_anything, "Arrow Shop"),
    "Screen 4B": (has_candle, "Potion Shop"),
    "Screen 4D": (has_candle, "Shield Shop"),
    "Screen 4E": (has_anything, "Secret Money Small"),
    "Screen 51": (has_candle, "Secret Money Small"),
    "Screen 56": (has_candle, "Secret Money Small"),
    "Screen 5B": (has_candle, "Secret Money Small"),
    "Screen 5E": (has_anything, "Candle Shop"),
    "Screen 62": (has_candle, "Secret Money Large"),
    "Screen 63": (has_candle, "Door Repair"),
    "Screen 64": (has_anything, "Potion Shop"),
    "Screen 66": (has_anything, "Candle Shop"),
    "Screen 67": (has_bombs, "Secret Money Medium"),
    "Screen 68": (has_candle, "Door Repair"),
    "Screen 6A": (has_candle, "Door Repair"),
    "Screen 6B": (has_candle, "Secret Money Large"),
    "Screen 6D": (has_candle, "Level 8"),
    "Screen 6F": (has_anything, "Arrow Shop"),
    "Screen 70": (has_anything, "Lost Woods Hint"),
    "Screen 71": (has_bombs, "Secret Money Medium"),
    "Screen 74": (has_anything, "Level 3"),
    "Screen 75": (has_anything, "Old Man Grave Hint"),
    "Screen 76": (has_bombs, "Money Making Game"),
    "Screen 77": (has_anything, "Starting Sword Cave"),
    "Screen 78": (has_candle, "Potion Shop"),
    "Screen 79": (has_power_bracelet, "Warp Cave"),
    "Screen 7B": (has_bombs, "Take Any Item"),
    "Screen 7C": (has_bombs, "Money Making Game"),
    "Screen 7D": (has_bombs, "Door Repair")

}

dungeon_entrances = [
    "Screen 37", "Screen 3C", "Screen 74", "Screen 45", "Screen 0B", "Screen 22", "Screen 42", "Screen 6D", "Screen 05"
]

major_entrances = [  # Dungeon entrances, major item locations, take any caves.
    *dungeon_entrances, "Screen 0A", "Screen 0E", "Screen 21", "Screen 77",
    "Screen 47", "Screen 2C", "Screen 2F", "Screen 7B"
]

warp_caves = [
    "Screen 1D", "Screen 23", "Screen 49", "Screen 79"
]

open_entrances = [
    "Screen 04", "Screen 0A", "Screen 0B", "Screen 0C", "Screen 0E", "Screen 0F", "Screen 1A", "Screen 1C", "Screen 1F",
    "Screen 21", "Screen 22", "Screen 25", "Screen 34", "Screen 37", "Screen 3C", "Screen 3D", "Screen 44", "Screen 4A",
    "Screen 4E", "Screen 5E", "Screen 64", "Screen 66", "Screen 6F", "Screen 70", "Screen 74", "Screen 75", "Screen 77"
]

all_entrances = overworld_entrances_data.keys()

overworld_regions = {  # These are not AP Regions (tm). They're for regional entrance shuffle.
    "Death Mountain West": ["Screen 01", "Screen 02", "Screen 03", "Screen 04", "Screen 05", "Screen 07", "Screen 10",
                            "Screen 12", "Screen 13", "Screen 14", "Screen 16"],
    "Death Mountain East": ["Screen 0A", "Screen 0B", "Screen 0C", "Screen 0D", "Screen 0E", "Screen 0F", "Screen 1A",
                            "Screen 1C", "Screen 1D", "Screen 1E", "Screen 1F", "Screen 2C"],
    "Shoreline": ["Screen 0E", "Screen 0F", "Screen 1E", "Screen 1F", "Screen 2D", "Screen 2F", "Screen 6F",
                  "Screen 7B", "Screen 7C", "Screen 7D"],
    "Graveyard Foothills": ["Screen 21", "Screen 22", "Screen 23", "Screen 25", "Screen 26", "Screen 33", "Screen 70",
                            "Screen 71"],
    "Lost Woods": ["Screen 42", "Screen 51", "Screen 62", "Screen 63", "Screen 70", "Screen 71", "Screen 74"],
    "Southern Lowlands": ["Screen 56", "Screen 64", "Screen 66", "Screen 67", "Screen 68", "Screen 74", "Screen 75",
                          "Screen 76", "Screen 77", "Screen 78", "Screen 79"],
    "Lake Hylia": ["Screen 26", "Screen 28", "Screen 34", "Screen 37", "Screen 44", "Screen 45", "Screen 46",
                   "Screen 47", "Screen 48", "Screen 56",],
    "Eastern Forest": ["Screen 49", "Screen 4A", "Screen 4B", "Screen 4D", "Screen 4E", "Screen 5B", "Screen 5E",
                       "Screen 6A", "Screen 6B", "Screen 6D"]
}

def should_shuffle_warp_cave(screen, world: World):
    if world.options.RandomizeWarpCaves == True:
        return True
    elif screen in warp_caves:
        return False
    else:
        return True

def create_entrance_randomizer_set(world: World):
    overworld_entrances = deepcopy(overworld_entrances_data)
    screens = []
    destinations = []
    shuffled_entrances = []
    if world.options.EntranceShuffle.value == 0:
        return overworld_entrances
    elif world.options.EntranceShuffle.value == 1:
        shuffled_entrances = [*dungeon_entrances]
    elif world.options.EntranceShuffle.value == 2:
        shuffled_entrances = [*major_entrances]
    elif world.options.EntranceShuffle.value == 3:
        shuffled_entrances = [*open_entrances]
    elif world.options.EntranceShuffle.value == 4:
        shuffled_entrances = list({*major_entrances, *open_entrances})
    elif world.options.EntranceShuffle.value == 5:
        shuffled_entrances = [*all_entrances]
    if world.options.RandomizeWarpCaves == True:
        shuffled_entrances.extend(warp_caves)
    shuffled_entrances = sorted(shuffled_entrances)
    screens = [screen for screen in overworld_entrances.keys()
                   if screen in shuffled_entrances and should_shuffle_warp_cave(screen, world)]
    destinations = [data[1] for screen, data in overworld_entrances.items()
                    if screen in shuffled_entrances and should_shuffle_warp_cave(screen, world)]

    world.random.shuffle(screens)
    world.random.shuffle(destinations)
    new_destinations = {screen[0]: screen[1] for screen in zip(screens, destinations)}
    for screen, destination in new_destinations.items():
        overworld_entrances[screen] = (overworld_entrances[screen][0], destination)
    starting_sword_cave = [screen for screen, dest in overworld_entrances.items() if dest[1] == "Starting Sword Cave"][0]

    while starting_sword_cave not in open_entrances and world.options.EntranceShuffle.value in [2, 4, 5]:
        world.random.shuffle(screens)
        world.random.shuffle(destinations)
        new_destinations = {screen[0]: screen[1] for screen in zip(screens, destinations)}
        for screen, destination in new_destinations.items():
            overworld_entrances[screen] = (overworld_entrances[screen][0], destination)
        starting_sword_cave = [screen for screen, dest in overworld_entrances.items() if dest[1] == "Starting Sword Cave"][0]

    return overworld_entrances
