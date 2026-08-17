from random import Random
from typing import Callable

from BaseClasses import Location, LocationProgressType, Region
from .data.strings import CATEGORY, LOCATIONS, REGIONS, OPTIONS, GOALS, OTHER, SHAPESANITY
from .options import max_shapesanity, max_levels_and_upgrades

categories = [CATEGORY.belt, CATEGORY.miner, CATEGORY.processors, CATEGORY.painting]

translate: list[tuple[int, str]] = [
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


location_description = {  # TODO change keys to global strings
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

shapesanity_simple: dict[str, str] = {}
shapesanity_1_4: dict[str, str] = {}
shapesanity_two_sided: dict[str, str] = {}
shapesanity_three_parts: dict[str, str] = {}
shapesanity_four_parts: dict[str, str] = {}

level_locations: list[str] = ([LOCATIONS.level(1, 1), LOCATIONS.level(20, 1), LOCATIONS.level(20, 2)]
                              + [LOCATIONS.level(x) for x in range(1, max_levels_and_upgrades)])
upgrade_locations: list[str] = [LOCATIONS.upgrade(cat, roman(x))
                                for cat in categories for x in range(2, max_levels_and_upgrades+1)]
achievement_locations: list[str] = [LOCATIONS.my_eyes, LOCATIONS.painter, LOCATIONS.cutter, LOCATIONS.rotater,
                                    LOCATIONS.wait_they_stack, LOCATIONS.wires, LOCATIONS.storage, LOCATIONS.freedom,
                                    LOCATIONS.the_logo, LOCATIONS.to_the_moon, LOCATIONS.its_piling_up,
                                    LOCATIONS.use_it_later, LOCATIONS.efficiency_1, LOCATIONS.preparing_to_launch,
                                    LOCATIONS.spacey, LOCATIONS.stack_overflow, LOCATIONS.its_a_mess, LOCATIONS.faster,
                                    LOCATIONS.even_faster, LOCATIONS.get_rid_of_them, LOCATIONS.a_long_time,
                                    LOCATIONS.addicted, LOCATIONS.cant_stop, LOCATIONS.is_this_the_end,
                                    LOCATIONS.getting_into_it, LOCATIONS.now_its_easy, LOCATIONS.computer_guy,
                                    LOCATIONS.speedrun_master, LOCATIONS.speedrun_novice, LOCATIONS.not_idle_game,
                                    LOCATIONS.efficiency_2, LOCATIONS.branding_1,
                                    LOCATIONS.branding_2, LOCATIONS.king_of_inefficiency, LOCATIONS.its_so_slow,
                                    LOCATIONS.mam, LOCATIONS.perfectionist, LOCATIONS.next_dimension, LOCATIONS.oops,
                                    LOCATIONS.copy_pasta, LOCATIONS.ive_seen_that_before, LOCATIONS.memories,
                                    LOCATIONS.i_need_trains, LOCATIONS.a_bit_early, LOCATIONS.gps]
shapesanity_locations: list[str] = [LOCATIONS.shapesanity(x) for x in range(1, max_shapesanity+1)]


def init_shapesanity_pool() -> None:
    """Imports the pregenerated shapesanity pool."""
    from .data import shapesanity_pool
    shapesanity_simple.update(shapesanity_pool.shapesanity_simple)
    shapesanity_1_4.update(shapesanity_pool.shapesanity_1_4)
    shapesanity_two_sided.update(shapesanity_pool.shapesanity_two_sided)
    shapesanity_three_parts.update(shapesanity_pool.shapesanity_three_parts)
    shapesanity_four_parts.update(shapesanity_pool.shapesanity_four_parts)


def addlevels(maxlevel: int, logictype: str,
              random_logic_phase_length: list[int]) -> dict[str, tuple[str, LocationProgressType]]:
    """Returns a dictionary with all level locations based on player options (maxlevel INCLUDED).
    If shape requirements are not randomized, the logic type is expected to be vanilla."""

    # Level 1 is always directly accessible
    locations: dict[str, tuple[str, LocationProgressType]] \
        = {LOCATIONS.level(1): (REGIONS.main, LocationProgressType.PRIORITY),
           LOCATIONS.level(1, 1): (REGIONS.main, LocationProgressType.PRIORITY)}
    level_regions = [REGIONS.main, REGIONS.levels_1, REGIONS.levels_2, REGIONS.levels_3,
                     REGIONS.levels_4, REGIONS.levels_5]

    def f(name: str, region: str, progress: LocationProgressType = LocationProgressType.DEFAULT) -> None:
        locations[name] = (region, progress)

    if logictype.startswith(OPTIONS.logic_vanilla):
        f(LOCATIONS.level(20, 1), REGIONS.levels_5)
        f(LOCATIONS.level(20, 2), REGIONS.levels_5)
        f(LOCATIONS.level(2), REGIONS.levels_1)
        f(LOCATIONS.level(3), REGIONS.levels_1)
        f(LOCATIONS.level(4), REGIONS.levels_1)
        f(LOCATIONS.level(5), REGIONS.levels_2)
        f(LOCATIONS.level(6), REGIONS.levels_2)
        f(LOCATIONS.level(7), REGIONS.levels_3)
        f(LOCATIONS.level(8), REGIONS.levels_3)
        f(LOCATIONS.level(9), REGIONS.levels_4)
        f(LOCATIONS.level(10), REGIONS.levels_4)
        for x in range(11, maxlevel+1):
            f(LOCATIONS.level(x), REGIONS.levels_5)

    elif logictype.startswith(OPTIONS.logic_stretched):
        phaselength = maxlevel//6
        f(LOCATIONS.level(20, 1), level_regions[20//phaselength])
        f(LOCATIONS.level(20, 2), level_regions[20//phaselength])
        for x in range(2, phaselength):
            f(LOCATIONS.level(x), REGIONS.main)
        for x in range(phaselength, phaselength*2):
            f(LOCATIONS.level(x), REGIONS.levels_1)
        for x in range(phaselength*2, phaselength*3):
            f(LOCATIONS.level(x), REGIONS.levels_2)
        for x in range(phaselength*3, phaselength*4):
            f(LOCATIONS.level(x), REGIONS.levels_3)
        for x in range(phaselength*4, phaselength*5):
            f(LOCATIONS.level(x), REGIONS.levels_4)
        for x in range(phaselength*5, maxlevel+1):
            f(LOCATIONS.level(x), REGIONS.levels_5)

    elif logictype.startswith(OPTIONS.logic_quick):
        f(LOCATIONS.level(20, 1), REGIONS.levels_5)
        f(LOCATIONS.level(20, 2), REGIONS.levels_5)
        f(LOCATIONS.level(2), REGIONS.levels_1)
        f(LOCATIONS.level(3), REGIONS.levels_2)
        f(LOCATIONS.level(4), REGIONS.levels_3)
        f(LOCATIONS.level(5), REGIONS.levels_4)
        for x in range(6, maxlevel+1):
            f(LOCATIONS.level(x), REGIONS.levels_5)

    elif logictype.startswith(OPTIONS.logic_random_steps):
        next_level = 2
        for phase in range(5):
            for x in range(random_logic_phase_length[phase]):
                f(LOCATIONS.level(next_level+x), level_regions[phase])
            next_level += random_logic_phase_length[phase]
            if next_level > 20:
                f(LOCATIONS.level(20, 1), level_regions[phase])
                f(LOCATIONS.level(20, 2), level_regions[phase])
        for x in range(next_level, maxlevel+1):
            f(LOCATIONS.level(x), REGIONS.levels_5)
        if next_level <= 20:
            f(LOCATIONS.level(20, 1), REGIONS.levels_5)
            f(LOCATIONS.level(20, 2), REGIONS.levels_5)

    elif logictype == OPTIONS.logic_hardcore:
        f(LOCATIONS.level(20, 1), REGIONS.levels_5)
        f(LOCATIONS.level(20, 2), REGIONS.levels_5)
        for x in range(2, maxlevel+1):
            f(LOCATIONS.level(x), REGIONS.levels_5)

    elif logictype == OPTIONS.logic_dopamine:
        f(LOCATIONS.level(20, 1), REGIONS.levels_2)
        f(LOCATIONS.level(20, 2), REGIONS.levels_2)
        for x in range(2, maxlevel+1):
            f(LOCATIONS.level(x), REGIONS.levels_2)

    elif logictype == OPTIONS.logic_dopamine_overflow:
        f(LOCATIONS.level(20, 1), REGIONS.main)
        f(LOCATIONS.level(20, 2), REGIONS.main)
        for x in range(2, maxlevel+1):
            f(LOCATIONS.level(x), REGIONS.main)

    else:
        raise Exception(f"Illegal level logic type {logictype}")

    return locations


def addupgrades(finaltier: int, logictype: str,
                category_random_logic_amounts: dict[str, int]) -> dict[str, tuple[str, LocationProgressType]]:
    """Returns a dictionary with all upgrade locations based on player options (finaltier INCLUDED).
    If shape requirements are not randomized, give logic type 0."""

    locations: dict[str, tuple[str, LocationProgressType]] = {}
    upgrade_regions = [REGIONS.main, REGIONS.upgrades_1, REGIONS.upgrades_2, REGIONS.upgrades_3,
                       REGIONS.upgrades_4, REGIONS.upgrades_5]

    def f(name: str, region: str, progress: LocationProgressType = LocationProgressType.DEFAULT) -> None:
        locations[name] = (region, progress)

    if logictype == OPTIONS.logic_vanilla_like:
        f(LOCATIONS.upgrade(CATEGORY.belt, "II"), REGIONS.main)
        f(LOCATIONS.upgrade(CATEGORY.miner, "II"), REGIONS.main)
        f(LOCATIONS.upgrade(CATEGORY.processors, "II"), REGIONS.main)
        f(LOCATIONS.upgrade(CATEGORY.painting, "II"), REGIONS.upgrades_3)
        f(LOCATIONS.upgrade(CATEGORY.belt, "III"), REGIONS.upgrades_2)
        f(LOCATIONS.upgrade(CATEGORY.miner, "III"), REGIONS.upgrades_2)
        f(LOCATIONS.upgrade(CATEGORY.processors, "III"), REGIONS.upgrades_1)
        f(LOCATIONS.upgrade(CATEGORY.painting, "III"), REGIONS.upgrades_3)
        for x in range(4, finaltier+1):
            tier = roman(x)
            for cat in categories:
                f(LOCATIONS.upgrade(cat, tier), REGIONS.upgrades_5)

    elif logictype == OPTIONS.logic_linear:
        for x in range(2, 7):
            tier = roman(x)
            for cat in categories:
                f(LOCATIONS.upgrade(cat, tier), upgrade_regions[x-2])
        for x in range(7, finaltier+1):
            tier = roman(x)
            for cat in categories:
                f(LOCATIONS.upgrade(cat, tier), REGIONS.upgrades_5)

    elif logictype == OPTIONS.logic_category:
        for x in range(2, 7):
            tier = roman(x)
            f(LOCATIONS.upgrade(CATEGORY.belt, tier), REGIONS.main)
            f(LOCATIONS.upgrade(CATEGORY.miner, tier), REGIONS.main)
        for x in range(7, finaltier + 1):
            tier = roman(x)
            f(LOCATIONS.upgrade(CATEGORY.belt, tier), REGIONS.upgrades_5)
            f(LOCATIONS.upgrade(CATEGORY.miner, tier), REGIONS.upgrades_5)
        f(LOCATIONS.upgrade(CATEGORY.processors, "II"), REGIONS.upgrades_1)
        f(LOCATIONS.upgrade(CATEGORY.processors, "III"), REGIONS.upgrades_2)
        f(LOCATIONS.upgrade(CATEGORY.processors, "IV"), REGIONS.upgrades_2)
        f(LOCATIONS.upgrade(CATEGORY.processors, "V"), REGIONS.upgrades_3)
        f(LOCATIONS.upgrade(CATEGORY.processors, "VI"), REGIONS.upgrades_3)
        for x in range(7, finaltier+1):
            f(LOCATIONS.upgrade(CATEGORY.processors, roman(x)), REGIONS.upgrades_5)
        for x in range(2, 4):
            f(LOCATIONS.upgrade(CATEGORY.painting, roman(x)), REGIONS.upgrades_4)
        for x in range(4, finaltier+1):
            f(LOCATIONS.upgrade(CATEGORY.painting, roman(x)), REGIONS.upgrades_5)

    elif logictype == OPTIONS.logic_category_random:
        for x in range(2, 7):
            tier = roman(x)
            f(LOCATIONS.upgrade(CATEGORY.belt, tier),
              upgrade_regions[category_random_logic_amounts[CATEGORY.belt_low]])
            f(LOCATIONS.upgrade(CATEGORY.miner, tier),
              upgrade_regions[category_random_logic_amounts[CATEGORY.miner_low]])
            f(LOCATIONS.upgrade(CATEGORY.processors, tier),
              upgrade_regions[category_random_logic_amounts[CATEGORY.processors_low]])
            f(LOCATIONS.upgrade(CATEGORY.painting, tier),
              upgrade_regions[category_random_logic_amounts[CATEGORY.painting_low]])
        for x in range(7, finaltier+1):
            tier = roman(x)
            for cat in categories:
                f(LOCATIONS.upgrade(cat, tier), REGIONS.upgrades_5)

    else:  # logictype == hardcore
        for cat in categories:
            f(LOCATIONS.upgrade(cat, "II"), REGIONS.main)
        for x in range(3, finaltier+1):
            tier = roman(x)
            for cat in categories:
                f(LOCATIONS.upgrade(cat, tier), REGIONS.upgrades_5)

    return locations


def addachievements(excludesoftlock: bool, excludelong: bool, excludeprogressive: bool,
                    maxlevel: int, upgradelogictype: str, category_random_logic_amounts: dict[str, int],
                    goal: str, presentlocations: dict[str, tuple[str, LocationProgressType]],
                    add_alias: Callable[[str, str], None], has_upgrade_traps: bool
                    ) -> dict[str, tuple[str, LocationProgressType]]:
    """Returns a dictionary with all achievement locations based on player options."""

    locations: dict[str, tuple[str, LocationProgressType]] = dict()
    upgrade_regions = [REGIONS.main, REGIONS.upgrades_1, REGIONS.upgrades_2, REGIONS.upgrades_3,
                       REGIONS.upgrades_4, REGIONS.upgrades_5]

    def f(name: str, region: str, alias: str, progress: LocationProgressType = LocationProgressType.DEFAULT):
        locations[name] = (region, progress)
        add_alias(name, alias)

    f(LOCATIONS.my_eyes, REGIONS.menu, "Activate dark mode")
    f(LOCATIONS.painter, REGIONS.paint_not_quad, "Paint a shape (no Quad Painter)")
    f(LOCATIONS.cutter, REGIONS.cut_not_quad, "Cut a shape (no Quad Cutter)")
    f(LOCATIONS.rotater, REGIONS.rotate_cw, "Rotate a shape clock wise")
    f(LOCATIONS.wait_they_stack, REGIONS.stack_shape, "Stack a shape")
    f(LOCATIONS.storage, REGIONS.store_shape, "Store a shape in the storage")
    f(LOCATIONS.the_logo, REGIONS.all_buildings, "Produce the shapez logo")
    f(LOCATIONS.to_the_moon, REGIONS.all_buildings, "Produce the rocket shape")
    f(LOCATIONS.its_piling_up, REGIONS.all_buildings, "100k blueprint shapes")
    f(LOCATIONS.use_it_later, REGIONS.all_buildings, "1 million blueprint shapes")

    f(LOCATIONS.stack_overflow, REGIONS.stack_shape, "4 layers shape")
    f(LOCATIONS.its_a_mess, REGIONS.main, "100 different shapes in hub")
    f(LOCATIONS.get_rid_of_them, REGIONS.trash_shape, "1000 shapes trashed")
    f(LOCATIONS.getting_into_it, REGIONS.menu, "1 hour")
    f(LOCATIONS.now_its_easy, REGIONS.blueprint, "Place a blueprint")
    f(LOCATIONS.computer_guy, REGIONS.wiring, "Place 5000 wires")
    f(LOCATIONS.perfectionist, REGIONS.any_building, "Destroy more than 1000 objects at once")
    f(LOCATIONS.next_dimension, REGIONS.wiring, "Open the wires layer")
    f(LOCATIONS.copy_pasta, REGIONS.blueprint, "Place a 1000 buildings blueprint")
    f(LOCATIONS.ive_seen_that_before, REGIONS.all_buildings, "Produce RgRyRbRr")
    f(LOCATIONS.memories, REGIONS.all_buildings, "Produce WrRgWrRg:CwCrCwCr:SgSgSgSg")
    f(LOCATIONS.i_need_trains, REGIONS.belt, "Have a 500 tiles belt")
    f(LOCATIONS.gps, REGIONS.menu, "15 map markers")

    # Per second delivery achievements
    f(LOCATIONS.preparing_to_launch, REGIONS.all_buildings, "10 rocket shapes / second")
    if not has_upgrade_traps:
        f(LOCATIONS.spacey, REGIONS.all_buildings, "20 rocket shapes / second")
        f(LOCATIONS.efficiency_1, REGIONS.all_buildings, "25 blueprints shapes / second")
        f(LOCATIONS.efficiency_2, REGIONS.all_buildings_x1_6_belt, "50 blueprints shapes / second")
        f(LOCATIONS.branding_1, REGIONS.all_buildings, "25 logo shapes / second")
        f(LOCATIONS.branding_2, REGIONS.all_buildings_x1_6_belt, "50 logo shapes / second")

    # Achievements that depend on upgrades
    f(LOCATIONS.even_faster, REGIONS.upgrades_5, "All upgrades on tier VIII")
    if upgradelogictype == OPTIONS.logic_linear:
        f(LOCATIONS.faster, REGIONS.upgrades_3, "All upgrades on tier V")
    elif upgradelogictype == OPTIONS.logic_category_random:
        f(LOCATIONS.faster, upgrade_regions[
            max(category_random_logic_amounts[CATEGORY.belt_low],
                category_random_logic_amounts[CATEGORY.miner_low],
                category_random_logic_amounts[CATEGORY.processors_low],
                category_random_logic_amounts[CATEGORY.painting_low])
        ], "All upgrades on tier V")
    else:
        f(LOCATIONS.faster, REGIONS.upgrades_5, "All upgrades on tier V")

    # Achievements that depend on the level
    f(LOCATIONS.wires, presentlocations[LOCATIONS.level(20)][0], "Complete level 20")
    if not goal == GOALS.vanilla:
        f(LOCATIONS.freedom, presentlocations[LOCATIONS.level(26)][0], "Complete level 26")
        f(LOCATIONS.mam, REGIONS.mam, "Complete any level > 26 without modifications")
    if maxlevel >= 50:
        f(LOCATIONS.cant_stop, presentlocations[LOCATIONS.level(50)][0], "Reach level 50")
    elif goal not in [GOALS.vanilla, GOALS.mam]:
        f(LOCATIONS.cant_stop, REGIONS.levels_5, "Reach level 50")
    if maxlevel >= 100:
        f(LOCATIONS.is_this_the_end, presentlocations[LOCATIONS.level(100)][0], "Reach level 100")
    elif goal not in [GOALS.vanilla, GOALS.mam]:
        f(LOCATIONS.is_this_the_end, REGIONS.levels_5, "Reach level 100")

    # Achievements that depend on player preferences
    if excludeprogressive:
        unreasonable_type = LocationProgressType.EXCLUDED
    else:
        unreasonable_type = LocationProgressType.DEFAULT
    if not excludesoftlock:
        f(LOCATIONS.speedrun_master, presentlocations[LOCATIONS.level(12)][0],
          "Complete level 12 in under 30 min", unreasonable_type)
        f(LOCATIONS.speedrun_novice, presentlocations[LOCATIONS.level(12)][0],
          "Complete level 12 in under 60 min", unreasonable_type)
        f(LOCATIONS.not_idle_game, presentlocations[LOCATIONS.level(12)][0],
          "Complete level 12 in under 120 min", unreasonable_type)
        f(LOCATIONS.its_so_slow, presentlocations[LOCATIONS.level(12)][0],
          "Complete level 12 without upgrading belts", unreasonable_type)
        f(LOCATIONS.king_of_inefficiency, presentlocations[LOCATIONS.level(14)][0],
          "No ccw rotator until level 14", unreasonable_type)
        f(LOCATIONS.a_bit_early, REGIONS.all_buildings,
          "Produce logo shape before level 18", unreasonable_type)
    if not excludelong:
        f(LOCATIONS.a_long_time, REGIONS.menu, "10 hours")
        f(LOCATIONS.addicted, REGIONS.menu, "20 hours")

    # Achievements with a softlock chance of less than
    # 1 divided by 2 to the power of the number of all atoms in the universe
    f(LOCATIONS.oops, REGIONS.main, "Deliver an irrelevant shape")

    return locations


def addshapesanity(amount: int, random: Random, append_shapesanity: Callable[[str], None],
                   add_alias: Callable[[str, str], None]) -> dict[str, tuple[str, LocationProgressType]]:
    """Returns a dictionary with a given number of random shapesanity locations."""

    included_shapes: dict[str, tuple[str, LocationProgressType]] = {}

    def f(name: str, region: str, alias: str, progress: LocationProgressType = LocationProgressType.DEFAULT) -> None:
        included_shapes[name] = (region, progress)
        append_shapesanity(alias)
        shapes_list.remove((alias, region))
        add_alias(name, alias)

    # Always have at least 4 shapesanity checks because of sphere 1 usefulls + both hardcore logic
    shapes_list = list(shapesanity_simple.items())
    f(LOCATIONS.shapesanity(1), REGIONS.sanity(REGIONS.full, REGIONS.uncol),
      SHAPESANITY.full(SHAPESANITY.uncolored, SHAPESANITY.circle))
    f(LOCATIONS.shapesanity(2), REGIONS.sanity(REGIONS.full, REGIONS.uncol),
      SHAPESANITY.full(SHAPESANITY.uncolored, SHAPESANITY.square))
    f(LOCATIONS.shapesanity(3), REGIONS.sanity(REGIONS.full, REGIONS.uncol),
      SHAPESANITY.full(SHAPESANITY.uncolored, SHAPESANITY.star))
    f(LOCATIONS.shapesanity(4), REGIONS.sanity(REGIONS.east_wind, REGIONS.uncol),
      SHAPESANITY.full(SHAPESANITY.uncolored, SHAPESANITY.windmill))

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
        included_shapes[LOCATIONS.shapesanity(counting+1)] = (next_shape[1], LocationProgressType.DEFAULT)
        append_shapesanity(next_shape[0])
        add_alias(LOCATIONS.shapesanity(counting+1), next_shape[0])

    return included_shapes


def addshapesanity_ut(shapesanity_names: list[str], add_alias: Callable[[str, str], None]
                      ) -> dict[str, tuple[str, LocationProgressType]]:
    """Returns the same information as addshapesanity but will add specific values based on a UT rebuild."""

    included_shapes: dict[str, tuple[str, LocationProgressType]] = {}

    for name in shapesanity_names:
        for options in [shapesanity_simple, shapesanity_1_4, shapesanity_two_sided, shapesanity_three_parts,
                        shapesanity_four_parts]:
            if name in options:
                next_shape = options[name]
                break
        else:
            raise ValueError(f"Could not find shapesanity name {name}")
        included_shapes[LOCATIONS.shapesanity(len(included_shapes)+1)] = (next_shape, LocationProgressType.DEFAULT)
        add_alias(LOCATIONS.shapesanity(len(included_shapes)), name)
    return included_shapes


class ShapezLocation(Location):
    game = OTHER.game_name

    def __init__(self, player: int, name: str, address: int | None, region: Region,
                 progress_type: LocationProgressType):
        super(ShapezLocation, self).__init__(player, name, address, region)
        self.progress_type = progress_type
