from base64 import b64encode
import logging
import os
import json
from typing import Callable, Optional

import Utils
from worlds.generic.Rules import forbid_items_for_player
from worlds.LauncherComponents import Component, SuffixIdentifier, components, Type, launch_subprocess

from .Data import item_table, location_table, region_table, category_table, meta_table
from .Game import game_name, filler_item_name, starting_items
from .Meta import world_description, world_webworld, enable_region_diagram
from .Locations import location_id_to_name, location_name_to_id, location_name_to_location, location_name_groups, victory_names
from .Items import item_id_to_name, item_name_to_id, item_name_to_item, item_name_groups
from .DataValidation import runGenerationDataValidation, runPreFillDataValidation

from .Regions import create_regions
from .Items import ManualItem
from .Rules import set_rules
from .Options import manual_options_data
from .Helpers import is_item_enabled, get_option_value, get_items_for_player, resolve_yaml_option

from BaseClasses import ItemClassification, Tutorial, Item
from Options import PerGameCommonOptions
from worlds.AutoWorld import World, WebWorld

from .hooks.World import \
    hook_get_filler_item_name, before_create_regions, after_create_regions, \
    before_create_items_starting, before_create_items_filler, after_create_items, \
    before_create_item, after_create_item, \
    before_set_rules, after_set_rules, \
    before_generate_basic, after_generate_basic, \
    before_fill_slot_data, after_fill_slot_data, before_write_spoiler, \
    before_extend_hint_information, after_extend_hint_information
from .hooks.Data import hook_interpret_slot_data

