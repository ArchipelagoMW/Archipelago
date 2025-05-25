from typing import List, Dict, Any
import random

from BaseClasses import Region, Tutorial
from worlds.AutoWorld import WebWorld, World
from .Items import SohItem, item_data_table, item_table
from .Locations import SohLocation, base_location_table, cows_location_table,\
                                          location_table
from .Options import SohOptions
from .Regions import region_data_table
from .Rules import get_soh_rule


class SohWebWorld(WebWorld):
    theme = "ice"
    
    setup_en = Tutorial(
        tutorial_name="Start Guide",
        description="A guide to playing Ship of Harkinian.",
        language="English",
        file_name="guide_en.md",
        link="guide/en",
        authors=["aMannus"]
    )
    
    tutorials = [setup_en]
    game_info_languages = ["en"]


class SohWorld(World):
    """A PC Port of Ocarina of Time"""

    game = "Ship of Harkinian"
    web = SohWebWorld()
    options: SohOptions
    options_dataclass = SohOptions
    location_name_to_id = location_table
    item_name_to_id = item_table

    def create_item(self, name: str) -> SohItem:
        return SohItem(name, item_data_table[name].type, item_data_table[name].code, self.player)

    def create_items(self) -> None:
        item_pool: List[SohItem] = []

        location_count: int = 0
        # Count Total Locations.
        for location_name, location_data in location_table.items():
            location_count += 1

        # Filler item list
        filler_items = ["Recovery Heart", "Blue Rupee", "Red Rupee", "Purple Rupee", "Huge Rupee", "Bombs (5)", "Bombs (10)", "Arrows (5)", "Arrows (10)", "Deku Nuts (5)", "Deku Nuts (10)", "Deku Stick (1)"]

        # Add Base Progression Items
        item_pool.append(self.create_item("Kokiri Sword"))
        item_pool.append(self.create_item("Biggoron's Sword"))
        item_pool.append(self.create_item("Deku Shield"))
        item_pool.append(self.create_item("Hylian Shield"))
        item_pool.append(self.create_item("Mirror Shield"))
        item_pool.append(self.create_item("Goron Tunic"))
        item_pool.append(self.create_item("Zora Tunic"))
        item_pool.append(self.create_item("Iron Boots"))
        item_pool.append(self.create_item("Hover Boots"))
        item_pool.append(self.create_item("Boomerang"))
        item_pool.append(self.create_item("Lens of Truth"))
        item_pool.append(self.create_item("Megaton Hammer"))
        item_pool.append(self.create_item("Stone of Agony"))
        item_pool.append(self.create_item("Din's Fire"))
        item_pool.append(self.create_item("Farore's Wind"))
        item_pool.append(self.create_item("Nayru's Love"))
        item_pool.append(self.create_item("Fire Arrow"))
        item_pool.append(self.create_item("Ice Arrow"))
        item_pool.append(self.create_item("Light Arrow"))
        item_pool.append(self.create_item("Gerudo Membership Card"))
        item_pool.append(self.create_item("Double Defense"))
        item_pool.append(self.create_item("Claim Check"))
        for i in range(100): item_pool.append(self.create_item("Gold Skulltula Token"))
        for i in range(2): item_pool.append(self.create_item("Progressive Hookshot"))
        for i in range(3): item_pool.append(self.create_item("Strength Upgrade"))
        for i in range(3): item_pool.append(self.create_item("Progressive Bomb Bag"))
        for i in range(3): item_pool.append(self.create_item("Progressive Bow"))
        for i in range(3): item_pool.append(self.create_item("Progressive Slingshot"))
        for i in range(3): item_pool.append(self.create_item("Progressive Wallet"))
        for i in range(2): item_pool.append(self.create_item("Progressive Scale"))
        for i in range(2): item_pool.append(self.create_item("Progressive Nut Capacity"))
        for i in range(2): item_pool.append(self.create_item("Progressive Stick Capacity"))
        for i in range(6): item_pool.append(self.create_item("Progressive Bombchu"))
        for i in range(2): item_pool.append(self.create_item("Progressive Magic Meter"))
        for i in range(2): item_pool.append(self.create_item("Progressive Ocarina"))
        item_pool.append(self.create_item("Empty Bottle"))
        item_pool.append(self.create_item("Bottle with Ruto's Letter"))
        item_pool.append(self.create_item("Bottle with Big Poe"))
        item_pool.append(self.create_item("Bottle with Bugs"))
        item_pool.append(self.create_item("Zelda's Lullaby"))
        item_pool.append(self.create_item("Epona's Song"))
        item_pool.append(self.create_item("Saria's Song"))
        item_pool.append(self.create_item("Sun's Song"))
        item_pool.append(self.create_item("Song of Time"))
        item_pool.append(self.create_item("Song of Storms"))
        item_pool.append(self.create_item("Minuet of Forest"))
        item_pool.append(self.create_item("Bolero of Fire"))
        item_pool.append(self.create_item("Serenade of Water"))
        item_pool.append(self.create_item("Requiem of Spirit"))
        item_pool.append(self.create_item("Nocturne of Shadow"))
        item_pool.append(self.create_item("Prelude of Light"))
        item_pool.append(self.create_item("Great Deku Tree Map"))
        item_pool.append(self.create_item("Dodongo's Cavern Map"))
        item_pool.append(self.create_item("Jabu-Jabu's Belly Map"))
        item_pool.append(self.create_item("Forest Temple Map"))
        item_pool.append(self.create_item("Fire Temple Map"))
        item_pool.append(self.create_item("Water Temple Map"))
        item_pool.append(self.create_item("Spirit Temple Map"))
        item_pool.append(self.create_item("Shadow Temple Map"))
        item_pool.append(self.create_item("Bottom of the Well Map"))
        item_pool.append(self.create_item("Ice Cavern Map"))
        item_pool.append(self.create_item("Great Deku Tree Compass"))
        item_pool.append(self.create_item("Dodongo's Cavern Compass"))
        item_pool.append(self.create_item("Jabu-Jabu's Belly Compass"))
        item_pool.append(self.create_item("Forest Temple Compass"))
        item_pool.append(self.create_item("Fire Temple Compass"))
        item_pool.append(self.create_item("Water Temple Compass"))
        item_pool.append(self.create_item("Spirit Temple Compass"))
        item_pool.append(self.create_item("Shadow Temple Compass"))
        item_pool.append(self.create_item("Bottom of the Well Compass"))
        item_pool.append(self.create_item("Ice Cavern Compass"))
        item_pool.append(self.create_item("Forest Temple Boss Key"))
        item_pool.append(self.create_item("Fire Temple Boss Key"))
        item_pool.append(self.create_item("Water Temple Boss Key"))
        item_pool.append(self.create_item("Spirit Temple Boss Key"))
        item_pool.append(self.create_item("Shadow Temple Boss Key"))
        item_pool.append(self.create_item("Ganon's Castle Boss Key"))
        for i in range(5): item_pool.append(self.create_item("Forest Temple Small Key"))
        for i in range(8): item_pool.append(self.create_item("Fire Temple Small Key"))
        for i in range(6): item_pool.append(self.create_item("Water Temple Small Key"))
        for i in range(5): item_pool.append(self.create_item("Spirit Temple Small Key"))
        for i in range(5): item_pool.append(self.create_item("Shadow Temple Small Key"))
        for i in range(3): item_pool.append(self.create_item("Bottom of the Well Small Key"))
        for i in range(9): item_pool.append(self.create_item("Training Ground Small Key"))
        for i in range(2): item_pool.append(self.create_item("Ganon's Castle Small Key"))
        item_pool.append(self.create_item("Kokiri's Emerald"))
        item_pool.append(self.create_item("Goron's Ruby"))
        item_pool.append(self.create_item("Zora's Sapphire"))
        item_pool.append(self.create_item("Forest Medallion"))
        item_pool.append(self.create_item("Fire Medallion"))
        item_pool.append(self.create_item("Water Medallion"))
        item_pool.append(self.create_item("Spirit Medallion"))
        item_pool.append(self.create_item("Shadow Medallion"))
        item_pool.append(self.create_item("Light Medallion"))
        item_pool.append(self.create_item("Greg the Green Rupee"))
        for i in range(35): item_pool.append(self.create_item("Piece of Heart"))
        item_pool.append(self.create_item("Piece of Heart (WINNER)"))
        for i in range(8): item_pool.append(self.create_item("Heart Container"))
        for i in range(6): item_pool.append(self.create_item("Ice Trap"))

        filler_item_count: int = location_count - len(item_pool)
        item_pool += [self.create_item(filler_items[random.randint(0, 11)]) for _ in range(filler_item_count)]

        self.multiworld.itempool += item_pool

    def create_regions(self) -> None:
        # Create regions.
        for region_name in region_data_table.keys():
            region = Region(region_name, self.player, self.multiworld)
            self.multiworld.regions.append(region)

        # Create locations.
        for region_name, region_data in region_data_table.items():
            region = self.multiworld.get_region(region_name, self.player)
            region.add_locations({
                location_name: location_data.address for location_name, location_data in base_location_table.items()
                if location_data.region == region_name
            }, SohLocation)

            if self.options.shuffle_cows:
                region.add_locations({
                    location_name: location_data.address for location_name, location_data in cows_location_table.items()
                    if location_data.region == region_name
                }, SohLocation)
                
            region.add_exits(region_data_table[region_name].connecting_regions)

    def get_filler_item_name(self) -> str:
        return "Blue Rupee"

    def set_rules(self) -> None:
        # Completion condition.
        self.multiworld.completion_condition[self.player] = lambda state: True

    def fill_slot_data(self) -> Dict[str, Any]:
        return {
            "death_link": self.options.death_link.value,
        }
