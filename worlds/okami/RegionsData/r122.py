from typing import TYPE_CHECKING
from ..Types import ExitData, LocData, BrushTechniques

if TYPE_CHECKING:
    from .. import OkamiWorld

regions = {
    "r122_1": "River of the Heavens (Kamiki Side)",
    "r122_2": "River of the Heavens (Nagi side)"
}
exits = {
    "r122_1": [ExitData("Exit to Cursed Kamiki", "r100",
                        doesnt_have_events=["Cursed Kamiki - Cutting the peach"]),
               ExitData("Exit to Kamiki (stone)", "r102_1",
                        has_events=["Cursed Kamiki - Cutting the peach"]
                        ,doesnt_have_events=["Kamiki Village - Restoring the villagers"]),
               ExitData("Exit to Kamiki", "r102_2",
                        has_events=["Cursed Kamiki - Cutting the peach","Kamiki Village - Restoring the villagers"]),
               ExitData("Crossing the River to the Cave of Nagi", "r122_2",
                        has_events=["River of the Heavens - Restoring the River"])],
    "r122_2": [ExitData("Crossing the River to Kamiki Village", "r122_1",
                        has_events=["River of the Heavens - Restoring the River"]),
               ExitData("Exit to Cave of Nagi", "r101_1")]
}
events = {
    "r122_1": {
        "River of the Heavens - Restoring the River": LocData(0,
                                                              required_brush_techniques=[BrushTechniques.REJUVENATION]),
    }
}
locations = {
    "r122_1": {
        "River of the Heavens - Ledge Chest": LocData(1),
        "River of the Heavens - Yomigami": LocData(2),
    },
    "r122_2": {
        "River of the Heavens - Astral Pouch": LocData(3),
    }
}
