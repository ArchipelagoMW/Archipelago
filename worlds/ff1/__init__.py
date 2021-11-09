from typing import Dict
from BaseClasses import Item, Location, MultiWorld
from .Items import ItemData, FF1Items
from .Locations import EventId, FF1Locations, generate_rule
from .Options import ff1_options
from ..AutoWorld import World


CHAOS_TERMINATED_EVENT = 'Terminated Chaos'


class FF1World(World):
    """
    FF1 is an JPRG originally release on the NES
    """

    options = ff1_options
    game = "Final Fantasy"
    topology_present = False
    remote_items = True
    data_version = 1
    remote_start_inventory = True

    ff1_items = FF1Items()
    ff1_locations = FF1Locations()
    item_name_groups = ff1_items.get_item_names_per_category()
    item_name_to_id = ff1_items.get_item_name_to_code_dict()
    location_name_to_id = ff1_locations.get_location_name_to_address_dict()

    def generate_early(self):
        return

    def create_regions(self):
        locations = get_options(self.world, 'locations')
        rules = get_options(self.world, 'rules')
        menu_region = self.ff1_locations.create_menu_region(self.player, locations, rules)
        terminated_event = Location(self.player, CHAOS_TERMINATED_EVENT, EventId, menu_region)
        terminated_item = Item(CHAOS_TERMINATED_EVENT, True, EventId, self.player)
        terminated_event.place_locked_item(terminated_item)
        # Require all items for now
        items = get_options(self.world, 'items')
        terminated_event.access_rule = generate_rule([[name for name in items.keys()]], self.player)
        menu_region.locations.append(terminated_event)
        self.world.regions = [menu_region]

    def create_item(self, name: str) -> Item:
        return self.ff1_items.generate_item(name, self.player)

    def set_rules(self):
        self.world.completion_condition[self.player] = lambda state: state.has(CHAOS_TERMINATED_EVENT, self.player)

    def generate_basic(self):
        items = get_options(self.world, 'items')
        self.world.itempool = [self.create_item(name) for name in items.keys()]

    def fill_slot_data(self) -> Dict[str, object]:
        slot_data: Dict[str, object] = {}

        return slot_data


def get_options(world: MultiWorld, name: str):
    return getattr(world, name, None)[1].value
