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
    m_code: int
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
        base_id = 99251000
        return {location_data.name: (base_id + location_data.m_code) for location_data in location_tables["MainWorld"]}

    def place_locked_item(self, item: MedievilItem):
        self.item = item
        self.locked = True
        item.location = self
# don't forget you need minimum number of locations to be the max of the progression items
location_tables = {
"MainWorld": [
    MedievilLocationData("Dan's Crypt: Cleared","Level_End",1,MedievilLocationCategory.LEVEL_END), 
    MedievilLocationData("The Graveyard Cleared","Level_End",2,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData("Return to the Graveyard Cleared","Level_End",3,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData("Cemetery Hill Cleared","Level_End",4,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData("The Hilltop Mausoleum Cleared","Level_End",5,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData("Scarecrow Fields Cleared","Level_End",6,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData("Ant Hill Cleared","Level_End",7,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData("The Crystal Caves Cleared","Level_End",8,MedievilLocationCategory.LEVEL_END), 
    MedievilLocationData("The Lake Cleared","Level_End",9,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData("Pumpkin Gorge Cleared","Level_End",10,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData("Pumpkin Serpent Cleared","Level_End",11,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData("Sleeping Village Cleared","Level_End",12,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData("Pools of the Ancient Dead Cleared","Level_End",13,MedievilLocationCategory.LEVEL_END), 
    MedievilLocationData("Asylum Grounds Cleared","Level_End",14,MedievilLocationCategory.LEVEL_END), 
    MedievilLocationData("Inside the Asylum Cleared","Level_End",15,MedievilLocationCategory.LEVEL_END), 
    MedievilLocationData("Enchanted Earth Cleared","Level_End",16,MedievilLocationCategory.LEVEL_END), 
    MedievilLocationData("The Gallows Gauntlet Cleared","Level_End" ,17,MedievilLocationCategory.LEVEL_END), 
    MedievilLocationData("The Haunted Ruins Cleared","Level_End",18,MedievilLocationCategory.LEVEL_END), 
    MedievilLocationData("Ghost Ship Cleared","Level_End",19,MedievilLocationCategory.LEVEL_END), 
    MedievilLocationData("The Entrance Hall Cleared","Level_End",20,MedievilLocationCategory.LEVEL_END), 
    MedievilLocationData("The Time Device Cleared","Level_End",21,MedievilLocationCategory.LEVEL_END), 
    MedievilLocationData("Zaroks Lair Cleared","Level_End",22,MedievilLocationCategory.PROGRESSION), 
    MedievilLocationData("Adding Tons of locations for filler1","Level_End",23 ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData("Adding Tons of locations for filler2","Level_End",24 ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData("Adding Tons of locations for filler3","Level_End",25 ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData("Adding Tons of locations for filler4","Level_End",26,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData("Adding Tons of locations for filler5","Level_End",27 ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData("Adding Tons of locations for filler6","Level_End",28 ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData("Adding Tons of locations for filler7","Level_End",29 ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData("Adding Tons of locations for filler8","Level_End",30 ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData("Adding Tons of locations for filler9","Level_End",31 ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData("Adding Tons of locations for filler0","Level_End",32 ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData("1Adding Tons of locations for filler","Level_End",33 ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData("2Adding Tons of locations for filler","Level_End",34 ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData("3Adding Tons of locations for filler","Level_End",35 ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData("4Adding Tons of locations for filler","Level_End",36 ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData("5Adding Tons of locations for filler","Level_End",37 ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData("6Adding Tons of locations for filler","Level_End",38 ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData("7Adding Tons of locations for filler","Level_End",39 ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData("8Adding Tons of locations for filler","Level_End",40 ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData("9Adding Tons of locations for filler","Level_End",41 ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData("0Adding Tons of locations for filler","Level_End",42 ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData("Adding1 Tons of locations for filler","Level_End",43 ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData("Adding2 Tons of locations for filler","Level_End",44 ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData("Adding3 Tons of locations for filler","Level_End",45 ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData("Adding4 Tons of locations for filler","Level_End",46 ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData("Adding5 Tons of locations for filler","Level_End",47 ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData("Adding6 Tons of locations for filler","Level_End",48 ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData("Adding7 Tons of locations for filler","Level_End",49 ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData("Adding8 Tons of locations for filler","Level_End",50 ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData("Adding9 Tons of locations for filler","Level_End",51 ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData("Adding0 Tons of locations for filler","Level_End",52 ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData("Adding Tons1 of locations for filler","Level_End",53 ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData("Adding Tons2 of locations for filler","Level_End",54 ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData("Adding Tons3 of locations for filler","Level_End",55 ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData("Adding Tons4 of locations for filler","Level_End",56 ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData("Adding Tons5 of locations for filler","Level_End",57 ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData("Adding Tons6 of locations for filler","Level_End",58 ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData("Adding Tons7 of locations for filler","Level_End",59 ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData("Adding Tons8 of locations for filler","Level_End",60 ,MedievilLocationCategory.LEVEL_END),
]
}

location_dictionary: Dict[str, MedievilLocationData] = {}
for location_table in location_tables.values():
    location_dictionary.update({location_data.name: location_data for location_data in location_table})