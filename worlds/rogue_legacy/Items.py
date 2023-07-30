from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Set

from BaseClasses import Item, ItemClassification, MultiWorld
from .Options import Architect, ShuffleBlacksmith, \
    ShuffleEnchantress, SpendingRestrictions, StartingClass

__all__ = ["RLItem", "RLItemData", "item_groups", "item_table", "filler_items"]

ITEM_ID_OFFSET = 90_000


def get_none(multiworld: MultiWorld, player: int) -> int:
    """Returns no items, for items that should not generate automatically in `create_items`."""
    return 0


def get_one(multiworld: MultiWorld, player: int) -> int:
    """Returns only a single item. Default for most items."""
    return 1


def get_architect_quantity(multiworld: MultiWorld, player: int) -> int:
    """Returns the number of Architects to create."""
    architect: Architect = getattr(multiworld, "architect")[player]
    if architect == "start_unlocked" or architect == "disabled":
        return 0

    return 1


def get_class_quantity(multiworld: MultiWorld, player: int, class_name: str, maximum: int = 1) -> int:
    """Returns the number of classes to create."""
    starting_class: StartingClass = getattr(multiworld, "starting_class")[player]
    class_included = class_name in getattr(multiworld, "available_classes")[player].value

    # Starting Knights
    if class_name == "Knights" and starting_class == "knight":
        return maximum - 1
    # Starting Mages
    if class_name == "Mages" and starting_class == "mage":
        return maximum - 1
    # Starting Barbarians
    if class_name == "Barbarians" and starting_class == "barbarian":
        return maximum - 1
    # Starting Knaves
    if class_name == "Knaves" and starting_class == "knave":
        return maximum - 1
    # Starting Miners
    if class_name == "Miners" and starting_class == "miner":
        return maximum - 1
    # Starting Shinobis
    if class_name == "Shinobis" and starting_class == "shinobi":
        return maximum - 1
    # Starting Liches
    if class_name == "Liches" and starting_class == "lich":
        return maximum - 1
    # Starting Spellthieves
    if class_name == "Spellthieves" and starting_class == "spellthief":
        return maximum - 1
    # Starting Dragons
    if class_name == "Dragons" and starting_class == "dragon":
        return maximum - 1
    # Starting Traitors
    if class_name == "Traitors" and starting_class == "traitor":
        return maximum - 1

    return maximum if class_included else 0


def get_knights_quantity(multiworld: MultiWorld, player: int) -> int:
    return get_class_quantity(multiworld, player, "Knights", 2)


def get_mages_quantity(multiworld: MultiWorld, player: int) -> int:
    return get_class_quantity(multiworld, player, "Mages", 2)


def get_barbarians_quantity(multiworld: MultiWorld, player: int) -> int:
    return get_class_quantity(multiworld, player, "Barbarians", 2)


def get_knaves_quantity(multiworld: MultiWorld, player: int) -> int:
    return get_class_quantity(multiworld, player, "Knaves", 2)


def get_shinobis_quantity(multiworld: MultiWorld, player: int) -> int:
    return get_class_quantity(multiworld, player, "Shinobis", 2)


def get_miners_quantity(multiworld: MultiWorld, player: int) -> int:
    return get_class_quantity(multiworld, player, "Miners", 2)


def get_liches_quantity(multiworld: MultiWorld, player: int) -> int:
    return get_class_quantity(multiworld, player, "Liches", 2)


def get_spellthieves_quantity(multiworld: MultiWorld, player: int) -> int:
    return get_class_quantity(multiworld, player, "Spellthieves", 2)


def get_dragons_quantity(multiworld: MultiWorld, player: int) -> int:
    return get_class_quantity(multiworld, player, "Dragons")


def get_traitors_quantity(multiworld: MultiWorld, player: int) -> int:
    return get_class_quantity(multiworld, player, "Traitors")


def get_blueprints_quantity(multiworld: MultiWorld, player: int) -> int:
    """Get the number of normal blueprints to create."""
    if getattr(multiworld, "progressive_blueprints")[player]:
        return 0

    return 1


def get_progressive_blueprints_quantity(multiworld: MultiWorld, player: int) -> int:
    """Get the number of progressive blueprints to create."""
    if not getattr(multiworld, "progressive_blueprints")[player]:
        return 0

    return 15  # There are 15 blueprints!


def get_haggling_quantity(multiworld: MultiWorld, player: int) -> int:
    return 0 if getattr(multiworld, "disable_charon")[player] else 1


def get_health_quantity(multiworld: MultiWorld, player: int) -> int:
    return getattr(multiworld, "health_pool")[player].value


