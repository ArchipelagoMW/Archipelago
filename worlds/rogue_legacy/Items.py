from typing import Dict, NamedTuple, Optional

from BaseClasses import Item, ItemClassification


class RLItem(Item):
    game: str = "Rogue Legacy"


class RLItemData(NamedTuple):
    category: str
    code: Optional[int] = None
    classification: ItemClassification = ItemClassification.filler
    max_quantity: int = 1
    weight: int = 1


def get_items_by_category(category: str) -> Dict[str, RLItemData]:
    item_dict: Dict[str, RLItemData] = {}
    for name, data in item_table.items():
        if data.category == category:
            item_dict.setdefault(name, data)

    return item_dict


item_table: Dict[str, RLItemData] = {
    # Vendors
    "Blacksmith":               RLItemData("Vendors",    90_000, ItemClassification.progression),
    "Enchantress":              RLItemData("Vendors",    90_001, ItemClassification.progression),
    "Architect":                RLItemData("Vendors",    90_002, ItemClassification.useful),

    # Classes
    "Progressive Knights":      RLItemData("Classes",    90_003, ItemClassification.useful,                      2),
    "Progressive Mages":        RLItemData("Classes",    90_004, ItemClassification.useful,                      2),
    "Progressive Barbarians":   RLItemData("Classes",    90_005, ItemClassification.useful,                      2),
    "Progressive Knaves":       RLItemData("Classes",    90_006, ItemClassification.useful,                      2),
    "Progressive Shinobis":     RLItemData("Classes",    90_007, ItemClassification.useful,                      2),
    "Progressive Miners":       RLItemData("Classes",    90_008, ItemClassification.useful,                      2),
    "Progressive Liches":       RLItemData("Classes",    90_009, ItemClassification.useful,                      2),
    "Progressive Spellthieves": RLItemData("Classes",    90_010, ItemClassification.useful,                      2),
    "Dragons":                  RLItemData("Classes",    90_096, ItemClassification.progression),
    "Traitors":                 RLItemData("Classes",    90_097, ItemClassification.useful),

    # Skills
    "Health Up":                RLItemData("Skills",     90_013, ItemClassification.progression_skip_balancing, 15),
    "Mana Up":                  RLItemData("Skills",     90_014, ItemClassification.progression_skip_balancing, 15),
    "Attack Up":                RLItemData("Skills",     90_015, ItemClassification.progression_skip_balancing, 15),
    "Magic Damage Up":          RLItemData("Skills",     90_016, ItemClassification.progression_skip_balancing, 15),
    "Armor Up":                 RLItemData("Skills",     90_017, ItemClassification.useful,                     15),
    "Equip Up":                 RLItemData("Skills",     90_018, ItemClassification.useful,                      5),
    "Crit Chance Up":           RLItemData("Skills",     90_019, ItemClassification.useful,                      5),
    "Crit Damage Up":           RLItemData("Skills",     90_020, ItemClassification.useful,                      5),
    "Down Strike Up":           RLItemData("Skills",     90_021),
    "Gold Gain Up":             RLItemData("Skills",     90_022),
    "Potion Efficiency Up":     RLItemData("Skills",     90_023),
    "Invulnerability Time Up":  RLItemData("Skills",     90_024),
    "Mana Cost Down":           RLItemData("Skills",     90_025),
    "Death Defiance":           RLItemData("Skills",     90_026, ItemClassification.useful),
    "Haggling":                 RLItemData("Skills",     90_027, ItemClassification.useful),
    "Randomize Children":       RLItemData("Skills",     90_028, ItemClassification.useful),

    # Blueprints
    "Progressive Blueprints":   RLItemData("Blueprints", 90_055, ItemClassification.useful,                     15),
    "Squire Blueprints":        RLItemData("Blueprints", 90_040, ItemClassification.useful),
    "Silver Blueprints":        RLItemData("Blueprints", 90_041, ItemClassification.useful),
    "Guardian Blueprints":      RLItemData("Blueprints", 90_042, ItemClassification.useful),
    "Imperial Blueprints":      RLItemData("Blueprints", 90_043, ItemClassification.useful),
    "Royal Blueprints":         RLItemData("Blueprints", 90_044, ItemClassification.useful),
    "Knight Blueprints":        RLItemData("Blueprints", 90_045, ItemClassification.useful),
    "Ranger Blueprints":        RLItemData("Blueprints", 90_046, ItemClassification.useful),
    "Sky Blueprints":           RLItemData("Blueprints", 90_047, ItemClassification.useful),
    "Dragon Blueprints":        RLItemData("Blueprints", 90_048, ItemClassification.useful),
    "Slayer Blueprints":        RLItemData("Blueprints", 90_049, ItemClassification.useful),
    "Blood Blueprints":         RLItemData("Blueprints", 90_050, ItemClassification.useful),
    "Sage Blueprints":          RLItemData("Blueprints", 90_051, ItemClassification.useful),
    "Retribution Blueprints":   RLItemData("Blueprints", 90_052, ItemClassification.useful),
    "Holy Blueprints":          RLItemData("Blueprints", 90_053, ItemClassification.useful),
    "Dark Blueprints":          RLItemData("Blueprints", 90_054, ItemClassification.useful),

    # Runes
    "Vault Runes":              RLItemData("Runes",      90_060, ItemClassification.progression),
    "Sprint Runes":             RLItemData("Runes",      90_061, ItemClassification.progression),
    "Vampire Runes":            RLItemData("Runes",      90_062, ItemClassification.useful),
    "Sky Runes":                RLItemData("Runes",      90_063, ItemClassification.progression),
    "Siphon Runes":             RLItemData("Runes",      90_064, ItemClassification.useful),
    "Retaliation Runes":        RLItemData("Runes",      90_065),
    "Bounty Runes":             RLItemData("Runes",      90_066),
    "Haste Runes":              RLItemData("Runes",      90_067),
    "Curse Runes":              RLItemData("Runes",      90_068),
    "Grace Runes":              RLItemData("Runes",      90_069),
    "Balance Runes":            RLItemData("Runes",      90_070, ItemClassification.useful),

    # Junk
    "Triple Stat Increase":     RLItemData("Filler",     90_030, weight=6),
    "1000 Gold":                RLItemData("Filler",     90_031, weight=3),
    "3000 Gold":                RLItemData("Filler",     90_032, weight=2),
    "5000 Gold":                RLItemData("Filler",     90_033, weight=1),
}

event_item_table: Dict[str, RLItemData] = {
    "Defeat Khidr":             RLItemData("Event", classification=ItemClassification.progression),
    "Defeat Alexander":         RLItemData("Event", classification=ItemClassification.progression),
    "Defeat Ponce de Leon":     RLItemData("Event", classification=ItemClassification.progression),
    "Defeat Herodotus":         RLItemData("Event", classification=ItemClassification.progression),
    "Defeat Neo Khidr":         RLItemData("Event", classification=ItemClassification.progression),
    "Defeat Alexander IV":      RLItemData("Event", classification=ItemClassification.progression),
    "Defeat Ponce de Freon":    RLItemData("Event", classification=ItemClassification.progression),
    "Defeat Astrodotus":        RLItemData("Event", classification=ItemClassification.progression),
    "Defeat The Fountain":      RLItemData("Event", classification=ItemClassification.progression),
}
