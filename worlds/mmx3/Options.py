from dataclasses import dataclass
import typing

from Options import Choice, Range, Toggle, DefaultOnToggle, OptionGroup, OptionDict, OptionSet, DeathLink, PerGameCommonOptions, StartInventoryPool
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
    them together, meaning that a boss can be weak to Charged Frost Shield but not its
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
    weakness_and_upgraded_buster: Only allow the weakness and buster charge levels 3 & 4 to deal damage to the bosses
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

class DisableChargeFreeze(DefaultOnToggle):
    """
    Allows X and Zero to move while shooting a level 3 charged shot.
    """
    display_name = "Disable Level 3 Charge freeze after shooting"

class LongJumps(Toggle):
    """
    Allows X to perform longer jumps when holding down the Dash button. Only works after getting a Legs Upgrade.
    """
    display_name = "Long Jumps"

class LogicBossWeakness(DefaultOnToggle):
    """
    Most bosses will logically expect you to have its weakness.

    This option will be forced if the Boss Weakness Strictness setting is set to require only the weakness or
    the upgraded buster option.
    """
    display_name = "Boss Weakness Logic"

class LogicRequireVileDefeatForDoppler(DefaultOnToggle):
    """
    Adds a logic check for Dr. Doppler's Lab access so that it expects Vile to be defeated before accessing it.

    Note: It does not affect the actual Dr. Doppler's Lab access options.
    """
    display_name = "Vile in logic for Lab Access"

class ZSaberInPool(DefaultOnToggle):
    """
    Adds Z-Saber to the item pool.

    Z-Saber melee attack will deal 100% HP as DMG, ranged attack will deal 50% HP and its DoT will deal 4x2 DMG.
    On strict weakness settings Z-Saber will deal half the DMG (doesn't affect DoT from ranged attack)
    """
    display_name = "Z-Saber In Pool"

class QuickChargeInPool(DefaultOnToggle):
    """
    Adds Quick Charge Chip from Mega Man X5 into the item pool.

    Halves charge time for X-Buster and Special Weapon shots.
    """
    display_name = "Quick Charge In Pool"

class SpeedsterInPool(DefaultOnToggle):
    """
    Adds Speedster Chip from Mega Man X5 into the item pool.

    Increases walking speed by 50%
    """
    display_name = "Speedster In Pool"

class SuperRecoverInPool(DefaultOnToggle):
    """
    Adds Super Recover Chip from Mega Man X5 into the item pool.

    Increases recovery from items by 25%. Also affects EnergyLink deposit rate. Doesn't affect Sub Tanks.
    """
    display_name = "Super Recover In Pool"

class RapidFiveInPool(DefaultOnToggle):
    """
    Adds Rapid Five Chip from Mega Man X5 into the item pool.

    Increases the amount of buster shots on screen to 5.
    """
    display_name = "Rapid Five In Pool"

class SpeedShotInPool(DefaultOnToggle):
    """
    Adds Speed Shot Chip from Mega Man X5 into the item pool.

    Increases X's buster shots (lemons) horizontal speed by 50%.
    """
    display_name = "Speed Shot In Pool"

class BusterPlusInPool(DefaultOnToggle):
    """
    Adds Buster Plus Chip from Mega Man X5 into the item pool.

    Increases Buster (lemon) damage by 1.
    """
    display_name = "Buster Plus In Pool"

class WeaponPlusInPool(DefaultOnToggle):
    """
    Adds Weapon Plus Chip from Mega Man X6 into the item pool.

    Increases Weapon damage by 1.
    """
    display_name = "Weapon Plus In Pool"

class ItemPlusInPool(DefaultOnToggle):
    """
    Adds Item Plus Chip from Mega Man X7 into the item pool.

    Increases item drop rates by roughly 33%.
    """
    display_name = "Item Plus In Pool"

class PickupSanity(Toggle):
    """
    Whether collecting freestanding 1ups, HP and Weapon Energy capsules will grant a check.
    """
    display_name = "Pickupsanity"

class Lab2Boss(Choice):
    """
    Which boss will appear in the second Dr Doppler's Lab stage.

    Note: Also affects the stage variation.
    """
    display_name = "Doppler Lab 2 Boss"
    option_volt_kurageil = 0
    option_vile = 1
    default = 0

