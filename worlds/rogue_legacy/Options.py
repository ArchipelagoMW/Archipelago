from typing import Dict

from Options import Choice, DefaultOnToggle, Option, OptionSet, Range, StartInventoryPool, Toggle


class StartingGender(Choice):
    """
    Determines the gender of your initial 'Sir Lee' character.
    """
    display_name = "Starting Gender"
    option_sir = 0
    option_lady = 1
    alias_male = 0
    alias_female = 1
    default = "random"


class StartingClass(Choice):
    """
    Determines the starting class of your initial 'Sir Lee' character.
    """
    display_name = "Starting Class"
    option_knight = 0
    option_mage = 1
    option_barbarian = 2
    option_knave = 3
    option_shinobi = 4
    option_miner = 5
    option_spellthief = 6
    option_lich = 7
    option_dragon = 8
    option_traitor = 9
    default = 0


class NewGamePlus(Toggle):
    """
    Puts the castle in new game plus mode which vastly increases enemy level, but increases gold gain by 50%. Not
    recommended for those inexperienced to Rogue Legacy!
    """
    display_name = "New Game+ Mode"


class FairyChestsPerZone(Range):
    """
    Determines the number of Fairy Chests in a given zone that contain items. After these have been checked, only stat
    bonuses can be found in Fairy Chests.
    """
    display_name = "Fairy Chests Per Zone"
    range_start = 0
    range_end = 15
    default = 0


class ChestsPerZone(Range):
    """
    Determines the number of Non-Fairy Chests in a given zone that contain items. After these have been checked, only
    gold or stat bonuses can be found in Chests.
    """
    display_name = "Chests Per Zone"
    range_start = 25
    range_end = 50
    default = 25


class UniversalFairyChests(Toggle):
    """
    Determines if fairy chests should be combined into one pool instead of per zone.
    """
    display_name = "Universal Fairy Chests"


class UniversalChests(Toggle):
    """
    Determines if non-fairy chests should be combined into one pool instead of per zone.
    """
    display_name = "Universal Non-Fairy Chests"


class Architect(Choice):
    """
    Determines where the Architect sits in the item pool.
    """
    display_name = "Architect"
    option_start_unlocked = 0
    option_early = 1
    option_anywhere = 2
    option_disabled = 3
    default = 1


class ArchitectFee(Range):
    """
    Determines how large of a percentage the architect takes from the player when utilizing his services. 100 means he
    takes all your gold. 0 means his services are free.
    """
    display_name = "Architect Fee Percentage"
    range_start = 0
    range_end = 100
    default = 40


class DisableCharon(Toggle):
    """
    Prevents Charon from taking your money when you re-enter the castle.

    This also removes the Haggling skill and Charon's Obol Shrine from the item pool.
    """
    display_name = "Remove Charon"


class ShuffleBlacksmith(DefaultOnToggle):
    """
    Shuffles the types of items you can purchase from the Blacksmith into the item pool.

    For example, to purchase Limbs-type equipment, you need to find the Blacksmith - Limbs item.
    """
    display_name = "Shuffle Blacksmith Specialties"


class ShuffleEnchantress(DefaultOnToggle):
    """
    Shuffles the types of items you can purchase from the Enchantress into the item pool.

    For example, to purchase Limbs-type runes, you need to find the Enchantress - Limbs item.
    """
    display_name = "Shuffle Enchantress Specialties"


class RequireVendorPurchasing(DefaultOnToggle):
    """
    Determines where you will be required to purchase equipment and runes from the Blacksmith and Enchantress before
    equipping them.
    """
    display_name = "Require Purchasing from Vendors"


class RequireSkillPurchasing(Toggle):
    """
    Determines if you will be required to purchase your skill upgrades in the manor when received.

    If disabled, you will automatically obtain the skill levels.
    """
    display_name = "Require Purchasing from Skills"


class ProgressiveBlueprints(Toggle):
    """
    Instead of shuffling blueprints randomly into the pool, blueprint unlocks are progressively unlocked. You would get
    Squire first, then Knight, etc., until finally Dark.
    """
    display_name = "Progressive Blueprints"


class GoldGainMultiplier(Choice):
    """
    Adjusts the multiplier for gaining gold from all sources.
    """
    display_name = "Gold Gain Multiplier"
    option_normal = 0
    option_quarter = 1
    option_half = 2
    option_double = 3
    option_quadruple = 4
    default = 0


