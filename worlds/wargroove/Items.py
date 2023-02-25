import typing

from BaseClasses import Item, ItemClassification
from typing import Dict, List

PROGRESSION = ItemClassification.progression
PROGRESSION_SKIP_BALANCING = ItemClassification.progression_skip_balancing
USEFUL = ItemClassification.useful
FILLER = ItemClassification.filler


class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    type: str
    classification: ItemClassification = PROGRESSION


item_table: Dict[str, ItemData] = {
    # Units
    'Spearman': ItemData(52000, 'Unit'),
    'Wagon': ItemData(52001, 'Unit', USEFUL),
    'Mage': ItemData(52002, 'Unit'),
    'Archer': ItemData(52003, 'Unit'),
    'Knight': ItemData(52004, 'Unit'),
    'Ballista': ItemData(52005, 'Unit'),
    'Golem': ItemData(52006, 'Unit', USEFUL),
    'Harpy': ItemData(52007, 'Unit'),
    'Witch': ItemData(52008, 'Unit', USEFUL),
    'Dragon': ItemData(52009, 'Unit'),
    'Balloon': ItemData(52010, 'Unit', USEFUL),
    'Barge': ItemData(52011, 'Unit'),
    'Merfolk': ItemData(52012, 'Unit'),
    'Turtle': ItemData(52013, 'Unit'),
    'Harpoon Ship': ItemData(52014, 'Unit'),
    'Warship': ItemData(52015, 'Unit'),
    'Thief': ItemData(52016, 'Unit'),
    'Rifleman': ItemData(52017, 'Unit'),

    # Map Triggers
    'Eastern Bridges': ItemData(52018, 'Trigger'),
    'Southern Walls': ItemData(52019, 'Trigger'),
    'Final Bridges': ItemData(52020, 'Trigger', PROGRESSION_SKIP_BALANCING),
    'Final Walls': ItemData(52021, 'Trigger', PROGRESSION_SKIP_BALANCING),
    'Final Sickle': ItemData(52022, 'Trigger', PROGRESSION_SKIP_BALANCING),

    # Player Buffs
    'Income Boost': ItemData(52023, 'Boost', FILLER),

    'Commander Defense Boost': ItemData(52024, 'Boost', FILLER),

    # Factions
    'Cherrystone Commanders': ItemData(52025, 'Faction', USEFUL),
    'Felheim Commanders': ItemData(52026, 'Faction', USEFUL),
    'Floran Commanders': ItemData(52027, 'Faction', USEFUL),
    'Heavensong Commanders': ItemData(52028, 'Faction', USEFUL),
    'Requiem Commanders': ItemData(52029, 'Faction', USEFUL),
    'Outlaw Commanders': ItemData(52030, 'Faction', USEFUL),

    # Event Items
    'Wargroove Victory': ItemData(None, 'Goal')

}


class CommanderData(typing.NamedTuple):
    name: str
    internal_name: str
    alt_name: str = None


faction_table: Dict[str, List[CommanderData]] = {
    'Starter': [
        CommanderData('Mercival', 'commander_mercival')
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
        CommanderData('Greenfinger', 'commander_greenfinger'),
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
    'Outlaw': [
        CommanderData('Wulfar', 'commander_wulfar'),
        CommanderData('Twins', 'commander_twins', 'Errol & Orla'),
        CommanderData('Vesper', 'commander_vesper')
    ]
}