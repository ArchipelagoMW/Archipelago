from dataclasses import dataclass
from Options import OptionGroup, Choice, Range, Toggle, PerGameCommonOptions, StartInventoryPool, DeathLink


class IgnoreCleansing(Toggle):
    """
    Removes the logical requirement for the Cleansing to go beyond the first Underground Waterway rooms from either of the area's sides. You may be required to brave the harmful water without it.
    """
    display_name = "Ignore Cleansing"


class AutoRun(Toggle):
    """
    Makes Nathan always run when pressing left or right without needing to double-tap.
    """
    display_name = "Auto Run"


class DSSPatch(Toggle):
    """
    Patches out being able to pause during the DSS startup animation and switch the cards in the menu to use any combos you don't currently have, as well as changing the element of a summon to one you don't currently have.
    """
    display_name = "DSS Patch"


class AlwaysAllowSpeedDash(Toggle):
    """
    Allows activating the speed dash combo (Pluto + Griffin) without needing the respective cards first.
    """
    display_name = "Always Allow Speed Dash"


class IronMaidenBehavior(Choice):
    """
    Sets how the iron maiden barriers blocking the entrances to Underground Gallery and Waterway will behave.
    Vanilla: Vanilla behavior. Must press the button guarded by Adramelech to break them.
    Start Broken: The maidens will be broken from the start.
    Detonator In Pool: Adds a Maiden Detonator item in the pool that will detonate the maidens when found. Adramelech will guard an extra check.
    """
    display_name = "Iron Maiden Behavior"
    option_vanilla = 0
    option_start_broken = 1
    option_detonator_in_pool = 2


class RequiredLastKeys(Range):
    """
    How many Last Keys are needed to open the door to the Ceremonial Room. This will lower if higher than Available Last Keys.
    """
    range_start = 0
    range_end = 9
    default = 1
    display_name = "Required Last Keys"


class AvailableLastKeys(Range):
    """
    How many Last Keys are in the pool in total.
    To see this in-game, select the Last Key in the Magic Item menu (when you have at least one) or touch the Ceremonial Room door.
    """
    range_start = 0
    range_end = 9
    default = 1
    display_name = "Available Last Keys"


class BuffRangedFamiliars(Toggle):
    """
    Makes Familiar projectiles deal double damage to enemies.
    """
    display_name = "Buff Ranged Familiars"


class BuffSubWeapons(Toggle):
    """
    Increases damage dealt by sub-weapons and item crushes in Shooter and non-Shooter Modes.
    """
    display_name = "Buff Sub-weapons"


class BuffShooterStrength(Toggle):
    """
    Increases Nathan's strength in Shooter Mode to match his strength in Vampire Killer Mode.
    """
    display_name = "Buff Shooter Strength"


class ItemDropRandomization(Choice):
    """
    Randomizes what enemies drop what items as well as the drop rates for said items.
    Bosses and candle enemies will be guaranteed to have high-tier items in all of their drop slots, and "easy" enemies (below 61 HP) will only drop low-tier items in all of theirs.
    All other enemies will drop a low or mid-tier item in their common drop slot, and a low, mid, or high-tier item in their rare drop slot.
    The common slot item has a 6-10% base chance of appearing, and the rare has a 3-6% chance.
    If Tiered is chosen, all enemies below 144 (instead of 61) HP will be considered "easy", rare items that land on bosses will be exclusive to them, enemies with 144-369 HP will have a low-tier in its common slot and a mid-tier in its rare slot, and enemies with more than 369 HP will have a mid-tier in its common slot and a high-tier in its rare slot.
    See the Game Page for more info.
    """
    display_name = "Item Drop Randomization"
    option_disabled = 0
    option_normal = 1
    option_tiered = 2
    default = 1


class HalveDSSCardsPlaced(Toggle):
    """
    Places only half of the DSS Cards in the item pool.
    A valid combo that lets you freeze or petrify enemies to use as platforms will always be placed.
    """
    display_name = "Halve DSS Cards Placed"


class Countdown(Choice):
    """
    Displays, below and near the right side of the MP bar, the number of un-found progression/useful-marked items or the total check locations remaining in the area you are currently in.
    """
    display_name = "Countdown"
    option_none = 0
    option_majors = 1
    option_all_locations = 2
    default = 0


class SubWeaponShuffle(Toggle):
    """
    Randomizes which sub-weapon candles have which sub-weapons.
    The total available count of each sub-weapon will be consistent with that of the vanilla game.
    """
    display_name = "Sub-weapon Shuffle"


class DisableBattleArenaMPDrain(Toggle):
    """
    Makes the Battle Arena not drain Nathan's MP, so that DSS combos can be used like normal.
    """
    display_name = "Disable Battle Arena MP Drain"


class RequiredSkirmishes(Choice):
    """
    Forces a Last Key after every boss or after every boss and the Battle Arena and forces the required Last Keys to enter the Ceremonial Room to 8 or 9 for All Bosses and All Bosses And Arena respectively.
    The Available and Required Last Keys options will be overridden to the respective values.
    """
    display_name = "Required Skirmishes"
    option_none = 0
    option_all_bosses = 1
    option_all_bosses_and_arena = 2
    default = 0


