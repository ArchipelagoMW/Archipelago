from BaseClasses import Item, Tutorial, ItemClassification, Region, Entrance, CollectionState, MultiWorld
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

    def __init__(self, world: MultiWorld, player: int):
        super().__init__(world, player)
        self.region_name_to_data = {}
        self.location_name_to_data = {}

        self.location_rows_by_name = {}
        self.region_rows_by_name = {}
        self.resource_rows_by_name = {}
        self.item_rows_by_name = {}

        self.starting_area_item = ""
        self.allow_brutal_grinds = False

        self.location_categories = {}
        self.locations_by_category = {}

    def generate_early(self) -> None:
        self.location_categories = {location_row.category for location_row in load_location_csv()}
        self.locations_by_category = {category:
                                          [location_row for location_row in self.location_rows if
                                           location_row.category == category]
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
        self.multiworld.push_precollected(self.create_item(self.starting_area_item))

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
        starting_entrance.access_rule = lambda state: state.has(self.starting_area_item, self.player)
        starting_entrance.connect(self.region_name_to_data[starting_area_region])

        # Create entrances between regions
        for region_row in self.region_rows:
            region = self.region_name_to_data[region_row.name]
            for outbound_region_name in region_row.connections:
                entrance = region.create_exit(f"{region_row.name}->{outbound_region_name.replace('*', '')}")
                if "*" not in outbound_region_name:
                    item_name = self.region_rows_by_name[outbound_region_name].itemReq
                    if "*" not in item_name:
                        entrance.access_rule = lambda state, item_name=item_name: state.has(item_name, self.player)
                    else:
                        self.generate_special_rules_for(entrance, region_row, outbound_region_name)
                else:
                    self.generate_special_rules_for(entrance, region_row, outbound_region_name)
                entrance.connect(self.region_name_to_data[outbound_region_name.replace('*', '')])
            for resource_region in region_row.resources:
                if resource_region != "":
                    entrance = region.create_exit(f"{region_row.name}->{resource_region.replace('*', '')}")
                    if "*" not in resource_region:
                        entrance.connect(self.region_name_to_data[resource_region])
                    else:
                        self.generate_special_rules_for(entrance, region_row, resource_region)
                        entrance.connect(self.region_name_to_data[resource_region.replace('*', '')])

        self.roll_locations()

    def generate_special_rules_for(self, entrance, region_row, outbound_region_name):
        # print(f"Special rules required to access region {outbound_region_name} from {region_row.name}")
        if outbound_region_name == "Cook's Guild":
            item_name = self.region_rows_by_name[outbound_region_name.replace('*', '')].itemReq
            entrance.access_rule = lambda state: state.has(item_name, self.player) and\
                self.can_reach_skill(state, "cooking", 32)
            return
        if outbound_region_name == "Crafting Guild":
            item_name = self.region_rows_by_name[outbound_region_name.replace('*', '')].itemReq
            entrance.access_rule = lambda state:  state.has(item_name, self.player) and\
                self.can_reach_skill(state, "crafting", 40)
            return
        if outbound_region_name == "Corsair Cove":
            item_name = self.region_rows_by_name[outbound_region_name].itemReq.replace('*', '')
            # Need to be able to start Corsair Curse in addition to having the item
            entrance.access_rule = lambda state: state.has(item_name, self.player) and \
                                                 state.can_reach(RegionNames.Falador_Farm, None, self.player)
            return
        if outbound_region_name == "Camdozaal*":
            item_name = self.region_rows_by_name[outbound_region_name.replace('*', '')].itemReq
            entrance.access_rule = lambda state:  state.has(item_name, self.player) and\
                state.has(ItemNames.QP_Below_Ice_Mountain, self.player)
            return
        if region_row.name == "Dwarven Mountain Pass" and outbound_region_name == "Anvil*":
            entrance.access_rule = lambda state: state.has(ItemNames.QP_Dorics_Quest, self.player)
            return

        print(f"Special rules required to access region {outbound_region_name} from {region_row.name}")

    def roll_locations(self):
        locations_required = 0
        for item_row in self.item_rows:
            locations_required += item_row.count

        locations_added = 1 # At this point we've already added the starting area, so we start at 1 instead of 0

        # Quests are always added
        for i in range(len(self.location_rows)):
            location_row = self.location_rows[i]
            if location_row.category in ["Quest", "Points", "Goal"]:
                self.create_and_add_location(i)
                if location_row.category == "Quest":
                    locations_added += 1

        # Build up the weighted Task Pool
        rnd = self.multiworld.per_slot_randoms[self.player]

        # Start with the minimum general tasks
        general_tasks = [task for task in self.locations_by_category["General"]]
        if not self.multiworld.progressive_tasks[self.player]:
            rnd.shuffle(general_tasks)
        for i in range(0, self.multiworld.minimum_general_tasks[self.player]):
            task = general_tasks.pop()
            self.add_location(task)
            locations_added += 1

        general_weight = self.multiworld.general_task_weight[self.player] if len(general_tasks) > 0 else 0
        combat_tasks = [task for task in self.locations_by_category["Combat"]
                        if task.skills[0].level <= int(self.multiworld.max_combat_level[self.player])]
        #if not self.multiworld.progressive_tasks[self.player]:
        rnd.shuffle(combat_tasks)
        combat_tasks = combat_tasks[0:self.multiworld.max_combat_tasks[self.player]]
        combat_weight = self.multiworld.combat_task_weight[self.player] if len(combat_tasks) > 0 else 0

        prayer_tasks = [task for task in self.locations_by_category["Prayer"]
                        if task.skills[0].level <= int(self.multiworld.max_prayer_level[self.player])]
        if not self.multiworld.progressive_tasks[self.player]:
            rnd.shuffle(prayer_tasks)
        prayer_tasks = prayer_tasks[0:self.multiworld.max_prayer_tasks[self.player]]
        prayer_weight = self.multiworld.prayer_task_weight[self.player] if len(prayer_tasks) > 0 else 0

        magic_tasks = [task for task in self.locations_by_category["Magic"]
                       if task.skills[0].level <= int(self.multiworld.max_magic_level[self.player])]
        if not self.multiworld.progressive_tasks[self.player]:
            rnd.shuffle(magic_tasks)
        magic_tasks = magic_tasks[0:self.multiworld.max_magic_tasks[self.player]]
        magic_weight = self.multiworld.magic_task_weight[self.player] if len(magic_tasks) > 0 else 0

        runecraft_tasks = [task for task in self.locations_by_category["Runecraft"]
                           if task.skills[0].level <= int(self.multiworld.max_runecraft_level[self.player])]
        if not self.multiworld.progressive_tasks[self.player]:
            rnd.shuffle(runecraft_tasks)
        runecraft_tasks = runecraft_tasks[0:self.multiworld.max_runecraft_tasks[self.player]]
        runecraft_weight = self.multiworld.runecraft_task_weight[self.player] if len(runecraft_tasks) > 0 else 0

        crafting_tasks = [task for task in self.locations_by_category["Crafting"]
                          if task.skills[0].level <= int(self.multiworld.max_crafting_level[self.player])]
        if not self.multiworld.progressive_tasks[self.player]:
            rnd.shuffle(crafting_tasks)
        crafting_tasks = crafting_tasks[0:self.multiworld.max_crafting_tasks[self.player]]
        crafting_weight = self.multiworld.crafting_task_weight[self.player] if len(crafting_tasks) > 0 else 0

        mining_tasks = [task for task in self.locations_by_category["Mining"]
                        if task.skills[0].level <= int(self.multiworld.max_mining_level[self.player])]
        if not self.multiworld.progressive_tasks[self.player]:
            rnd.shuffle(mining_tasks)
        mining_tasks = mining_tasks[0:self.multiworld.max_mining_tasks[self.player]]
        mining_weight = self.multiworld.mining_task_weight[self.player] if len(mining_tasks) > 0 else 0

        smithing_tasks = [task for task in self.locations_by_category["Smithing"]
                          if task.skills[0].level <= int(self.multiworld.max_smithing_level[self.player])]
        if not self.multiworld.progressive_tasks[self.player]:
            rnd.shuffle(smithing_tasks)
        smithing_tasks = smithing_tasks[0:self.multiworld.max_smithing_tasks[self.player]]
        smithing_weight = self.multiworld.smithing_task_weight[self.player] if len(smithing_tasks) > 0 else 0

        fishing_tasks = [task for task in self.locations_by_category["Fishing"]
                         if task.skills[0].level <= int(self.multiworld.max_fishing_level[self.player])]
        if not self.multiworld.progressive_tasks[self.player]:
            rnd.shuffle(fishing_tasks)
        fishing_tasks = fishing_tasks[0:self.multiworld.max_fishing_tasks[self.player]]
        fishing_weight = self.multiworld.fishing_task_weight[self.player] if len(fishing_tasks) > 0 else 0

        cooking_tasks = [task for task in self.locations_by_category["Cooking"]
                         if task.skills[0].level <= int(self.multiworld.max_cooking_level[self.player])]
        if not self.multiworld.progressive_tasks[self.player]:
            rnd.shuffle(cooking_tasks)
        cooking_tasks = cooking_tasks[0:self.multiworld.max_cooking_tasks[self.player]]
        cooking_weight = self.multiworld.cooking_task_weight[self.player] if len(cooking_tasks) > 0 else 0

        firemaking_tasks = [task for task in self.locations_by_category["Firemaking"]
                            if task.skills[0].level <= int(self.multiworld.max_firemaking_level[self.player])]
        if not self.multiworld.progressive_tasks[self.player]:
            rnd.shuffle(firemaking_tasks)
        firemaking_tasks = firemaking_tasks[0:self.multiworld.max_firemaking_tasks[self.player]]
        firemaking_weight = self.multiworld.firemaking_task_weight[self.player] if len(firemaking_tasks) > 0 else 0

        woodcutting_tasks = [task for task in self.locations_by_category["Woodcutting"]
                             if task.skills[0].level <= int(self.multiworld.max_woodcutting_level[self.player])]
        if not self.multiworld.progressive_tasks[self.player]:
            rnd.shuffle(woodcutting_tasks)
        woodcutting_tasks = woodcutting_tasks[0:self.multiworld.max_woodcutting_tasks[self.player]]
        woodcutting_weight = self.multiworld.woodcutting_task_weight[self.player] if len(woodcutting_tasks) > 0 else 0

        all_tasks = [
            combat_tasks,
            prayer_tasks,
            magic_tasks,
            runecraft_tasks,
            crafting_tasks,
            mining_tasks,
            smithing_tasks,
            fishing_tasks,
            cooking_tasks,
            firemaking_tasks,
            woodcutting_tasks,
            general_tasks
        ]
        all_weights = [
            combat_weight,
            prayer_weight,
            magic_weight,
            runecraft_weight,
            crafting_weight,
            mining_weight,
            smithing_weight,
            fishing_weight,
            cooking_weight,
            firemaking_weight,
            woodcutting_weight,
            general_weight
        ]

        while locations_added < locations_required:
            if all_tasks:
                chosen_task = rnd.choices(all_tasks, all_weights)[0]
                task = chosen_task.pop()
                if (len(chosen_task) == 0):
                    index = all_tasks.index(chosen_task)
                    del all_tasks[index]
                    del all_weights[index]

            else:
                # assert len(general_tasks) > 0, "There are not enough avaialbe tasks to vfill the remaining pool for OSRS"
                # task = general_tasks.pop()
                pass

            self.add_location(task)
            locations_added += 1

    def add_location(self, location):
        index = [i for i in range(0, len(self.location_rows)) if self.location_rows[i].name == location.name][0]
        self.create_and_add_location(index)

    def create_items(self) -> None:
        for item_row in self.item_rows:
            if item_row.name != self.starting_area_item:
                for c in range(item_row.count):
                    item = self.create_item(item_row.name)
                    self.multiworld.itempool.append(item)

    def create_and_add_location(self, row_index) -> None:
        location_row = self.location_rows[row_index]
        # print(f"Adding task {location_row.name}")

        # Create Location
        id = self.base_id + row_index
        if location_row.category == "Points" or location_row.category == "Goal":
            id = None
        location = OSRSLocation(self.player, location_row.name, id)
        self.location_name_to_data[location_row.name] = location

        # Add the location to its first region, or if it doesn't belong to one, to Menu
        region = self.region_name_to_data["Menu"]
        if len(location_row.regions) > 0:
            region = self.region_name_to_data[location_row.regions[0]]
        location.parent_region = region
        region.locations.append(location)

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

        # place "Victory" at "Dragon Slayer" and set collection as win condition
        self.multiworld.get_location(LocationNames.Q_Dragon_Slayer, self.player) \
            .place_locked_item(self.create_event("Victory"))

        for location_name, location in self.location_name_to_data.items():
            location_row = self.location_rows_by_name[location_name]
            # Set up requirements for region
            for region_required_name in location_row.regions:
                region_required = self.region_name_to_data[region_required_name]
                add_rule(location, lambda state, region_required=region_required: state.can_reach(region_required, None, self.player))
            for skill_req in location_row.skills:
                add_rule(location, lambda state, skill_req=skill_req: self.can_reach_skill(state, skill_req.skill, skill_req.level))
            for item_req in location_row.items:
                add_rule(location, lambda state, item_req=item_req: state.has(item_req, self.player))
            if location_row.qp != 0:
                add_rule(location, lambda state, location_row=location_row: self.quest_points(state) > location_row.qp)
        self.multiworld.completion_condition[self.player] = lambda state: (state.has("Victory", self.player))

    def create_region(self, name: str) -> "Region":
        region = Region(name, self.player, self.multiworld)
        self.region_name_to_data[name] = region
        self.multiworld.regions.append(region)
        return region

    def create_item(self, item_name: str) -> "Item":
        item = [item for item in self.item_rows if item.name == item_name][0]
        index = self.item_rows.index(item)
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
        if skill == "Fishing":
            can_train = state.can_reach(RegionNames.Shrimp, None, self.player)
            if not self.allow_brutal_grinds:
                fishing_shop = state.can_reach(RegionNames.Port_Sarim, None, self.player)
                if level >= 5:
                    can_train = can_train and fishing_shop
                if level >= 20:
                    can_train = can_train and state.can_reach(RegionNames.Fly_Fish, None, self.player)
            return can_train
        if skill == "Mining":
            can_train = state.can_reach(RegionNames.Bronze_Ores, None, self.player) or state.can_reach(
                RegionNames.Clay_Rock, None, self.player)
            if not self.allow_brutal_grinds:
                # Iron is the best way to train all the way to 99, so having access to iron is all you need
                if level >= 15:
                    can_train = can_train and state.can_reach(RegionNames.Iron_Rock, None, self.player)
            return can_train
        if skill == "Woodcutting":
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
        if skill == "Smithing":
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
        if skill == "Crafting":
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
        if skill == "Cooking":
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
        if skill == "Runecraft":
            return state.has(ItemNames.QP_Rune_Mysteries, self.player)
        if skill == "Magic":
            return state.can_reach(RegionNames.Mind_Runes, None, self.player)
        # If it's not listed here, it can be trained just fine without needing locations
        # print(f"Attempting to check for reaching level {level} in {skill} which does not have rules set so it's fine")
        return True