class Lab3BossRematchCount(Range):
    """
    How many boss rematches are needed in the third Dr. Doppler's Lab stage.
    """
    display_name = "Doppler Lab 3 Rematch count"
    range_start = 0
    range_end = 8
    default = 8

class LabsBundleUnlock(Toggle):
    """
    Whether to unlock Dr. Doppler's Lab 1-3 levels as a group or not.

    Unlocking level 4 requires getting all Lab levels cleared.
    """
    display_name = "Doppler Lab Levels Bundle Unlock"

class DopplerOpen(OptionSet):
    """
    Under which conditions will Dr. Doppler's lab open.
    If no options are selected a multiworld item granting access to the lab will be created.

    Medals: Consider Maverick medals to get access to the lab.
    Weapons: Consider weapons to get access to the lab.
    Armor Upgrades: Consider upgrades to get access to the lab.
    Heart Tanks: Consider heart tanks to get access to the lab.
    Sub Tanks: Consider sub tanks to get access to the lab.
    """
    display_name = "Doppler Lab rules"
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

class DopplerMedalCount(Range):
    """
    How many Maverick Medals are required to access Dr. Doppler's Lab.
    """
    display_name = "Doppler Medal Count"
    range_start = 0
    range_end = 8
    default = 8

class DopplerWeaponCount(Range):
    """
    How many weapons are required to access Dr. Doppler's Lab.
    """
    display_name = "Doppler Weapon Count"
    range_start = 0
    range_end = 6
    default = 6

class DopplerArmorUpgradeCount(Range):
    """
    How many armor upgrades are required to access Dr. Doppler's Lab.
    """
    display_name = "Doppler Armor Upgrade Count"
    range_start = 0
    range_end = 5
    default = 4

class DopplerHeartTankCount(Range):
    """
    How many Heart Tanks are required to access Dr. Doppler's Lab.
    """
    display_name = "Doppler Heart Tank Count"
    range_start = 0
    range_end = 6
    default = 6

class DopplerSubTankCount(Range):
    """
    How many Sub Tanks are required to access Dr. Doppler's Lab.
    """
    display_name = "Doppler Sub Tank Count"
    range_start = 0
    range_end = 2
    default = 2

class VileOpen(OptionSet):
    """
    Under which conditions will Vile's Stage open.
    If no options are selected a multiworld item granting access to the stage will be created.

    Medals: Consider Maverick medals to get access to the lab.
    Weapons: Consider weapons to get access to the lab.
    Armor Upgrades: Consider upgrades to get access to the lab.
    Heart Tanks: Consider heart tanks to get access to the lab.
    Sub Tanks: Consider sub tanks to get access to the lab.
    """
    display_name = "Vile Stage rules"
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

class VileMedalCount(Range):
    """
    How many Maverick Medals are required to access Vile's Stage.
    """
    display_name = "Vile Medal Count"
    range_start = 0
    range_end = 8
    default = 2

class VileWeaponCount(Range):
    """
    How many weapons are required to access Vile's Stage.
    """
    display_name = "Vile Weapon Count"
    range_start = 0
    range_end = 6
    default = 2

class VileArmorUpgradeCount(Range):
    """
    How many armor upgrades are required to access Vile's Stage.
    """
    display_name = "Vile Armor Upgrade Count"
    range_start = 0
    range_end = 5
    default = 4

class VileHeartTankCount(Range):
    """
    How many Heart Tanks are required to access Vile's Stage.
    """
    display_name = "Vile Heart Tank Count"
    range_start = 0
    range_end = 6
    default = 4

class VileSubTankCount(Range):
    """
    How many Sub Tanks are required to access Vile's Stage.
    """
    display_name = "Vile Sub Tank Count"
    range_start = 0
    range_end = 2
    default = 2

class BitMedalCount(Range):
    """
    How many Maverick Medals are required to access Bit's fight.
    """
    display_name = "Bit Medal Count"
    range_start = 0
    range_end = 5
    default = 2

