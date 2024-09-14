from random import Random
from typing import List, Tuple, Dict, Optional, Callable

from BaseClasses import Location, LocationProgressType, Region
from .options import max_shapesanity

location_description = {  # TODO give at least some locations a description
    "Level 1": "TODO",
    "Level 1 Additional": "TODO",
    "Level 20 Additional": "TODO",
    "Level 20 Additional 2": "TODO",
    "Level 26": "TODO",
    "Level 1000": "TODO",
    "Belt Upgrade Tier II": "TODO",
    "Miner Upgrade Tier II": "TODO",
    "Processors Upgrade Tier II": "TODO",
    "Painting Upgrade Tier II": "TODO",
    "Belt Upgrade Tier VIII": "TODO",
    "Miner Upgrade Tier VIII": "TODO",
    "Processors Upgrade Tier VIII": "TODO",
    "Painting Upgrade Tier VIII": "TODO",
    "Belt Upgrade Tier M": "TODO",
    "Miner Upgrade Tier M": "TODO",
    "Processors Upgrade Tier M": "TODO",
    "Painting Upgrade Tier M": "TODO"
}

categories = ["Belt", "Miner", "Processors", "Painting"]

translate: List[Tuple[int, str]] = [
    (1000, "M"),
    (900, "CM"),
    (500, "D"),
    (400, "CD"),
    (100, "C"),
    (90, "XC"),
    (50, "L"),
    (40, "XL"),
    (10, "X"),
    (9, "IX"),
    (5, "V"),
    (4, "IV"),
    (1, "I")
]


def roman(num: int) -> str:
    """Converts positive integers into roman numbers."""
    rom: str = ""
    for key, val in translate:
        while num >= key:
            rom += val
            num -= key
    return rom


def color_to_needed_building(color_list: List[str]) -> str:
    for next_color in color_list:
        if next_color in ["Yellow", "Purple", "Cyan", "White", "y", "p", "c", "w"]:
            return "Mixed"
    for next_color in color_list:
        if next_color not in ["Uncolored", "u"]:
            return "Painted"
    return "Uncolored"


shapesanity_simple: Dict[str, str] = {}
shapesanity_1_4: Dict[str, str] = {}
shapesanity_two_sided: Dict[str, str] = {}
shapesanity_three_parts: Dict[str, str] = {}
shapesanity_four_parts: Dict[str, str] = {}

achievement_locations: List[str] = ["My eyes no longer hurt", "Painter", "Cutter", "Rotater", "Wait, they stack?",
                                    "Wires", "Storage", "Freedom", "The logo!", "To the moon", "It's piling up",
                                    "I'll use it later", "Efficiency 1", "Preparing to launch", "SpaceY",
                                    "Stack overflow", "It's a mess", "Faster", "Even faster", "Get rid of them",
                                    "It's been a long time", "Addicted", "Can't stop", "Is this the end?",
                                    "Getting into it", "Now it's easy", "Computer Guy", "Speedrun Master",
                                    "Speedrun Novice", "Not an idle game", "Efficiency 2", "Branding specialist 1",
                                    "Branding specialist 2", "King of Inefficiency", "It's so slow",
                                    "MAM (Make Anything Machine)", "Perfectionist", "The next dimension", "Oops",
                                    "Copy-Pasta", "I've seen that before ...", "Memories from the past",
                                    "I need trains", "A bit early?", "GPS"]

all_locations: List[str] = (["Level 1 Additional", "Level 20 Additional", "Level 20 Additional 2"]
                            + [f"Level {x}" for x in range(1, 500)]
                            + [f"{cat} Upgrade Tier {roman(x)}" for cat in categories for x in range(2, 501)]
                            + achievement_locations
                            + [f"Shapesanity {x}" for x in range(1, max_shapesanity+1)])


