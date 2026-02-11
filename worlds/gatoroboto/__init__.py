from typing import List

from BaseClasses import ItemClassification, Region, Tutorial
from worlds.AutoWorld import WebWorld, World
from .Items import GatoRobotoItem, item_table, modules_item_data_table, cartridges_item_data_table
from .Items import (heater_events_item_data_table, 
                    aqueduct_events_item_data_table, 
                    vent_events_item_data_table, 
                    healthkits_item_data_table, 
                    item_data_table)
from .Locations import (GatoRobotoLocation,
                        location_table,
                        healthkit_location_data_table,
                        cartridge_location_data_table,
                        module_location_data_table,
                        event_location_data_table,
                        victory_location_data_table)
from .Names import ItemName, LocationName
from .Options import GatoRobotoOptions, gatoroboto_option_groups
from worlds.LauncherComponents import Type, launch_subprocess, Component, icon_paths, components
from .Presets import gatoroboto_options_presets
from Utils import local_path

from .Names import RegionName

def launch_client(*args):
    """
    Launch the Gato Roboto Client
    """
    from .GatoRobotoClient import launch
    from CommonClient import gui_enabled
    if gui_enabled:
        launch_subprocess(launch, name="GatoRobotoClient", args=args)
    else:
        launch()


components.append(Component("Gato Roboto Client",
                            func=launch_client,
                            component_type=Type.CLIENT,
                            icon="kiki",
                            supports_uri=True,
                            game_name="Gato Roboto"))

icon_paths['kiki'] = f"ap:{__name__}/data/Kiki.png"

def data_path(file_name: str):
    import pkgutil
    return pkgutil.get_data(__name__, f"data/{file_name}")

class GatoRobotoWebWorld(WebWorld):
    theme = "grass"
    
    setup_en = Tutorial(
        tutorial_name="Start Guide",
        description="A guide to playing Gato Roboto Archipelago",
        language="English",
        file_name="guide_en.md",
        link="guide/en",
        authors=["Pathkendle", "TheNickRyan"]
    )
    
    tutorials = [setup_en]
    options_presets = gatoroboto_options_presets
    option_groups = gatoroboto_option_groups
    
class GatoRobotoWorld(World):
    """
    Gato Roboto is a 2D Metroidvania Platformer where you play as a cat named Kiki attempting to save her owner after
    they crash-land on an alien planet. Collect weapon modules as you explore the various regions of the planet, but
    beware of irritable creatures and treacherous obstacles, and the dark secrets it holds...
    """
    # Class Data
    game = "Gato Roboto"
    web = GatoRobotoWebWorld()
    options_dataclass = GatoRobotoOptions
    options: GatoRobotoOptions
    location_name_to_id = location_table
    item_name_to_id = item_table
    
    # Instance Data
    def create_item(self, name) -> GatoRobotoItem:
        return GatoRobotoItem(name, item_data_table[name].type, item_data_table[name].code, self.player)
    
    def create_items(self) -> None:
        item_pool: List[GatoRobotoItem] = []
        item_count: int = 42 # this will be useful for future updates
        location_count: int = 42 # this will be useful for future updates

        item_pool += [self.create_item(name) 
                for name in modules_item_data_table.keys()]
        item_pool += [self.create_item(name) 
                for name in cartridges_item_data_table.keys()]
        item_pool += [self.create_item(name) 
                for name in healthkits_item_data_table.keys()]
        item_pool += [self.create_item(name) 
                for name in aqueduct_events_item_data_table.keys()]
        item_pool += [self.create_item(name) 
                for name in heater_events_item_data_table.keys()]
        item_pool += [self.create_item(name) 
                for name in vent_events_item_data_table.keys()]

        #Place aqua 3 check if not rocket jumps to prevent softlock
        # if not self.options.rocket_jumps:
        #     item_pool.remove(self.create_item(ItemName.progressive_aqueducts_3))
        #     aqueducts_3 = self.get_location(LocationName.loc_progressive_aqueducts_3)
        #     aqueducts_3.place_locked_item(GatoRobotoItem(ItemName.progressive_aqueducts_3,
        #                                                  ItemClassification.progression,
        #                                                  10239, self.player))
        
        #Place locked victory item & set completion condition
        victory_loc = self.get_location(LocationName.loc_victory)
        victory_loc.place_locked_item(GatoRobotoItem(ItemName.victory,
                                                     ItemClassification.progression,
                                                     10999, self.player))
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

        self.multiworld.itempool += item_pool
    
    def create_regions(self) -> None:
        from .Regions import region_data_table
        # Create Regions
        for region_name in region_data_table.keys():
            region = Region(region_name, self.player, self.multiworld)
            self.multiworld.regions.append(region)
        
        # Create Locations
        for region_name, region_data in region_data_table.items():
            region = self.multiworld.get_region(region_name, self.player)
            region.add_locations({
                location_name: location_data.address 
                for location_name, location_data in healthkit_location_data_table.items()
                if location_data.region == region_name
            })
            region.add_locations({
                location_name: location_data.address
                for location_name, location_data in cartridge_location_data_table.items()
                if location_data.region == region_name
            })
            region.add_locations({
                location_name: location_data.address 
                for location_name, location_data in module_location_data_table.items()
                if location_data.region == region_name
            })
            region.add_locations({
                location_name: location_data.address 
                for location_name, location_data in event_location_data_table.items()
                if location_data.region == region_name
            })
            region.add_locations({
                location_name: location_data.address
                for location_name, location_data in victory_location_data_table.items()
                if location_data.region == region_name
            })
            
            region.add_exits(region_data_table[region_name].connecting_regions)
            
    def get_filler_item_name(self):
        return ItemName.healthkit # not sure what this is doing
    
    def set_rules(self) -> None:
        from .Rules import set_rules
        set_rules(self)
        
    def fill_slot_data(self):
        return {
            "rocket_jumps": self.options.rocket_jumps.value,
            "precise_tricks": self.options.precise_tricks.value,
            "water_mech": self.options.water_mech.value,
            "small_mech": self.options.small_mech.value
        }