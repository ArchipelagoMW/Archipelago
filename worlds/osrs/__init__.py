import typing

from BaseClasses import Item, Tutorial, ItemClassification, Region, Entrance, CollectionState
from worlds.AutoWorld import WebWorld, World

from .Regions import all_regions, regions_by_name
from .Items import OSRSItem, all_items, item_table, starting_area_dict, Location_Items, \
    chunksanity_starting_chunks, QP_Items
from .Locations import OSRSLocation, all_locations
from .Options import OSRSOptions
from .Names import LocationNames, ItemNames, RegionNames


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

    data_version = 1

    item_name_to_id = {name: data.id for name, data in item_table.items()}
    location_name_to_id = {loc_data.name: loc_data.id for loc_data in all_locations}

    starting_area_item = None
    allow_brutal_grinds = False

    def generate_early(self) -> None:
        rnd = self.multiworld.per_slot_randoms[self.player]
        starting_area = self.multiworld.starting_area[self.player]
        allow_brutal_grinds = self.multiworld.brutal_grinds[self.player]

        if starting_area.value < 8:
            self.starting_area_item = starting_area_dict[starting_area.value]
        elif starting_area.value == 8:
            random_bank = rnd.randint(0, 7)
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
        name_to_region: typing.Dict[str, Region] = {}
        # Gotta loop through once and make all the region objects
        for region_info in all_regions:
            region = Region(region_info.name, self.player, self.multiworld)
            for location in region_info.locations:
                loc = OSRSLocation(self.player, location, self.location_name_to_id.get(location, None), region)
                region.locations.append(loc)

            name_to_region[region_info.name] = region
            self.multiworld.regions.append(region)

        # Now set up the entrances and exits
        for region_info in all_regions:
            region = name_to_region[region_info.name]
            if region_info.name == "Menu":
                start_region = self.starting_area_item.unlocksRegion
                connection_region = name_to_region[start_region]
                entrance = Entrance(self.player, start_region, region)
                entrance.connect(connection_region)
                region.exits.append(entrance)
            else:
                exits = region_info.build_exits_dict()
                exit_rules: typing.Dict[str, typing.Callable[[CollectionState], bool]] = {}

                for connected_region in region_info.connects_to:
                    default_access_rule = regions_by_name[connected_region].access_rule(self.player)
                    # If there's extra rules, combine them with the region's global access rule
                    if connected_region in region_info.extra_conditions(self.player):
                        special_rule = region_info.extra_conditions(self.player)[connected_region]
                        exit_rules[connected_region] = lambda state: (
                                default_access_rule(state) and special_rule(state))
                    else:
                        # If there's no extra, the rule is whatever the target location's rule is
                        exit_rules[connected_region] = default_access_rule
                for resource_region in region_info.resources:
                    # Resource nodes have no rules to access unless they're in extra conditions
                    exit_rules[resource_region] = region_info.build_extra_condition(self.player, resource_region)

                region.add_exits(exits, exit_rules)

    def create_items(self) -> None:
        for item in all_items:
            if item.itemName is not self.starting_area_item.itemName:
                for i in range(item.count):
                    self.multiworld.itempool.append(self.create_item(item.itemName))

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
        self.multiworld.get_location(LocationNames.Q_Cooks_Assistant, self.player).access_rule = lambda state: (
                state.can_reach(RegionNames.Lumbridge, None, self.player) and
                # Eggs
                state.can_reach(RegionNames.Egg, None, self.player) and
                state.can_reach(RegionNames.Wheat, None, self.player) and
                state.can_reach(RegionNames.Windmill, None, self.player) and
                state.can_reach(RegionNames.Milk, None, self.player)
        )
        self.multiworld.get_location(LocationNames.Q_Demon_Slayer, self.player).access_rule = lambda state: (
                state.can_reach(RegionNames.Central_Varrock, None, self.player) and
                state.can_reach(RegionNames.Varrock_Palace, None, self.player) and
                state.can_reach(RegionNames.Wizards_Tower, None, self.player) and
                state.can_reach(RegionNames.South_Of_Varrock, None, self.player)
        )
        self.multiworld.get_location(LocationNames.Q_Restless_Ghost, self.player).access_rule = lambda state: (
                state.can_reach(RegionNames.Lumbridge, None, self.player) and
                state.can_reach(RegionNames.Lumbridge_Swamp, None, self.player) and
                state.can_reach(RegionNames.Wizards_Tower, None, self.player)
        )
        self.multiworld.get_location(LocationNames.Q_Romeo_Juliet, self.player).access_rule = lambda state: (
                state.can_reach(RegionNames.Central_Varrock, None, self.player) and
                state.can_reach(RegionNames.Varrock_Palace, None, self.player) and
                state.can_reach(RegionNames.South_Of_Varrock, None, self.player) and
                state.can_reach(RegionNames.West_Varrock, None, self.player)
        )
        self.multiworld.get_location(LocationNames.Q_Sheep_Shearer, self.player).access_rule = lambda state: (
                state.can_reach(RegionNames.Lumbridge_Farms, None, self.player) and
                state.can_reach(RegionNames.Spinning_Wheel, None, self.player)
        )
        self.multiworld.get_location(LocationNames.Q_Shield_of_Arrav, self.player).access_rule = lambda state: (
                state.can_reach(RegionNames.Central_Varrock, None, self.player) and
                state.can_reach(RegionNames.Varrock_Palace, None, self.player) and
                state.can_reach(RegionNames.South_Of_Varrock, None, self.player) and
                state.can_reach(RegionNames.West_Varrock, None, self.player)
        )
        self.multiworld.get_location(LocationNames.Q_Vampyre_Slayer, self.player).access_rule = lambda state: (
                state.can_reach(RegionNames.Draynor_Village, None, self.player) and
                state.can_reach(RegionNames.Central_Varrock, None, self.player) and
                state.can_reach(RegionNames.Draynor_Manor, None, self.player)
        )
        self.multiworld.get_location(LocationNames.Q_Imp_Catcher, self.player).access_rule = lambda state: (
                state.can_reach(RegionNames.Wizards_Tower, None, self.player) and
                state.can_reach(RegionNames.Imp, None, self.player)
        )
        self.multiworld.get_location(LocationNames.Q_Prince_Ali_Rescue, self.player).access_rule = lambda state: (
                state.can_reach(RegionNames.Al_Kharid, None, self.player) and
                state.can_reach(RegionNames.Central_Varrock, None, self.player) and
                state.can_reach(RegionNames.Bronze_Ores, None, self.player) and
                state.can_reach(RegionNames.Clay_Rock, None, self.player) and
                state.can_reach(RegionNames.Sheep, None, self.player) and
                state.can_reach(RegionNames.Spinning_Wheel, None, self.player) and
                state.can_reach(RegionNames.Draynor_Village, None, self.player)
        )
        self.multiworld.get_location(LocationNames.Q_Black_Knights_Fortress, self.player).access_rule = lambda state: (
                (state.can_reach(RegionNames.Edgeville, None, self.player) or
                 state.can_reach(RegionNames.Falador_Farm, None, self.player)) and
                state.has(ItemNames.Progressive_Armor, self.player) and
                state.can_reach(RegionNames.Falador, None, self.player) and
                state.can_reach(RegionNames.Monastery, None, self.player) and
                state.can_reach(RegionNames.Ice_Mountain, None, self.player) and
                self.quest_points(state) >= 12
        )
        self.multiworld.get_location(LocationNames.Q_Witchs_Potion, self.player).access_rule = lambda state: (
                state.can_reach(RegionNames.Rimmington, None, self.player) and
                state.can_reach(RegionNames.Port_Sarim, None, self.player)
        )
        self.multiworld.get_location(LocationNames.Q_Knights_Sword, self.player).access_rule = lambda state: (
                state.can_reach(RegionNames.Falador, None, self.player) and
                state.can_reach(RegionNames.Varrock_Palace, None, self.player) and
                state.can_reach(RegionNames.Mudskipper_Point, None, self.player) and
                state.can_reach(RegionNames.South_Of_Varrock, None, self.player) and
                (state.can_reach(RegionNames.Lumbridge_Farms, None, self.player) or state.can_reach(
                    RegionNames.West_Varrock, None, self.player))
        )
        self.multiworld.get_location(LocationNames.Q_Goblin_Diplomacy, self.player).access_rule = lambda state: (
                state.can_reach(RegionNames.Ice_Mountain, None, self.player) and
                state.can_reach(RegionNames.Draynor_Village, None, self.player) and
                state.can_reach(RegionNames.Falador, None, self.player) and
                state.can_reach(RegionNames.South_Of_Varrock, None, self.player) and
                (state.can_reach(RegionNames.Lumbridge_Farms, None, self.player) or state.can_reach(
                    RegionNames.Rimmington, None, self.player))
        )
        self.multiworld.get_location(LocationNames.Q_Pirates_Treasure, self.player).access_rule = lambda state: (
                state.can_reach(RegionNames.Port_Sarim, None, self.player) and
                state.can_reach(RegionNames.Karamja, None, self.player) and
                state.can_reach(RegionNames.Falador, None, self.player)
        )
        self.multiworld.get_location(LocationNames.Q_Rune_Mysteries, self.player).access_rule = lambda state: (
                state.can_reach(RegionNames.Lumbridge, None, self.player) and
                state.can_reach(RegionNames.Wizards_Tower, None, self.player) and
                state.can_reach(RegionNames.Central_Varrock, None, self.player)
        )
        self.multiworld.get_location(LocationNames.Q_Corsair_Curse, self.player).access_rule = lambda state: (
                state.can_reach(RegionNames.Falador_Farm, None, self.player) and
                state.can_reach(RegionNames.Corsair_Cove, None, self.player)
        )
        self.multiworld.get_location(LocationNames.Q_X_Marks_the_Spot, self.player).access_rule = lambda state: (
                state.can_reach(RegionNames.Lumbridge, None, self.player) and
                state.can_reach(RegionNames.Draynor_Village, None, self.player) and
                state.can_reach(RegionNames.Port_Sarim, None, self.player)
        )
        self.multiworld.get_location(LocationNames.Q_Below_Ice_Mountain, self.player).access_rule = lambda state: (
                state.can_reach(RegionNames.Dwarven_Mines, None, self.player) and
                state.can_reach(RegionNames.Ice_Mountain, None, self.player) and
                state.can_reach(RegionNames.Barbarian_Village, None, self.player) and
                state.can_reach(RegionNames.Falador, None, self.player) and
                state.can_reach(RegionNames.Central_Varrock, None, self.player) and
                state.can_reach(RegionNames.Edgeville, None, self.player) and
                self.quest_points(state) >= 16
        )

        # QP Locations
        self.multiworld.get_location(LocationNames.QP_Cooks_Assistant, self.player).access_rule = lambda state: (
            self.multiworld.get_location(LocationNames.Q_Cooks_Assistant, self.player).can_reach(state)
        )
        self.multiworld.get_location(LocationNames.QP_Demon_Slayer, self.player).access_rule = lambda state: (
            self.multiworld.get_location(LocationNames.Q_Demon_Slayer, self.player).can_reach(state)
        )
        self.multiworld.get_location(LocationNames.QP_Restless_Ghost, self.player).access_rule = lambda state: (
            self.multiworld.get_location(LocationNames.Q_Restless_Ghost, self.player).can_reach(state)
        )
        self.multiworld.get_location(LocationNames.QP_Romeo_Juliet, self.player).access_rule = lambda state: (
            self.multiworld.get_location(LocationNames.Q_Romeo_Juliet, self.player).can_reach(state)
        )
        self.multiworld.get_location(LocationNames.QP_Sheep_Shearer, self.player).access_rule = lambda state: (
            self.multiworld.get_location(LocationNames.Q_Sheep_Shearer, self.player).can_reach(state)
        )
        self.multiworld.get_location(LocationNames.QP_Shield_of_Arrav, self.player).access_rule = lambda state: (
            self.multiworld.get_location(LocationNames.Q_Shield_of_Arrav, self.player).can_reach(state)
        )
        self.multiworld.get_location(LocationNames.QP_Ernest_the_Chicken, self.player).access_rule = lambda state: (
            self.multiworld.get_location(LocationNames.Q_Ernest_the_Chicken, self.player).can_reach(state)
        )
        self.multiworld.get_location(LocationNames.QP_Vampyre_Slayer, self.player).access_rule = lambda state: (
            self.multiworld.get_location(LocationNames.Q_Vampyre_Slayer, self.player).can_reach(state)
        )
        self.multiworld.get_location(LocationNames.QP_Imp_Catcher, self.player).access_rule = lambda state: (
            self.multiworld.get_location(LocationNames.Q_Imp_Catcher, self.player).can_reach(state)
        )
        self.multiworld.get_location(LocationNames.QP_Prince_Ali_Rescue, self.player).access_rule = lambda state: (
            self.multiworld.get_location(LocationNames.Q_Prince_Ali_Rescue, self.player).can_reach(state)
        )
        self.multiworld.get_location(LocationNames.QP_Dorics_Quest, self.player).access_rule = lambda state: (
            self.multiworld.get_location(LocationNames.Q_Dorics_Quest, self.player).can_reach(state)
        )
        self.multiworld.get_location(LocationNames.QP_Black_Knights_Fortress, self.player).access_rule = lambda state: (
            self.multiworld.get_location(LocationNames.Q_Black_Knights_Fortress, self.player).can_reach(state)
        )
        self.multiworld.get_location(LocationNames.QP_Witchs_Potion, self.player).access_rule = lambda state: (
            self.multiworld.get_location(LocationNames.Q_Witchs_Potion, self.player).can_reach(state)
        )
        self.multiworld.get_location(LocationNames.QP_Knights_Sword, self.player).access_rule = lambda state: (
            self.multiworld.get_location(LocationNames.Q_Knights_Sword, self.player).can_reach(state)
        )
        self.multiworld.get_location(LocationNames.QP_Goblin_Diplomacy, self.player).access_rule = lambda state: (
            self.multiworld.get_location(LocationNames.Q_Goblin_Diplomacy, self.player).can_reach(state)
        )
        self.multiworld.get_location(LocationNames.QP_Pirates_Treasure, self.player).access_rule = lambda state: (
            self.multiworld.get_location(LocationNames.Q_Pirates_Treasure, self.player).can_reach(state)
        )
        self.multiworld.get_location(LocationNames.QP_Rune_Mysteries, self.player).access_rule = lambda state: (
            self.multiworld.get_location(LocationNames.Q_Rune_Mysteries, self.player).can_reach(state)
        )
        self.multiworld.get_location(LocationNames.QP_Misthalin_Mystery, self.player).access_rule = lambda state: (
            self.multiworld.get_location(LocationNames.Q_Misthalin_Mystery, self.player).can_reach(state)
        )
        self.multiworld.get_location(LocationNames.QP_Corsair_Curse, self.player).access_rule = lambda state: (
            self.multiworld.get_location(LocationNames.Q_Corsair_Curse, self.player).can_reach(state)
        )
        self.multiworld.get_location(LocationNames.QP_X_Marks_the_Spot, self.player).access_rule = lambda state: (
            self.multiworld.get_location(LocationNames.Q_X_Marks_the_Spot, self.player).can_reach(state)
        )
        self.multiworld.get_location(LocationNames.QP_Below_Ice_Mountain, self.player).access_rule = lambda state: (
            self.multiworld.get_location(LocationNames.Q_Below_Ice_Mountain, self.player).can_reach(state)
        )

        # Other locations
        self.multiworld.get_location(LocationNames.Guppy, self.player).access_rule = lambda state: (
            state.has(ItemNames.QP_Below_Ice_Mountain, self.player)
        )
        self.multiworld.get_location(LocationNames.Cavefish, self.player).access_rule = lambda state: (
            state.has(ItemNames.QP_Below_Ice_Mountain, self.player)
        )
        self.multiworld.get_location(LocationNames.Tetra, self.player).access_rule = lambda state: (
            state.has(ItemNames.QP_Below_Ice_Mountain, self.player)
        )
        self.multiworld.get_location(LocationNames.Barronite_Deposit, self.player).access_rule = lambda state: (
            state.has(ItemNames.QP_Below_Ice_Mountain, self.player)
        )
        self.multiworld.get_location(LocationNames.Catch_Lobster, self.player).access_rule = lambda state: (
                state.can_reach(RegionNames.Port_Sarim, None, self.player) and
                (state.can_reach(RegionNames.Karamja, None, self.player) or state.can_reach(RegionNames.Corsair_Cove,
                                                                                            None, self.player))
        )
        self.multiworld.get_location(LocationNames.Smelt_Silver, self.player).access_rule = lambda state: (
                state.can_reach(RegionNames.Silver_Rock, None, self.player) and
                state.can_reach(RegionNames.Furnace, None, self.player)
        )
        self.multiworld.get_location(LocationNames.Smelt_Steel, self.player).access_rule = lambda state: (
                state.can_reach(RegionNames.Coal_Rock, None, self.player) and
                state.can_reach(RegionNames.Iron_Rock, None, self.player) and
                state.can_reach(RegionNames.Furnace, None, self.player)
        )
        self.multiworld.get_location(LocationNames.Smelt_Gold, self.player).access_rule = lambda state: (
                state.can_reach(RegionNames.Gold_Rock, None, self.player) and
                state.can_reach(RegionNames.Furnace, None, self.player)
        )
        self.multiworld.get_location(LocationNames.Bake_Apple_Pie, self.player).access_rule = lambda state: (
                state.can_reach(RegionNames.Wheat, None, self.player) and
                state.can_reach(RegionNames.Windmill, None, self.player) and
                state.can_reach(RegionNames.West_Varrock, None, self.player) and
                state.can_reach(RegionNames.Imp, None, self.player)
        )
        self.multiworld.get_location(LocationNames.Bake_Cake, self.player).access_rule = lambda state: (
                state.can_reach(RegionNames.Wheat, None, self.player) and
                state.can_reach(RegionNames.Egg, None, self.player) and
                state.can_reach(RegionNames.Milk, None, self.player) and
                state.can_reach(RegionNames.Windmill, None, self.player)
        )
        self.multiworld.get_location(LocationNames.Bake_Meat_Pizza, self.player).access_rule = lambda state: (
                state.can_reach(RegionNames.Wheat, None, self.player) and
                state.can_reach(RegionNames.Windmill, None, self.player)
        )
        self.multiworld.get_location(LocationNames.K_Lesser_Demon, self.player).access_rule = lambda state: (
                state.can_reach(RegionNames.Wilderness, None, self.player) or
                state.can_reach(RegionNames.Crandor, None, self.player) or
                state.can_reach(RegionNames.Wizards_Tower, None, self.player) or
                state.can_reach(RegionNames.Karamja, None, self.player)
        )

        self.multiworld.get_location(LocationNames.Q_Dragon_Slayer, self.player).access_rule = lambda state: (
                self.quest_points(state) >= 32 and state.can_reach(RegionNames.Crandor, None, self.player)
        )

        # Put some of the later grinds behind some QP so it's not all front-loaded
        self.multiworld.get_location(LocationNames.Total_Level_150, self.player).access_rule = lambda state: (
                self.quest_points(state) >= 3
        )
        self.multiworld.get_location(LocationNames.Total_Level_200, self.player).access_rule = lambda state: (
                self.quest_points(state) >= 5
        )
        self.multiworld.get_location(LocationNames.Combat_Level_15, self.player).access_rule = lambda state: (
                self.quest_points(state) >= 3
        )
        self.multiworld.get_location(LocationNames.Combat_Level_25, self.player).access_rule = lambda state: (
                self.quest_points(state) >= 8
        )
        self.multiworld.get_location(LocationNames.Total_XP_25000, self.player).access_rule = lambda state: (
                self.quest_points(state) >= 3
        )
        self.multiworld.get_location(LocationNames.Total_XP_50000, self.player).access_rule = lambda state: (
                self.quest_points(state) >= 5
        )
        self.multiworld.get_location(LocationNames.Total_XP_100000, self.player).access_rule = lambda state: (
                self.quest_points(state) >= 12
        )

        # place "Victory" at "Dragon Slayer" and set collection as win condition
        self.multiworld.get_location(LocationNames.Q_Dragon_Slayer, self.player) \
            .place_locked_item(self.create_event("Victory"))
        self.multiworld.completion_condition[self.player] = lambda state: (state.has("Victory", self.player))

    def create_item(self, name: str) -> "Item":
        item = item_table[name]
        return OSRSItem(item.itemName, item.progression, item.id, self.player)

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

    def can_reach(self, state, skill, level):
        match skill:
            case "fishing":
            case "mining":
                can_train = state.can_reach(RegionNames.Bronze_Ores, None, self.player) or state.can_reach(
                    RegionNames.Clay_Rock)
                if not self.allow_brutal_grinds:
                    # Iron is the best way to train all the way to 99, so having access to iron is all you need
                    if level >= 15:
                        can_train = can_train and state.can_reach(RegionNames.Iron_Rock, None, self.player)
                return can_train
            case "woodcutting":
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
            case "smithing":
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
            case "crafting":
                # There are many ways to start training
                can_spin = state.can_reach(RegionNames.Sheep, None, self.player) and state.can_reach(RegionNames.Spinning_Wheel, None, self.player)
                can_pot = state.can_reach(RegionNames.Clay_Rock, None, self.player) and state.can_reach(RegionNames.Barbarian_Village, None, self.player)
                can_tan = state.can_reach(RegionNames.Milk, None, self.player) and state.can_reach(RegionNames.Al_Kharid, None, self.player)
                can_train = can_spin or can_pot or can_tan
                return can_train
            case "cooking":
        pass
