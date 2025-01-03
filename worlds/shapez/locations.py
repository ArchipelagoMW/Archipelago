from random import Random
from typing import List, Tuple, Dict, Optional, Callable

from BaseClasses import Location, LocationProgressType, Region
from .options import max_shapesanity, max_levels_and_upgrades

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
    """Converts positive non-zero integers into roman numbers."""
    rom: str = ""
    for key, val in translate:
        while num >= key:
            rom += val
            num -= key
    return rom


location_description = {
    "Level 1": "Levels are completed by delivering certain shapes in certain amounts to the hub. The required shape "
               "and amount for the current level are always displayed on the hub.",
    "Level 1 Additional": "In the vanilla game, levels 1 and 20 have unlock more than one building.",
    "Level 20 Additional": "In the vanilla game, levels 1 and 20 have unlock more than one building.",
    "Level 20 Additional 2": "In the vanilla game, levels 1 and 20 have unlock more than one building.",
    "Level 26": "In the vanilla game, level 26 is the final level of the tutorial, unlocking freeplay.",
    f"Level {max_levels_and_upgrades-1}": "This is the highest possible level that can contains an item, if your goal "
                                          "is set to \"mam\"",
    "Belt Upgrade Tier II": "Upgrades can be purchased by having certain shapes in certain amounts stored in your hub. "
                            "This is the first upgrade in the belt, balancers, and tunnel category.",
    "Miner Upgrade Tier II": "Upgrades can be purchased by having certain shapes in certain amounts stored in your "
                             "hub. This is the first upgrade in the extractor category.",
    "Processors Upgrade Tier II": "Upgrades can be purchased by having certain shapes in certain amounts stored in "
                                  "your hub. This is the first upgrade in the cutter, rotators, and stacker category.",
    "Painting Upgrade Tier II": "Upgrades can be purchased by having certain shapes in certain amounts stored in your "
                                "hub. This is the first upgrade in the painters and color mixer category.",
    "Belt Upgrade Tier VIII": "This is the final upgrade in the belt, balancers, and tunnel category, if your goal is "
                              "**not** set to \"even_fasterer\".",
    "Miner Upgrade Tier VIII": "This is the final upgrade in the extractor category, if your goal is **not** set to "
                               "\"even_fasterer\".",
    "Processors Upgrade Tier VIII": "This is the final upgrade in the cutter, rotators, and stacker category, if your "
                                    "goal is **not** set to \"even_fasterer\".",
    "Painting Upgrade Tier VIII": "This is the final upgrade in the painters and color mixer category, if your goal is "
                                  "**not** set to \"even_fasterer\".",
    f"Belt Upgrade Tier {roman(max_levels_and_upgrades)}": "This is the highest possible upgrade in the belt, "
                                                           "balancers, and tunnel category, if your goal is set to "
                                                           "\"even_fasterer\".",
    f"Miner Upgrade Tier {roman(max_levels_and_upgrades)}": "This is the highest possible upgrade in the extractor "
                                                            "category, if your goal is set to \"even_fasterer\".",
    f"Processors Upgrade Tier {roman(max_levels_and_upgrades)}": "This is the highest possible upgrade in the cutter, "
                                                                 "rotators, and stacker category, if your goal is set "
                                                                 "to \"even_fasterer\".",
    f"Painting Upgrade Tier {roman(max_levels_and_upgrades)}": "This is the highest possible upgrade in the painters "
                                                               "and color mixer category, if your goal is set to "
                                                               "\"even_fasterer\".",
    "My eyes no longer hurt": "This is an achievement, that is unlocked by activating dark mode.",
    "Painter": "This is an achievement, that is unlocked by painting a shape using the painter or double painter.",
    "Cutter": "This is an achievement, that is unlocked by cutting a shape in half using the cutter.",
    "Rotater": "This is an achievement, that is unlocked by rotating a shape clock wise.",
    "Wait, they stack?": "This is an achievement, that is unlocked by stacking two shapes on top of each other.",
    "Wires": "This is an achievement, that is unlocked by completing level 20.",
    "Storage": "This is an achievement, that is unlocked by storing a shape in a storage.",
    "Freedom": "This is an achievement, that is unlocked by completing level 20. It is only included if the goal is "
               "**not** set to vanilla.",
    "The logo!": "This is an achievement, that is unlocked by producing the logo of the game.",
    "To the moon": "This is an achievement, that is unlocked by producing the rocket shape.",
    "It's piling up": "This is an achievement, that is unlocked by having 100.000 blueprint shapes stored in the hub.",
    "I'll use it later": "This is an achievement, that is unlocked by having one million blueprint shapes stored in "
                         "the hub.",
    "Efficiency 1": "This is an achievement, that is unlocked by delivering 25 blueprint shapes per second to the hub.",
    "Preparing to launch": "This is an achievement, that is unlocked by delivering 10 rocket shapes per second to the "
                           "hub.",
    "SpaceY": "This is an achievement, that is unlocked by 20 rocket shapes per second to the hub.",
    "Stack overflow": "This is an achievement, that is unlocked by stacking 4 layers on top of each other.",
    "It's a mess": "This is an achievement, that is unlocked by having 100 different shapes stored in the hub.",
    "Faster": "This is an achievement, that is unlocked by upgrading everything to at least tier V.",
    "Even faster": "This is an achievement, that is unlocked by upgrading everything to at least tier VIII.",
    "Get rid of them": "This is an achievement, that is unlocked by transporting 1000 shapes into a trash can.",
    "It's been a long time": "This is an achievement, that is unlocked by playing your save file for 10 hours "
                             "(combined playtime).",
    "Addicted": "This is an achievement, that is unlocked by playing your save file for 20 hours (combined playtime).",
    "Can't stop": "This is an achievement, that is unlocked by reaching level 50.",
    "Is this the end?": "This is an achievement, that is unlocked by reaching level 100.",
    "Getting into it": "This is an achievement, that is unlocked by playing your save file for 1 hour (combined "
                       "playtime).",
    "Now it's easy": "This is an achievement, that is unlocked by placing a blueprint.",
    "Computer Guy": "This is an achievement, that is unlocked by placing 5000 wires.",
    "Speedrun Master": "This is an achievement, that is unlocked by completing level 12 in under 30 Minutes. This "
                       "location is excluded by default, as it can become inaccessible in a save file after that time.",
    "Speedrun Novice": "This is an achievement, that is unlocked by completing level 12 in under 60 Minutes. This "
                       "location is excluded by default, as it can become inaccessible in a save file after that time.",
    "Not an idle game": "This is an achievement, that is unlocked by completing level 12 in under 120 Minutes. This "
                       "location is excluded by default, as it can become inaccessible in a save file after that time.",
    "Efficiency 2": "This is an achievement, that is unlocked by delivering 50 blueprint shapes per second to the hub.",
    "Branding specialist 1": "This is an achievement, that is unlocked by delivering 25 logo shapes per second to the "
                             "hub.",
    "Branding specialist 2": "This is an achievement, that is unlocked by delivering 50 logo shapes per second to the "
                             "hub.",
    "King of Inefficiency": "This is an achievement, that is unlocked by **not** placing a counter clock wise rotator "
                            "until level 14. This location is excluded by default, as it can become inaccessible in a "
                            "save file after placing that building.",
    "It's so slow": "This is an achievement, that is unlocked by completing level 12 **without** buying any belt "
                    "upgrade. This location is excluded by default, as it can become inaccessible in a save file after "
                    "buying that upgrade.",
    "MAM (Make Anything Machine)": "This is an achievement, that is unlocked by completing any level after level 26 "
                                   "**without** modifying your factory. It is recommended to build a Make Anything "
                                   "Machine.",
    "Perfectionist": "This is an achievement, that is unlocked by destroying more than 1000 buildings at once.",
    "The next dimension": "This is an achievement, that is unlocked by opening the wires layer.",
    "Oops": "This is an achievement, that is unlocked by delivering a shape, that neither a level requirement nor an "
            "upgrade requirement.",
    "Copy-Pasta": "This is an achievement, that is unlocked by placing a blueprint with at least 1000 buildings.",
    "I've seen that before ...": "This is an achievement, that is unlocked by producing RgRyRbRr.",
    "Memories from the past": "This is an achievement, that is unlocked by producing WrRgWrRg:CwCrCwCr:SgSgSgSg.",
    "I need trains": "This is an achievement, that is unlocked by placing a 500 tiles long belt.",
    "A bit early?": "This is an achievement, that is unlocked by producing the logo shape before reaching level 18. "
                    "This location is excluded by default, as it can become inaccessible in a save file after reaching "
                    "that level.",
    "GPS": "This is an achievement, that is unlocked by placing 15 or more map markers.",
    "Shapesanity 1": "Shapesanity locations can be checked by delivering a described shape to the hub, without "
                     "requiring a certain roation, orientation, or ordering. Shapesanity 1 is always an uncolored "
                     "circle.",
    "Shapesanity 2": "Shapesanity locations can be checked by delivering a described shape to the hub, without "
                     "requiring a certain roation, orientation, or ordering. Shapesanity 2 is always an uncolored "
                     "square.",
    "Shapesanity 3": "Shapesanity locations can be checked by delivering a described shape to the hub, without "
                     "requiring a certain roation, orientation, or ordering. Shapesanity 3 is always an uncolored "
                     "star.",
    "Shapesanity 4": "Shapesanity locations can be checked by delivering a described shape to the hub, without "
                     "requiring a certain roation, orientation, or ordering. Shapesanity 4 is always an uncolored "
                     "windmill.",
}

