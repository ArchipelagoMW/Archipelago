import typing

from BaseClasses import Item
from typing import Dict


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

    'CO Defense Boost': ItemData(52024, False, True),

    # Factions
    'Cherrystone': ItemData(52025, False),
    'Felheim': ItemData(52026, False),
    'Florans': ItemData(52027, False),
    'Heavensong': ItemData(52028, False),
    'Requiem': ItemData(52029, False),
    'Outlaws': ItemData(52030, False),

    # Event Items
    'Wargroove Victory': ItemData(None, True, True)

}


class CommanderData(typing.NamedTuple):
    name: str
    charge_rate: int
    internal_name: str
    alt_name: str = None


faction_table = {
    'Starter': [
        CommanderData('Mercival', 7, 'commander_mercival')
    ],
    'Cherrystone': [
        CommanderData('Mercia', 10, 'commander_mercia'),
        CommanderData('Emeric', 10, 'commander_emeric'),
        CommanderData('Caesar', 7, 'commander_caesar'),
    ],
    'Felheim': [
        CommanderData('Valder', 20, 'commander_valder'),
        CommanderData('Ragna', 5, 'commander_ragna'),
        CommanderData('Sigrid', 7, 'commander_sigrid')
    ],
    'Florans': [
        CommanderData('Greenfinger', 7, 'commander_greenfinger'),
        CommanderData('Sedge', 5, 'commander_sedge'),
        CommanderData('Nuru', 7, 'commander_nuru')
    ],
    'Heavensong': [
        CommanderData('Tenri', 5, 'commander_tenri'),
        CommanderData('Koji', 5, 'commander_koji'),
        CommanderData('Ryota', 10, 'commander_ryota')
    ],
    'Requiem': [
        CommanderData('Elodie', 5, 'commander_elodie'),
        CommanderData('Dark Mercia', 5, 'commander_darkmercia')
    ],
    'Outlaws': [
        CommanderData('Wulfar', 10, 'commander_wulfar'),
        CommanderData('Twins', 7, 'commander_twins', 'Errol & Orla'),
        CommanderData('Vesper', 5, 'commander_vesper')
    ]
}