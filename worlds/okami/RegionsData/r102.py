from typing import TYPE_CHECKING
from ..Types import ExitData, LocData, BrushTechniques

if TYPE_CHECKING:
    from .. import OkamiWorld

regions ={
    "r102_1": "Kamiki Village (Stone state)",
    "r102_2": "Kamiki Village",
    "r102_3": "Kamiki Village Islands",
}
exits = {
    "r102_1":[ExitData("Kamiki Village (stone) Torii","r122_1"),
            ExitData("Restore the villagers","r102_2",
                     has_events=["Kamiki Village - Restoring the villagers"])],
    "r101_2":[ExitData("Kamiki Village Torii","r_122_1"),
              ExitData("Swim to Kamiki Islands", "r_102_3",needs_swim=True)],
    "r101_3":[ExitData("Swim to Kamiki Village", "r_102_2",needs_swim=True)],
}
events={
    "r102_1":{
        "Kamiki Village - Restoring the villagers": LocData(0,[BrushTechniques.SUNRISE])
    }
}
locations={
    "r102_1":{
        "Kamiki Village - Sunrise": LocData(6),
    },
    "r101_2":{
        "Kamiki Village - Chest After Mr.Orange Yokai Fight": LocData(7),
        "Kamiki Village - Buried Chest near Komuso": LocData(8, buried_chest=1)
    }
}