shapesanity_simple: Dict[str, str] = {}
shapesanity_1_4: Dict[str, str] = {}
shapesanity_two_sided: Dict[str, str] = {}
shapesanity_three_parts: Dict[str, str] = {}
shapesanity_four_parts: Dict[str, str] = {}

level_locations: List[str] = (["Level 1 Additional", "Level 20 Additional", "Level 20 Additional 2"]
                              + [f"Level {x}" for x in range(1, max_levels_and_upgrades)])
upgrade_locations: List[str] = [f"{cat} Upgrade Tier {roman(x)}"
                                for cat in categories for x in range(2, max_levels_and_upgrades+1)]
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
shapesanity_locations: List[str] = [f"Shapesanity {x}" for x in range(1, max_shapesanity+1)]


def init_shapesanity_pool() -> None:
    """Imports the pregenerated shapesanity pool."""
    from .data import shapesanity_pool
    shapesanity_simple.update(shapesanity_pool.shapesanity_simple)
    shapesanity_1_4.update(shapesanity_pool.shapesanity_1_4)
    shapesanity_two_sided.update(shapesanity_pool.shapesanity_two_sided)
    shapesanity_three_parts.update(shapesanity_pool.shapesanity_three_parts)
    shapesanity_four_parts.update(shapesanity_pool.shapesanity_four_parts)