def addlevels(maxlevel: int, logictype: str,
              random_logic_phase_length: List[int]) -> Dict[str, Tuple[str, LocationProgressType]]:
    """Returns a dictionary with all level locations based on player options (maxlevel INCLUDED).
    If shape requirements are not randomized, give logic type 0."""

    # Level 1 is always directly accessible
    locations: Dict[str, Tuple[str, LocationProgressType]] = {"Level 1": ("Main", LocationProgressType.PRIORITY),
                                                              "Level 1 Additional": (
                                                              "Main", LocationProgressType.PRIORITY)}

    if logictype.startswith("vanilla"):
        locations["Level 20 Additional"] = ("Levels with 5 Buildings", LocationProgressType.DEFAULT)
        locations["Level 20 Additional 2"] = ("Levels with 5 Buildings", LocationProgressType.DEFAULT)
        locations["Level 2"] = ("Levels with 1 Building", LocationProgressType.DEFAULT)
        locations["Level 3"] = ("Levels with 1 Building", LocationProgressType.DEFAULT)
        locations["Level 4"] = ("Levels with 1 Building", LocationProgressType.DEFAULT)
        locations["Level 5"] = ("Levels with 2 Buildings", LocationProgressType.DEFAULT)
        locations["Level 6"] = ("Levels with 2 Buildings", LocationProgressType.DEFAULT)
        locations["Level 7"] = ("Levels with 3 Buildings", LocationProgressType.DEFAULT)
        locations["Level 8"] = ("Levels with 3 Buildings", LocationProgressType.DEFAULT)
        locations["Level 9"] = ("Levels with 4 Buildings", LocationProgressType.DEFAULT)
        locations["Level 10"] = ("Levels with 4 Buildings", LocationProgressType.DEFAULT)
        for x in range(11, maxlevel+1):
            locations[f"Level {x}"] = ("Levels with 5 Buildings", LocationProgressType.DEFAULT)

    elif logictype.startswith("stretched"):
        phaselength = maxlevel//6
        l20phase = 20//phaselength
        if l20phase == 0:
            locations["Level 20 Additional"] = ("Main", LocationProgressType.DEFAULT)
            locations["Level 20 Additional 2"] = ("Main", LocationProgressType.DEFAULT)
        elif l20phase == 1:
            locations["Level 20 Additional"] = ("Levels with 1 Building", LocationProgressType.DEFAULT)
            locations["Level 20 Additional 2"] = ("Levels with 1 Building", LocationProgressType.DEFAULT)
        else:
            locations["Level 20 Additional"] = (f"Levels with {min(l20phase, 5)} Buildings",
                                                LocationProgressType.DEFAULT)
            locations["Level 20 Additional 2"] = (f"Levels with {min(l20phase, 5)} Buildings",
                                                  LocationProgressType.DEFAULT)
        for x in range(2, phaselength):
            locations[f"Level {x}"] = ("Main", LocationProgressType.DEFAULT)
        for x in range(phaselength, phaselength*2):
            locations[f"Level {x}"] = ("Levels with 1 Building", LocationProgressType.DEFAULT)
        for x in range(phaselength*2, phaselength*3):
            locations[f"Level {x}"] = ("Levels with 2 Buildings", LocationProgressType.DEFAULT)
        for x in range(phaselength*3, phaselength*4):
            locations[f"Level {x}"] = ("Levels with 3 Buildings", LocationProgressType.DEFAULT)
        for x in range(phaselength*4, phaselength*5):
            locations[f"Level {x}"] = ("Levels with 4 Buildings", LocationProgressType.DEFAULT)
        for x in range(phaselength*5, maxlevel+1):
            locations[f"Level {x}"] = ("Levels with 5 Buildings", LocationProgressType.DEFAULT)

    elif logictype.startswith("quick"):
        locations["Level 20 Additional"] = ("Levels with 5 Buildings", LocationProgressType.DEFAULT)
        locations["Level 20 Additional 2"] = ("Levels with 5 Buildings", LocationProgressType.DEFAULT)
        locations["Level 2"] = ("Levels with 1 Building", LocationProgressType.DEFAULT)
        locations["Level 3"] = ("Levels with 2 Buildings", LocationProgressType.DEFAULT)
        locations["Level 4"] = ("Levels with 3 Buildings", LocationProgressType.DEFAULT)
        locations["Level 5"] = ("Levels with 4 Buildings", LocationProgressType.DEFAULT)
        for x in range(6, maxlevel+1):
            locations[f"Level {x}"] = ("Levels with 5 Buildings", LocationProgressType.DEFAULT)

    elif logictype.startswith("random_steps"):
        nextlevel = 2
        l20set = False
        for _ in range(0, random_logic_phase_length[0]):
            locations[f"Level {nextlevel}"] = ("Main", LocationProgressType.DEFAULT)
            nextlevel += 1
        if nextlevel > 20 and not l20set:
            locations["Level 20 Additional"] = ("Main", LocationProgressType.DEFAULT)
            locations["Level 20 Additional 2"] = ("Main", LocationProgressType.DEFAULT)
            l20set = True
        for _ in range(0, random_logic_phase_length[1]):
            locations[f"Level {nextlevel}"] = ("Levels with 1 Building", LocationProgressType.DEFAULT)
            nextlevel += 1
        if nextlevel > 20 and not l20set:
            locations["Level 20 Additional"] = ("Levels with 1 Building", LocationProgressType.DEFAULT)
            locations["Level 20 Additional 2"] = ("Levels with 1 Building", LocationProgressType.DEFAULT)
            l20set = True
        for _ in range(0, random_logic_phase_length[2]):
            locations[f"Level {nextlevel}"] = ("Levels with 2 Buildings", LocationProgressType.DEFAULT)
            nextlevel += 1
        if nextlevel > 20 and not l20set:
            locations["Level 20 Additional"] = ("Levels with 2 Buildings", LocationProgressType.DEFAULT)
            locations["Level 20 Additional 2"] = ("Levels with 2 Buildings", LocationProgressType.DEFAULT)
            l20set = True
        for _ in range(0, random_logic_phase_length[3]):
            locations[f"Level {nextlevel}"] = ("Levels with 3 Buildings", LocationProgressType.DEFAULT)
            nextlevel += 1
        if nextlevel > 20 and not l20set:
            locations["Level 20 Additional"] = ("Levels with 3 Buildings", LocationProgressType.DEFAULT)
            locations["Level 20 Additional 2"] = ("Levels with 3 Buildings", LocationProgressType.DEFAULT)
            l20set = True
        for _ in range(0, random_logic_phase_length[4]):
            locations[f"Level {nextlevel}"] = ("Levels with 4 Buildings", LocationProgressType.DEFAULT)
            nextlevel += 1
        if nextlevel > 20 and not l20set:
            locations["Level 20 Additional"] = ("Levels with 4 Buildings", LocationProgressType.DEFAULT)
            locations["Level 20 Additional 2"] = ("Levels with 4 Buildings", LocationProgressType.DEFAULT)
            l20set = True
        for x in range(nextlevel, maxlevel+1):
            locations[f"Level {x}"] = ("Levels with 5 Buildings", LocationProgressType.DEFAULT)
        if not l20set:
            locations["Level 20 Additional"] = ("Levels with 5 Buildings", LocationProgressType.DEFAULT)
            locations["Level 20 Additional 2"] = ("Levels with 5 Buildings", LocationProgressType.DEFAULT)

    else:  # logictype == hardcore
        locations["Level 20 Additional"] = ("Levels with 5 Buildings", LocationProgressType.DEFAULT)
        locations["Level 20 Additional 2"] = ("Levels with 5 Buildings", LocationProgressType.DEFAULT)
        for x in range(2, maxlevel+1):
            locations[f"Level {x}"] = ("Levels with 5 Buildings", LocationProgressType.DEFAULT)

    return locations


