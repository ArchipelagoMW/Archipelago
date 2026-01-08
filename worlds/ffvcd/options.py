from dataclasses import dataclass
from Options import Toggle, DefaultOnToggle, Choice, PerGameCommonOptions, Range, OptionSet, FreeText


class JobPalettes(Toggle):
    """
    When enabled, randomizes palettes for each characters' jobs
    """
    display_name = "Randomize Job Palettes"

class FourJob(Toggle):
    """
    When enabled, enables four job mode. No crystals are placed in the world, and the player starts with 4 crystals.
    Players are disallowed from leaving the menu if every character doesnt have a unique job.

    For ability settings only "Don't Place" or "Only for Available Jobs" will work with four job mode.
    If neither is set it defaults to don't place.
    """
    display_name = "Enable Four Job Mode"

class RemoveFlashes(DefaultOnToggle):
    """
    When enabled, optional patches for removing flashes (notably Neo ExDeath) are applied
    """
    display_name = "Apply flash removal"

class WorldLock(Choice):
    """Determines how many worlds are available from the start.
    1: The first world is available. Adamantite unlocks World 2. Defeating Exdeath in World 2 unlocks World 3 via Anti Barrier and Bracelet.
    2: Worlds 1 and 2 are available. Defeating Exdeath in World 2 unlocks World 3 via Anti Barrier and Bracelet.
    3: All worlds are available immediately.    
    """
    display_name = "World Lock"
    option_world_1 = 0
    option_world_2 = 1
    option_world_3 = 2

class ProgressionChecks(Choice):
    """Determines where progression checks are in the game for the multiworld.
    1: All boss locations are valid checks for progression
    2: All bosses, all events, & all chests are valid checks for progression
    """
    display_name = "Progression Checks"
    option_bosses = 0
    option_all = 1

class TrappedChests(Toggle):
    """
    When enabled, 30 trapped chests will be spread across the world.
    """
    display_name = "Enable Trapped Chests"

class TrappedChestsSetting(Choice):
    """
    Local High Value: These chests will only give high value items local to the player's world.
    Local High Value and Progression: These chests will give high value items local to the player's world or local progression.
    Any: Any items in the multiworld can appear in the chests.

    If progression checks are set to bosses then options 2 and 3 will not add progression to trapped chests.
    If set to "Any" gil cannot land in trapped chests, due to how the world is built gil landing in trapped locations
    will result in one fewer trapped chests per.
    """
    display_name = "Enable Trapped Chests"
    option_local_high_value = 0
    option_local_high_value_and_progression = 1
    option_any = 2
    default = 0

class JobsIncluded(OptionSet):
    """
    Sets which jobs and job groups for abilities are allowed to appear in the world.

    Possible values are:
    "Knight"
    "Monk"
    "Thief"
    "Dragoon"
    "Ninja"
    "Samurai"
    "Berserker"
    "Hunter"
    "Mystic Knight"
    "White Mage"
    "Black Mage"
    "Time Mage"
    "Summoner"
    "Blue Mage"
    "Red Mage"
    "Trainer"
    "Chemist"
    "Geomancer"
    "Bard"
    "Dancer"
    "Mimic"
    "Freelancer"
    """
    display_name = "Job and Groups in World"
    valid_keys = frozenset([
        "Knight",
        "Monk",
        "Thief",
        "Dragoon",
        "Ninja",
        "Samurai",
        "Berserker",
        "Hunter",
        "Mystic Knight",
        "White Mage",
        "Black Mage",
        "Time Mage",
        "Summoner",
        "Blue Mage",
        "Red Mage",
        "Trainer",
        "Chemist",
        "Geomancer",
        "Bard",
        "Dancer",
        "Mimic",
        "Freelancer"
    ])
    default = valid_keys.copy()


class RandomJobCount(Range):
    """
    Set the range for jobs available in the world. Lower numbers will likely create harder seeds and vice versa.
    Be wary of setting this too low, as it could create some extreme difficulty depending on starting job.
    Will not exceed available jobs from the "Job and Groups in World" list.
    This setting only applies when "Four Job Mode" is off.
    """
    display_name = "Job Crystals Available"
    range_start = 4
    range_end = 22
    default = 22

