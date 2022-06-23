import logging
import threading
import copy
from collections import Counter

logger = logging.getLogger("Ocarina of Time")

from .Location import OOTLocation, LocationFactory, location_name_to_id
from .Entrance import OOTEntrance
from .EntranceShuffle import shuffle_random_entrances, entrance_shuffle_table, EntranceShuffleError
from .Items import OOTItem, item_table, oot_data_to_ap_id
from .ItemPool import generate_itempool, add_dungeon_items, get_junk_item, get_junk_pool
from .Regions import OOTRegion, TimeOfDay
from .Rules import set_rules, set_shop_rules, set_entrances_based_rules
from .RuleParser import Rule_AST_Transformer
from .Options import oot_options
from .Utils import data_path, read_json
from .LocationList import business_scrubs, set_drop_location_names
from .DungeonList import dungeon_table, create_dungeons
from .LogicTricks import normalized_name_tricks
from .Rom import Rom
from .Patches import patch_rom
from .N64Patch import create_patch_file
from .Cosmetics import patch_cosmetics
from .Hints import hint_dist_keys, get_hint_area, buildWorldGossipHints
from .HintList import getRequiredHints
from .SaveContext import SaveContext

from Utils import get_options, output_path
from BaseClasses import MultiWorld, CollectionState, RegionType, Tutorial
from Options import Range, Toggle, OptionList
from Fill import fill_restrictive, FillError
from worlds.generic.Rules import exclusion_rules
from ..AutoWorld import World, AutoLogicRegister, WebWorld

location_id_offset = 67000

# OoT's generate_output doesn't benefit from more than 2 threads, instead it uses a lot of memory.
i_o_limiter = threading.Semaphore(2)


class OOTCollectionState(metaclass=AutoLogicRegister):
    def init_mixin(self, parent: MultiWorld):
        all_ids = parent.get_all_ids()
        self.child_reachable_regions = {player: set() for player in all_ids}
        self.adult_reachable_regions = {player: set() for player in all_ids}
        self.child_blocked_connections = {player: set() for player in all_ids}
        self.adult_blocked_connections = {player: set() for player in all_ids}
        self.day_reachable_regions = {player: set() for player in all_ids}
        self.dampe_reachable_regions = {player: set() for player in all_ids}
        self.age = {player: None for player in all_ids}

    def copy_mixin(self, ret) -> CollectionState:
        ret.child_reachable_regions = {player: copy.copy(self.child_reachable_regions[player]) for player in
                                       self.child_reachable_regions}
        ret.adult_reachable_regions = {player: copy.copy(self.adult_reachable_regions[player]) for player in
                                       self.adult_reachable_regions}
        ret.child_blocked_connections = {player: copy.copy(self.child_blocked_connections[player]) for player in
                                         self.child_blocked_connections}
        ret.adult_blocked_connections = {player: copy.copy(self.adult_blocked_connections[player]) for player in
                                         self.adult_blocked_connections}
        ret.day_reachable_regions = {player: copy.copy(self.adult_reachable_regions[player]) for player in
                                     self.day_reachable_regions}
        ret.dampe_reachable_regions = {player: copy.copy(self.adult_reachable_regions[player]) for player in
                                       self.dampe_reachable_regions}
        return ret


class OOTWeb(WebWorld):
    setup = Tutorial(
        "Multiworld Setup Tutorial",
        "A guide to setting up the Archipelago Ocarina of Time software on your computer.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Edos"]
    )

    setup_es = Tutorial(
        setup.tutorial_name,
        setup.description,
        "Español",
        "setup_es.md",
        "setup/es",
        setup.author
    )

    tutorials = [setup, setup_es]


