from dataclasses import dataclass

from Options import Choice, Range, Toggle, DeathLink, DefaultOnToggle, OptionGroup, PerGameCommonOptions

class Goal(Choice):
    """
    Determines the goal of the seed

    Final Battle: Beat Boss Cass in Final Battle and rescue your parents from The Dreaming

    All Bosses: Beat all five bosses - (Bull, Crikey, Fluffy, Shadow, and Boss Cass)

    All Thunder Eggs: Collect all Thunder Eggs

    100%: Reach 100% completion by collecting all Thunder Eggs, Golden Cogs, and Talismans
    """
    display_name = "Goal"
    option_final_battle = 0
    option_all_bosses = 1
    option_all_thunder_eggs = 2
    option_completion = 3
    default = 0

class LevelShuffle(Toggle):
    """
    Determines whether the levels that portals lead to will be shuffled
    """
    display_name = "Level Shuffle"

class LevelUnlockStyle(Choice):
    """
    Determines how levels are unlocked

    Vanilla: All levels are unlocked from the start of the world

    Checks: The first level is unlocked from the start but all other levels are unlocked via checks

    Vanilla Bosses: The first level is unlocked from the start. Bosses are unlocked via vanilla hub Thunder Egg counts. All other levels are unlocked via checks
    """
    display_name = "Vanilla Boss Unlock"
    option_vanilla = 0
    option_checks = 1
    option_vanilla_bosses = 2
    default = 1

class ProgressiveLevel(Toggle):
    """
    Determines if level unlocks are progressive (only if levels are check based)
    """
    default = True

class Cogsanity(Choice):
    """
    Determines how cogs grant checks

    Each Cog: Every cog grants a check (90 Locations)

    Per Level: Collecting all 10 cogs in a level grants a check (9 Locations)

    None: Cogs do not grant any checks
    """
    display_name = "Cogsanity"
    option_each_cog = 0
    option_per_level = 1
    option_none = 2
    default = 0

class Bilbysanity(Choice):
    """
    Determines how bilbies grant checks

    All No TE: All bilbies grant checks but no check is granted for the bilby Thunder Eggs (36 Locations)

    All With TE: Every bilby grants a check as well as the bilby Thunder Eggs (45 Locations)

    None: Bilbies do not grant any checks
    """
    display_name = "Bilbysanity"
    option_all_no_te = 0
    option_all_with_te = 1
    option_none = 2
    default = 0

class Attributesanity(Choice):
    """
    Determines how rangs and abilities grant checks
    
    Skip Elementals: All rangs and abilities except elemental rangs grant checks (avoids double check from talismans) (11 Locations)
    
    All: All rangs and abilities grant checks (15 Locations)
    
    None: Rangs and abilities do not grant any checks
    """
    display_name = ("Attributesanity")
    option_skip_elementals = 0
    option_all = 1
    option_none = 2
    default = 0

class StartWithBoom(Choice):
    """
    Determines if Ty starts with his boomerang
    """
    display_name = ("Start With Boomerang")
    default = True

class ProgressiveElementals(Toggle):
    """
    Determines if elemental rangs are a progressive check
    """
    display_name = "Progressive Elemental Rangs"
    default = True

class Framesanity(Choice):
    """
    Determines how collecting Picture Frames grants checks

    Per Level: Collecting all frames in a level grants a check (9 Locations - Bonus Worlds not included)

    All: Every frame grants a check (127 Locations - Bonus Worlds not included)

    None: Frames do not grant any checks
    """
    display_name = "Framesanity"
    option_none = 0
    option_per_level = 1
    option_all = 2
    default = 0

class JunkFillPercentage(Range):
    """
    Replace a percentage of non-required checks in the item pool with random junk items
    """
    display_name = "Junk Fill Percentage"
    range_start = 0
    range_end = 100
    default = 50

class HubThunderEggCounts(Range):
    """
    If bosses are unlocked via vanilla hub Thunder Egg counts, required count per hub can be set here
    """
    display_name = "Hub Thunder Egg Requirement"
    range_start = 0
    range_end = 24
    default = 17

class LogicDifficulty(Choice):
    """
    What set of logic to use

    Standard: The logic assumes elemental rangs are required to enter hubs

    Advanced: Assumes hubs may be entered early and elemental rangs are optional.
    """
    display_name = "Logic Difficulty"
    option_standard = 0
    option_advanced = 1
    default = 0


ty1_option_groups = [
    OptionGroup("General Options", [
        Goal,
        LogicDifficulty,
        ProgressiveElementals,
        StartWithBoom
    ]),
    OptionGroup("Stages", [
        LevelShuffle,
        LevelUnlockStyle,
        ProgressiveLevel,
        HubThunderEggCounts,
    ]),
    OptionGroup("Sanity Options", [
        Cogsanity,
        Bilbysanity,
        Attributesanity,
        Framesanity,
    ]),
    OptionGroup("Junk", [
        JunkFillPercentage,
    ]),
]


@dataclass
class Ty1Options(PerGameCommonOptions):
    goal: Goal
    logic_difficulty: LogicDifficulty
    progressive_elementals: ProgressiveElementals
    start_with_boom: StartWithBoom

    level_shuffle: LevelShuffle
    level_unlock_style: LevelUnlockStyle
    progressive_level: ProgressiveLevel
    hub_te_counts: HubThunderEggCounts

    cogsanity: Cogsanity
    bilbysanity: Bilbysanity
    attributesanity: Attributesanity
    framesanity: Framesanity

    junk_fill_percentage: JunkFillPercentage
    death_link: DeathLink
