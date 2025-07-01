from typing import TYPE_CHECKING

from ..Enums.BrushTechniques import BrushTechniques
from ..Enums.OkamiEnnemies import OkamiEnnemies
from ..Enums.RegionNames import RegionNames
from ..Types import ExitData, LocData,EventData

if TYPE_CHECKING:
    from .. import OkamiWorld

exits = {
    RegionNames.SHINSHU_FIELD: [
        ExitData("Cross Cave to Agata Forest", RegionNames.SHINSHU_FIELD_AGATA_CAVE, needs_swim=True),
        ExitData("Enter Tama's house", RegionNames.TAMA_HOUSE)],
    RegionNames.SHINSHU_FIELD_AGATA_CAVE: [ExitData('To Cursed Agata Forest', RegionNames.CURSED_AGATA_FOREST,
                                                    has_events=["Shinshu Field - Open Entrance to Agata Forest"])],
}
events = {
    RegionNames.SHINSHU_FIELD_AGATA_CAVE: {
        "Shinshu Field - Open Entrance to Agata Forest": EventData(cherry_bomb_level=1)
    }
}
locations = {
    RegionNames.SHINSHU_FIELD: {
        "Shinshu Field - Buried chest between near Guardian Sapling": LocData(27, buried=True),
        "Shinshu Field - Freestanding chest near Guardian Sapling": LocData(28),
        "Shinshu Field - Buried chest near Tama's house": LocData(29, buried=True),
        "Shinshu Field - Buried chest near Lake": LocData(30, buried=True),
        "Shinshu Field - Chest Under Bombable ground near Agata Forest": LocData(31, cherry_bomb_level=1,
                                                                                 required_brush_techniques=[
                                                                                     BrushTechniques.GREENSPROUT_BLOOM]),
        "Shinshu Field - Buried chest near Dojo": LocData(32, buried=True),
        "Shinshu Field - Chest after devil gate": LocData(33, mandatory_enemies=[OkamiEnnemies.GREEN_IMP,
                                                                                 OkamiEnnemies.RED_IMP,
                                                                                 OkamiEnnemies.YELLOW_IMP]),
        # Probably should find a better name for this one
        "Shinshu Field - Buried chest on ledge": LocData(34, buried=True),
        "Shinshu Field - Buried chest near Ovens": LocData(35, buried=True),
        # This is the cherry bomb tutorial. Need to check what happens if you blow the wall before doing the tutorial.
        "Shinshu Field - In Bombable cave near Tama's house": LocData(36, cherry_bomb_level=1),
        "Shinshu Field - In Bombable cave near cat statue": LocData(37, cherry_bomb_level=1),
        "Shinshu Field - Buried Chest in leaf pile near Tama's house": LocData(38, buried=True,
                                                                               required_brush_techniques=[
                                                                                   BrushTechniques.GALESTROM]),
        "Shinshu Field - Chest on Big Torii": LocData(39, required_brush_techniques=[BrushTechniques.WATERSPROUT],
                                                      needs_swim=True),
        "Shinshu Field - Freestanding chest after Rejuvenation": LocData(40),
        "Shinshu Field - Freestanding chest near Agata Forest Cave": LocData(41),
        "Shinshu Field - Freestanding chest near Tama's house": LocData(42),
        "Shinshu Field - Buried Chest in burning leaf pile behind Dojo": LocData(43, buried=1,
                                                                                 required_brush_techniques=[
                                                                                     BrushTechniques.GALESTROM])
    },

    RegionNames.TAMA_HOUSE: {
        "Shinshu Field - Bakigami": LocData(17, required_items_events=["Kamiki Village - Restore Sakuya's Tree"])
    }
}
