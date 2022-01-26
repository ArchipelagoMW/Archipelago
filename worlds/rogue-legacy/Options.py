import typing

from Options import Choice, Range, Option, Toggle, DeathLink, DefaultOnToggle, OptionList


class StartingGender(Choice):
    """
    Determines the gender of your initial 'Sir Lee' character.
    """
    displayname = "Starting Gender"
    option_sir = 0
    option_lady = 1
    alias_male = 0
    alias_female = 1
    default = 0


class StartingClass(Choice):
    """
    Determines the starting class of your initial 'Sir Lee' character.
    """
    displayname = "Starting Class"
    option_knight = 0
    option_mage = 1
    option_barbarian = 2
    option_knave = 3
    option_shinobi = 4
    option_miner = 5
    option_spellthief = 6
    option_lich = 7
    default = 0


class NewGamePlus(Choice):
    """
    Puts the castle in new game plus mode which vastly increases enemy level, but increases gold gain by 50%. Not
    recommended for those inexperienced to Rogue Legacy!
    """
    displayname = "New Game Plus"
    option_normal = 0
    option_new_game_plus = 1
    option_new_game_plus_2 = 2
    alias_hard = 1
    alias_brutal = 2
    default = 0


class LevelScaling(Range):
    """
    A percentage modifier for scaling enemy level as you continue throughout the castle. 100 means enemies will have
    100% level scaling (normal). Setting this too high will result in enemies with absurdly high levels, you have been
    warned.
    """
    displayname = "Enemy Level Scaling Percentage"
    range_start = 1
    range_end = 300
    default = 100


class FairyChestsPerZone(Range):
    """
    Determines the number of Fairy Chests in a given zone that contain items. After these have been checked, only stat
    bonuses can be found in Fairy Chests.
    """
    displayname = "Fairy Chests Per Zone"
    range_start = 5
    range_end = 15
    default = 5


class ChestsPerZone(Range):
    """
    Determines the number of Non-Fairy Chests in a given zone that contain items. After these have been checked, only
    gold or stat bonuses can be found in Chests.
    """
    displayname = "Chests Per Zone"
    range_start = 15
    range_end = 30
    default = 15


class UniversalFairyChests(Toggle):
    """
    Determines if fairy chests should be combined into one pool instead of per zone, similar to Risk of Rain 2.
    """
    displayname = "Universal Fairy Chests"


class UniversalChests(Toggle):
    """
    Determines if non-fairy chests should be combined into one pool instead of per zone, similar to Risk of Rain 2.
    """
    displayname = "Universal Non-Fairy Chests"


class Vendors(Choice):
    """
    Determines where to place the Blacksmith and Enchantress unlocks in logic (or start with them unlocked).
    """
    displayname = "Vendors"
    option_start_unlocked = 0
    option_early = 1
    option_normal = 2
    option_anywhere = 3
    default = 1


class Architect(Choice):
    """
    Determines where the Architect sits in the item pool.
    """
    displayname = "Architect"
    option_start_unlocked = 0
    option_normal = 2
    option_disabled = 3
    default = 2


class ArchitectFee(Range):
    """
    Determines how large of a percentage the architect takes from the player when utilizing his services. 100 means he
    takes all your gold. 0 means his services are free.
    """
    displayname = "Architect Fee Percentage"
    range_start = 0
    range_end = 100
    default = 40


class DisableCharon(Toggle):
    """
    Prevents Charon from taking your money when you re-enter the castle. Also removes Haggling from the Item Pool.
    """
    displayname = "Disable Charon"


class RequirePurchasing(DefaultOnToggle):
    """
    Determines where you will be required to purchase equipment and runes from the Blacksmith and Enchantress before
    equipping them. If you disable require purchasing, Manor Renovations are scaled to take this into account.
    """
    displayname = "Require Purchasing"


class ProgressiveBlueprints(Toggle):
    """
    Instead of shuffling blueprints randomly into the pool, blueprint unlocks are progressively unlocked. You would get
    Squire first, then Silver, etc., until finally Dark.
    """
    displayname = "Progressive Blueprints"


class GoldGainMultiplier(Choice):
    """
    Adjusts the multiplier for gaining gold from all sources.
    """
    displayname = "Gold Gain Multiplier"
    option_normal = 0
    option_quarter = 1
    option_half = 2
    option_double = 3
    option_quadruple = 4
    default = 0


class NumberOfChildren(Range):
    """
    Determines the number of offspring you can choose from on the lineage screen after a death.
    """
    displayname = "Number of Children"
    range_start = 1
    range_end = 5
    default = 3


