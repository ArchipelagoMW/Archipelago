from dataclasses import dataclass
import typing

from Options import Choice, Range, Toggle, DefaultOnToggle, OptionDict, OptionSet, OptionGroup, DeathLink, PerGameCommonOptions, StartInventoryPool
from schema import Schema, And, Use, Optional

from .Rom import action_buttons, action_names
from .Weaknesses import boss_weaknesses, weapons_chaotic

class EnergyLink(DefaultOnToggle):
    """
    Enable EnergyLink support.

    EnergyLink in MMX2 works as a big HP and Weapon Energy pool that the players can use to request HP
    or Weapon Energy whenever they need to.
    
    You make use of this feature by typing /pool, /heal <amount>, /refill <amount> or /autoheal in the client.
    """
    display_name = "Energy Link"

class StartingLifeCount(Range):
    """
    How many lives to start the game with.

    Note: This number becomes the new default life count, meaning that it will persist after a game over.
    """
    display_name = "Starting Life Count"
    range_start = 0
    range_end = 9
    default = 2

class StartingHP(Range):
    """
    How much HP X will have at the start of the game.

    Notes: Going over 32 HP may cause visual bugs in either gameplay or the pause menu. The max HP is capped at 56.
    """
    display_name = "Starting HP"
    range_start = 1
    range_end = 32
    default = 16

class HeartTankEffectiveness(Range):
    """
    How many units of HP each Heart tank will provide to the user.

    Note: Going over 32 HP may cause visual bugs in either gameplay or the pause menu. The max HP is capped at 56.
    """
    display_name = "Heart Tank Effectiveness"
    range_start = 1
    range_end = 8
    default = 2

class BossWeaknessRando(Choice):
    """
    Every main boss will have its weakness randomized.

    vanilla: Bosses retain their original weaknesses
    shuffled: Bosses have their weaknesses shuffled
    chaotic_double: Bosses will have two random weaknesses under the chaotic set
    chaotic_single: Bosses will have one random weakness under the chaotic set

    The chaotic set makes every weapon charge level a separate weakness instead of keeping
    them together, meaning that a boss can be weak to Charged Silk Shot but not its
    uncharged version.
    """
    display_name = "Boss Weakness Randomization"
    option_vanilla = 0
    option_shuffled = 1
    option_chaotic_double = 3
    option_chaotic_single = 2
    default = 0

class BossWeaknessStrictness(Choice):
    """
    How strict boss weaknesses will be.

    not_strict: Allow every weapon to deal damage to the bosses
    weakness_and_buster: Only allow the weakness and buster to deal damage to the bosses
    weakness_and_upgraded_buster: Only allow the weakness and buster charge levels 3 to deal damage to the bosses
    only_weakness: Only the weakness will deal damage to the bosses
    """
    display_name = "Boss Weakness Strictness"
    option_not_strict = 0
    option_weakness_and_buster = 1
    option_weakness_and_upgraded_buster = 2
    option_only_weakness = 3
    default = 0

class BossRandomizedHP(Choice):
    """
    Wheter to randomize the boss' hp or not.

    off: Bosses' HP will not be randomized
    weak: Bosses will have [1,32] HP
    regular: Bosses will have [16,48] HP
    strong: Bosses will have [32,64] HP
    chaotic: Bosses will have [1,64] HP
    """
    display_name = "Boss Randomize HP"
    option_off = 0
    option_weak = 1
    option_regular = 2
    option_strong = 3
    option_chaotic = 4
    default = 0

class JammedBuster(Toggle):
    """
    Jams X's buster making it only able to shoot lemons.
    Note: This adds another Arms Upgrade into the item pool.
    """
    display_name = "Jammed Buster"

class LongJumps(Toggle):
    """
    Allows X to perform longer jumps when holding down the Dash button.
    """
    display_name = "Long Jumps"

class LogicBossWeakness(DefaultOnToggle):
    """
    Most bosses will logically expect you to have its weakness.

    This option will be forced if the Boss Weakness Strictness setting is set to require only the weakness or
    the upgraded buster option.
    """
    display_name = "Boss Weakness Logic"

class ShoryukenInPool(DefaultOnToggle):
    """
    Adds Shoryuken to the item pool.
    """
    display_name = "Shoryuken In Pool"

class PickupSanity(Toggle):
    """
    Whether collecting freestanding 1ups, HP and Weapon Energy capsules will grant a check.
    """
    display_name = "Pickupsanity"

class BaseBossRematchCount(Range):
    """
    How many boss rematches are needed in the fourth X-Hunter's Base stage.
    """
    display_name = "Doppler Lab 3 Rematch count"
    range_start = 0
    range_end = 8
    default = 8

class BaseBundleUnlock(Toggle):
    """
    Whether to unlock X-Hunter's Base 1-4 levels as a group or not.

    Unlocking level 5 requires getting all X-Hunter's Base levels cleared.
    """
    display_name = "Base Levels Bundle Unlock"