class ByteMedalCount(Range):
    """
    How many Maverick Medals are required to access Byte's fight.

    Note: If Byte's medal count is less than or equal to Bit's, the value will be adjusted to Bit's + 1.
    """
    display_name = "Byte Medal Count"
    range_start = 1
    range_end = 6
    default = 5

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

class BasePalette(Choice):
    """
    Base class for palettes
    """
    option_blue = 0
    option_gold_armor = 1
    option_charge_blue = 2
    option_charge_pink = 3
    option_charge_red = 4
    option_charge_green = 5
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
    option_x4_default_armor = 30
    option_x4_ultimate_armor = 31
    option_x5_ultimate_armor = 32
    option_x6_shadow_armor = 33
    option_x6_blade_armor = 34
    option_classic_blue = 35
    option_smw_mario = 80
    option_smw_luigi = 81
    option_salvager_rex = 100
    option_master_driver_rex_2 = 101
    option_master_driver_rex_3 = 102
    option_grand_marshall_shulk = 103
    option_lifesage_nia = 104
    option_royal_summoner_melia = 105
    option_youmu = 180
    option_yohane = 190
    option_okayu = 200


class PaletteDefault(BasePalette):
    """
    Which color to use for X's default color
    """
    display_name = "X Palette"
    default = 0

class PaletteGoldArmor(BasePalette):
    """
    Which color to use for X's Gold Armor
    """
    display_name = "Gold Armor Palette"
    default = 1

class PaletteChargeBlue(BasePalette):
    """
    Which color to use for X's Level 1 & 2 Charge
    """
    display_name = "Level 1 & 2 Charge Palette"
    default = 2

class PaletteChargePink(BasePalette):
    """
    Which color to use for X's Level 3 Charge
    """
    display_name = "Level 3 Charge Palette"
    default = 3

class PaletteChargeRed(BasePalette):
    """
    Which color to use for X's Level 4 Charge
    """
    display_name = "Level 4 Charge Palette"
    default = 4

class PaletteChargeGreen(BasePalette):
    """
    Which color to use for X's Z-Saber Charge
    """
    display_name = "Z-Saber Charge Palette"
    default = 5

class PaletteAcidBurst(BasePalette):
    """
    Which color to use for X's Acid Burst
    """
    display_name = "Acid Burst Palette"
    default = 6

class PaletteParasiticBomb(BasePalette):
    """
    Which color to use for X's Parasitic Bomb
    """
    display_name = "Parasitic Bomb Palette"
    default = 7

class PaletteTriadThunder(BasePalette):
    """
    Which color to use for X's Triad Thunder
    """
    display_name = "Triad Thunder Palette"
    default = 8

class PaletteSpinningBlade(BasePalette):
    """
    Which color to use for X's Spinning Blade
    """
    display_name = "Spinning Blade Palette"
    default = 9

class PaletteRaySplasher(BasePalette):
    """
    Which color to use for X's Ray Splasher
    """
    display_name = "Ray Splasher Palette"
    default = 10

class PaletteGravityWell(BasePalette):
    """
    Which color to use for X's Gravity Well
    """
    display_name = "Gravity Well Palette"
    default = 11

class PaletteFrostShield(BasePalette):
    """
    Which color to use for X's Frost Shield
    """
    display_name = "Frost Shield Palette"
    default = 12

class PaletteTornadoFang(BasePalette):
    """
    Which color to use for X's Tornado Fang
    """
    display_name = "Tornado Fang Palette"
    default = 13

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
    default = {
        "Default": [],
        "Gold Armor": [],
        "Charge Blue": [],
        "Charge Pink": [],
        "Charge Red": [],
        "Charge Green": [],
        "Acid Burst": [],
        "Parasitic Bomb": [],
        "Triad Thunder": [],
        "Spinning Blade": [],
        "Ray Splasher": [],
        "Gravity Well": [],
        "Frost Shield": [],
        "Tornado Fang": [],
    }