class SpendingRestrictions(Toggle):
    """
    Prevents the player from spending more than a certain amount of gold per life without certain upgrades.

    Tier 0: Can only spend up to 2,500 gold per life.
    Tier 1: Can only spend up to 5,000 gold per life.
    Tier 2: Can only spend up to 10,000 gold per life.
    Tier 3: Can only spend up to 20,000 gold per life.
    Tier 4: Can spend an unlimited amount of gold.
    """
    display_name = "Gold Spending Limits"


class NumberOfChildren(Choice):
    """
    Determines the number of offspring you can choose from on the lineage screen after a death.

    "Variable" means the number of children you can choose from will between randomly picked from 1 and 5 every
    generation.
    """
    display_name = "Number of Children"
    option_one = 1
    option_two = 2
    option_three = 3
    option_four = 4
    option_five = 5
    option_variable = 6
    alias_1 = 1
    alias_2 = 2
    alias_3 = 3
    alias_4 = 4
    alias_5 = 5
    default = 3


class CastleSize(Choice):
    """
    Adjusts the scaling factor for how big a castle can be. Larger castles scale enemy levels quicker, but will take
    longer to generate.

    Standard: Castle Hamson is the same size as in vanilla Rogue Legacy.
    Large: Castle Hamson is 4x larger than vanilla Rogue Legacy.
    Very Large: Castle Hamson is 8x larger than vanilla Rogue Legacy.
    Labyrinth: Castle Hamson is 12x larger than vanilla Rogue Legacy.
    """
    display_name = "Castle Hamson Size"
    option_standard = 0
    option_large = 1
    option_very_large = 2
    option_labyrinth = 3


class ChallengeBossKhidr(Choice):
    """
    Determines if Neo Khidr replaces Khidr in their boss room.
    """
    display_name = "Khidr Boss"
    option_vanilla = 0
    option_challenge = 1
    default = 0


class ChallengeBossAlexander(Choice):
    """
    Determines if Alexander the IV replaces Alexander in their boss room.
    """
    display_name = "Alexander Boss"
    option_vanilla = 0
    option_challenge = 1
    default = 0


class ChallengeBossLeon(Choice):
    """
    Determines if Ponce de Freon replaces Ponce de Leon in their boss room.
    """
    display_name = "Ponce de Leon Boss"
    option_vanilla = 0
    option_challenge = 1
    default = 0


class ChallengeBossHerodotus(Choice):
    """
    Determines if Astrodotus replaces Herodotus in their boss room.
    """
    display_name = "Herodotus Boss"
    option_vanilla = 0
    option_challenge = 1
    default = 0


class HealthUpPool(Range):
    """
    Determines the number of Health Ups in the item pool.
    """
    display_name = "Health Up Pool"
    range_start = 0
    range_end = 15
    default = 15


class ManaUpPool(Range):
    """
    Determines the number of Mana Ups in the item pool.
    """
    display_name = "Mana Up Pool"
    range_start = 0
    range_end = 15
    default = 15


class AttackUpPool(Range):
    """
    Determines the number of Attack Ups in the item pool.
    """
    display_name = "Attack Up Pool"
    range_start = 0
    range_end = 15
    default = 15


class MagicDamageUpPool(Range):
    """
    Determines the number of Magic Damage Ups in the item pool.
    """
    display_name = "Magic Damage Up Pool"
    range_start = 0
    range_end = 15
    default = 15


class ArmorUpPool(Range):
    """
    Determines the number of Armor Ups in the item pool.
    """
    display_name = "Armor Up Pool"
    range_start = 0
    range_end = 10
    default = 10


class EquipUpPool(Range):
    """
    Determines the number of Equip Ups in the item pool.
    """
    display_name = "Equip Up Pool"
    range_start = 0
    range_end = 10
    default = 10


class CritChanceUpPool(Range):
    """
    Determines the number of Crit Chance Ups in the item pool.
    """
    display_name = "Crit Chance Up Pool"
    range_start = 0
    range_end = 5
    default = 5


class CritDamageUpPool(Range):
    """
    Determines the number of Crit Damage Ups in the item pool.
    """
    display_name = "Crit Damage Up Pool"
    range_start = 0
    range_end = 5
    default = 5


