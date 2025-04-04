from typing import TYPE_CHECKING
from ..Types import ExitData, LocData, BrushTechniques

if TYPE_CHECKING:
    from .. import OkamiWorld

regions ={
    "r101_1": "Cave of Nagi",
    "r101_2": "Cave of Nagi (Tachigami Cutscene)"
}
exits = {
    "r101_1":[ExitData("Exit to River of the Heavens","r122_2"),
             ExitData("Repair Nagi's statue","r101_2",has_events=["Cave of Nagi - Repair statue"])],
    "r101_2":[ExitData("Clear power slash tutorial","r101_1",has_events=["Cave of Nagi - Cut tutorial rock"])]
}
events={
    'r101_1':{
        "Cave of Nagi - Repair statue": LocData(0, required_brush_techniques=[BrushTechniques.REJUVENATION]),
    },
    "r101_2":{
        "Cave of Nagi - Cut tutorial rock": LocData(0, power_slash_level=1)
    }
}
locations={
    "r101_1":{
        "Cave of Nagi - Stray Bead Chest": LocData(4),
    },
    "r101_2":{
        "Cave of Nagi - Tachigami": LocData(5),
    }
}