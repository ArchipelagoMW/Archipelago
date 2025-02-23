from BaseClasses import Item, ItemClassification
from typing import Dict, List, NamedTuple, Optional

PROGRESSION = ItemClassification.progression
PROGRESSION_SKIP_BALANCING = ItemClassification.progression_skip_balancing
USEFUL = ItemClassification.useful
FILLER = ItemClassification.filler


class ItemData(NamedTuple):
    code: Optional[int]
    type: str
    classification: ItemClassification = PROGRESSION


item_table: Dict[str, ItemData] = {
    # Units
    'Spearman': ItemData(252000, 'Unit'),
    'Wagon': ItemData(252001, 'Unit'),
    'Mage': ItemData(252002, 'Unit'),
    'Archer': ItemData(252003, 'Unit'),
    'Knight': ItemData(252004, 'Unit'),
    'Ballista': ItemData(252005, 'Unit'),
    'Trebuchet': ItemData(252006, 'Unit'),
    'Golem': ItemData(252007, 'Unit'),
    'Air Trooper': ItemData(252008, 'Unit'),
    'Harpy': ItemData(252009, 'Unit'),
    'Witch': ItemData(252010, 'Unit'),
    'Dragon': ItemData(252011, 'Unit'),
    'Balloon': ItemData(252012, 'Unit'),
    'Barge': ItemData(252013, 'Unit'),
    'River Boat': ItemData(252014, 'Unit'),
    'Merfolk': ItemData(252015, 'Unit'),
    'Turtle': ItemData(252016, 'Unit'),
    'Harpoon Ship': ItemData(252017, 'Unit'),
    'Warship': ItemData(252018, 'Unit'),
    'Frog': ItemData(252019, 'Unit'),
    'Kraken': ItemData(252020, 'Unit'),
    'Thief': ItemData(252021, 'Unit'),
    'Rifleman': ItemData(252022, 'Unit'),

    # Map Triggers
    'Bridges Event': ItemData(252023, 'Trigger'),
    'Walls Event': ItemData(252024, 'Trigger'),
    'Landing Event': ItemData(252025, 'Trigger'),
    'Airstrike Event': ItemData(252026, 'Trigger'),
    'Final North': ItemData(252027, 'Trigger', PROGRESSION_SKIP_BALANCING),
    'Final East': ItemData(252028, 'Trigger', PROGRESSION_SKIP_BALANCING),
    'Final South': ItemData(252029, 'Trigger', PROGRESSION_SKIP_BALANCING),
    'Final West': ItemData(252030, 'Trigger', PROGRESSION_SKIP_BALANCING),
    'Final Center': ItemData(252031, 'Trigger', PROGRESSION_SKIP_BALANCING),

    # Player Buffs
    'Income Boost': ItemData(252032, 'Boost', FILLER),

    'Commander Defense Boost': ItemData(252033, 'Boost', FILLER),
    'Groove Boost': ItemData(252041, 'Boost', FILLER),

    # Factions
    'Cherrystone Commanders': ItemData(252034, 'Faction', USEFUL),
    'Felheim Commanders': ItemData(252035, 'Faction', USEFUL),
    'Floran Commanders': ItemData(252036, 'Faction', USEFUL),
    'Heavensong Commanders': ItemData(252037, 'Faction', USEFUL),
    'Requiem Commanders': ItemData(252038, 'Faction', USEFUL),
    'Pirate Commanders': ItemData(252039, 'Faction', USEFUL),
    'Faahri Commanders': ItemData(252040, 'Faction', USEFUL),

    # Event Items
    'Wargroove 2 Victory': ItemData(None, 'Goal')

}

item_id_name: Dict[int, str] = {}
for name in item_table.keys():
    id = item_table[name].code
    if id is not None:
        item_id_name[id] = name


class CommanderData(NamedTuple):
    name: str
    internal_name: str
    alt_name: Optional[str] = None


faction_table: Dict[str, List[CommanderData]] = {
    'Starter': [
        CommanderData('Mercival', 'commander_mercival', 'Mercival II')
    ],
    'Cherrystone': [
        CommanderData('Mercia', 'commander_mercia'),
        CommanderData('Emeric', 'commander_emeric'),
        CommanderData('Caesar', 'commander_caesar'),
    ],
    'Felheim': [
        CommanderData('Valder', 'commander_valder'),
        CommanderData('Ragna', 'commander_ragna'),
        CommanderData('Sigrid', 'commander_sigrid')
    ],
    'Floran': [
        CommanderData('Greenfinger', 'commander_greenfinger', 'Zawan'),
        CommanderData('Sedge', 'commander_sedge'),
        CommanderData('Nuru', 'commander_nuru')
    ],
    'Heavensong': [
        CommanderData('Tenri', 'commander_tenri'),
        CommanderData('Koji', 'commander_koji'),
        CommanderData('Ryota', 'commander_ryota')
    ],
    'Requiem': [
        CommanderData('Elodie', 'commander_elodie'),
        CommanderData('Dark Mercia', 'commander_darkmercia')
    ],
    'Pirate': [
        CommanderData('Wulfar', 'commander_wulfar_pirate'),
        CommanderData('Twins', 'commander_twins', 'Errol & Orla'),
        CommanderData('Vesper', 'commander_vesper'),
        CommanderData('Nadia', 'commander_nadia')
    ],
    'Faahri': [
        CommanderData('Lytra', 'commander_lytra'),
        CommanderData('Pistil', 'commander_pistil'),
        CommanderData('Rhomb', 'commander_rhomb')
    ]
}


class Wargroove2Item(Item):
    game = "Wargroove 2"

    def __init__(self, name, player):
        item_data = item_table[name]
        super(Wargroove2Item, self).__init__(
            name,
            item_data.classification,
            item_data.code,
            player
        )