def get_mana_quantity(multiworld: MultiWorld, player: int) -> int:
    return getattr(multiworld, "mana_pool")[player].value


def get_attack_quantity(multiworld: MultiWorld, player: int) -> int:
    return getattr(multiworld, "attack_pool")[player].value


def get_magic_damage_quantity(multiworld: MultiWorld, player: int) -> int:
    return getattr(multiworld, "magic_damage_pool")[player].value


def get_armor_quantity(multiworld: MultiWorld, player: int) -> int:
    return getattr(multiworld, "armor_pool")[player].value


def get_equip_quantity(multiworld: MultiWorld, player: int) -> int:
    return getattr(multiworld, "equip_pool")[player].value


def get_crit_chance_quantity(multiworld: MultiWorld, player: int) -> int:
    return getattr(multiworld, "crit_chance_pool")[player].value


def get_crit_damage_quantity(multiworld: MultiWorld, player: int) -> int:
    return getattr(multiworld, "crit_damage_pool")[player].value


def get_wallet_quantity(multiworld: MultiWorld, player: int) -> int:
    wallet_enabled: SpendingRestrictions = getattr(multiworld, "spending_restrictions")[player]
    if wallet_enabled:
        return 4

    return 0


def get_blacksmith_quantity(multiworld: MultiWorld, player: int) -> int:
    shuffle_blacksmith: ShuffleBlacksmith = getattr(multiworld, "shuffle_blacksmith")[player]
    if shuffle_blacksmith:
        return 1

    return 0


def get_enchantress_quantity(multiworld: MultiWorld, player: int) -> int:
    shuffle_enchantress: ShuffleEnchantress = getattr(multiworld, "shuffle_enchantress")[player]
    if shuffle_enchantress:
        return 1

    return 0


class RLItem(Item):
    game: str = "Rogue Legacy"


@dataclass
class RLItemData:
    """A collection of metadata for each item prior to creation into an RLItem."""
    name: str
    classification: ItemClassification
    code: Optional[int]
    creation_quantity: Callable[[MultiWorld, int], int]
    filler_item_weight: int

    def __init__(
            self,
            classification: ItemClassification = ItemClassification.filler,
            code: Optional[int] = None,
            creation_quantity: Callable[[MultiWorld, int], int] = get_one,
            filler_item_weight: int = 0):
        self.classification = classification
        self.code = code + ITEM_ID_OFFSET if code is not None else None
        self.creation_quantity = creation_quantity
        self.filler_item_weight = filler_item_weight

    @property
    def event(self) -> bool:
        """Returns True if this is an event item."""
        return self.code is None


item_groups: Dict[str, Set[str]] = {
    "Vendor": {
        "Enchantress - Sword",
        "Enchantress - Helm",
        "Enchantress - Chest",
        "Enchantress - Limbs",
        "Enchantress - Cape",
        "Blacksmith - Sword",
        "Blacksmith - Helm",
        "Blacksmith - Chest",
        "Blacksmith - Limbs",
        "Blacksmith - Cape",
    },
    "Class": {
        "Progressive Knights",
        "Progressive Mages",
        "Progressive Barbarians",
        "Progressive Knaves",
        "Progressive Shinobis",
        "Progressive Miners",
        "Progressive Liches",
        "Progressive Spellthieves",
        "Dragons",
        "Traitors",
    },
    "Skill": {
        "Health Up",
        "Mana Up",
        "Attack Up",
        "Magic Damage Up",
    },
}

