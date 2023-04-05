import typing
from .Items import item_table, ShiversItem, get_full_item_list
# from .Options import Shivers_options
from .Rules import set_rules
from BaseClasses import Item, Tutorial, Region, Entrance, Location, ItemClassification
from Fill import fill_restrictive
from ..AutoWorld import World, WebWorld
from . import Constants

client_version = 1


class ShiversWeb(WebWorld):
    tutorials = [Tutorial(
        "Shivers Setup Guide",
        "A guide to setting up Shivers for Multiworld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Godl-Fire"]
    )]


class ShiversWorld(World):
    """ 
     Shivers is a horror themed point and click adventure. Explore the mysteries of Windlenot's Museum of the Strange and Unusual.
    """

    game: str = "Shivers"
    topology_present = False
    web = ShiversWeb()

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = Constants.location_name_to_id
    data_version = 0

    def create_item(self, name: str) -> Item:
        data = get_full_item_list()[name]
        return ShiversItem(name, data.classification, data.code, self.player)

    def create_event(self, region_name: str, event_name: str) -> None:
        region = self.multiworld.get_region(region_name, self.player)
        loc = ShiversLocation(self.player, event_name, None, region)
        loc.place_locked_item(self.create_event_item(event_name))
        region.locations.append(loc)

    def create_event_item(self, name: str) -> None:
        item = self.create_item(name)
        item.classification = ItemClassification.progression
        return item

    # option_definitions = Shivers_options
    def pre_fill(self) -> None:
        storagelocs = []
        storageitems = []
         
        for region_name, locations in Constants.location_info["locations_by_region"].items():
            region = self.multiworld.get_region(region_name, self.player)
            for loc_name in locations:
                if loc_name.startswith("Accessible: "):
                    loc = ShiversLocation(self.player, loc_name,
                                          self.location_name_to_id.get(loc_name, None), region)
                    storagelocs.append(loc)
        
        storageitems += [self.create_item(name) for name, data in item_table.items() if data.type == 'potduplicate']

        state = self.multiworld.get_all_state(False)

        fill_restrictive(self.multiworld, state, storagelocs, storageitems, True)

    def create_regions(self):
        # Create regions
        for region_name, exits in Constants.region_info["regions"]:
            r = Region(region_name, self.player, self.multiworld)
            for exit_name in exits:
                r.exits.append(Entrance(self.player, exit_name, r))
            self.multiworld.regions.append(r)

        # Bind mandatory connections
        for entr_name, region_name in Constants.region_info["mandatory_connections"]:
            e = self.multiworld.get_entrance(entr_name, self.player)
            r = self.multiworld.get_region(region_name, self.player)
            e.connect(r)

        # Add locations
        for region_name, locations in Constants.location_info["locations_by_region"].items():
            region = self.multiworld.get_region(region_name, self.player)
            for loc_name in locations:
                if not loc_name.startswith("Accessible: "):
                    loc = ShiversLocation(self.player, loc_name,
                                          self.location_name_to_id.get(loc_name, None), region)
                    region.locations.append(loc)

    def generate_basic(self):

        # Add pots
        pots = [self.create_item(name) for name, data in item_table.items() if data.type == 'pot']

        # Add keys
        keys = [self.create_item(name) for name, data in item_table.items() if data.type == 'key']

        # Add abilities
        abilities = [self.create_item(name) for name, data in item_table.items() if data.type == 'ability']

        self.multiworld.itempool += pots
        self.multiworld.itempool += keys
        self.multiworld.itempool += abilities

        self.multiworld.completion_condition[self.player] = lambda state: state.has("Ash Pot Top", self.player)

    set_rules = set_rules

    # def _place_events(self):

    def generate_output(self, output_directory: str) -> None:

        return super().generate_output(output_directory)


class ShiversLocation(Location):
    game = "Shivers"