class BaseOpen(OptionSet):
    """
    Under which conditions will X-Hunter's Base open.
    If no options are selected a multiworld item granting access to the lab will be created.

    Medals: Consider Maverick medals to get access to the lab.
    Weapons: Consider weapons to get access to the lab.
    Armor Upgrades: Consider upgrades to get access to the lab.
    Heart Tanks: Consider heart tanks to get access to the lab.
    Sub Tanks: Consider sub tanks to get access to the lab.
    """
    display_name = "Base Rules"
    valid_keys = {
        "Medals",
        "Weapons",
        "Armor Upgrades",
        "Heart Tanks",
        "Sub Tanks",
    }
    default = {
        "Medals",
    }

class BaseMedalCount(Range):
    """
    How many Maverick Medals are required to access X-Hunter's Stage.
    """
    display_name = "Base Medal Count"
    range_start = 0
    range_end = 8
    default = 8

class BaseWeaponCount(Range):
    """
    How many weapons are required to access X-Hunter's Stage.
    """
    display_name = "Base Weapon Count"
    range_start = 0
    range_end = 8
    default = 8

class BaseArmorUpgradeCount(Range):
    """
    How many armor upgrades are required to access X-Hunter's Stage.
    """
    display_name = "Base Armor Upgrade Count"
    range_start = 0
    range_end = 4
    default = 4

class BaseHeartTankCount(Range):
    """
    How many Heart Tanks are required to access X-Hunter's Stage.
    """
    display_name = "Base Heart Tank Count"
    range_start = 0
    range_end = 8
    default = 8

class BaseSubTankCount(Range):
    """
    How many Sub Tanks are required to access X-Hunter's Stage.
    """
    display_name = "Base Sub Tank Count"
    range_start = 0
    range_end = 4
    default = 4

class XHuntersMedalCount(Range):
    """
    How many Maverick Medals are required to allow X-Hunters to spawn on the main map.
    """
    display_name = "X-Hunters Medal Count"
    range_start = 0
    range_end = 5
    default = 2

class ButtonConfiguration(OptionDict):
    """
    Default buttons for every action.
    """
    display_name = "Button Configuration"
    schema = Schema({action_name: And(str, Use(str.upper), lambda s: s in action_buttons) for action_name in action_names})
    default = {
        "SHOT": "Y",
        "JUMP": "B",
        "DASH": "A",
        "SELECT_L": "L",
        "SELECT_R": "R",
        "MENU": "START"
    }

class PlandoWeaknesses(OptionDict):
    """
    Forces bosses to have a specific weakness. Uses the names that appear on the chaotic weakness set.

    Format: 
      Boss Name: Weakness Name
    """
    display_name = "Button Configuration"
    schema = Schema({
        Optional(boss_name): 
            And(str, lambda weapon: weapon in weapons_chaotic.keys()) for boss_name in boss_weaknesses.keys()
    })
    default = {}


mmx2_option_groups = [
    OptionGroup("Gameplay Options", [
        StartingLifeCount,
        StartingHP,
        HeartTankEffectiveness,
        JammedBuster,
        LongJumps,
        ShoryukenInPool,
        XHuntersMedalCount,
    ]),
    OptionGroup("Boss Weakness Options", [
        BossWeaknessRando,
        BossWeaknessStrictness,
        BossRandomizedHP,
        LogicBossWeakness,
    ]),
    OptionGroup("X-Hunter's Base Options", [
        BaseOpen,
        BaseMedalCount,
        BaseWeaponCount,
        BaseArmorUpgradeCount,
        BaseHeartTankCount,
        BaseSubTankCount,
        BaseBossRematchCount,
        BaseBundleUnlock,
    ]),
]

@dataclass
class MMX2Options(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    death_link: DeathLink
    energy_link: EnergyLink
    button_configuration: ButtonConfiguration
    starting_life_count: StartingLifeCount
    starting_hp: StartingHP
    heart_tank_effectiveness: HeartTankEffectiveness
    boss_weakness_rando: BossWeaknessRando
    boss_weakness_strictness: BossWeaknessStrictness
    boss_weakness_plando: PlandoWeaknesses
    boss_randomize_hp: BossRandomizedHP
    pickupsanity: PickupSanity
    jammed_buster: JammedBuster
    long_jumps: LongJumps
    shoryuken_in_pool: ShoryukenInPool
    logic_boss_weakness: LogicBossWeakness
    base_boss_rematch_count: BaseBossRematchCount
    base_all_levels: BaseBundleUnlock
    base_open: BaseOpen
    base_medal_count: BaseMedalCount
    base_weapon_count: BaseWeaponCount
    base_upgrade_count: BaseArmorUpgradeCount
    base_heart_tank_count: BaseHeartTankCount
    base_sub_tank_count: BaseSubTankCount
    x_hunters_medal_count: XHuntersMedalCount
