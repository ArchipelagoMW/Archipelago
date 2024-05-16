from BaseClasses import Item, ItemClassification

AP_METROID_PRIME_ITEM_ID_BASE = 5031000


class ItemData:
    name: str
    code: int
    classification: ItemClassification
    max_capacity: int
    id: int

    def __init__(self, name: str, id: int, progression: ItemClassification, max_capacity: int = 1) -> None:
        self.name = name
        self.id = id
        self.code = id + AP_METROID_PRIME_ITEM_ID_BASE
        self.classification = progression
        self.max_capacity = max_capacity


class MetroidPrimeItem(Item):
    game: str = "Metroid Prime"


suit_upgrade_table: dict[str, ItemData] = {
    "Power Beam": ItemData("Power Beam", 0, ItemClassification.progression),
    "Ice Beam": ItemData("Ice Beam", 1, ItemClassification.progression),
    "Wave Beam": ItemData("Wave Beam", 2, ItemClassification.progression),
    "Plasma Beam": ItemData("Plasma Beam", 3, ItemClassification.progression),
    "Missile Expansion": ItemData("Missile Expansion", 4, ItemClassification.useful, 999),
    "Scan Visor": ItemData("Scan Visor", 5, ItemClassification.progression),
    "Morph Ball Bomb": ItemData("Morph Ball Bomb", 6, ItemClassification.progression),
    "Power Bomb Expansion": ItemData("Power Bomb Expansion", 7, ItemClassification.useful, 99),
    "Flamethrower": ItemData("Flamethrower", 8, ItemClassification.filler),
    "Thermal Visor": ItemData("Thermal Visor", 9, ItemClassification.progression),
    "Charge Beam": ItemData("Charge Beam", 10, ItemClassification.progression),
    "Super Missile": ItemData("Super Missile", 11, ItemClassification.progression),
    "Grapple Beam": ItemData("Grapple Beam", 12, ItemClassification.progression),
    "X-Ray Visor": ItemData("X-Ray Visor", 13, ItemClassification.progression),
    "Ice Spreader": ItemData("Ice Spreader", 14, ItemClassification.filler),
    "Space Jump Boots": ItemData("Space Jump Boots", 15, ItemClassification.progression),
    "Morph Ball": ItemData("Morph Ball", 16, ItemClassification.progression),
    "Combat Visor": ItemData("Combat Visor", 17, ItemClassification.progression),
    "Boost Ball": ItemData("Boost Ball", 18, ItemClassification.progression),
    "Spider Ball": ItemData("Spider Ball", 19, ItemClassification.progression),
    "Power Suit": ItemData("Power Suit", 20, ItemClassification.progression),
    "Gravity Suit": ItemData("Gravity Suit", 21, ItemClassification.progression),
    "Varia Suit": ItemData("Varia Suit", 22, ItemClassification.progression),
    "Phazon Suit": ItemData("Phazon Suit", 23, ItemClassification.progression),
    "Energy Tank": ItemData("Energy Tank", 24, ItemClassification.useful, 14),
    # item 026 is a health refill
    "Wavebuster": ItemData("Wavebuster", 28, ItemClassification.filler),
}

misc_item_table: dict[str, ItemData] = {
    "UnknownItem1": ItemData("UnknownItem1", 25, ItemClassification.useful),
    "Ice Trap": ItemData("Ice Trap", 27, ItemClassification.trap),
}

# These item ids are invalid in the player state, we'll need to exclude it from logic relying on that
custom_suit_upgrade_table: dict[str, ItemData] = {
    "Main Missile": ItemData("Main Missile", 41, ItemClassification.progression),
    "Power Bomb": ItemData("Power Bomb", 42, ItemClassification.progression),

}

artifact_table: dict[str, ItemData] = {
    "Artifact of Truth": ItemData("Artifact of Truth", 29, ItemClassification.progression),
    "Artifact of Strength": ItemData("Artifact of Strength", 30, ItemClassification.progression),
    "Artifact of Elder": ItemData("Artifact of Elder", 31, ItemClassification.progression),
    "Artifact of Wild": ItemData("Artifact of Wild", 32, ItemClassification.progression),
    "Artifact of Lifegiver": ItemData("Artifact of Lifegiver", 33, ItemClassification.progression),
    "Artifact of Warrior": ItemData("Artifact of Warrior", 34, ItemClassification.progression),
    "Artifact of Chozo": ItemData("Artifact of Chozo", 35, ItemClassification.progression),
    "Artifact of Nature": ItemData("Artifact of Nature", 36, ItemClassification.progression),
    "Artifact of Sun": ItemData("Artifact of Sun", 37, ItemClassification.progression),
    "Artifact of World": ItemData("Artifact of World", 38, ItemClassification.progression),
    "Artifact of Spirit": ItemData("Artifact of Spirit", 39, ItemClassification.progression),
    "Artifact of Newborn": ItemData("Artifact of Newborn", 40, ItemClassification.progression),
}

item_table: dict[str, ItemData] = {
    **suit_upgrade_table, **artifact_table, **custom_suit_upgrade_table, **misc_item_table}
