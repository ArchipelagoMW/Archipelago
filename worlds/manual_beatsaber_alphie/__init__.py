from base64 import b64encode
import os
import random
import json

from .Data import item_table, progressive_item_table, location_table
from .Game import game_name, filler_item_name, starting_items
from .Locations import location_id_to_name, location_name_to_id, location_name_to_location
from .Items import item_id_to_name, item_name_to_id, item_name_to_item, advancement_item_names

from .Regions import create_regions
from .Items import ManualItem
from .Rules import set_rules
from .Options import manual_options
from .Helpers import is_option_enabled, get_option_value

from BaseClasses import ItemClassification, Tutorial, Item
from Fill import fill_restrictive
from worlds.AutoWorld import World, WebWorld

from .hooks.World import \
    before_pre_fill, after_pre_fill, \
    before_generate_basic, after_generate_basic, \
    before_create_item, after_create_item, \
    before_set_rules, after_set_rules, \
    before_create_regions, after_create_regions, \
    before_fill_slot_data, after_fill_slot_data

class ManualWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up manual game integration for Archipelago multiworld games.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Fuzzy"]
    )]


class ManualWorld(World):
    """
    Manual games allow you to set custom check locations and custom item names that will be rolled into a multiworld.
    This allows any variety of game -- PC, console, board games, Microsoft Word memes... really anything -- to be part of a multiworld randomizer.
    The key component to including these games is some level of manual restriction. Since the items are not actually withheld from the player, 
    the player must manually refrain from using these gathered items until the tracker shows that they have been acquired or sent.
    """
    game: str = game_name
    web = ManualWeb()

    option_definitions = manual_options
    data_version = 2
    required_client_version = (0, 3, 4)

    # These properties are set from the imports of the same name above.
    item_table = item_table
    progressive_item_table = progressive_item_table
    item_id_to_name = item_id_to_name
    item_name_to_id = item_name_to_id
    item_name_to_item = item_name_to_item
    advancement_item_names = advancement_item_names
    location_table = location_table # this is likely imported from Data instead of Locations because the Game Complete location should not be in here, but is used for lookups
    location_id_to_name = location_id_to_name
    location_name_to_id = location_name_to_id
    location_name_to_location = location_name_to_location

    def pre_fill(self):
        before_pre_fill(self, self.multiworld, self.player)

        location_game_complete = self.multiworld.get_location("__Manual Game Complete__", self.player)
        location_game_complete.address = None

        location_game_complete.place_locked_item(
            ManualItem("__Victory__", ItemClassification.progression, None, player=self.player))
        
        after_pre_fill(self, self.multiworld, self.player)

    def generate_basic(self):
        # Generate item pool
        pool = []
        configured_item_names = self.item_id_to_name.copy()

        for name in configured_item_names.values():
            if name == "__Victory__":
                continue

            # If it's the filler item, skip it until we know if we need any extra items
            if name == filler_item_name:
                continue

            # if (hasattr(self.multiworld, "progressive_items") and len(self.multiworld.progressive_items) > 0):
            #     shouldUseProgressive = (self.multiworld.progressive_items[self.player].value);

            #     if shouldUseProgressive and name in self.progressive_item_table:
            #         name = self.progressive_item_table[name]

            item = self.item_name_to_item[name]
            item_count = 1

            if "count" in item:
                item_count = int(item["count"])

            for i in range(item_count):
                new_item = self.create_item(name)
                pool.append(new_item)
                
        items_started = []

        if starting_items:
            for starting_item_block in starting_items:
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

                random.shuffle(items)

                # if the setting lists a specific number of random items that should be pulled, only use a subset equal to that number
                if "random" in starting_item_block:
                    items = items[0:starting_item_block["random"]]

                for starting_item in items:
                    items_started.append(starting_item)
                    self.multiworld.push_precollected(starting_item)
                    pool.remove(starting_item)

        extras = len(location_table) - len(pool) - 1 # subtracting 1 because of Victory; seems right

        if extras > 0:
            for i in range(0, extras):
                extra_item = self.create_item(filler_item_name)
                pool.append(extra_item)

        pool = before_generate_basic(pool, self, self.multiworld, self.player)

        # need to put all of the items in the pool so we can have a full state for placement
        # then will remove specific item placements below from the overall pool
        self.multiworld.itempool += pool

        # Handle specific item placements using fill_restrictive
        locations_with_placements = [location for location in location_name_to_location.values() if "place_item" in location or "place_item_category" in location]

        for location in locations_with_placements:
            eligible_items = []

            if "place_item" in location:
                if len(location["place_item"]) == 0:
                    continue

                eligible_items = [item for item in self.multiworld.itempool if item.name in location["place_item"] and item.player == self.player]
                
                if len(eligible_items) == 0:
                    raise Exception("Could not find a suitable item to place at %s. No items that match %s." % (location["name"], ", ".join(location["place_item"])))

            if "place_item_category" in location:
                if len(location["place_item_category"]) == 0:
                    continue

                eligible_item_names = [i["name"] for i in item_name_to_item.values() if "category" in i and set(i["category"]).intersection(location["place_item_category"])]
                eligible_items = [item for item in self.multiworld.itempool if item.name in eligible_item_names and item.player == self.player]

                if len(eligible_items) == 0:
                    raise Exception("Could not find a suitable item to place at %s. No items that match categories %s." % (location["name"], ", ".join(location["place_item_category"])))

            # if we made it here and items is empty, then we encountered an unknown issue... but also can't do anything to place, so error
            if len(eligible_items) == 0:
                raise Exception("Custom item placement at location %s failed." % (location["name"]))

            item_to_place = random.choice(eligible_items)
            location_to_place_list = list(filter(lambda l: l.name == location["name"], self.multiworld.get_unfilled_locations(player=self.player)))

            if len(location_to_place_list) > 0:
                location_to_place = location_to_place_list[0]
                location_to_place.place_locked_item(item_to_place)
            else:
                raise Exception("Failed to find a suitable location named %s to place item %s." % (location["name"], item_to_place.name))

            # remove the item we're about to place from the pool so it isn't placed twice
            self.multiworld.itempool.remove(item_to_place)

        after_generate_basic(self, self.multiworld, self.player)
                        
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

    def create_regions(self):
        before_create_regions(self, self.multiworld, self.player)

        create_regions(self, self.multiworld, self.player)

        after_create_regions(self, self.multiworld, self.player)
        
    def fill_slot_data(self):
        slot_data = before_fill_slot_data({}, self, self.multiworld, self.player)

        # slot_data["DeathLink"] = bool(self.multiworld.death_link[self.player].value)

        slot_data = after_fill_slot_data(slot_data, self, self.multiworld, self.player)

        return slot_data

    def client_data(self):
        return {
            "game": self.game,
            'player_name': self.multiworld.get_player_name(self.player),
            'player_id': self.player,
        }

    def generate_output(self, output_directory: str):
        data = self.client_data()
        filename = f"{self.multiworld.get_out_file_name_base(self.player)}.apmanual"
        with open(os.path.join(output_directory, filename), 'wb') as f:
            f.write(b64encode(bytes(json.dumps(data), 'utf-8')))