item_table: Dict[str, RLItemData] = {
    # Vendors
    "Blacksmith":               RLItemData(ItemClassification.useful,         0, get_none),
    "Enchantress":              RLItemData(ItemClassification.useful,         1, get_none),
    "Architect":                RLItemData(ItemClassification.useful,         2, get_architect_quantity),

    # Classes
    "Progressive Knights":      RLItemData(ItemClassification.useful,         3, get_knights_quantity),
    "Progressive Mages":        RLItemData(ItemClassification.useful,         4, get_mages_quantity),
    "Progressive Barbarians":   RLItemData(ItemClassification.useful,         5, get_barbarians_quantity),
    "Progressive Knaves":       RLItemData(ItemClassification.useful,         6, get_knaves_quantity),
    "Progressive Shinobis":     RLItemData(ItemClassification.useful,         7, get_shinobis_quantity),
    "Progressive Miners":       RLItemData(ItemClassification.useful,         8, get_miners_quantity),
    "Progressive Liches":       RLItemData(ItemClassification.useful,         9, get_liches_quantity),
    "Progressive Spellthieves": RLItemData(ItemClassification.useful,        10, get_spellthieves_quantity),
    "Dragons":                  RLItemData(ItemClassification.progression,   96, get_dragons_quantity),
    "Traitors":                 RLItemData(ItemClassification.useful,        97, get_traitors_quantity),

    # Skills
    "Health Up":                RLItemData(ItemClassification.progression,   13, get_health_quantity),
    "Mana Up":                  RLItemData(ItemClassification.progression,   14, get_mana_quantity),
    "Attack Up":                RLItemData(ItemClassification.progression,   15, get_attack_quantity),
    "Magic Damage Up":          RLItemData(ItemClassification.progression,   16, get_magic_damage_quantity),
    "Armor Up":                 RLItemData(ItemClassification.useful,        17, get_armor_quantity),
    "Equip Up":                 RLItemData(ItemClassification.useful,        18, get_equip_quantity),
    "Crit Chance Up":           RLItemData(ItemClassification.useful,        19, get_crit_chance_quantity),
    "Crit Damage Up":           RLItemData(ItemClassification.useful,        20, get_crit_damage_quantity),
    "Down Strike Up":           RLItemData(ItemClassification.filler,        21),
    "Gold Gain Up":             RLItemData(ItemClassification.filler,        22),
    "Potion Efficiency Up":     RLItemData(ItemClassification.filler,        23),
    "Invulnerability Time Up":  RLItemData(ItemClassification.filler,        24),
    "Mana Cost Down":           RLItemData(ItemClassification.filler,        25),
    "Death Defiance":           RLItemData(ItemClassification.useful,        26),
    "Haggling":                 RLItemData(ItemClassification.useful,        27, get_haggling_quantity),
    "Randomize Children":       RLItemData(ItemClassification.useful,        28),

    # Blueprints
    "Progressive Blueprints":   RLItemData(ItemClassification.useful,        55, get_progressive_blueprints_quantity),
    "Squire Blueprints":        RLItemData(ItemClassification.useful,        40, get_blueprints_quantity),
    "Silver Blueprints":        RLItemData(ItemClassification.useful,        41, get_blueprints_quantity),
    "Guardian Blueprints":      RLItemData(ItemClassification.useful,        42, get_blueprints_quantity),
    "Imperial Blueprints":      RLItemData(ItemClassification.useful,        43, get_blueprints_quantity),
    "Royal Blueprints":         RLItemData(ItemClassification.useful,        44, get_blueprints_quantity),
    "Knight Blueprints":        RLItemData(ItemClassification.useful,        45, get_blueprints_quantity),
    "Ranger Blueprints":        RLItemData(ItemClassification.useful,        46, get_blueprints_quantity),
    "Sky Blueprints":           RLItemData(ItemClassification.useful,        47, get_blueprints_quantity),
    "Dragon Blueprints":        RLItemData(ItemClassification.useful,        48, get_blueprints_quantity),
    "Slayer Blueprints":        RLItemData(ItemClassification.useful,        49, get_blueprints_quantity),
    "Blood Blueprints":         RLItemData(ItemClassification.useful,        50, get_blueprints_quantity),
    "Sage Blueprints":          RLItemData(ItemClassification.useful,        51, get_blueprints_quantity),
    "Retribution Blueprints":   RLItemData(ItemClassification.useful,        52, get_blueprints_quantity),
    "Holy Blueprints":          RLItemData(ItemClassification.useful,        53, get_blueprints_quantity),
    "Dark Blueprints":          RLItemData(ItemClassification.useful,        54, get_blueprints_quantity),

    # Runes
    "Vault Runes":              RLItemData(ItemClassification.progression,   60),
    "Sprint Runes":             RLItemData(ItemClassification.progression,   61),
    "Vampire Runes":            RLItemData(ItemClassification.useful,        62),
    "Sky Runes":                RLItemData(ItemClassification.progression,   63),
    "Siphon Runes":             RLItemData(ItemClassification.useful,        64),
    "Retaliation Runes":        RLItemData(ItemClassification.filler,        65),
    "Bounty Runes":             RLItemData(ItemClassification.filler,        66),
    "Haste Runes":              RLItemData(ItemClassification.filler,        67),
    "Curse Runes":              RLItemData(ItemClassification.filler,        68),
    "Grace Runes":              RLItemData(ItemClassification.filler,        69),
    "Balance Runes":            RLItemData(ItemClassification.useful,        70),

    # Specialties
    "Enchantress - Sword":      RLItemData(ItemClassification.progression,  100, get_enchantress_quantity),
    "Enchantress - Helm":       RLItemData(ItemClassification.progression,  101, get_enchantress_quantity),
    "Enchantress - Chest":      RLItemData(ItemClassification.progression,  102, get_enchantress_quantity),
    "Enchantress - Limbs":      RLItemData(ItemClassification.progression,  103, get_enchantress_quantity),
    "Enchantress - Cape":       RLItemData(ItemClassification.progression,  104, get_enchantress_quantity),
    "Blacksmith - Sword":       RLItemData(ItemClassification.useful,       105, get_blacksmith_quantity),
    "Blacksmith - Helm":        RLItemData(ItemClassification.useful,       106, get_blacksmith_quantity),
    "Blacksmith - Chest":       RLItemData(ItemClassification.useful,       107, get_blacksmith_quantity),
    "Blacksmith - Limbs":       RLItemData(ItemClassification.useful,       108, get_blacksmith_quantity),
    "Blacksmith - Cape":        RLItemData(ItemClassification.useful,       109, get_blacksmith_quantity),

    # Free Relics
    "Charon's Obol Shrine":     RLItemData(ItemClassification.useful,       160, get_haggling_quantity),
    "Hyperion's Ring Shrine":   RLItemData(ItemClassification.useful,       161),
    "Hermes' Boots Shrine":     RLItemData(ItemClassification.filler,       162),
    "Helios' Blessing Shrine":  RLItemData(ItemClassification.filler,       163),
    "Calypso's Compass Shrine": RLItemData(ItemClassification.progression,  164),
    "Nerdy Glasses Shrine":     RLItemData(ItemClassification.progression,  165),
    "Phar's Guidance Shrine":   RLItemData(ItemClassification.useful,       169),

    # Wallets
    "Progressive Spending":     RLItemData(ItemClassification.progression,  190, get_wallet_quantity),

    # Fountain Pieces - Handled differently during `create_items` stage.
    "Piece of the Fountain":    RLItemData(ItemClassification.progression_skip_balancing, 180, get_none),

    # Filler and Traps - These will be generated automatically when filler items are needed.
    "Triple Stat Increase":     RLItemData(ItemClassification.filler,        30, get_none, 5),
    "1,000 Gold Stimulus":      RLItemData(ItemClassification.filler,        31, get_none, 3),
    "3,000 Gold Stimulus":      RLItemData(ItemClassification.filler,        32, get_none, 2),
    "5,000 Gold Stimulus":      RLItemData(ItemClassification.filler,        33, get_none, 1),
    "Random Teleport":          RLItemData(ItemClassification.trap,         150, get_none, 0),
    "Hedgehog's Curse":         RLItemData(ItemClassification.trap,         151, get_none, 2),
    "Vertigo":                  RLItemData(ItemClassification.trap,         152, get_none, 2),
    "Genetic Lottery":          RLItemData(ItemClassification.trap,         153, get_none, 2),

    # Events - These are automatically created and placed when their respective event location is made.
    "Defeat Khidr":             RLItemData(ItemClassification.progression, None, get_none),
    "Defeat Alexander":         RLItemData(ItemClassification.progression, None, get_none),
    "Defeat Ponce de Leon":     RLItemData(ItemClassification.progression, None, get_none),
    "Defeat Herodotus":         RLItemData(ItemClassification.progression, None, get_none),
    "Defeat Neo Khidr":         RLItemData(ItemClassification.progression, None, get_none),
    "Defeat Alexander IV":      RLItemData(ItemClassification.progression, None, get_none),
    "Defeat Ponce de Freon":    RLItemData(ItemClassification.progression, None, get_none),
    "Defeat Astrodotus":        RLItemData(ItemClassification.progression, None, get_none),
    "Open Fountain Room Door":  RLItemData(ItemClassification.progression, None, get_none),
    "Defeat The Fountain":      RLItemData(ItemClassification.progression, None, get_none),
}


# Set the item name for each item based on key.
for item_name, item_data in item_table.items():
    item_data.name = item_name

filler_items: Dict[str, List[Any]] = {
    "names": [
        item.name for item in item_table.values()
        if item.filler_item_weight and item.classification != ItemClassification.trap
    ],
    "weights": [
        item.filler_item_weight for item in item_table.values()
        if item.filler_item_weight and item.classification != ItemClassification.trap
    ],
    "trap_names": [
        item.name for item in item_table.values()
        if item.filler_item_weight and item.classification == ItemClassification.trap
    ],
    "trap_weights": [
        item.filler_item_weight for item in item_table.values()
        if item.filler_item_weight and item.classification == ItemClassification.trap
    ],
}
