from dataclasses import dataclass

from Options import Choice, Range, Toggle, ItemDict, PerGameCommonOptions, StartInventoryPool

from worlds.kh2 import default_itempool_option


class SoraEXP(Range):
    """Sora Level Exp Multiplier"""
    display_name = "Sora Level EXP"
    range_start = 1
    range_end = 10
    default = 5


class FinalEXP(Range):
    """Final Form Exp Multiplier"""
    display_name = "Final Form EXP"
    range_start = 1
    range_end = 10
    default = 3


class MasterEXP(Range):
    """Master Form Exp Multiplier"""
    display_name = "Master Form EXP"
    range_start = 1
    range_end = 10
    default = 3


class LimitEXP(Range):
    """Limit Form Exp Multiplier"""
    display_name = "Limit Form EXP"
    range_start = 1
    range_end = 10
    default = 3


class WisdomEXP(Range):
    """Wisdom Form Exp Multiplier"""
    display_name = "Wisdom Form EXP"
    range_start = 1
    range_end = 10
    default = 3


class ValorEXP(Range):
    """Valor Form Exp Multiplier"""
    display_name = "Valor Form EXP"
    range_start = 1
    range_end = 10
    default = 3


class SummonEXP(Range):
    """Summon Exp Multiplier"""
    display_name = "Summon level EXP"
    range_start = 1
    range_end = 10
    default = 5


class Schmovement(Choice):
    """Level of Progressive Movement Abilities You Start With"""
    display_name = "Schmovement"
    option_level_0 = 0
    option_level_1 = 1
    option_level_2 = 2
    option_level_3 = 3
    option_level_4 = 4
    default = 1


class RandomGrowth(Range):
    """Amount of Random Progressive Movement Abilities You Start With"""
    display_name = "Random Starting Growth"
    range_start = 0
    range_end = 20
    default = 0


class KeybladeMin(Range):
    """Minimum Stats for Keyblades"""
    display_name = "Keyblade Minimum Stats"
    range_start = 0
    range_end = 20
    default = 3


class KeybladeMax(Range):
    """Maximum Stats for Keyblades"""
    display_name = "Keyblade Max Stats"
    range_start = 0
    range_end = 20
    default = 7


class Visitlocking(Choice):
    """Determines the level of visit locking

    No Visit Locking: Start with all 25 visit locking items.


    Second Visit Locking: Start with 13 visit locking items for every first visit.


    First and Second Visit Locking: One item for First Visit Two For Second Visit"""
    display_name = "Visit locking"
    option_no_visit_locking = 0  # starts with 25 visit locking
    option_second_visit_locking = 1  # starts with 12 visit locking
    option_first_and_second_visit_locking = 2  # starts with nothing
    default = 2


class FightLogic(Choice):
    """
    The level of logic to use when determining what fights in each KH2 world are beatable.

    Easy: For Players not very comfortable doing things without a lot of tools.

    Normal: For Players somewhat comfortable doing fights with some of the tools.

    Hard: For Players comfortable doing fights with almost no tools.
    """
    display_name = "Fight Logic"
    option_easy = 0
    option_normal = 1
    option_hard = 2
    default = 1


class FinalFormLogic(Choice):
    """Determines forcing final form logic

    No Light and Darkness: Light and Darkness is not in logic.
    Light And Darkness: Final Forcing with light and darkness is in logic.
    Just a Form: All that requires final forcing is another form.
    """
    display_name = "Final Form Logic"
    option_no_light_and_darkness = 0
    option_light_and_darkness = 1
    option_just_a_form = 2
    default = 1


class AutoFormLogic(Toggle):
    """ Have Auto Forms levels in logic.
    """
    display_name = "Auto Form Logic"
    default = False


class RandomVisitLockingItem(Range):
    """Start with random amount of visit locking items."""
    display_name = "Random Visit Locking Item"
    range_start = 0
    range_end = 25
    default = 0


class SuperBosses(Toggle):
    """Terra Sephiroth and Data Fights Toggle."""
    display_name = "Super Bosses"
    default = True


class Cups(Choice):
    """Olympus Cups Toggles
        No Cups: All Cups are placed into Excluded Locations.
        Cups: Hades Paradox Cup is placed into Excluded Locations
        Cups and Hades Paradox: Has Every Cup On."""
    display_name = "Olympus Cups"
    option_no_cups = 0
    option_cups = 1
    option_cups_and_hades_paradox = 2
    default = 0


class LevelDepth(Choice):
    """Determines How many locations you want on levels

    Level 50: 23 checks spread through 50 levels.
    Level 99: 23 checks spread through 99 levels.

    Level 50 sanity: 49 checks spread through 50 levels.
    Level 99 sanity: 98 checks spread through 99 levels.

    Level 1: no checks on levels(checks are replaced with stats)"""
    display_name = "Level Depth"
    option_level_50 = 0
    option_level_99 = 1
    option_level_50_sanity = 2
    option_level_99_sanity = 3
    option_level_1 = 4
    default = 0


class DonaldGoofyStatsanity(Toggle):
    """Toggles if on Donald and Goofy's Get Bonus locations can be any item"""
    display_name = "Donald & Goofy Statsanity"
    default = True


class AtlanticaToggle(Toggle):
    """Atlantica Toggle"""
    display_name = "Atlantica Toggle"
    default = False


