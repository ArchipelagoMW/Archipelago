from enum import IntEnum
from typing import Optional, NamedTuple, Dict

from BaseClasses import Location, Region
from .Items import MedievilItem

class MedievilLocationCategory(IntEnum):
    FILLER = 0
    PROGRESSION = 1
    FUN = 2
    LEVEL_END = 4
    SKIP = 5

class MedievilLocationData(NamedTuple):
    name: str
    default_item: str
    category: MedievilLocationCategory


class MedievilLocation(Location):
    game: str = "Medievil"
    category: MedievilLocationCategory
    default_item_name: str

    def __init__(
            self,
            player: int,
            name: str,
            category: MedievilLocationCategory,
            default_item_name: str,
            address: Optional[int] = None,
            parent: Optional[Region] = None):
        super().__init__(player, name, address, parent)
        self.default_item_name = default_item_name
        self.category = category

    @staticmethod
    def get_name_to_id() -> dict:
        base_id = 9900000
        return ({location_data.name: id for id, location_data in enumerate(location_tables["MainWorld"], base_id + 1 )})

    def place_locked_item(self, item: MedievilItem):
        self.item = item
        self.locked = True
        item.location = self
# don't forget you need minimum number of locations to be the max of the progression items
location_tables = {
"MainWorld": [
    MedievilLocationData(f"Adding Tons of locations for filler1",f"Level_End" ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData(f"Adding Tons of locations for filler2",f"Level_End" ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData(f"Adding Tons of locations for filler3",f"Level_End" ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData(f"Adding Tons of locations for filler4",f"Level_End",MedievilLocationCategory.LEVEL_END),
    MedievilLocationData(f"Adding Tons of locations for filler5",f"Level_End" ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData(f"Adding Tons of locations for filler6",f"Level_End" ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData(f"Adding Tons of locations for filler7",f"Level_End" ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData(f"Adding Tons of locations for filler8",f"Level_End" ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData(f"Adding Tons of locations for filler9",f"Level_End" ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData(f"Adding Tons of locations for filler0",f"Level_End" ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData(f"1Adding Tons of locations for filler",f"Level_End" ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData(f"2Adding Tons of locations for filler",f"Level_End" ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData(f"3Adding Tons of locations for filler",f"Level_End" ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData(f"4Adding Tons of locations for filler",f"Level_End" ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData(f"5Adding Tons of locations for filler",f"Level_End" ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData(f"6Adding Tons of locations for filler",f"Level_End" ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData(f"7Adding Tons of locations for filler",f"Level_End" ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData(f"8Adding Tons of locations for filler",f"Level_End" ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData(f"9Adding Tons of locations for filler",f"Level_End" ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData(f"0Adding Tons of locations for filler",f"Level_End" ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData(f"Adding1 Tons of locations for filler",f"Level_End" ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData(f"Adding2 Tons of locations for filler",f"Level_End" ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData(f"Adding3 Tons of locations for filler",f"Level_End" ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData(f"Adding4 Tons of locations for filler",f"Level_End" ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData(f"Adding5 Tons of locations for filler",f"Level_End" ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData(f"Adding6 Tons of locations for filler",f"Level_End" ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData(f"Adding7 Tons of locations for filler",f"Level_End" ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData(f"Adding8 Tons of locations for filler",f"Level_End" ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData(f"Adding9 Tons of locations for filler",f"Level_End" ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData(f"Adding0 Tons of locations for filler",f"Level_End" ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData(f"Adding Tons1 of locations for filler",f"Level_End" ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData(f"Adding Tons2 of locations for filler",f"Level_End" ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData(f"Adding Tons3 of locations for filler",f"Level_End" ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData(f"Adding Tons4 of locations for filler",f"Level_End" ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData(f"Adding Tons5 of locations for filler",f"Level_End" ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData(f"Adding Tons6 of locations for filler",f"Level_End" ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData(f"Adding Tons7 of locations for filler",f"Level_End" ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData(f"Adding Tons8 of locations for filler",f"Level_End" ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData(f"Dan's Crypt: Cleared",f"Level_End" ,MedievilLocationCategory.LEVEL_END),    
    MedievilLocationData(f"The Graveyard Cleared",f"Level_End" ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData(f"Return to the Graveyard Cleared",f"Level_End" ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData(f"Cemetery Hill Cleared",f"Level_End" ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData(f"The Hilltop Mausoleum Cleared",f"Level_End" ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData(f"Scarecrow Fields Cleared",f"Level_End" ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData(f"Ant Caves Cleared",f"Level_End" ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData(f"The Crystal Caves Cleared",f"Level_End" ,MedievilLocationCategory.LEVEL_END),                    
    MedievilLocationData(f"The Lake Cleared",f"Level_End" ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData(f"Pumpkin Gorge Cleared",f"Level_End" ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData(f"Pumpkin Serpent Cleared",f"Level_End" ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData(f"Sleeping Village Cleared",f"Level_End" ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData(f"Pools of the Ancient Dead Cleared",f"Level_End" ,MedievilLocationCategory.LEVEL_END), 
    MedievilLocationData(f"Asylum Grounds Cleared",f"Level_End" ,MedievilLocationCategory.LEVEL_END),     
    MedievilLocationData(f"Inside the Asylum Cleared",f"Level_End" ,MedievilLocationCategory.LEVEL_END),     
    MedievilLocationData(f"Enchanted Earth Cleared",f"Level_End" ,MedievilLocationCategory.LEVEL_END),     
    MedievilLocationData(f"The Gallows Gauntlet (needs more info) Cleared",f"Level_End" ,MedievilLocationCategory.LEVEL_END),     
    MedievilLocationData(f"The Haunted Ruins Cleared",f"Level_End" ,MedievilLocationCategory.LEVEL_END),     
    MedievilLocationData(f"Ghost Ship Cleared",f"Level_End" ,MedievilLocationCategory.LEVEL_END),     
    MedievilLocationData(f"The Entrance Hall Cleared",f"Level_End" ,MedievilLocationCategory.LEVEL_END),     
    MedievilLocationData(f"The Time Device Cleared",f"Level_End" ,MedievilLocationCategory.LEVEL_END),     
    MedievilLocationData(f"Zaroks Lair Cleared",f"Level_End" ,MedievilLocationCategory.PROGRESSION),                      
]
}

location_dictionary: Dict[str, MedievilLocationData] = {}
for location_table in location_tables.values():
    location_dictionary.update({location_data.name: location_data for location_data in location_table})