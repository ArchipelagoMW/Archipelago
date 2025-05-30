from dataclasses import dataclass
import typing

from Options import OptionGroup, Choice, Range, Toggle, DefaultOnToggle, OptionSet, OptionDict, DeathLink, PerGameCommonOptions, StartInventoryPool
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
    Note: Going over 32 HP may cause visual bugs in either gameplay or the pause menu.
          The max HP is capped at 56.
    """
    display_name = "Starting HP"
    range_start = 1
    range_end = 32
    default = 16

class HeartTankEffectiveness(Range):
    """
    How many units of HP each Heart tank will provide to the user.
    Note: Going over 32 HP may cause visual bugs in either gameplay or the pause menu.
          The max HP is capped at 56.
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
    them together, meaning that a boss can be weak to Charged Rolling Shield but not its
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
    weakness_and_upgraded_buster: Only allow the weakness and buster charge level 3 to deal damage to the bosses
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

class HadoukenInPool(DefaultOnToggle):
    """
    Adds Hadouken to the item pool.
    Hadouken will deal the current HP as damage and half the current HP on strict weakness settings.
    """
    display_name = "Hadouken In Pool"

class EarlyLegs(Toggle):
    """
    Places the Legs Upgrade item in sphere 1.
    """
    display_name = "Early Legs"

class PickupSanity(Toggle):
    """
    Whether collecting freestanding 1ups, HP and Weapon Energy capsules will grant a check.
    """
    display_name = "Pickupsanity"

class LogicBossWeakness(DefaultOnToggle):
    """
    Every main boss will logically expect you to have its weakness.
    """
    display_name = "Boss Weakness Logic"

class LogicLegSigma(DefaultOnToggle):
    """
    Sigma's Fortress will logically expect you to have the legs upgrade.
    """
    display_name = "Sigma's Fortress Legs Upgrade Logic"

class LogicChargedShotgunIce(Toggle):
    """
    Adds Charged Shotgun Ice as logic to some locations. Some of those may be hard to execute.
    """
    display_name = "Charged Shotgun Ice Logic"

class FortressBundleUnlock(Toggle):
    """
    Whether to unlock Sigma's Fortress 1-3 levels as a group or not.
    Unlocking level 4 requires getting all Fortress levels cleared.
    """
    display_name = "Fortress Levels Bundle Unlock"

class SigmaOpen(OptionSet):
    """
    Under which conditions will Sigma's Fortress open.
    If no options are selected a multiworld item granting access to the stage will be created.

    Medals: Consider Maverick medals to get access to the fortress.
    Weapons: Consider weapons to get access to the fortress.
    Armor Upgrades: Consider upgrades to get access to the fortress.
    Heart Tanks: Consider heart tanks to get access to the fortress.
    Sub Tanks: Consider sub tanks to get access to the fortress.
    """
    display_name = "Sigma Fortress Rules"
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

class SigmaMedalCount(Range):
    """
    How many Maverick Medals are required to access Sigma's Fortress.
    """
    display_name = "Sigma Medal Count"
    range_start = 0
    range_end = 8
    default = 8

class SigmaWeaponCount(Range):
    """
    How many weapons are required to access Sigma's Fortress.
    """
    display_name = "Sigma Weapon Count"
    range_start = 0
    range_end = 6
    default = 6

class SigmaArmorUpgradeCount(Range):
    """
    How many armor upgrades are required to access Sigma's Fortress.
    """
    display_name = "Sigma Armor Upgrade Count"
    range_start = 0
    range_end = 4
    default = 3

class SigmaHeartTankCount(Range):
    """
    How many Heart Tanks are required to access Sigma's Fortress.
    """
    display_name = "Sigma Heart Tank Count"
    range_start = 0
    range_end = 6
    default = 6

class SigmaSubTankCount(Range):
    """
    How many Sub Tanks are required to access Sigma's Fortress.
    """
    display_name = "Sigma Sub Tank Count"
    range_start = 0
    range_end = 2
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

class BetterWallJump(Toggle):
    """
    Enables performing a dash wall jump by holding down the button instead of pressing it every time.
    """
    display_name = "Better Wall Jump"

class AirDash(Toggle):
    """
    Adds another Legs Upgrade that allows X to perform an Air Dash.
    """
    display_name = "Air Dash"

class LongJumps(Toggle):
    """
    Allows X to perform longer jumps when holding down the Dash button. Only works after getting a Legs Upgrade.
    """
    display_name = "Long Jumps"

class LogicHelmetCheckpoints(Toggle):
    """
    Makes the "Use Any Checkpoint" feature from the Helmet Upgrade be in logic
    """
    display_name = "Helmet Checkpoints In Logic"

class ChillPenguinTweaks(OptionSet):
    """
    Behavior options for Chill Penguin. Everything can be stacked.
    """
    display_name = "Chill Penguin Tweaks"
    valid_keys = {
        "Random horizontal slide speed",
        "Jumps when starting slide",
        "Random ice block horizontal speed",
        "Random ice block vertical speed",
        "Shoot random amount of ice blocks",
        "Ice block shooting rate enhancer #1",
        "Ice block shooting rate enhancer #2",
        "Ice block shooting rate enhancer #3",
        "Random blizzard strength",
        "Fast falls after jumping",
        "Random mist range",
        "Can't be stunned/set on fire with incoming damage",
        "Can't be set on fire with weakness",
    }
    default = {}


