from BaseClasses import Region, Entrance, Location, MultiWorld, Item, RegionType, Tutorial
from .Items import TunicItems
from .Locations import TunicLocations
from .Options import TunicOptions
from .Regions import TunicRegions
from ..AutoWorld import World, LogicMixin, WebWorld


class TunicWeb(WebWorld):
    settings_page = True
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing Tunic randomizer and multiworld.",
        "English",
        "en_Tunic.md",
        "tunic_guide/en",
        ["dr4g0nsoul"]
    )]


class TunicWorld(World):
    """
    Explore a land filled with lost legends, ancient powers, and ferocious monsters in TUNIC, an isometric action game
    about a small fox on a big adventure. Stranded in a ruined land, and armed with only your own curiosity, you will
    confront colossal beasts, collect strange and powerful items, and unravel long-lost secrets
    """

    web = TunicWeb()

    game: str = "Tunic"  # name of the game/world
    options = TunicOptions.generate_tunic_options()  # options the player can set
    topology_present: bool = True  # show path to required location checks in spoiler
    remote_items: bool = True  # True if all items come from the server
    remote_start_inventory: bool = True  # True if start inventory comes from the server

    # data_version is used to signal that items, locations or their names
    # changed. Set this to 0 during development so other games' clients do not
    # cache any texts, then increase by 1 for each release that makes changes.
    data_version = 1

    # ID of first item and location
    base_id_item = 1234
    base_id_location = 1234

    # The following two dicts are required for the generation to know which
    # items exist. They could be generated from json or something else. They can
    # include events, but don't have to since events will be placed manually.
    tunic_items = TunicItems()
    tunic_locations = TunicLocations()
    tunic_regions = TunicRegions()
    item_name_to_id = tunic_items.get_item_name_to_code_dict()
    location_name_to_id = tunic_locations.get_location_name_to_code_dict()

    # Items can be grouped using their names to allow easy checking if any item
    # from that group has been collected. Group names can also be used for !hint
    item_name_groups = tunic_items.get_item_names_per_category()

    def create_item(self, name: str) -> Item:
        return self.tunic_items.generate_item(name, self.player)

    def create_items(self):
        for item_name in self.tunic_items.get_all_item_names():
            for _ in range(self.tunic_items.get_item_quantity(item_name)):
                self.world.itempool.append(self.create_item(item_name))

    def create_regions(self) -> None:
        # Create start region
        r = Region("Menu", RegionType.Generic, "Menu", self.player, self.world)
        r.exits.append(Entrance(self.player, "New Game", r))
        self.world.regions.append(r)

        # Generate ingame regions
        for tunic_region in self.tunic_regions.get_tunic_regions():
            r = Region(tunic_region.name, RegionType.Generic, tunic_region.name, self.player, self.world)
            r.exits = [Entrance(self.player, exitName, r) for exitName in tunic_region.exits]
            # Add locations
            r.locations = self.tunic_locations.generate_area_locations(tunic_region.name, self.player, r)
            self.world.regions.append(r)

        # Add starting connection
        self.world.get_entrance("New Game", self.player).connect(self.world.get_region("Overworld Redux", self.player))

        # Add other connections
        for tunic_connection in self.tunic_regions.get_tunic_connections():
            if tunic_connection.destination:
                self.world.get_entrance(tunic_connection.exit, self.player)\
                    .connect(self.world.get_region(tunic_connection.destination, self.player))

    def generate_basic(self):
        for locations in self.world.get_locations():
            locations.always_allow = TunicWorld.locations_always_allow
        print(len(self.world.get_locations()))

    @staticmethod
    def locations_always_allow(item, state: False):
        return True
