from dataclasses import dataclass
import typing

from Options import Choice, Range, Toggle, DefaultOnToggle, DeathLink, PerGameCommonOptions, StartInventoryPool

class EnergyLink(DefaultOnToggle):
    """
    Enable EnergyLink support.
    EnergyLink works as a big Sub Tank/HP pool where players can request HP manually or automatically when
    they lose HP. You make use of this feature by typing /pool, /heal <amount> or /autoheal in the client.
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

    Z-Saber damage output will be cut to 50%/37.5%/25% of its original damage according to the strictness setting.
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

class FortressBundleUnlock(Toggle):
    """
    Whether to unlock Sigma's Fortress 1-3 levels as a group or not.
    Unlocking level 4 requires getting all Fortress levels cleared.
    """
    display_name = "Fortress Levels Bundle Unlock"

class SigmaOpen(Choice):
    """
    Under what conditions will Sigma's Fortress open.
      multiworld: Access will require an Access Code multiworld item, similar to the main stages.
      medals: Access will be granted after collecting a certain amount of Maverick Medals.
      weapons: Access will be granted after collecting a certain amount of weapons.
      armor_upgrades: Access will be granted after collecting a certain amount of armor upgrades.
      heart_tanks: Access will be granted after collecting a certain amount of Heart Tanks.
      sub_tanks: Access will be granted after collecting a certain amount of Sub Tanks.
      all: Access will be granted after collecting a certain amount of Medals, Weapons, Armor Upgrades
           Heart Tanks and Sub Tanks.
    Do not enable all on solo seeds without pickupsanity or sessions with very few items.
    There's a big chance it'll cause an error.
    """
    display_name = "Sigma Fortress Rules"
    option_multiworld = 0
    option_medals = 1
    option_weapons = 2
    option_armor_upgrades = 4
    option_heart_tanks = 8
    option_sub_tanks = 16
    option_all = 31
    default = 1

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
    range_end = 8
    default = 8

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
    range_end = 8
    default = 8

class SigmaSubTankCount(Range):
    """
    How many Sub Tanks are required to access Sigma's Fortress.
    """
    display_name = "Sigma Sub Tank Count"
    range_start = 0
    range_end = 4
    default = 4


@dataclass
class MMXOptions(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    death_link: DeathLink
    energy_link: EnergyLink
    starting_life_count: StartingLifeCount
    starting_hp: StartingHP
    heart_tank_effectiveness: HeartTankEffectiveness
    boss_weakness_rando: BossWeaknessRando
    boss_weakness_strictness: BossWeaknessStrictness
    boss_randomize_hp: BossRandomizedHP
    jammed_buster: JammedBuster
    pickupsanity: PickupSanity
    logic_boss_weakness: LogicBossWeakness
    logic_leg_sigma: LogicLegSigma
    logic_charged_shotgun_ice: LogicChargedShotgunIce
    early_legs: EarlyLegs
    sigma_all_levels: FortressBundleUnlock
    sigma_open: SigmaOpen
    sigma_medal_count: SigmaMedalCount
    sigma_weapon_count: SigmaWeaponCount
    sigma_upgrade_count: SigmaArmorUpgradeCount
    sigma_heart_tank_count: SigmaHeartTankCount
    sigma_sub_tank_count: SigmaSubTankCount
