from BaseClasses import ItemClassification
from .logic.regions.Sector4 import Sector4PumpControl
from .logic.regions.MainDeck import OperationsDeck

all_item_data = [
    # Name, Major, Groups, ID
    ("Level 0 Keycard", ItemClassification.progression, ["Keycards"], 1),
    ("Missile Data", ItemClassification.progression, ["Weapons", "Missiles"], 2),
    ("Morph Ball", ItemClassification.progression, ["Movement", "Morph Ball"], 3),
    ("Charge Beam", ItemClassification.progression, ["Weapons", "Beams"], 4),
    ("Level 1 Keycard", ItemClassification.progression, ["Keycards"], 5),
    ("Bomb Data", ItemClassification.progression, ["Weapons", "Morph Ball"], 6),
    ("Hi-Jump", ItemClassification.progression, ["Movement"], 7),
    ("Speed Booster", ItemClassification.progression, ["Movement"], 8),
    ("Level 2 Keycard", ItemClassification.progression, ["Keycards"], 9),
    ("Super Missile", ItemClassification.progression, ["Weapons", "Missiles"], 10),
    ("Varia Suit", ItemClassification.progression, ["Suit", "Defense"], 11),
    ("Level 3 Keycard", ItemClassification.progression, ["Keycards"], 12),
    ("Ice Missile", ItemClassification.progression, ["Weapons", "Missiles"], 13),
    ("Wide Beam", ItemClassification.progression, ["Weapons", "Beams"], 14),
    ("Power Bomb Data", ItemClassification.progression, ["Weapons", "Morph Ball"], 15),
    ("Space Jump", ItemClassification.progression, ["Movement"], 16),
    ("Plasma Beam", ItemClassification.progression, ["Weapons", "Beams"], 17),
    ("Gravity Suit", ItemClassification.progression, ["Suit", "Defense"], 18),
    ("Level 4 Keycard", ItemClassification.progression, ["Keycards"], 19),
    ("Diffusion Missile", ItemClassification.progression, ["Weapons", "Missiles"], 20),
    ("Wave Beam", ItemClassification.progression, ["Weapons", "Beams"], 21),
    ("Screw Attack", ItemClassification.progression, ["Weapons", "Suit"], 22),
    ("Ice Beam", ItemClassification.progression, ["Weapons", "Beams"], 23),
    ("Missile Tank", ItemClassification.filler, ["Weapons", "Missiles"], 24),
    ("Energy Tank", ItemClassification.progression_deprioritized_skip_balancing, ["Suit", "Defense"], 25),
    ("Power Bomb Tank", ItemClassification.filler, ["Weapons", "Bombs"], 26),
    ("Ice Trap", ItemClassification.trap, [], 27),
    ("Infant Metroid", ItemClassification.progression, ["Metroid"], 28),
    ("Nothing", ItemClassification.trap, [], 29),
]

events: list[tuple[str, ItemClassification, str, str]] = [
    ("Victory", ItemClassification.progression, OperationsDeck.name, "Victory"),
    ("Pump Control", ItemClassification.progression, Sector4PumpControl.name, "Pump Control Activated")
]