def addlevels(maxlevel: int, logictype: str,
              random_logic_phase_length: List[int]) -> Dict[str, Tuple[str, LocationProgressType]]:
    """Returns a dictionary with all level locations based on player options (maxlevel INCLUDED).
    If shape requirements are not randomized, the logic type is expected to be vanilla."""

    # Level 1 is always directly accessible
    locations: Dict[str, Tuple[str, LocationProgressType]] \
        = {"Level 1": ("Main", LocationProgressType.PRIORITY),
           "Level 1 Additional": ("Main", LocationProgressType.PRIORITY)}
    level_regions = ["Main", "Levels with 1 Building", "Levels with 2 Buildings", "Levels with 3 Buildings",
                     "Levels with 4 Buildings", "Levels with 5 Buildings"]

    def f(name: str, region: str, progress: LocationProgressType = LocationProgressType.DEFAULT) -> None:
        locations[name] = (region, progress)

    if logictype.startswith("vanilla"):
        f("Level 20 Additional", "Levels with 5 Buildings")
        f("Level 20 Additional 2", "Levels with 5 Buildings")
        f("Level 2", "Levels with 1 Building")
        f("Level 3", "Levels with 1 Building")
        f("Level 4", "Levels with 1 Building")
        f("Level 5", "Levels with 2 Buildings")
        f("Level 6", "Levels with 2 Buildings")
        f("Level 7", "Levels with 3 Buildings")
        f("Level 8", "Levels with 3 Buildings")
        f("Level 9", "Levels with 4 Buildings")
        f("Level 10", "Levels with 4 Buildings")
        for x in range(11, maxlevel+1):
            f(f"Level {x}", "Levels with 5 Buildings")

    elif logictype.startswith("stretched"):
        phaselength = maxlevel//6
        f("Level 20 Additional", level_regions[20//phaselength])
        f("Level 20 Additional 2", level_regions[20//phaselength])
        for x in range(2, phaselength):
            f(f"Level {x}", "Main")
        for x in range(phaselength, phaselength*2):
            f(f"Level {x}", "Levels with 1 Building")
        for x in range(phaselength*2, phaselength*3):
            f(f"Level {x}", "Levels with 2 Buildings")
        for x in range(phaselength*3, phaselength*4):
            f(f"Level {x}", "Levels with 3 Buildings")
        for x in range(phaselength*4, phaselength*5):
            f(f"Level {x}", "Levels with 4 Buildings")
        for x in range(phaselength*5, maxlevel+1):
            f(f"Level {x}", "Levels with 5 Buildings")

    elif logictype.startswith("quick"):
        f("Level 20 Additional", "Levels with 5 Buildings")
        f("Level 20 Additional 2", "Levels with 5 Buildings")
        f("Level 2", "Levels with 1 Building")
        f("Level 3", "Levels with 2 Buildings")
        f("Level 4", "Levels with 3 Buildings")
        f("Level 5", "Levels with 4 Buildings")
        for x in range(6, maxlevel+1):
            f(f"Level {x}", "Levels with 5 Buildings")

    elif logictype.startswith("random_steps"):
        next_level = 2
        for phase in range(5):
            for x in range(random_logic_phase_length[phase]):
                f(f"Level {next_level+x}", level_regions[phase])
            next_level += random_logic_phase_length[phase]
            if next_level > 20:
                f("Level 20 Additional", level_regions[phase])
                f("Level 20 Additional 2", level_regions[phase])
        for x in range(next_level, maxlevel+1):
            f(f"Level {x}", "Levels with 5 Buildings")
        if next_level <= 20:
            f("Level 20 Additional", "Levels with 5 Buildings")
            f("Level 20 Additional 2", "Levels with 5 Buildings")

    elif logictype == "hardcore":
        f("Level 20 Additional", "Levels with 5 Buildings")
        f("Level 20 Additional 2", "Levels with 5 Buildings")
        for x in range(2, maxlevel+1):
            f(f"Level {x}", "Levels with 5 Buildings")

    elif logictype == "dopamine":
        f("Level 20 Additional", "Levels with 2 Buildings")
        f("Level 20 Additional 2", "Levels with 2 Buildings")
        for x in range(2, maxlevel+1):
            f(f"Level {x}", "Levels with 2 Buildings")

    elif logictype == "dopamine_overflow":
        f("Level 20 Additional", "Main")
        f("Level 20 Additional 2", "Main")
        for x in range(2, maxlevel+1):
            f(f"Level {x}", "Main")

    else:
        raise Exception(f"Illegal level logic type {logictype}")

    return locations


def addupgrades(finaltier: int, logictype: str,
                category_random_logic_amounts: Dict[str, int]) -> Dict[str, Tuple[str, LocationProgressType]]:
    """Returns a dictionary with all upgrade locations based on player options (finaltier INCLUDED).
    If shape requirements are not randomized, give logic type 0."""

    locations: Dict[str, Tuple[str, LocationProgressType]] = {}
    upgrade_regions = ["Main", "Upgrades with 1 Building", "Upgrades with 2 Buildings", "Upgrades with 3 Buildings",
                       "Upgrades with 4 Buildings", "Upgrades with 5 Buildings"]

    def f(name: str, region: str, progress: LocationProgressType = LocationProgressType.DEFAULT) -> None:
        locations[name] = (region, progress)

    if logictype == "vanilla_like":
        f("Belt Upgrade Tier II", "Main")
        f("Miner Upgrade Tier II", "Main")
        f("Processors Upgrade Tier II", "Main")
        f("Painting Upgrade Tier II", "Upgrades with 3 Buildings")
        f("Belt Upgrade Tier III", "Upgrades with 2 Buildings")
        f("Miner Upgrade Tier III", "Upgrades with 2 Buildings")
        f("Processors Upgrade Tier III", "Upgrades with 1 Building")
        f("Painting Upgrade Tier III", "Upgrades with 3 Buildings")
        for x in range(4, finaltier+1):
            tier = roman(x)
            for cat in categories:
                f(f"{cat} Upgrade Tier {tier}", "Upgrades with 5 Buildings")

    elif logictype == "linear":
        for cat in categories:
            for x in range(2, 7):
                f(f"{cat} Upgrade Tier {roman(x)}", upgrade_regions[x-2])
            for x in range(7, finaltier+1):
                f(f"{cat} Upgrade Tier {roman(x)}", "Upgrades with 5 Buildings")

    elif logictype == "category":
        for x in range(2, 7):
            f(f"Belt Upgrade Tier {roman(x)}", "Main")
            f(f"Miner Upgrade Tier {roman(x)}", "Main")
        for x in range(7, finaltier + 1):
            f(f"Belt Upgrade Tier {roman(x)}", "Upgrades with 5 Buildings")
            f(f"Miner Upgrade Tier {roman(x)}", "Upgrades with 5 Buildings")
        f("Processors Upgrade Tier II", "Upgrades with 1 Building")
        f("Processors Upgrade Tier III", "Upgrades with 2 Buildings")
        f("Processors Upgrade Tier IV", "Upgrades with 2 Buildings")
        f("Processors Upgrade Tier V", "Upgrades with 3 Buildings")
        f("Processors Upgrade Tier VI", "Upgrades with 3 Buildings")
        for x in range(7, finaltier+1):
            f(f"Processors Upgrade Tier {roman(x)}", "Upgrades with 5 Buildings")
        for x in range(2, 4):
            f(f"Painting Upgrade Tier {roman(x)}", "Upgrades with 4 Buildings")
        for x in range(4, finaltier+1):
            f(f"Painting Upgrade Tier {roman(x)}", "Upgrades with 5 Buildings")

    elif logictype == "category_random":
        for x in range(2, 6):
            tier = roman(x)
            f(f"Belt Upgrade Tier {tier}", upgrade_regions[category_random_logic_amounts["belt"]])
            f(f"Miner Upgrade Tier {tier}", upgrade_regions[category_random_logic_amounts["miner"]])
            f(f"Processors Upgrade Tier {tier}", upgrade_regions[category_random_logic_amounts["processors"]])
            f(f"Painting Upgrade Tier {tier}", upgrade_regions[category_random_logic_amounts["painting"]])
        for x in range(6, finaltier+1):
            tier = roman(x)
            f(f"Belt Upgrade Tier {tier}", "Upgrades with 5 Buildings")
            f(f"Miner Upgrade Tier {tier}", "Upgrades with 5 Buildings")
            f(f"Processors Upgrade Tier {tier}", "Upgrades with 5 Buildings")
            f(f"Painting Upgrade Tier {tier}", "Upgrades with 5 Buildings")

    else:  # logictype == hardcore
        for cat in categories:
            f(f"{cat} Upgrade Tier II", "Main")
        for x in range(3, finaltier+1):
            tier = roman(x)
            for cat in categories:
                f(f"{cat} Upgrade Tier {tier}", "Upgrades with 5 Buildings")

    return locations


def addachievements(excludesoftlock: bool, excludelong: bool, excludeprogressive: bool,
                    maxlevel: int, upgradelogictype: str, category_random_logic_amounts: Dict[str, int],
                    goal: str, presentlocations: Dict[str, Tuple[str, LocationProgressType]],
                    add_alias: Callable[[str,str],None]) -> Dict[str, Tuple[str, LocationProgressType]]:
    """Returns a dictionary with all achievement locations based on player options."""

    locations: Dict[str, Tuple[str, LocationProgressType]] = dict()
    upgrade_regions = ["Main", "Upgrades with 1 Building", "Upgrades with 2 Buildings", "Upgrades with 3 Buildings",
                       "Upgrades with 4 Buildings", "Upgrades with 5 Buildings"]

    def f(name: str, region: str, alias: str, progress: LocationProgressType = LocationProgressType.DEFAULT):
        locations[name] = (region, progress)
        add_alias(name, alias)

    f("My eyes no longer hurt", "Menu", "Activate dark mode")
    f("Painter", "Painted Shape Achievements", "Paint a shape (no Quad Painter)")
    f("Cutter", "Cut Shape Achievements", "Cut a shape (no Quad Cutter)")
    f("Rotater", "Rotated Shape Achievements", "Rotate a shape clock wise")
    f("Wait, they stack?", "Stacked Shape Achievements", "Stack a shape")
    f("Storage", "Stored Shape Achievements", "Store a shape in the storage")
    f("The logo!", "All Buildings Shapes", "Produce the shapez logo")
    f("To the moon", "All Buildings Shapes", "Produce the rocket shape")
    f("It's piling up", "All Buildings Shapes", "100k blueprint shapes")
    f("I'll use it later", "All Buildings Shapes", "1 million blueprint shapes")
    f("Efficiency 1", "All Buildings Shapes", "25 blueprints shapes / second")
    f("Preparing to launch", "All Buildings Shapes", "10 rocket shapes / second")
    f("SpaceY", "All Buildings Shapes", "20 rocket shapes / second")

    f("Stack overflow", "Stacked Shape Achievements", "4 layers shape")
    f("It's a mess", "Main", "100 different shapes in hub")
    f("Get rid of them", "Trashed Shape Achievements", "1000 shapes trashed")
    f("Getting into it", "Menu", "1 hour")
    f("Now it's easy", "Blueprint Achievements", "Place a blueprint")
    f("Computer Guy", "Wiring Achievements", "Place 5000 wires")
    f("Efficiency 2", "All Buildings Shapes", "50 blueprints shapes / second")
    f("Branding specialist 1", "All Buildings Shapes", "25 logo shapes / second")
    f("Branding specialist 2", "All Buildings Shapes", "50 logo shapes / second")
    f("Perfectionist", "Main", "Destroy more than 1000 objects at once")
    f("The next dimension", "Wiring Achievements", "Open the wires layer")
    f("Oops", "Main", "Deliver an irrelevant shape")
    f("Copy-Pasta", "Blueprint Achievements", "Place a 1000 buildings blueprint")
    f("I've seen that before ...", "All Buildings Shapes", "Produce RgRyRbRr")
    f("Memories from the past", "All Buildings Shapes", "Produce WrRgWrRg:CwCrCwCr:SgSgSgSg")
    f("I need trains", "Main", "Have a 500 tiles belt")
    f("GPS", "Menu", "15 map markers")
    # Achievements that depend on upgrades
    f("Even faster", "Upgrades with 5 Buildings", "All upgrades on tier VIII")
    if upgradelogictype == "linear":
        f("Faster", "Upgrades with 3 Buildings", "All upgrades on tier V")
    elif upgradelogictype == "category_random":
        f("Faster", upgrade_regions[
            max(category_random_logic_amounts["belt"], category_random_logic_amounts["miner"],
                category_random_logic_amounts["processors"], category_random_logic_amounts["painting"])
        ], "All upgrades on tier V")
    else:
        f("Faster", "Upgrades with 5 Buildings", "All upgrades on tier V")
    # Achievements that depend on the level
    f("Wires", presentlocations["Level 20"][0], "Complete level 20")
    if not goal == "vanilla":
        f("Freedom", presentlocations["Level 26"][0], "Complete level 26")
        f("MAM (Make Anything Machine)", "MAM needed", "Complete any level > 26 without modifications")
    if maxlevel >= 50:
        f("Can't stop", presentlocations["Level 50"][0], "Reach level 50")
    elif not goal == "vanilla":
        f("Can't stop", "Levels with 5 Buildings", "Reach level 50")
    if maxlevel >= 100:
        f("Is this the end?", presentlocations["Level 100"][0], "Reach level 100")
    elif not goal == "vanilla":
        f("Is this the end?", "Levels with 5 Buildings", "Reach level 100")

    if excludeprogressive:
        unreasonable_type = LocationProgressType.EXCLUDED
    else:
        unreasonable_type = LocationProgressType.DEFAULT

    if not excludesoftlock:
        f("Speedrun Master", presentlocations["Level 12"][0], "Complete level 12 in under 30 min", unreasonable_type)
        f("Speedrun Novice", presentlocations["Level 12"][0], "Complete level 12 in under 60 min", unreasonable_type)
        f("Not an idle game", presentlocations["Level 12"][0], "Complete level 12 in under 120 min", unreasonable_type)
        f("It's so slow", presentlocations["Level 12"][0],
          "Complete level 12 without upgrading belts", unreasonable_type)
        f("King of Inefficiency", presentlocations["Level 14"][0], "No ccw rotator until level 14", unreasonable_type)
        f("A bit early?", "All Buildings Shapes", "Produce logo shape before level 18", unreasonable_type)

    if not excludelong:
        f("It's been a long time", "Menu", "10 hours")
        f("Addicted", "Menu", "20 hours")

    return locations


def addshapesanity(amount: int, random: Random, append_shapesanity: Callable[[str],None],
                   add_alias: Callable[[str,str],None]) -> Dict[str, Tuple[str, LocationProgressType]]:
    """Returns a dictionary with a given number of random shapesanity locations."""

    included_shapes: Dict[str, Tuple[str, LocationProgressType]] = {}

    def f(name: str, region: str, alias: str, progress: LocationProgressType = LocationProgressType.DEFAULT) -> None:
        included_shapes[name] = (region, progress)
        append_shapesanity(alias)
        shapes_list.remove((alias, region))
        add_alias(name, alias)

    # Always have at least 4 shapesanity checks because of sphere 1 usefulls + both hardcore logic
    shapes_list = list(shapesanity_simple.items())
    f("Shapesanity 1", "Shapesanity Full Uncolored", "Uncolored Circle")
    f("Shapesanity 2", "Shapesanity Full Uncolored", "Uncolored Square")
    f("Shapesanity 3", "Shapesanity Full Uncolored", "Uncolored Star")
    f("Shapesanity 4", "Shapesanity East Windmill Uncolored", "Uncolored Windmill")

    # The pool switches dynamically depending on if either it's ratio or limit is reached
    switched = 0
    for counting in range(4, amount):
        if switched == 0 and (len(shapes_list) == 0 or counting == amount//2):
            shapes_list = list(shapesanity_1_4.items())
            switched = 1
        elif switched == 1 and (len(shapes_list) == 0 or counting == amount*7//12):
            shapes_list = list(shapesanity_two_sided.items())
            switched = 2
        elif switched == 2 and (len(shapes_list) == 0 or counting == amount*5//6):
            shapes_list = list(shapesanity_three_parts.items())
            switched = 3
        elif switched == 3 and (len(shapes_list) == 0 or counting == amount*11//12):
            shapes_list = list(shapesanity_four_parts.items())
            switched = 4
        x = random.randint(0, len(shapes_list)-1)
        next_shape = shapes_list.pop(x)
        included_shapes[f"Shapesanity {counting+1}"] = (next_shape[1], LocationProgressType.DEFAULT)
        append_shapesanity(next_shape[0])
        add_alias(f"Shapesanity {counting+1}", next_shape[0])

    return included_shapes


def addshapesanity_ut(shapesanity_names: List[str], add_alias: Callable[[str,str],None]
                      ) -> Dict[str, Tuple[str, LocationProgressType]]:
    """Returns the same information as addshapesanity but will add specific values based on a UT rebuild."""

    included_shapes: Dict[str, Tuple[str, LocationProgressType]] = {}

    for name in shapesanity_names:
        for options in [shapesanity_simple, shapesanity_1_4, shapesanity_two_sided, shapesanity_three_parts,
                        shapesanity_four_parts]:
            if name in options:
                next_shape = options[name]
                break
        else:
            raise ValueError(f"Could not find shapesanity name {name}")
        included_shapes[f"Shapesanity {len(included_shapes)+1}"] = (next_shape, LocationProgressType.DEFAULT)
        add_alias(f"Shapesanity {len(included_shapes)}", name)
    return included_shapes


class ShapezLocation(Location):
    game = "shapez"

    def __init__(self, player: int, name: str, address: Optional[int], region: Region,
                 progress_type: LocationProgressType):
        super(ShapezLocation, self).__init__(player, name, address, region)
        self.progress_type = progress_type
