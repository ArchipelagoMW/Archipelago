import typing

from BaseClasses import Item, Tutorial, ItemClassification, Region, MultiWorld
from worlds.AutoWorld import WebWorld, World
from worlds.generic.Rules import add_rule, CollectionRule
from .Items import OSRSItem, starting_area_dict, chunksanity_starting_chunks, QP_Items, ItemRow, \
    chunksanity_special_region_names
from .Locations import OSRSLocation, LocationRow

from .Options import OSRSOptions, StartingArea
from .Names import LocationNames, ItemNames, RegionNames

from .LogicCSV.LogicCSVToPython import data_csv_tag
from .LogicCSV.items_generated import item_rows
from .LogicCSV.locations_generated import location_rows
from .LogicCSV.regions_generated import region_rows
from .LogicCSV.resources_generated import resource_rows
from .Regions import RegionRow, ResourceRow


class OSRSWeb(WebWorld):
    theme = "stone"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Old School Runescape Randomizer connected to an Archipelago Multiworld",
        "English",
        "docs/setup_en.md",
        "setup/en",
        ["digiholic"]
    )
    tutorials = [setup_en]


class OSRSWorld(World):
    game = "Old School Runescape"
    options_dataclass = OSRSOptions
    options: OSRSOptions
    topology_present = True
    web = OSRSWeb()
    base_id = 0x070000
    data_version = 1

    item_name_to_id = {item_rows[i].name: 0x070000 + i for i in range(len(item_rows))}
    location_name_to_id = {location_rows[i].name: 0x070000 + i for i in range(len(location_rows))}

    region_name_to_data: typing.Dict[str, Region]
    location_name_to_data: typing.Dict[str, OSRSLocation]

    location_rows_by_name: typing.Dict[str, LocationRow]
    region_rows_by_name: typing.Dict[str, RegionRow]
    resource_rows_by_name: typing.Dict[str, ResourceRow]
    item_rows_by_name: typing.Dict[str, ItemRow]

    starting_area_item: str

    locations_by_category: typing.Dict[str, typing.List[LocationRow]]

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.region_name_to_data = {}
        self.location_name_to_data = {}

        self.location_rows_by_name = {}
        self.region_rows_by_name = {}
        self.resource_rows_by_name = {}
        self.item_rows_by_name = {}

        self.starting_area_item = ""

        self.locations_by_category = {}

    def generate_early(self) -> None:
        location_categories = [location_row.category for location_row in location_rows]
        self.locations_by_category = {category:
                                          [location_row for location_row in location_rows if
                                           location_row.category == category]
                                      for category in location_categories}

        self.location_rows_by_name = {loc_row.name: loc_row for loc_row in location_rows}
        self.region_rows_by_name = {reg_row.name: reg_row for reg_row in region_rows}
        self.resource_rows_by_name = {rec_row.name: rec_row for rec_row in resource_rows}
        self.item_rows_by_name = {it_row.name: it_row for it_row in item_rows}

        rnd = self.random
        starting_area = self.options.starting_area

        if starting_area.value == StartingArea.option_any_bank:
            self.starting_area_item = rnd.choice(starting_area_dict)
        elif starting_area.value < StartingArea.option_chunksanity:
            self.starting_area_item = starting_area_dict[starting_area.value]
        else:
            self.starting_area_item = rnd.choice(chunksanity_starting_chunks)

        # Set Starting Chunk
        self.multiworld.push_precollected(self.create_item(self.starting_area_item))

    """
    This function pulls from LogicCSVToPython so that it sends the correct tag of the repository to the client.
    _Make sure to update that value whenever the CSVs change!_
    """

    def fill_slot_data(self):
        data = self.options.as_dict("brutal_grinds")
        data["data_csv_tag"] = data_csv_tag
        return data

    def create_regions(self) -> None:
        """
        called to place player's regions into the MultiWorld's regions list. If it's hard to separate, this can be done
        during generate_early or basic as well.
        """

        # First, create the "Menu" region to start
        menu_region = self.create_region("Menu")

        for region_row in region_rows:
            self.create_region(region_row.name)

        for resource_row in resource_rows:
            self.create_region(resource_row.name)

        # Removes the word "Area: " from the item name to get the region it applies to.
        # I figured tacking "Area: " at the beginning would make it _easier_ to tell apart. Turns out it made it worse
        if self.starting_area_item in chunksanity_special_region_names:
            starting_area_region = chunksanity_special_region_names[self.starting_area_item]
        else:
            starting_area_region = self.starting_area_item[6:]  # len("Area: ")
        starting_entrance = menu_region.create_exit(f"Start->{starting_area_region}")
        starting_entrance.access_rule = lambda state: state.has(self.starting_area_item, self.player)
        starting_entrance.connect(self.region_name_to_data[starting_area_region])

        # Create entrances between regions
        for region_row in region_rows:
            region = self.region_name_to_data[region_row.name]

            for outbound_region_name in region_row.connections:
                parsed_outbound = outbound_region_name.replace('*', '')
                entrance = region.create_exit(f"{region_row.name}->{parsed_outbound}")
                entrance.connect(self.region_name_to_data[parsed_outbound])

                item_name = self.region_rows_by_name[parsed_outbound].itemReq
                if "*" not in outbound_region_name and "*" not in item_name:
                    entrance.access_rule = lambda state, item_name=item_name: state.has(item_name, self.player)
                    continue

                self.generate_special_rules_for(entrance, region_row, outbound_region_name)

            for resource_region in region_row.resources:
                if not resource_region:
                    continue

                entrance = region.create_exit(f"{region_row.name}->{resource_region.replace('*', '')}")
                if "*" not in resource_region:
                    entrance.connect(self.region_name_to_data[resource_region])
                else:
                    self.generate_special_rules_for(entrance, region_row, resource_region)
                    entrance.connect(self.region_name_to_data[resource_region.replace('*', '')])

        self.roll_locations()

    def generate_special_rules_for(self, entrance, region_row, outbound_region_name):
        # print(f"Special rules required to access region {outbound_region_name} from {region_row.name}")
        if outbound_region_name == RegionNames.Cooks_Guild:
            item_name = self.region_rows_by_name[outbound_region_name].itemReq.replace('*', '')
            cooking_level_rule = self.get_skill_rule("cooking", 32)
            entrance.access_rule = lambda state: state.has(item_name, self.player) and \
                                                 cooking_level_rule(state)
            return
        if outbound_region_name == RegionNames.Crafting_Guild:
            item_name = self.region_rows_by_name[outbound_region_name].itemReq.replace('*', '')
            crafting_level_rule = self.get_skill_rule("crafting", 40)
            entrance.access_rule = lambda state: state.has(item_name, self.player) and \
                                                 crafting_level_rule(state)
            return
        if outbound_region_name == RegionNames.Corsair_Cove:
            item_name = self.region_rows_by_name[outbound_region_name].itemReq.replace('*', '')
            # Need to be able to start Corsair Curse in addition to having the item
            entrance.access_rule = lambda state: state.has(item_name, self.player) and \
                                                 state.can_reach(RegionNames.Falador_Farm, "Region", self.player)
            self.multiworld.register_indirect_condition(
                self.multiworld.get_region(RegionNames.Falador_Farm, self.player), entrance)

            return
        if outbound_region_name == "Camdozaal*":
            item_name = self.region_rows_by_name[outbound_region_name.replace('*', '')].itemReq
            entrance.access_rule = lambda state: state.has(item_name, self.player) and \
                                                 state.has(ItemNames.QP_Below_Ice_Mountain, self.player)
            return
        if region_row.name == "Dwarven Mountain Pass" and outbound_region_name == "Anvil*":
            entrance.access_rule = lambda state: state.has(ItemNames.QP_Dorics_Quest, self.player)
            return
        # Special logic for canoes
        canoe_regions = [RegionNames.Lumbridge, RegionNames.South_Of_Varrock, RegionNames.Barbarian_Village,
                         RegionNames.Edgeville, RegionNames.Wilderness]
        if region_row.name in canoe_regions:
            # Skill rules for greater distances
            woodcutting_rule_d1 = self.get_skill_rule("woodcutting", 12)
            woodcutting_rule_d2 = self.get_skill_rule("woodcutting", 27)
            woodcutting_rule_d3 = self.get_skill_rule("woodcutting", 42)
            woodcutting_rule_all = self.get_skill_rule("woodcutting", 57)

            if region_row.name == RegionNames.Lumbridge:
                # Canoe Tree access for the Location
                if outbound_region_name == RegionNames.Canoe_Tree:
                    entrance.access_rule = \
                        lambda state: (state.can_reach_region(RegionNames.South_Of_Varrock, self.player)
                                       and woodcutting_rule_d1(state) and self.options.max_woodcutting_level >= 12) or \
                                      (state.can_reach_region(RegionNames.Barbarian_Village)
                                       and woodcutting_rule_d2(state) and self.options.max_woodcutting_level >= 27) or \
                                      (state.can_reach_region(RegionNames.Edgeville)
                                       and woodcutting_rule_d3(state) and self.options.max_woodcutting_level >= 42) or \
                                      (state.can_reach_region(RegionNames.Wilderness)
                                       and woodcutting_rule_all(state) and self.options.max_woodcutting_level >= 57)
                    self.multiworld.register_indirect_condition(
                        self.multiworld.get_region(RegionNames.South_Of_Varrock, self.player), entrance)
                    self.multiworld.register_indirect_condition(
                        self.multiworld.get_region(RegionNames.Barbarian_Village, self.player), entrance)
                    self.multiworld.register_indirect_condition(
                        self.multiworld.get_region(RegionNames.Edgeville, self.player), entrance)
                    self.multiworld.register_indirect_condition(
                        self.multiworld.get_region(RegionNames.Wilderness, self.player), entrance)
                # Access to other chunks based on woodcutting settings
                # South of Varrock does not need to be checked, because it's already adjacent
                if outbound_region_name == RegionNames.Barbarian_Village:
                    entrance.access_rule = lambda state: woodcutting_rule_d2(state) \
                                                         and self.options.max_woodcutting_level >= 27
                if outbound_region_name == RegionNames.Edgeville:
                    entrance.access_rule = lambda state: woodcutting_rule_d3(state) \
                                                         and self.options.max_woodcutting_level >= 42
                if outbound_region_name == RegionNames.Wilderness:
                    entrance.access_rule = lambda state: woodcutting_rule_all(state) \
                                                         and self.options.max_woodcutting_level >= 57

            if region_row.name == RegionNames.South_Of_Varrock:
                if outbound_region_name == RegionNames.Canoe_Tree:
                    entrance.access_rule = \
                        lambda state: (state.can_reach_region(RegionNames.Lumbridge, self.player)
                                       and woodcutting_rule_d1(state) and self.options.max_woodcutting_level >= 12) or \
                                      (state.can_reach_region(RegionNames.Barbarian_Village)
                                       and woodcutting_rule_d1(state) and self.options.max_woodcutting_level >= 12) or \
                                      (state.can_reach_region(RegionNames.Edgeville)
                                       and woodcutting_rule_d2(state) and self.options.max_woodcutting_level >= 27) or \
                                      (state.can_reach_region(RegionNames.Wilderness)
                                       and woodcutting_rule_d3(state) and self.options.max_woodcutting_level >= 42)
                    self.multiworld.register_indirect_condition(
                        self.multiworld.get_region(RegionNames.Lumbridge, self.player), entrance)
                    self.multiworld.register_indirect_condition(
                        self.multiworld.get_region(RegionNames.Barbarian_Village, self.player), entrance)
                    self.multiworld.register_indirect_condition(
                        self.multiworld.get_region(RegionNames.Edgeville, self.player), entrance)
                    self.multiworld.register_indirect_condition(
                        self.multiworld.get_region(RegionNames.Wilderness, self.player), entrance)
                # Access to other chunks based on woodcutting settings
                # Lumbridge does not need to be checked, because it's already adjacent
                if outbound_region_name == RegionNames.Barbarian_Village:
                    entrance.access_rule = lambda state: woodcutting_rule_d1(state) \
                                                         and self.options.max_woodcutting_level >= 12
                if outbound_region_name == RegionNames.Edgeville:
                    entrance.access_rule = lambda state: woodcutting_rule_d3(state) \
                                                         and self.options.max_woodcutting_level >= 27
                if outbound_region_name == RegionNames.Wilderness:
                    entrance.access_rule = lambda state: woodcutting_rule_all(state) \
                                                         and self.options.max_woodcutting_level >= 42
            if region_row.name == RegionNames.Barbarian_Village:
                if outbound_region_name == RegionNames.Canoe_Tree:
                    entrance.access_rule = \
                        lambda state: (state.can_reach_region(RegionNames.Lumbridge, self.player)
                                       and woodcutting_rule_d2(state) and self.options.max_woodcutting_level >= 27) or \
                                      (state.can_reach_region(RegionNames.South_Of_Varrock)
                                       and woodcutting_rule_d1(state) and self.options.max_woodcutting_level >= 12) or \
                                      (state.can_reach_region(RegionNames.Edgeville)
                                       and woodcutting_rule_d1(state) and self.options.max_woodcutting_level >= 12) or \
                                      (state.can_reach_region(RegionNames.Wilderness)
                                       and woodcutting_rule_d2(state) and self.options.max_woodcutting_level >= 27)
                    self.multiworld.register_indirect_condition(
                        self.multiworld.get_region(RegionNames.Lumbridge, self.player), entrance)
                    self.multiworld.register_indirect_condition(
                        self.multiworld.get_region(RegionNames.South_Of_Varrock, self.player), entrance)
                    self.multiworld.register_indirect_condition(
                        self.multiworld.get_region(RegionNames.Edgeville, self.player), entrance)
                    self.multiworld.register_indirect_condition(
                        self.multiworld.get_region(RegionNames.Wilderness, self.player), entrance)
                # Access to other chunks based on woodcutting settings
                if outbound_region_name == RegionNames.Lumbridge:
                    entrance.access_rule = lambda state: woodcutting_rule_d2(state) \
                                                         and self.options.max_woodcutting_level >= 27
                if outbound_region_name == RegionNames.South_Of_Varrock:
                    entrance.access_rule = lambda state: woodcutting_rule_d1(state) \
                                                         and self.options.max_woodcutting_level >= 12
                # Edgeville does not need to be checked, because it's already adjacent
                if outbound_region_name == RegionNames.Wilderness:
                    entrance.access_rule = lambda state: woodcutting_rule_d3(state) \
                                                         and self.options.max_woodcutting_level >= 42
            if region_row.name == RegionNames.Edgeville:
                if outbound_region_name == RegionNames.Canoe_Tree:
                    entrance.access_rule = \
                        lambda state: (state.can_reach_region(RegionNames.Lumbridge, self.player)
                                       and woodcutting_rule_d3(state) and self.options.max_woodcutting_level >= 42) or \
                                      (state.can_reach_region(RegionNames.South_Of_Varrock)
                                       and woodcutting_rule_d2(state) and self.options.max_woodcutting_level >= 27) or \
                                      (state.can_reach_region(RegionNames.Barbarian_Village)
                                       and woodcutting_rule_d1(state) and self.options.max_woodcutting_level >= 12) or \
                                      (state.can_reach_region(RegionNames.Wilderness)
                                       and woodcutting_rule_d1(state) and self.options.max_woodcutting_level >= 12)
                    self.multiworld.register_indirect_condition(
                        self.multiworld.get_region(RegionNames.Lumbridge, self.player), entrance)
                    self.multiworld.register_indirect_condition(
                        self.multiworld.get_region(RegionNames.South_Of_Varrock, self.player), entrance)
                    self.multiworld.register_indirect_condition(
                        self.multiworld.get_region(RegionNames.Barbarian_Village, self.player), entrance)
                    self.multiworld.register_indirect_condition(
                        self.multiworld.get_region(RegionNames.Wilderness, self.player), entrance)
                # Access to other chunks based on woodcutting settings
                if outbound_region_name == RegionNames.Lumbridge:
                    entrance.access_rule = lambda state: woodcutting_rule_d3(state) \
                                                         and self.options.max_woodcutting_level >= 42
                if outbound_region_name == RegionNames.South_Of_Varrock:
                    entrance.access_rule = lambda state: woodcutting_rule_d2(state) \
                                                         and self.options.max_woodcutting_level >= 27
                # Barbarian Village does not need to be checked, because it's already adjacent
                # Wilderness does not need to be checked, because it's already adjacent
            if region_row.name == RegionNames.Wilderness:
                if outbound_region_name == RegionNames.Canoe_Tree:
                    entrance.access_rule = \
                        lambda state: (state.can_reach_region(RegionNames.Lumbridge, self.player)
                                       and woodcutting_rule_all(state) and self.options.max_woodcutting_level >= 57) or \
                                      (state.can_reach_region(RegionNames.South_Of_Varrock)
                                       and woodcutting_rule_d3(state) and self.options.max_woodcutting_level >= 42) or \
                                      (state.can_reach_region(RegionNames.Barbarian_Village)
                                       and woodcutting_rule_d2(state) and self.options.max_woodcutting_level >= 27) or \
                                      (state.can_reach_region(RegionNames.Edgeville)
                                       and woodcutting_rule_d1(state) and self.options.max_woodcutting_level >= 12)
                    self.multiworld.register_indirect_condition(
                        self.multiworld.get_region(RegionNames.Lumbridge, self.player), entrance)
                    self.multiworld.register_indirect_condition(
                        self.multiworld.get_region(RegionNames.South_Of_Varrock, self.player), entrance)
                    self.multiworld.register_indirect_condition(
                        self.multiworld.get_region(RegionNames.Barbarian_Village, self.player), entrance)
                    self.multiworld.register_indirect_condition(
                        self.multiworld.get_region(RegionNames.Edgeville, self.player), entrance)
                # Access to other chunks based on woodcutting settings
                if outbound_region_name == RegionNames.Lumbridge:
                    entrance.access_rule = lambda state: woodcutting_rule_all(state) \
                                                         and self.options.max_woodcutting_level >= 57
                if outbound_region_name == RegionNames.South_Of_Varrock:
                    entrance.access_rule = lambda state: woodcutting_rule_d3(state) \
                                                         and self.options.max_woodcutting_level >= 42
                if outbound_region_name == RegionNames.Barbarian_Village:
                    entrance.access_rule = lambda state: woodcutting_rule_d2(state) \
                                                         and self.options.max_woodcutting_level >= 27
                # Edgeville does not need to be checked, because it's already adjacent

    def roll_locations(self):
        locations_required = 0
        generation_is_fake = hasattr(self.multiworld, "generation_is_fake")  # UT specific override
        for item_row in item_rows:
            locations_required += item_row.amount

        locations_added = 1  # At this point we've already added the starting area, so we start at 1 instead of 0

        # Quests are always added
        for i, location_row in enumerate(location_rows):
            if location_row.category in {"quest", "points", "goal"}:
                self.create_and_add_location(i)
                if location_row.category == "quest":
                    locations_added += 1

        # Build up the weighted Task Pool
        rnd = self.random

        # Start with the minimum general tasks
        general_tasks = [task for task in self.locations_by_category["general"]]
        if not self.options.progressive_tasks:
            rnd.shuffle(general_tasks)
        else:
            general_tasks.reverse()
        for i in range(self.options.minimum_general_tasks):
            task = general_tasks.pop()
            self.add_location(task)
            locations_added += 1

        general_weight = self.options.general_task_weight if len(general_tasks) > 0 else 0

        tasks_per_task_type: typing.Dict[str, typing.List[LocationRow]] = {}
        weights_per_task_type: typing.Dict[str, int] = {}

        task_types = ["prayer", "magic", "runecraft", "mining", "crafting",
                      "smithing", "fishing", "cooking", "firemaking", "woodcutting", "combat"]
        for task_type in task_types:
            max_level_for_task_type = getattr(self.options, f"max_{task_type}_level")
            max_amount_for_task_type = getattr(self.options, f"max_{task_type}_tasks")
            tasks_for_this_type = [task for task in self.locations_by_category[task_type]
                                   if task.skills[0].level <= max_level_for_task_type]
            if not self.options.progressive_tasks:
                rnd.shuffle(tasks_for_this_type)
            else:
                tasks_for_this_type.reverse()

            tasks_for_this_type = tasks_for_this_type[:max_amount_for_task_type]
            weight_for_this_type = getattr(self.options,
                                                       f"{task_type}_task_weight")
            if weight_for_this_type > 0 and tasks_for_this_type:
                tasks_per_task_type[task_type] = tasks_for_this_type
                weights_per_task_type[task_type] = weight_for_this_type

        # Build a list of collections and weights in a matching order for rnd.choices later
        all_tasks = []
        all_weights = []
        for task_type in task_types:
            if task_type in tasks_per_task_type:
                all_tasks.append(tasks_per_task_type[task_type])
                all_weights.append(weights_per_task_type[task_type])

        # Even after the initial forced generals, they can still be rolled randomly
        if general_weight > 0:
            all_tasks.append(general_tasks)
            all_weights.append(general_weight)

        while locations_added < locations_required or (generation_is_fake and len(all_tasks) > 0):
            if all_tasks:
                chosen_task = rnd.choices(all_tasks, all_weights)[0]
                if chosen_task:
                    task = chosen_task.pop()
                    self.add_location(task)
                    locations_added += 1

                # This isn't an else because chosen_task can become empty in the process of resolving the above block
                # We still want to clear this list out while we're doing that
                if not chosen_task:
                    index = all_tasks.index(chosen_task)
                    del all_tasks[index]
                    del all_weights[index]

            else:
                if len(general_tasks) == 0:
                    raise Exception(f"There are not enough available tasks to fill the remaining pool for OSRS " +
                                    f"Please adjust {self.player_name}'s settings to be less restrictive of tasks.")
                task = general_tasks.pop()
                self.add_location(task)
                locations_added += 1

    def add_location(self, location):
        index = [i for i in range(len(location_rows)) if location_rows[i].name == location.name][0]
        self.create_and_add_location(index)

    def create_items(self) -> None:
        for item_row in item_rows:
            if item_row.name != self.starting_area_item:
                for c in range(item_row.amount):
                    item = self.create_item(item_row.name)
                    self.multiworld.itempool.append(item)

    def get_filler_item_name(self) -> str:
        return self.random.choice(
            [ItemNames.Progressive_Armor, ItemNames.Progressive_Weapons, ItemNames.Progressive_Magic,
             ItemNames.Progressive_Tools, ItemNames.Progressive_Range_Armor, ItemNames.Progressive_Range_Weapon])

    def create_and_add_location(self, row_index) -> None:
        location_row = location_rows[row_index]
        # print(f"Adding task {location_row.name}")

        # Create Location
        location_id = self.base_id + row_index
        if location_row.category == "points" or location_row.category == "goal":
            location_id = None
        location = OSRSLocation(self.player, location_row.name, location_id)
        self.location_name_to_data[location_row.name] = location

        # Add the location to its first region, or if it doesn't belong to one, to Menu
        region = self.region_name_to_data["Menu"]
        if location_row.regions:
            region = self.region_name_to_data[location_row.regions[0]]
        location.parent_region = region
        region.locations.append(location)

    def set_rules(self) -> None:
        """
        called to set access and item rules on locations and entrances.
        """
        quest_attr_names = ["Cooks_Assistant", "Demon_Slayer", "Restless_Ghost", "Romeo_Juliet",
                            "Sheep_Shearer", "Shield_of_Arrav", "Ernest_the_Chicken", "Vampyre_Slayer",
                            "Imp_Catcher", "Prince_Ali_Rescue", "Dorics_Quest", "Black_Knights_Fortress",
                            "Witchs_Potion", "Knights_Sword", "Goblin_Diplomacy", "Pirates_Treasure",
                            "Rune_Mysteries", "Misthalin_Mystery", "Corsair_Curse", "X_Marks_the_Spot",
                            "Below_Ice_Mountain"]
        for qp_attr_name in quest_attr_names:
            loc_name = getattr(LocationNames, f"QP_{qp_attr_name}")
            item_name = getattr(ItemNames, f"QP_{qp_attr_name}")
            self.multiworld.get_location(loc_name, self.player) \
                .place_locked_item(self.create_event(item_name))

        for quest_attr_name in quest_attr_names:
            qp_loc_name = getattr(LocationNames, f"QP_{quest_attr_name}")
            q_loc_name = getattr(LocationNames, f"Q_{quest_attr_name}")
            add_rule(self.multiworld.get_location(qp_loc_name, self.player), lambda state, q_loc_name=q_loc_name: (
                self.multiworld.get_location(q_loc_name, self.player).can_reach(state)
            ))

        # place "Victory" at "Dragon Slayer" and set collection as win condition
        self.multiworld.get_location(LocationNames.Q_Dragon_Slayer, self.player) \
            .place_locked_item(self.create_event("Victory"))
        self.multiworld.completion_condition[self.player] = lambda state: (state.has("Victory", self.player))

        for location_name, location in self.location_name_to_data.items():
            location_row = self.location_rows_by_name[location_name]
            # Set up requirements for region
            for region_required_name in location_row.regions:
                region_required = self.region_name_to_data[region_required_name]
                add_rule(location,
                         lambda state, region_required=region_required: state.can_reach(region_required, "Region",
                                                                                        self.player))
            for skill_req in location_row.skills:
                add_rule(location, self.get_skill_rule(skill_req.skill, skill_req.level))
            for item_req in location_row.items:
                add_rule(location, lambda state, item_req=item_req: state.has(item_req, self.player))
            if location_row.qp:
                add_rule(location, lambda state, location_row=location_row: self.quest_points(state) > location_row.qp)

    def create_region(self, name: str) -> "Region":
        region = Region(name, self.player, self.multiworld)
        self.region_name_to_data[name] = region
        self.multiworld.regions.append(region)
        return region

    def create_item(self, item_name: str) -> "Item":
        items = [item for item in item_rows if item.name == item_name]
        assert len(items) > 0, f"No matching item found for name {item_name} for player {self.player_name}"
        item = items[0]
        index = item_rows.index(item)
        return OSRSItem(item.name, item.progression, self.base_id + index, self.player)

    def create_event(self, event: str):
        # while we are at it, we can also add a helper to create events
        return OSRSItem(event, ItemClassification.progression, None, self.player)

    def quest_points(self, state):
        qp = 0
        for qp_event in QP_Items:
            if state.has(qp_event, self.player):
                qp += int(qp_event[0])
        return qp

    """
    Ensures a target level can be reached with available resources
    """

    def get_skill_rule(self, skill, level) -> CollectionRule:
        if skill.lower() == "fishing":
            if self.options.brutal_grinds or level < 5:
                return lambda state: state.can_reach(RegionNames.Shrimp, "Region", self.player)
            if level < 20:
                return lambda state: state.can_reach(RegionNames.Shrimp, "Region", self.player) and \
                                     state.can_reach(RegionNames.Port_Sarim, "Region", self.player)
            else:
                return lambda state: state.can_reach(RegionNames.Shrimp, "Region", self.player) and \
                                     state.can_reach(RegionNames.Port_Sarim, "Region", self.player) and \
                                     state.can_reach(RegionNames.Fly_Fish, "Region", self.player)
        if skill.lower() == "mining":
            if self.options.brutal_grinds or level < 15:
                return lambda state: state.can_reach(RegionNames.Bronze_Ores, "Region", self.player) or \
                                     state.can_reach(RegionNames.Clay_Rock, "Region", self.player)
            else:
                # Iron is the best way to train all the way to 99, so having access to iron is all you need to check for
                return lambda state: (state.can_reach(RegionNames.Bronze_Ores, "Region", self.player) or
                                      state.can_reach(RegionNames.Clay_Rock, "Region", self.player)) and \
                                     state.can_reach(RegionNames.Iron_Rock, "Region", self.player)
        if skill.lower() == "woodcutting":
            if self.options.brutal_grinds or level < 15:
                # I've checked. There is not a single chunk in the f2p that does not have at least one normal tree.
                # Even the desert.
                return lambda state: True
            if level < 30:
                return lambda state: state.can_reach(RegionNames.Oak_Tree, "Region", self.player)
            else:
                return lambda state: state.can_reach(RegionNames.Oak_Tree, "Region", self.player) and \
                                     state.can_reach(RegionNames.Willow_Tree, "Region", self.player)
        if skill.lower() == "smithing":
            if self.options.brutal_grinds:
                return lambda state: state.can_reach(RegionNames.Bronze_Ores, "Region", self.player) and \
                                     state.can_reach(RegionNames.Furnace, "Region", self.player)
            if level < 15:
                # Lumbridge has a special bronze-only anvil. This is the only anvil of its type so it's not included
                # in the "Anvil" resource region. We still need to check for it though.
                return lambda state: state.can_reach(RegionNames.Bronze_Ores, "Region", self.player) and \
                                     state.can_reach(RegionNames.Furnace, "Region", self.player) and \
                                     (state.can_reach(RegionNames.Anvil, "Region", self.player) or
                                      state.can_reach(RegionNames.Lumbridge, "Region", self.player))
            if level < 30:
                # For levels between 15 and 30, the lumbridge anvil won't cut it. Only a real one will do
                return lambda state: state.can_reach(RegionNames.Bronze_Ores, "Region", self.player) and \
                                     state.can_reach(RegionNames.Iron_Rock, "Region", self.player) and \
                                     state.can_reach(RegionNames.Furnace, "Region", self.player) and \
                                     state.can_reach(RegionNames.Anvil, "Region", self.player)
            else:
                return lambda state: state.can_reach(RegionNames.Bronze_Ores, "Region", self.player) and \
                                     state.can_reach(RegionNames.Iron_Rock, "Region", self.player) and \
                                     state.can_reach(RegionNames.Coal_Rock, "Region", self.player) and \
                                     state.can_reach(RegionNames.Furnace, "Region", self.player) and \
                                     state.can_reach(RegionNames.Anvil, "Region", self.player)
        if skill.lower() == "crafting":
            # Crafting is really complex. Need a lot of sub-rules to make this even remotely readable
            def can_spin(state):
                return state.can_reach(RegionNames.Sheep, "Region", self.player) and \
                    state.can_reach(RegionNames.Spinning_Wheel, "Region", self.player)

            def can_pot(state):
                return state.can_reach(RegionNames.Clay_Rock, "Region", self.player) and \
                    state.can_reach(RegionNames.Barbarian_Village, "Region", self.player)

            def can_tan(state):
                return state.can_reach(RegionNames.Milk, "Region", self.player) and \
                    state.can_reach(RegionNames.Al_Kharid, "Region", self.player)

            def mould_access(state):
                return state.can_reach(RegionNames.Al_Kharid, "Region", self.player) or \
                    state.can_reach(RegionNames.Rimmington, "Region", self.player)

            def can_silver(state):

                return state.can_reach(RegionNames.Silver_Rock, "Region", self.player) and \
                    state.can_reach(RegionNames.Furnace, "Region", self.player) and mould_access(state)

            def can_gold(state):
                return state.can_reach(RegionNames.Gold_Rock, "Region", self.player) and \
                    state.can_reach(RegionNames.Furnace, "Region", self.player) and mould_access(state)

            if self.options.brutal_grinds or level < 5:
                return lambda state: can_spin(state) or can_pot(state) or can_tan(state)

            can_smelt_gold = self.get_skill_rule("smithing", 40)
            can_smelt_silver = self.get_skill_rule("smithing", 20)
            if level < 16:
                return lambda state: can_pot(state) or can_tan(state) or (can_gold(state) and can_smelt_gold(state))
            else:
                return lambda state: can_tan(state) or (can_silver(state) and can_smelt_silver(state)) or \
                                     (can_gold(state) and can_smelt_gold(state))
        if skill.lower() == "Cooking":
            if self.options.brutal_grinds or level < 15:
                return lambda state: state.can_reach(RegionNames.Milk, "Region", self.player) or \
                                     state.can_reach(RegionNames.Egg, "Region", self.player) or \
                                     state.can_reach(RegionNames.Shrimp, "Region", self.player) or \
                                     (state.can_reach(RegionNames.Wheat, "Region", self.player) and
                                      state.can_reach(RegionNames.Windmill, "Region", self.player))
            else:
                can_catch_fly_fish = self.get_skill_rule("fishing", 20)
                return lambda state: state.can_reach(RegionNames.Fly_Fish, "Region", self.player) and \
                                     can_catch_fly_fish(state) and \
                                     (state.can_reach(RegionNames.Milk, "Region", self.player) or
                                      state.can_reach(RegionNames.Egg, "Region", self.player) or
                                      state.can_reach(RegionNames.Shrimp, "Region", self.player) or
                                      (state.can_reach(RegionNames.Wheat, "Region", self.player) and
                                       state.can_reach(RegionNames.Windmill, "Region", self.player)))
        if skill.lower() == "runecraft":
            return lambda state: state.has(ItemNames.QP_Rune_Mysteries, self.player)
        if skill.lower() == "magic":
            return lambda state: state.can_reach(RegionNames.Mind_Runes, "Region", self.player)

        return lambda state: True
