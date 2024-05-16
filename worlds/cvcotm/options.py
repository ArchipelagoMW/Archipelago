from dataclasses import dataclass
from Options import Choice, Range, Toggle, PerGameCommonOptions, StartInventoryPool, DefaultOnToggle


class IgnoreCleansing(Toggle):
    """Makes the Cleansing not logically expected to traverse the water in Underground Waterway."""
    display_name = "Ignore Cleansing"


class AutoRun(Toggle):
    """Causes Nathan to always run when pressing left or right without having to double-tap."""
    display_name = "Auto Run"


class DSSPatch(Toggle):
    """Patches being able to pause during the DSS startup animation and switch the cards in the menu to use any combos
    you don't currently have."""
    display_name = "DSS Patch"


class AlwaysAllowSpeedDash(Toggle):
    """Allows activating the speed dash combo (Pluto + Griffin) without needing the respective cards first."""
    display_name = "Always Allow Speed Dash"


class BreakIronMaidens(Toggle):
    """Breaks the iron maiden barriers from the start of the game, so you will not have to climb Chapel Tower and defeat
    Adramelech to go past them."""
    display_name = "Break Iron Maidens"


class RequiredLastKeys(Range):
    """How many Last Keys are needed to open the door to the Ceremonial
    Room. This will lower if higher than Available Last Keys."""
    range_start = 0
    range_end = 9
    default = 1
    display_name = "Required Last Keys"


class AvailableLastKeys(Range):
    """How many Last Keys are in the pool in total.
    To see this in-game, check the Last Key in the Magic Item menu or touch the Ceremonial Room door."""
    range_start = 0
    range_end = 9
    default = 1
    display_name = "Available Last Keys"


class BuffRangedFamiliars(Toggle):
    """Makes Familiar projectiles do double damage."""
    display_name = "Buff Ranged Familiars"


class BuffSubWeapons(Toggle):
    """Increases damage dealt by sub-weapons and item crushes in Shooter and non-Shooter Modes."""
    display_name = "Buff Sub-weapons"


class BuffShooterStrength(Toggle):
    """Increases Nathan's strength in Shooter Mode to match his strength in Vampire Killer Mode."""
    display_name = "Buff Shooter Strength"


class ItemDropRandomization(Choice):
    """Randomizes what enemies drop what items as well as the drop rates for said items.
    Bosses and candle enemies will be guaranteed to have rare items in all of
    their drop slots, and easily-farmable enemies (like most that infinitely spawn) will only drop low-tier items in
    all of theirs. All other enemies will drop a low or regular-tier item in their common drop slot, and a low, regular,
    or rare-tier item in their rare drop slot. The common slot item has a 5-10% base chance of appearing, and the
    rare has a 3-5% chance.
    If Hard is chosen, all enemies below 150 HP will be considered easily-farmable (in addition to the ones that
    already are) and rare items that land on bosses and candle enemies will be exclusive to them."""
    display_name = "Item Drop Randomization"
    option_disabled = 0
    option_normal = 1
    option_hard = 2
    default = 1


class HalveDSSCardsPlaced(Toggle):
    """Places only half of the DSS Cards in the item pool.
    A valid combo that lets you freeze or petrify enemies as platforms will always be placed."""
    display_name = "Halve DSS Cards Placed"


class Countdown(Choice):
    """Displays, below and near the right side of the MP bar, the number of un-found progression/useful-marked items or
    the total check locations remaining in the area you are currently in."""
    display_name = "Countdown"
    option_none = 0
    option_majors = 1
    option_all_locations = 2
    default = 0


class SubWeaponShuffle(Toggle):
    """Randomizes which sub-weapon candles have which sub-weapons.
    The total count of each sub-weapon will be consistent with that of the vanilla game."""
    display_name = "Sub-weapon Shuffle"


class DisableBattleArenaMPDrain(Toggle):
    """Makes the Battle Arena not drain Nathan's MP, so that DSS combos can be freely used."""
    display_name = "Disable Battle Arena MP Drain"


class RequireAllBosses(Toggle):
    """Forces a Last Key behind every boss and requires all 8 of them to enter the Ceremonial Room.
    The Required and Available Last Keys options will both be forced to 8."""
    display_name = "Require All Bosses"


class EarlyDouble(DefaultOnToggle):
    """Ensures the Double will be placed somewhere within the Catacomb in your own game, accessible with nothing."""
    display_name = "Early Double"


class DeathLink(Choice):
    """When you die, everyone dies. Of course the reverse is true too.
    Received DeathLinks will not kill you in the Battle Arena unless Arena On is chosen."""
    display_name = "DeathLink"
    option_off = 0
    alias_no = 0
    alias_true = 1
    alias_yes = 1
    option_on = 1
    option_arena_on = 2
    default = 0


class CompletionGoal(Choice):
    """The goal for game completion. Can be defeating Dracula, winning in the Battle Arena, or both.
    If you aren't sure which one you have while playing, check the Dash Boots in the Magic Item menu."""
    display_name = "Completion Goal"
    option_dracula = 0
    option_battle_arena = 1
    option_battle_arena_and_dracula = 2
    default = 0


@dataclass
class CVCotMOptions(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    ignore_cleansing: IgnoreCleansing
    auto_run: AutoRun
    dss_patch: DSSPatch
    always_allow_speed_dash: AlwaysAllowSpeedDash
    break_iron_maidens: BreakIronMaidens
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
    require_all_bosses: RequireAllBosses
    early_double: EarlyDouble
    death_link: DeathLink
    completion_goal: CompletionGoal