class PromiseCharm(Toggle):
    """Add Promise Charm to the pool"""
    display_name = "Promise Charm"
    default = False


class AntiForm(Toggle):
    """Add Anti Form to the pool"""
    display_name = "Anti Form"
    default = False


class Goal(Choice):
    """Win Condition
    Three Proofs: Find the 3 Proofs to unlock the final door.

    Lucky Emblem Hunt: Find required amount of Lucky Emblems.

    Hitlist (Bounty Hunt): Find required amount of Bounties.

    Lucky Emblem and Hitlist: Find the required amount of Lucky Emblems and Bounties."""
    display_name = "Goal"
    option_three_proofs = 0
    option_lucky_emblem_hunt = 1
    option_hitlist = 2
    option_hitlist_and_lucky_emblem = 3
    default = 1


class FinalXemnas(Toggle):
    """Kill Final Xemnas to Beat the Game.

    This is in addition to your Goal.

    I.E. get three proofs+kill final Xemnas"""
    display_name = "Final Xemnas"
    default = True


class LuckyEmblemsRequired(Range):
    """Number of Lucky Emblems to collect to Win/Unlock Final Xemnas' Door.

    If Goal is not Lucky Emblem Hunt or Lucky Emblem and Hitlist this does nothing."""
    display_name = "Lucky Emblems Required"
    range_start = 1
    range_end = 60
    default = 35


class LuckyEmblemsAmount(Range):
    """Number of Lucky Emblems that are in the pool.

    If Goal is not Lucky Emblem Hunt or Lucky Emblem and Hitlist this does nothing."""
    display_name = "Lucky Emblems Available"
    range_start = 1
    range_end = 60
    default = 40


class BountyRequired(Range):
    """Number of Bounties to collect to Win/Unlock Final Xemnas Door.

    If Goal is not Hitlist or Lucky Emblem and Hitlist this does nothing."""
    display_name = "Bounties Required"
    range_start = 1
    range_end = 26
    default = 7


class BountyAmount(Range):
    """Number of Bounties that are in the pool.

    If Goal is not Hitlist or Lucky Emblem and Hitlist this does nothing."""
    display_name = "Bounties Available"
    range_start = 1
    range_end = 26
    default = 10


class BountyStartHint(Toggle):
    """Start with Bounties Hinted"""
    display_name = "Start with Bounties Hinted"
    default = False


class WeaponSlotStartHint(Toggle):
    """Start with Weapon Slots' Hinted"""
    display_name = "Start with Weapon Slots Hinted"
    default = False


class CorSkipToggle(Toggle):
    """Toggle for Cor skip.

    Tools depend on which difficulty was chosen on Fight Difficulty.

    Toggle does not negate fight logic but is an alternative.

    Final Chest is also can be put into logic with this skip.
    """
    display_name = "CoR Skip Toggle."
    default = False


class CustomItemPoolQuantity(ItemDict):
    """Add more of an item into the itempool. Note: You cannot take out items from the pool."""
    display_name = "Custom Item Pool"
    verify_item_name = True
    default = default_itempool_option


class FillerItemsLocal(Toggle):
    """Make all dynamic filler classified items local. Recommended when playing with games with fewer locations than kh2"""
    display_name = "Local Filler Items"
    default = True


class SummonLevelLocationToggle(Toggle):
    """Toggle Summon levels to have locations."""
    display_name = "Summon Level Locations"
    default = False


# shamelessly stolen from the messanger
@dataclass
class KingdomHearts2Options(PerGameCommonOptions):
    start_inventory: StartInventoryPool
    LevelDepth: LevelDepth
    Sora_Level_EXP: SoraEXP
    Valor_Form_EXP: ValorEXP
    Wisdom_Form_EXP: WisdomEXP
    Limit_Form_EXP: LimitEXP
    Master_Form_EXP: MasterEXP
    Final_Form_EXP: FinalEXP
    Summon_EXP: SummonEXP
    Schmovement: Schmovement
    RandomGrowth: RandomGrowth
    AntiForm: AntiForm
    Promise_Charm: PromiseCharm
    Goal: Goal
    FinalXemnas: FinalXemnas
    LuckyEmblemsAmount: LuckyEmblemsAmount
    LuckyEmblemsRequired: LuckyEmblemsRequired
    BountyAmount: BountyAmount
    BountyRequired: BountyRequired
    BountyStartingHintToggle: BountyStartHint
    Keyblade_Minimum: KeybladeMin
    Keyblade_Maximum: KeybladeMax
    WeaponSlotStartHint: WeaponSlotStartHint
    FightLogic: FightLogic
    FinalFormLogic: FinalFormLogic
    AutoFormLogic: AutoFormLogic
    DonaldGoofyStatsanity: DonaldGoofyStatsanity
    FillerItemsLocal: FillerItemsLocal
    Visitlocking: Visitlocking
    RandomVisitLockingItem: RandomVisitLockingItem
    SuperBosses: SuperBosses
    Cups: Cups
    SummonLevelLocationToggle: SummonLevelLocationToggle
    AtlanticaToggle: AtlanticaToggle
    CorSkipToggle: CorSkipToggle
    CustomItemPoolQuantity: CustomItemPoolQuantity