class FountainDoorRequirement(Choice):
    """
    Determines the requirements to open the door to the Fountain Room.

    Adds Pieces of the Fountain to the pool if one of the chosen requirements requires them.
    """
    display_name = "Fountain Door Requirement"
    option_bosses = 0
    option_fountain_pieces = 1
    option_both = 2
    default = 0


class FountainPiecesAvailable(Range):
    """
    If Fountain Door Requirement requires Pieces of the Fountain, how many should exist to be found? If there are not
    enough locations to hold all the requested fountain pieces, it will add as many as possible until locations are
    filled.
    """
    display_name = "Maximum Fountain Pieces Available"
    range_start = 1
    range_end = 100
    default = 15


class FountainPiecesRequired(Range):
    """
    If Fountain Door Requirement requires Pieces of the Fountain, what percentage of available fountain pieces should
    be required to fulfil the Fountain Door Requirement? There will always be at least 1 fountain piece in the pool.
    """
    display_name = "Required Fountain Pieces Percentage"
    range_start = 25
    range_end = 100
    default = 75


class AvailableClasses(OptionSet):
    """
    List of classes that will be in the item pool to find. The upgraded form of the class will be added with it.

    The upgraded form of your starting class will always be available.
    """
    display_name = "Available Classes"
    default = {
        "Knights",
        "Mages",
        "Barbarians",
        "Knaves",
        "Shinobis",
        "Miners",
        "Spellthieves",
        "Liches",
        "Dragons",
        "Traitors",
    }
    valid_keys = default.copy()


class IncludeTraps(Toggle):
    """
    Includes some items that only exist to make your life worse.
    """
    display_name = "Include Traps"


class FreeDiaryOnGeneration(DefaultOnToggle):
    """
    Gives a free diary location check (up to 24) each generation. If disabled, you'll have to find the other 23
    organically!

    Note: The 25th diary is always before the final boss.
    """
    display_name = "Free Diary Per Generation"


class RLDeathLink(Choice):
    """
    When you die, everyone dies. Of course, the reverse is true too.

    "Disabled": You will start with DeathLink disabled, but can turn it on in-game.
    "Enabled": You will start with DeathLink enabled, but can turn it off in-game.
    "Forced Disabled": You will start with DeathLink disabled and cannot turn it on in-game.
    "Forced Enabled": You will start with DeathLink enabled and cannot turn it off in-game.
    """
    display_name = "Death Link"
    option_disabled = 0
    option_enabled = 1
    option_forced_disabled = 2
    option_forced_enabled = 3
    default = 0


options_table: Dict[str, type(Option)] = {
    "start_inventory": StartInventoryPool,
    "starting_gender": StartingGender,
    "starting_class": StartingClass,
    "new_game_plus": NewGamePlus,
    "universal_chests": UniversalChests,
    "chests_per_zone": ChestsPerZone,
    "universal_fairy_chests": UniversalFairyChests,
    "fairy_chests_per_zone": FairyChestsPerZone,
    "free_diary_per_generation": FreeDiaryOnGeneration,
    "architect": Architect,
    "architect_fee": ArchitectFee,
    "disable_charon": DisableCharon,
    "shuffle_blacksmith": ShuffleBlacksmith,
    "shuffle_enchantress": ShuffleEnchantress,
    "require_vendor_purchasing": RequireVendorPurchasing,
    "require_skill_purchasing": RequireSkillPurchasing,
    "progressive_blueprints": ProgressiveBlueprints,
    "gold_gain_multiplier": GoldGainMultiplier,
    "spending_restrictions": SpendingRestrictions,
    "number_of_children": NumberOfChildren,
    "castle_size": CastleSize,
    "khidr": ChallengeBossKhidr,
    "alexander": ChallengeBossAlexander,
    "leon": ChallengeBossLeon,
    "herodotus": ChallengeBossHerodotus,
    "health_pool": HealthUpPool,
    "mana_pool": ManaUpPool,
    "attack_pool": AttackUpPool,
    "magic_damage_pool": MagicDamageUpPool,
    "armor_pool": ArmorUpPool,
    "equip_pool": EquipUpPool,
    "crit_chance_pool": CritChanceUpPool,
    "crit_damage_pool": CritDamageUpPool,
    "fountain_door_requirement": FountainDoorRequirement,
    "fountain_pieces_available": FountainPiecesAvailable,
    "fountain_pieces_percentage": FountainPiecesRequired,
    "include_traps": IncludeTraps,
    "available_classes": AvailableClasses,
    "death_link": RLDeathLink,
}
