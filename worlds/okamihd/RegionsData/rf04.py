from typing import TYPE_CHECKING

from ..Enums.BrushTechniques import BrushTechniques
from ..Enums.OkamiEnnemies import OkamiEnnemies
from ..Enums.RegionNames import RegionNames
from ..Types import ExitData, LocData, EventData

if TYPE_CHECKING:
    from .. import OkamiWorld

exits = {
    # small region to force waka fight to be cleared before acessing the rest of the forest.
    RegionNames.AGATA_FOREST_WAKA: [
        ExitData("Agata Forest Waka cutscene", RegionNames.AGATA_FOREST, has_events=["Agata Forest - Defeat Waka"])],
    RegionNames.AGATA_FOREST: [ExitData("Agata Forest - To Taka Pass", RegionNames.CURSED_TAKA_PASS)
        , ExitData("Agata Ruins - Enter Tsuta Ruins", RegionNames.TSUTA_RUINS_1F_MAIN_PART,
                   has_events=["Agata Forest - Open Ruins Door"])]
}
events = {
    RegionNames.AGATA_FOREST_WAKA: {
        "Agata Forest - Defeat Waka": EventData(mandatory_enemies=[OkamiEnnemies.WAKA_1])
    },
    RegionNames.AGATA_FOREST: {
        "Agata Forest - Open Ruins Door": EventData(required_items_events=["Tsuta Ruins Key"])
    }
}
locations = {
    RegionNames.AGATA_FOREST: {
        # the names here could be better.
        "Agata Forest - Treasure Bud near Guardian Sapling Cave": LocData(46, required_brush_techniques=[
            BrushTechniques.GREENSPROUT_BLOOM]),
        "Agata Forest - Treasure Bud 1": LocData(47, required_brush_techniques=[BrushTechniques.GREENSPROUT_BLOOM]),
        "Agata Forest - Treasure Bud on big island": LocData(48, required_brush_techniques=[
            BrushTechniques.GREENSPROUT_BLOOM]),
        "Agata Forest - Treasure Bud island near Kokari": LocData(49, required_brush_techniques=[
            BrushTechniques.GREENSPROUT_BLOOM]),
        "Agata Forest - Treasure Bud near Karude's house": LocData(50, required_brush_techniques=[
            BrushTechniques.GREENSPROUT_BLOOM]),
        "Agata Forest - Treasure Bud near Karude's house cursed patch": LocData(51, required_brush_techniques=[
            BrushTechniques.GREENSPROUT_BLOOM]),
        "Agata Forest - Treasure Bud near waterfall": LocData(52, required_brush_techniques=[
            BrushTechniques.GREENSPROUT_BLOOM]),
        "Agata Forest - Treasure Bud near Mme. Fawn's Cave": LocData(53, required_brush_techniques=[
            BrushTechniques.GREENSPROUT_BLOOM]),
        "Agata Forest - Treasure Bud 2": LocData(54, required_brush_techniques=[BrushTechniques.GREENSPROUT_BLOOM]),
        "Agata Forest - Treasure Bud Inside Tree": LocData(55, required_brush_techniques=[
            BrushTechniques.GREENSPROUT_BLOOM]),
        "Agata Forest - Chest at Guardian Sapling": LocData(56),
        "Agata Forest - Buried chest near shortcut": LocData(57, buried=1),
        # Probably needs something more to get on top
        "Agata Forest - Chest on top of the big tree": LocData(61, power_slash_level=1, required_brush_techniques=[
            BrushTechniques.GREENSPROUT_VINE]),
        "Agata Forest - Freestanding stray Bead": LocData(62,
                                                          required_brush_techniques=[BrushTechniques.GREENSPROUT_VINE]),
        "Agata Forest - Freestanding Bull Horn": LocData(63,
                                                         required_brush_techniques=[BrushTechniques.GREENSPROUT_VINE]),
        "Agata Forest - Buried Chest on Lake shore": LocData(65, buried=1),
        "Agata Forest - Buried Chest behind Karude's house": LocData(66, buried=1),
        "Agata Forest - Buried Chest on Island": LocData(67, buried=1),
        "Agata Forest - Chest under leaf pile near Shinshu Field entrance": LocData(68, buried=1,
                                                                                    required_brush_techniques=[
                                                                                        BrushTechniques.GALESTROM]),
        "Agata Forest - Chest under leaf pile on ledge": LocData(69, buried=1,
                                                                 required_brush_techniques=[BrushTechniques.GALESTROM]),
        "Agata Forest - Chest under leaf pile near river": LocData(70, buried=1, required_brush_techniques=[
            BrushTechniques.GALESTROM]),
        # "Agata Forest - Buried chest near Tsuta Ruins entrance": LocData(71, buried=2),
        # Add required event after Bridge cutscene
        "Agata Forest - Chest after Bridge cutscene": LocData(72),
        "Agata Forest - Chest near Demon Fang merchant": LocData(73),
        "Agata Forest - Chest near Tusta ruins door": LocData(74),
        "Agata Forest - Fish Giant Salmon with Kokari": LocData(77, power_slash_level=1)
    }
}
