from dataclasses import dataclass
from Options import Choice, Range, Toggle, PerGameCommonOptions, StartInventoryPool, DefaultOnToggle


class IgnoreCleansing(Toggle):
    """Whether the logic expects Cleansing to touch the water in Underground Waterway or not."""
    display_name = "Ignore Cleansing"


class AutoRun(Toggle):
    """Causes Nathan to always run when pressing left or right without having to double-tap."""
    display_name = "Auto Run"


class DSSPatch(Toggle):
    """Patches being able to pause during the DSS startup animation and switch the cards in the menu to use combos you
    don't currently have."""
    display_name = "DSS Patch"


class AlwaysAllowSpeedDash(Toggle):
    """Allows activating the speed dash combo without needing the Pluto and Griffin cards first."""
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
    """How many Last Keys are in the pool in total."""
    range_start = 0
    range_end = 9
    default = 1
    display_name = "Available Last Keys"


class BuffRangedFamiliars(Toggle):
    """Makes Familiar projectiles do double damage."""
    display_name = "Buff Ranged Familiars"


class BuffSubWeapons(Toggle):
    """Increases damage dealt via sub-weapons and item crushes. Stacks with Shooter Mode buffs."""
    display_name = "Buff Sub-weapons"


class BuffShooterStrength(Toggle):
    """Increases Nathan's strength in Shooter Mode to be his strength in Vampire Killer Mode."""
    display_name = "Buff Shooter Strength"


class ItemDropRandomization(Choice):
    """Disabled: No item drop randomization; enemies will drop their vanilla items.
    Normal: Any enemy and boss can drop anything. Valuable items will more likely be dropped by harder enemies.
    Hard: Enemies with less than 150 HP will only drop low-tier items and rare items can only drop from bosses."""
    display_name = "Item Drop Randomization"
    option_disabled = 0
    option_normal = 1
    option_hard = 2
    default = 1


class HalveDSSCardsPlaced(Toggle):
    """Places only half of the DSS cards in the item pool. The cards left out can be
    any number of Action and Attribute ones."""
    display_name = "Halve DSS Cards Placed"


class Countdown(Toggle):
    """Displays, below and near the right side of the health HUD, the number of unobtained progression-marked items
    and DSS cards in the area you are currently in."""
    display_name = "Countdown"


class SubWeaponShuffle(Toggle):
    """Shuffles all sub-weapons in the game within each other in their own pool."""
    display_name = "Sub-weapon Shuffle"


class DisableBattleArenaMPDrain(Toggle):
    """Makes the Battle Arena not drain Nathan's MP, so that DSS combos can be freely used."""
    display_name = "Disable Battle Arena MP Drain"


class RequireAllBosses(Toggle):
    """Forces a Last Key behind every boss and requires all 8 of them to enter the Ceremonial Room.
    The Required and Available Last Keys settings will both be forced to 8."""
    display_name = "Require All Bosses"


class EarlyDouble(DefaultOnToggle):
    """Ensures the Double will be placed somewhere within the Catacombs in your own game, accessible with nothing."""
    display_name = "Early Double"


@dataclass
class CVCotMOptions(PerGameCommonOptions):
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
    start_inventory_from_pool: StartInventoryPool
