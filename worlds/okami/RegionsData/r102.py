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
    "r102_2":[ExitData("Kamiki Village Torii","r122_1"),
              ExitData("Swim to Kamiki Islands", "r102_3",needs_swim=True)],
    "r102_3":[ExitData("Swim to Kamiki Village", "r102_2",needs_swim=True)],
}
events={
    "r102_1":{
        "Kamiki Village - Restoring the villagers": LocData(0,[BrushTechniques.SUNRISE])
    },
    "r102_3":{
        "End for now" : LocData(0,[BrushTechniques.CRESCENT])
    }
}
locations={
    "r102_1":{
        "Kamiki Village - Sunrise": LocData(6),
    },
    "r102_2":{
        "Kamiki Village - Chest After Mr.Orange Yokai Fight": LocData(7),
        "Kamiki Village - Buried Chest near Komuso": LocData(8, buried_chest=1),
    },
    "r102_3":{
        "Kamiki Village - Island Chest 1": LocData(9),
        "Kamiki Village - Island buried Chest 1": LocData(10,buried_chest=1),
    }
}