mmx3_option_groups = [
    OptionGroup("Gameplay Options", [
        StartingLifeCount,
        StartingHP,
        HeartTankEffectiveness,
        JammedBuster,
        DisableChargeFreeze,
        LongJumps,
        ZSaberInPool,
        QuickChargeInPool,
        SpeedsterInPool,
        SuperRecoverInPool,
        RapidFiveInPool,
        SpeedShotInPool,
        BusterPlusInPool,
        WeaponPlusInPool,
        ItemPlusInPool,
    ]),
    OptionGroup("Boss Weakness Options", [
        BossWeaknessRando,
        PlandoWeaknesses,
        BossWeaknessStrictness,
        BossRandomizedHP,
        LogicBossWeakness,
    ]),
    OptionGroup("Dr. Doppler's Lab Options", [
        DopplerOpen,
        DopplerMedalCount,
        DopplerWeaponCount,
        DopplerArmorUpgradeCount,
        DopplerHeartTankCount,
        DopplerSubTankCount,
        Lab2Boss,
        Lab3BossRematchCount,
        LabsBundleUnlock,
        LogicRequireVileDefeatForDoppler,
    ]),
    OptionGroup("Vile's Stage Options", [
        VileOpen,
        VileMedalCount,
        VileWeaponCount,
        VileArmorUpgradeCount,
        VileHeartTankCount,
        VileSubTankCount,
    ]),
    OptionGroup("Bit & Byte Options", [
        BitMedalCount,
        ByteMedalCount,
    ]),
    OptionGroup("Aesthetic", [
        SetPalettes,
        PaletteDefault,
        PaletteGoldArmor,
        PaletteChargeBlue,
        PaletteChargePink,
        PaletteChargeRed,
        PaletteChargeGreen,
        PaletteAcidBurst,
        PaletteParasiticBomb,
        PaletteTriadThunder,
        PaletteSpinningBlade,
        PaletteRaySplasher,
        PaletteGravityWell,
        PaletteFrostShield,
        PaletteTornadoFang,
    ]),
]

@dataclass
class MMX3Options(PerGameCommonOptions):
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
    zsaber_in_pool: ZSaberInPool
    quick_charge_in_pool: QuickChargeInPool
    speedster_in_pool: SpeedsterInPool
    super_recover_in_pool: SuperRecoverInPool
    rapid_five_in_pool: RapidFiveInPool
    speed_shot_in_pool: SpeedShotInPool
    buster_plus_in_pool: BusterPlusInPool
    weapon_plus_in_pool: WeaponPlusInPool
    item_plus_in_pool: ItemPlusInPool
    disable_charge_freeze: DisableChargeFreeze
    long_jumps: LongJumps
    doppler_open: DopplerOpen
    doppler_medal_count: DopplerMedalCount
    doppler_weapon_count: DopplerWeaponCount
    doppler_upgrade_count: DopplerArmorUpgradeCount
    doppler_heart_tank_count: DopplerHeartTankCount
    doppler_sub_tank_count: DopplerSubTankCount
    doppler_lab_2_boss: Lab2Boss
    doppler_lab_3_boss_rematch_count: Lab3BossRematchCount
    doppler_all_labs: LabsBundleUnlock
    vile_open: VileOpen
    vile_medal_count: VileMedalCount
    vile_weapon_count: VileWeaponCount
    vile_upgrade_count: VileArmorUpgradeCount
    vile_heart_tank_count: VileHeartTankCount
    vile_sub_tank_count: VileSubTankCount
    bit_medal_count: BitMedalCount
    byte_medal_count: ByteMedalCount
    logic_boss_weakness: LogicBossWeakness
    logic_vile_required: LogicRequireVileDefeatForDoppler
    player_palettes: SetPalettes
    palette_default: PaletteDefault
    palette_gold_armor: PaletteGoldArmor
    palette_charge_blue: PaletteChargeBlue
    palette_charge_pink: PaletteChargePink
    palette_charge_red: PaletteChargeRed
    palette_charge_green: PaletteChargeGreen
    palette_acid_burst: PaletteAcidBurst
    palette_parasitic_bomb: PaletteParasiticBomb
    palette_triad_thunder: PaletteTriadThunder
    palette_spinning_blade: PaletteSpinningBlade
    palette_ray_splasher: PaletteRaySplasher
    palette_gravity_well: PaletteGravityWell
    palette_frost_shield: PaletteFrostShield
    palette_tornado_fang: PaletteTornadoFang