class ManualWorld(World):
    __doc__ = world_description
    game: str = game_name
    web = world_webworld

    options_dataclass = manual_options_data
    data_version = 2
    required_client_version = (0, 3, 4)

    # These properties are set from the imports of the same name above.
    item_table = item_table
    location_table = location_table # this is likely imported from Data instead of Locations because the Game Complete location should not be in here, but is used for lookups
    category_table = category_table

    item_id_to_name = item_id_to_name
    item_name_to_id = item_name_to_id
    item_name_to_item = item_name_to_item
    item_name_groups = item_name_groups

    filler_item_name = filler_item_name

    item_counts = {}
    start_inventory = {}

    location_id_to_name = location_id_to_name
    location_name_to_id = location_name_to_id
    location_name_to_location = location_name_to_location
    location_name_groups = location_name_groups
    victory_names = victory_names

    def get_filler_item_name(self) -> str:
        return hook_get_filler_item_name(self, self.multiworld, self.player) or self.filler_item_name

    def interpret_slot_data(self, slot_data: dict[str, any]):
        #this is called by tools like UT

        regen = False
        for key, value in slot_data.items():
            if key in self.options_dataclass.type_hints:
                getattr(self.options, key).value = value
                regen = True

        regen = hook_interpret_slot_data(self, self.player, slot_data) or regen
        return regen

    @classmethod
    def stage_assert_generate(cls, multiworld) -> None:
        runGenerationDataValidation()


    def create_regions(self):
        before_create_regions(self, self.multiworld, self.player)

        create_regions(self, self.multiworld, self.player)

        location_game_complete = self.multiworld.get_location(victory_names[get_option_value(self.multiworld, self.player, 'goal')], self.player)
        location_game_complete.address = None

        for unused_goal in [self.multiworld.get_location(name, self.player) for name in victory_names if name != location_game_complete.name]:
            unused_goal.parent_region.locations.remove(unused_goal)

        location_game_complete.place_locked_item(
            ManualItem("__Victory__", ItemClassification.progression, None, player=self.player))

        after_create_regions(self, self.multiworld, self.player)

    def create_items(self):
        # Generate item pool
        pool = []
        traps = []
        configured_item_names = self.item_id_to_name.copy()

        for name in configured_item_names.values():
            # victory gets placed via place_locked_item at the victory location in create_regions
            if name == "__Victory__": continue
            # the game.json filler item name is added to the item lookup, so skip it until it's potentially needed later
            if name == filler_item_name: continue # intentionally using the Game.py filler_item_name here because it's a non-Items item

            item = self.item_name_to_item[name]
            item_count = int(item.get("count", 1))

            if item.get("trap"):
                traps.append(name)

            if "category" in item:
                if not is_item_enabled(self.multiworld, self.player, item):
                    item_count = 0

            if item_count == 0: continue

            for _ in range(item_count):
                new_item = self.create_item(name)
                pool.append(new_item)

            if item.get("early"): # Some or all early
                if isinstance(item["early"],int) or (isinstance(item["early"],str) and item["early"].isnumeric()):
                    self.multiworld.early_items[self.player][name] = int(item["early"])

                elif isinstance(item["early"],bool): #No need to deal with true vs false since false wont get here
                    self.multiworld.early_items[self.player][name] = item_count

                else:
                    raise Exception(f"Item {name}'s 'early' has an invalid value of '{item['early']}'. \nA boolean or an integer was expected.")

            if item.get("local"): # All local
                if name not in self.options.local_items.value:
                    self.options.local_items.value.add(name)

            if item.get("local_early"): # Some or all local and early
                if isinstance(item["local_early"],int) or (isinstance(item["local_early"],str) and item["local_early"].isnumeric()):
                    self.multiworld.local_early_items[self.player][name] = int(item["local_early"])

                elif isinstance(item["local_early"],bool):
                    self.multiworld.local_early_items[self.player][name] = item_count

                else:
                    raise Exception(f"Item {name}'s 'local_early' has an invalid value of '{item['local_early']}'. \nA boolean or an integer was expected.")


        pool = before_create_items_starting(pool, self, self.multiworld, self.player)

        items_started = []

        if starting_items:
            for starting_item_block in starting_items:
                if not resolve_yaml_option(self.multiworld, self.player, starting_item_block):
                    continue
                # if there's a condition on having a previous item, check for any of them
                # if not found in items started, this starting item rule shouldn't execute, and check the next one
                if "if_previous_item" in starting_item_block:
                    matching_items = [item for item in items_started if item.name in starting_item_block["if_previous_item"]]

                    if len(matching_items) == 0:
                        continue

                # start with the full pool of items
                items = pool

                # if the setting lists specific item names, limit the items to just those
                if "items" in starting_item_block:
                    items = [item for item in pool if item.name in starting_item_block["items"]]

                # if the setting lists specific item categories, limit the items to ones that have any of those categories
                if "item_categories" in starting_item_block:
                    items_in_categories = [item["name"] for item in self.item_name_to_item.values() if "category" in item and len(set(starting_item_block["item_categories"]).intersection(item["category"])) > 0]
                    items = [item for item in pool if item.name in items_in_categories]

                self.random.shuffle(items)

                # if the setting lists a specific number of random items that should be pulled, only use a subset equal to that number
                if "random" in starting_item_block:
                    items = items[0:starting_item_block["random"]]

                for starting_item in items:
                    items_started.append(starting_item)
                    self.multiworld.push_precollected(starting_item)
                    pool.remove(starting_item)

        self.start_inventory = {i.name: items_started.count(i) for i in items_started}

        pool = before_create_items_filler(pool, self, self.multiworld, self.player)
        pool = self.adjust_filler_items(pool, traps)
        pool = after_create_items(pool, self, self.multiworld, self.player)

        # need to put all of the items in the pool so we can have a full state for placement
        # then will remove specific item placements below from the overall pool
        self.multiworld.itempool += pool

    def create_item(self, name: str) -> Item:
        name = before_create_item(name, self, self.multiworld, self.player)

        item = self.item_name_to_item[name]
        classification = ItemClassification.filler

        if "trap" in item and item["trap"]:
            classification = ItemClassification.trap

        if "useful" in item and item["useful"]:
            classification = ItemClassification.useful

        if "progression" in item and item["progression"]:
            classification = ItemClassification.progression

        if "progression_skip_balancing" in item and item["progression_skip_balancing"]:
            classification = ItemClassification.progression_skip_balancing

        item_object = ManualItem(name, classification,
                        self.item_name_to_id[name], player=self.player)

        item_object = after_create_item(item_object, self, self.multiworld, self.player)

        return item_object

    def set_rules(self):
        before_set_rules(self, self.multiworld, self.player)

        set_rules(self, self.multiworld, self.player)

        after_set_rules(self, self.multiworld, self.player)

    def generate_basic(self):
        before_generate_basic(self, self.multiworld, self.player)

        # Handle item forbidding
        manual_locations_with_forbid = {location['name']: location for location in location_name_to_location.values() if "dont_place_item" in location or "dont_place_item_category" in location}
        locations_with_forbid = [l for l in self.multiworld.get_unfilled_locations(player=self.player) if l.name in manual_locations_with_forbid.keys()]
        for location in locations_with_forbid:
            manual_location = manual_locations_with_forbid[location.name]
            forbidden_item_names = []

            if manual_location.get("dont_place_item"):
                forbidden_item_names.extend([i["name"] for i in item_name_to_item.values() if i["name"] in manual_location["dont_place_item"]])

            if manual_location.get("dont_place_item_category"):
                forbidden_item_names.extend([i["name"] for i in item_name_to_item.values() if "category" in i and set(i["category"]).intersection(manual_location["dont_place_item_category"])])

            if forbidden_item_names:
                forbid_items_for_player(location, set(forbidden_item_names), self.player)

        # Handle specific item placements using fill_restrictive
        manual_locations_with_placements = {location['name']: location for location in location_name_to_location.values() if "place_item" in location or "place_item_category" in location}
        locations_with_placements = [l for l in self.multiworld.get_unfilled_locations(player=self.player) if l.name in manual_locations_with_placements.keys()]
        for location in locations_with_placements:
            manual_location = manual_locations_with_placements[location.name]
            eligible_items = []
            eligible_item_names = []
            forbidden_item_names = []
            place_messages = []
            forbid_messages = []

            #First we get possible items names
            if manual_location.get("place_item"):
                eligible_item_names += manual_location["place_item"]
                place_messages.append('", "'.join(manual_location["place_item"]))

            if manual_location.get("place_item_category"):
                eligible_item_names += [i["name"] for i in item_name_to_item.values() if "category" in i and set(i["category"]).intersection(manual_location["place_item_category"])]
                place_messages.append('", "'.join(manual_location["place_item_category"]) + " category(ies)")

            # Second we check for forbidden items names
            if manual_location.get("dont_place_item"):
                forbidden_item_names += manual_location["dont_place_item"]
                forbid_messages.append('", "'.join(manual_location["dont_place_item"]) + ' items')

            if manual_location.get("dont_place_item_category"):
                forbidden_item_names += [i["name"] for i in item_name_to_item.values() if "category" in i and set(i["category"]).intersection(manual_location["dont_place_item_category"])]
                forbid_messages.append('", "'.join(manual_location["dont_place_item_category"]) + ' category(ies)')

            # If we forbid some names, check for those in the possible names and remove them
            if forbidden_item_names:
                eligible_item_names = [name for name in eligible_item_names if name not in forbidden_item_names]

            if eligible_item_names:
                eligible_items = [item for item in self.multiworld.itempool if item.player == self.player and item.name in eligible_item_names]

            if len(eligible_items) == 0:
                nl = "\n"
                if forbidden_item_names:
                    raise Exception(f'Could not find a suitable item to place at "{manual_location["name"]}".\n    No items that match "{f"{nl}     or ".join(place_messages)}"\n    Maybe because of forbidden "{f"{nl}     or ".join(forbid_messages)}"')
                raise Exception(f'Could not find a suitable item to place at "{manual_location["name"]}". \n    No items that match "{f"{nl}     or ".join(place_messages)}"')

            item_to_place = self.random.choice(eligible_items)
            location.place_locked_item(item_to_place)

            # remove the item we're about to place from the pool so it isn't placed twice
            self.multiworld.itempool.remove(item_to_place)


        after_generate_basic(self, self.multiworld, self.player)

        # Enable this in Meta.json to generate a diagram of your manual.  Only works on 0.4.4+
        if enable_region_diagram:
            from Utils import visualize_regions
            visualize_regions(self.multiworld.get_region("Menu", self.player), f"{self.game}_{self.player}.puml")

    def pre_fill(self):
        # DataValidation after all the hooks are done but before fill
        runPreFillDataValidation(self, self.multiworld)

    def fill_slot_data(self):
        slot_data = before_fill_slot_data({}, self, self.multiworld, self.player)

        # slot_data["DeathLink"] = bool(self.multiworld.death_link[self.player].value)
        common_options = set(PerGameCommonOptions.type_hints.keys())
        for option_key, _ in self.options_dataclass.type_hints.items():
            if option_key in common_options:
                continue
            slot_data[option_key] = get_option_value(self.multiworld, self.player, option_key)

        slot_data = after_fill_slot_data(slot_data, self, self.multiworld, self.player)

        return slot_data

    def generate_output(self, output_directory: str):
        data = self.client_data()
        filename = f"{self.multiworld.get_out_file_name_base(self.player)}.apmanual"
        with open(os.path.join(output_directory, filename), 'wb') as f:
            f.write(b64encode(bytes(json.dumps(data), 'utf-8')))

    def write_spoiler(self, spoiler_handle):
        before_write_spoiler(self, self.multiworld, spoiler_handle)

    def extend_hint_information(self, hint_data: dict[int, dict[int, str]]) -> None:
        before_extend_hint_information(hint_data, self, self.multiworld, self.player)
        
        for location in self.multiworld.get_locations(self.player):
            if not location.address:
                continue
            if "hint_entrance" in self.location_name_to_location[location.name]:
                if self.player not in hint_data:
                    hint_data.update({self.player: {}})
                hint_data[self.player][location.address] = self.location_name_to_location[location.name]["hint_entrance"]
        
        after_extend_hint_information(hint_data, self, self.multiworld, self.player)

    ###
    # Non-standard AP world methods
    ###

    def add_filler_items(self, item_pool, traps):
        Utils.deprecate("Use adjust_filler_items instead.")
        return self.adjust_filler_items(item_pool, traps)

    def adjust_filler_items(self, item_pool, traps):
        extras = len(self.multiworld.get_unfilled_locations(player=self.player)) - len(item_pool)

        if extras > 0:
            trap_percent = get_option_value(self.multiworld, self.player, "filler_traps")
            if not traps:
                trap_percent = 0

            trap_count = extras * trap_percent // 100
            filler_count = extras - trap_count

            for _ in range(0, trap_count):
                extra_item = self.create_item(self.random.choice(traps))
                item_pool.append(extra_item)

            for _ in range(0, filler_count):
                extra_item = self.create_item(self.get_filler_item_name())
                item_pool.append(extra_item)
        elif extras < 0:
            logging.warning(f"{self.game} has more items than locations. {abs(extras)} non-progression items will be removed at random.")
            fillers = [item for item in item_pool if item.classification == ItemClassification.filler]
            traps = [item for item in item_pool if item.classification == ItemClassification.trap]
            useful = [item for item in item_pool if item.classification == ItemClassification.useful]
            self.random.shuffle(fillers)
            self.random.shuffle(traps)
            self.random.shuffle(useful)
            for _ in range(0, abs(extras)):
                popped = None
                if fillers:
                    popped = fillers.pop()
                elif traps:
                    popped = traps.pop()
                elif useful:
                    popped = useful.pop()
                else:
                    logging.warning("Could not remove enough non-progression items from the pool.")
                    break
                item_pool.remove(popped)

        return item_pool

    def get_item_counts(self, player: Optional[int] = None, reset: bool = False) -> dict[str, int]:
        """returns the player real item count"""
        if player is None:
            player = self.player

        if not self.item_counts.get(player, {}) or reset:
            real_pool = get_items_for_player(self.multiworld, player, True)
            self.item_counts[player] = {i.name: real_pool.count(i) for i in real_pool}
        return self.item_counts.get(player)

    def client_data(self):
        return {
            "game": self.game,
            'player_name': self.multiworld.get_player_name(self.player),
            'player_id': self.player,
            'items': self.item_name_to_item,
            'locations': self.location_name_to_location,
            # todo: extract connections out of multiworld.get_regions() instead, in case hooks have modified the regions.
            'regions': region_table,
            'categories': category_table
        }

###
# Non-world client methods
###

def launch_client(*args):
    import CommonClient
    from .ManualClient import launch as Main

    if CommonClient.gui_enabled:
        launch_subprocess(Main, name="Manual client")
    else:
        Main()

class VersionedComponent(Component):
    def __init__(self, display_name: str, script_name: Optional[str] = None, func: Optional[Callable] = None, version: int = 0, file_identifier: Optional[Callable[[str], bool]] = None):
        super().__init__(display_name=display_name, script_name=script_name, func=func, component_type=Type.CLIENT, file_identifier=file_identifier)
        self.version = version

def add_client_to_launcher() -> None:
    version = 2024_09_19 # YYYYMMDD
    found = False
    for c in components:
        if c.display_name == "Manual Client":
            found = True
            if getattr(c, "version", 0) < version:  # We have a newer version of the Manual Client than the one the last apworld added
                c.version = version
                c.func = launch_client
                return
    if not found:
        components.append(VersionedComponent("Manual Client", "ManualClient", func=launch_client, version=version, file_identifier=SuffixIdentifier('.apmanual')))

add_client_to_launcher()
