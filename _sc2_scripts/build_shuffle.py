"""
A script for modifying mod files directly to shuffle what units are built where
"""

from typing import *
from dataclasses import dataclass

abil_data_filepath = 'D:/Battle.net/Starcraft II/Mods/ArchipelagoPlayer.SC2Mod/Base.SC2Data/GameData/AbilData.xml'
unit_data_filepath = 'D:/Battle.net/Starcraft II/Mods/ArchipelagoPlayer.SC2Mod/Base.SC2Data/GameData/UnitData.xml'

T = TypeVar('T')
Field = Tuple[T, int]

@dataclass
class TrainInfo:
    abil: Field[str]
    abil_index: Field[int]
    abil_index_time: Field[int]
    abil_index_unit: Field[str]
    abil_index_button: Field[str]


def parse_train_commands() -> List[TrainInfo]:
    result: List[TrainInfo] = []
    with open(abil_data_filepath, 'r') as fp:
        for line_num, line in enumerate(fp):
            if '<CAbilTrain ' not in line:
                continue
            print(f'{line_num}: {line}', end='')

if __name__ == '__main__':
    parse_train_commands()