class AdditionalNames(OptionList):
    """
    Set of additional names your potential offspring can have. If Allow Default Names is disabled, this is the only list
    of names your children can have.
    """
    displayname = "Additional Names"


class AllowDefaultNames(DefaultOnToggle):
    """
    Determines if the names defined in Additional Names are allowed or not. Warning: This will not generate if the
    number of Additional Names defined is less than the Number of Children value.
    """
    displayname = "Allow Default Names"


class CastleScaling(Range):
    """
    Adjusts the scaling factor for how big a castle can be. Larger castles scale enemies quicker and also take longer
    to generate. 100 means normal castle size.
    """
    displayname = "Castle Size Scaling Percentage"
    range_start = 50
    range_end = 300
    default = 100


class ChallengeBossKhidr(Choice):
    """
    Determines if Neo Khidr replaces Khidr in their boss room.
    """
    displayname = "Khidr"
    option_vanilla = 0
    option_challenge = 1
    default = 0


class ChallengeBossAlexander(Choice):
    """
    Determines if Alexander the IV replaces Alexander in their boss room.
    """
    displayname = "Alexander"
    option_vanilla = 0
    option_challenge = 1
    default = 0


class ChallengeBossLeon(Choice):
    """
    Determines if Ponce de Freon replaces Ponce de Leon in their boss room.
    """
    displayname = "Ponce de Leon"
    option_vanilla = 0
    option_challenge = 1
    default = 0


class ChallengeBossHerodotus(Choice):
    """
    Determines if Astrodotus replaces Herodotus in their boss room.
    """
    displayname = "Herodotus"
    option_vanilla = 0
    option_challenge = 1
    default = 0


class HealthUpPool(Range):
    """
    Determines the number of Health Ups in the item pool.
    """
    displayname = "Health Up Pool"
    range_start = 0
    range_end = 15
    default = 15


class ManaUpPool(Range):
    """
    Determines the number of Mana Ups in the item pool.
    """
    displayname = "Mana Up Pool"
    range_start = 0
    range_end = 15
    default = 15


class AttackUpPool(Range):
    """
    Determines the number of Attack Ups in the item pool.
    """
    displayname = "Attack Up Pool"
    range_start = 0
    range_end = 15
    default = 15


class MagicDamageUpPool(Range):
    """
    Determines the number of Magic Damage Ups in the item pool.
    """
    displayname = "Magic Damage Up Pool"
    range_start = 0
    range_end = 15
    default = 15


class ArmorUpPool(Range):
    """
    Determines the number of Armor Ups in the item pool.
    """
    displayname = "Armor Up Pool"
    range_start = 0
    range_end = 10
    default = 10


class EquipUpPool(Range):
    """
    Determines the number of Equip Ups in the item pool.
    """
    displayname = "Equip Up Pool"
    range_start = 0
    range_end = 10
    default = 10


class CritChanceUpPool(Range):
    """
    Determines the number of Crit Chance Ups in the item pool.
    """
    displayname = "Crit Chance Up Pool"
    range_start = 0
    range_end = 5
    default = 5


class CritDamageUpPool(Range):
    """
    Determines the number of Crit Damage Ups in the item pool.
    """
    displayname = "Crit Damage Up Pool"
    range_start = 0
    range_end = 5
    default = 5


class FreeDiaryOnGeneration(DefaultOnToggle):
    """
    Allows the player to get a free diary check every time they regenerate the castle in the starting room.
    """
    displayname = "Free Diary On Generation"


legacy_options: typing.Dict[str, type(Option)] = {
    "starting_gender": StartingGender,
    "starting_class": StartingClass,
    "new_game_plus": NewGamePlus,
    "fairy_chests_per_zone": FairyChestsPerZone,
    "chests_per_zone": ChestsPerZone,
    "universal_fairy_chests": UniversalFairyChests,
    "universal_chests": UniversalChests,
    "vendors": Vendors,
    "architect": Architect,
    "architect_fee": ArchitectFee,
    "disable_charon": DisableCharon,
    "require_purchasing": RequirePurchasing,
    "progressive_blueprints": ProgressiveBlueprints,
    "gold_gain_multiplier": GoldGainMultiplier,
    "number_of_children": NumberOfChildren,
    "free_diary_on_generation": FreeDiaryOnGeneration,
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
    "allow_default_names": AllowDefaultNames,
    "additional_lady_names": AdditionalNames,
    "additional_sir_names": AdditionalNames,
    "death_link": DeathLink,
}
