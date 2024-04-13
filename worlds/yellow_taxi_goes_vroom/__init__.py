from binascii import hexlify
from typing import List
from BaseClasses import ItemClassification, Region
from worlds.AutoWorld import World
from .Options import YTGVOptions
from .Items import YTGVItem
from .Locations import YTGVLocation
from .Names import ItemName, RegionName
from . import Items, Locations, Regions, Rules

class YTGVWorld(World):
    """Make full use of your advanced move-set to navigate hand-crafted retro worlds
    without a jump button in this vibrant love letter to the N64 era of collectathons!"""
    
    game = "Yellow Taxi Goes Vroom"
    # web = YellowTaxiGoesVroomWebWorld()

    options_dataclass = YTGVOptions
    options: YTGVOptions

    location_name_to_id = Locations.name_to_id
    item_name_to_id = Items.name_to_id

    print("####!!!!####!!!! DEBUG")
    print("location_name_to_id length:", len(location_name_to_id))
    print("item_name_to_id length:", len(item_name_to_id))

    def create_item(self, name: str) -> YTGVItem:
        print("###### DEBUG: create item: " + name)
        classification = ItemClassification.progression
        return YTGVItem(name, classification, Items.name_to_id[name], self.player)

    def create_regions(self) -> None:
        region_data_table = Regions.create_region_data_table(self);

        # Create regions
        for region_name in region_data_table.keys():
            print("#### DEBUG: creating region:", region_name)
            region = Region(region_name, self.player, self.multiworld);

            self.multiworld.regions.append(region)
        
        # Create locations
        for region_name in region_data_table.keys():
            region = self.multiworld.get_region(region_name, self.player)
            
            from pprint import pprint
            locations = Regions.region_name_to_locations.get(region_name, {})
            print("#### DEBUG: creating locations for region:", region_name)
            pprint(locations)
            region.add_locations(locations, YTGVLocation)

            region_data = region_data_table[region_name]
            region.add_exits(region_data.exits, region_data.rules)

    def create_items(self) -> None:
        item_pool: List[YTGVItem] = []

        item_pool += [
            self.create_item(ItemName.GEAR)
            for location_data
            in Locations.location_data_table.values()
            if location_data.is_gear
        ]

        from pprint import pprint
        print("##### DEBUG: item_pool size:", len(item_pool))

        self.multiworld.itempool += item_pool

    def set_rules(self) -> None:
        Rules.set_rules(self)

    def create_event(self, event: str) -> YTGVItem:
        return YTGVItem(event, ItemClassification.progression, None, self.player)