class EarlyEscapeItem(Choice):
    """
    Ensures the chosen Catacomb escape item will be placed in a starting location within your own game, accessible with nothing.
    """
    display_name = "Early Escape Item"
    option_none = 0
    option_double = 1
    option_roc_wing = 2
    option_double_or_roc_wing = 3
    default = 1


class NerfRocWing(Toggle):
    """
    Initially nerfs the Roc Wing by removing its ability to jump infinitely and reducing its jump height. You can power it back up to its vanilla behavior by obtaining the following:
    Double: Allows one jump in midair, using your double jump.
    Kick Boots: Restores its vanilla jump height.
    Both: Enables infinite midair jumping.
    Note that holding A while Roc jumping will cause you to rise slightly higher; this is accounted for in logic.
    """
    display_name = "Nerf Roc Wing"


class PlutoGriffinAirSpeed(Toggle):
    """
    Increases Nathan's air speeds with the Pluto + Griffin combo active to be the same as his ground speeds. Anything made possible with the increased air speed is out of logic.
    """
    display_name = "DSS Pluto and Griffin Run Speed in Air"


class SkipDialogues(Toggle):
    """
    Skips all cutscene dialogue besides the ending.
    """
    display_name = "Skip Cutscene Dialogue"


class SkipTutorials(Toggle):
    """
    Skips all Magic Item and DSS-related tutorial textboxes.
    """
    display_name = "Skip Magic Item Tutorials"


class BattleArenaMusic(Choice):
    """
    Enables any looping song from the game to play inside the Battle Arena instead of it being silent the whole time.
    """
    display_name = "Battle Arena Music"
    option_nothing = 0
    option_requiem = 1
    option_a_vision_of_dark_secrets = 2
    option_inversion = 3
    option_awake = 4
    option_the_sinking_old_sanctuary = 5
    option_clockwork = 6
    option_shudder = 7
    option_fate_to_despair = 8
    option_aquarius = 9
    option_clockwork_mansion = 10
    option_big_battle = 11
    option_nightmare = 12
    option_vampire_killer = 13
    option_illusionary_dance = 14
    option_proof_of_blood = 15
    option_repose_of_souls = 16
    option_circle_of_the_moon = 17
    default = 0


class CVCotMDeathLink(Choice):
    __doc__ = (DeathLink.__doc__ +
               "\n\n    Received DeathLinks will not kill you in the Battle Arena unless Arena On is chosen.")
    display_name = "Death Link"
    option_off = 0
    alias_false = 0
    alias_no = 0
    option_on = 1
    alias_true = 1
    alias_yes = 1
    option_arena_on = 2
    default = 0


class CompletionGoal(Choice):
    """
    The goal for game completion. Can be defeating Dracula, winning in the Battle Arena, or both.
    If you aren't sure which one you have while playing, select the Dash Boots in the Magic Item menu.
    """
    display_name = "Completion Goal"
    option_dracula = 0
    option_battle_arena = 1
    option_battle_arena_and_dracula = 2
    default = 0


@dataclass
class CVCotMOptions(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    completion_goal: CompletionGoal
    ignore_cleansing: IgnoreCleansing
    auto_run: AutoRun
    dss_patch: DSSPatch
    always_allow_speed_dash: AlwaysAllowSpeedDash
    iron_maiden_behavior: IronMaidenBehavior
    required_last_keys: RequiredLastKeys
    available_last_keys: AvailableLastKeys
    buff_ranged_familiars: BuffRangedFamiliars
    buff_sub_weapons: BuffSubWeapons
    buff_shooter_strength: BuffShooterStrength
    item_drop_randomization: ItemDropRandomization
    halve_dss_cards_placed: HalveDSSCardsPlaced
    countdown: Countdown
    sub_weapon_shuffle: SubWeaponShuffle
    disable_battle_arena_mp_drain: DisableBattleArenaMPDrain
    required_skirmishes: RequiredSkirmishes
    pluto_griffin_air_speed: PlutoGriffinAirSpeed
    skip_dialogues: SkipDialogues
    skip_tutorials: SkipTutorials
    nerf_roc_wing: NerfRocWing
    early_escape_item: EarlyEscapeItem
    battle_arena_music: BattleArenaMusic
    death_link: CVCotMDeathLink


cvcotm_option_groups = [
    OptionGroup("difficulty", [
        BuffRangedFamiliars, BuffSubWeapons, BuffShooterStrength, ItemDropRandomization, IgnoreCleansing,
        HalveDSSCardsPlaced, SubWeaponShuffle, EarlyEscapeItem, CVCotMDeathLink]),
    OptionGroup("quality of life", [
        AutoRun, DSSPatch, AlwaysAllowSpeedDash, PlutoGriffinAirSpeed, Countdown, DisableBattleArenaMPDrain,
        SkipDialogues, SkipTutorials, BattleArenaMusic])
]
