import binascii
import os
import copy
import itertools
from .Locations import connector_info
from .LADXR.entranceInfo import ENTRANCE_INFO, entrances_by_type
import pkgutil
import tempfile
import typing

import bsdiff4


import settings
from BaseClasses import Entrance, Item, ItemClassification, Location, Tutorial, CollectionState
from Fill import fill_restrictive
from worlds.AutoWorld import WebWorld, World
from .Common import *
from .Items import (DungeonItemData, DungeonItemType, ItemName, LinksAwakeningItem, TradeItemData,
                    ladxr_item_to_la_item_name, links_awakening_items, links_awakening_items_by_name)
from .LADXR import generator
from .LADXR.itempool import ItemPool as LADXRItemPool
from .LADXR.locations.constants import CHEST_ITEMS
from .LADXR.locations.instrument import Instrument
from .LADXR.logic import Logic as LAXDRLogic
from .LADXR.logic.requirements import RequirementsSettings
from .LADXR.main import get_parser
from .LADXR.settings import Settings as LADXRSettings
from .LADXR.worldSetup import WorldSetup as LADXRWorldSetup
from .Locations import (LinksAwakeningLocation, LinksAwakeningRegion,
                        create_regions_from_ladxr, get_locations_to_id)
from .Options import links_awakening_options, DungeonItemShuffle, EntranceShuffle
from .Rom import LADXDeltaPatch


DEVELOPER_MODE = False


class LinksAwakeningSettings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the Link's Awakening DX rom"""
        copy_to = "Legend of Zelda, The - Link's Awakening DX (USA, Europe) (SGB Enhanced).gbc"
        description = "LADX ROM File"
        md5s = [LADXDeltaPatch.hash]

    class RomStart(str):
        """
        Set this to false to never autostart a rom (such as after patching)
                    true  for operating system default program
        Alternatively, a path to a program to open the .gbc file with
        Examples:
           Retroarch:
        rom_start: "C:/RetroArch-Win64/retroarch.exe -L sameboy"
           BizHawk:
        rom_start: "C:/BizHawk-2.9-win-x64/EmuHawk.exe --lua=data/lua/connector_ladx_bizhawk.lua"
        """

    class DisplayMsgs(settings.Bool):
        """Display message inside of Bizhawk"""

    rom_file: RomFile = RomFile(RomFile.copy_to)
    rom_start: typing.Union[RomStart, bool] = True

class LinksAwakeningWebWorld(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Links Awakening DX for MultiWorld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["zig"]
    )]
    theme = "dirt"


