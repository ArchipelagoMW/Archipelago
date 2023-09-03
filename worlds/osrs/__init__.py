from BaseClasses import Item, Tutorial, ItemClassification, Region, Entrance, CollectionState
from worlds.AutoWorld import WebWorld, World
from worlds.generic.Rules import add_rule
from .Items import OSRSItem, starting_area_dict, chunksanity_starting_chunks, QP_Items
from .Locations import OSRSLocation

from .Options import OSRSOptions, StartingArea
from .Names import LocationNames, ItemNames, RegionNames
from .LogicCSVParser import load_location_csv, load_region_csv, load_resource_csv, load_item_csv


class OSRSWeb(WebWorld):
    theme = "stone"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Oldschool Runescape Randomizer connected to an Archipelago Multiworld",
        "English",
        "docs/setup_en.md",
        "setup/en",
        ["digiholic"]
    )
    tutorials = [setup_en]


class OSRSWorld(World):
    game = "Old School Runescape"
    option_definitions = OSRSOptions
    topology_present = True
    web = OSRSWeb()
    base_id = 0x070000
    data_version = 0

    location_rows = load_location_csv()
    region_rows = load_region_csv()
    resource_rows = load_resource_csv()
    item_rows = load_item_csv()

    # Don't worry, the load_X_csv functions are cached. It just gets the list it generated the first time
    item_name_to_id = {load_item_csv()[i].name: 0x070000 + i for i in range(len(load_item_csv()))}
    location_name_to_id = {load_location_csv()[i].name: 0x070000 + i for i in range(len(load_location_csv()))}

    region_name_to_data = {}
    location_name_to_data = {}

    location_rows_by_name = {}
    region_rows_by_name = {}
    resource_rows_by_name = {}
    item_rows_by_name = {}

    starting_area_item = ""
    allow_brutal_grinds = False

    local_item_pool = []
    location_categories = {}
    locations_by_category = {}

    def generate_early(self) -> None:
        self.location_categories = {location_row.category for location_row in load_location_csv()}
        self.locations_by_category = {category:
            [location_row for location_row in self.location_rows if location_row.category == category]
            for category in self.location_categories}

        self.location_rows_by_name = {loc_row.name: loc_row for loc_row in self.location_rows}
        self.region_rows_by_name = {reg_row.name: reg_row for reg_row in self.region_rows}
        self.resource_rows_by_name = {rec_row.name: rec_row for rec_row in self.resource_rows}
        self.item_rows_by_name = {it_row.name: it_row for it_row in self.item_rows}

        rnd = self.multiworld.per_slot_randoms[self.player]
        starting_area = self.multiworld.starting_area[self.player]
        self.allow_brutal_grinds = self.multiworld.brutal_grinds[self.player]

        if starting_area.value == StartingArea.option_any_bank:
            random_bank = rnd.randint(0, len(starting_area_dict) - 1)
            self.starting_area_item = starting_area_dict[random_bank]
        elif starting_area.value < StartingArea.option_chunksanity:
            self.starting_area_item = starting_area_dict[starting_area.value]
        else:
            chunksanity_random = rnd.randint(0, len(chunksanity_starting_chunks) - 1)
            self.starting_area_item = chunksanity_starting_chunks[chunksanity_random]

        # Set Starting Chunk
        starting_index = [i for i in range(0, len(self.item_rows)) if self.item_rows[i].name == self.starting_area_item][0]
        self.multiworld.push_precollected(self.create_item(starting_index))

    def create_regions(self) -> None:
        """
        called to place player's regions into the MultiWorld's regions list. If it's hard to separate, this can be done
        during generate_early or basic as well.
        """

        # First, create the "Menu" region to start
        menu_region = self.create_region("Menu")

        for region_row in self.region_rows:
            self.create_region(region_row.name)

        for resource_row in self.resource_rows:
            self.create_region(resource_row.name)

        # Removes the word "Area: " from the item name to get the region it applies to.
        # I figured tacking "Area: " at the beginning would make it _easier_ to tell apart. Turns out it made it worse
        starting_area_region = self.starting_area_item[len("Area: "):]
        starting_entrance = menu_region.create_exit(f"Start->{starting_area_region}")
        starting_entrance.connect(self.region_name_to_data[starting_area_region])
        menu_region.exits.append(starting_entrance)

        # Create entrances between regions
        for region_row in self.region_rows:
            region = self.region_name_to_data[region_row.name]
            for outbound_region_name in region_row.connections:
                if "*" not in outbound_region_name:
                    entrance = region.create_exit(f"{region_row.name}->{outbound_region_name}")
                    item_name = self.region_rows_by_name[outbound_region_name]
                    entrance.access_rule = lambda state: state.has(item_name, self.player)
                    entrance.connect(self.region_name_to_data[outbound_region_name])
                    region.exits.append(entrance)
                else:
                    print(f"Special access rule needed for {outbound_region_name}")
            for resource_region in region_row.resources:
                if resource_region != "" and "*" not in resource_region:
                    entrance = region.create_exit(f"{region_row.name}->{resource_region}")
                    entrance.connect(self.region_name_to_data[resource_region])
                    region.exits.append(entrance)
                else:
                    print(f"Special access rule needed for {resource_region}")

    def roll_locations(self):
        locations_required = len(self.local_item_pool)
        locations_added = 0

        # Quests are always added
        for i in range(len(self.location_rows)):
            location_row = self.location_rows[i]
            if location_row.category == "Quest":
                self.create_and_add_location(i)
                locations_added += 1

        # Build up the weighted Task Pool
        rnd = self.multiworld.per_slot_randoms[self.player]

        # Start with the minimum general tasks
        general_tasks = [task for task in self.locations_by_category["General"]]
        if not self.multiworld.progressive_tasks[self.player]:
            rnd.shuffle(general_tasks)
        for i in range(0, self.multiworld.minimum_general_tasks):
            task = general_tasks.pop()
            self.add_location(task)
            locations_added += 1

        general_weight = self.multiworld.general_task_weight[self.player] if len(general_tasks > 0) else 0
        combat_tasks = [task for task in self.locations_by_category["Combat"]
                        if task.Skills[0].level <= self.max_combat_level]
        if not self.multiworld.progressive_tasks[self.player]:
            rnd.shuffle(combat_tasks)
        combat_tasks = combat_tasks[0:self.max_combat_tasks]
        combat_weight = self.multiworld.combat_task_weight[self.player] if len(combat_tasks) > 0 else 0
        prayer_tasks = [task for task in self.locations_by_category["Prayer"]
                        if task.Skills[0].level <= self.max_prayer_level]
        if not self.multiworld.progressive_tasks[self.player]:
            rnd.shuffle(prayer_tasks)
        prayer_tasks = prayer_tasks[0:self.max_prayer_tasks]
        prayer_weight = self.multiworld.prayer_task_weight[self.player] if len(prayer_tasks) > 0 else 0
        magic_tasks = [task for task in self.locations_by_category["Magic"]
                       if task.Skills[0].level <= self.max_magic_level]
        if not self.multiworld.progressive_tasks[self.player]:
            rnd.shuffle(magic_tasks)
        magic_tasks = magic_tasks[0:self.max_magic_tasks]
        magic_weight = self.multiworld.magic_task_weight[self.player] if len(magic_tasks) > 0 else 0
        runecraft_tasks = [task for task in self.locations_by_category["Runecraft"]
                           if task.Skills[0].level <= self.max_runecraft_level]
        if not self.multiworld.progressive_tasks[self.player]:
            rnd.shuffle(runecraft_tasks)
        runecraft_tasks = runecraft_tasks[0:self.max_runecraft_tasks]
        runecraft_weight = self.multiworld.runecraft_task_weight[self.player] if len(runecraft_tasks) > 0 else 0
        crafting_tasks = [task for task in self.locations_by_category["Crafting"]
                          if task.Skills[0].level <= self.max_crafting_level]
        if not self.multiworld.progressive_tasks[self.player]:
            rnd.shuffle(crafting_tasks)
        crafting_tasks = crafting_tasks[0:self.max_crafting_tasks]
        crafting_weight = self.multiworld.crafting_task_weight[self.player] if len(crafting_tasks) > 0 else 0
        mining_tasks = [task for task in self.locations_by_category["Mining"]
                        if task.Skills[0].level <= self.max_mining_level]
        if not self.multiworld.progressive_tasks[self.player]:
            rnd.shuffle(mining_tasks)
        mining_tasks = mining_tasks[0:self.max_mining_tasks]
        mining_weight = self.multiworld.mining_task_weight[self.player] if len(mining_tasks) > 0 else 0
        smithing_tasks = [task for task in self.locations_by_category["Smithing"]
                          if task.Skills[0].level <= self.max_smithing_level]
        if not self.multiworld.progressive_tasks[self.player]:
            rnd.shuffle(smithing_tasks)
        smithing_tasks = smithing_tasks[0:self.max_smithing_tasks]
        smithing_weight = self.multiworld.smithing_task_weight[self.player] if len(smithing_tasks) > 0 else 0
        fishing_tasks = [task for task in self.locations_by_category["Fishing"]
                         if task.Skills[0].level <= self.max_fishing_level]
        if not self.multiworld.progressive_tasks[self.player]:
            rnd.shuffle(fishing_tasks)
        fishing_tasks = fishing_tasks[0:self.max_fishing_tasks]
        fishing_weight = self.multiworld.fishing_task_weight[self.player] if len(fishing_tasks) > 0 else 0
        cooking_tasks = [task for task in self.locations_by_category["Cooking"]
                         if task.Skills[0].level <= self.max_cooking_level]
        if not self.multiworld.progressive_tasks[self.player]:
            rnd.shuffle(cooking_tasks)
        cooking_tasks = cooking_tasks[0:self.max_cooking_tasks]
        cooking_weight = self.multiworld.cooking_task_weight[self.player] if len(cooking_tasks) > 0 else 0
        firemaking_tasks = [task for task in self.locations_by_category["Firemaking"]
                            if task.Skills[0].level <= self.max_firemaking_level]
        if not self.multiworld.progressive_tasks[self.player]:
            rnd.shuffle(firemaking_tasks)
        firemaking_tasks = firemaking_tasks[0:self.max_firemaking_tasks]
        firemaking_weight = self.multiworld.firemaking_task_weight[self.player] if len(firemaking_tasks) > 0 else 0
        woodcutting_tasks = [task for task in self.locations_by_category["Woodcutting"]
                             if task.Skills[0].level <= self.max_woodcutting_level]
        if not self.multiworld.progressive_tasks[self.player]:
            rnd.shuffle(woodcutting_tasks)
        woodcutting_tasks = woodcutting_tasks[0:self.max_woodcutting_tasks]
        woodcutting_weight = self.multiworld.woodcutting_task_weight[self.player] if len(woodcutting_tasks) > 0 else 0

        total_weight = combat_weight + prayer_weight + magic_weight + runecraft_weight + \
                       crafting_weight + mining_weight + smithing_weight + fishing_weight + \
                       cooking_weight + firemaking_weight + woodcutting_weight + general_weight

        while locations_added < locations_required:
            random_roll = rnd.randint(0, total_weight)
            if random_roll < combat_weight:
                task = combat_tasks.pop()
                self.add_location(task)
                if len(combat_tasks) == 0:
                    total_weight -= combat_weight
                    combat_weight = 0
                locations_added += 1
                continue
            random_roll -= combat_weight
            if random_roll < prayer_weight:
                task = prayer_tasks.pop()
                self.add_location(task)
                if len(prayer_tasks) == 0:
                    total_weight -= prayer_weight
                    prayer_weight = 0
                locations_added += 1
                continue
            random_roll -= magic_weight
            if random_roll < magic_weight:
                task = magic_tasks.pop()
                self.add_location(task)
                if len(magic_tasks) == 0:
                    total_weight -= magic_weight
                    magic_weight = 0
                locations_added += 1
                continue
            random_roll -= magic_weight
            if random_roll < runecraft_weight:
                task = runecraft_tasks.pop()
                self.add_location(task)
                if len(runecraft_tasks) == 0:
                    total_weight -= runecraft_weight
                    runecraft_weight = 0
                locations_added += 1
                continue
            random_roll -= runecraft_weight
            if random_roll < crafting_weight:
                task = crafting_tasks.pop()
                self.add_location(task)
                if len(crafting_tasks) == 0:
                    total_weight -= crafting_weight
                    crafting_weight = 0
                locations_added += 1
                continue
            random_roll -= crafting_weight
            if random_roll < mining_weight:
                task = mining_tasks.pop()
                self.add_location(task)
                if len(mining_tasks) == 0:
                    total_weight -= mining_weight
                    mining_weight = 0
                locations_added += 1
                continue
            random_roll -= mining_weight
            if random_roll < smithing_weight:
                task = smithing_tasks.pop()
                self.add_location(task)
                if len(smithing_tasks) == 0:
                    total_weight -= smithing_weight
                    smithing_weight = 0
                locations_added += 1
                continue
            random_roll -= smithing_weight
            if random_roll < fishing_weight:
                task = fishing_tasks.pop()
                self.add_location(task)
                if len(fishing_tasks) == 0:
                    total_weight -= fishing_weight
                    fishing_weight = 0
                locations_added += 1
                continue
            random_roll -= fishing_weight
            if random_roll < cooking_weight:
                task = cooking_tasks.pop()
                self.add_location(task)
                if len(cooking_tasks) == 0:
                    total_weight -= cooking_weight
                    cooking_weight = 0
                locations_added += 1
                continue
            random_roll -= cooking_weight
            if random_roll < firemaking_weight:
                task = firemaking_tasks.pop()
                self.add_location(task)
                if len(firemaking_tasks) == 0:
                    total_weight -= firemaking_weight
                    firemaking_weight = 0
                locations_added += 1
                continue
            random_roll -= firemaking_weight
            if random_roll < woodcutting_weight:
                task = woodcutting_tasks.pop()
                self.add_location(task)
                if len(woodcutting_tasks) == 0:
                    total_weight -= woodcutting_weight
                    woodcutting_weight = 0
                locations_added += 1
                continue
            # If it hasn't hit anything else, add a general
            assert len(general_tasks) > 0, "There are not enough available tasks to fill the remaining pool for OSRS"
            task = general_tasks.pop()
            self.add_location(task)
            locations_added += 1

    def add_location(self, location):
        index = [i for i in range(0, len(self.location_rows)) if self.location_rows[i].name == location.name][0]
        self.create_and_add_location(index)

    def create_items(self) -> None:
        for i in range(len(self.item_rows)):
            item_row = self.item_rows[i]
            for c in range(item_row.count):
                item = self.create_item(i)
                self.multiworld.itempool.append(item)
                self.local_item_pool.append(item)

    def create_and_add_location(self, row_index) -> None:
        location_row = self.location_rows[row_index]

        # Create Location
        location = OSRSLocation(self.player, location_row.name, self.base_id + row_index)
        self.location_name_to_data[location_row.name] = location

        # Add the location to its first region, or if it doesn't belong to one, to Menu
        region = self.region_name_to_data["Menu"]
        if len(location_row.regions) > 0:
            region = self.region_name_to_data[location_row.regions[0]]
        location.parent_region = region
        region.locations.append(location)

        # Set up requirements for region
        for region_required_name in location_row.regions:
            region_required = self.region_name_to_data[region_required_name]
            add_rule(location, lambda state: state.can_reach(region_required, self.player))
            for skill_req in location_row.skills:
                add_rule(location, lambda state: self.can_reach_skill(state, skill_req.skill, skill_req.level))
            for item_req in location_row.items:
                add_rule(location, lambda state: state.has(item_req, self.player))
            if location_row.qp != 0:
                add_rule(location, lambda state: self.quest_points(state) > location_row.qp)

    def set_rules(self) -> None:
        """
        called to set access and item rules on locations and entrances.
        """
        # Place QP events
        self.multiworld.get_location(LocationNames.QP_Cooks_Assistant, self.player) \
            .place_locked_item(self.create_event(ItemNames.QP_Cooks_Assistant))
        self.multiworld.get_location(LocationNames.QP_Demon_Slayer, self.player) \
            .place_locked_item(self.create_event(ItemNames.QP_Demon_Slayer))
        self.multiworld.get_location(LocationNames.QP_Restless_Ghost, self.player) \
            .place_locked_item(self.create_event(ItemNames.QP_Restless_Ghost))
        self.multiworld.get_location(LocationNames.QP_Romeo_Juliet, self.player) \
            .place_locked_item(self.create_event(ItemNames.QP_Romeo_Juliet))
        self.multiworld.get_location(LocationNames.QP_Sheep_Shearer, self.player) \
            .place_locked_item(self.create_event(ItemNames.QP_Sheep_Shearer))
        self.multiworld.get_location(LocationNames.QP_Shield_of_Arrav, self.player) \
            .place_locked_item(self.create_event(ItemNames.QP_Shield_of_Arrav))
        self.multiworld.get_location(LocationNames.QP_Ernest_the_Chicken, self.player) \
            .place_locked_item(self.create_event(ItemNames.QP_Ernest_the_Chicken))
        self.multiworld.get_location(LocationNames.QP_Vampyre_Slayer, self.player) \
            .place_locked_item(self.create_event(ItemNames.QP_Vampyre_Slayer))
        self.multiworld.get_location(LocationNames.QP_Imp_Catcher, self.player) \
            .place_locked_item(self.create_event(ItemNames.QP_Imp_Catcher))
        self.multiworld.get_location(LocationNames.QP_Prince_Ali_Rescue, self.player) \
            .place_locked_item(self.create_event(ItemNames.QP_Prince_Ali_Rescue))
        self.multiworld.get_location(LocationNames.QP_Dorics_Quest, self.player) \
            .place_locked_item(self.create_event(ItemNames.QP_Dorics_Quest))
        self.multiworld.get_location(LocationNames.QP_Black_Knights_Fortress, self.player) \
            .place_locked_item(self.create_event(ItemNames.QP_Black_Knights_Fortress))
        self.multiworld.get_location(LocationNames.QP_Witchs_Potion, self.player) \
            .place_locked_item(self.create_event(ItemNames.QP_Witchs_Potion))
        self.multiworld.get_location(LocationNames.QP_Knights_Sword, self.player) \
            .place_locked_item(self.create_event(ItemNames.QP_Knights_Sword))
        self.multiworld.get_location(LocationNames.QP_Goblin_Diplomacy, self.player) \
            .place_locked_item(self.create_event(ItemNames.QP_Goblin_Diplomacy))
        self.multiworld.get_location(LocationNames.QP_Pirates_Treasure, self.player) \
            .place_locked_item(self.create_event(ItemNames.QP_Pirates_Treasure))
        self.multiworld.get_location(LocationNames.QP_Rune_Mysteries, self.player) \
            .place_locked_item(self.create_event(ItemNames.QP_Rune_Mysteries))
        self.multiworld.get_location(LocationNames.QP_Misthalin_Mystery, self.player) \
            .place_locked_item(self.create_event(ItemNames.QP_Misthalin_Mystery)),
        self.multiworld.get_location(LocationNames.QP_Corsair_Curse, self.player) \
            .place_locked_item(self.create_event(ItemNames.QP_Corsair_Curse))
        self.multiworld.get_location(LocationNames.QP_X_Marks_the_Spot, self.player) \
            .place_locked_item(self.create_event(ItemNames.QP_X_Marks_the_Spot))
        self.multiworld.get_location(LocationNames.QP_Below_Ice_Mountain, self.player) \
            .place_locked_item(self.create_event(ItemNames.QP_Below_Ice_Mountain))

        # Quest locations
        add_rule(self.multiworld.get_location(LocationNames.Q_Cooks_Assistant, self.player), lambda state: (
                state.can_reach(RegionNames.Lumbridge, None, self.player) and
                # Eggs
                state.can_reach(RegionNames.Egg, None, self.player) and
                state.can_reach(RegionNames.Wheat, None, self.player) and
                state.can_reach(RegionNames.Windmill, None, self.player) and
                state.can_reach(RegionNames.Milk, None, self.player)
        ))
        add_rule(self.multiworld.get_location(LocationNames.Q_Demon_Slayer, self.player), lambda state: (
                state.can_reach(RegionNames.Central_Varrock, None, self.player) and
                state.can_reach(RegionNames.Varrock_Palace, None, self.player) and
                state.can_reach(RegionNames.Wizards_Tower, None, self.player) and
                state.can_reach(RegionNames.South_Of_Varrock, None, self.player)
        ))
        add_rule(self.multiworld.get_location(LocationNames.Q_Restless_Ghost, self.player), lambda state: (
                state.can_reach(RegionNames.Lumbridge, None, self.player) and
                state.can_reach(RegionNames.Lumbridge_Swamp, None, self.player) and
                state.can_reach(RegionNames.Wizards_Tower, None, self.player)
        ))
        add_rule(self.multiworld.get_location(LocationNames.Q_Romeo_Juliet, self.player), lambda state: (
                state.can_reach(RegionNames.Central_Varrock, None, self.player) and
                state.can_reach(RegionNames.Varrock_Palace, None, self.player) and
                state.can_reach(RegionNames.South_Of_Varrock, None, self.player) and
                state.can_reach(RegionNames.West_Varrock, None, self.player)
        ))
        add_rule(self.multiworld.get_location(LocationNames.Q_Sheep_Shearer, self.player), lambda state: (
                state.can_reach(RegionNames.Lumbridge_Farms_West, None, self.player) and
                state.can_reach(RegionNames.Spinning_Wheel, None, self.player)
        ))
        add_rule(self.multiworld.get_location(LocationNames.Q_Shield_of_Arrav, self.player), lambda state: (
                state.can_reach(RegionNames.Central_Varrock, None, self.player) and
                state.can_reach(RegionNames.Varrock_Palace, None, self.player) and
                state.can_reach(RegionNames.South_Of_Varrock, None, self.player) and
                state.can_reach(RegionNames.West_Varrock, None, self.player)
        ))
        add_rule(self.multiworld.get_location(LocationNames.Q_Vampyre_Slayer, self.player), lambda state: (
                state.can_reach(RegionNames.Draynor_Village, None, self.player) and
                state.can_reach(RegionNames.Central_Varrock, None, self.player) and
                state.can_reach(RegionNames.Draynor_Manor, None, self.player)
        ))
        add_rule(self.multiworld.get_location(LocationNames.Q_Imp_Catcher, self.player), lambda state: (
                state.can_reach(RegionNames.Wizards_Tower, None, self.player) and
                state.can_reach(RegionNames.Imp, None, self.player)
        ))
        add_rule(self.multiworld.get_location(LocationNames.Q_Prince_Ali_Rescue, self.player), lambda state: (
                state.can_reach(RegionNames.Al_Kharid, None, self.player) and
                state.can_reach(RegionNames.Central_Varrock, None, self.player) and
                state.can_reach(RegionNames.Bronze_Ores, None, self.player) and
                state.can_reach(RegionNames.Clay_Rock, None, self.player) and
                state.can_reach(RegionNames.Sheep, None, self.player) and
                state.can_reach(RegionNames.Spinning_Wheel, None, self.player) and
                state.can_reach(RegionNames.Draynor_Village, None, self.player)
        ))
        add_rule(self.multiworld.get_location(LocationNames.Q_Black_Knights_Fortress, self.player), lambda state: (
                (state.can_reach(RegionNames.Edgeville, None, self.player) or
                 state.can_reach(RegionNames.Falador_Farm, None, self.player)) and
                state.has(ItemNames.Progressive_Armor, self.player) and
                state.can_reach(RegionNames.Falador, None, self.player) and
                state.can_reach(RegionNames.Monastery, None, self.player) and
                state.can_reach(RegionNames.Ice_Mountain, None, self.player) and
                self.quest_points(state) >= 12
        ))
        add_rule(self.multiworld.get_location(LocationNames.Q_Witchs_Potion, self.player), lambda state: (
                state.can_reach(RegionNames.Rimmington, None, self.player) and
                state.can_reach(RegionNames.Port_Sarim, None, self.player)
        ))
        add_rule(self.multiworld.get_location(LocationNames.Q_Knights_Sword, self.player), lambda state: (
                state.can_reach(RegionNames.Falador, None, self.player) and
                state.can_reach(RegionNames.Varrock_Palace, None, self.player) and
                state.can_reach(RegionNames.Mudskipper_Point, None, self.player) and
                state.can_reach(RegionNames.South_Of_Varrock, None, self.player) and
                (state.can_reach(RegionNames.Lumbridge_Farms_West, None, self.player) or state.can_reach(
                    RegionNames.West_Varrock, None, self.player))
        ))
        add_rule(self.multiworld.get_location(LocationNames.Q_Goblin_Diplomacy, self.player), lambda state: (
                state.can_reach(RegionNames.Ice_Mountain, None, self.player) and
                state.can_reach(RegionNames.Draynor_Village, None, self.player) and
                state.can_reach(RegionNames.Falador, None, self.player) and
                state.can_reach(RegionNames.South_Of_Varrock, None, self.player) and
                (state.can_reach(RegionNames.Lumbridge_Farms_West, None, self.player) or state.can_reach(
                    RegionNames.Rimmington, None, self.player))
        ))
        add_rule(self.multiworld.get_location(LocationNames.Q_Pirates_Treasure, self.player), lambda state: (
                state.can_reach(RegionNames.Port_Sarim, None, self.player) and
                state.can_reach(RegionNames.Karamja, None, self.player) and
                state.can_reach(RegionNames.Falador, None, self.player)
        ))
        add_rule(self.multiworld.get_location(LocationNames.Q_Rune_Mysteries, self.player), lambda state: (
                state.can_reach(RegionNames.Lumbridge, None, self.player) and
                state.can_reach(RegionNames.Wizards_Tower, None, self.player) and
                state.can_reach(RegionNames.Central_Varrock, None, self.player)
        ))
        add_rule(self.multiworld.get_location(LocationNames.Q_Corsair_Curse, self.player), lambda state: (
                state.can_reach(RegionNames.Falador_Farm, None, self.player) and
                state.can_reach(RegionNames.Corsair_Cove, None, self.player)
        ))
        add_rule(self.multiworld.get_location(LocationNames.Q_X_Marks_the_Spot, self.player), lambda state: (
                state.can_reach(RegionNames.Lumbridge, None, self.player) and
                state.can_reach(RegionNames.Draynor_Village, None, self.player) and
                state.can_reach(RegionNames.Port_Sarim, None, self.player)
        ))
        add_rule(self.multiworld.get_location(LocationNames.Q_Below_Ice_Mountain, self.player), lambda state: (
                state.can_reach(RegionNames.Dwarven_Mines, None, self.player) and
                state.can_reach(RegionNames.Ice_Mountain, None, self.player) and
                state.can_reach(RegionNames.Barbarian_Village, None, self.player) and
                state.can_reach(RegionNames.Falador, None, self.player) and
                state.can_reach(RegionNames.Central_Varrock, None, self.player) and
                state.can_reach(RegionNames.Edgeville, None, self.player) and
                self.quest_points(state) >= 16
        ))

        # QP Locations
        add_rule(self.multiworld.get_location(LocationNames.QP_Cooks_Assistant, self.player), lambda state: (
            self.multiworld.get_location(LocationNames.Q_Cooks_Assistant, self.player).can_reach(state)
        ))
        add_rule(self.multiworld.get_location(LocationNames.QP_Demon_Slayer, self.player), lambda state: (
            self.multiworld.get_location(LocationNames.Q_Demon_Slayer, self.player).can_reach(state)
        ))
        add_rule(self.multiworld.get_location(LocationNames.QP_Restless_Ghost, self.player), lambda state: (
            self.multiworld.get_location(LocationNames.Q_Restless_Ghost, self.player).can_reach(state)
        ))
        add_rule(self.multiworld.get_location(LocationNames.QP_Romeo_Juliet, self.player), lambda state: (
            self.multiworld.get_location(LocationNames.Q_Romeo_Juliet, self.player).can_reach(state)
        ))
        add_rule(self.multiworld.get_location(LocationNames.QP_Sheep_Shearer, self.player), lambda state: (
            self.multiworld.get_location(LocationNames.Q_Sheep_Shearer, self.player).can_reach(state)
        ))
        add_rule(self.multiworld.get_location(LocationNames.QP_Shield_of_Arrav, self.player), lambda state: (
            self.multiworld.get_location(LocationNames.Q_Shield_of_Arrav, self.player).can_reach(state)
        ))
        add_rule(self.multiworld.get_location(LocationNames.QP_Ernest_the_Chicken, self.player), lambda state: (
            self.multiworld.get_location(LocationNames.Q_Ernest_the_Chicken, self.player).can_reach(state)
        ))
        add_rule(self.multiworld.get_location(LocationNames.QP_Vampyre_Slayer, self.player), lambda state: (
            self.multiworld.get_location(LocationNames.Q_Vampyre_Slayer, self.player).can_reach(state)
        ))
        add_rule(self.multiworld.get_location(LocationNames.QP_Imp_Catcher, self.player), lambda state: (
            self.multiworld.get_location(LocationNames.Q_Imp_Catcher, self.player).can_reach(state)
        ))
        add_rule(self.multiworld.get_location(LocationNames.QP_Prince_Ali_Rescue, self.player), lambda state: (
            self.multiworld.get_location(LocationNames.Q_Prince_Ali_Rescue, self.player).can_reach(state)
        ))
        add_rule(self.multiworld.get_location(LocationNames.QP_Dorics_Quest, self.player), lambda state: (
            self.multiworld.get_location(LocationNames.Q_Dorics_Quest, self.player).can_reach(state)
        ))
        add_rule(self.multiworld.get_location(LocationNames.QP_Black_Knights_Fortress, self.player), lambda state: (
            self.multiworld.get_location(LocationNames.Q_Black_Knights_Fortress, self.player).can_reach(state)
        ))
        add_rule(self.multiworld.get_location(LocationNames.QP_Witchs_Potion, self.player), lambda state: (
            self.multiworld.get_location(LocationNames.Q_Witchs_Potion, self.player).can_reach(state)
        ))
        add_rule(self.multiworld.get_location(LocationNames.QP_Knights_Sword, self.player), lambda state: (
            self.multiworld.get_location(LocationNames.Q_Knights_Sword, self.player).can_reach(state)
        ))
        add_rule(self.multiworld.get_location(LocationNames.QP_Goblin_Diplomacy, self.player), lambda state: (
            self.multiworld.get_location(LocationNames.Q_Goblin_Diplomacy, self.player).can_reach(state)
        ))
        add_rule(self.multiworld.get_location(LocationNames.QP_Pirates_Treasure, self.player), lambda state: (
            self.multiworld.get_location(LocationNames.Q_Pirates_Treasure, self.player).can_reach(state)
        ))
        add_rule(self.multiworld.get_location(LocationNames.QP_Rune_Mysteries, self.player), lambda state: (
            self.multiworld.get_location(LocationNames.Q_Rune_Mysteries, self.player).can_reach(state)
        ))
        add_rule(self.multiworld.get_location(LocationNames.QP_Misthalin_Mystery, self.player), lambda state: (
            self.multiworld.get_location(LocationNames.Q_Misthalin_Mystery, self.player).can_reach(state)
        ))
        add_rule(self.multiworld.get_location(LocationNames.QP_Corsair_Curse, self.player), lambda state: (
            self.multiworld.get_location(LocationNames.Q_Corsair_Curse, self.player).can_reach(state)
        ))
        add_rule(self.multiworld.get_location(LocationNames.QP_X_Marks_the_Spot, self.player), lambda state: (
            self.multiworld.get_location(LocationNames.Q_X_Marks_the_Spot, self.player).can_reach(state)
        ))
        add_rule(self.multiworld.get_location(LocationNames.QP_Below_Ice_Mountain, self.player), lambda state: (
            self.multiworld.get_location(LocationNames.Q_Below_Ice_Mountain, self.player).can_reach(state)
        ))

        # Other locations
        add_rule(self.multiworld.get_location(LocationNames.Guppy, self.player), lambda state: (
            state.has(ItemNames.QP_Below_Ice_Mountain, self.player)
        ))
        add_rule(self.multiworld.get_location(LocationNames.Cavefish, self.player), lambda state: (
            state.has(ItemNames.QP_Below_Ice_Mountain, self.player)
        ))
        add_rule(self.multiworld.get_location(LocationNames.Tetra, self.player), lambda state: (
            state.has(ItemNames.QP_Below_Ice_Mountain, self.player)
        ))
        add_rule(self.multiworld.get_location(LocationNames.Barronite_Deposit, self.player), lambda state: (
            state.has(ItemNames.QP_Below_Ice_Mountain, self.player)
        ))
        add_rule(self.multiworld.get_location(LocationNames.Catch_Lobster, self.player), lambda state: (
                state.can_reach(RegionNames.Port_Sarim, None, self.player) and
                state.can_reach(RegionNames.Lobster, None, self.player)
        ))
        add_rule(self.multiworld.get_location(LocationNames.Smelt_Silver, self.player), lambda state: (
                self.multiworld.get_location(LocationNames.Mine_Silver, self.player).can_reach(state) and
                state.can_reach(RegionNames.Furnace, None, self.player)
        ))
        add_rule(self.multiworld.get_location(LocationNames.Smelt_Steel, self.player), lambda state: (
                self.multiworld.get_location(LocationNames.Mine_Coal, self.player).can_reach(state) and
                state.can_reach(RegionNames.Iron_Rock, None, self.player) and
                state.can_reach(RegionNames.Furnace, None, self.player)
        ))
        add_rule(self.multiworld.get_location(LocationNames.Smelt_Gold, self.player), lambda state: (
                self.multiworld.get_location(LocationNames.Mine_Gold, self.player).can_reach(state) and
                state.can_reach(RegionNames.Furnace, None, self.player)
        ))
        add_rule(self.multiworld.get_location(LocationNames.Bake_Apple_Pie, self.player), lambda state: (
                state.can_reach(RegionNames.Wheat, None, self.player) and
                state.can_reach(RegionNames.Windmill, None, self.player) and
                state.can_reach(RegionNames.West_Varrock, None, self.player) and
                state.can_reach(RegionNames.Imp, None, self.player)
        ))
        add_rule(self.multiworld.get_location(LocationNames.Bake_Cake, self.player), lambda state: (
                state.can_reach(RegionNames.Wheat, None, self.player) and
                state.can_reach(RegionNames.Egg, None, self.player) and
                state.can_reach(RegionNames.Milk, None, self.player) and
                state.can_reach(RegionNames.Windmill, None, self.player)
        ))
        add_rule(self.multiworld.get_location(LocationNames.Bake_Meat_Pizza, self.player), lambda state: (
                state.can_reach(RegionNames.Wheat, None, self.player) and
                state.can_reach(RegionNames.Windmill, None, self.player)
        ))
        add_rule(self.multiworld.get_location(LocationNames.K_Lesser_Demon, self.player), lambda state: (
                state.can_reach(RegionNames.Wilderness, None, self.player) or
                state.can_reach(RegionNames.Crandor, None, self.player) or
                state.can_reach(RegionNames.Wizards_Tower, None, self.player) or
                state.can_reach(RegionNames.Karamja, None, self.player)
        ))

        # Put some of the later grinds behind some QP so it's not all front-loaded
        add_rule(self.multiworld.get_location(LocationNames.Total_Level_150, self.player), lambda state: (
                self.quest_points(state) >= 3
        ))
        add_rule(self.multiworld.get_location(LocationNames.Total_Level_200, self.player), lambda state: (
                self.quest_points(state) >= 5
        ))
        add_rule(self.multiworld.get_location(LocationNames.Combat_Level_15, self.player), lambda state: (
                self.quest_points(state) >= 3
        ))
        add_rule(self.multiworld.get_location(LocationNames.Combat_Level_25, self.player), lambda state: (
                self.quest_points(state) >= 8
        ))
        add_rule(self.multiworld.get_location(LocationNames.Total_XP_25000, self.player), lambda state: (
                self.quest_points(state) >= 3
        ))
        add_rule(self.multiworld.get_location(LocationNames.Total_XP_50000, self.player), lambda state: (
                self.quest_points(state) >= 5
        ))
        add_rule(self.multiworld.get_location(LocationNames.Total_XP_100000, self.player), lambda state: (
                self.quest_points(state) >= 12
        ))

        # place "Victory" at "Dragon Slayer" and set collection as win condition
        self.multiworld.get_location(LocationNames.Q_Dragon_Slayer, self.player) \
            .place_locked_item(self.create_event("Victory"))

        add_rule(self.multiworld.get_location(LocationNames.Q_Dragon_Slayer, self.player), lambda state: (
                self.quest_points(state) >= 32 and state.can_reach(RegionNames.Crandor, None, self.player)
        ))

        self.multiworld.completion_condition[self.player] = lambda state: (state.has("Victory", self.player))

    def create_region(self, name: str) -> "Region":
        region = Region(name, self.player, self.multiworld)
        self.region_name_to_data[name] = region
        self.multiworld.regions.append(region)
        return region

    def create_item(self, index: int) -> "Item":
        item = self.item_rows[index]
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

    def can_reach_skill(self, state, skill, level):
        if skill == "fishing":
            can_train = state.can_reach(RegionNames.Shrimp, None, self.player)
            if not self.allow_brutal_grinds:
                fishing_shop = state.can_reach(RegionNames.Port_Sarim, None, self.player)
                if level >= 5:
                    can_train = can_train and fishing_shop
                if level >= 20:
                    can_train = can_train and state.can_reach(RegionNames.Fly_Fish, None, self.player)
            return can_train
        if skill == "mining":
            can_train = state.can_reach(RegionNames.Bronze_Ores, None, self.player) or state.can_reach(
                RegionNames.Clay_Rock)
            if not self.allow_brutal_grinds:
                # Iron is the best way to train all the way to 99, so having access to iron is all you need
                if level >= 15:
                    can_train = can_train and state.can_reach(RegionNames.Iron_Rock, None, self.player)
            return can_train
        if skill == "woodcutting":
            # Trees are literally everywhere and you start with an axe
            if self.allow_brutal_grinds:
                return True
            else:
                can_train = True
                if level >= 15:
                    can_train = state.can_reach(RegionNames.Oak_Tree, None, self.player)
                if level >= 30:
                    can_train = can_train and state.can_reach(RegionNames.Willow_Tree, None, self.player)
                return can_train
        if skill == "smithing":
            can_train = state.can_reach(RegionNames.Bronze_Ores, None, self.player) and state.can_reach(
                RegionNames.Furnace, None, self.player)
            if not self.allow_brutal_grinds:
                if level < 15:
                    # The special bronze-only anvil in Lumbridge makes this a bit more tricky
                    can_train = can_train and state.can_reach(RegionNames.Anvil, None,
                                                              self.player) or state.can_reach(RegionNames.Lumbridge,
                                                                                              None, self.player)
                if level >= 15:
                    can_train = can_train and state.can_reach(RegionNames.Anvil, None,
                                                              self.player) and state.can_reach(
                        RegionNames.Iron_Rock, None, self.player)
                if level >= 30:
                    # We already know we can reach anvils and iron rocks from before. Just add coal for steel
                    can_train = can_train and state.can_reach(RegionNames.Coal_Rock, None, self.player)
            return can_train
        if skill == "crafting":
            # There are many ways to start training
            can_spin = state.can_reach(RegionNames.Sheep, None, self.player) and state.can_reach(
                RegionNames.Spinning_Wheel, None, self.player)
            can_pot = state.can_reach(RegionNames.Clay_Rock, None, self.player) and state.can_reach(
                RegionNames.Barbarian_Village, None, self.player)
            can_tan = state.can_reach(RegionNames.Milk, None, self.player) and state.can_reach(
                RegionNames.Al_Kharid, None, self.player)

            mould_access = state.can_reach(RegionNames.Al_Kharid, None, self.player) or state.can_reach(
                RegionNames.Rimmington, None, self.player)
            if self.allow_brutal_grinds:
                # Only force killing barbarians for moulds in brutal grinds
                mould_access = mould_access or state.can_reach(RegionNames.Barbarian_Village, None, self.player)
            can_silver = state.can_reach(RegionNames.Silver_Rock, None, self.player) and state.can_reach(
                RegionNames.Furnace, None, self.player) and mould_access
            can_gold = state.can_reach(RegionNames.Gold_Rock, None, self.player) and \
                       state.can_reach(RegionNames.Furnace, None, self.player) and mould_access

            can_train = can_spin or can_pot or can_tan
            if not self.allow_brutal_grinds:
                if level > 5:
                    can_tran = can_pot or can_tan or can_gold
                if level > 16:
                    can_train = can_tan or can_gold or can_silver
            return can_train
        if skill == "cooking":
            # Meat and Chicken can be found with milk and eggs.
            can_bread = state.can_reach(RegionNames.Wheat, None, self.player) and state.can_reach(
                RegionNames.Windmill, None, self.player)
            can_train = state.can_reach(RegionNames.Milk, None, self.player) or \
                        state.can_reach(RegionNames.Egg, None, self.player) or state.can_reach(
                RegionNames.Shrimp, None, self.player) or can_bread
            if not self.allow_brutal_grinds:
                if level > 15:
                    can_train = can_train and state.can_reach(RegionNames.Fly_Fish, None,
                                                              self.player) and self.can_reach_skill(state,
                                                                                                    "fishing", 20)
            return can_train
        print(f"Attempting to check for reaching level {level} in {skill} which does not have rules set so it's fine")
        return True
