import typing

from BaseClasses import Item, Tutorial, ItemClassification, Region, MultiWorld, CollectionState
from Fill import fill_restrictive, FillError
from worlds.AutoWorld import WebWorld, World
from .Items import OSRSItem, starting_area_dict, chunksanity_starting_chunks, QP_Items, ItemRow, \
    chunksanity_special_region_names
from .Locations import OSRSLocation, LocationRow
from .Rules import *
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
    """
    The best retro fantasy MMORPG on the planet. Old School is RuneScape but… older! This is the open world you know and love, but as it was in 2007.
    The Randomizer takes the form of a Chunk-Restricted f2p Ironman that takes a brand new account up through defeating
    the Green Dragon of Crandor and earning a spot in the fabled Champion's Guild!
    """

    game = "Old School Runescape"
    options_dataclass = OSRSOptions
    options: OSRSOptions
    topology_present = True
    web = OSRSWeb()
    base_id = 0x070000
    data_version = 1
    explicit_indirect_conditions = False

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
    available_QP_locations: typing.List[str]

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
        self.available_QP_locations = []

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

        #UT specific override, if we are in normal gen, resolve starting area, we will get it from slot_data in UT
        if not hasattr(self.multiworld, "generation_is_fake"):
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
        data["starting_area"] = str(self.starting_area_item) #these aren't actually strings, they just play them on tv
        return data

    def interpret_slot_data(self, slot_data: typing.Dict[str, typing.Any]) -> None:
        if "starting_area" in slot_data:
            self.starting_area_item = slot_data["starting_area"]
            menu_region = self.multiworld.get_region("Menu",self.player)
            menu_region.exits.clear() #prevent making extra exits if players just reconnect to a differnet slot
            if self.starting_area_item in chunksanity_special_region_names:
                starting_area_region = chunksanity_special_region_names[self.starting_area_item]
            else:
                starting_area_region = self.starting_area_item[6:]  # len("Area: ")
            starting_entrance = menu_region.create_exit(f"Start->{starting_area_region}")
            starting_entrance.access_rule = lambda state: state.has(self.starting_area_item, self.player)
            starting_entrance.connect(self.region_name_to_data[starting_area_region])

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
        # if area hasn't been set, then we shouldn't connect it
        if self.starting_area_item != "":
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
                entrance.access_rule = lambda state, item_name=item_name.replace("*",""): state.has(item_name, self.player)
                generate_special_rules_for(entrance, region_row, outbound_region_name, self.player, self.options, self)

            for resource_region in region_row.resources:
                if not resource_region:
                    continue

                entrance = region.create_exit(f"{region_row.name}->{resource_region.replace('*', '')}")
                if "*" not in resource_region:
                    entrance.connect(self.region_name_to_data[resource_region])
                else:
                    entrance.connect(self.region_name_to_data[resource_region.replace('*', '')])
                generate_special_rules_for(entrance, region_row, resource_region, self.player, self.options, self)

        self.roll_locations()

    def task_within_skill_levels(self, skills_required):
        # Loop through each required skill. If any of its requirements are out of the defined limit, return false
        for skill in skills_required:
            max_level_for_skill = getattr(self.options, f"max_{skill.skill.lower()}_level")
            if skill.level > max_level_for_skill:
                return False
        return True

    def roll_locations(self):
        generation_is_fake = hasattr(self.multiworld, "generation_is_fake")  # UT specific override
        locations_required = 0
        for item_row in item_rows:
            # If it's a filler item, set it aside for later
            if item_row.progression == ItemClassification.filler:
                continue

            # If it starts with "Care Pack", only add it if Care Packs are enabled
            if item_row.name.startswith("Care Pack"):
                if not self.options.enable_carepacks:
                    continue
            locations_required += item_row.amount
        if self.options.enable_duds: locations_required += self.options.dud_count

        locations_added = 1  # At this point we've already added the starting area, so we start at 1 instead of 0

        # Quests are always added first, before anything else is rolled
        for i, location_row in enumerate(location_rows):
            if location_row.category in {"quest", "points", "goal"}:
                if self.task_within_skill_levels(location_row.skills):
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
            max_amount_for_task_type = getattr(self.options, f"max_{task_type}_tasks")
            tasks_for_this_type = [task for task in self.locations_by_category[task_type]
                                   if self.task_within_skill_levels(task.skills)]
            max_amount_for_task_type = min(max_amount_for_task_type, len(tasks_for_this_type))
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
        filler_items = []
        for item_row in item_rows:
            if item_row.name != self.starting_area_item:
                # If it's a filler item, set it aside for later
                if item_row.progression == ItemClassification.filler:
                    filler_items.append(item_row)
                    continue

                # If it starts with "Care Pack", only add it if Care Packs are enabled
                if item_row.name.startswith("Care Pack"):
                    if not self.options.enable_carepacks:
                        continue

                for c in range(item_row.amount):
                    item = self.create_item(item_row.name)
                    self.multiworld.itempool.append(item)
        if self.options.enable_duds:
            self.random.shuffle(filler_items)
            filler_items = filler_items[0:self.options.dud_count]
            for item_row in filler_items:
                item = self.create_item(item_row.name)
                self.multiworld.itempool.append(item)

    def get_filler_item_name(self) -> str:
        if self.options.enable_duds:
            return self.random.choice([item for item in item_rows if item.progression == ItemClassification.filler])
        else:
            return self.random.choice([ItemNames.Progressive_Weapons, ItemNames.Progressive_Magic,
                                       ItemNames.Progressive_Range_Weapon, ItemNames.Progressive_Armor,
                                       ItemNames.Progressive_Range_Armor, ItemNames.Progressive_Tools])

    def create_and_add_location(self, row_index) -> None:
        location_row = location_rows[row_index]

        # Quest Points are handled differently now, but in case this gets fed an older version of the data sheet,
        # the points might still be listed in a different row
        if location_row.category == "points":
            return

        # Create Location
        location_id = self.base_id + row_index
        if location_row.category == "goal":
            location_id = None
        location = OSRSLocation(self.player, location_row.name, location_id)
        self.location_name_to_data[location_row.name] = location

        # Add the location to its first region, or if it doesn't belong to one, to Menu
        region = self.region_name_to_data["Menu"]
        if location_row.regions:
            region = self.region_name_to_data[location_row.regions[0]]
        location.parent_region = region
        region.locations.append(location)

        # If it's a quest, generate a "Points" location we'll add an event to
        if location_row.category == "quest":
            points_name = location_row.name.replace("Quest:", "Points:")
            points_location = OSRSLocation(self.player, points_name)
            self.location_name_to_data[points_name] = points_location
            points_location.parent_region = region
            region.locations.append(points_location)

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

        for quest_attr_name in quest_attr_names:
            qp_loc_name = getattr(LocationNames, f"QP_{quest_attr_name}")
            qp_loc = self.location_name_to_data.get(qp_loc_name)

            q_loc_name = getattr(LocationNames, f"Q_{quest_attr_name}")
            q_loc = self.location_name_to_data.get(q_loc_name)

            # Checks to make sure the task is actually in the list before trying to create its rules
            if qp_loc and q_loc:
                # Create the QP Event Item
                item_name = getattr(ItemNames, f"QP_{quest_attr_name}")
                qp_loc.place_locked_item(self.create_event(item_name))

                # If a quest is excluded, don't actually consider it for quest point progression
                if q_loc_name not in self.options.exclude_locations:
                    self.available_QP_locations.append(item_name)

                # Set the access rule for the QP Location
                add_rule(qp_loc, lambda state, loc=q_loc: (loc.can_reach(state)))

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
                add_rule(location, get_skill_rule(skill_req.skill, skill_req.level, self.player, self.options))
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
        for qp_event in self.available_QP_locations:
            if state.has(qp_event, self.player):
                qp += int(qp_event[0])
        return qp