def addupgrades(finaltier: int, logictype: str,
                category_random_logic_amounts: Dict[str, int]) -> Dict[str, Tuple[str, LocationProgressType]]:
    """Returns a dictionary with all upgrade locations based on player options (finaltier INCLUDED).
    If shape requirements are not randomized, give logic type 0."""

    locations: Dict[str, Tuple[str, LocationProgressType]] = {}

    if logictype == "vanilla_like":
        locations["Belt Upgrade Tier II"] = ("Main", LocationProgressType.DEFAULT)
        locations["Miner Upgrade Tier II"] = ("Main", LocationProgressType.DEFAULT)
        locations["Processors Upgrade Tier II"] = ("Main", LocationProgressType.DEFAULT)
        locations["Painting Upgrade Tier II"] = ("Upgrades with 3 Buildings", LocationProgressType.DEFAULT)
        locations["Belt Upgrade Tier III"] = ("Upgrades with 2 Buildings", LocationProgressType.DEFAULT)
        locations["Miner Upgrade Tier III"] = ("Upgrades with 2 Buildings", LocationProgressType.DEFAULT)
        locations["Processors Upgrade Tier III"] = ("Upgrades with 1 Building", LocationProgressType.DEFAULT)
        locations["Painting Upgrade Tier III"] = ("Upgrades with 3 Buildings", LocationProgressType.DEFAULT)
        for x in range(4, finaltier+1):
            for cat in categories:
                locations[f"{cat} Upgrade Tier {roman(x)}"] = ("Upgrades with 5 Buildings",
                                                               LocationProgressType.DEFAULT)
    elif logictype == "linear":
        for cat in categories:
            locations[f"{cat} Upgrade Tier II"] = ("Main", LocationProgressType.DEFAULT)
        for cat in categories:
            locations[f"{cat} Upgrade Tier III"] = ("Upgrades with 1 Building", LocationProgressType.DEFAULT)
        for x in range(4, 7):
            for cat in categories:
                locations[f"{cat} Upgrade Tier {roman(x)}"] = (f"Upgrades with {x-2} Buildings",
                                                               LocationProgressType.DEFAULT)
        for x in range(7, finaltier+1):
            for cat in categories:
                locations[f"{cat} Upgrade Tier {roman(x)}"] = ("Upgrades with 5 Buildings",
                                                               LocationProgressType.DEFAULT)

    elif logictype == "category":
        for x in range(2, 5):
            locations[f"Belt Upgrade Tier {roman(x)}"] = ("Main", LocationProgressType.DEFAULT)
        for x in range(5, finaltier+1):
            locations[f"Belt Upgrade Tier {roman(x)}"] = ("Upgrades with 5 Buildings", LocationProgressType.DEFAULT)
        for x in range(2, 5):
            locations[f"Miner Upgrade Tier {roman(x)}"] = ("Main", LocationProgressType.DEFAULT)
        for x in range(5, finaltier+1):
            locations[f"Miner Upgrade Tier {roman(x)}"] = ("Upgrades with 5 Buildings", LocationProgressType.DEFAULT)
        locations["Processors Upgrade Tier II"] = ("Upgrades with 1 Building", LocationProgressType.DEFAULT)
        locations["Processors Upgrade Tier III"] = ("Upgrades with 1 Building", LocationProgressType.DEFAULT)
        locations["Processors Upgrade Tier IV"] = ("Upgrades with 2 Buildings", LocationProgressType.DEFAULT)
        locations["Processors Upgrade Tier V"] = ("Upgrades with 2 Buildings", LocationProgressType.DEFAULT)
        locations["Processors Upgrade Tier VI"] = ("Upgrades with 3 Buildings", LocationProgressType.DEFAULT)
        for x in range(7, finaltier+1):
            locations[f"Processors Upgrade Tier {roman(x)}"] = ("Upgrades with 5 Buildings",
                                                                LocationProgressType.DEFAULT)
        locations["Painting Upgrade Tier II"] = ("Upgrades with 4 Buildings", LocationProgressType.DEFAULT)
        locations["Painting Upgrade Tier III"] = ("Upgrades with 4 Buildings", LocationProgressType.DEFAULT)
        locations["Painting Upgrade Tier IV"] = ("Upgrades with 4 Buildings", LocationProgressType.DEFAULT)
        for x in range(5, finaltier+1):
            locations[f"Painting Upgrade Tier {roman(x)}"] = ("Upgrades with 5 Buildings", LocationProgressType.DEFAULT)

    elif logictype == "category_random":
        regions = ["Main", "Upgrades with 1 Building", "Upgrades with 2 Buildings", "Upgrades with 3 Buildings",
                   "Upgrades with 4 Buildings", "Upgrades with 5 Buildings"]
        for x in range(2, 5):
            locations[f"Belt Upgrade Tier {roman(x)}"] = (regions[category_random_logic_amounts["belt"]],
                                                          LocationProgressType.DEFAULT)
        for x in range(5, finaltier+1):
            locations[f"Belt Upgrade Tier {roman(x)}"] = ("Upgrades with 5 Buildings",
                                                          LocationProgressType.DEFAULT)
        for x in range(2, 5):
            locations[f"Miner Upgrade Tier {roman(x)}"] = (regions[category_random_logic_amounts["miner"]],
                                                           LocationProgressType.DEFAULT)
        for x in range(5, finaltier+1):
            locations[f"Miner Upgrade Tier {roman(x)}"] = ("Upgrades with 5 Buildings",
                                                           LocationProgressType.DEFAULT)
        for x in range(2, 5):
            locations[f"Processors Upgrade Tier {roman(x)}"] = (regions[category_random_logic_amounts["processors"]],
                                                                LocationProgressType.DEFAULT)
        for x in range(5, finaltier+1):
            locations[f"Processors Upgrade Tier {roman(x)}"] = ("Upgrades with 5 Buildings",
                                                                LocationProgressType.DEFAULT)
        for x in range(2, 5):
            locations[f"Painting Upgrade Tier {roman(x)}"] = (regions[category_random_logic_amounts["painting"]],
                                                              LocationProgressType.DEFAULT)
        for x in range(5, finaltier+1):
            locations[f"Painting Upgrade Tier {roman(x)}"] = ("Upgrades with 5 Buildings",
                                                              LocationProgressType.DEFAULT)

    else:  # logictype == hardcore
        for cat in categories:
            locations[f"{cat} Upgrade Tier II"] = ("Main", LocationProgressType.DEFAULT)
        for x in range(3, finaltier+1):
            for cat in categories:
                locations[f"{cat} Upgrade Tier {roman(x)}"] = ("Upgrades with 5 Buildings",
                                                               LocationProgressType.DEFAULT)

    return locations


