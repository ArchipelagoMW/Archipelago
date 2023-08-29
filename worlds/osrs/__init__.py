import typing

from BaseClasses import Item, Tutorial, ItemClassification, Region, Entrance, CollectionState
from worlds.AutoWorld import WebWorld, World
from worlds.generic.Rules import add_rule
from .Items import OSRSItem
from .Locations import OSRSLocation

from .Options import OSRSOptions, StartingArea
from .Names import LocationNames, ItemNames, RegionNames
from .LogicCSVParser import load_logic_csvs, location_rows, resource_rows, region_rows, item_rows


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

    item_name_to_id = {name: data.id for name, data in item_table.items()}
    location_name_to_id = {loc_data.name: loc_data.id for loc_data in all_locations}

    #location_name_to_data = {loc_data.name: loc_data for loc_data in all_locations}

    region_name_to_data = {}
    location_name_to_data = {}

    location_rows_by_name = {}
    region_rows_by_name = {}
    resource_rows_by_name = {}
    item_rows_by_name = {}

    starting_area_item = None
    allow_brutal_grinds = False

    def generate_early(self) -> None:
        # Load the lgic CSVs and set up the name-indexed dictionaries
        load_logic_csvs()
        self.location_rows_by_name = {loc_row.name: loc_row for loc_row in location_rows}
        self.region_rows_by_name = {reg_row.name: reg_row for reg_row in region_rows}
        self.resource_rows_by_name = {rec_row.name: rec_row for rec_row in resource_rows}
        self.item_rows_by_name = {it_row.name: it_row for it_row in item_rows}
        self.item_name_to_id = {location_rows[i].name: self.base_id + i for i in range(location_rows.count())}
        rnd = self.multiworld.per_slot_randoms[self.player]
        starting_area = self.multiworld.starting_area[self.player]
        allow_brutal_grinds = self.multiworld.brutal_grinds[self.player]

        if starting_area.value < StartingArea.option_chunksanity:
            self.starting_area_item = starting_area_dict[starting_area.value]
        elif starting_area.value == StartingArea.option_any_bank:
            random_bank = rnd.randint(0, len(starting_area_dict) - 1)
            self.starting_area_item = starting_area_dict[random_bank]
        else:
            chunksanity_random = rnd.randint(0, len(chunksanity_starting_chunks) - 1)
            self.starting_area_item = chunksanity_starting_chunks[chunksanity_random]

        # Set Starting Chunk
        self.multiworld.push_precollected(self.create_item(self.starting_area_item.itemName))

    def create_regions(self) -> None:
        """
        called to place player's regions into the MultiWorld's regions list. If it's hard to separate, this can be done
        during generate_early or basic as well.
        """

        # First, create the "Menu" region to start
        self.create_region("Menu")

        for region_row in region_rows:
            self.create_region(region_row.name)

        for resource_row in resource_rows:
            self.create_region(resource_row.name)

        # Create entrances between regions
        for region_row in region_rows:
            region = self.region_name_to_data[region_row.name]
            for outbound_region_name in region_row.connections:
                if not "*" in outbound_region_name:
                    entrance = region.create_exit(f"{region_row.name}->{outbound_region_name}")
                    item_name = self.region_rows_by_name[outbound_region_name]
                    entrance.access_rule = lambda state: state.has(item_name, self.player)
                    entrance.connect(self.region_name_to_data[outbound_region_name])
                    region.exits.append(entrance)
                else:
                    print(f"Special access rule needed for {outbound_region_name}")
            for resource_region in region_row.resources:
                if not "*" in resource_region:
                    entrance = region.create_exit(f"{region_row.name}->{resource_region}")
                    entrance.connect(self.region_name_to_data[resource_region])
                    region.exits.append(entrance)
                else:
                    print(f"Special access rule needed for {resource_region}")

    def create_items(self) -> None:
        for i in range(item_rows.count()):
            item_row = item_rows[i]
            for c in range(item_row.count):
                self.multiworld.itempool.append(self.create_item(i))

    def create_locations(self) -> None:
        for i in range(location_rows.count()):
            location_row = location_rows[i]

            location = OSRSLocation(self.player, location_row.name, self.base_id + i)
            self.location_name_to_data[location_row.name] = location
            for region_required_name in location_row.regions:
                region_required = self.region_name_to_data[region_required_name]
                add_rule(location, lambda state: state.can_reach(region_required, self.player))
                for skill_req in location_row.skills:
                    skill_name, skill_val = skill_req.split(" ")
                    add_rule(location, lambda state: self.can_reach_skill(state, skill_name, int(skill_val)))
                for item_req in location_row.items:
                    add_rule(location, lambda state: state.has(item_req, self.player))
                if location_row.qp != 0:
                    add_rule(location, lambda state: self.quest_points(state) > location_row.qp)

    def add_location_to_region(self, location: OSRSLocation):
        location_row = self.location_rows_by_name[location.name]
        region = self.region_name_to_data["Menu"]
        if location_row.regions.count() > 0:
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
        item = item_rows[index]
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
