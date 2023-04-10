import binascii
import os

from BaseClasses import Entrance, Item, ItemClassification, Location, Tutorial
from Fill import fill_restrictive
from worlds.AutoWorld import WebWorld, World

from .Common import *
from .Items import (DungeonItemData, DungeonItemType, LinksAwakeningItem,
                    ladxr_item_to_la_item_name, links_awakening_items,
                    links_awakening_items_by_name)
from .LADXR import generator
from .LADXR.itempool import ItemPool as LADXRItemPool
from .LADXR.locations.tradeSequence import TradeSequenceItem
from .LADXR.logic import Logic as LAXDRLogic
from .LADXR.main import get_parser
from .LADXR.settings import Settings as LADXRSettings
from .LADXR.worldSetup import WorldSetup as LADXRWorldSetup
from .LADXR.locations.instrument import Instrument
from .LADXR.locations.constants import CHEST_ITEMS
from .Locations import (LinksAwakeningLocation, LinksAwakeningRegion,
                        create_regions_from_ladxr, get_locations_to_id)
from .Options import links_awakening_options
from .Rom import LADXDeltaPatch

DEVELOPER_MODE = False

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
    game: str = LINKS_AWAKENING # name of the game/world
    web = LinksAwakeningWebWorld()
    
    option_definitions = links_awakening_options  # options the player can set
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

        self.trade_items = []

        dungeon_item_types = {

        }
        from .Options import DungeonItemShuffle        
        self.prefill_original_dungeon = [ [], [], [], [], [], [], [], [], [] ]
        self.prefill_own_dungeons = []
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

                    if not self.multiworld.tradequest[self.player] and ladx_item_name.startswith("TRADING_"):
                        self.trade_items.append(item)
                        continue
                    if isinstance(item.item_data, DungeonItemData):
                        if item.item_data.dungeon_item_type == DungeonItemType.INSTRUMENT:
                            # Find instrument, lock
                            # TODO: we should be able to pinpoint the region we want, save a lookup table please
                            found = False
                            for r in self.multiworld.get_regions():
                                if r.player != self.player:
                                    continue
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
                            elif shuffle_type == DungeonItemShuffle.option_own_dungeons:
                                self.prefill_own_dungeons.append(item)
                            else:
                                self.multiworld.itempool.append(item)
                    else:
                        self.multiworld.itempool.append(item)

    def pre_fill(self):
        self.multi_key = self.generate_multi_key()

        dungeon_locations = []
        dungeon_locations_by_dungeon = [[], [], [], [], [], [], [], [], []]
        all_state = self.multiworld.get_all_state(use_cache=False)
        
        # Add special case for trendy shop access
        trendy_region = self.multiworld.get_region("Trendy Shop", self.player)
        event_location = Location(self.player, "Can Play Trendy Game", parent=trendy_region)
        trendy_region.locations.insert(0, event_location)
        event_location.place_locked_item(self.create_event("Can Play Trendy Game"))
        
        # For now, special case first item
        FORCE_START_ITEM = True
        if FORCE_START_ITEM:
            start_loc = self.multiworld.get_location("Tarin's Gift (Mabe Village)", self.player)
            if not start_loc.item:
                possible_start_items = [index for index, item in enumerate(self.multiworld.itempool)
                    if item.player == self.player 
                        and item.item_data.ladxr_id in start_loc.ladxr_item.OPTIONS]
                
                index = self.multiworld.random.choice(possible_start_items)
                start_item = self.multiworld.itempool.pop(index)
                start_loc.place_locked_item(start_item)
        
        for r in self.multiworld.get_regions():
            if r.player != self.player:
                continue

            # Set aside dungeon locations
            if r.dungeon_index:
                dungeon_locations += r.locations
                dungeon_locations_by_dungeon[r.dungeon_index - 1] += r.locations
                for location in r.locations:
                    if location.name == "Pit Button Chest (Tail Cave)":
                        # Don't place dungeon items on pit button chest, to reduce chance of the filler blowing up
                        # TODO: no need for this if small key shuffle
                        dungeon_locations.remove(location)
                        dungeon_locations_by_dungeon[r.dungeon_index - 1].remove(location)
                    # Properly fill locations within dungeon
                    location.dungeon = r.dungeon_index

                    # Tell the filler that if we're placing a dungeon item, restrict it to the dungeon the item associates with
                    # This will need changed once keysanity is implemented
                    #orig_rule = location.item_rule
                    #location.item_rule = lambda item, orig_rule=orig_rule: \
                    #    (not isinstance(item, DungeonItemData) or item.dungeon_index == location.dungeon) and orig_rule(item)

            for location in r.locations:
                # If tradequests are disabled, place trade items directly in their proper location
                if not self.multiworld.tradequest[self.player] and isinstance(location, LinksAwakeningLocation) and isinstance(location.ladxr_item, TradeSequenceItem):
                    item = next(i for i in self.trade_items if i.item_data.ladxr_id == location.ladxr_item.default_item)
                    location.place_locked_item(item)

        for dungeon_index in range(0, 9):
            locs = dungeon_locations_by_dungeon[dungeon_index]
            locs = [loc for loc in locs if not loc.item]
            self.multiworld.random.shuffle(locs)
            self.multiworld.random.shuffle(self.prefill_original_dungeon[dungeon_index])
            fill_restrictive(self.multiworld, all_state, locs, self.prefill_original_dungeon[dungeon_index], lock=True)
            assert not self.prefill_original_dungeon[dungeon_index]

        # Fill dungeon items first, to not torture the fill algo
        dungeon_locations = [loc for loc in dungeon_locations if not loc.item]
        # dungeon_items = sorted(self.prefill_own_dungeons, key=lambda item: item.item_data.dungeon_item_type)
        self.multiworld.random.shuffle(self.prefill_own_dungeons)
        self.multiworld.random.shuffle(dungeon_locations)
        fill_restrictive(self.multiworld, all_state, dungeon_locations, self.prefill_own_dungeons, lock=True)

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

                    # TODO: if the item name contains "sword", use a sword icon, etc
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

        rom_path = "Legend of Zelda, The - Link's Awakening DX (USA, Europe) (SGB Enhanced).gbc"
        out_name = f"AP-{self.multiworld.seed_name}-P{self.player}-{self.multiworld.player_name[self.player]}.gbc"
        out_file = os.path.join(output_directory, out_name)

        rompath = os.path.join(output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}.gbc")



        parser = get_parser()
        args = parser.parse_args([rom_path, "-o", out_name, "--dump"])

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
            player_id = self.player)
      
        handle = open(rompath, "wb")
        rom.save(handle, name="LADXR")
        handle.close()
        patch = LADXDeltaPatch(os.path.splitext(rompath)[0]+LADXDeltaPatch.patch_file_ending, player=self.player,
                                player_name=self.multiworld.player_name[self.player], patched_path=rompath)
        patch.write()
        if not DEVELOPER_MODE:
            os.unlink(rompath)

    def generate_multi_key(self):
        return bytearray(self.multiworld.random.getrandbits(8) for _ in range(10)) + self.player.to_bytes(2, 'big')

    def modify_multidata(self, multidata: dict):
        multidata["connect_names"][binascii.hexlify(self.multi_key).decode()] = multidata["connect_names"][self.multiworld.player_name[self.player]]