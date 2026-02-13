from BaseClasses import ItemClassification
from .data.items import all_item_data, events


class ItemData:
    name: str
    classification: ItemClassification
    groups: list[str]
    mars_id: int

    def __init__(self, name: str, classification: ItemClassification, groups: list[str], mars_id: int):
        self.name = name
        self.classification = classification
        self.groups = groups
        self.mars_id = mars_id

    def to_json(self):
        return {
            "name": self.name,
            "mars_id": self.mars_id
        }

    def __repr__(self):
        return self.name

item_table: dict[str, ItemData] = dict()

for item in all_item_data:
    item_table[item[0]] = ItemData(item[0], item[1], item[2], item[3])

item_names = [item for item in item_table.keys()]

valid_item_names = [*item_names, *[event[3] for event in events], "Wall Jump Boots"]

# Everything not listed here has a quantity of one
default_item_quantities = {
    "Nothing": 0,
    "Level 0 Keycard": 0,
    "Missile Tank": 48,
    "Energy Tank": 20,
    "Power Bomb Tank": 36,
    "Ice Trap": 0,
    "Infant Metroid": 0
}

major_upgrades = [
    "Missile Data",
    "Morph Ball",
    "Charge Beam",
    "Bomb Data",
    "Hi-Jump",
    "Speed Booster",
    "Level 1 Keycard",
    "Level 2 Keycard",
    "Level 3 Keycard",
    "Level 4 Keycard",
    "Super Missile",
    "Varia Suit",
    "Ice Missile",
    "Wide Beam",
    "Power Bomb Data",
    "Space Jump",
    "Plasma Beam",
    "Gravity Suit",
    "Diffusion Missile",
    "Wave Beam",
    "Screw Attack",
    "Ice Beam"
]

major_jingles = [
    *major_upgrades,
    "Infant Metroid"
]

ap_name_to_mars_name = {
    "Nothing": "None",
    "Level 0 Keycard": "Level0",
    "Missile Data": "Missiles",
    "Morph Ball": "MorphBall",
    "Charge Beam": "ChargeBeam",
    "Level 1 Keycard": "Level1",
    "Bomb Data": "Bombs",
    "Hi-Jump": "HiJump",
    "Speed Booster": "SpeedBooster",
    "Level 2 Keycard": "Level2",
    "Super Missile": "SuperMissiles",
    "Varia Suit": "VariaSuit",
    "Level 3 Keycard": "Level3",
    "Ice Missile": "IceMissiles",
    "Wide Beam": "WideBeam",
    "Power Bomb Data": "PowerBombs",
    "Space Jump": "SpaceJump",
    "Plasma Beam": "PlasmaBeam",
    "Gravity Suit": "GravitySuit",
    "Level 4 Keycard": "Level4",
    "Diffusion Missile": "DiffusionMissiles",
    "Wave Beam": "WaveBeam",
    "Screw Attack": "ScrewAttack",
    "Ice Beam": "IceBeam",
    "Missile Tank": "MissileTank",
    "Energy Tank": "EnergyTank",
    "Power Bomb Tank": "PowerBombTank",
    "Ice Trap": "IceTrap",
    "Infant Metroid": "InfantMetroid"
}

mars_name_to_ap_name = {v: k for k, v in ap_name_to_mars_name.items()}