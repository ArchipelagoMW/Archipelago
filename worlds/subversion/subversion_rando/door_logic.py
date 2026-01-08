from typing import Union

from .area_rando_types import AreaDoor
from .connection_data import area_doors
from .item_data import Item, Items
from .logic_shortcut import LogicShortcut
from .logicCommon import can_use_pbs


def canOpen(door: AreaDoor) -> LogicShortcut:
    return LogicShortcut(lambda loadout: (
        (loadout.game.options.area_rando and door.name in area_doors) or
        loadout.game.door_data[door] in loadout
    ))


vanilla_doors: "dict[AreaDoor, Union[Item, LogicShortcut]]" = {
    area_doors["CraterR"]: can_use_pbs(1),
    area_doors["WestTerminalAccessL"]: can_use_pbs(1),
    area_doors["VulnarCanyonL"]: can_use_pbs(1),
    area_doors["FoyerR"]: Items.Super
}