def addachievements(excludesoftlock: bool, excludelong: bool, excludeprogressive: bool,
                    maxlevel: int, upgradelogictype: str, category_random_logic_amounts: Dict[str, int],
                    goal: str, presentlocations: Dict[str, Tuple[str, LocationProgressType]]) \
                    -> Dict[str, Tuple[str, LocationProgressType]]:
    """Returns a dictionary with all achievement locations based on player options."""

    locations: Dict[str, Tuple[str, LocationProgressType]] = dict()

    locations["My eyes no longer hurt"] = ("Menu", LocationProgressType.DEFAULT)
    locations["Painter"] = ("Painted Shape Achievements", LocationProgressType.DEFAULT)
    locations["Cutter"] = ("Cut Shape Achievements", LocationProgressType.DEFAULT)
    locations["Rotater"] = ("Rotated Shape Achievements", LocationProgressType.DEFAULT)
    locations["Wait, they stack?"] = ("Stacked Shape Achievements", LocationProgressType.DEFAULT)
    locations["Storage"] = ("Stored Shape Achievements", LocationProgressType.DEFAULT)
    locations["The logo!"] = ("All Buildings Shapes", LocationProgressType.DEFAULT)
    locations["To the moon"] = ("All Buildings Shapes", LocationProgressType.DEFAULT)
    locations["It's piling up"] = ("All Buildings Shapes", LocationProgressType.DEFAULT)
    locations["I'll use it later"] = ("All Buildings Shapes", LocationProgressType.DEFAULT)
    locations["Efficiency 1"] = ("All Buildings Shapes", LocationProgressType.DEFAULT)
    locations["Preparing to launch"] = ("All Buildings Shapes", LocationProgressType.DEFAULT)
    locations["SpaceY"] = ("All Buildings Shapes", LocationProgressType.DEFAULT)
    locations["Stack overflow"] = ("Stacked Shape Achievements", LocationProgressType.DEFAULT)
    locations["It's a mess"] = ("Main", LocationProgressType.DEFAULT)
    locations["Even faster"] = ("Upgrades with 5 Buildings", LocationProgressType.DEFAULT)
    locations["Get rid of them"] = ("Trashed Shape Achievements", LocationProgressType.DEFAULT)
    locations["Getting into it"] = ("Menu", LocationProgressType.DEFAULT)
    locations["Now it's easy"] = ("Blueprint Achievements", LocationProgressType.DEFAULT)
    locations["Computer Guy"] = ("Wiring Achievements", LocationProgressType.DEFAULT)
    locations["Efficiency 2"] = ("All Buildings Shapes", LocationProgressType.DEFAULT)
    locations["Branding specialist 1"] = ("All Buildings Shapes", LocationProgressType.DEFAULT)
    locations["Branding specialist 2"] = ("All Buildings Shapes", LocationProgressType.DEFAULT)
    locations["Perfectionist"] = ("Main", LocationProgressType.DEFAULT)
    locations["The next dimension"] = ("Wiring Achievements", LocationProgressType.DEFAULT)
    locations["Oops"] = ("Main", LocationProgressType.DEFAULT)
    locations["Copy-Pasta"] = ("Blueprint Achievements", LocationProgressType.DEFAULT)
    locations["I've seen that before ..."] = ("All Buildings Shapes", LocationProgressType.DEFAULT)
    locations["Memories from the past"] = ("All Buildings Shapes", LocationProgressType.DEFAULT)
    locations["I need trains"] = ("Main", LocationProgressType.DEFAULT)
    locations["GPS"] = ("Menu", LocationProgressType.DEFAULT)
    # Achievements that depend on upgrades
    if upgradelogictype == "linear":
        locations["Faster"] = ("Upgrades with 3 Buildings", LocationProgressType.DEFAULT)
    elif upgradelogictype == "category_random":
        maxneededbuildings = max(category_random_logic_amounts["belt"], category_random_logic_amounts["miner"],
                                 category_random_logic_amounts["processors"], category_random_logic_amounts["painting"])
        if maxneededbuildings == 0:
            locations["Faster"] = ("Main", LocationProgressType.DEFAULT)
        elif maxneededbuildings == 1:
            locations["Faster"] = ("Upgrades with 1 Building", LocationProgressType.DEFAULT)
        else:
            locations["Faster"] = (f"Upgrades with {maxneededbuildings} Buildings", LocationProgressType.DEFAULT)
    else:
        locations["Faster"] = ("Upgrades with 5 Buildings", LocationProgressType.DEFAULT)
    # Achievements that depend on the level
    locations["Wires"] = (presentlocations["Level 20"][0], LocationProgressType.DEFAULT)
    if not goal == "vanilla":
        locations["Freedom"] = (presentlocations["Level 26"][0], LocationProgressType.DEFAULT)
        locations["MAM (Make Anything Machine)"] = ("MAM needed", LocationProgressType.DEFAULT)
    if maxlevel >= 50:
        locations["Can't stop"] = (presentlocations["Level 50"][0], LocationProgressType.DEFAULT)
    elif not goal == "vanilla":
        locations["Can't stop"] = ("Levels with 5 Buildings", LocationProgressType.DEFAULT)
    if maxlevel >= 100:
        locations["Is this the end?"] = (presentlocations["Level 100"][0], LocationProgressType.DEFAULT)
    elif not goal == "vanilla":
        locations["Is this the end?"] = ("Levels with 5 Buildings", LocationProgressType.DEFAULT)

    if excludeprogressive:
        unreasonable_type = LocationProgressType.EXCLUDED
    else:
        unreasonable_type = LocationProgressType.DEFAULT

    if not excludesoftlock:
        locations["Speedrun Master"] = (presentlocations["Level 12"][0], unreasonable_type)
        locations["Speedrun Novice"] = (presentlocations["Level 12"][0], unreasonable_type)
        locations["Not an idle game"] = (presentlocations["Level 12"][0], unreasonable_type)
        locations["It's so slow"] = (presentlocations["Level 12"][0], unreasonable_type)
        locations["King of Inefficiency"] = (presentlocations["Level 14"][0], unreasonable_type)
        locations["A bit early?"] = ("All Buildings Shapes", unreasonable_type)

    if not excludelong:
        locations["It's been a long time"] = ("Menu", unreasonable_type)
        locations["Addicted"] = ("Menu", unreasonable_type)

    return locations


