from BaseClasses import Item, ItemClassification
import typing


class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    progression: ItemClassification


class MetroidPrimeItem(Item):
    game: str = "Metroid Prime"


suit_upgrade_table = {
    "Power Suit": ItemData(5031000, ItemClassification.progression),
    "Power Beam": ItemData(5031001, ItemClassification.progression),
    "Combat Visor": ItemData(5031002, ItemClassification.progression),
    "Scan Visor": ItemData(5031003, ItemClassification.progression),
    "Wave Beam": ItemData(5031004, ItemClassification.progression),
    "Ice Beam": ItemData(5031005, ItemClassification.progression),
    "Plasma Beam": ItemData(5031006, ItemClassification.progression),
    "Morph Ball": ItemData(5031007, ItemClassification.progression),
    "Morph Ball Bombs": ItemData(5031008, ItemClassification.progression),
    "Boost Ball": ItemData(5031009, ItemClassification.progression),
    "Spider Ball": ItemData(5031010, ItemClassification.progression),
    "Power Bomb": ItemData(5031011, ItemClassification.progression),
    "Varia Suit": ItemData(5031012, ItemClassification.progression),
    "Gravity Suit": ItemData(5031013, ItemClassification.progression),
    "Phazon Suit": ItemData(5031014, ItemClassification.progression),
    "Thermal Visor": ItemData(5031015, ItemClassification.progression),
    "X-Ray Visor": ItemData(5031016, ItemClassification.progression),
    "Missile Launcher": ItemData(5031017, ItemClassification.progression),
    "Charge Beam": ItemData(5031018, ItemClassification.progression),
    "Super Missile": ItemData(5031019, ItemClassification.progression),
    "Wavebuster": ItemData(5031020, ItemClassification.filler),
    "Ice Spreader": ItemData(5031021, ItemClassification.filler),
    "Flamethrower": ItemData(5031022, ItemClassification.filler),
    "Space Jump Boots": ItemData(5031023, ItemClassification.progression),
    "Grapple Beam": ItemData(5031024, ItemClassification.progression)
}

expansion_table = {
    "Missile Expansion": ItemData(5031025, ItemClassification.useful),
    "Energy Tank": ItemData(5031026, ItemClassification.useful),
    "Power Bomb Expansion": ItemData(5031027, ItemClassification.useful)
}

artifact_table = {
    "Artifact of Truth": ItemData(5031028, ItemClassification.progression),
    "Artifact of Strength": ItemData(5031029, ItemClassification.progression),
    "Artifact of Nature": ItemData(5031030, ItemClassification.progression),
    "Artifact of Wild": ItemData(5031031, ItemClassification.progression),
    "Artifact of Lifegiver": ItemData(5031032, ItemClassification.progression),
    "Artifact of Chozo": ItemData(5031033, ItemClassification.progression),
    "Artifact of Warrior": ItemData(5031034, ItemClassification.progression),
    "Artifact of Sun": ItemData(5031035, ItemClassification.progression),
    "Artifact of Elder": ItemData(5031036, ItemClassification.progression),
    "Artifact of Spirit": ItemData(5031037, ItemClassification.progression),
    "Artifact of World": ItemData(5031038, ItemClassification.progression),
    "Artifact of Newborn": ItemData(5031039, ItemClassification.progression),
}

item_table = {**suit_upgrade_table, **expansion_table, **artifact_table}
