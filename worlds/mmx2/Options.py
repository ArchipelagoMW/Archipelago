from dataclasses import dataclass
import typing

from Options import Choice, Range, Toggle, DefaultOnToggle, OptionDict, OptionSet, OptionGroup, DeathLink, PerGameCommonOptions, StartInventoryPool
from schema import Schema, And, Use, Optional

from .Rom import action_buttons, action_names, x_palette_set_offsets
from .Weaknesses import boss_weaknesses, weapons_chaotic

class EnergyLink(DefaultOnToggle):
    """
    Enable EnergyLink support.

    EnergyLink in MMX2 works as a big HP and Weapon Energy pool that the players can use to request HP
    or Weapon Energy whenever they need to.
    
    You make use of this feature by typing /heal <amount> or /refill <amount> in the client.
    """
    display_name = "Energy Link"

class StartingLifeCount(Range):
    """
    How many lives to start the game with.

    Note: This number becomes the new default life count, meaning that it will persist after a game over.
    """
    display_name = "Starting Life Count"
    range_start = 0
    range_end = 99
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

class ShoryukenUseHadoukenInput(Toggle):
    """
    Makes Shoryuken use the Hadouken input.
    """
    display_name = "Shoryuken Uses Hadouken Input"

class PickupSanity(Toggle):
    """
    Whether collecting freestanding 1ups, HP and Weapon Energy capsules will grant a check.
    """
    display_name = "Pickupsanity"

class BaseBossRematchCount(Range):
    """
    How many boss rematches are needed in the fourth X-Hunter's Base stage.
    """
    display_name = "X-Hunter Base 4 Rematch count"
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
    range_end = 6
    default = 6

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
    range_end = 6
    default = 6

class BaseSubTankCount(Range):
    """
    How many Sub Tanks are required to access X-Hunter's Stage.
    """
    display_name = "Base Sub Tank Count"
    range_start = 0
    range_end = 2
    default = 2

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

class LogicHelmetCheckpoints(Toggle):
    """
    Makes the "Use Any Checkpoint" feature from the Helmet Upgrade be in logic
    """
    display_name = "Helmet Checkpoints In Logic"

class BasePalette(Choice):
    """
    Base class for palettes
    """
    option_blue = 0
    option_gold_armor = 1
    option_acid_burst = 6
    option_parasitic_bomb = 7
    option_triad_thunder = 8
    option_spinning_blade = 9
    option_ray_splasher = 10
    option_gravity_well = 11
    option_frost_shield = 12
    option_tornado_fang = 13
    option_crystal_hunter = 14
    option_bubble_splash = 15
    option_silk_shot = 16
    option_spin_wheel = 17
    option_sonic_slicer = 18
    option_strike_chain = 19
    option_magnet_mine = 20
    option_speed_burner = 21
    option_homing_torpedo = 22
    option_chameleon_sting = 23
    option_rolling_shield = 24
    option_fire_wave = 25
    option_storm_tornado = 26
    option_electric_spark = 27
    option_boomerang_cutter = 28
    option_shotgun_ice = 29


class PaletteDefault(BasePalette):
    """
    Which color to use for X's default color
    """
    display_name = "X Palette"
    default = 0

class PaletteCrystalHunter(BasePalette):
    """
    Which color to use for X's Crystal Hunter
    """
    display_name = "Crystal Hunter Palette"
    default = 14

class PaletteBubbleSplash(BasePalette):
    """
    Which color to use for X's Bubble Splash
    """
    display_name = "Bubble Splash Palette"
    default = 15

class PaletteSilkShot(BasePalette):
    """
    Which color to use for X's Silk Shot
    """
    display_name = "Silk Shot Palette"
    default = 16

class PaletteSpinWheel(BasePalette):
    """
    Which color to use for X's Spin Wheel
    """
    display_name = "Spin Wheel Palette"
    default = 17

class PaletteSonicSlicer(BasePalette):
    """
    Which color to use for X's Sonic Slicer
    """
    display_name = "Sonic Slicer Palette"
    default = 18

class PaletteStrikeChain(BasePalette):
    """
    Which color to use for X's Strike Chain
    """
    display_name = "Strike Chain Palette"
    default = 19

class PaletteMagnetMine(BasePalette):
    """
    Which color to use for X's Magnet Mine
    """
    display_name = "Magnet Mine Palette"
    default = 20

class PaletteSpeedBurner(BasePalette):
    """
    Which color to use for X's Speed Burner
    """
    display_name = "Speed Burner Palette"
    default = 21

class SetPalettes(OptionDict):
    """
    Allows you to create colors for each weapon X has. Includes charge levels and Gold Armor customization.
    This will override the option preset
    
    Each one expects 16 values which are mapped to X's colors.
    The values can be in SNES RGB (bgr555) with the $ prefix or PC RGB (rgb888) with the # prefix.
    """
    display_name = "Set Custom Palettes"
    schema = Schema({
        Optional(color_set): list for color_set in x_palette_set_offsets.keys()
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
        ShoryukenUseHadoukenInput,
        XHuntersMedalCount,
        LogicHelmetCheckpoints,
    ]),
    OptionGroup("Boss Weakness Options", [
        BossWeaknessRando,
        PlandoWeaknesses,
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
    OptionGroup("Aesthetic", [
        SetPalettes,
        PaletteDefault,
        PaletteCrystalHunter,
        PaletteBubbleSplash,
        PaletteSilkShot,
        PaletteSpinWheel,
        PaletteSonicSlicer,
        PaletteStrikeChain,
        PaletteMagnetMine,
        PaletteSpeedBurner,
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
    shoryuken_use_hadouken_input: ShoryukenUseHadoukenInput
    logic_helmet_checkpoints: LogicHelmetCheckpoints
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
    player_palettes: SetPalettes
    palette_default: PaletteDefault
    palette_crystal_hunter: PaletteCrystalHunter
    palette_bubble_splash: PaletteBubbleSplash
    palette_silk_shot: PaletteSilkShot
    palette_spin_wheel: PaletteSpinWheel
    palette_sonic_slicer: PaletteSonicSlicer
    palette_strike_chain: PaletteStrikeChain
    palette_magnet_mine: PaletteMagnetMine
    palette_speed_burner: PaletteSpeedBurner
