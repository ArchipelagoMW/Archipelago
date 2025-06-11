from typing import TYPE_CHECKING
from ..Types import ExitData, LocData, BrushTechniques, RegionNames, EventData

if TYPE_CHECKING:
    from .. import OkamiWorld

exits = {
    RegionNames.SHINSHU_FIELD: [ExitData("Shinshu Field - To Cursed Hana Valley", RegionNames.CURSED_HANA_VALLEY,
                                         doesnt_have_events=["Hana Valley - Guardian Sapling Restoration"]),
                                ExitData("Shinshu field - To Hana Valley", RegionNames.HANA_VALLEY,
                                         has_events=["Hana Valley - Guardian Sapling Restoration"]),
                                ExitData("Shinshu field - To Kamiki Village", RegionNames.KAMIKI_VILLAGE),
                                ExitData("Cross Cave to Agata Forest", RegionNames.SHINSHU_FIELD_AGATA_CAVE,
                                         needs_swim=True),
                                ExitData("Enter Tama's house",RegionNames.TAMA_HOUSE)],
    RegionNames.SHINSHU_FIELD_AGATA_CAVE: [ExitData('To Curesed Agata Forest', RegionNames.CURSED_AGATA_FOREST,
                                                    has_events=["Shinshu Field - Open Entrance to Agata Forest"]),
                                           ExitData("Cross Cave to Shinshu Field", RegionNames.SHINSHU_FIELD)],
    RegionNames.TAMA_HOUSE: [ExitData("Exit to Shinshu field",RegionNames.SHINSHU_FIELD)]

}
events = {
    RegionNames.SHINSHU_FIELD_AGATA_CAVE: {
        "Shinshu Field - Open Entrance to Agata Forest": EventData(cherry_bomb_level=1)
    }
}
locations = {
    RegionNames.TAMA_HOUSE: {
        "Shinshu Field - Bakigami" : LocData(17,has_events=["Kamiki Village - Restore Sakuya's Tree"])
    }
}
