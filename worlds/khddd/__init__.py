from typing import List, Dict, Any

from BaseClasses import Region, Entrance, Tutorial
from worlds.AutoWorld import World, WebWorld
from .Items import KHDDDItem, item_data_table, item_table, get_items_by_category, get_items_by_character_category
from .Locations import KHDDDLocation, location_data_table, location_table, event_location_table, get_locations_by_region
from .Options import KHDDDOptions
from .Regions import region_data_table, create_regions
from .Rules import set_rules
from worlds.LauncherComponents import Component, components, Type, launch as launch_component
import random

def launch_client():
    from .Client import launch
    launch_component(launch, name="KHDDD Client")

components.append(Component("KHDDD Client", "KHDDD Client", func=launch_client, component_type=Type.CLIENT))


class KHDDDWebWorld(WebWorld):
    theme = "grass"

    setup_en = Tutorial(
        tutorial_name="Start Guide",
        description="A guide to playing Kingdom Hearts 3D Archipelago",
        language="English",
        file_name="setup_en.md",
        link="setup/en",
        authors=["Unknown"]
    )

    tutorials = [setup_en]

class KHDDDWorld(World):
    """Dream Drop Distance focuses on Sora and Riku's Mark of Mastery exam, foreshadowed in Reconnect. Kingdom Hearts, the secret ending for Kingdom Hearts Re:coded, and its ending will lead fairly directly into Kingdom Hearts III. The plot will also have connections to Kingdom Hearts Birth by Sleep and Kingdom Hearts 358/2 Days. The setting of Dream Drop Distance will again be spread across several worlds; several Kingdom Hearts-original worlds will return, such as Traverse Town, but all of the Disney-based worlds will be entirely new. """
    game = "Kingdom Hearts Dream Drop Distance"
    web = KHDDDWebWorld()
    options: KHDDDOptions
    options_dataclass = KHDDDOptions
    #location_name_to_id = event_location_table
    location_name_to_id = {name: data.code for name, data in location_data_table.items()}
    item_name_to_id = item_table
    origin_region_name = "World"

    def create_item(self, name: str) -> KHDDDItem:
        return KHDDDItem(name, item_data_table[name].type, item_data_table[name].code, self.player)

    def create_items(self) -> None:
        self.place_predetermined_items()

        #Starting Worlds
        starting_worlds = []
        if self.options.starting_worlds > 0:
            possible_starting_worlds = []
            if self.options.character < 2: #TODO: Include Traverse Town
                possible_starting_worlds = possible_starting_worlds + ["La Cite des Cloches [Sora]", "Prankster's Paradise [Sora]",
                    "Country of the Musketeers [Sora]", "Symphony of Sorcery [Sora]"]
            if self.options.character == 2 or self.options.character == 0:
                possible_starting_worlds = possible_starting_worlds + [ "The Grid [Riku]",
                    "La Cite des Cloches [Riku]", "Prankster's Paradise [Riku]", "Country of the Musketeers [Riku]", "Symphony of Sorcery [Riku]"]
            starting_worlds = self.random.sample(possible_starting_worlds, min(self.options.starting_worlds, len(possible_starting_worlds)))
            for starting_world in starting_worlds:
                self.multiworld.push_precollected(self.create_item(starting_world))

        item_pool: List[KHDDDItem] = []

        # Pre-fill level up locations if applicable
        filler_stat_names = ["Strength Increase [Sora]", "Magic Increase [Sora]", "Defense Increase [Sora]",
                             "Strength Increase [Riku]", "Magic Increase [Riku]", "Defense Increase [Riku]"]

        if not self.options.stats_on_levels:
            for _ in range(self.options.strength_in_pool):
                if self.options.character == 0 or self.options.character == 1:
                    item_pool += [self.create_item("Strength Increase [Sora]")]
                if self.options.character == 0 or self.options.character == 2:
                    item_pool += [self.create_item("Strength Increase [Riku]")]
            for _ in range(self.options.magic_in_pool):
                if self.options.character == 0 or self.options.character == 1:
                    item_pool += [self.create_item("Magic Increase [Sora]")]
                if self.options.character == 0 or self.options.character == 2:
                    item_pool += [self.create_item("Magic Increase [Riku]")]
            for _ in range(self.options.defense_in_pool):
                if self.options.character == 0 or self.options.character == 1:
                    item_pool += [self.create_item("Defense Increase [Sora]")]
                if self.options.character == 0 or self.options.character == 2:
                    item_pool += [self.create_item("Defense Increase [Riku]")]

        if self.options.stats_on_levels:  # Place Stats on levels
            possible_level_up_item_pool = []

            for name, data in get_items_by_category("Stat").items():
                quantity = data.qty
                if data.category == "Stat":
                    if name in filler_stat_names:
                        if self.options.character == 0 or self.options.character == 1 and "Sora" in name or self.options.character == 2 and "Riku" in name:
                            for _ in range(quantity):
                                possible_level_up_item_pool.append(name)

            self.random.shuffle(possible_level_up_item_pool)

            level_up_item_pool = possible_level_up_item_pool
            level_up_locations = list(get_locations_by_region("Levels").keys())

            current_level_for_placing_stats = 1

            if self.options.character == 2:
                current_level_for_placing_stats = 50  # Riku's levels start here

            level_range = 99
            if self.options.character == 1:
                level_range = 50

            while len(level_up_item_pool) > 0 and current_level_for_placing_stats < level_range:
                self.get_location(level_up_locations[current_level_for_placing_stats - 1]).place_locked_item(
                    self.create_item(level_up_item_pool.pop()))
                current_level_for_placing_stats += 1

        total_locations = len(self.multiworld.get_unfilled_locations(self.player))

        #Add correct flowmotion to the item pool
        if int(self.options.single_flowmotion) == 1: #Flowmotion is a single item
            item_pool += [self.create_item("Flowmotion")]
        else:
            for name, data in get_items_by_category("Flowmotion").items(): #Each flowmotion is an individual item
                if name != "Flowmotion":
                    item_pool += [self.create_item(name)]

        #Add recipes to the item pool
        recipe_count = max(int(self.options.recipes_in_pool-2), int(self.options.recipe_reqs-2))
        recipes = []
        for name, data in get_items_by_category("Recipe").items():
            if name != "Meow Wow Recipe" and name != "Komory Bat Recipe":
                recipes.append(name)

        #Shuffle recipes and add to item pool based on reqs
        random.shuffle(recipes)
        for x in range(recipe_count):
            item_pool += [self.create_item(recipes[x])]

        #Always have Meow Wow and Komory Bat in the item pool
        item_pool += [self.create_item("Meow Wow Recipe")]
        item_pool += [self.create_item("Komory Bat Recipe")]

        non_filler_categories = ["Stat", "World", "Keyblade", "Movement", "Defense", "Ability", "Special"]

        for name, data in item_data_table.items():
            quantity = data.qty
            if data.category in non_filler_categories:
                #Prevent starting worlds and str/mag/def increases from being placed in pool again
                if name in starting_worlds or name in filler_stat_names:
                    continue

                #Omit any items not for the selected character
                if data.character > 0 and int(self.options.character) > 0 and data.character != self.options.character:
                    continue

                item_pool += [self.create_item(name) for _ in range(0, quantity)]

            #if name!="Victory":
            #    item_pool += [self.create_item(name)]

        #Fill empty locations with filler
        while len(item_pool) < total_locations:
            item_pool.append(self.create_item(self.get_filler_item_name()))

        self.multiworld.itempool += item_pool


    def place_predetermined_items(self) -> None:
        if self.options.goal == 1: #Place Superboss Goal Item
            self.get_location("All Superbosses Defeated [Sora] [Riku]").place_locked_item(self.create_item("Victory"))
        else:
            #Place Goal item based on who the final boss actually is
            if self.options.character == 0 or self.options.character == 2: #Either both characters or riku
                if self.options.armored_ventus_nightmare: #Are we fighting avn?
                    self.get_location("Armored Ventus Nightmare Defeated [Riku]").place_locked_item(self.create_item("Victory"))
                else: #We are fighting YX
                    self.get_location("The World That Never Was Young Xehanort Defeated [Riku]").place_locked_item(self.create_item("Victory"))
            else: #We are fighting Xemnas
                self.get_location("The World That Never Was Xemnas Bonus Slot 1 [Sora]").place_locked_item(self.create_item("Victory"))

    def create_regions(self) -> None:
        create_regions(self.multiworld, self.player, self.options)

    def get_filler_item_name(self) -> str:
        if int(self.options.instant_drop_trap_chance) > 0: #Check to see if a trap was rolled
            if int(self.random.randint(0, 99) < int(self.options.instant_drop_trap_chance)):
                return "Instant Drop"
        fillers = {}
        fillers.update(get_items_by_character_category(int(self.options.character), "Command"))
        fillers.update(get_items_by_character_category(int(self.options.character), "Item"))
        return self.random.choices([filler for filler in fillers.keys()])[0]


    def set_rules(self):
        set_rules(self)

    def fill_slot_data(self) -> Dict[str, Any]:
        slot_data = {"character": int(self.options.character)}
        #Roll random keyblade stats
        if self.options.randomize_keyblade_stats:
            slot_data["keyblade_stats"] = ""
            min_str_bonus = self.options.keyblade_min_str.value
            max_str_bonus = self.options.keyblade_max_str.value
            min_mag_bonus = self.options.keyblade_min_mag.value
            max_mag_bonus = self.options.keyblade_max_mag.value
            for i in range(30):
                str_bonus = int(self.random.randint(min_str_bonus, max_str_bonus))
                mag_bonus = int(self.random.randint(min_mag_bonus, max_mag_bonus))
                slot_data["keyblade_stats"] = slot_data["keyblade_stats"] + str(str_bonus) + "," + str(mag_bonus) + ","
            slot_data["keyblade_stats"] = slot_data["keyblade_stats"][:-1]

        if int(self.options.character) < 2:
            slot_data["play_destiny_islands"] = str(self.options.play_destiny_islands.value)
        else:
            slot_data["play_destiny_islands"] = "0"

        slot_data["skip_light_cycle"] = str(self.options.skip_light_cycle.value)
        slot_data["fast_go_mode"] = str(self.options.fast_go_mode.value)
        slot_data["exp_multiplier"] = int(self.options.exp_multiplier.value)
        slot_data["stat_bonus"] = int(self.options.stat_bonus.value)

        slot_data["recipe_reqs"] = int(self.options.recipe_reqs.value)
        slot_data["win_con"] = int(self.options.goal.value)

        slot_data["lord_kyroo"] = str(self.options.lord_kyroo.value)
        slot_data["local_item_notifs"] = str(self.options.received_notifications.value)
        slot_data["remote_item_notifs"] = str(self.options.sent_notifications.value)

        return slot_data
