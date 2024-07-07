from typing import List

from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld, World
from .Items import KH1Item, KH1ItemData, event_item_table, get_items_by_category, item_table, item_name_groups
from .Locations import KH1Location, location_table, get_locations_by_category, location_name_groups
from .Options import KH1Options
from .Regions import create_regions
from .Rules import set_rules
from worlds.LauncherComponents import Component, components, Type, launch_subprocess


def launch_client():
    from .Client import launch
    launch_subprocess(launch, name="KH1 Client")


components.append(Component("KH1 Client", "KH1Client", func=launch_client, component_type=Type.CLIENT))


class KH1Web(WebWorld):
    theme = "ocean"
    tutorials = [Tutorial(
            "Multiworld Setup Guide",
            "A guide to setting up the Kingdom Hearts Randomizer software on your computer. This guide covers single-player, "
            "multiworld, and related software.",
            "English",
            "kh1_en.md",
            "kh1/en",
            ["Gicu"]
    )]


class KH1World(World):
    """
    Kingdom Hearts is an action RPG following Sora on his journey 
    through many worlds to find Riku and Kairi.
    """
    game = "Kingdom Hearts"
    options_dataclass = KH1Options
    options: KH1Options
    topology_present = True
    required_client_version = (0, 3, 5)
    web = KH1Web()

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {name: data.code for name, data in location_table.items()}
    item_name_groups = item_name_groups
    location_name_groups = location_name_groups

    def create_items(self):
        #Handle starting worlds
        starting_worlds = []
        if self.options.starting_worlds > 0:
            possible_starting_worlds = ["Wonderland", "Olympus Coliseum", "Deep Jungle", "Agrabah", "Monstro", "Halloween Town", "Neverland", "Hollow Bastion"]
            if self.options.atlantica:
                possible_starting_worlds.append("Atlantica")
            if self.options.end_of_the_world_unlock == "item":
                possible_starting_worlds.append("End of the World")
            starting_worlds = self.random.sample(possible_starting_worlds, min(self.options.starting_worlds, len(possible_starting_worlds)))
            for starting_world in starting_worlds:
                self.multiworld.push_precollected(self.create_item(starting_world))
        
        item_pool: List[KH1Item] = []
        possible_level_up_item_pool = []
        level_up_item_pool = []
        
        #Calculate Level Up Items
        if True: #Allow notepad++ to collapse this section
            # Fill pool with mandatory items
            for _ in range(self.options.item_slot_increase):
                level_up_item_pool.append("Item Slot Increase")
            for _ in range(self.options.accessory_slot_increase):
                level_up_item_pool.append("Accessory Slot Increase")

            # Create other pool
            for _ in range(self.options.strength_increase):
                possible_level_up_item_pool.append("Strength Increase")
            for _ in range(self.options.defense_increase):
                possible_level_up_item_pool.append("Defense Increase")
            for _ in range(self.options.hp_increase):
                possible_level_up_item_pool.append("Max HP Increase")
            for _ in range(self.options.mp_increase):
                possible_level_up_item_pool.append("Max MP Increase")
            for _ in range(self.options.ap_increase):
                possible_level_up_item_pool.append("Max AP Increase")

            # Fill remaining pool with items from other pool
            while len(level_up_item_pool) < 100 and len(possible_level_up_item_pool) > 0:
                level_up_item_pool.append(possible_level_up_item_pool.pop(self.random.randrange(len(possible_level_up_item_pool))))

            level_up_locations = list(get_locations_by_category("Levels").keys())
            self.random.shuffle(level_up_item_pool)
            starting_level_for_stats_only = self.options.force_stats_on_levels - 1
            while len(level_up_item_pool) > 0 and starting_level_for_stats_only < self.options.level_checks:
                self.multiworld.get_location(level_up_locations[starting_level_for_stats_only], self.player).place_locked_item(self.create_item(level_up_item_pool.pop()))
                starting_level_for_stats_only += 1
        
        #Calculate prefilled locations and items
        if True: #Allow notepad++ to collpase this section
            prefilled_items = []
            prefilled_locations = 1 #Victory
            if self.options.junk_in_missable_locations:
                prefilled_locations = prefilled_locations + 15
            if self.options.vanilla_emblem_pieces:
                prefilled_locations = prefilled_locations + 4
                prefilled_items = prefilled_items + ["Emblem Piece (Flame)", "Emblem Piece (Chest)", "Emblem Piece (Fountain)", "Emblem Piece (Statue)"]
        
        total_locations = len(self.multiworld.get_unfilled_locations(self.player)) - prefilled_locations
        
        non_filler_item_categories = ["Key", "Magic", "Worlds", "Trinities", "Cups", "Summons", "Abilities", "Shared Abilities", "Keyblades", "Accessory", "Weapons", "Puppies"]
        if self.options.hundred_acre_wood:
            non_filler_item_categories.append("Torn Pages")
        for name, data in item_table.items():
            quantity = data.max_quantity
            if data.category not in non_filler_item_categories:
                continue
            if name in starting_worlds:
                continue
            if data.category == "Puppies":
                if self.options.puppies == "triplets" and "-" in name:
                    item_pool += [self.create_item(name) for _ in range(quantity)]
                if self.options.puppies == "individual" and "Puppy" in name:
                    item_pool += [self.create_item(name) for _ in range(0, quantity)]
                if self.options.puppies == "full" and name == "All Puppies":
                    item_pool += [self.create_item(name) for _ in range(0, quantity)]
            elif name == "Atlantica":
                if self.options.atlantica:
                    item_pool += [self.create_item(name) for _ in range(0, quantity)]
            elif name == "Mermaid Kick":
                if self.options.atlantica:
                    if self.options.extra_shared_abilities:
                        item_pool += [self.create_item(name) for _ in range(0, 2)]
                    else:
                        item_pool += [self.create_item(name) for _ in range(0, quantity)]
            elif name == "Crystal Trident":
                if self.options.atlantica:
                    item_pool += [self.create_item(name) for _ in range(0, quantity)]
            elif name == "High Jump":
                if self.options.extra_shared_abilities:
                    item_pool += [self.create_item(name) for _ in range(0, 3)]
                else:
                    item_pool += [self.create_item(name) for _ in range(0, quantity)]
            elif name == "Progressive Glide":
                if self.options.extra_shared_abilities:
                    item_pool += [self.create_item(name) for _ in range(0, 4)]
                else:
                    item_pool += [self.create_item(name) for _ in range(0, quantity)]
            elif name == "End of the World":
                if self.options.end_of_the_world_unlock.current_key == "item":
                    item_pool += [self.create_item(name) for _ in range(0, quantity)]
            elif name == "EXP Zero":
                if self.options.exp_zero_in_pool:
                    item_pool += [self.create_item(name) for _ in range(0, quantity)]
            elif name not in prefilled_items:
                item_pool += [self.create_item(name) for _ in range(0, quantity)]
        
        for i in range(self.determine_reports_in_pool()):
            item_pool += [self.create_item("Ansem's Report " + str(i+1))]
        
        while len(item_pool) > total_locations:
            item_pool.pop(0)
        
        while len(item_pool) < total_locations and len(level_up_item_pool) > 0:
            item_pool += [self.create_item(level_up_item_pool.pop())]
        
        # Fill any empty locations with filler items.
        item_names = []
        attempts = 0  # If we ever try to add items 200 times, and all the items are used up, lets clear the item_names array, we probably don't have enough items
        while len(item_pool) < total_locations:
            item_name = self.get_filler_item_name()
            if item_name not in item_names:
                item_names.append(item_name)
                item_pool.append(self.create_item(item_name))
                attempts = 0
            elif attempts >= 200:
                item_names = []
                attempts = 0
            else:
                attempts = attempts + 1

        self.multiworld.itempool += item_pool

    def pre_fill(self) -> None:
        goal_dict = {
            "sephiroth":       "Olympus Coliseum Defeat Sephiroth Ansem's Report 12",
            "unknown":         "Hollow Bastion Defeat Unknown Ansem's Report 13",
            "postcards":       "Traverse Town Mail Postcard 10 Event",
            "final_ansem":     "Final Ansem",
            "puppies":         "Traverse Town Piano Room Return 99 Puppies Reward 2",
            "final_rest":      "End of the World Final Rest Chest"
        }
        self.multiworld.get_location(goal_dict[self.options.goal.current_key], self.player).place_locked_item(self.create_item("Victory"))
        if self.options.junk_in_missable_locations:
            self.multiworld.get_location("Traverse Town 1st District Leon Gift", self.player).place_locked_item(self.create_item("Elixir"))
            self.multiworld.get_location("Traverse Town 1st District Aerith Gift", self.player).place_locked_item(self.create_item("Elixir"))
            self.multiworld.get_location("End of the World World Terminus Hollow Bastion Chest", self.player).place_locked_item(self.create_item("Elixir"))
            self.multiworld.get_location("Neverland Clock Tower 01:00 Door", self.player).place_locked_item(self.create_item("Elixir"))
            self.multiworld.get_location("Neverland Clock Tower 02:00 Door", self.player).place_locked_item(self.create_item("Elixir"))
            self.multiworld.get_location("Neverland Clock Tower 03:00 Door", self.player).place_locked_item(self.create_item("Elixir"))
            self.multiworld.get_location("Neverland Clock Tower 04:00 Door", self.player).place_locked_item(self.create_item("Elixir"))
            self.multiworld.get_location("Neverland Clock Tower 05:00 Door", self.player).place_locked_item(self.create_item("Elixir"))
            self.multiworld.get_location("Neverland Clock Tower 06:00 Door", self.player).place_locked_item(self.create_item("Elixir"))
            self.multiworld.get_location("Neverland Clock Tower 07:00 Door", self.player).place_locked_item(self.create_item("Elixir"))
            self.multiworld.get_location("Neverland Clock Tower 08:00 Door", self.player).place_locked_item(self.create_item("Elixir"))
            self.multiworld.get_location("Neverland Clock Tower 09:00 Door", self.player).place_locked_item(self.create_item("Elixir"))
            self.multiworld.get_location("Neverland Clock Tower 10:00 Door", self.player).place_locked_item(self.create_item("Elixir"))
            self.multiworld.get_location("Neverland Clock Tower 11:00 Door", self.player).place_locked_item(self.create_item("Elixir"))
            self.multiworld.get_location("Neverland Clock Tower 12:00 Door", self.player).place_locked_item(self.create_item("Elixir"))
        if self.options.vanilla_emblem_pieces:
            self.multiworld.get_location("Hollow Bastion Entrance Hall Emblem Piece (Flame)", self.player).place_locked_item(self.create_item("Emblem Piece (Flame)"))
            self.multiworld.get_location("Hollow Bastion Entrance Hall Emblem Piece (Statue)", self.player).place_locked_item(self.create_item("Emblem Piece (Statue)"))
            self.multiworld.get_location("Hollow Bastion Entrance Hall Emblem Piece (Fountain)", self.player).place_locked_item(self.create_item("Emblem Piece (Fountain)"))
            self.multiworld.get_location("Hollow Bastion Entrance Hall Emblem Piece (Chest)", self.player).place_locked_item(self.create_item("Emblem Piece (Chest)"))

    def get_filler_item_name(self) -> str:
        fillers = {}
        disclude = []
        fillers.update(get_items_by_category("Item", disclude))
        fillers.update(get_items_by_category("Camping", disclude))
        fillers.update(get_items_by_category("Stat Ups", disclude))
        weights = [data.weight for data in fillers.values()]
        return self.random.choices([filler for filler in fillers.keys()], weights, k=1)[0]

    def fill_slot_data(self) -> dict:
        slot_data = {"xpmult": int(self.options.exp_multiplier)/16,
                    "required_reports_eotw": self.determine_reports_required_to_open_end_of_the_world(),
                    "required_reports_door": self.determine_reports_required_to_open_final_rest_door(),
                    "door": self.options.final_rest_door.current_key,
                    "seed": self.multiworld.seed_name,
                    "advanced_logic": bool(self.options.advanced_logic),
                    "hundred_acre_wood": bool(self.options.hundred_acre_wood),
                    "atlantica": bool(self.options.atlantica),
                    "goal": str(self.options.goal.current_key)}
        if self.options.randomize_keyblade_stats:
            min_str_bonus = min(self.options.keyblade_min_str, self.options.keyblade_max_str)
            max_str_bonus = max(self.options.keyblade_min_str, self.options.keyblade_max_str)
            min_mp_bonus = min(self.options.keyblade_min_mp, self.options.keyblade_max_mp)
            max_mp_bonus = max(self.options.keyblade_min_mp, self.options.keyblade_max_mp)
            slot_data["keyblade_stats"] = ""
            for i in range(22):
                if i < 4 and self.options.bad_starting_weapons:
                    slot_data["keyblade_stats"] = slot_data["keyblade_stats"] + "1,0,"
                else:
                    if min_str_bonus != max_str_bonus:
                        str_bonus = int(self.random.randrange(min_str_bonus,max_str_bonus))
                    else:
                        str_bonus = int(min_str_bonus)
                    if min_mp_bonus != max_mp_bonus:
                        mp_bonus = int(self.random.randrange(min_mp_bonus,max_mp_bonus))
                    else:
                        mp_bonus = int(min_mp_bonus)
                    slot_data["keyblade_stats"] = slot_data["keyblade_stats"] + str(str_bonus) + "," + str(mp_bonus) + ","
            slot_data["keyblade_stats"] = slot_data["keyblade_stats"][:-1]
        if self.options.donald_death_link:
            slot_data["donalddl"] = ""
        if self.options.goofy_death_link:
            slot_data["goofydl"] = ""
        if self.options.keyblades_unlock_chests:
            slot_data["chestslocked"] = ""
        else:
            slot_data["chestsunlocked"] = ""
        if self.options.interact_in_battle:
            slot_data["interactinbattle"] = ""
        return slot_data
    
    def create_item(self, name: str) -> KH1Item:
        data = item_table[name]
        return KH1Item(name, data.classification, data.code, self.player)

    def create_event(self, name: str) -> KH1Item:
        data = event_item_table[name]
        return KH1Item(name, data.classification, data.code, self.player)

    def set_rules(self):
        set_rules(self)

    def create_regions(self):
        create_regions(self.multiworld, self.player, self.options)
    
    def get_numbers_of_reports_to_consider(self) -> List[int]:
        numbers_to_consider = []
        if self.options.end_of_the_world_unlock.current_key == "reports":
            numbers_to_consider.append(self.options.required_reports_eotw.value)
        if self.options.final_rest_door.current_key == "reports":
            numbers_to_consider.append(self.options.required_reports_door.value)
        if self.options.final_rest_door.current_key == "reports" or self.options.end_of_the_world_unlock.current_key == "reports":
            numbers_to_consider.append(self.options.reports_in_pool.value)
        numbers_to_consider.sort()
        return numbers_to_consider
    
    def determine_reports_in_pool(self) -> int:
        numbers_to_consider = self.get_numbers_of_reports_to_consider()
        if len(numbers_to_consider) > 0:
            return max(numbers_to_consider)
        else:
            return 0
    
    def determine_reports_required_to_open_end_of_the_world(self) -> int:
        if self.options.end_of_the_world_unlock.current_key == "reports":
            numbers_to_consider = self.get_numbers_of_reports_to_consider()
            if len(numbers_to_consider) > 0:
                return numbers_to_consider[0]
        return 14
    
    def determine_reports_required_to_open_final_rest_door(self) -> int:
        if self.options.final_rest_door.current_key == "reports":
            numbers_to_consider = self.get_numbers_of_reports_to_consider()
            if len(numbers_to_consider) == 3:
                return numbers_to_consider[1]
            elif len(numbers_to_consider) == 2:
                return numbers_to_consider[0]
        return 14
        