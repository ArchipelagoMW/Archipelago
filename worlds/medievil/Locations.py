from enum import IntEnum
from typing import Optional, NamedTuple, Dict

from BaseClasses import Location, Region
from .Items import MedievilItem

class MedievilLocationCategory(IntEnum):
    FILLER = 0
    PROGRESSION = 1
    WEAPON = 2
    CHALICE = 3
    FUN = 4
    LEVEL_END = 5
    SKIP = 6

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
        
def make_locations_table():
    all_locations = []
    location_id = 1
    
    for level_location in list_of_level_locations:
        all_locations.append(MedievilLocationData(level_location[0],level_location[1],location_id, level_location[2])),
        location_id += 1
        
    return all_locations
    
list_of_level_locations = [
    # Hall Of Heroes
    ["Life Bottle: Hall of Heroes (Canny Tim)","Level_End",MedievilLocationCategory.FUN],
    ["Life Bottle: Hall of Heroes (Ravenhooves The Archer)","Level_End",MedievilLocationCategory.FUN],
    ["Life Bottle: Hall of Heroes (Dirk Steadfast)","Level_End",MedievilLocationCategory.FUN],
    ["Equipment: Broadsword from Woden the Mighty - HH","Level_End",MedievilLocationCategory.FUN],
    ["Equipment: Magic Sword from Dirk Steadfast - HH","Level_End",MedievilLocationCategory.FUN],
    ["Equipment: Hammer from Stanyer Iron Hewer - HH","Level_End",MedievilLocationCategory.FUN],
    ["Equipment: Axe from Bloodmonath- HH","Level_End",MedievilLocationCategory.FUN],
    ["Equipment: Crossbow from Canny Tim - HH","Level_End",MedievilLocationCategory.FUN],
    ["Equipment: Longbow from Ravenhooves The Archer - HH","Level_End",MedievilLocationCategory.FUN],
    ["Equipment: Fire Longbow from Ravenhooves the Archer - HH","Level_End",MedievilLocationCategory.FUN],
    ["Equipment: Magic Longbow from Ravenhooves the Archer - HH","Level_End",MedievilLocationCategory.FUN],
    ["Equipment: Spear from Imanzi Shongama - HH","Level_End",MedievilLocationCategory.FUN],
    ["Equipment: Lightning from Megwynne Stormbinder - HH","Level_End",MedievilLocationCategory.FUN],
    ["Equipment: Gold Shield from Karl Sturngard - HH","Level_End",MedievilLocationCategory.FUN], 
    ["Energy Vials: Imanzi Shongama 1 - HH","Level_End",MedievilLocationCategory.FUN],
    ["Energy Vials: Imanzi Shongama 2 - HH","Level_End",MedievilLocationCategory.FUN],
    ["Energy Vials: Megwynne Stormbinder 1 - HH","Level_End",MedievilLocationCategory.FUN],
    ["Energy Vials: Megwynne Stormbinder 2 - HH","Level_End",MedievilLocationCategory.FUN],
    ["Energy Vials: Megwynne Stormbinder 3 - HH","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Stanyer Iron Hewer 1- HH","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Stanyer Iron Hewer 2- HH","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Woden the Mighty 1- HH","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Woden the Mighty 2- HH","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Bloodmonath 1 - HH","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Bloodmonath 2 - HH","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Bloodmonath 3 - HH","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Karl Sturngard 1 - HH","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Karl Sturngard 2 - HH","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Karl Sturngard 3 - HH","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Karl Sturngard 4 - HH","Level_End",MedievilLocationCategory.FUN],

    # Dans Crypt
    ["Star Rune: Dan's Crypt","Level_End",MedievilLocationCategory.PROGRESSION],
    ["Equipment: Small Sword - DC","Level_End",MedievilLocationCategory.FUN],
    ["Equipment: Copper Shield in Chest - DC","Level_End",MedievilLocationCategory.FUN],
    ["Equipment: Daggers - DC","Level_End",MedievilLocationCategory.FUN],
    ["Life Bottle: Dan's Crypt","Level_End",MedievilLocationCategory.FUN],
    ["Life Bottle: Dan's Crypt - Behind Wall","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Over the water - DC","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Behind Wall in Crypt - Left - DC","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Behind Wall in Crypt - Right - DC","Level_End",MedievilLocationCategory.FUN],
    ["Cleared: Dan's Crypt","Level_End",MedievilLocationCategory.LEVEL_END],
    

    # The Graveyard
    ["Earth Rune: The Graveyard","Level_End",MedievilLocationCategory.PROGRESSION],
    ["Chaos Rune: The Graveyard","Level_End",MedievilLocationCategory.PROGRESSION],
    ["Equipment: Copper Shield - TG","Level_End",MedievilLocationCategory.FUN],
    ["Life Bottle: The Graveyard","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Near Chaos Rune - TG","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Life Potion Left Chest - TG","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Life Potion Right Chest - TG","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Shop Chest - TG","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Bag Near Hill Fountain - TG","Level_End",MedievilLocationCategory.FUN],
    ["Cleared: The Graveyard","Level_End",MedievilLocationCategory.LEVEL_END], 
    ["Chalice: The Graveyard","Chalice of Souls",MedievilLocationCategory.CHALICE],

    # Cemetery Hill
    ["Key Item: Witches Talisman - CH","Level_End",MedievilLocationCategory.PROGRESSION],
    ["Equipment: Copper Shield in CH 1 - CH","Level_End",MedievilLocationCategory.FUN],
    ["Equipment: Copper Shield in CH 2 - CH","Level_End",MedievilLocationCategory.FUN],
    ["Equipment: Copper Shield in CH 3 - CH","Level_End",MedievilLocationCategory.FUN],
    ["Equipment: Club - CH","Level_End",MedievilLocationCategory.FUN],
    ["Equipment: Copper Shield in Arena - CH","Level_End",MedievilLocationCategory.FUN],
    ["Energy Vial: Near Sh4op - CH","Level_End",MedievilLocationCategory.FUN],
    ["Energy Vial: Arena - CH","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Near Boulder Entrance - CH","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Up Hill 1 - CH","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Up Hill 2 - CH","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Chest at Exit - CH","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Chest in Arena - CH","Level_End",MedievilLocationCategory.FUN],
    ["Cleared: Cemetery Hill","Level_End",MedievilLocationCategory.LEVEL_END],
    ["Chalice: Cemetery Hill","Chalice of Souls",MedievilLocationCategory.CHALICE],
    
    # Hilltop Mausoleum
    # REQUIRES CLUB TO PROGRESS
    ["Key Item: Sheet Music - HM","Level_End",MedievilLocationCategory.PROGRESSION],
    ["Key Item: Skull Key - HM","Level_End",MedievilLocationCategory.PROGRESSION],
    ["Chaos Rune: The Hilltop Mausoleum","Level_End",MedievilLocationCategory.PROGRESSION],
    ["Earth Rune: The Hilltop Mausoleum","Level_End",MedievilLocationCategory.PROGRESSION],
    ["Moon Rune: The Hilltop Mausoleum","Level_End",MedievilLocationCategory.PROGRESSION],
    ["Equipment: Club near Broken Benches - HM","Level_End",MedievilLocationCategory.FUN],
    ["Equipment: Daggers near Block Puzzle - HM","Level_End",MedievilLocationCategory.FUN],
    ["Equipment: Copper Shield near Block Puzzle - HM","Level_End",MedievilLocationCategory.FUN],
    ["Energy Vial: Right Coffin - HM","Level_End",MedievilLocationCategory.FUN],
    ["Energy Vial: Near Rune - Left Ramp - HM","Level_End",MedievilLocationCategory.FUN],
    ["Energy Vial: Phantom of the Opera - Left - HM","Level_End",MedievilLocationCategory.FUN],
    ["Energy Vial: Phantom of the Opera - Right - HM","Level_End",MedievilLocationCategory.FUN],
    ["Energy Vial: Moon Room - HM","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Left Coffin - HM","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: After Earth Rune Door - HM","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Chest in Moon Room - HM","Level_End",MedievilLocationCategory.FUN],
    ["Gold Chest: Phantom of the Opera 1 - HM","Level_End",MedievilLocationCategory.FUN],
    ["Gold Chest: Phantom of the Opera 2 - HM","Level_End",MedievilLocationCategory.FUN],
    ["Gold Chest: Phantom of the Opera 3 - HM","Level_End",MedievilLocationCategory.FUN],
    ["Cleared: The Hilltop Mausoleum","Level_End",MedievilLocationCategory.LEVEL_END],
    ["Chalice: The Hilltop Mausoleum","Chalice of Souls",MedievilLocationCategory.CHALICE],
    
    # Return to the Graveyard
    # REQUIRES SKULL KEY TO PROGRESS
    ["Star Rune: Return to the Graveyard","Level_End",MedievilLocationCategory.PROGRESSION],
    ["Equipment: Silver Shield in Chest At Shop - RTG","Level_End",MedievilLocationCategory.FUN],
    ["Skill: Daring Dash","Level_End", MedievilLocationCategory.FUN],
    ["Energy Vial: Coffin Area West - RTG","Level_End",MedievilLocationCategory.FUN],
    ["Energy Vial: Coffin Area East - RTG","Level_End",MedievilLocationCategory.FUN],
    ["Energy Vial: Below Shop","Level_End - RTG",MedievilLocationCategory.FUN],
    ["Energy Vial: Undertakers Entrance - RTG","Level_End",MedievilLocationCategory.FUN],
    ["Energy Vial: Cliffs Right - RTG","Level_End",MedievilLocationCategory.FUN],
    ["Energy Vial: Cliffs Left - RTG","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Chest in Coffin Area 1 - RTG","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Chest in Coffin Area 2 - RTG","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Chest in Coffin Area 3 - RTG","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Chest in Coffin Area 4 - RTG","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Chest in Coffin Area 5 - RTG","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Bag above Coffin Area - RTG","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Bag after Bridge - RTG","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Bag at Shop - RTG","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Bag at Closed Gate - RTG","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Chest on Island - RTG","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Undertakers Entrance - RTG","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Cliffs Left - RTG","Level_End",MedievilLocationCategory.FUN],
    ["Cleared: Return to the Graveyard","Level_End",MedievilLocationCategory.LEVEL_END],
    ["Chalice: Return to the Graveyard","Chalice of Souls",MedievilLocationCategory.CHALICE],

    # Scarecrow Fields
    # Requires Harvester Parts for Chalice
    ["Chaos Rune: Scarecrow Fields","Level_End",MedievilLocationCategory.PROGRESSION],
    ["Earth Rune: Scarecrow Fields","Level_End",MedievilLocationCategory.PROGRESSION],
    ["Moon Rune: Scarecrow Fields","Level_End",MedievilLocationCategory.PROGRESSION],
    ["Key Item: Harvester Parts - SF","Level_End",MedievilLocationCategory.PROGRESSION],
    ["Equipment: Club Inside Hut - SF","Level_End",MedievilLocationCategory.FUN],
    ["Equipment: Silver Shield Behind Windmill - SF","Level_End",MedievilLocationCategory.FUN],
    ["Equipment: Copper Shield in Chest In the Barn - SF","Level_End",MedievilLocationCategory.FUN],
    ["Life Bottle: Scarecrow Fields","Level_End",MedievilLocationCategory.FUN],
    ["Energy Vial: Right of fire near Moon Door - SF","Level_End",MedievilLocationCategory.FUN],
    ["Energy Vial: Cornfield Path - SF","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Haystack at Beginning - SF","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Chest in Haystack near Moon Door - SF","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Left of fire near Moon Door - SF","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Bag in the Barn - SF","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Cornfield Square near Barn - SF","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Cornfield Path 1 - SF","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Chest Under Haybail - SF","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Bag under Barn Haybail - SF","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Bag in the Press - SF","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Bag in the Spinner - SF","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Chest next to Harvester Part - SF","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Chest Next to Chalice - SF","Level_End",MedievilLocationCategory.FUN],
    ["Cleared: Scarecrow Fields","Level_End",MedievilLocationCategory.LEVEL_END] ,
    ["Chalice: Scarecrow Fields","Chalice of Souls",MedievilLocationCategory.CHALICE],
        
    # The Anthill
    # Requres Witches Talisman
    ["Key Item: Amber Piece 1 - AH","Level_End",MedievilLocationCategory.PROGRESSION],
    ["Key Item: Amber Piece 2 - AH","Level_End",MedievilLocationCategory.PROGRESSION],
    ["Key Item: Amber Piece 3 - AH","Level_End",MedievilLocationCategory.PROGRESSION],
    ["Key Item: Amber Piece 4 - AH","Level_End",MedievilLocationCategory.PROGRESSION],
    ["Key Item: Amber Piece 5 - AH","Level_End",MedievilLocationCategory.PROGRESSION],
    ["Key Item: Amber Piece 6 - AH","Level_End",MedievilLocationCategory.PROGRESSION],
    ["Key Item: Amber Piece 7 - AH","Level_End",MedievilLocationCategory.PROGRESSION],
    ["Key Item: Amber Piece 8 - AH","Level_End",MedievilLocationCategory.PROGRESSION],
    ["Key Item: Amber Piece 9 - AH","Level_End",MedievilLocationCategory.PROGRESSION],
    ["Key Item: Amber Piece 10 - AH","Level_End",MedievilLocationCategory.PROGRESSION],
    ["Equipment: Club in Chest at Barrier - AH","Level_End",MedievilLocationCategory.FUN],
    ["Equipment: Chicken Drumsticks - AH","Level_End",MedievilLocationCategory.FUN],
    ["Energy Vial: Before Fairy 1 - AH","Level_End",MedievilLocationCategory.FUN],
    ["Energy Vial: After Amber 2 - AH","Level_End",MedievilLocationCategory.FUN],
    ["Energy Vial: Fairy 2 Room Center - AH","Level_End",MedievilLocationCategory.FUN],
    ["Energy Vial: Fairy 3 - AH","Level_End",MedievilLocationCategory.FUN],
    ["Energy Vial: Birthing room exit - AH","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Chest at Barrier Fairy - AH","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Maggot at Amber 2 - AH","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Maggot after Amber 2 - AH","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Fairy 2 Room Center - AH","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Fairy 2 Room Maggot - AH","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Maggots before Amber 4 - AH","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Maggots at Amber 5 - AH","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Maggots at Amber 7 - AH","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Maggot in nest at Amber 7 - AH","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Maggot in Nest - AH","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Maggot after Fairy 4 - AH","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Maggot after Fairy 4 in Nest - AH","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Maggot at Fairy 5 - AH","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Maggot near Amber 9 - AH","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Maggot near Shop - AH","Level_End",MedievilLocationCategory.FUN],
    ["Cleared: Ant Hill","Level_End",MedievilLocationCategory.LEVEL_END],
    ["Chalice: Ant Hill","Chalice of Souls",MedievilLocationCategory.CHALICE],
         
        
    # Enchanted Earth
    # Requires Shadow Talisman
    ["Key Item: Shadow Talisman - EE","Level_End",MedievilLocationCategory.PROGRESSION],
    ["Star Rune: Enchanted Earth","Level_End",MedievilLocationCategory.PROGRESSION],
    ["Earth Rune: Enchanted Earth","Level_End",MedievilLocationCategory.PROGRESSION],
    ["Equipment: Copper Shield in Egg - EE","Level_End",MedievilLocationCategory.FUN],
    ["Energy Vial: Shadow Talisman Cave - EE","Level_End",MedievilLocationCategory.FUN],
    ["Energy Vial: Left of Tree Drop - EE","Level_End",MedievilLocationCategory.FUN],
    ["Energy Vial: Right of Tree Drop - EE","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Bag Near Tree Hollow - EE","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Bag Behind Big Tree - EE","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Chest In Egg - EE","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Bag at Cave Entrance - EE","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins:Chest Near Barrier - EE","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Chest Left of Fountain - EE","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Chest Top of Fountain - EE","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Chest Right of Fountain - EE","Level_End",MedievilLocationCategory.FUN],
    ["Cleared: Enchanted Earth","Level_End",MedievilLocationCategory.LEVEL_END],
    ["Chalice: Enchanted Earth","Chalice of Souls",MedievilLocationCategory.CHALICE],

    # Sleeping Village
    ["Earth Rune: Sleeping Village","Level_End",MedievilLocationCategory.PROGRESSION],
    ["Chaos Rune: Sleeping Village","Level_End",MedievilLocationCategory.PROGRESSION],
    ["Key Item: Safe Key - SV","Level_End",MedievilLocationCategory.PROGRESSION],
    ["Key Item: Shadow Artefact - SV","Level_End",MedievilLocationCategory.PROGRESSION],
    ["Key Item: Crucifix - SV","Level_End",MedievilLocationCategory.PROGRESSION],
    ["Key Item: Landlords Bust - SV","Level_End",MedievilLocationCategory.PROGRESSION],
    ["Key Item: Crucifix Cast - SV","Level_End",MedievilLocationCategory.PROGRESSION],
    ["Equipment: Silver Shield in Blacksmiths - SV","Level_End",MedievilLocationCategory.FUN],
    ["Equipment: Club Chest under Inn Stairs - SV","Level_End",MedievilLocationCategory.FUN],
    ["Energy Vial: At Pond - SV","Level_End",MedievilLocationCategory.FUN],
    ["Energy Vial: Bust Switch - SV","Level_End",MedievilLocationCategory.FUN],
    ["Energy Vial: Near Exit - SV","Level_End",MedievilLocationCategory.FUN],
    ["Energy Vial: Near Chalice - SV","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Bag in Left Barrel at Blacksmith - SV","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Bag in Right Barrel at Blacksmith - SV","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Bag at Pond - SV","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Bag in Barrel at Inn - SV","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Bag in Barrel at bottom of Inn Stairs - SV","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Bag in Barrel Behind Inn Stairs - SV","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Bag In Top Bust Barrel - SV","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Bag In Switch Bust Barrel - SV","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Bag in Library - SV","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Bag at Top of table - SV","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Bag at Bottom of table - SV","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Chest next to Chalice - SV","Level_End",MedievilLocationCategory.FUN],
    ["Cleared: Sleeping Village","Level_End",MedievilLocationCategory.LEVEL_END],
    ["Chalice: Sleeping Village","Chalice of Souls",MedievilLocationCategory.CHALICE],

    # Pools of the Ancient Dead
    ["Life Bottle: Pools of the Ancient Dead","Level_End",MedievilLocationCategory.FUN],
    ["Chaos Rune: Pools of the Ancient Dead","Level_End",MedievilLocationCategory.PROGRESSION],
    ["Key Item: Soul Helmet 1 - PAD","Level_End",MedievilLocationCategory.PROGRESSION],
    ["Key Item: Soul Helmet 2 - PAD","Level_End",MedievilLocationCategory.PROGRESSION],
    ["Key Item: Soul Helmet 3 - PAD","Level_End",MedievilLocationCategory.PROGRESSION],
    ["Key Item: Soul Helmet 4 - PAD","Level_End",MedievilLocationCategory.PROGRESSION],
    ["Key Item: Soul Helmet 5 - PAD","Level_End",MedievilLocationCategory.PROGRESSION],
    ["Key Item: Soul Helmet 6 - PAD","Level_End",MedievilLocationCategory.PROGRESSION],
    ["Key Item: Soul Helmet 7 - PAD","Level_End",MedievilLocationCategory.PROGRESSION],
    ["Key Item: Soul Helmet 8 - PAD","Level_End",MedievilLocationCategory.PROGRESSION],
    ["Equipment: Silver Shield in Chest Near Soul 5 - PAD","Level_End",MedievilLocationCategory.FUN],
    ["Energy Vial: Broken Structure near Entrance - PAD","Level_End",MedievilLocationCategory.FUN],
    ["Energy Vial: Next to Lost Soul 3 - PAD","Level_End",MedievilLocationCategory.FUN],
    ["Energy Vial: Near Gate - PAD","Level_End",MedievilLocationCategory.FUN],
    ["Energy Vial: Chariot Right - PAD","Level_End",MedievilLocationCategory.FUN],
    ["Energy Vial: Chariot Left - PAD","Level_End",MedievilLocationCategory.FUN],
    ["Energy Vial: Jump Spot 1 - PAD","Level_End",MedievilLocationCategory.FUN],
    ["Energy Vial: Jump Spot 2 - PAD","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Bag at Entrance - PAD","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Bag on Island Near Soul 2 - PAD","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Jump Spot 1 - PAD","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Jump Spot 2 - PAD","Level_End", MedievilLocationCategory.FUN],
    ["Cleared: Pools of the Ancient Dead","Level_End",MedievilLocationCategory.LEVEL_END],
    ["Chalice: Pools of the Ancient Dead","Chalice of Souls",MedievilLocationCategory.CHALICE],
        
    # The Lake
    ["Chaos Rune: The Lake","Level_End",MedievilLocationCategory.PROGRESSION],
    ["Earth Rune: The Lake","Level_End",MedievilLocationCategory.PROGRESSION],
    ["Star Rune: The Lake","Level_End",MedievilLocationCategory.PROGRESSION],
    ["Time Rune: The Lake","Level_End",MedievilLocationCategory.PROGRESSION],
    ["Equipment: Silver Shield in TL In Whirlpool - TL","Level_End",MedievilLocationCategory.FUN],
    ["Energy Vial: Flooded House - TL","Level_End",MedievilLocationCategory.FUN],
    ["Energy Vial: Whirpool Wind 1 - TL","Level_End",MedievilLocationCategory.FUN],
    ["Energy Vial: Whirpool Wind 2 - TL","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Bag Outside Flooded House - TL","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Bag Near Closed Gate - TL","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Bag at the Whirlpool Entrance - TL","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Whirlpool Wind 1 - TL","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Whirlpool Wind 2 - TL","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Outside Whirlpool Exit - TL","Level_End",MedievilLocationCategory.FUN],
    ["Cleared: The Lake","Level_End",MedievilLocationCategory.LEVEL_END],
    ["Chalice: The Lake","Chalice of Souls",MedievilLocationCategory.CHALICE],
        
    # Crystal Caves
    ["Earth Rune: The Crystal Caves","Level_End",MedievilLocationCategory.PROGRESSION],
    ["Star Rune: The Crystal Caves","Level_End",MedievilLocationCategory.PROGRESSION],
    ["Equipment: Silver Shield in Crystal - CC","Level_End",MedievilLocationCategory.FUN],
    ["Equipment: Dragon Armour - CC","Level_End",MedievilLocationCategory.FUN],
    ["Energy Vial: Dragon Room 1st Platform - CC","Level_End",MedievilLocationCategory.FUN],
    ["Energy Vial: Dragon Room 3rd Platform - CC","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Chest in Crystal after Pool - CC","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Bag in Crystal at Start - CC","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Bag in Spinner - CC","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Bag near Silver Shield - CC","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Chest in Crystal After Earth Door - CC","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Bag in Dragon Room 1 1st Platform - CC","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Bag in Dragon Room 2 1st Platform - CC","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Chest in Dragon Room 1st Platform - CC","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Bag in Dragon Room 2nd Platform - CC","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Bag in Dragon Room 1 3rd Platform - CC","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Bag in Dragon Room 2 3rd Platform - CC","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Chest in Dragon Room 3rd Platform - CC","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Bag in Dragon Room 4th Platform 1 - CC","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Chest in Dragon Room 4th Platform - CC","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Bag in Dragon Room 4th Platform 2 - CC","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Bag on Left of Pool - CC","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Bag on Right of Pool - CC","Level_End",MedievilLocationCategory.FUN],
    ["Cleared: The Crystal Caves","Level_End",MedievilLocationCategory.LEVEL_END],
    ["Chalice: The Crystal Caves","Chalice of Souls",MedievilLocationCategory.CHALICE],
        
    # Gallows Gauntlet
    # Requires Dragon Armour
    ["Star Rune: The Gallows Gauntlet - GG","Level_End",MedievilLocationCategory.PROGRESSION],
    ["Equipment: Silver Shield in Chest Near Exit - GG","Level_End",MedievilLocationCategory.FUN],
    ["Energy Vial: Near Chalice - GG","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Bag Behind Stone Dragon 1 - GG","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Bag Behind Stone Dragon 2 - GG","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Chest at Serpent - GG","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Chest Near Star Entrance - GG","Level_End",MedievilLocationCategory.FUN],
    ["Cleared: The Gallows Gauntlet","Level_End",MedievilLocationCategory.LEVEL_END],
    ["Chalice: The Gallows Gauntlet","Chalice of Souls",MedievilLocationCategory.CHALICE],
        
    # Asylum Grounds
    ["Chaos Rune: Asylum Grounds - AG","Level_End",MedievilLocationCategory.PROGRESSION],
    ["Equipment: Silver Shield in Chest Behind Door - AG","Level_End",MedievilLocationCategory.FUN],
    ["Energy Vial: Near Bishop - AG","Level_End",MedievilLocationCategory.FUN],
    ["Energy Vial: Near King - AG","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Bag in Bell Grave Near Bell - AG","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Bag in Bell Grave Near Entrance - AG","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Bag Near Shooting Statue - AG","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Bag in Rat Grave - AG","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Behind Chaos Gate - AG","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Behind Elephant in Grave - AG","Level_End",MedievilLocationCategory.FUN],
    ["Cleared: Asylum Grounds","Level_End",MedievilLocationCategory.LEVEL_END],
    ["Chalice: Asylum Grounds","Chalice of Souls",MedievilLocationCategory.CHALICE],
         
    # Inside the Asylum
    ["Earth Rune: Inside the Asylum","Level_End",MedievilLocationCategory.PROGRESSION], 
    ["Key Item: Dragon Gem - IA","Level_End",MedievilLocationCategory.PROGRESSION], 
    ["Equipment: Silver Shield in Bat Room - IA","Level_End",MedievilLocationCategory.FUN], 
    ["Energy Vial: Bat Room - IA","Level_End",MedievilLocationCategory.FUN], 
    ["Energy Vial: Asylumn Room 1 - IA","Level_End",MedievilLocationCategory.FUN], 
    ["Energy Vial: Asylumn Room 2 - IA","Level_End",MedievilLocationCategory.FUN], 
    ["Gold Coins: Bag in Bat Room Left - IA","Level_End",MedievilLocationCategory.FUN], 
    ["Gold Coins: Chest in Bat Room - IA","Level_End",MedievilLocationCategory.FUN], 
    ["Gold Coins: Bag in Bat Room Centre - IA","Level_End",MedievilLocationCategory.FUN], 
    ["Gold Coins: Bag in Bat Room Right - IA","Level_End",MedievilLocationCategory.FUN], 
    ["Gold Coins: Bag in Asylumn Room - IA","Level_End",MedievilLocationCategory.FUN], 
    ["Gold Coins: Bag in Sewer Prison Entrance - IA","Level_End",MedievilLocationCategory.FUN], 
    ["Gold Coins: Bag on Sewer Prison Bench - IA","Level_End",MedievilLocationCategory.FUN], 
    ["Cleared: Inside the Asylum","Level_End",MedievilLocationCategory.LEVEL_END], 
    ["Chalice: Inside the Asylum","Chalice of Souls",MedievilLocationCategory.CHALICE], 
        
    # Pumpkin Gorge
    ["Time Rune: Pumpkin Gorge","Level_End",MedievilLocationCategory.PROGRESSION],
    ["Chaos Rune: Pumpkin Gorge","Level_End",MedievilLocationCategory.PROGRESSION],
    ["Earth Rune: Pumpkin Gorge","Level_End",MedievilLocationCategory.PROGRESSION],
    ["Moon Rune: Pumpkin Gorge","Level_End",MedievilLocationCategory.PROGRESSION],
    ["Equipment: Club in Chest in Tunnel - PG","Level_End",MedievilLocationCategory.FUN],
    ["Equipment: Silver Shield in Chest at Top of Hill - PG","Level_End",MedievilLocationCategory.FUN],
    ["Energy Vial: Vine Patch Left - PG","Level_End",MedievilLocationCategory.FUN],
    ["Energy Vial: Vine Patch Right - PG","Level_End",MedievilLocationCategory.FUN],
    ["Energy Vial: In Coop - PG","Level_End",MedievilLocationCategory.FUN],
    ["Energy Vial: In Moon Hut - PG","Level_End",MedievilLocationCategory.FUN],
    ["Energy Vial: Top of Hill - PG","Level_End",MedievilLocationCategory.FUN],
    ["Energy Vial: Boulders After Star Rune - PG","Level_End",MedievilLocationCategory.FUN],
    ["Energy Vial: Chalice Path - PG","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Bag Behind Rocks At Start - PG","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Chest in Coop 1 - PG","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Chest in Coop 2 - PG","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Chest in Coop 3 - PG","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Bag in Mushroom Area - PG","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Chest at Boulders after Star Rune - PG","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Chest Near Chalice - PG","Level_End",MedievilLocationCategory.FUN],
    ["Cleared: Pumpkin Gorge","Level_End",MedievilLocationCategory.LEVEL_END],
    ["Chalice: Pumpkin Gorge","Chalice of Souls",MedievilLocationCategory.CHALICE],
        
    # Pumpkin Servent
    ["Key Item: Dragon Gem - PS","Level_End",MedievilLocationCategory.PROGRESSION],     
    ["Equipment: Silver Shield in Chest near Leeches - PS","Level_End",MedievilLocationCategory.FUN],
    ["Energy Vial: Left at Merchant Gargoyle - PS","Level_End",MedievilLocationCategory.FUN],
    ["Energy Vial: Right at Merchant Gargoyle - PS","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Bag Behind House - PS","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Bag Behind Vines and Pod - PS","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Chest at Merchant Gargoyle - PS","Level_End",MedievilLocationCategory.FUN],
    ["Cleared: Pumpkin Serpent","Level_End",MedievilLocationCategory.LEVEL_END],
    ["Chalice: Pumpkin Serpent","Chalice of Souls",MedievilLocationCategory.CHALICE],
        
    # Haunted Ruins
    ["Key Item: King Peregrine's Crown - HR","Level_End",MedievilLocationCategory.PROGRESSION],
    ["Chaos Rune: The Haunted Ruins","Level_End",MedievilLocationCategory.PROGRESSION],
    ["Earth Rune: The Haunted Ruins","Level_End",MedievilLocationCategory.PROGRESSION],
    ["Equipment: Silver Shield in Chest Near Rune Door - HR","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Near First Set of farmers - HR","Level_End",MedievilLocationCategory.FUN],
    ["Energy Vial: Above Rune - HR","Level_End",MedievilLocationCategory.FUN],
    ["Energy Vial: Corner of Walls 1 - HR","Level_End",MedievilLocationCategory.FUN],
    ["Energy Vial: Corner of Walls 2 - HR","Level_End",MedievilLocationCategory.FUN],
    ["Energy Vial: Corner of Walls 3 - HR","Level_End",MedievilLocationCategory.FUN],
    ["Energy Vial: Up from Oil - HR","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Bag Near Chalice North - HR","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Bag Near Chalice South - HR","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Bag in Crown Room - HR","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Chest at Catapult 1 - HR","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Chest at Catapult 2 - HR","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Chest at Catapult 3 - HR","Level_End",MedievilLocationCategory.FUN],
    ["Cleared: The Haunted Ruins","Level_End",MedievilLocationCategory.LEVEL_END],
    ["Chalice: The Haunted Ruins","Chalice of Souls",MedievilLocationCategory.CHALICE],
    
    # Ghost Ship
    ["Moon Rune: Ghost Ship","Level_End",MedievilLocationCategory.PROGRESSION],
    ["Chaos Rune: Ghost Ship","Level_End",MedievilLocationCategory.PROGRESSION],
    ["Star Rune: Ghost Ship","Level_End",MedievilLocationCategory.PROGRESSION],
    ["Equipment: Silver Shield in Chest in Barrel Room - GS","Level_End",MedievilLocationCategory.FUN],
    ["Equipment: Club in Chest at Captain - GS","Level_End",MedievilLocationCategory.FUN],
    ["Energy Vial: In Cabin - GS","Level_End",MedievilLocationCategory.FUN],
    ["Energy Vial: In Cannon Room - GS","Level_End",MedievilLocationCategory.FUN],
    ["Energy Vial: Rope Bridge 1 - GS","Level_End",MedievilLocationCategory.FUN],
    ["Energy Vial: Rope Bridge 2 - GS","Level_End",MedievilLocationCategory.FUN],
    ["Energy Vial: Cage Lift 1 - GS","Level_End",MedievilLocationCategory.FUN],
    ["Energy Vial: Cage Lift 2 - GS","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Bag in Rolling Barrels Room - GS","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Bag on Deck At Barrels - GS","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Chest in Cannon Room - GS","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Rope Bridge - GS","Level_End",MedievilLocationCategory.FUN],
    ["Cleared: Ghost Ship","Level_End",MedievilLocationCategory.LEVEL_END],
    ["Chalice: Ghost Ship","Chalice of Souls",MedievilLocationCategory.CHALICE],

    # The Entrance Hall
    ["Cleared: The Entrance Hall","Level_End",MedievilLocationCategory.LEVEL_END],
    ["Chalice: The Entrance Hall","Chalice of Souls",MedievilLocationCategory.CHALICE], 
    
    # The Time Device
    ["Life Bottle: The Time Device","Level_End",MedievilLocationCategory.FUN],
    ["Chaos Rune: The Time Device","Level_End",MedievilLocationCategory.PROGRESSION],
    ["Earth Rune: The Time Device","Level_End",MedievilLocationCategory.PROGRESSION], 
    ["Moon Rune: The Time Device","Level_End",MedievilLocationCategory.PROGRESSION],
    ["Time Rune: The Time Device","Level_End",MedievilLocationCategory.PROGRESSION],
    ["Equipment: Silver Shield on Clock","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Laser Platform Right","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Laser Platform Left","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Lone Pillar 1","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Lone Pillar 2","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Lone Pillar 3","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Bag at Earth Station 1","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Bag at Earth Station 1","Level_End",MedievilLocationCategory.FUN],
    ["Gold Coins: Bag at Earth Station 1","Level_End",MedievilLocationCategory.FUN],
    ["Cleared: The Time Device","Level_End",MedievilLocationCategory.LEVEL_END],
    ["Chalice: The Time Device","Chalice of Souls",MedievilLocationCategory.CHALICE],   
        
    # Zaroks Lair    
    ["Equipment: Good Lightning in ZL","Level_End",MedievilLocationCategory.FUN],
    ["Equipment: Silver Shield in ZL Arena","Level_End",MedievilLocationCategory.FUN],
    ["Cleared: Zaroks Lair","Level_End",MedievilLocationCategory.PROGRESSION],
    
    # Books for Booksanity go here
    
    # Bosses go here
    
    # Monsters for Monstersanity also go here
]
        
# don't forget you need minimum number of locations to be the max of the progression items
# The MainWorld can probably be split out into seperate areas at a later date. But for now one big one is fine.
location_tables = {
    "MainWorld": make_locations_table()
}

location_dictionary: Dict[str, MedievilLocationData] = {}
for location_table in location_tables.values():
    location_dictionary.update({location_data.name: location_data for location_data in location_table})