class LinksAwakeningWorld(World):
    """
    After a previous adventure, Link is stranded on Koholint Island, full of mystery and familiar faces.
    Gather the 8 Instruments of the Sirens to wake the Wind Fish, so that Link can go home!
    """
    game = LINKS_AWAKENING  # name of the game/world
    web = LinksAwakeningWebWorld()
    
    option_definitions = links_awakening_options  # options the player can set
    settings: typing.ClassVar[LinksAwakeningSettings]
    topology_present = True  # show path to required location checks in spoiler

    # data_version is used to signal that items, locations or their names
    # changed. Set this to 0 during development so other games' clients do not
    # cache any texts, then increase by 1 for each release that makes changes.
    data_version = 1

    # ID of first item and location, could be hard-coded but code may be easier
    # to read with this as a propery.
    base_id = BASE_ID
    # Instead of dynamic numbering, IDs could be part of data.

    # The following two dicts are required for the generation to know which
    # items exist. They could be generated from json or something else. They can
    # include events, but don't have to since events will be placed manually.
    item_name_to_id = {
        item.item_name : BASE_ID + item.item_id for item in links_awakening_items
    }

    item_name_to_data = links_awakening_items_by_name

    location_name_to_id = get_locations_to_id()

    # Items can be grouped using their names to allow easy checking if any item
    # from that group has been collected. Group names can also be used for !hint
    #item_name_groups = {
    #    "weapons": {"sword", "lance"}
    #}

    player_options = None

    rupees = {
        ItemName.RUPEES_20: 20,
        ItemName.RUPEES_50: 50,
        ItemName.RUPEES_100: 100,
        ItemName.RUPEES_200: 200,
        ItemName.RUPEES_500: 500,
    }

    def convert_ap_options_to_ladxr_logic(self):
        self.player_options = {
            option: getattr(self.multiworld, option)[self.player] for option in self.option_definitions
        }

        self.laxdr_options = LADXRSettings(self.player_options)
        
        self.laxdr_options.validate()
        self.world_setup = LADXRWorldSetup()
        self.world_setup.randomize(self.laxdr_options, self.multiworld.random)
        self.randomize_entrances()
        self.ladxr_logic = LAXDRLogic(configuration_options=self.laxdr_options, world_setup=self.world_setup)
        self.ladxr_itempool = LADXRItemPool(self.ladxr_logic, self.laxdr_options, self.multiworld.random).toDict()
    
    def randomize_entrances(self):
        banned_starts = [
            # All of these lead directly to nothing or another connector
            "obstacle_cave_outside_chest",
            "multichest_top",
            "right_taltal_connector2",
            "right_taltal_connector3",
            "right_taltal_connector4",
            "right_taltal_connector5",
            "right_fairy",
            "castle_upper_left",
            "castle_upper_right",
            "prairie_madbatter_connector_exit",
            "prairie_madbatter",
            # Risky, two exits
            "prairie_right_cave_high",
            "richard_maze",
            # Three
            "multichest_right",
            "right_taltal_connector1",
            # Inside castle - funny but only if we force the castle button to be available (or open)
            "castle_main_entrance",
            "castle_secret_exit",
            # Five exits
            # This drops you down into the water, required flippers start
            # "right_taltal_connector6",
            # "d7"
        ]
   
        from .LADXR.logic.overworld import World
        entrance_pools = {}
        indoor_pools = {}
        entrance_pool_mapping = {}

        random = self.multiworld.per_slot_randoms[self.player]
        world = World(self.laxdr_options, self.world_setup, RequirementsSettings(self.laxdr_options))
        # First shuffle the start location, if needed
        start = world.start
        start_entrance = "start_house"
        
        start_shuffle = self.player_options["start_shuffle"]

        start_type_mappings = {}

        for option_name, option in self.player_options.items():
            if isinstance(option, EntranceShuffle):
                for cat in option.entrance_type:
                    start_type_mappings[option_name] = cat
                if option.value == EntranceShuffle.option_simple:
                    entrance_pool_mapping[option.entrance_type[0]] = option.entrance_type[0]
                elif option.value == EntranceShuffle.option_mixed:
                    entrance_pool_mapping[option.entrance_type[0]] = "mixed"
                else:
                    continue
                pool = entrance_pools.setdefault(entrance_pool_mapping[option.entrance_type[0]], [])
                indoor_pool = indoor_pools.setdefault(entrance_pool_mapping[option.entrance_type[0]], [])

                # TODO: Gross N*M behavior, we can just iterate the entrance info once or twice
                for entrance_name, entrance in ENTRANCE_INFO.items():
                    if entrance.type in option.entrance_type:
                        pool.append(entrance_name)
                        # Connectors have special handling
                        if entrance.type != "connector":
                            indoor_pool.append(entrance_name)

        # Shuffle starting location
        if start_shuffle.value:
            start_candidates = []
            
            # Find all possible start locations
            for category in start_shuffle.value:
                start_candidates += entrances_by_type[category]
                # TODO: cleaner plz
                if category == "single":
                    start_candidates += entrances_by_type["trade"]

            # Some start locations result in either
            # (A) requiring certain arrangements of connectors 
            # (B) immediately deadending
            # these could be fixed with chaos entrance rando or smarter connector shuffle
            # but for now we aren't gonna handle it            

            start_candidates = [c for c in start_candidates if c not in banned_starts]
            if start_candidates:
                start_candidates.sort()
                start_entrance = random.choice(start_candidates)
                self.world_setup.entrance_mapping[start_entrance] = "start_house"
                start = world.overworld_entrance[start_entrance].location
                for pool in entrance_pools.values():
                    if start_entrance in pool:
                        pool.remove(start_entrance)
                        pool.append("start_house")
                        break
                else:
                    # This entrance wasn't shuffled, just map back
                    self.world_setup.entrance_mapping["start_house"] = start_entrance


        for pool in itertools.chain(entrance_pools.values(), indoor_pools.values()):
            # Sort first so that we get the same result every time
            pool.sort()

        has_castle_button = False

        

        # NOTE: this code uses LADXR terms for things where:
        # Region -> Location
        # Location -> ItemInfo
        # Item -> ...also Item? but not used here
        # Helper to apply function to every ladxr region

        # If we haven't found the castle button, don't allow going back and forth over the gate
        def check_castle_button(a, b):
            if has_castle_button:
                return True
            gate_names = ("Kanalet Castle Front Door", "Ukuku Prairie")
            return a.name not in gate_names or b.name not in gate_names

        def walk_locations(callback, current_location, filter=lambda _: True, walked=None) -> None:
            walked = walked or set()
            if current_location in walked:
                return
            if not filter(current_location):
                return
            callback(current_location)
            walked.add(current_location)

            for o, req in itertools.chain(current_location.simple_connections, current_location.gated_connections):
                if check_castle_button(current_location, o):
                    walk_locations(callback, o, filter, walked)




        # First shuffle connectors, as they will fail if shuffled randomly
        if "connector" in entrance_pool_mapping:
            # Get the list of unshuffled connectors
            unshuffled_connectors = copy.copy(connector_info)
            random.shuffle(unshuffled_connectors)

            # Get the list of unshuffled candidates connector entrances 
            unseen_entrances = copy.copy(entrance_pools[entrance_pool_mapping["connector"]])

            location_to_entrances = {}
            for k,v in world.overworld_entrance.items():
                location_to_entrances.setdefault(v.location,[]).append(k)

            unshuffled_entrances = entrance_pools[entrance_pool_mapping["connector"]]
            seen_locations = set()

            def mark_location(l):
                if l in location_to_entrances:
                    for entrance in location_to_entrances[l]:
                        seen_locations.add(entrance)
                        if entrance in unseen_entrances:
                            unseen_entrances.remove(entrance)

            # TODO: we can reuse our walked location cache
            walked = set()
            walk_locations(callback=mark_location, current_location=start, walked=walked)

            while unseen_entrances:
                # Find the places we haven't yet seen
                # Pick one
                unseen_entrance_to_connect = random.choice(unseen_entrances)

                # Pick an unshuffled seen entrance
                l = list(seen_locations.intersection(unshuffled_entrances))
                l.sort()
                seen_entrance_to_connect = random.choice(l)
                
                # Pick a connector
                connector = unshuffled_connectors.pop()
                if connector.castle_button:
                    has_castle_button = True
                # Pick the connector direction
                entrances = connector.entrances
                if not connector.oneway:
                    entrances = list(entrances)
                    random.shuffle(entrances)
                else:
                    assert len(connector.entrances) == 2
                A = connector.entrances[0]
                B = connector.entrances[1]
                C = len(connector.entrances) > 2 and connector.entrances[2] or None

                # Flag the two doors as connected
                self.world_setup.entrance_mapping[seen_entrance_to_connect] = A            
                self.world_setup.entrance_mapping[unseen_entrance_to_connect] = B
                # Walk the new locations
                walk_locations(callback=mark_location, current_location=world.overworld_entrance[unseen_entrance_to_connect].location)
                assert unseen_entrance_to_connect not in unseen_entrances
                unshuffled_entrances.remove(seen_entrance_to_connect)
                unshuffled_entrances.remove(unseen_entrance_to_connect)
                if C:
                    third_entrance_to_connect = random.choice(list(unshuffled_entrances))
                    self.world_setup.entrance_mapping[third_entrance_to_connect] = C
                    walk_locations(callback=mark_location, current_location=world.overworld_entrance[third_entrance_to_connect].location)
                    unshuffled_entrances.remove(third_entrance_to_connect)

            # Shuffle the remainder
            random.shuffle(unshuffled_entrances)
            random.shuffle(unshuffled_connectors)
            while unshuffled_connectors:
                connector = unshuffled_connectors.pop()
                for entrance in connector.entrances:
                    self.world_setup.entrance_mapping[unshuffled_entrances.pop()] = entrance

        # Now for each pool of entrances, shuffle
        for pool_name, pool in entrance_pools.items():
            random.shuffle(pool)
            indoor_pool = indoor_pools[pool_name]
            random.shuffle(indoor_pool)
            for a, b in zip(pool, indoor_pool):
                self.world_setup.entrance_mapping[a] = b

        seen_keys = set()
        seen_values = set()
        for k, v in self.world_setup.entrance_mapping.items():
            assert k not in seen_keys
            assert v not in seen_values, v
            seen_keys.add(k)
            seen_values.add(v)


    def create_regions(self) -> None:
        # Initialize
        self.convert_ap_options_to_ladxr_logic()
        regions = create_regions_from_ladxr(self.player, self.multiworld, self.ladxr_logic)
        self.multiworld.regions += regions

        # Connect Menu -> Start
        start = None
        for region in regions:
            if region.name == "Tarin's House":
                start = region
                break

        assert(start)

        menu_region = LinksAwakeningRegion("Menu", None, "Menu", self.player, self.multiworld)        
        menu_region.exits = [Entrance(self.player, "Start Game", menu_region)]
        menu_region.exits[0].connect(start)
        
        self.multiworld.regions.append(menu_region)

        # Place RAFT, other access events
        for region in regions:
            for loc in region.locations:
                if loc.event:
                    loc.place_locked_item(self.create_event(loc.ladxr_item.event))
        
        # Connect Windfish -> Victory
        windfish = self.multiworld.get_region("Windfish", self.player)
        l = Location(self.player, "Windfish", parent=windfish)
        windfish.locations = [l]
                
        l.place_locked_item(self.create_event("An Alarm Clock"))
        
        self.multiworld.completion_condition[self.player] = lambda state: state.has("An Alarm Clock", player=self.player)
        

    def create_item(self, item_name: str):
        return LinksAwakeningItem(self.item_name_to_data[item_name], self, self.player)

    def create_event(self, event: str):
        return Item(event, ItemClassification.progression, None, self.player)

    def create_items(self) -> None:
        itempool = []

        exclude = [item.name for item in self.multiworld.precollected_items[self.player]]

        dungeon_item_types = {

        }

        self.prefill_original_dungeon = [ [], [], [], [], [], [], [], [], [] ]
        self.prefill_own_dungeons = []
        self.pre_fill_items = []
        # For any and different world, set item rule instead
        
        for option in ["maps", "compasses", "small_keys", "nightmare_keys", "stone_beaks"]:
            option = "shuffle_" + option
            option = self.player_options[option]

            dungeon_item_types[option.ladxr_item] = option.value

            if option.value == DungeonItemShuffle.option_own_world:
                self.multiworld.local_items[self.player].value |= {
                    ladxr_item_to_la_item_name[f"{option.ladxr_item}{i}"] for i in range(1, 10)
                }
            elif option.value == DungeonItemShuffle.option_different_world:
                self.multiworld.non_local_items[self.player].value |= {
                    ladxr_item_to_la_item_name[f"{option.ladxr_item}{i}"] for i in range(1, 10)
                }
        # option_original_dungeon = 0
        # option_own_dungeons = 1
        # option_own_world = 2
        # option_any_world = 3
        # option_different_world = 4
        # option_delete = 5

        for ladx_item_name, count in self.ladxr_itempool.items():
            # event
            if ladx_item_name not in ladxr_item_to_la_item_name:
                continue
            item_name = ladxr_item_to_la_item_name[ladx_item_name]
            for _ in range(count):
                if item_name in exclude:
                    exclude.remove(item_name)  # this is destructive. create unique list above
                    itempool.append(self.create_item("Master Stalfos' Message"))
                else:
                    item = self.create_item(item_name)

                    if not self.multiworld.tradequest[self.player] and isinstance(item.item_data, TradeItemData):
                        location = self.multiworld.get_location(item.item_data.vanilla_location, self.player)
                        location.place_locked_item(item)
                        location.show_in_spoiler = False
                        continue

                    if isinstance(item.item_data, DungeonItemData):
                        if item.item_data.dungeon_item_type == DungeonItemType.INSTRUMENT:
                            # Find instrument, lock
                            # TODO: we should be able to pinpoint the region we want, save a lookup table please
                            found = False
                            for r in self.multiworld.get_regions(self.player):
                                if r.dungeon_index != item.item_data.dungeon_index:
                                    continue
                                for loc in r.locations:
                                    if not isinstance(loc, LinksAwakeningLocation):
                                        continue
                                    if not isinstance(loc.ladxr_item, Instrument):
                                        continue
                                    loc.place_locked_item(item)
                                    found = True
                                    break
                                if found:
                                    break                            
                        else:
                            item_type = item.item_data.ladxr_id[:-1]
                            shuffle_type = dungeon_item_types[item_type]
                            if shuffle_type == DungeonItemShuffle.option_original_dungeon:
                                self.prefill_original_dungeon[item.item_data.dungeon_index - 1].append(item)
                                self.pre_fill_items.append(item)
                            elif shuffle_type == DungeonItemShuffle.option_own_dungeons:
                                self.prefill_own_dungeons.append(item)
                                self.pre_fill_items.append(item)
                            else:
                                itempool.append(item)
                    else:
                        itempool.append(item)

        self.multi_key = self.generate_multi_key()

        # Add special case for trendy shop access
        trendy_region = self.multiworld.get_region("Trendy Shop", self.player)
        event_location = Location(self.player, "Can Play Trendy Game", parent=trendy_region)
        trendy_region.locations.insert(0, event_location)
        event_location.place_locked_item(self.create_event("Can Play Trendy Game"))
       
        self.dungeon_locations_by_dungeon = [[], [], [], [], [], [], [], [], []]     
        for r in self.multiworld.get_regions(self.player):
            # Set aside dungeon locations
            if r.dungeon_index:
                self.dungeon_locations_by_dungeon[r.dungeon_index - 1] += r.locations
                for location in r.locations:
                    # This probably isn't needed any more, but we'll see
                    # Don't place dungeon items on pit button chest, to reduce chance of the filler blowing up
                    # TODO: no need for this if small key shuffle
                    if location.name == "Pit Button Chest (Tail Cave)" or location.item:
                        self.dungeon_locations_by_dungeon[r.dungeon_index - 1].remove(location)
                    # Properly fill locations within dungeon
                    location.dungeon = r.dungeon_index
        if self.multiworld.tarin_gifts_your_item[self.player]:
            self.force_start_item(itempool)

        self.multiworld.itempool += itempool

    def force_start_item(self, itempool):
        start_loc = self.multiworld.get_location("Tarin's Gift (Mabe Village)", self.player)
        if not start_loc.item:
            """
            Find an item that forces progression for the player
            """
            base_collection_state = CollectionState(self.multiworld)
            base_collection_state.update_reachable_regions(self.player)
            reachable_count = len(base_collection_state.reachable_regions[self.player])

            def gives_progression(item):
                collection_state = base_collection_state.copy()
                collection_state.collect(item)
                # Why isn't this needed?
                # collection_state.update_reachable_regions(self.player)
                return len(collection_state.reachable_regions[self.player]) > reachable_count
            possible_start_items = [item for item in itempool if item.advancement]
            self.random.shuffle(possible_start_items)

            for item in possible_start_items:
                if gives_progression(item):
                    itempool.remove(item)
                    start_loc.place_locked_item(item)
                    return

    def get_pre_fill_items(self):
        return self.pre_fill_items

    def pre_fill(self) -> None:
        allowed_locations_by_item = {}

        # Set up filter rules

        # The list of items we will pass to fill_restrictive, contains at first the items that go to all dungeons
        all_dungeon_items_to_fill = list(self.prefill_own_dungeons)
        # set containing the list of all possible dungeon locations for the player
        all_dungeon_locs = set()
        
        # Do dungeon specific things
        for dungeon_index in range(0, 9):
            # set up allow-list for dungeon specific items
            locs = set(loc for loc in self.dungeon_locations_by_dungeon[dungeon_index] if not loc.item)
            for item in self.prefill_original_dungeon[dungeon_index]:
                allowed_locations_by_item[item] = locs

            # put the items for this dungeon in the list to fill
            all_dungeon_items_to_fill.extend(self.prefill_original_dungeon[dungeon_index])

            # ...and gather the list of all dungeon locations
            all_dungeon_locs |= locs
            # ...also set the rules for the dungeon
            for location in locs:
                orig_rule = location.item_rule
                # If an item is about to be placed on a dungeon location, it can go there iff 
                # 1. it fits the general rules for that location (probably 'return True' for most places)
                # 2. Either
                #    2a. it's not a restricted dungeon item
                #    2b. it's a restricted dungeon item and this location is specified as allowed
                location.item_rule = lambda item, location=location, orig_rule=orig_rule: \
                    (item not in allowed_locations_by_item or location in allowed_locations_by_item[item]) and orig_rule(item)

        # Now set up the allow-list for any-dungeon items
        for item in self.prefill_own_dungeons:
            # They of course get to go in any spot
            allowed_locations_by_item[item] = all_dungeon_locs

        # Get the list of locations and shuffle
        all_dungeon_locs_to_fill = sorted(all_dungeon_locs)

        self.multiworld.random.shuffle(all_dungeon_locs_to_fill)

        # Get the list of items and sort by priority
        def priority(item):
            # 0 - Nightmare dungeon-specific
            # 1 - Key dungeon-specific
            # 2 - Other dungeon-specific
            # 3 - Nightmare any local dungeon
            # 4 - Key any local dungeon
            # 5 - Other any local dungeon
            i = 2
            if "Nightmare" in item.name:
                i = 0
            elif "Key" in item.name:
                i = 1
            if allowed_locations_by_item[item] is all_dungeon_locs:
                i += 3
            return i
        all_dungeon_items_to_fill.sort(key=priority)

        # Set up state
        all_state = self.multiworld.get_all_state(use_cache=False)
        # Remove dungeon items we are about to put in from the state so that we don't double count
        for item in all_dungeon_items_to_fill:
            all_state.remove(item)
        
        # Finally, fill!
        fill_restrictive(self.multiworld, all_state, all_dungeon_locs_to_fill, all_dungeon_items_to_fill, lock=True, single_player_placement=True, allow_partial=False)

    name_cache = {}
    # Tries to associate an icon from another game with an icon we have
    def guess_icon_for_other_world(self, other):
        if not self.name_cache:
            forbidden = [
                "TRADING",
                "ITEM",
                "BAD",
                "SINGLE",
                "UPGRADE",
                "BLUE",
                "RED",
                "NOTHING",
                "MESSAGE",
            ]
            for item in ladxr_item_to_la_item_name.keys():
                self.name_cache[item] = item
                splits = item.split("_")
                self.name_cache["".join(splits)] = item
                if 'RUPEES' in splits:
                    self.name_cache["".join(reversed(splits))] = item
                    
                for word in item.split("_"):
                    if word not in forbidden and not word.isnumeric():
                        self.name_cache[word] = item
            others = {
                'KEY': 'KEY',
                'COMPASS': 'COMPASS',
                'BIGKEY': 'NIGHTMARE_KEY',
                'MAP': 'MAP',
                'FLUTE': 'OCARINA',
                'SONG': 'OCARINA',
                'MUSHROOM': 'TOADSTOOL',
                'GLOVE': 'POWER_BRACELET',
                'BOOT': 'PEGASUS_BOOTS',
                'SHOE': 'PEGASUS_BOOTS',
                'SHOES': 'PEGASUS_BOOTS',
                'SANCTUARYHEARTCONTAINER': 'HEART_CONTAINER',
                'BOSSHEARTCONTAINER': 'HEART_CONTAINER',
                'HEARTCONTAINER': 'HEART_CONTAINER',
                'ENERGYTANK': 'HEART_CONTAINER',
                'MISSILE': 'SINGLE_ARROW',
                'BOMBS': 'BOMB',
                'BLUEBOOMERANG': 'BOOMERANG',
                'MAGICMIRROR': 'TRADING_ITEM_MAGNIFYING_GLASS',
                'MIRROR': 'TRADING_ITEM_MAGNIFYING_GLASS',
                'MESSAGE': 'TRADING_ITEM_LETTER',
                # TODO: Also use AP item name
            }
            for name in others.values():
                assert name in self.name_cache, name
                assert name in CHEST_ITEMS, name
            self.name_cache.update(others)
            
        
        uppered = other.upper()
        if "BIG KEY" in uppered:
            return 'NIGHTMARE_KEY'
        possibles = other.upper().split(" ")
        rejoined = "".join(possibles)
        if rejoined in self.name_cache:
            return self.name_cache[rejoined]
        for name in possibles:
            if name in self.name_cache:
                return self.name_cache[name]
        
        return "TRADING_ITEM_LETTER"

    def generate_output(self, output_directory: str):
        # copy items back to locations
        for r in self.multiworld.get_regions(self.player):
            for loc in r.locations:
                if isinstance(loc, LinksAwakeningLocation):
                    assert(loc.item)
                        
                    # If we're a links awakening item, just use the item
                    if isinstance(loc.item, LinksAwakeningItem):
                        loc.ladxr_item.item = loc.item.item_data.ladxr_id

                    # If the item name contains "sword", use a sword icon, etc
                    # Otherwise, use a cute letter as the icon
                    else:
                        loc.ladxr_item.item = self.guess_icon_for_other_world(loc.item.name)
                        loc.ladxr_item.custom_item_name = loc.item.name

                    if loc.item:
                        loc.ladxr_item.item_owner = loc.item.player
                    else:
                        loc.ladxr_item.item_owner = self.player

                    # Kind of kludge, make it possible for the location to differentiate between local and remote items
                    loc.ladxr_item.location_owner = self.player

        rom_name = Rom.get_base_rom_path()
        out_name = f"AP-{self.multiworld.seed_name}-P{self.player}-{self.multiworld.player_name[self.player]}.gbc"
        out_path = os.path.join(output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}.gbc")

        parser = get_parser()
        args = parser.parse_args([rom_name, "-o", out_name, "--dump"])

        name_for_rom = self.multiworld.player_name[self.player]

        all_names = [self.multiworld.player_name[i + 1] for i in range(len(self.multiworld.player_name))]

        rom = generator.generateRom(
            args,
            self.laxdr_options,
            self.player_options,
            self.multi_key,
            self.multiworld.seed_name,
            self.ladxr_logic,
            rnd=self.multiworld.per_slot_randoms[self.player],
            player_name=name_for_rom,
            player_names=all_names,
            player_id = self.player,
            multiworld=self.multiworld)
      
        with open(out_path, "wb") as handle:
            rom.save(handle, name="LADXR")

        # Write title screen after everything else is done - full gfxmods may stomp over the egg tiles
        if self.player_options["ap_title_screen"]:
            with tempfile.NamedTemporaryFile(delete=False) as title_patch:
                title_patch.write(pkgutil.get_data(__name__, "LADXR/patches/title_screen.bdiff4"))
        
            bsdiff4.file_patch_inplace(out_path, title_patch.name)
            os.unlink(title_patch.name)

        patch = LADXDeltaPatch(os.path.splitext(out_path)[0]+LADXDeltaPatch.patch_file_ending, player=self.player,
                               player_name=self.multiworld.player_name[self.player], patched_path=out_path)
        patch.write()
        if not DEVELOPER_MODE:
            os.unlink(out_path)

    def generate_multi_key(self):
        return bytearray(self.multiworld.random.getrandbits(8) for _ in range(10)) + self.player.to_bytes(2, 'big')

    def modify_multidata(self, multidata: dict):
        multidata["connect_names"][binascii.hexlify(self.multi_key).decode()] = multidata["connect_names"][self.multiworld.player_name[self.player]]

    def collect(self, state, item: Item) -> bool:
        change = super().collect(state, item)
        if change and item.name in self.rupees:
            state.prog_items[self.player]["RUPEES"] += self.rupees[item.name]
        return change

    def remove(self, state, item: Item) -> bool:
        change = super().remove(state, item)
        if change and item.name in self.rupees:
            state.prog_items[self.player]["RUPEES"] -= self.rupees[item.name]
        return change
