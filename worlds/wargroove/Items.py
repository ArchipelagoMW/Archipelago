import typing

from BaseClasses import Item
from typing import Dict, List


class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    progression: bool
    filler: bool = False


item_table: Dict[str, ItemData] = {
    # Units
    'Spearman': ItemData(52000, True),
    'Wagon': ItemData(52001, False),
    'Mage': ItemData(52002, True),
    'Archer': ItemData(52003, True),
    'Knight': ItemData(52004, True),
    'Ballista': ItemData(52005, True),
    'Golem': ItemData(52006, False),
    'Harpy': ItemData(52007, True),
    'Witch': ItemData(52008, False),
    'Dragon': ItemData(52009, False),
    'Balloon': ItemData(52010, False),
    'Barge': ItemData(52011, True),
    'Merfolk': ItemData(52012, True),
    'Turtle': ItemData(52013, True),
    'Harpoon Ship': ItemData(52014, True),
    'Warship': ItemData(52015, True),
    'Thief': ItemData(52016, True),
    'Rifleman': ItemData(52017, False),

    # Map Triggers
    'Eastern Bridges': ItemData(52018, True),
    'Southern Walls': ItemData(52019, True),
    'Final Bridges': ItemData(52020, True),
    'Final Walls': ItemData(52021, True),
    'Final Sickle': ItemData(52022, True),

    # Player Buffs
    'Income Boost': ItemData(52023, False, True),

    'Commander Defense Boost': ItemData(52024, False, True),

    # Factions
    'Cherrystone Commanders': ItemData(52025, False),
    'Felheim Commanders': ItemData(52026, False),
    'Floran Commanders': ItemData(52027, False),
    'Heavensong Commanders': ItemData(52028, False),
    'Requiem Commanders': ItemData(52029, False),
    'Outlaw Commanders': ItemData(52030, False),

    # Event Items
    'Wargroove Victory': ItemData(None, True, True)

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