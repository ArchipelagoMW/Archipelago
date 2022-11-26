import typing

from BaseClasses import Item
from typing import Dict, List


class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    type: str
    progression: bool
    filler: bool = False


item_table: Dict[str, ItemData] = {
    # Units
    'Spearman': ItemData(52000, 'Unit', True),
    'Wagon': ItemData(52001, 'Unit', False),
    'Mage': ItemData(52002, 'Unit', True),
    'Archer': ItemData(52003, 'Unit', True),
    'Knight': ItemData(52004, 'Unit', True),
    'Ballista': ItemData(52005, 'Unit', True),
    'Golem': ItemData(52006, 'Unit', False),
    'Harpy': ItemData(52007, 'Unit', True),
    'Witch': ItemData(52008, 'Unit', False),
    'Dragon': ItemData(52009, 'Unit', True),
    'Balloon': ItemData(52010, 'Unit', False),
    'Barge': ItemData(52011, 'Unit', True),
    'Merfolk': ItemData(52012, 'Unit', True),
    'Turtle': ItemData(52013, 'Unit', True),
    'Harpoon Ship': ItemData(52014, 'Unit', True),
    'Warship': ItemData(52015, 'Unit', True),
    'Thief': ItemData(52016, 'Unit', True),
    'Rifleman': ItemData(52017, 'Unit', True),

    # Map Triggers
    'Eastern Bridges': ItemData(52018, 'Trigger', True),
    'Southern Walls': ItemData(52019, 'Trigger', True),
    'Final Bridges': ItemData(52020, 'Trigger', True),
    'Final Walls': ItemData(52021, 'Trigger', True),
    'Final Sickle': ItemData(52022, 'Trigger', True),

    # Player Buffs
    'Income Boost': ItemData(52023, 'Boost', False, True),

    'Commander Defense Boost': ItemData(52024, 'Boost', False, True),

    # Factions
    'Cherrystone Commanders': ItemData(52025, 'Faction', False),
    'Felheim Commanders': ItemData(52026, 'Faction', False),
    'Floran Commanders': ItemData(52027, 'Faction', False),
    'Heavensong Commanders': ItemData(52028, 'Faction', False),
    'Requiem Commanders': ItemData(52029, 'Faction', False),
    'Outlaw Commanders': ItemData(52030, 'Faction', False),

    # Event Items
    'Wargroove Victory': ItemData(None, 'Goal', True)

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