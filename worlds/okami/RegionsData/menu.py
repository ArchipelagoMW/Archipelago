from typing import TYPE_CHECKING
from ..Types import ExitData, LocData

if TYPE_CHECKING:
    from .. import OkamiWorld

regions ={
    "menu": "Menu"
}
exits = {
    # TODO: in ER this should be the starting point ?  What if the player starts in cursed Kamiki?
    "menu":[ExitData("New Game","r100", doesnt_have_events=["Cursed Kamiki - Cutting the peach"]),
            ExitData("Load Kamiki","r103_1",has_events=["Cursed Kamiki - Cutting the peach"])]
}
events={
}
locations={
}