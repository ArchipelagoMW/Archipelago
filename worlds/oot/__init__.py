import logging
import os
import copy
from collections import Counter

logger = logging.getLogger("Ocarina of Time")

from .Location import OOTLocation, LocationFactory
from .Entrance import OOTEntrance
from .EntranceShuffle import shuffle_random_entrances
from .Items import OOTItem, item_table, oot_data_to_ap_id
from .ItemPool import generate_itempool, get_junk_item, get_junk_pool
from .Regions import OOTRegion, TimeOfDay
from .Rules import set_rules, set_shop_rules, set_entrances_based_rules
from .RuleParser import Rule_AST_Transformer
from .Options import oot_options
from .Utils import data_path, read_json
from .LocationList import location_table, business_scrubs, set_drop_location_names
from .DungeonList import dungeon_table, create_dungeons
from .LogicTricks import known_logic_tricks
from .Rom import Rom, compress_rom_file
from .Patches import patch_rom
from .N64Patch import create_patch_file

import Utils
from BaseClasses import MultiWorld, CollectionState
from Options import Range, OptionList
from Fill import fill_restrictive, FillError
from ..AutoWorld import World

location_id_offset = 67000

class OOTWorld(World):
    game: str = "Ocarina of Time"
    options: dict = oot_options
    topology_present: bool = True
    item_name_to_id = {item_name: oot_data_to_ap_id(data, False) for item_name, data in item_table.items() if data[2] is not None}
    location_name_to_id = {name: (location_id_offset + index) for (index, name) in enumerate(location_table) 
        if location_table[name][0] not in ['Event', 'Drop', 'HintStone', 'Hint']}
    remote_items: bool = False


    def __new__(cls, world, player):
        # Add necessary objects to CollectionState on initialization
        orig_init = CollectionState.__init__
        orig_copy = CollectionState.copy

        def oot_init(self, parent: MultiWorld):
            orig_init(self, parent)
            self.child_reachable_regions = {player: set() for player in range(1, parent.players + 1)}
            self.adult_reachable_regions = {player: set() for player in range(1, parent.players + 1)}
            self.child_blocked_connections = {player: set() for player in range(1, parent.players + 1)}
            self.adult_blocked_connections = {player: set() for player in range(1, parent.players + 1)}
            self.age = {player: None for player in range(1, parent.players + 1)}

        def oot_copy(self):
            ret = orig_copy(self)
            ret.child_reachable_regions = {player: copy.copy(self.child_reachable_regions[player]) for player in
                                           range(1, self.world.players + 1)}
            ret.adult_reachable_regions = {player: copy.copy(self.adult_reachable_regions[player]) for player in
                                           range(1, self.world.players + 1)}
            ret.child_blocked_connections = {player: copy.copy(self.child_blocked_connections[player]) for player in
                                           range(1, self.world.players + 1)}
            ret.adult_blocked_connections = {player: copy.copy(self.adult_blocked_connections[player]) for player in
                                           range(1, self.world.players + 1)}
            return ret

        CollectionState.__init__ = oot_init
        CollectionState.copy = oot_copy
        # also need to add the names to the passed MultiWorld's CollectionState, since it was initialized before we could get to it
        if world:
            world.state.child_reachable_regions = {player: set() for player in range(1, world.players + 1)}
            world.state.adult_reachable_regions = {player: set() for player in range(1, world.players + 1)}
            world.state.child_blocked_connections = {player: set() for player in range(1, world.players + 1)}
            world.state.adult_blocked_connections = {player: set() for player in range(1, world.players + 1)}
            world.state.age = {player: None for player in range(1, world.players + 1)}

        return super().__new__(cls)


    def generate_early(self):
        self.rom = Rom(file=Utils.get_options()['oot_options']['rom_file'])  # a ROM must be provided, cannot produce patches without it
        self.parser = Rule_AST_Transformer(self, self.player)

        for (option_name, option) in oot_options.items(): 
            result = getattr(self.world, option_name)[self.player]
            if isinstance(result, Range): 
                option_value = int(result)
            elif isinstance(result, OptionList):
                option_value = result.value
            else:
                option_value = result.get_option_name()
            setattr(self, option_name, option_value)
        self.shop_prices = {}
        self.regions = []  # internal cache of regions for this world, used later
        self.remove_from_start_inventory = []  # some items will be precollected but not in the inventory
        self.starting_items = Counter()
        self.starting_songs = False  # whether starting_items contains a song
        self.file_hash = [self.world.random.randint(0, 31) for i in range(5)]

        # Incompatible option handling
        # ER and glitched logic are not compatible; glitched takes priority
        if self.logic_rules == 'glitched':         
            self.shuffle_interior_entrances = False
            self.shuffle_grotto_entrances = False
            self.shuffle_dungeon_entrances = False
            self.shuffle_overworld_entrances = False
            self.owl_drops = False
            self.warp_songs = False
            self.spawn_positions = False

        # Closed forest and adult start are not compatible; closed forest takes priority
        if self.open_forest == 'closed': 
            self.starting_age = 'child'

        # Determine skipped trials in GT
        # This needs to be done before the logic rules in GT are parsed
        trial_list = ['Forest', 'Fire', 'Water', 'Spirit', 'Shadow', 'Light']
        chosen_trials = self.world.random.sample(trial_list, self.trials)  # chooses a list of trials to NOT skip
        self.skipped_trials = {trial: (trial not in chosen_trials) for trial in trial_list}

        # Determine which dungeons are MQ
        # Possible future plan: allow user to pick which dungeons are MQ
        self.mq_dungeons = 0  # temporary disable for client-side issues
        mq_dungeons = self.world.random.sample(dungeon_table, self.mq_dungeons)
        self.dungeon_mq = {item['name']: (item in mq_dungeons) for item in dungeon_table}

        # Determine tricks in logic
        for trick in self.logic_tricks: 
            if trick in known_logic_tricks: 
                setattr(self, known_logic_tricks[trick]['name'], True)
            else:
                raise Exception(f'Unknown OOT logic trick for player {self.player}: {trick}')

        # Not implemented for now, but needed to placate the generator. Remove as they are implemented
        self.mq_dungeons_random = False  # this will be a deprecated option later
        self.hints = 'none'  # Hints will probably look very different in the future. disabled for now
        # Disabled due to client-side implementation issues
        self.big_poe_count = 1
        # These three are likely to never be implemented
        self.skip_child_zelda = False
        self.ocarina_songs = False
        self.correct_chest_sizes = False
        # ER options
        self.shuffle_interior_entrances = 'off'
        self.shuffle_grotto_entrances = False
        self.shuffle_dungeon_entrances = False
        self.shuffle_overworld_entrances = False
        self.owl_drops = False
        self.warp_songs = False
        self.spawn_positions = False

        # Set internal names used by the OoT generator
        self.keysanity = self.shuffle_smallkeys in ['keysanity', 'remove', 'any_dungeon', 'overworld'] # only 'keysanity' and 'remove' implemented
        self.misc_hints = True  # this is just always on
        self.ensure_tod_access = (self.shuffle_interior_entrances != 'off') or self.shuffle_overworld_entrances or self.spawn_positions
        self.entrance_shuffle = (self.shuffle_interior_entrances != 'off') or self.shuffle_grotto_entrances or self.shuffle_dungeon_entrances or \
                                self.shuffle_overworld_entrances or self.owl_drops or self.warp_songs or self.spawn_positions
        self.disable_trade_revert = (self.shuffle_interior_entrances != 'off') or self.shuffle_overworld_entrances
        self.shuffle_special_interior_entrances = self.shuffle_interior_entrances == 'all'
        self.starting_tod = self.starting_tod.replace('_', '-')  # Fixes starting time spelling: "witching_hour" -> "witching-hour"


    def load_regions_from_json(self, file_path):
        region_json = read_json(file_path)
            
        for region in region_json:
            new_region = OOTRegion(region['region_name'], None, None, self.player)
            new_region.world = self.world
            if 'scene' in region:
                new_region.scene = region['scene']
            if 'hint' in region:
                new_region.hint_text = region['hint']
            if 'dungeon' in region:
                new_region.dungeon = region['dungeon']
            if 'time_passes' in region:
                new_region.time_passes = region['time_passes']
                new_region.provides_time = TimeOfDay.ALL
            if new_region.name == 'Ganons Castle Grounds':
                new_region.provides_time = TimeOfDay.DAMPE
            if 'locations' in region:
                for location, rule in region['locations'].items():
                    new_location = LocationFactory(location, self.player)
                    if new_location.type in ['HintStone', 'Hint']:
                        continue
                    new_location.parent_region = new_region
                    new_location.rule_string = rule
                    if self.world.logic_rules != 'none':
                        self.parser.parse_spot_rule(new_location)
                    if new_location.never:
                        # We still need to fill the location even if ALR is off.
                        logger.debug('Unreachable location: %s', new_location.name)
                    new_location.player = self.player
                    new_region.locations.append(new_location)
            if 'events' in region:
                for event, rule in region['events'].items():
                    # Allow duplicate placement of events
                    lname = '%s from %s' % (event, new_region.name)
                    new_location = OOTLocation(self.player, lname, type='Event', parent=new_region)
                    new_location.rule_string = rule
                    if self.world.logic_rules != 'none':
                        self.parser.parse_spot_rule(new_location)
                    if new_location.never:
                        logger.debug('Dropping unreachable event: %s', new_location.name)
                    else:
                        new_location.player = self.player
                        new_region.locations.append(new_location)
                        self.make_event_item(event, new_location)
                        new_location.show_in_spoiler = False
            if 'exits' in region:
                for exit, rule in region['exits'].items():
                    new_exit = OOTEntrance(self.player, '%s => %s' % (new_region.name, exit), new_region)
                    new_exit.vanilla_connected_region = exit
                    new_exit.rule_string = rule
                    if self.world.logic_rules != 'none':
                        self.parser.parse_spot_rule(new_exit)
                    if new_exit.never:
                        logger.debug('Dropping unreachable exit: %s', new_exit.name)
                    else:
                        new_region.exits.append(new_exit)

            self.world.regions.append(new_region)
            self.regions.append(new_region)
        self.world._recache()


    def set_scrub_prices(self):
        # Get Deku Scrub Locations
        scrub_locations = [location for location in self.get_locations() if 'Deku Scrub' in location.name]
        scrub_dictionary = {}
        self.scrub_prices = {}
        for location in scrub_locations:
            if location.default not in scrub_dictionary:
                scrub_dictionary[location.default] = []
            scrub_dictionary[location.default].append(location)

        # Loop through each type of scrub.
        for (scrub_item, default_price, text_id, text_replacement) in business_scrubs:
            price = default_price
            if self.shuffle_scrubs == 'low':
                price = 10
            elif self.shuffle_scrubs == 'random':
                # this is a random value between 0-99
                # average value is ~33 rupees
                price = int(self.world.random.betavariate(1, 2) * 99)

            # Set price in the dictionary as well as the location.
            self.scrub_prices[scrub_item] = price
            if scrub_item in scrub_dictionary:
                for location in scrub_dictionary[scrub_item]:
                    location.price = price
                    if location.item is not None:
                        location.item.price = price


    def random_shop_prices(self):
        shop_item_indexes = ['7', '5', '8', '6']
        self.shop_prices = {}
        for region in self.regions:
            if self.shopsanity == 'random':
                shop_item_count = self.world.random.randint(0,4)
            else:
                shop_item_count = int(self.shopsanity)

            for location in region.locations:
                if location.type == 'Shop':
                    if location.name[-1:] in shop_item_indexes[:shop_item_count]:
                        self.shop_prices[location.name] = int(self.world.random.betavariate(1.5, 2) * 60) * 5


    def fill_bosses(self, bossCount=9):    
        rewardlist = (
            'Kokiri Emerald',
            'Goron Ruby',
            'Zora Sapphire',
            'Forest Medallion',
            'Fire Medallion',
            'Water Medallion',
            'Spirit Medallion',
            'Shadow Medallion',
            'Light Medallion'
        )
        boss_location_names = (
            'Queen Gohma',
            'King Dodongo',
            'Barinade',
            'Phantom Ganon',
            'Volvagia',
            'Morpha',
            'Bongo Bongo',
            'Twinrova',
            'Links Pocket'
        )
        boss_rewards = [self.create_item(reward) for reward in rewardlist]
        boss_locations = [self.world.get_location(loc, self.player) for loc in boss_location_names]

        placed_prizes = [loc.item.name for loc in boss_locations if loc.item is not None]
        unplaced_prizes = [item for item in boss_rewards if item.name not in placed_prizes]
        empty_boss_locations = [loc for loc in boss_locations if loc.item is None]
        prizepool = list(unplaced_prizes)
        prize_locs = list(empty_boss_locations)

        while bossCount:
            bossCount -= 1
            self.world.random.shuffle(prizepool)
            self.world.random.shuffle(prize_locs)
            item = prizepool.pop()
            loc = prize_locs.pop()
            self.world.push_item(loc, item, collect=False)
            loc.locked = True
            loc.event = True


    def create_item(self, name: str): 
        if name in item_table: 
            return OOTItem(name, self.player, item_table[name], False)
        return OOTItem(name, self.player, ('Event', True, None, None), True)

    def make_event_item(self, name, location, item=None):
        if item is None:
            item = self.create_item(name)
        self.world.push_item(location, item, collect=False)
        location.locked = True
        location.event = True
        if name not in item_table:
            location.internal = True
        return item


    def create_regions(self):  # create and link regions
        overworld_data_path = data_path('World', 'Overworld.json')
        menu = OOTRegion('Menu', None, None, self.player)
        start = OOTEntrance(self.player, 'New Game', menu)
        menu.exits.append(start)
        self.world.regions.append(menu)
        self.load_regions_from_json(overworld_data_path)
        start.connect(self.world.get_region('Root', self.player))
        create_dungeons(self)
        self.parser.create_delayed_rules()

        if self.shopsanity != 'off':
            self.random_shop_prices()
        self.set_scrub_prices()

        # logger.info('Setting Entrances.')
        # set_entrances(self)
        # Enforce vanilla for now
        for region in self.regions:
            for exit in region.exits:
                exit.connect(self.world.get_region(exit.vanilla_connected_region, self.player))
        if self.entrance_shuffle:
            shuffle_random_entrances(self)


    def set_rules(self): 
        set_rules(self)


    def generate_basic(self):  # generate item pools, place fixed items
        # Generate itempool
        generate_itempool(self)
        junk_pool = get_junk_pool(self)
        # Determine starting items
        for item in self.world.precollected_items: 
            if item.player != self.player:
                continue
            if item.name in self.remove_from_start_inventory:
                self.remove_from_start_inventory.remove(item.name)
            else:
                self.starting_items[item.name] += 1
                if item.type == 'Song': 
                    self.starting_songs = True
                # Call the junk fill and get a replacement
                if item in self.itempool:
                    self.itempool.remove(item)
                    self.itempool.append(self.create_item(*get_junk_item(pool=junk_pool)))
        if self.start_with_consumables: 
            self.starting_items['Deku Sticks'] = 30
            self.starting_items['Deku Nuts'] = 40
        if self.start_with_rupees: 
            self.starting_items['Rupees'] = 999

        self.world.itempool += self.itempool

        # Uniquely rename drop locations for each region and erase them from the spoiler
        set_drop_location_names(self)

        # Fill boss prizes
        self.fill_bosses()

        # relevant for both dungeon item fill and song fill
        dungeon_song_locations = [
            "Deku Tree Queen Gohma Heart",
            "Dodongos Cavern King Dodongo Heart",
            "Jabu Jabus Belly Barinade Heart",
            "Forest Temple Phantom Ganon Heart",
            "Fire Temple Volvagia Heart",
            "Water Temple Morpha Heart",
            "Shadow Temple Bongo Bongo Heart",
            "Spirit Temple Twinrova Heart",
            "Song from Impa",
            "Sheik in Ice Cavern",
            "Bottom of the Well Lens of Truth Chest", "Bottom of the Well MQ Lens of Truth Chest", # only one exists
            "Gerudo Training Grounds Maze Path Final Chest", "Gerudo Training Grounds MQ Ice Arrows Chest", # only one exists
        ]

        # Place/set rules for dungeon items
        itempools = {
            'dungeon': [],
            'overworld': [],
            'any_dungeon': [],
            'keysanity': [],
        }
        any_dungeon_locations = []
        for dungeon in self.dungeons: 
            itempools['dungeon'] = []
            # Put the dungeon items into their appropriate pools.
            # Build in reverse order since we need to fill boss key first and pop() returns the last element
            if self.shuffle_mapcompass in itempools:
                itempools[self.shuffle_mapcompass].extend(dungeon.dungeon_items)
            if self.shuffle_smallkeys in itempools:
                itempools[self.shuffle_smallkeys].extend(dungeon.small_keys)
            shufflebk = self.shuffle_bosskeys if dungeon.name != 'Ganons Castle' else self.shuffle_ganon_bosskey
            if shufflebk in itempools:
                itempools[shufflebk].extend(dungeon.boss_key)

            # We can't put a dungeon item on the end of a dungeon if a song is supposed to go there. Make sure not to include it. 
            dungeon_locations = [loc for region in dungeon.regions for loc in region.locations 
                if loc.item is None and (self.shuffle_song_items != 'dungeon' or loc.name not in dungeon_song_locations)]
            if itempools['dungeon']: # only do this if there's anything to shuffle
                self.world.random.shuffle(dungeon_locations)
                fill_restrictive(self.world, self.world.get_all_state(), dungeon_locations, itempools['dungeon'], True, True)
            any_dungeon_locations.extend(dungeon_locations)  # adds only the unfilled locations

        # Now fill items that can go into any dungeon. Retrieve the Gerudo Fortress keys from the pool if necessary
        if self.shuffle_fortresskeys == 'any_dungeon': 
            fortresskeys = list(filter(lambda item: item.player == self.player and item.type == 'FortressSmallKey', self.world.itempool))
            itempools['any_dungeon'].extend(fortresskeys)
            for key in fortresskeys:
                self.world.itempool.remove(key)
        if itempools['any_dungeon']:
            itempools['any_dungeon'].sort(key=lambda item: {'GanonBossKey': 4, 'BossKey': 3, 'SmallKey': 2, 'FortressSmallKey': 1}.get(item.type, 0))
            self.world.random.shuffle(any_dungeon_locations)
            fill_restrictive(self.world, self.world.get_all_state(), any_dungeon_locations, itempools['any_dungeon'], True, True)

        # If anything is overworld-only, enforce them as local and not in the remaining dungeon locations
        if itempools['overworld'] or self.shuffle_fortresskeys == 'overworld':
            from worlds.generic.Rules import forbid_items_for_player
            fortresskeys = {'Small Key (Gerudo Fortress)'} if self.shuffle_fortresskeys == 'overworld' else set()
            local_overworld_items = set(map(lambda item: item.name, itempools['overworld'])).union(fortresskeys)
            for location in self.world.get_locations():
                if location.player != self.player or location in any_dungeon_locations:
                    forbid_items_for_player(location, local_overworld_items, self.player)
            self.world.itempool.extend(itempools['overworld'])

        # Put all the remaining items into the general itempool
        self.world.itempool.extend(itempools['keysanity'])

        # Now that keys are in the pool, we can forbid tunics from child-only shops 
        set_entrances_based_rules(self)

        # Place songs
        # 5 built-in retries because this section can fail sometimes
        if self.shuffle_song_items != 'any': 
            tries = 5
            if self.shuffle_song_items == 'song':
                song_locations = list(filter(lambda location: location.type == 'Song', 
                    self.world.get_unfilled_locations(player=self.player)))
            elif self.shuffle_song_items == 'dungeon': 
                song_locations = list(filter(lambda location: location.name in dungeon_song_locations, 
                    self.world.get_unfilled_locations(player=self.player)))
            else:
                raise Exception(f"Unknown song shuffle type: {self.shuffle_song_items}")

            songs = list(filter(lambda item: item.player == self.player and item.type == 'Song', self.world.itempool))
            for song in songs: 
                self.world.itempool.remove(song)
            while tries:
                try:
                    self.world.random.shuffle(songs) # shuffling songs makes it less likely to fail by placing ZL last
                    self.world.random.shuffle(song_locations)
                    fill_restrictive(self.world, self.world.get_all_state(), song_locations[:], songs[:], True, True)
                    logger.debug(f"Successfully placed songs for player {self.player} after {6-tries} attempt(s)")
                    tries = 0
                except FillError as e:
                    tries -= 1
                    if tries == 0:
                        raise e
                    logger.debug(f"Failed placing songs for player {self.player}. Retries left: {tries}")
                    # undo what was done
                    for song in songs:
                        song.location = None
                        song.world = None
                    for location in song_locations:
                        location.item = None
                        location.locked = False
                        location.event = False

        # Place shop items
        # fast fill will fail because there is some logic on the shop items. we'll gather them up and place the shop items
        if self.shopsanity != 'off': 
            shop_items = list(filter(lambda item: item.player == self.player and item.type == 'Shop', self.world.itempool))
            shop_locations = list(filter(lambda location: location.type == 'Shop' and location.name not in self.shop_prices, 
                self.world.get_unfilled_locations(player=self.player)))
            self.world.random.shuffle(shop_locations)
            for item in shop_items: 
                self.world.itempool.remove(item)
            fill_restrictive(self.world, self.world.get_all_state(), shop_locations, shop_items, True, True)
        set_shop_rules(self)


        # Kill unreachable events that can't be gotten even with all items
        # Make sure to only kill actual internal events, not in-game "events"
        all_state = self.world.get_all_state()
        all_state.sweep_for_events()
        all_locations = [loc for loc in self.world.get_locations() if loc.player == self.player]
        reachable = self.world.get_reachable_locations(all_state, self.player)
        unreachable = [loc for loc in all_locations if loc.internal and loc.event and loc.locked and loc not in reachable]
        for loc in unreachable: 
            loc.parent_region.locations.remove(loc)
        # Exception: Sell Big Poe is an event which is only reachable if Bottle with Big Poe is in the item pool. 
        # We allow it to be removed only if Bottle with Big Poe is not in the itempool.
        bigpoe = self.world.get_location('Sell Big Poe from Market Guard House', self.player)
        if not all_state.has('Bottle with Big Poe', self.player) and bigpoe not in reachable:
            bigpoe.parent_region.locations.remove(bigpoe)
        self.world.clear_location_cache()
            

    # For now we will always output a patch file.
    def generate_output(self, output_directory: str): 
        outfile_name = f"AP_{self.world.seed_name}_P{self.player}_{self.world.get_player_names(self.player)}"
        patch_rom(self, self.rom)
        # patch cosmetics here
        self.rom.update_header()

        # make patch file
        create_patch_file(self.rom, Utils.output_path(output_directory, outfile_name+'.apz5'))

        # produce uncompressed file path, compress if desired
        # TODO: remove this once client can patch
        # filename_uncompressed = Utils.output_path(outfile_name+'.z64')
        # filename_compressed = Utils.output_path(outfile_name+'-comp.z64')
        # self.rom.write_to_file(filename_uncompressed)
        # logger.info(f"Compressing OOT ROM file for player {self.player}. This might take a while...")
        # compress_rom_file(filename_uncompressed, filename_compressed)
        # os.remove(filename_uncompressed)

        self.rom.restore()


    # Helper functions
    def get_shuffled_entrances(self):
        return []

    def get_locations(self):
        return [loc for region in self.regions for loc in region.locations]

    def get_location(self, location): 
        return self.world.get_location(location, self.player)

    def get_region(self, region):
        return self.world.get_region(region, self.player)
