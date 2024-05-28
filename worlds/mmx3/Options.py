from dataclasses import dataclass
import typing

#from Options import OptionGroup, Choice, Range, Toggle, DefaultOnToggle, OptionSet, DeathLink, PerGameCommonOptions, StartInventoryPool
from Options import Choice, Range, Toggle, DefaultOnToggle, OptionSet, DeathLink, PerGameCommonOptions, StartInventoryPool

class EnergyLink(DefaultOnToggle):
    """
    Enable EnergyLink support.

    EnergyLink in MMX3 works as a big HP and Weapon Energy pool that the players can use to request HP
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
    them together, meaning that a boss can be weak to Charged Frost Shield but not its
    uncharged version.
    """
    display_name = "Boss Weakness Randomization"
    option_vanilla = 0
    option_shuffled = 1
    option_chaotic_double = 2
    option_chaotic_single = 3
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
    range_end = 8
    default = 8

class DopplerArmorUpgradeCount(Range):
    """
    How many armor upgrades are required to access Dr. Doppler's Lab.
    """
    display_name = "Doppler Armor Upgrade Count"
    range_start = 0
    range_end = 8
    default = 5

class DopplerHeartTankCount(Range):
    """
    How many Heart Tanks are required to access Dr. Doppler's Lab.
    """
    display_name = "Doppler Heart Tank Count"
    range_start = 0
    range_end = 8
    default = 8

class DopplerSubTankCount(Range):
    """
    How many Sub Tanks are required to access Dr. Doppler's Lab.
    """
    display_name = "Doppler Sub Tank Count"
    range_start = 0
    range_end = 4
    default = 4

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
    range_end = 8
    default = 2

class VileArmorUpgradeCount(Range):
    """
    How many armor upgrades are required to access Vile's Stage.
    """
    display_name = "Vile Armor Upgrade Count"
    range_start = 0
    range_end = 8
    default = 4

class VileHeartTankCount(Range):
    """
    How many Heart Tanks are required to access Vile's Stage.
    """
    display_name = "Vile Heart Tank Count"
    range_start = 0
    range_end = 8
    default = 4

class VileSubTankCount(Range):
    """
    How many Sub Tanks are required to access Vile's Stage.
    """
    display_name = "Vile Sub Tank Count"
    range_start = 0
    range_end = 4
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

mmx3_option_groups = [
    """
    OptionGroup("Gameplay Options", [
        StartingLifeCount,
        StartingHP,
        HeartTankEffectiveness,
        JammedBuster,
        DisableChargeFreeze,
    ]),
    OptionGroup("Boss Weakness Options", [
        BossWeaknessRando,
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
    """
]

@dataclass
class MMX3Options(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    death_link: DeathLink
    energy_link: EnergyLink
    starting_life_count: StartingLifeCount
    starting_hp: StartingHP
    heart_tank_effectiveness: HeartTankEffectiveness
    boss_weakness_rando: BossWeaknessRando
    boss_weakness_strictness: BossWeaknessStrictness
    boss_randomize_hp: BossRandomizedHP
    pickupsanity: PickupSanity
    jammed_buster: JammedBuster
    zsaber_in_pool: ZSaberInPool
    disable_charge_freeze: DisableChargeFreeze
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

