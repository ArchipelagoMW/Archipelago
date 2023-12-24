import binascii
import os
import pkgutil
import tempfile
import typing

import bsdiff4

import settings
from BaseClasses import Entrance, Item, ItemClassification, Location, Tutorial
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
from .LADXR.main import get_parser
from .LADXR.settings import Settings as LADXRSettings
from .LADXR.worldSetup import WorldSetup as LADXRWorldSetup
from .Locations import (LinksAwakeningLocation, LinksAwakeningRegion,
                        create_regions_from_ladxr, get_locations_to_id)
from .Options import DungeonItemShuffle, links_awakening_options
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

    prefill_dungeon_items = None

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
        world_setup = LADXRWorldSetup()
        world_setup.randomize(self.laxdr_options, self.multiworld.random)
        self.ladxr_logic = LAXDRLogic(configuration_options=self.laxdr_options, world_setup=world_setup)
        self.ladxr_itempool = LADXRItemPool(self.ladxr_logic, self.laxdr_options, self.multiworld.random).toDict()

    def create_regions(self) -> None:
        # Initialize
        self.convert_ap_options_to_ladxr_logic()
        regions = create_regions_from_ladxr(self.player, self.multiworld, self.ladxr_logic)
        self.multiworld.regions += regions

        # Connect Menu -> Start
        start = None
        for region in regions:
            if region.name == "Start House":
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
                    self.multiworld.itempool.append(self.create_item("Master Stalfos' Message"))
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
                                self.multiworld.itempool.append(item)
                    else:
                        self.multiworld.itempool.append(item)

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
                    # Don't place dungeon items on pit button chest, to reduce chance of the filler blowing up
                    # TODO: no need for this if small key shuffle
                    if location.name == "Pit Button Chest (Tail Cave)" or location.item:
                        self.dungeon_locations_by_dungeon[r.dungeon_index - 1].remove(location)
                    # Properly fill locations within dungeon
                    location.dungeon = r.dungeon_index

    def force_start_item(self):    
        start_loc = self.multiworld.get_location("Tarin's Gift (Mabe Village)", self.player)
        if not start_loc.item:
            possible_start_items = [index for index, item in enumerate(self.multiworld.itempool)
                if item.player == self.player 
                    and item.item_data.ladxr_id in start_loc.ladxr_item.OPTIONS and not item.location]
            if possible_start_items:
                index = self.multiworld.random.choice(possible_start_items)
                start_item = self.multiworld.itempool.pop(index)
                start_loc.place_locked_item(start_item)


    def get_pre_fill_items(self):
        return self.pre_fill_items

    def pre_fill(self) -> None:
        allowed_locations_by_item = {}

        # For now, special case first item
        FORCE_START_ITEM = True
        if FORCE_START_ITEM:
            self.force_start_item()

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