class AbilitySettings(Choice):
    """
    All job abilities from "Job and Groups in World" list are placed by default.
    
    Only for Available Jobs: Places only abilities for whichever jobs crystals are in the world
    (controlled by the Jobs Available and "Job and Groups in World" setting or "Four Job Mode").

    Available Jobs Plus Extra: Places abilities for whichever job crystals are in the world plus a small amount extra, 
    controlled by the "Job Group Abilities Number" setting.

    Random by Job: Places random abilities in the world but keeps them grouped by jobs
    (for instance if Time Magic Lvl 1 is in the world so will 2-6). The number of random job groups is controlled by the setting 
    "Job Group Abilities Number" setting.

    Random All Abilities: Places abilities randomly with no regard for job groupings, but doesn't place all.

    Don't Place: Places no abilties in the item world.

    Random Only for Unavailable Jobs: Includes some number of job ability groups controlled by "Job Group Abilities Number" 
    while excluding jobs excluded via "Job and Groups in World" and included via "Job Crystals Available".

    If a setting other than "Don't Place" or "Only for Available Jobs" is selected with "Four Job Mode" then this will default to "Don't Place".
    """
    display_name = "Ability Settings"
    option_place_all = 0
    option_only_for_available_jobs = 1
    option_available_jobs_plus_extra = 2
    option_random_by_job = 3
    option_random_all_abilities = 4
    option_dont_place = 5
    option_random_only_for_unavailable_jobs = 6
    default = 0

class JobGroupAbilitiesNumber(Range):
    """
    Sets how many extra job groups worth of abilities will be in the world if the Ability Setting "Available Jobs Plus Extra" is selected. 
    Sets how many job groups worth of abilities will be in the world if the Ability Setting "Random by Job" or "Random Only for Unavailable Jobs" is selected.  

    If this number plus "Job Crystals Available" exceeds items in "Job and Groups in World" then it will place all from "Job and Groups in World" list.
    """
    display_name = "Job Group Abilities Number"
    range_start = 4
    range_end = 22
    default = 22

class OnlyUsableMagic(DefaultOnToggle):
    """
    When enabled, only includes magic for jobs and ability groups that exist in the world.

    If "Random All Abilities" is selected for Ability Settings some magic might still be unusable.
    This will go off the jobs and ability groups in the world not what individual abilities might exist in the world.
    """
    display_name = "Only Include Usable Magic"

class DisableTier1Magic(Toggle):
    """
    When enabled, removes level 1 and 2 magic from the game. 

    This applies to Black, White, Time, and Red Mages, Summoner, and Mystic Knight.
    This will not affect starting magic pool, only what will be placed in the world.
    """
    display_name = "Disable Tier 1 Magic"

class DisableTier2Magic(Toggle):
    """
    When enabled, removes level 3 and 4 magic from the game. 

    This applies to Black, White, Time, and Red Mages, Summoner, and Mystic Knight.
    """
    display_name = "Disable Tier 2 Magic"

class DisableTier3Magic(Toggle):
    """
    When enabled, removes level 5 and 6 magic from the game. 

    This applies to Black, White, Time, and Red Mages, Summoner, and Mystic Knight.
    """
    display_name = "Disable Tier 3 Magic"

class KuzarProgression(Toggle):
    """
    When enabled, allows Kuzar to have progression items. 

    Items in Kuzar logically require all 4 tablets.
    """
    display_name = "Enable Kuzar Progression"

class RiftAndVoidProgression(Toggle):
    """
    When enabled, allows areas within the Rift and Void to have progression. 

    """
    display_name = "Enable Rift and Void Progression"

class LennaName(FreeText):
    """
    Enter a name for Lenna. 
    Anything over 6 characters will be truncated. Alphanumeric only.
    """
    display_name = "Lenna's Name"
    default = "Lenna"

class GalufName(FreeText):
    """
    Enter a name for Galuf. 
    Anything over 6 characters will be truncated. Alphanumeric only.
    """
    display_name = "Galuf's Name"
    default = "Galuf"

class KrileName(FreeText):
    """
    Enter a name for Krile. 
    Anything over 6 characters will be truncated. Alphanumeric only.
    """
    display_name = "Krile's Name"
    default = "Krile"

class FarisName(FreeText):
    """
    Enter a name for Faris. 
    Anything over 6 characters will be truncated. Alphanumeric only.
    """
    display_name = "Faris's Name"
    default = "Faris"

class PianoPercent(Toggle):
    """
    For the memes! Alternatively send goal completed when all pianos are played.
    """
    display_name = "Piano Percent"

@dataclass
class ffvcd_options(PerGameCommonOptions):
    job_palettes: JobPalettes
    four_job: FourJob
    remove_flashes : RemoveFlashes
    world_lock : WorldLock
    progression_checks : ProgressionChecks
    trapped_chests: TrappedChests
    trapped_chests_settings: TrappedChestsSetting
    jobs_included: JobsIncluded
    random_job_count: RandomJobCount
    ability_settings: AbilitySettings
    job_group_abilities_number: JobGroupAbilitiesNumber
    only_usable_magic: OnlyUsableMagic
    disable_tier_1_magic: DisableTier1Magic
    disable_tier_2_magic: DisableTier2Magic
    disable_tier_3_magic: DisableTier3Magic
    kuzar_progression: KuzarProgression
    rift_and_void_progression: RiftAndVoidProgression
    lenna_name: LennaName
    galuf_name: GalufName
    krile_name: KrileName
    faris_name: FarisName
    piano_percent: PianoPercent