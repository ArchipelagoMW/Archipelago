from typing import Dict
from BaseClasses import Item, Location, MultiWorld
from .Items import ItemData, FF1Items, FF1_STARTER_ITEMS, FF1_PROGRESSION_LIST
from .Locations import EventId, FF1Locations, generate_rule, CHAOS_TERMINATED_EVENT
from .Options import ff1_options
from ..AutoWorld import World


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

        items = get_options(self.world, 'items')
        terminated_event.access_rule = generate_rule([[name for name in items.keys() if name in FF1_PROGRESSION_LIST]],
                                                     self.player)
        menu_region.locations.append(terminated_event)
        self.world.regions += [menu_region]

    def create_item(self, name: str) -> Item:
        return self.ff1_items.generate_item(name, self.player)

    def set_rules(self):
        self.world.completion_condition[self.player] = lambda state: state.has(CHAOS_TERMINATED_EVENT, self.player)

    def generate_basic(self):
        items = get_options(self.world, 'items')
        progression_item = self.world.random.choice([name for name in FF1_STARTER_ITEMS if name in items.keys()])
        self._place_first_item(progression_item)
        items = [self.create_item(name) for name in items.keys() if name != progression_item]

        self.world.itempool += items

    def _place_first_item(self, progression_item: str):
        if progression_item:
            rules = get_options(self.world, 'rules')
            starter_locations = [name for name, rules in rules.items() if rules and len(rules[0]) == 0]
            initial_location = self.world.random.choice(starter_locations)
            self.world.get_location(initial_location, self.player).place_locked_item(self.create_item(progression_item))

    def fill_slot_data(self) -> Dict[str, object]:
        slot_data: Dict[str, object] = {}

        return slot_data


def get_options(world: MultiWorld, name: str):
    return getattr(world, name, None)[1].value