def addshapesanity(amount: int, random: Random,
                   append_shapesanity: Callable[[str],None]) -> Dict[str, Tuple[str, LocationProgressType]]:
    """Returns a dictionary with a given number of random shapesanity locations."""

    included_shapes: Dict[str, Tuple[str, LocationProgressType]] = {}
    shapes_list = list(shapesanity_simple.items())
    # Always have at least 4 shapesanity checks because of sphere 1 usefulls + both hardcore logic
    included_shapes[f"Shapesanity 1"] = ("Shapesanity Full Uncolored", LocationProgressType.DEFAULT)
    included_shapes[f"Shapesanity 2"] = ("Shapesanity Full Uncolored", LocationProgressType.DEFAULT)
    included_shapes[f"Shapesanity 3"] = ("Shapesanity Full Uncolored", LocationProgressType.DEFAULT)
    included_shapes[f"Shapesanity 4"] = ("Shapesanity East Windmill Uncolored", LocationProgressType.DEFAULT)
    append_shapesanity(f"Uncolored Circle")
    append_shapesanity(f"Uncolored Star")
    append_shapesanity(f"Uncolored Square")
    append_shapesanity(f"Uncolored Windmill")
    shapes_list.remove((f"Uncolored Circle", "Shapesanity Full Uncolored"))
    shapes_list.remove((f"Uncolored Star", "Shapesanity Full Uncolored"))
    shapes_list.remove((f"Uncolored Square", "Shapesanity Full Uncolored"))
    shapes_list.remove((f"Uncolored Windmill", "Shapesanity East Windmill Uncolored"))
    switched = 0
    for counting in range(5, amount+1):
        if switched == 0 and (len(shapes_list) == 0 or counting == amount//2):
            shapes_list = list(shapesanity_1_4.items())
            switched = 1
        if switched == 1 and (len(shapes_list) == 0 or counting == amount*7//12):
            shapes_list = list(shapesanity_two_sided.items())
            switched = 2
        if switched == 2 and (len(shapes_list) == 0 or counting == amount*5//6):
            shapes_list = list(shapesanity_three_parts.items())
            switched = 3
        if switched == 3 and (len(shapes_list) == 0 or counting == amount*11//12):
            shapes_list = list(shapesanity_four_parts.items())
            switched = 4
        x = random.randint(0, len(shapes_list)-1)
        next_shape = shapes_list.pop(x)
        included_shapes[f"Shapesanity {counting}"] = (next_shape[1], LocationProgressType.DEFAULT)
        append_shapesanity(next_shape[0])

    return included_shapes


def addshapesanity_ut(shapesanity_names: List[str]) -> Dict[str, Tuple[str, LocationProgressType]]:
    """Returns the same information as addshapesanity but will add specific values based on a UT rebuild"""

    included_shapes: Dict[str, Tuple[str, LocationProgressType]] = {}

    for name in shapesanity_names:
        for options in [shapesanity_simple, shapesanity_1_4, shapesanity_two_sided,
                        shapesanity_three_parts, shapesanity_four_parts]:
            if name in options:
                next_shape = options[name]
                break
        else:
            raise ValueError(f"Could not find shapesanity name {name}")
        included_shapes[f"Shapesanity {len(included_shapes)}"] = (next_shape, LocationProgressType.DEFAULT)
    return included_shapes


class ShapezLocation(Location):
    game = "shapez"

    def __init__(self, player: int, name: str, address: Optional[int], region: Region,
                 progress_type: LocationProgressType):
        super(ShapezLocation, self).__init__(player, name, address, region)
        self.progress_type = progress_type
