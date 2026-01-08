from dataclasses import dataclass
from Options import (Toggle, Range, PerGameCommonOptions, StartInventoryPool,
                     OptionGroup, FreeText, Visibility, DefaultOnToggle, Choice)


class TrophiesRequired(Range):
    """How many Trophies need to be found to complete the seed."""
    display_name = "Trophies Required"
    range_start = 1
    range_end = 293
    default = 100

class TrophiesExtra(Range):
    """How many extra Trophies will be in the item pool. Total trophies cannot exceed 293."""
    display_name = "Extra Trophies"
    range_start = 0
    range_end = 293
    default = 50

class BonusSanity(Toggle):
    """Enables Bonuses as checks. Which bonuses are enabled can be tweaked."""
    display_name = "Bonus-sanity"

class EventSanity(Toggle):
    """Enables all Event match clears as checks. If this is disabled, events
        with major unlocks will still give checks."""
    display_name = "Eventsanity"

class GoalGigaBowser(DefaultOnToggle):
    """If enabled, you will need to defeat Giga Bowser in Adventure Mode and collect your required trophies to win.
       This option can stack with other Goals."""
    display_name = "Giga Bowser Goal"

class GoalCrazyHand(Toggle):
    """If enabled, you will need to defeat Crazy Hand in Classic Mode and collect your required trophies to win.
       This option can stack with other Goals."""
    display_name = "Crazy Hand Goal"

class GoalEvent51(Toggle):
    """If enabled, you will need to complete Event 51 and collect your required trophies to win.
       This option can stack with other Goals."""
    display_name = "Event 51 Goal"

class GoalAllEvents(Toggle):
    """If enabled, you will need to complete every event besides 51 and collect your required trophies to win.
       This option can stack with other Goals."""
    display_name = "All Events Goal"

class RarePokemonChecks(Toggle):
    """Enables 2 checks for seeing Mew and Celebi as well as 2 related Bonus checks."""
    display_name = "Pokemon Bonus Checks"

class HardBonuses(Toggle):
    """Enables a few specific difficult Bonus checks. Does nothing with Bonus-sanity off, such as All Variations or bonuses which are easier with 2 human players."""
    display_name = "Hard Bonus Checks"

class ExtremeBonuses(Toggle):
    """Enables a few very difficult Bonus checks, such as Hammer Throw or No-Damage Clear. Does nothing with Bonus-sanity off."""
    display_name = "Extreme Bonus Checks"

class DiskunTrophyCheck(Toggle):
    """Enables a check on the Diskun trophy, which requires getting all 249 Bonuses."""
    display_name = "Diskun Check"

class MewtwoUnlockCheck(Toggle):
    """Enables a check on unlocking Mewtwo, which requires 1 total hour of VS play."""
    display_name = "Mewtwo Check"

class GoalTargets(Toggle):
    """If enabled, you will need to complete Target Test with every character and collect your required trophies to win.
       This option can stack with other Goals."""
    display_name = "All Targets Goal"

class AnnoyingMultiMan(Toggle):
    """Enables checks on 15-Minute and Cruel Melee"""
    display_name = "Annoying Multi-Man Checks"

class VsCountChecks(Toggle):
    """Enables checks on VS match counts. WARNING. These are really high and will likely take a long time."""
    display_name = "VS Count Checks"

class LotteryPool(Choice):
    """Changes how the Lottery Trophy pool works.
       Vanilla: The lottery pool expands when meeting the vanilla requirement. The 200 VS trophies are unlocked with 5 matches instead.
       Progressive: The lottery pool will increase every time you get a Progressive Lottery Pool item.
       Non-progressive: The lottery pool has specific upgrade items"""
    display_name = "Lottery Pool Mode"
    option_vanilla = 0
    option_progressive = 1
    option_non_progressive = 2
    default = 1

class SoloCSmash(DefaultOnToggle):
    """Enables the use of Smash Attacks with the C-Stick during 1-Player modes."""
    display_name = "1-P C Smash"

class TargetSanity(Toggle):
    """Enables a check for every individual character's Target Test being cleared."""
    display_name = "Target Clear Checks"

class LongTargetChecks(Toggle):
    """Enables Target Test checks locked behind most or all characters."""
    display_name = "Long Target Test Checks"

class DisableTapJump(Toggle):
    """Removes the ability to jump by tapping Up on the control stick."""
    display_name = "Disable Tap Jump"

class HardModeClears(Toggle):
    """Enables checks for completing the main 1-P Modes on Hard or higher."""
    display_name = "Hard Mode Clears"

class StartingCharacter(Choice):
    """This is the character you will start with."""
    display_name = "Starting Character"
    option_dr_mario = 0
    option_mario = 1
    option_luigi = 2
    option_bowser = 3
    option_peach = 4
    option_yoshi = 5
    option_donkey_kong = 6
    option_captain_falcon = 7
    option_ganondorf = 8
    option_falco = 9
    option_fox = 10
    option_ness = 11
    option_ice_climbers = 12
    option_kirby = 13
    option_samus = 14
    option_zelda = 15
    option_link = 16
    option_young_link = 17
    option_pichu = 18
    option_pikachu = 19
    option_jigglypuff = 20
    option_mewtwo = 21
    option_mr_game_and_watch = 22
    option_marth = 23
    option_roy = 24
    default = "random"

class TenManSanity(Toggle):
    """Enables a check for every individual character clearing 10-Man Melee"""
    display_name = "Ten-Man Sanity"

@dataclass
class SSBMOptions(PerGameCommonOptions):
    starting_character: StartingCharacter
    trophies_required: TrophiesRequired
    extra_trophies: TrophiesExtra
    bonus_checks: BonusSanity
    target_checks: TargetSanity
    ten_man_checks: TenManSanity
    enable_rare_pokemon_checks: RarePokemonChecks
    enable_hard_bonuses: HardBonuses
    enable_extreme_bonuses: ExtremeBonuses
    enable_annoying_multiman_checks: AnnoyingMultiMan
    diskun_trophy_check: DiskunTrophyCheck
    mewtwo_unlock_check: MewtwoUnlockCheck
    vs_count_checks: VsCountChecks
    hard_modes_clear: HardModeClears
    long_targettest_checks: LongTargetChecks
    lottery_pool_mode: LotteryPool
    event_checks: EventSanity
    goal_giga_bowser: GoalGigaBowser
    goal_crazy_hand: GoalCrazyHand
    goal_event_51: GoalEvent51
    goal_all_events: GoalAllEvents
    goal_all_targets: GoalTargets
    solo_cstick_smash: SoloCSmash
    disable_tap_jump: DisableTapJump
    start_inventory_from_pool: StartInventoryPool


ssbm_option_groups = [
    OptionGroup("Starting Options", [
        StartingCharacter
    ]),

    OptionGroup("Trophy Settings", [
        TrophiesRequired,
        TrophiesExtra,
    ]),

    OptionGroup("Check Settings", [
        BonusSanity,
        EventSanity,
        TargetSanity,
        TenManSanity
    ]),

    OptionGroup("Annoying Checks", [
        HardBonuses,
        RarePokemonChecks,
        ExtremeBonuses,
        AnnoyingMultiMan,
        VsCountChecks,
        DiskunTrophyCheck,
        MewtwoUnlockCheck,
        LongTargetChecks,
        HardModeClears
    ]),

    OptionGroup("Goal Settings", [
        GoalGigaBowser,
        GoalCrazyHand,
        GoalEvent51,
        GoalAllEvents,
        GoalTargets
    ]),

    OptionGroup("QOL Settings", [
        SoloCSmash,
        DisableTapJump
    ]),
]
