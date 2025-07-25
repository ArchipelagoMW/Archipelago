from enum import IntEnum
from typing import Optional, NamedTuple, Dict

from BaseClasses import Location, Region
from .Items import MedievilItem

class MedievilLocationCategory(IntEnum):
    FILLER = 0
    PROGRESSION = 1
    WEAPON = 2
    CHALICE = 3
    RUNE = 4
    DYNAMIC_ITEM = 5
    KEY_ITEM = 6
    FUN = 7
    LEVEL_END = 8

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
        self.name = name

    @staticmethod
    def get_name_to_id() -> dict:
        base_id = 99250000
        region_offset = 1000        
        table_order = [
            "Map",
            "Hall of Heroes",
            "Dan's Crypt",
            "The Graveyard",
            "Cemetery Hill",
            "The Hilltop Mausoleum",
            "Return to the Graveyard",
            "Scarecrow Fields",
            "Ant Hill",
            "Enchanted Earth",
            "The Sleeping Village",
            "Pools of the Ancient Dead",
            "The Lake",
            "The Crystal Caves",
            "The Gallows Gauntlet",
            "Asylum Grounds",
            "Inside the Asylum",
            "Pumpkin Gorge",
            "Pumpkin Serpent",
            "The Haunted Ruins",
            "The Ghost Ship",
            "The Entrance Hall",
            "The Time Device",
            "Zaroks Lair"           
        ]

        output = {}
        for i, region_name in enumerate(table_order):
            current_region_base_id = base_id + (i * region_offset)
            # Ensure the region exists in location_tables
            if region_name in location_tables:
                # Enumerate the items within the current region, starting from current_region_base_id
                for j, location_data in enumerate(location_tables[region_name]):
                    # Assign an ID to each location within the region
                    # The ID for each location in a region will be current_region_base_id + j
                    # print(f"{current_region_base_id + j}: {location_data.name}")
                    output[location_data.name] = current_region_base_id + j

        return output
    
        # return {location_data.name: (base_id + location_data.m_code) for location_data in location_tables["MainWorld"]}

    def place_locked_item(self, item: MedievilItem):
        self.item = item
        self.locked = True
        item.location = self
    
# Gold shield ammo is used as a default. If you start picking up a lot, there's something wrong

