from typing import TYPE_CHECKING
from ..Types import ExitData, LocData, BrushTechniques, RegionNames, EventData

if TYPE_CHECKING:
    from .. import OkamiWorld

exits = {
    RegionNames.CURSED_AGATA_FOREST: [ExitData("Cursed Agata Forest - To Shinshu Field", RegionNames.CURSED_SHINSHU_FIELD),
                                      ExitData("Agata Forest Restoration",RegionNames.AGATA_FOREST_WAKA)],

}
events = {
    RegionNames.CURSED_AGATA_FOREST: {
        "Agata Forest - Restore Guardian Sapling": EventData(
            required_brush_techniques=[BrushTechniques.GREENSPROUT_BLOOM],cherry_bomb_level=1)
    },
}
locations = {
    RegionNames.CURSED_AGATA_FOREST:{
        "Agata Forest - Burning Chest near Madame Fawn's 1": LocData(58),
        "Agata Forest - Burning Chest near Madame Fawn's 2": LocData(59),
        "Agata Forest - Burning Chest near Madame Fawn's 3": LocData(60),
        "Agata Forest - Ledge chest near Madame Fawn's ": LocData(64, required_brush_techniques=[BrushTechniques.WATERSPROUT]),

    }
}