class ArmoredArmadilloTweaks(OptionSet):
    """
    Behavior options for Armored Armadillo. Everything can be stacked.
    """
    display_name = "Armored Armadillo Tweaks"
    valid_keys = {
        "Random bouncing speed",
        "Random bouncing angle",
        "Random energy horizontal speed",
        "Random energy vertical speed",
        "Energy shooting rate enhancer #1",
        "Energy shooting rate enhancer #2",
        "Don't absorb any projectile",
        "Absorbs any projectile except weakness",
        "Don't flinch from incoming damage without armor",
        "Can't block incoming projectiles",
    }
    default = {}


class SparkMandrillTweaks(OptionSet):
    """
    Behavior options for Spark Mandrill. Everything can be stacked.
    """
    display_name = "Spark Mandrill Tweaks"
    valid_keys = {
        "Random Electric Spark speed",
        "Additional Electric Spark #1",
        "Additional Electric Spark #2",
        "Landing creates Electric Spark",
        "Hitting a wall creates Electric Spark",
        "Can't be stunned during Dash Punch with weakness",
        "Can't be frozen with weakness",
    }
    default = {}

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

class PaletteHomingTorpedo(BasePalette):
    """
    Which color to use for X's Homing Torpedo
    """
    display_name = "Homing Torpedo Palette"
    default = 22

class PaletteChameleonSting(BasePalette):
    """
    Which color to use for X's Chameleon Sting
    """
    display_name = "Chameleon Sting Palette"
    default = 23

class PaletteRollingShield(BasePalette):
    """
    Which color to use for X's Rolling Shield
    """
    display_name = "Rolling Shield Palette"
    default = 24

class PaletteFireWave(BasePalette):
    """
    Which color to use for X's Fire Wave
    """
    display_name = "Fire Wave Palette"
    default = 25

class PaletteStormTornado(BasePalette):
    """
    Which color to use for X's Storm Tornado
    """
    display_name = "Storm Tornado Palette"
    default = 26

class PaletteElectricSpark(BasePalette):
    """
    Which color to use for X's Electric Spark
    """
    display_name = "Electric Spark Palette"
    default = 27

class PaletteBoomerangCutter(BasePalette):
    """
    Which color to use for X's Boomerang Cutter
    """
    display_name = "Boomerang Cutter Palette"
    default = 28

class PaletteShotgunIce(BasePalette):
    """
    Which color to use for X's Shotgun Ice
    """
    display_name = "Shotgun Ice Palette"
    default = 29

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

mmx_option_groups = [
    OptionGroup("Gameplay Options", [
        StartingLifeCount,
        StartingHP,
        HeartTankEffectiveness,
        JammedBuster,
        BetterWallJump,
        LongJumps,
        AirDash,
        HadoukenInPool,
        LogicChargedShotgunIce,
        LogicHelmetCheckpoints,
    ]),
    OptionGroup("Sigma Fortress Options", [
        SigmaOpen,
        SigmaMedalCount,
        SigmaWeaponCount,
        SigmaArmorUpgradeCount,
        SigmaHeartTankCount,
        SigmaSubTankCount,
        FortressBundleUnlock,
        LogicLegSigma,
    ]),
    OptionGroup("Boss Weaknesses", [
        BossWeaknessRando,
        PlandoWeaknesses,
        BossWeaknessStrictness,
        BossRandomizedHP,
        LogicBossWeakness,
    ]),
    OptionGroup("Enemy Tweaks", [
        ChillPenguinTweaks,
        ArmoredArmadilloTweaks,
        SparkMandrillTweaks,
    ]),
    OptionGroup("Aesthetic", [
        SetPalettes,
        PaletteDefault,
        PaletteHomingTorpedo,
        PaletteChameleonSting,
        PaletteRollingShield,
        PaletteFireWave,
        PaletteStormTornado,
        PaletteElectricSpark,
        PaletteBoomerangCutter,
        PaletteShotgunIce,
    ]),
]

@dataclass
class MMXOptions(PerGameCommonOptions):
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
    jammed_buster: JammedBuster
    better_walljump: BetterWallJump
    air_dash: AirDash
    long_jumps: LongJumps
    hadouken_in_pool: HadoukenInPool
    pickupsanity: PickupSanity
    early_legs: EarlyLegs
    logic_boss_weakness: LogicBossWeakness
    logic_leg_sigma: LogicLegSigma
    logic_charged_shotgun_ice: LogicChargedShotgunIce
    logic_helmet_checkpoints: LogicHelmetCheckpoints
    sigma_all_levels: FortressBundleUnlock
    sigma_open: SigmaOpen
    sigma_medal_count: SigmaMedalCount
    sigma_weapon_count: SigmaWeaponCount
    sigma_upgrade_count: SigmaArmorUpgradeCount
    sigma_heart_tank_count: SigmaHeartTankCount
    sigma_sub_tank_count: SigmaSubTankCount
    chill_penguin_tweaks: ChillPenguinTweaks
    armored_armadillo_tweaks: ArmoredArmadilloTweaks
    spark_mandrill_tweaks: SparkMandrillTweaks
    player_palettes: SetPalettes
    palette_default: PaletteDefault
    palette_homing_torpedo: PaletteHomingTorpedo
    palette_chameleon_sting: PaletteChameleonSting
    palette_rolling_shield: PaletteRollingShield
    palette_fire_wave: PaletteFireWave
    palette_storm_tornado: PaletteStormTornado
    palette_electric_spark: PaletteElectricSpark
    palette_boomerang_cutter: PaletteBoomerangCutter
    palette_shotgun_ice: PaletteShotgunIce