location_tables = {
    "Map": [],
    "Hall of Heroes": [ # HALL OF HEROES DROP USE AN ARRAY SO FOR NOW I'M PUTTING THEM ON DYNAMIC
        MedievilLocationData("Life Bottle: Hall of Heroes (Canny Tim)","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
        MedievilLocationData("Life Bottle: Hall of Heroes (Ravenhooves The Archer)","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
        MedievilLocationData("Life Bottle: Hall of Heroes (Dirk Steadfast)","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
        MedievilLocationData("Equipment: Broadsword from Woden the Mighty - HH","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
        MedievilLocationData("Equipment: Magic Sword from Dirk Steadfast - HH","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
        MedievilLocationData("Equipment: Hammer from Stanyer Iron Hewer - HH","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
        MedievilLocationData("Equipment: Axe from Bloodmonath- HH","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
        MedievilLocationData("Equipment: Crossbow from Canny Tim - HH","Gold Shield Ammo (100)",MedievilLocationCategory.WEAPON),
        MedievilLocationData("Equipment: Longbow from Ravenhooves The Archer - HH","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
        MedievilLocationData("Equipment: Fire Longbow from Ravenhooves the Archer - HH","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
        MedievilLocationData("Equipment: Magic Longbow from Ravenhooves the Archer - HH","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
        MedievilLocationData("Equipment: Spear from Imanzi Shongama - HH","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
        MedievilLocationData("Equipment: Lightning from Megwynne Stormbinder - HH","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
        MedievilLocationData("Equipment: Gold Shield from Karl Sturngard - HH","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
        MedievilLocationData("Energy Vial: Imanzi Shongama 1 - HH","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
        MedievilLocationData("Energy Vial: Imanzi Shongama 2 - HH","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
        MedievilLocationData("Energy Vial: Megwynne Stormbinder 1 - HH","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
        MedievilLocationData("Energy Vial: Megwynne Stormbinder 2 - HH","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
        MedievilLocationData("Energy Vial: Megwynne Stormbinder 3 - HH","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
        MedievilLocationData("Gold Coins: Stanyer Iron Hewer 1 - HH","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
        MedievilLocationData("Gold Coins: Stanyer Iron Hewer 2 - HH","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
        MedievilLocationData("Gold Coins: Woden the Mighty 1 - HH","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
        MedievilLocationData("Gold Coins: Woden the Mighty 2 - HH","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
        MedievilLocationData("Gold Coins: Bloodmonath 1 - HH","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
        MedievilLocationData("Gold Coins: Bloodmonath 2 - HH","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
        MedievilLocationData("Gold Coins: Bloodmonath 3 - HH","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
        MedievilLocationData("Gold Coins: Karl Sturngard 1 - HH","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
        MedievilLocationData("Gold Coins: Karl Sturngard 2 - HH","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
        MedievilLocationData("Gold Coins: Karl Sturngard 3 - HH","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
        MedievilLocationData("Gold Coins: Karl Sturngard 4 - HH","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
    ],

    "Dan's Crypt": [
         MedievilLocationData("Star Rune: Dan's Crypt","Gold Shield Ammo (100)",MedievilLocationCategory.PROGRESSION),
         MedievilLocationData("Life Bottle: Dan's Crypt","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Life Bottle: Dan's Crypt - Behind Wall","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Equipment: Small Sword - DC","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Equipment: Copper Shield in Chest - DC","Gold Shield Ammo (100)",MedievilLocationCategory.WEAPON),
         MedievilLocationData("Equipment: Daggers - DC","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Over the water - DC","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Behind Wall in Crypt - Left - DC","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Behind Wall in Crypt - Right - DC","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Cleared: Dan's Crypt","Gold Shield Ammo (100)",MedievilLocationCategory.LEVEL_END),
    ],
    
    "The Graveyard": [
         MedievilLocationData("Life Bottle: The Graveyard","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Earth Rune: The Graveyard","Gold Shield Ammo (100)",MedievilLocationCategory.PROGRESSION),
         MedievilLocationData("Chaos Rune: The Graveyard","Gold Shield Ammo (100)",MedievilLocationCategory.PROGRESSION),
         MedievilLocationData("Equipment: Copper Shield - TG","Gold Shield Ammo (100)",MedievilLocationCategory.WEAPON),
         MedievilLocationData("Gold Coins: Bag at Start - TG","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Near Chaos Rune - TG","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Behind Fence at Statue - TG","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),         
         MedievilLocationData("Gold Coins: Life Bottle Left Chest - TG","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Life Bottle Right Chest - TG","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Shop Chest - TG","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Bag Near Hill Fountain - TG","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Cleared: The Graveyard","Gold Shield Ammo (100)",MedievilLocationCategory.LEVEL_END),
         MedievilLocationData("Chalice: The Graveyard","Chalice of Souls",MedievilLocationCategory.CHALICE),
    ],

    "Cemetery Hill": [
         MedievilLocationData("Key Item: Witches Talisman - CH","Gold Shield Ammo (100)",MedievilLocationCategory.PROGRESSION),
         MedievilLocationData("Equipment: Copper Shield 1 - CH","Gold Shield Ammo (100)",MedievilLocationCategory.WEAPON),
         MedievilLocationData("Equipment: Copper Shield 2 - CH","Gold Shield Ammo (100)",MedievilLocationCategory.WEAPON),
         MedievilLocationData("Equipment: Copper Shield 3 - CH","Gold Shield Ammo (100)",MedievilLocationCategory.WEAPON),
         MedievilLocationData("Equipment: Club - CH","Gold Shield Ammo (100)",MedievilLocationCategory.WEAPON),
         MedievilLocationData("Equipment: Copper Shield in Arena - CH","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Energy Vial: Near Shop - CH","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Energy Vial: Arena - CH","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Near Boulder Entrance - CH","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Up Hill 1 - CH","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Up Hill 2 - CH","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Chest at Exit - CH","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Chest in Arena - CH","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Cleared: Cemetery Hill","Gold Shield Ammo (100)",MedievilLocationCategory.LEVEL_END),
         MedievilLocationData("Chalice: Cemetery Hill","Chalice of Souls",MedievilLocationCategory.CHALICE),
    ],
    
    "The Hilltop Mausoleum": [
        # REQUIRES CLUB TO PROGRESS
         MedievilLocationData("Key Item: Sheet Music - HM","Gold Shield Ammo (100)",MedievilLocationCategory.PROGRESSION),
         MedievilLocationData("Key Item: Skull Key - HM","Gold Shield Ammo (100)",MedievilLocationCategory.PROGRESSION),
         MedievilLocationData("Chaos Rune: The Hilltop Mausoleum","Gold Shield Ammo (100)",MedievilLocationCategory.PROGRESSION),
         MedievilLocationData("Earth Rune: The Hilltop Mausoleum","Gold Shield Ammo (100)",MedievilLocationCategory.PROGRESSION),
         MedievilLocationData("Moon Rune: The Hilltop Mausoleum","Gold Shield Ammo (100)",MedievilLocationCategory.PROGRESSION),
         MedievilLocationData("Equipment: Club near Broken Benches - HM","Gold Shield Ammo (100)",MedievilLocationCategory.WEAPON),
         MedievilLocationData("Equipment: Daggers near Block Puzzle - HM","Gold Shield Ammo (100)",MedievilLocationCategory.WEAPON),
         MedievilLocationData("Equipment: Copper Shield near Block Puzzle - HM","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Energy Vial: Right Coffin - HM","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Energy Vial: Near Rune on Left Ramp - HM","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Energy Vial: Phantom of the Opera on Left - HM","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Energy Vial: Phantom of the Opera on Right - HM","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Energy Vial: Moon Room - HM","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Left Coffin - HM","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: After Earth Rune Door - HM","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Chest in Moon Room - HM","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Gold Chest at Phantom of the Opera 1 - HM","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Gold Chest at Phantom of the Opera 2 - HM","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Gold Chest at Phantom of the Opera 3 - HM","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Cleared: The Hilltop Mausoleum","Gold Shield Ammo (100)",MedievilLocationCategory.LEVEL_END),
         MedievilLocationData("Chalice: The Hilltop Mausoleum","Chalice of Souls",MedievilLocationCategory.CHALICE),
    ],
    
    "Return to the Graveyard": [
        # REQUIRES SKULL KEY TO PROGRESS
         MedievilLocationData("Star Rune: Return to the Graveyard","Gold Shield Ammo (100)",MedievilLocationCategory.PROGRESSION),
         MedievilLocationData("Equipment: Silver Shield in Chest at Shop - RTG","Gold Shield Ammo (100)",MedievilLocationCategory.WEAPON),
         MedievilLocationData("Skill: Daring Dash","Gold Shield Ammo (100)", MedievilLocationCategory.PROGRESSION),
         MedievilLocationData("Energy Vial: Coffin Area West - RTG","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Energy Vial: Coffin Area East - RTG","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Energy Vial: Below Shop - RTG","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Energy Vial: Undertakers Entrance - RTG","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Energy Vial: Cliffs Right - RTG","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Energy Vial: Cliffs Left - RTG","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Chest in Coffin Area 1 - RTG","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Chest in Coffin Area 2 - RTG","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Chest in Coffin Area 3 - RTG","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Chest in Coffin Area 4 - RTG","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Chest in Coffin Area 5 - RTG","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Bag above Coffin Area - RTG","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Bag after Bridge - RTG","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Bag at Shop - RTG","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Bag at Closed Gate - RTG","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Chest on Island - RTG","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Undertakers Entrance - RTG","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Cliffs Left - RTG","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Cleared: Return to the Graveyard","Gold Shield Ammo (100)",MedievilLocationCategory.LEVEL_END),
         MedievilLocationData("Chalice: Return to the Graveyard","Chalice of Souls",MedievilLocationCategory.CHALICE),
    ],

    "Scarecrow Fields": [
        # Requires Harvester Parts for Chalice
         MedievilLocationData("Life Bottle: Scarecrow Fields","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Key Item: Harvester Parts - SF","Gold Shield Ammo (100)",MedievilLocationCategory.PROGRESSION),
         MedievilLocationData("Chaos Rune: Scarecrow Fields","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
         MedievilLocationData("Earth Rune: Scarecrow Fields","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Moon Rune: Scarecrow Fields","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
         MedievilLocationData("Equipment: Club Inside Hut - SF","Gold Shield Ammo (100)",MedievilLocationCategory.WEAPON),
         MedievilLocationData("Equipment: Silver Shield Behind Windmill - SF","Gold Shield Ammo (100)",MedievilLocationCategory.WEAPON),
         MedievilLocationData("Equipment: Copper Shield in Chest In the Barn - SF","Gold Shield Ammo (100)",MedievilLocationCategory.WEAPON),
         MedievilLocationData("Energy Vial: Right of fire near Moon Door - SF","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Energy Vial: Cornfield Path - SF","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Haystack at Beginning - SF","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Chest in Haystack near Moon Door - SF","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Left of fire near Moon Door - SF","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Bag in the Barn - SF","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Cornfield Square near Barn - SF","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Cornfield Path 1 - SF","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Chest Under Haybail - SF","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
         MedievilLocationData("Gold Coins: Bag under Barn Haybail - SF","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
         MedievilLocationData("Gold Coins: Bag in the Press - SF","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Bag in the Spinner - SF","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Chest next to Harvester Part - SF","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Chest Next to Chalice - SF","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Cleared: Scarecrow Fields","Gold Shield Ammo (100)",MedievilLocationCategory.LEVEL_END),
         MedievilLocationData("Chalice: Scarecrow Fields","Chalice of Souls",MedievilLocationCategory.CHALICE),
    ],
        
    "Ant Hill": [
        # Requres Witches Talisman
         MedievilLocationData("Key Item: Amber Piece 1 - TA","Gold Shield Ammo (100)",MedievilLocationCategory.PROGRESSION),
         MedievilLocationData("Key Item: Amber Piece 2 - TA","Gold Shield Ammo (100)",MedievilLocationCategory.PROGRESSION),
         MedievilLocationData("Key Item: Amber Piece 3 - TA","Gold Shield Ammo (100)",MedievilLocationCategory.PROGRESSION),
         MedievilLocationData("Key Item: Amber Piece 4 - TA","Gold Shield Ammo (100)",MedievilLocationCategory.PROGRESSION),
         MedievilLocationData("Key Item: Amber Piece 5 - TA","Gold Shield Ammo (100)",MedievilLocationCategory.PROGRESSION),
         MedievilLocationData("Key Item: Amber Piece 6 - TA","Gold Shield Ammo (100)",MedievilLocationCategory.PROGRESSION),
         MedievilLocationData("Key Item: Amber Piece 7 - TA","Gold Shield Ammo (100)",MedievilLocationCategory.PROGRESSION),
         MedievilLocationData("Key Item: Amber Piece 8 - TA","Gold Shield Ammo (100)",MedievilLocationCategory.PROGRESSION),
         MedievilLocationData("Key Item: Amber Piece 9 - TA","Gold Shield Ammo (100)",MedievilLocationCategory.PROGRESSION),
         MedievilLocationData("Key Item: Amber Piece 10 - TA","Gold Shield Ammo (100)",MedievilLocationCategory.PROGRESSION),
         MedievilLocationData("Equipment: Club in Chest at Barrier - TA","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
         MedievilLocationData("Equipment: Chicken Drumsticks - TA","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Energy Vial: Before Fairy 1 - TA","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Energy Vial: After Amber 2 - TA","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Energy Vial: Fairy 2 Room Center - TA","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Energy Vial: Fairy 3 - TA","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Energy Vial: Birthing room exit - TA","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Chest at Barrier Fairy - TA","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Maggot at Amber 2 - TA","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
         MedievilLocationData("Gold Coins: Maggot after Amber 2 - TA","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
         MedievilLocationData("Gold Coins: Fairy 2 Room Center - TA","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Fairy 2 Room Maggot - TA","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
         MedievilLocationData("Gold Coins: Maggots before Amber 4 - TA","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
         MedievilLocationData("Gold Coins: Maggots at Amber 5 - TA","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
         MedievilLocationData("Gold Coins: Maggots at Amber 7 - TA","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
         MedievilLocationData("Gold Coins: Maggot in nest at Amber 7 - TA","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
         MedievilLocationData("Gold Coins: Maggot in Nest - TA","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
         MedievilLocationData("Gold Coins: Maggot after Fairy 4 - TA","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
         MedievilLocationData("Gold Coins: Maggot after Fairy 4 in Nest - TA","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
         MedievilLocationData("Gold Coins: Maggot at Fairy 5 - TA","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
         MedievilLocationData("Gold Coins: Maggot near Amber 9 - TA","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
         MedievilLocationData("Gold Coins: Maggot near Shop - TA","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
         MedievilLocationData("Cleared: Ant Hill","Gold Shield Ammo (100)",MedievilLocationCategory.LEVEL_END),
         MedievilLocationData("Chalice: Ant Hill","Chalice of Souls",MedievilLocationCategory.CHALICE),
    ],
         
        
    "Enchanted Earth": [
        # Requires Shadow Talisman
         MedievilLocationData("Key Item: Shadow Talisman - EE","Gold Shield Ammo (100)",MedievilLocationCategory.PROGRESSION),
         MedievilLocationData("Star Rune: Enchanted Earth","Gold Shield Ammo (100)",MedievilLocationCategory.PROGRESSION),
         MedievilLocationData("Earth Rune: Enchanted Earth","Gold Shield Ammo (100)",MedievilLocationCategory.PROGRESSION),
         MedievilLocationData("Equipment: Copper Shield in Egg - EE","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
         MedievilLocationData("Energy Vial: Shadow Talisman Cave - EE","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Energy Vial: Left of Tree Drop - EE","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Energy Vial: Right of Tree Drop - EE","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Bag Near Tree Hollow - EE","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Bag Behind Big Tree - EE","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Chest In Egg - EE","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
         MedievilLocationData("Gold Coins: Bag at Cave Entrance - EE","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Bag in Talisman Cave - EE","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Chest Near Barrier - EE","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Chest Left of Fountain - EE","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Chest Top of Fountain - EE","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Chest Right of Fountain - EE","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Cleared: Enchanted Earth","Gold Shield Ammo (100)",MedievilLocationCategory.LEVEL_END),
         MedievilLocationData("Chalice: Enchanted Earth","Chalice of Souls",MedievilLocationCategory.CHALICE),
    ],

    "The Sleeping Village": [
         MedievilLocationData("Earth Rune: Sleeping Village","Gold Shield Ammo (100)",MedievilLocationCategory.PROGRESSION),
         MedievilLocationData("Chaos Rune: Sleeping Village","Gold Shield Ammo (100)",MedievilLocationCategory.PROGRESSION),
         MedievilLocationData("Moon Rune: Sleeping Village","Gold Shield Ammo (100)",MedievilLocationCategory.PROGRESSION),
         MedievilLocationData("Key Item: Safe Key - SV","Gold Shield Ammo (100)",MedievilLocationCategory.PROGRESSION),
         MedievilLocationData("Key Item: Shadow Artefact - SV","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
         MedievilLocationData("Key Item: Crucifix - SV","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
         MedievilLocationData("Key Item: Landlords Bust - SV","Gold Shield Ammo (100)",MedievilLocationCategory.PROGRESSION),
         MedievilLocationData("Key Item: Crucifix Cast - SV","Gold Shield Ammo (100)",MedievilLocationCategory.PROGRESSION),
         MedievilLocationData("Equipment: Silver Shield in Blacksmiths - SV","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
         MedievilLocationData("Equipment: Club Chest under Inn Stairs - SV","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
         MedievilLocationData("Energy Vial: At Pond - SV","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Energy Vial: Bust Switch - SV","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Energy Vial: Near Exit - SV","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Energy Vial: Near Chalice - SV","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Bag in Left Barrel at Blacksmith - SV","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
         MedievilLocationData("Gold Coins: Bag in Right Barrel at Blacksmith - SV","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
         MedievilLocationData("Gold Coins: Bag at Pond - SV","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Bag in Barrel at Inn - SV","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
         MedievilLocationData("Gold Coins: Bag in Barrel at bottom of Inn Stairs - SV","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
         MedievilLocationData("Gold Coins: Bag in Barrel Behind Inn Stairs - SV","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
         MedievilLocationData("Gold Coins: Bag In Top Bust Barrel - SV","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
         MedievilLocationData("Gold Coins: Bag In Switch Bust Barrel - SV","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
         MedievilLocationData("Gold Coins: Bag in Library - SV","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Bag at Top of table - SV","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Bag at Bottom of table - SV","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Chest next to Chalice - SV","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Cleared: Sleeping Village","Gold Shield Ammo (100)",MedievilLocationCategory.LEVEL_END),
         MedievilLocationData("Chalice: Sleeping Village","Chalice of Souls",MedievilLocationCategory.CHALICE),
    ],

    "Pools of the Ancient Dead": [
         MedievilLocationData("Life Bottle: Pools of the Ancient Dead","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Chaos Rune: Pools of the Ancient Dead","Gold Shield Ammo (100)",MedievilLocationCategory.PROGRESSION),
         MedievilLocationData("Key Item: Soul Helmet 1 - PAD","Gold Shield Ammo (100)",MedievilLocationCategory.PROGRESSION),
         MedievilLocationData("Key Item: Soul Helmet 2 - PAD","Gold Shield Ammo (100)",MedievilLocationCategory.PROGRESSION),
         MedievilLocationData("Key Item: Soul Helmet 3 - PAD","Gold Shield Ammo (100)",MedievilLocationCategory.PROGRESSION),
         MedievilLocationData("Key Item: Soul Helmet 4 - PAD","Gold Shield Ammo (100)",MedievilLocationCategory.PROGRESSION),
         MedievilLocationData("Key Item: Soul Helmet 5 - PAD","Gold Shield Ammo (100)",MedievilLocationCategory.PROGRESSION),
         MedievilLocationData("Key Item: Soul Helmet 6 - PAD","Gold Shield Ammo (100)",MedievilLocationCategory.PROGRESSION),
         MedievilLocationData("Key Item: Soul Helmet 7 - PAD","Gold Shield Ammo (100)",MedievilLocationCategory.PROGRESSION),
         MedievilLocationData("Key Item: Soul Helmet 8 - PAD","Gold Shield Ammo (100)",MedievilLocationCategory.PROGRESSION),
         MedievilLocationData("Equipment: Silver Shield in Chest Near Soul 5 - PAD","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
         MedievilLocationData("Energy Vial: Broken Structure near Entrance - PAD","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Energy Vial: Next to Lost Soul 3 - PAD","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Energy Vial: Near Gate - PAD","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Energy Vial: Chariot Right - PAD","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Energy Vial: Chariot Left - PAD","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Energy Vial: Jump Spot 1 - PAD","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Energy Vial: Jump Spot 2 - PAD","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Bag at Entrance - PAD","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Bag on Island Near Soul 2 - PAD","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Jump Spot 1 - PAD","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Jump Spot 2 - PAD","Gold Shield Ammo (100)", MedievilLocationCategory.FUN),
         MedievilLocationData("Cleared: Pools of the Ancient Dead","Gold Shield Ammo (100)",MedievilLocationCategory.LEVEL_END),
         MedievilLocationData("Chalice: Pools of the Ancient Dead","Chalice of Souls",MedievilLocationCategory.CHALICE),
    ],
        
    "The Lake": [
         MedievilLocationData("Chaos Rune: The Lake","Gold Shield Ammo (100)",MedievilLocationCategory.PROGRESSION),
         MedievilLocationData("Earth Rune: The Lake","Gold Shield Ammo (100)",MedievilLocationCategory.PROGRESSION),
         MedievilLocationData("Star Rune: The Lake","Gold Shield Ammo (100)",MedievilLocationCategory.PROGRESSION),
         MedievilLocationData("Time Rune: The Lake","Gold Shield Ammo (100)",MedievilLocationCategory.PROGRESSION),
         MedievilLocationData("Equipment: Silver Shield In Whirlpool - TL","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
         MedievilLocationData("Energy Vial: Flooded House - TL","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Energy Vial: Whirpool Wind 1 - TL","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Energy Vial: Whirpool Wind 2 - TL","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Bag Outside Flooded House - TL","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Bag Near Closed Gate - TL","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Bag at the Whirlpool Entrance - TL","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Whirlpool Wind 1 - TL","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Whirlpool Wind 2 - TL","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Outside Whirlpool Exit - TL","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Cleared: The Lake","Gold Shield Ammo (100)",MedievilLocationCategory.LEVEL_END),
         MedievilLocationData("Chalice: The Lake","Chalice of Souls",MedievilLocationCategory.CHALICE),
    ],
        
    "The Crystal Caves": [
         MedievilLocationData("Earth Rune: The Crystal Caves","Gold Shield Ammo (100)",MedievilLocationCategory.PROGRESSION),
         MedievilLocationData("Star Rune: The Crystal Caves","Gold Shield Ammo (100)",MedievilLocationCategory.PROGRESSION),
         MedievilLocationData("Equipment: Silver Shield in Crystal - CC","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
         MedievilLocationData("Equipment: Dragon Armour - CC","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Energy Vial: Dragon Room 1st Platform - CC","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Energy Vial: Dragon Room 3rd Platform - CC","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Bag at bottom of winding staircase - CC", "Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Chest in Crystal after Pool - CC","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
         MedievilLocationData("Gold Coins: Bag in Crystal at Start - CC","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
         MedievilLocationData("Gold Coins: Bag in Spinner - CC","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Bag near Silver Shield - CC","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Chest in Crystal After Earth Door - CC","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
         MedievilLocationData("Gold Coins: Bag in Dragon Room 1 1st Platform - CC","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Bag in Dragon Room 2 1st Platform - CC","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Chest in Dragon Room 1st Platform - CC","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Bag in Dragon Room 2nd Platform - CC","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Bag in Dragon Room 1 3rd Platform - CC","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Bag in Dragon Room 2 3rd Platform - CC","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Chest in Dragon Room 3rd Platform - CC","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Bag in Dragon Room 4th Platform 1 - CC","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Chest in Dragon Room 4th Platform - CC","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Bag in Dragon Room 4th Platform 2 - CC","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Bag on Left of Pool - CC","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Bag on Right of Pool - CC","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Cleared: The Crystal Caves","Gold Shield Ammo (100)",MedievilLocationCategory.LEVEL_END),
         MedievilLocationData("Chalice: The Crystal Caves","Chalice of Souls",MedievilLocationCategory.CHALICE),
    ],
        
    "The Gallows Gauntlet": [
        # Requires Dragon Armour
         MedievilLocationData("Star Rune: The Gallows Gauntlet","Gold Shield Ammo (100)",MedievilLocationCategory.PROGRESSION),
         MedievilLocationData("Equipment: Silver Shield in Chest Near Exit - GG","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
         MedievilLocationData("Energy Vial: Near Chalice - GG","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Bag Behind Stone Dragon 1 - GG","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Bag Behind Stone Dragon 2 - GG","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Chest at Serpent - GG","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Chest Near Star Entrance - GG","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Cleared: The Gallows Gauntlet","Gold Shield Ammo (100)",MedievilLocationCategory.LEVEL_END),
         MedievilLocationData("Chalice: The Gallows Gauntlet","Chalice of Souls",MedievilLocationCategory.CHALICE),
    ],
        
    "Asylum Grounds": [
         MedievilLocationData("Chaos Rune: Asylum Grounds","Gold Shield Ammo (100)",MedievilLocationCategory.PROGRESSION),
         MedievilLocationData("Equipment: Silver Shield in Chest Behind Door - AG","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
         MedievilLocationData("Energy Vial: Near Bishop - AG","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Energy Vial: Near King - AG","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Bag in Bell Grave Near Bell - AG","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Bag in Bell Grave Near Entrance - AG","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Bag Near Shooting Statue - AG","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Bag in Rat Grave - AG","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Behind Chaos Gate - AG","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Behind Elephant in Grave - AG","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Cleared: Asylum Grounds","Gold Shield Ammo (100)",MedievilLocationCategory.LEVEL_END),
         MedievilLocationData("Chalice: Asylum Grounds","Chalice of Souls",MedievilLocationCategory.CHALICE),
    ],
         
    "Inside the Asylum": [
         MedievilLocationData("Earth Rune: Inside the Asylum","Gold Shield Ammo (100)",MedievilLocationCategory.PROGRESSION),
         MedievilLocationData("Key Item: Dragon Gem - IA","Gold Shield Ammo (100)",MedievilLocationCategory.PROGRESSION),
         MedievilLocationData("Equipment: Silver Shield in Bat Room - IA","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
         MedievilLocationData("Energy Vial: Bat Room - IA","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
         MedievilLocationData("Energy Vial: Asylumn Room 1 - IA","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
         MedievilLocationData("Energy Vial: Asylumn Room 2 - IA","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
         MedievilLocationData("Gold Coins: Bag in Bat Room Left - IA","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
         MedievilLocationData("Gold Coins: Chest in Bat Room - IA","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
         MedievilLocationData("Gold Coins: Bag in Bat Room Centre - IA","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
         MedievilLocationData("Gold Coins: Bag in Bat Room Right - IA","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
         MedievilLocationData("Gold Coins: Bag in Asylumn Room - IA","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
         MedievilLocationData("Gold Coins: Bag in Sewer Prison Entrance - IA","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Bag on Sewer Prison Bench - IA","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Cleared: Inside the Asylum","Gold Shield Ammo (100)",MedievilLocationCategory.LEVEL_END),
         MedievilLocationData("Chalice: Inside the Asylum","Chalice of Souls",MedievilLocationCategory.CHALICE),
    ],
        
    "Pumpkin Gorge": [
         MedievilLocationData("Time Rune: Pumpkin Gorge","Gold Shield Ammo (100)",MedievilLocationCategory.PROGRESSION), # this ones a bit wierd
         MedievilLocationData("Chaos Rune: Pumpkin Gorge","Gold Shield Ammo (100)",MedievilLocationCategory.PROGRESSION),
         MedievilLocationData("Earth Rune: Pumpkin Gorge","Gold Shield Ammo (100)",MedievilLocationCategory.PROGRESSION),
         MedievilLocationData("Moon Rune: Pumpkin Gorge","Gold Shield Ammo (100)",MedievilLocationCategory.PROGRESSION),
         MedievilLocationData("Equipment: Club in Chest in Tunnel - PG","Gold Shield Ammo (100)",MedievilLocationCategory.WEAPON),
         MedievilLocationData("Equipment: Silver Shield in Chest at Top of Hill - PG","Gold Shield Ammo (100)",MedievilLocationCategory.WEAPON),
         MedievilLocationData("Energy Vial: Vine Patch Left - PG","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Energy Vial: Vine Patch Right - PG","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Energy Vial: In Coop - PG","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Energy Vial: In Moon Hut - PG","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Energy Vial: Top of Hill - PG","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Energy Vial: Boulders After Star Rune - PG","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Energy Vial: Chalice Path - PG","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Bag Behind Rocks At Start - PG","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Chest in Coop 1 - PG","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Chest in Coop 2 - PG","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Chest in Coop 3 - PG","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Bag in Mushroom Area - PG","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Chest at Boulders after Star Rune - PG","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Chest Near Chalice - PG","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Cleared: Pumpkin Gorge","Gold Shield Ammo (100)",MedievilLocationCategory.LEVEL_END),
         MedievilLocationData("Chalice: Pumpkin Gorge","Chalice of Souls",MedievilLocationCategory.CHALICE),
    ],
        
    "Pumpkin Serpent": [
         MedievilLocationData("Key Item: Dragon Gem - PS","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
         MedievilLocationData("Equipment: Silver Shield in Chest near Leeches - PS","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
         MedievilLocationData("Energy Vial: Left at Merchant Gargoyle - PS","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Energy Vial: Right at Merchant Gargoyle - PS","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Bag Behind House - PS","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Bag Behind Vines and Pod - PS","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Chest at Merchant Gargoyle - PS","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Cleared: Pumpkin Serpent","Gold Shield Ammo (100)",MedievilLocationCategory.LEVEL_END),
         MedievilLocationData("Chalice: Pumpkin Serpent","Chalice of Souls",MedievilLocationCategory.CHALICE),
    ],
        
    "The Haunted Ruins": [
         MedievilLocationData("Key Item: King Peregrine's Crown - HR","Gold Shield Ammo (100)",MedievilLocationCategory.PROGRESSION),
         MedievilLocationData("Chaos Rune: The Haunted Ruins","Gold Shield Ammo (100)",MedievilLocationCategory.PROGRESSION),
         MedievilLocationData("Earth Rune: The Haunted Ruins","Gold Shield Ammo (100)",MedievilLocationCategory.PROGRESSION),
         MedievilLocationData("Equipment: Silver Shield in Chest Near Rune Door - HR","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
         MedievilLocationData("Energy Vial: Above Rune - HR","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Energy Vial: Corner of Walls 1 - HR","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Energy Vial: Corner of Walls 2 - HR","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Energy Vial: Corner of Walls 3 - HR","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Energy Vial: Up from Oil - HR","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Near First Set of farmers - HR","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Bag Near Chalice North - HR","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Bag Near Chalice South - HR","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Bag in Crown Room - HR","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Chest at Catapult 1 - HR","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Chest at Catapult 2 - HR","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Chest at Catapult 3 - HR","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Cleared: The Haunted Ruins","Gold Shield Ammo (100)",MedievilLocationCategory.LEVEL_END),
         MedievilLocationData("Chalice: The Haunted Ruins","Chalice of Souls",MedievilLocationCategory.CHALICE),
    ],
    
    "The Ghost Ship": [
         MedievilLocationData("Moon Rune: Ghost Ship","Gold Shield Ammo (100)",MedievilLocationCategory.PROGRESSION),
         MedievilLocationData("Chaos Rune: Ghost Ship","Gold Shield Ammo (100)",MedievilLocationCategory.PROGRESSION),
         MedievilLocationData("Star Rune: Ghost Ship","Gold Shield Ammo (100)",MedievilLocationCategory.PROGRESSION),
         MedievilLocationData("Equipment: Silver Shield in Chest in Barrel Room - GS","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
         MedievilLocationData("Equipment: Club in Chest at Captain - GS","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
         MedievilLocationData("Energy Vial: In Cabin - GS","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Energy Vial: In Cannon Room - GS","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Energy Vial: Rope Bridge 1 - GS","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Energy Vial: Rope Bridge 2 - GS","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Energy Vial: Cage Lift 1 - GS","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Energy Vial: Cage Lift 2 - GS","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Bag in Rolling Barrels Room - GS","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Bag on Deck At Barrels - GS","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Chest in Cannon Room - GS","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Rope Bridge - GS","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Cleared: Ghost Ship","Gold Shield Ammo (100)",MedievilLocationCategory.LEVEL_END),
         MedievilLocationData("Chalice: Ghost Ship","Chalice of Souls",MedievilLocationCategory.CHALICE),
    ],

    "The Entrance Hall":[
         MedievilLocationData("Cleared: The Entrance Hall","Gold Shield Ammo (100)",MedievilLocationCategory.LEVEL_END),
         MedievilLocationData("Chalice: The Entrance Hall","Chalice of Souls",MedievilLocationCategory.CHALICE),
    ],
    
    "The Time Device": [
         MedievilLocationData("Life Bottle: The Time Device","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Chaos Rune: The Time Device","Gold Shield Ammo (100)",MedievilLocationCategory.PROGRESSION),
         MedievilLocationData("Earth Rune: The Time Device","Gold Shield Ammo (100)",MedievilLocationCategory.PROGRESSION),
         MedievilLocationData("Moon Rune: The Time Device","Gold Shield Ammo (100)",MedievilLocationCategory.PROGRESSION),
         MedievilLocationData("Time Rune: The Time Device","Gold Shield Ammo (100)",MedievilLocationCategory.PROGRESSION),
         MedievilLocationData("Equipment: Silver Shield on Clock - TD","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
         MedievilLocationData("Gold Coins: Laser Platform Right - TD","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Laser Platform Left - TD","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Lone Pillar 1 - TD","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Lone Pillar 2 - TD","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Lone Pillar 3 - TD","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Bag at Earth Station 1 - TD","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Bag at Earth Station 2 - TD","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Gold Coins: Bag at Earth Station 3 - TD","Gold Shield Ammo (100)",MedievilLocationCategory.FUN),
         MedievilLocationData("Cleared: The Time Device","Gold Shield Ammo (100)",MedievilLocationCategory.LEVEL_END),
         MedievilLocationData("Chalice: The Time Device","Chalice of Souls",MedievilLocationCategory.CHALICE),
    ],
        
    "Zaroks Lair": [
         MedievilLocationData("Equipment: Good Lightning - ZL","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
         MedievilLocationData("Equipment: Silver Shield - ZL Arena","Gold Shield Ammo (100)",MedievilLocationCategory.DYNAMIC_ITEM),
         MedievilLocationData("Cleared: Zaroks Lair","Gold Shield Ammo (100)",MedievilLocationCategory.PROGRESSION),
    ]
    
    # Books for Booksanity go here
    
    # Bosses go here
    
    # Monsters for Monstersanity (if i hate myself) also go here
}

location_dictionary: Dict[str, MedievilLocationData] = {}
for location_table in location_tables.values():
    location_dictionary.update({location_data.name: location_data for location_data in location_table})