class OOTWorld(World):
    """
    The Legend of Zelda: Ocarina of Time is a 3D action/adventure game. Travel through Hyrule in two time periods, 
    learn magical ocarina songs, and explore twelve dungeons on your quest. Use Link's many items and abilities 
    to rescue the Seven Sages, and then confront Ganondorf to save Hyrule!
    """
    game: str = "Ocarina of Time"
    options: dict = oot_options
    topology_present: bool = True
    item_name_to_id = {item_name: oot_data_to_ap_id(data, False) for item_name, data in item_table.items() if
                       data[2] is not None}
    location_name_to_id = location_name_to_id
    remote_items: bool = False
    remote_start_inventory: bool = False
    web = OOTWeb()

    data_version = 2

    required_client_version = (0, 3, 2)

    def __init__(self, world, player):
        self.hint_data_available = threading.Event()
        super(OOTWorld, self).__init__(world, player)

    @classmethod
    def stage_assert_generate(cls, world: MultiWorld):
        rom = Rom(file=get_options()['oot_options']['rom_file'])

    def generate_early(self):
        # Player name MUST be at most 16 bytes ascii-encoded, otherwise won't write to ROM correctly
        if len(bytes(self.world.get_player_name(self.player), 'ascii')) > 16:
            raise Exception(
                f"OoT: Player {self.player}'s name ({self.world.get_player_name(self.player)}) must be ASCII-compatible")

        self.parser = Rule_AST_Transformer(self, self.player)

        for (option_name, option) in oot_options.items():
            result = getattr(self.world, option_name)[self.player]
            if isinstance(result, Range):
                option_value = int(result)
            elif isinstance(result, Toggle):
                option_value = bool(result)
            elif isinstance(result, OptionList):
                option_value = result.value
            else:
                option_value = result.current_key
            setattr(self, option_name, option_value)

        self.shop_prices = {}
        self.regions = []  # internal cache of regions for this world, used later
        self.remove_from_start_inventory = []  # some items will be precollected but not in the inventory
        self.starting_items = Counter()
        self.starting_songs = False  # whether starting_items contains a song
        self.file_hash = [self.world.random.randint(0, 31) for i in range(5)]

        self.item_name_groups = {
            "medallions": {"Light Medallion", "Forest Medallion", "Fire Medallion", "Water Medallion",
                           "Shadow Medallion", "Spirit Medallion"},
            "stones": {"Kokiri Emerald", "Goron Ruby", "Zora Sapphire"},
            "rewards": {"Light Medallion", "Forest Medallion", "Fire Medallion", "Water Medallion", "Shadow Medallion",
                        "Spirit Medallion", \
                        "Kokiri Emerald", "Goron Ruby", "Zora Sapphire"},
            "bottles": {"Bottle", "Bottle with Milk", "Deliver Letter", "Sell Big Poe", "Bottle with Red Potion",
                        "Bottle with Green Potion", \
                        "Bottle with Blue Potion", "Bottle with Fairy", "Bottle with Fish", "Bottle with Blue Fire",
                        "Bottle with Bugs", "Bottle with Poe"}
        }

        # Incompatible option handling
        # ER and glitched logic are not compatible; glitched takes priority
        if self.logic_rules == 'glitched':
            self.shuffle_interior_entrances = 'off'
            self.shuffle_grotto_entrances = False
            self.shuffle_dungeon_entrances = False
            self.shuffle_overworld_entrances = False
            self.owl_drops = False
            self.warp_songs = False
            self.spawn_positions = False

        # Closed forest and adult start are not compatible; closed forest takes priority
        if self.open_forest == 'closed':
            self.starting_age = 'child'
            # These ER options force closed forest to become closed deku
            if (self.shuffle_interior_entrances == 'all' or self.shuffle_overworld_entrances or self.warp_songs or self.spawn_positions):
                self.open_forest = 'closed_deku'

        # Skip child zelda and shuffle egg are not compatible; skip-zelda takes priority
        if self.skip_child_zelda:
            self.shuffle_weird_egg = False

        # Determine skipped trials in GT
        # This needs to be done before the logic rules in GT are parsed
        trial_list = ['Forest', 'Fire', 'Water', 'Spirit', 'Shadow', 'Light']
        chosen_trials = self.world.random.sample(trial_list, self.trials)  # chooses a list of trials to NOT skip
        self.skipped_trials = {trial: (trial not in chosen_trials) for trial in trial_list}

        # Determine which dungeons are MQ
        # Possible future plan: allow user to pick which dungeons are MQ
        mq_dungeons = self.world.random.sample(dungeon_table, self.mq_dungeons)
        self.dungeon_mq = {item['name']: (item in mq_dungeons) for item in dungeon_table}

        # Determine tricks in logic
        if self.logic_rules == 'glitchless':
            for trick in self.logic_tricks:
                normalized_name = trick.casefold()
                if normalized_name in normalized_name_tricks:
                    setattr(self, normalized_name_tricks[normalized_name]['name'], True)
                else:
                    raise Exception(f'Unknown OOT logic trick for player {self.player}: {trick}')

        # No Logic forces all tricks on, prog balancing off and beatable-only
        elif self.logic_rules == 'no_logic':
            self.world.progression_balancing[self.player].value = False
            self.world.accessibility[self.player] = self.world.accessibility[self.player].from_text("minimal")
            for trick in normalized_name_tricks.values():
                setattr(self, trick['name'], True)

        # Not implemented for now, but needed to placate the generator. Remove as they are implemented
        self.mq_dungeons_random = False  # this will be a deprecated option later
        self.ocarina_songs = False  # just need to pull in the OcarinaSongs module
        self.mix_entrance_pools = False
        self.decouple_entrances = False

        # Set internal names used by the OoT generator
        self.keysanity = self.shuffle_smallkeys in ['keysanity', 'remove', 'any_dungeon', 'overworld']

        # Hint stuff
        self.clearer_hints = True  # this is being enforced since non-oot items do not have non-clear hint text
        self.gossip_hints = {}
        self.required_locations = []
        self.empty_areas = {}
        self.major_item_locations = []

        # ER names
        self.ensure_tod_access = (self.shuffle_interior_entrances != 'off') or self.shuffle_overworld_entrances or self.spawn_positions
        self.entrance_shuffle = (self.shuffle_interior_entrances != 'off') or self.shuffle_grotto_entrances or self.shuffle_dungeon_entrances or \
                                self.shuffle_overworld_entrances or self.owl_drops or self.warp_songs or self.spawn_positions
        self.disable_trade_revert = (self.shuffle_interior_entrances != 'off') or self.shuffle_overworld_entrances
        self.shuffle_special_interior_entrances = self.shuffle_interior_entrances == 'all'

        # Convert the double option used by shopsanity into a single option
        if self.shopsanity == 'random_number':
            self.shopsanity = 'random'
        elif self.shopsanity == 'fixed_number':
            self.shopsanity = str(self.shop_slots)

        # fixing some options
        # Fixes starting time spelling: "witching_hour" -> "witching-hour"
        self.starting_tod = self.starting_tod.replace('_', '-')
        self.shuffle_scrubs = self.shuffle_scrubs.replace('_prices', '')

        # Get hint distribution
        self.hint_dist_user = read_json(data_path('Hints', f'{self.hint_dist}.json'))

        self.added_hint_types = {}
        self.item_added_hint_types = {}
        self.hint_exclusions = set()
        if self.skip_child_zelda:
            self.hint_exclusions.add('Song from Impa')
        self.hint_type_overrides = {}
        self.item_hint_type_overrides = {}

        # unused hint stuff
        self.named_item_pool = {}
        self.hint_text_overrides = {}

        for dist in hint_dist_keys:
            self.added_hint_types[dist] = []
            for loc in self.hint_dist_user['add_locations']:
                if 'types' in loc:
                    if dist in loc['types']:
                        self.added_hint_types[dist].append(loc['location'])
            self.item_added_hint_types[dist] = []
            for i in self.hint_dist_user['add_items']:
                if dist in i['types']:
                    self.item_added_hint_types[dist].append(i['item'])
            self.hint_type_overrides[dist] = []
            for loc in self.hint_dist_user['remove_locations']:
                if dist in loc['types']:
                    self.hint_type_overrides[dist].append(loc['location'])
            self.item_hint_type_overrides[dist] = []
            for i in self.hint_dist_user['remove_items']:
                if dist in i['types']:
                    self.item_hint_type_overrides[dist].append(i['item'])

        self.always_hints = [hint.name for hint in getRequiredHints(self)]

        # Determine items which are not considered advancement based on settings. They will never be excluded.
        self.nonadvancement_items = {'Double Defense', 'Ice Arrows'}
        if (self.damage_multiplier != 'ohko' and self.damage_multiplier != 'quadruple' and
                self.shuffle_scrubs == 'off' and not self.shuffle_grotto_entrances):
            # nayru's love may be required to prevent forced damage
            self.nonadvancement_items.add('Nayrus Love')
        if getattr(self, 'logic_grottos_without_agony', False) and self.hints != 'agony':
            # Stone of Agony skippable if not used for hints or grottos
            self.nonadvancement_items.add('Stone of Agony')
        if (not self.shuffle_special_interior_entrances and not self.shuffle_overworld_entrances and
                not self.warp_songs and not self.spawn_positions):
            # Serenade and Prelude are never required unless one of those settings is enabled
            self.nonadvancement_items.add('Serenade of Water')
            self.nonadvancement_items.add('Prelude of Light')
        if self.logic_rules == 'glitchless':
            # Both two-handed swords can be required in glitch logic, so only consider them nonprogression in glitchless
            self.nonadvancement_items.add('Biggoron Sword')
            self.nonadvancement_items.add('Giants Knife')
            if not getattr(self, 'logic_water_central_gs_fw', False):
                # Farore's Wind skippable if not used for this logic trick in Water Temple
                self.nonadvancement_items.add('Farores Wind')

    def load_regions_from_json(self, file_path):
        region_json = read_json(file_path)

        for region in region_json:
            new_region = OOTRegion(region['region_name'], RegionType.Generic, None, self.player)
            new_region.world = self.world
            if 'pretty_name' in region:
                new_region.pretty_name = region['pretty_name']
            if 'font_color' in region:
                new_region.font_color = region['font_color']
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
                    new_exit = OOTEntrance(self.player, self.world, '%s -> %s' % (new_region.name, exit), new_region)
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
                shop_item_count = self.world.random.randint(0, 4)
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
        prizepool = [item for item in boss_rewards if item.name not in placed_prizes]
        prize_locs = [loc for loc in boss_locations if loc.item is None]

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
            return OOTItem(name, self.player, item_table[name], False,
                           (name in self.nonadvancement_items if getattr(self, 'nonadvancement_items',
                                                                         None) else False))
        return OOTItem(name, self.player, ('Event', True, None, None), True, False)

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
        if self.logic_rules == 'glitchless' or self.logic_rules == 'no_logic':  # enables ER + NL
            world_type = 'World'
        else:
            world_type = 'Glitched World'
        overworld_data_path = data_path(world_type, 'Overworld.json')
        menu = OOTRegion('Menu', None, None, self.player)
        start = OOTEntrance(self.player, self.world, 'New Game', menu)
        menu.exits.append(start)
        self.world.regions.append(menu)
        self.load_regions_from_json(overworld_data_path)
        start.connect(self.world.get_region('Root', self.player))
        create_dungeons(self)
        self.parser.create_delayed_rules()

        if self.shopsanity != 'off':
            self.random_shop_prices()
        self.set_scrub_prices()

        # Bind entrances to vanilla
        for region in self.regions:
            for exit in region.exits:
                exit.connect(self.world.get_region(exit.vanilla_connected_region, self.player))

    def create_items(self):
        # Generate itempool
        generate_itempool(self)
        add_dungeon_items(self)
        junk_pool = get_junk_pool(self)
        removed_items = []
        # Determine starting items
        for item in self.world.precollected_items[self.player]:
            if item.name in self.remove_from_start_inventory:
                self.remove_from_start_inventory.remove(item.name)
                removed_items.append(item.name)
            else:
                if item.name not in SaveContext.giveable_items:
                    raise Exception(f"Invalid OoT starting item: {item.name}")
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
        self.remove_from_start_inventory.extend(removed_items)

    def set_rules(self):
        # This has to run AFTER creating items but BEFORE set_entrances_based_rules
        if self.entrance_shuffle:
            # 10 attempts at shuffling entrances
            tries = 10
            while tries:
                try:
                    shuffle_random_entrances(self)
                except EntranceShuffleError as e:
                    tries -= 1
                    logger.debug(
                        f"Failed shuffling entrances for world {self.player}, retrying {tries} more times")
                    if tries == 0:
                        raise e
                    # Restore original state and delete assumed entrances
                    for entrance in self.get_shuffled_entrances():
                        if entrance.connected_region is not None:
                            entrance.disconnect()
                        entrance.connect(self.world.get_region(entrance.vanilla_connected_region, self.player))
                        if entrance.assumed:
                            assumed_entrance = entrance.assumed
                            if assumed_entrance.connected_region is not None:
                                assumed_entrance.disconnect()
                            del assumed_entrance
                        entrance.reverse = None
                        entrance.replaces = None
                        entrance.assumed = None
                        entrance.shuffled = False
                    # Clean up root entrances
                    root = self.get_region("Root Exits")
                    root.exits = root.exits[:8]
                else:
                    break

        set_rules(self)
        set_entrances_based_rules(self)

    def generate_basic(self):  # mostly killing locations that shouldn't exist by settings

        # Fill boss prizes. needs to happen before killing unreachable locations
        self.fill_bosses()

        # Uniquely rename drop locations for each region and erase them from the spoiler
        set_drop_location_names(self)

        # Gather items for ice trap appearances
        self.fake_items = []
        if self.ice_trap_appearance in ['major_only', 'anything']:
            self.fake_items.extend(item for item in self.itempool if item.index and self.is_major_item(item))
        if self.ice_trap_appearance in ['junk_only', 'anything']:
            self.fake_items.extend(item for item in self.itempool if
                                   item.index and not item.type == 'Shop' and not self.is_major_item(item) and item.name != 'Ice Trap')

        # Kill unreachable events that can't be gotten even with all items
        # Make sure to only kill actual internal events, not in-game "events"
        all_state = self.world.get_all_state(False)
        all_locations = self.get_locations()
        reachable = self.world.get_reachable_locations(all_state, self.player)
        unreachable = [loc for loc in all_locations if
                       (loc.internal or loc.type == 'Drop') and loc.event and loc.locked and loc not in reachable]
        for loc in unreachable:
            loc.parent_region.locations.remove(loc)
        # Exception: Sell Big Poe is an event which is only reachable if Bottle with Big Poe is in the item pool. 
        # We allow it to be removed only if Bottle with Big Poe is not in the itempool.
        bigpoe = self.world.get_location('Sell Big Poe from Market Guard House', self.player)
        if not all_state.has('Bottle with Big Poe', self.player) and bigpoe not in reachable:
            bigpoe.parent_region.locations.remove(bigpoe)
        self.world.clear_location_cache()

        # If fast scarecrow then we need to kill the Pierre location as it will be unreachable
        if self.free_scarecrow:
            loc = self.world.get_location("Pierre", self.player)
            loc.parent_region.locations.remove(loc)
        # If open zora's domain then we need to kill Deliver Rutos Letter
        if self.zora_fountain == 'open':
            loc = self.world.get_location("Deliver Rutos Letter", self.player)
            loc.parent_region.locations.remove(loc)

    def pre_fill(self):

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
            # only one exists
            "Bottom of the Well Lens of Truth Chest", "Bottom of the Well MQ Lens of Truth Chest",
            # only one exists
            "Gerudo Training Ground Maze Path Final Chest", "Gerudo Training Ground MQ Ice Arrows Chest",
        ]

        # Place/set rules for dungeon items
        itempools = {
            'dungeon': [],
            'overworld': [],
            'any_dungeon': [],
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
                                 if loc.item is None and (
                                         self.shuffle_song_items != 'dungeon' or loc.name not in dungeon_song_locations)]
            if itempools['dungeon']:  # only do this if there's anything to shuffle
                for item in itempools['dungeon']:
                    self.world.itempool.remove(item)
                self.world.random.shuffle(dungeon_locations)
                fill_restrictive(self.world, self.world.get_all_state(False), dungeon_locations,
                                 itempools['dungeon'], True, True)
            any_dungeon_locations.extend(dungeon_locations)  # adds only the unfilled locations

        # Now fill items that can go into any dungeon. Retrieve the Gerudo Fortress keys from the pool if necessary
        if self.shuffle_fortresskeys == 'any_dungeon':
            fortresskeys = filter(lambda item: item.player == self.player and item.type == 'HideoutSmallKey',
                                  self.world.itempool)
            itempools['any_dungeon'].extend(fortresskeys)
        if itempools['any_dungeon']:
            for item in itempools['any_dungeon']:
                self.world.itempool.remove(item)
            itempools['any_dungeon'].sort(key=lambda item:
            {'GanonBossKey': 4, 'BossKey': 3, 'SmallKey': 2, 'HideoutSmallKey': 1}.get(item.type, 0))
            self.world.random.shuffle(any_dungeon_locations)
            fill_restrictive(self.world, self.world.get_all_state(False), any_dungeon_locations,
                             itempools['any_dungeon'], True, True)

        # If anything is overworld-only, fill into local non-dungeon locations
        if self.shuffle_fortresskeys == 'overworld':
            fortresskeys = filter(lambda item: item.player == self.player and item.type == 'HideoutSmallKey',
                                  self.world.itempool)
            itempools['overworld'].extend(fortresskeys)
        if itempools['overworld']:
            for item in itempools['overworld']:
                self.world.itempool.remove(item)
            itempools['overworld'].sort(key=lambda item:
            {'GanonBossKey': 4, 'BossKey': 3, 'SmallKey': 2, 'HideoutSmallKey': 1}.get(item.type, 0))
            non_dungeon_locations = [loc for loc in self.get_locations() if
                                     not loc.item and loc not in any_dungeon_locations and
                                     (loc.type != 'Shop' or loc.name in self.shop_prices) and
                                     (loc.type != 'Song' or self.shuffle_song_items != 'song') and
                                     (loc.name not in dungeon_song_locations or self.shuffle_song_items != 'dungeon')]
            self.world.random.shuffle(non_dungeon_locations)
            fill_restrictive(self.world, self.world.get_all_state(False), non_dungeon_locations,
                             itempools['overworld'], True, True)

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

            important_warps = (self.shuffle_special_interior_entrances or self.shuffle_overworld_entrances or
                               self.warp_songs or self.spawn_positions)
            song_order = {
                'Zeldas Lullaby': 1,
                'Eponas Song': 1,
                'Sarias Song': 3 if important_warps else 0,
                'Suns Song': 0,
                'Song of Time': 0,
                'Song of Storms': 3,
                'Minuet of Forest': 2 if important_warps else 0,
                'Bolero of Fire': 2 if important_warps else 0,
                'Serenade of Water': 2 if important_warps else 0,
                'Requiem of Spirit': 2,
                'Nocturne of Shadow': 2,
                'Prelude of Light': 2 if important_warps else 0,
            }
            songs.sort(key=lambda song: song_order.get(song.name, 0))

            while tries:
                try:
                    self.world.random.shuffle(song_locations)
                    fill_restrictive(self.world, self.world.get_all_state(False), song_locations[:], songs[:],
                                     True, True)
                    logger.debug(f"Successfully placed songs for player {self.player} after {6 - tries} attempt(s)")
                except FillError as e:
                    tries -= 1
                    if tries == 0:
                        raise Exception(f"Failed placing songs for player {self.player}. Error cause: {e}")
                    logger.debug(f"Failed placing songs for player {self.player}. Retries left: {tries}")
                    # undo what was done
                    for song in songs:
                        song.location = None
                        song.world = None
                    for location in song_locations:
                        location.item = None
                        location.locked = False
                        location.event = False
                else:
                    break

        # Place shop items
        # fast fill will fail because there is some logic on the shop items. we'll gather them up and place the shop items
        if self.shopsanity != 'off':
            shop_items = list(
                filter(lambda item: item.player == self.player and item.type == 'Shop', self.world.itempool))
            shop_locations = list(
                filter(lambda location: location.type == 'Shop' and location.name not in self.shop_prices,
                       self.world.get_unfilled_locations(player=self.player)))
            shop_items.sort(key=lambda item: {
                'Buy Deku Shield': 3 * int(self.open_forest == 'closed'),
                'Buy Goron Tunic': 2,
                'Buy Zora Tunic': 2
            }.get(item.name,
                  int(item.advancement)))  # place Deku Shields if needed, then tunics, then other advancement, then junk
            self.world.random.shuffle(shop_locations)
            for item in shop_items:
                self.world.itempool.remove(item)
            fill_restrictive(self.world, self.world.get_all_state(False), shop_locations, shop_items, True, True)
        set_shop_rules(self)  # sets wallet requirements on shop items, must be done after they are filled

        # If skip child zelda is active and Song from Impa is unfilled, put a local giveable item into it.
        impa = self.world.get_location("Song from Impa", self.player)
        if self.skip_child_zelda:
            if impa.item is None:
                item_to_place = self.world.random.choice(list(item for item in self.world.itempool if
                                                              item.player == self.player and item.name in SaveContext.giveable_items))
                impa.place_locked_item(item_to_place)
                self.world.itempool.remove(item_to_place)
            # Give items to startinventory
            self.world.push_precollected(impa.item)
            self.world.push_precollected(self.create_item("Zeldas Letter"))

        # Exclude locations in Ganon's Castle proportional to the number of items required to make the bridge
        # Check for dungeon ER later
        if self.logic_rules == 'glitchless':
            if self.bridge == 'medallions':
                ganon_junk_fill = self.bridge_medallions / 9
            elif self.bridge == 'stones':
                ganon_junk_fill = self.bridge_stones / 9
            elif self.bridge == 'dungeons':
                ganon_junk_fill = self.bridge_rewards / 9
            elif self.bridge == 'vanilla':
                ganon_junk_fill = 2 / 9
            elif self.bridge == 'tokens':
                ganon_junk_fill = self.bridge_tokens / 100
            elif self.bridge == 'open':
                ganon_junk_fill = 0
            else:
                raise Exception("Unexpected bridge setting")

            gc = next(filter(lambda dungeon: dungeon.name == 'Ganons Castle', self.dungeons))
            locations = [loc.name for region in gc.regions for loc in region.locations if loc.item is None]
            junk_fill_locations = self.world.random.sample(locations, round(len(locations) * ganon_junk_fill))
            exclusion_rules(self.world, self.player, junk_fill_locations)

        # Locations which are not sendable must be converted to events
        # This includes all locations for which show_in_spoiler is false, and shuffled shop items.
        for loc in self.get_locations():
            if loc.address is not None and (
                    not loc.show_in_spoiler or (loc.item is not None and loc.item.type == 'Shop')
                    or (self.skip_child_zelda and loc.name in ['HC Zeldas Letter', 'Song from Impa'])):
                loc.address = None

    def generate_output(self, output_directory: str):
        if self.hints != 'none':
            self.hint_data_available.wait()

        with i_o_limiter:
            # Make traps appear as other random items
            ice_traps = [loc.item for loc in self.get_locations() if loc.item.trap]
            for trap in ice_traps:
                trap.looks_like_item = self.create_item(self.world.slot_seeds[self.player].choice(self.fake_items).name)

            # Seed hint RNG, used for ganon text lines also
            self.hint_rng = self.world.slot_seeds[self.player]

            outfile_name = f"AP_{self.world.seed_name}_P{self.player}_{self.world.get_file_safe_player_name(self.player)}"
            rom = Rom(file=get_options()['oot_options']['rom_file'])
            if self.hints != 'none':
                buildWorldGossipHints(self)
            patch_rom(self, rom)
            patch_cosmetics(self, rom)
            rom.update_header()
            create_patch_file(rom, output_path(output_directory, outfile_name + '.apz5'))
            rom.restore()

            # Write entrances to spoiler log
            all_entrances = self.get_shuffled_entrances()
            all_entrances.sort(key=lambda x: x.name)
            all_entrances.sort(key=lambda x: x.type)
            if not self.decouple_entrances:
                for loadzone in all_entrances:
                    if loadzone.primary:
                        entrance = loadzone
                    else:
                        entrance = loadzone.reverse
                    if entrance.reverse is not None:
                        self.world.spoiler.set_entrance(entrance, entrance.replaces.reverse, 'both', self.player)
                    else:
                        self.world.spoiler.set_entrance(entrance, entrance.replaces, 'entrance', self.player)
            else:
                for entrance in all_entrances:
                    self.world.spoiler.set_entrance(entrance, entrance.replaces, 'entrance', self.player)

    # Gathers hint data for OoT. Loops over all world locations for woth, barren, and major item locations.
    @classmethod
    def stage_generate_output(cls, world: MultiWorld, output_directory: str):
        def hint_type_players(hint_type: str) -> set:
            return {autoworld.player for autoworld in world.get_game_worlds("Ocarina of Time")
                    if autoworld.hints != 'none' and autoworld.hint_dist_user['distribution'][hint_type]['copies'] > 0}

        try:
            item_hint_players = hint_type_players('item')
            barren_hint_players = hint_type_players('barren')
            woth_hint_players = hint_type_players('woth')

            items_by_region = {}
            for player in barren_hint_players:
                items_by_region[player] = {}
                for r in world.worlds[player].regions:
                    items_by_region[player][r.hint_text] = {'dungeon': False, 'weight': 0, 'is_barren': True}
                for d in world.worlds[player].dungeons:
                    items_by_region[player][d.hint_text] = {'dungeon': True, 'weight': 0, 'is_barren': True}
                del (items_by_region[player]["Link's Pocket"])
                del (items_by_region[player][None])

            if item_hint_players:  # loop once over all locations to gather major items. Check oot locations for barren/woth if needed
                for loc in world.get_locations():
                    player = loc.item.player
                    autoworld = world.worlds[player]
                    if ((player in item_hint_players and (autoworld.is_major_item(loc.item) or loc.item.name in autoworld.item_added_hint_types['item']))
                                or (loc.player in item_hint_players and loc.name in world.worlds[loc.player].added_hint_types['item'])):
                        autoworld.major_item_locations.append(loc)

                    if loc.game == "Ocarina of Time" and loc.item.code and (not loc.locked or
                        (loc.item.type == 'Song' or
                            (loc.item.type == 'SmallKey'         and world.worlds[loc.player].shuffle_smallkeys     == 'any_dungeon') or
                            (loc.item.type == 'HideoutSmallKey'  and world.worlds[loc.player].shuffle_fortresskeys  == 'any_dungeon') or
                            (loc.item.type == 'BossKey'          and world.worlds[loc.player].shuffle_bosskeys      == 'any_dungeon') or
                            (loc.item.type == 'GanonBossKey'     and world.worlds[loc.player].shuffle_ganon_bosskey == 'any_dungeon'))):
                        if loc.player in barren_hint_players:
                            hint_area = get_hint_area(loc)
                            items_by_region[loc.player][hint_area]['weight'] += 1
                            if loc.item.advancement or loc.item.useful:
                                items_by_region[loc.player][hint_area]['is_barren'] = False
                        if loc.player in woth_hint_players and loc.item.advancement:
                            # Skip item at location and see if game is still beatable
                            state = CollectionState(world)
                            state.locations_checked.add(loc)
                            if not world.can_beat_game(state):
                                world.worlds[loc.player].required_locations.append(loc)
            elif barren_hint_players or woth_hint_players:  # Check only relevant oot locations for barren/woth
                for player in (barren_hint_players | woth_hint_players):
                    for loc in world.worlds[player].get_locations():
                        if loc.item.code and (not loc.locked or loc.item.type == 'Song'):
                            if player in barren_hint_players:
                                hint_area = get_hint_area(loc)
                                items_by_region[player][hint_area]['weight'] += 1
                                if loc.item.advancement:
                                    items_by_region[player][hint_area]['is_barren'] = False
                            if player in woth_hint_players and loc.item.advancement:
                                state = CollectionState(world)
                                state.locations_checked.add(loc)
                                if not world.can_beat_game(state):
                                    world.worlds[player].required_locations.append(loc)
            for player in barren_hint_players:
                world.worlds[player].empty_areas = {region: info for (region, info) in items_by_region[player].items()
                                                    if info['is_barren']}
        except Exception as e:
            raise e
        finally:
            for autoworld in world.get_game_worlds("Ocarina of Time"):
                autoworld.hint_data_available.set()

    def modify_multidata(self, multidata: dict):

        hint_entrances = set()
        for entrance in entrance_shuffle_table:
            hint_entrances.add(entrance[1][0])
            if len(entrance) > 2:
                hint_entrances.add(entrance[2][0])

        # Get main hint entrance to region.
        # If the region is directly adjacent to a hint-entrance, we return that one.
        # If it's in a dungeon, scan all the entrances for all the regions in the dungeon.
        #   This should terminate on the first region anyway, but we scan everything to be safe.
        # If it's one of the special cases, go one level deeper.
        # Otherwise return None.
        def get_entrance_to_region(region):
            special_case_regions = {
                "Beyond Door of Time",
                "Kak Impas House Near Cow",
            }

            for entrance in region.entrances:
                if entrance.name in hint_entrances:
                    return entrance
            if region.dungeon is not None:
                for r in region.dungeon.regions:
                    for e in r.entrances:
                        if e.name in hint_entrances:
                            return e
            if region.name in special_case_regions:
                return get_entrance_to_region(region.entrances[0].parent_region)
            return None

        # Remove undesired items from start_inventory
        # This is because we don't want them to show up in the autotracker,
        # they just don't exist in-game.
        for item_name in self.remove_from_start_inventory:
            item_id = self.item_name_to_id.get(item_name, None)
            if item_id is None:
                continue
            multidata["precollected_items"][self.player].remove(item_id)

        # Add ER hint data
        if self.shuffle_interior_entrances != 'off' or self.shuffle_dungeon_entrances or self.shuffle_grotto_entrances:
            er_hint_data = {}
            for region in self.regions:
                if not any(bool(loc.address) for loc in region.locations): # check if region has any non-event locations
                    continue
                main_entrance = get_entrance_to_region(region)
                if main_entrance is not None and main_entrance.shuffled:
                    for location in region.locations:
                        if type(location.address) == int:
                            er_hint_data[location.address] = main_entrance.name
            multidata['er_hint_data'][self.player] = er_hint_data

    # Helper functions
    def get_shufflable_entrances(self, type=None, only_primary=False):
        return [entrance for entrance in self.world.get_entrances() if (entrance.player == self.player and
                                                                        (type == None or entrance.type == type) and
                                                                        (not only_primary or entrance.primary))]

    def get_shuffled_entrances(self, type=None, only_primary=False):
        return [entrance for entrance in self.get_shufflable_entrances(type=type, only_primary=only_primary) if
                entrance.shuffled]

    def get_locations(self):
        for region in self.regions:
            for loc in region.locations:
                yield loc

    def get_location(self, location):
        return self.world.get_location(location, self.player)

    def get_region(self, region):
        return self.world.get_region(region, self.player)

    def get_entrance(self, entrance):
        return self.world.get_entrance(entrance, self.player)

    def is_major_item(self, item: OOTItem):
        if item.type == 'Token':
            return self.bridge == 'tokens' or self.lacs_condition == 'tokens'

        if item.name in self.nonadvancement_items:
            return True

        if item.type in ('Drop', 'Event', 'Shop', 'DungeonReward') or not item.advancement:
            return False

        if item.name.startswith('Bombchus') and not self.bombchus_in_logic:
            return False

        if item.type in ['Map', 'Compass']:
            return False
        if item.type == 'SmallKey' and self.shuffle_smallkeys in ['dungeon', 'vanilla']:
            return False
        if item.type == 'HideoutSmallKey' and self.shuffle_fortresskeys == 'vanilla':
            return False
        if item.type == 'BossKey' and self.shuffle_bosskeys in ['dungeon', 'vanilla']:
            return False
        if item.type == 'GanonBossKey' and self.shuffle_ganon_bosskey in ['dungeon', 'vanilla']:
            return False

        return True

    # Specifically ensures that only real items are gotten, not any events.
    # In particular, ensures that Time Travel needs to be found.
    def get_state_with_complete_itempool(self):
        all_state = self.world.get_all_state(use_cache=False)
        # Remove event progression items
        for item, player in all_state.prog_items:
            if (item not in item_table or item_table[item][2] is None) and player == self.player:
                all_state.prog_items[(item, player)] = 0
        # Remove all events and checked locations
        all_state.locations_checked = {loc for loc in all_state.locations_checked if loc.player != self.player}
        all_state.events = {loc for loc in all_state.events if loc.player != self.player}
        # If free_scarecrow give Scarecrow Song
        if self.free_scarecrow:
            all_state.collect(self.create_item("Scarecrow Song"), event=True)

        # Invalidate caches
        all_state.child_reachable_regions[self.player] = set()
        all_state.adult_reachable_regions[self.player] = set()
        all_state.child_blocked_connections[self.player] = set()
        all_state.adult_blocked_connections[self.player] = set()
        all_state.day_reachable_regions[self.player] = set()
        all_state.dampe_reachable_regions[self.player] = set()
        all_state.stale[self.player] = True

        return all_state

    def get_filler_item_name(self) -> str:
        return get_junk_item(count=1, pool=get_junk_pool(self))[0]
