from typing import TYPE_CHECKING
from ..Types import ExitData, LocData

if TYPE_CHECKING:
    from .. import OkamiWorld

regions ={
    "r100": "Cursed Kamiki"
}
exits = {
    "r100":[ExitData("Cursed Kamiki Torii","r122_1"),
            ExitData("Kamiki Restoration Cutscene","r102_1",has_events=["Cursed Kamiki - Cutting the peach"])]
}
events={
    "r100":{
        "Cursed Kamiki - Cutting the peach": LocData(0, power_slash_level=1),
    }
}
locations={
}