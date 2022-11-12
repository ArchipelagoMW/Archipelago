import logging
import threading
import copy
from typing import Optional, List, AbstractSet  # remove when 3.8 support is dropped
from collections import Counter, deque
from string import printable

logger = logging.getLogger("Ocarina of Time")

from .Location import OOTLocation, LocationFactory, location_name_to_id
from .Entrance import OOTEntrance
from .EntranceShuffle import shuffle_random_entrances, entrance_shuffle_table, EntranceShuffleError
from .Items import OOTItem, item_table, oot_data_to_ap_id, oot_is_item_of_type
from .ItemPool import generate_itempool, add_dungeon_items, get_junk_item, get_junk_pool
from .Regions import OOTRegion, TimeOfDay
from .Rules import set_rules, set_shop_rules, set_entrances_based_rules
from .RuleParser import Rule_AST_Transformer
from .Options import oot_options
from .Utils import data_path, read_json
from .LocationList import business_scrubs, set_drop_location_names, dungeon_song_locations
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
from BaseClasses import MultiWorld, CollectionState, RegionType, Tutorial, LocationProgressType
from Options import Range, Toggle, OptionList
from Fill import fill_restrictive, fast_fill, FillError
from worlds.generic.Rules import exclusion_rules, add_item_rule
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
        setup.authors
    )

    tutorials = [setup, setup_es]


class OOTWorld(World):
    """
    The Legend of Zelda: Ocarina of Time is a 3D action/adventure game. Travel through Hyrule in two time periods,
    learn magical ocarina songs, and explore twelve dungeons on your quest. Use Link's many items and abilities
    to rescue the Seven Sages, and then confront Ganondorf to save Hyrule!
    """
    game: str = "Ocarina of Time"
    option_definitions: dict = oot_options
    topology_present: bool = True
    item_name_to_id = {item_name: oot_data_to_ap_id(data, False) for item_name, data in item_table.items() if
                       data[2] is not None}
    location_name_to_id = location_name_to_id
    remote_items: bool = False
    remote_start_inventory: bool = False
    web = OOTWeb()

    data_version = 2

    required_client_version = (0, 3, 2)

    item_name_groups = {
        # internal groups
        "medallions": {"Light Medallion", "Forest Medallion", "Fire Medallion",
            "Water Medallion", "Shadow Medallion", "Spirit Medallion"},
        "stones": {"Kokiri Emerald", "Goron Ruby", "Zora Sapphire"},
        "rewards": {"Light Medallion", "Forest Medallion", "Fire Medallion",
            "Water Medallion", "Shadow Medallion", "Spirit Medallion",
            "Kokiri Emerald", "Goron Ruby", "Zora Sapphire"},
        "logic_bottles": {"Bottle", "Bottle with Milk", "Deliver Letter",
            "Sell Big Poe", "Bottle with Red Potion", "Bottle with Green Potion", 
            "Bottle with Blue Potion", "Bottle with Fairy", "Bottle with Fish", 
            "Bottle with Blue Fire", "Bottle with Bugs", "Bottle with Poe"},

        # hint groups
        "Bottles": {"Bottle", "Bottle with Milk", "Rutos Letter",
            "Bottle with Big Poe", "Bottle with Red Potion", "Bottle with Green Potion", 
            "Bottle with Blue Potion", "Bottle with Fairy", "Bottle with Fish", 
            "Bottle with Blue Fire", "Bottle with Bugs", "Bottle with Poe"},
        "Adult Trade Item": {"Pocket Egg", "Pocket Cucco", "Odd Mushroom",
            "Odd Potion", "Poachers Saw", "Broken Sword", "Prescription",
            "Eyeball Frog", "Eyedrops", "Claim Check"}
    }

    def __init__(self, world, player):
        self.hint_data_available = threading.Event()
        super(OOTWorld, self).__init__(world, player)

    @classmethod
    def stage_assert_generate(cls, world: MultiWorld):
        rom = Rom(file=get_options()['oot_options']['rom_file'])

    def generate_early(self):
        self.parser = Rule_AST_Transformer(self, self.player)

        for (option_name, option) in oot_options.items():
            result = getattr(self.multiworld, option_name)[self.player]
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
        self.songs_as_items = False
        self.file_hash = [self.multiworld.random.randint(0, 31) for i in range(5)]
        self.connect_name = ''.join(self.multiworld.random.choices(printable, k=16))

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

        # Ganon boss key should not be in itempool in triforce hunt
        if self.triforce_hunt:
            self.shuffle_ganon_bosskey = 'remove'

        # If songs/keys locked to own world by settings, add them to local_items
        local_types = []
        if self.shuffle_song_items != 'any':
            local_types.append('Song')
        if self.shuffle_mapcompass != 'keysanity':
            local_types += ['Map', 'Compass']
        if self.shuffle_smallkeys != 'keysanity':
            local_types.append('SmallKey')
        if self.shuffle_fortresskeys != 'keysanity':
            local_types.append('HideoutSmallKey')
        if self.shuffle_bosskeys != 'keysanity':
            local_types.append('BossKey')
        if self.shuffle_ganon_bosskey != 'keysanity':
            local_types.append('GanonBossKey')
        self.multiworld.local_items[self.player].value |= set(name for name, data in item_table.items() if data[0] in local_types)

        # If any songs are itemlinked, set songs_as_items
        for group in self.multiworld.groups.values():
            if self.songs_as_items or group['game'] != self.game or self.player not in group['players']:
                continue
            for item_name in group['item_pool']:
                if oot_is_item_of_type(item_name, 'Song'):
                    self.songs_as_items = True
                    break

        # Determine skipped trials in GT
        # This needs to be done before the logic rules in GT are parsed
        trial_list = ['Forest', 'Fire', 'Water', 'Spirit', 'Shadow', 'Light']
        chosen_trials = self.multiworld.random.sample(trial_list, self.trials)  # chooses a list of trials to NOT skip
        self.skipped_trials = {trial: (trial not in chosen_trials) for trial in trial_list}

        # Determine which dungeons are MQ
        # Possible future plan: allow user to pick which dungeons are MQ
        if self.logic_rules == 'glitchless':
            mq_dungeons = self.multiworld.random.sample(dungeon_table, self.mq_dungeons)
        else:
            self.mq_dungeons = 0
            mq_dungeons = []
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
            self.multiworld.progression_balancing[self.player].value = False
            self.multiworld.accessibility[self.player] = self.multiworld.accessibility[self.player].from_text("minimal")
            for trick in normalized_name_tricks.values():
                setattr(self, trick['name'], True)

        # Not implemented for now, but needed to placate the generator. Remove as they are implemented
        self.mq_dungeons_random = False  # this will be a deprecated option later
        self.ocarina_songs = False  # just need to pull in the OcarinaSongs module
        self.mix_entrance_pools = False
        self.decouple_entrances = False

        # Set internal names used by the OoT generator
        self.keysanity = self.shuffle_smallkeys in ['keysanity', 'remove', 'any_dungeon', 'overworld']
        self.trials_random = self.multiworld.trials[self.player].randomized
        self.mq_dungeons_random = self.multiworld.mq_dungeons[self.player].randomized

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
            new_region.multiworld = self.multiworld
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
                    new_exit = OOTEntrance(self.player, self.multiworld, '%s -> %s' % (new_region.name, exit), new_region)
                    new_exit.vanilla_connected_region = exit
                    new_exit.rule_string = rule
                    if self.multiworld.logic_rules != 'none':
                        self.parser.parse_spot_rule(new_exit)
                    if new_exit.never:
                        logger.debug('Dropping unreachable exit: %s', new_exit.name)
                    else:
                        new_region.exits.append(new_exit)

            self.multiworld.regions.append(new_region)
            self.regions.append(new_region)
        self.multiworld._recache()

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
                price = int(self.multiworld.random.betavariate(1, 2) * 99)

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
                shop_item_count = self.multiworld.random.randint(0, 4)
            else:
                shop_item_count = int(self.shopsanity)

            for location in region.locations:
                if location.type == 'Shop':
                    if location.name[-1:] in shop_item_indexes[:shop_item_count]:
                        self.shop_prices[location.name] = int(self.multiworld.random.betavariate(1.5, 2) * 60) * 5

    def fill_bosses(self, bossCount=9):
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
        boss_rewards = [item for item in self.itempool if item.type == 'DungeonReward']
        boss_locations = [self.multiworld.get_location(loc, self.player) for loc in boss_location_names]

        placed_prizes = [loc.item.name for loc in boss_locations if loc.item is not None]
        prizepool = [item for item in boss_rewards if item.name not in placed_prizes]
        prize_locs = [loc for loc in boss_locations if loc.item is None]

        while bossCount:
            bossCount -= 1
            self.multiworld.random.shuffle(prizepool)
            self.multiworld.random.shuffle(prize_locs)
            item = prizepool.pop()
            loc = prize_locs.pop()
            loc.place_locked_item(item)
            self.multiworld.itempool.remove(item)

    def create_item(self, name: str):
        if name in item_table:
            return OOTItem(name, self.player, item_table[name], False,
                           (name in self.nonadvancement_items if getattr(self, 'nonadvancement_items',
                                                                         None) else False))
        return OOTItem(name, self.player, ('Event', True, None, None), True, False)

    def make_event_item(self, name, location, item=None):
        if item is None:
            item = self.create_item(name)
        self.multiworld.push_item(location, item, collect=False)
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
        start = OOTEntrance(self.player, self.multiworld, 'New Game', menu)
        menu.exits.append(start)
        self.multiworld.regions.append(menu)
        self.load_regions_from_json(overworld_data_path)
        start.connect(self.multiworld.get_region('Root', self.player))
        create_dungeons(self)
        self.parser.create_delayed_rules()

        if self.shopsanity != 'off':
            self.random_shop_prices()
        self.set_scrub_prices()

        # Bind entrances to vanilla
        for region in self.regions:
            for exit in region.exits:
                exit.connect(self.multiworld.get_region(exit.vanilla_connected_region, self.player))

    def create_items(self):
        # Generate itempool
        generate_itempool(self)
        add_dungeon_items(self)
        # Add dungeon rewards
        rewardlist = sorted(list(self.item_name_groups['rewards']))
        self.itempool += map(self.create_item, rewardlist)

        junk_pool = get_junk_pool(self)
        removed_items = []
        # Determine starting items
        for item in self.multiworld.precollected_items[self.player]:
            if item.name in self.remove_from_start_inventory:
                self.remove_from_start_inventory.remove(item.name)
                removed_items.append(item.name)
            else:
                if item.name not in SaveContext.giveable_items:
                    raise Exception(f"Invalid OoT starting item: {item.name}")
                else:
                    self.starting_items[item.name] += 1
                    if item.type == 'Song':
                        self.songs_as_items = True
                    # Call the junk fill and get a replacement
                    if item in self.itempool:
                        self.itempool.remove(item)
                        self.itempool.append(self.create_item(*get_junk_item(pool=junk_pool)))
        if self.start_with_consumables:
            self.starting_items['Deku Sticks'] = 30
            self.starting_items['Deku Nuts'] = 40
        if self.start_with_rupees:
            self.starting_items['Rupees'] = 999

        self.multiworld.itempool += self.itempool
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
                        entrance.connect(self.multiworld.get_region(entrance.vanilla_connected_region, self.player))
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
        all_state = self.multiworld.get_all_state(False)
        all_locations = self.get_locations()
        reachable = self.multiworld.get_reachable_locations(all_state, self.player)
        unreachable = [loc for loc in all_locations if
                       (loc.internal or loc.type == 'Drop') and loc.event and loc.locked and loc not in reachable]
        for loc in unreachable:
            loc.parent_region.locations.remove(loc)
        # Exception: Sell Big Poe is an event which is only reachable if Bottle with Big Poe is in the item pool.
        # We allow it to be removed only if Bottle with Big Poe is not in the itempool.
        bigpoe = self.multiworld.get_location('Sell Big Poe from Market Guard House', self.player)
        if not all_state.has('Bottle with Big Poe', self.player) and bigpoe not in reachable:
            bigpoe.parent_region.locations.remove(bigpoe)
        self.multiworld.clear_location_cache()

        # If fast scarecrow then we need to kill the Pierre location as it will be unreachable
        if self.free_scarecrow:
            loc = self.multiworld.get_location("Pierre", self.player)
            loc.parent_region.locations.remove(loc)
        # If open zora's domain then we need to kill Deliver Rutos Letter
        if self.zora_fountain == 'open':
            loc = self.multiworld.get_location("Deliver Rutos Letter", self.player)
            loc.parent_region.locations.remove(loc)

    def pre_fill(self):

        def get_names(items):
            for item in items:
                yield item.name

        # Place/set rules for dungeon items
        itempools = {
            'dungeon': set(),
            'overworld': set(),
            'any_dungeon': set(),
        }
        any_dungeon_locations = []
        for dungeon in self.dungeons:
            itempools['dungeon'] = set()
            # Put the dungeon items into their appropriate pools.
            # Build in reverse order since we need to fill boss key first and pop() returns the last element
            if self.shuffle_mapcompass in itempools:
                itempools[self.shuffle_mapcompass].update(get_names(dungeon.dungeon_items))
            if self.shuffle_smallkeys in itempools:
                itempools[self.shuffle_smallkeys].update(get_names(dungeon.small_keys))
            shufflebk = self.shuffle_bosskeys if dungeon.name != 'Ganons Castle' else self.shuffle_ganon_bosskey
            if shufflebk in itempools:
                itempools[shufflebk].update(get_names(dungeon.boss_key))

            # We can't put a dungeon item on the end of a dungeon if a song is supposed to go there. Make sure not to include it.
            dungeon_locations = [loc for region in dungeon.regions for loc in region.locations
                                 if loc.item is None and (
                                         self.shuffle_song_items != 'dungeon' or loc.name not in dungeon_song_locations)]
            if itempools['dungeon']:  # only do this if there's anything to shuffle
                dungeon_itempool = [item for item in self.multiworld.itempool if item.player == self.player and item.name in itempools['dungeon']]
                for item in dungeon_itempool:
                    self.multiworld.itempool.remove(item)
                self.multiworld.random.shuffle(dungeon_locations)
                fill_restrictive(self.multiworld, self.multiworld.get_all_state(False), dungeon_locations,
                                 dungeon_itempool, True, True)
            any_dungeon_locations.extend(dungeon_locations)  # adds only the unfilled locations

        # Now fill items that can go into any dungeon. Retrieve the Gerudo Fortress keys from the pool if necessary
        if self.shuffle_fortresskeys == 'any_dungeon':
            itempools['any_dungeon'].add('Small Key (Thieves Hideout)')
        if itempools['any_dungeon']:
            any_dungeon_itempool = [item for item in self.multiworld.itempool if item.player == self.player and item.name in itempools['any_dungeon']]
            for item in any_dungeon_itempool:
                self.multiworld.itempool.remove(item)
            any_dungeon_itempool.sort(key=lambda item:
                {'GanonBossKey': 4, 'BossKey': 3, 'SmallKey': 2, 'HideoutSmallKey': 1}.get(item.type, 0))
            self.multiworld.random.shuffle(any_dungeon_locations)
            fill_restrictive(self.multiworld, self.multiworld.get_all_state(False), any_dungeon_locations,
                             any_dungeon_itempool, True, True)

        # If anything is overworld-only, fill into local non-dungeon locations
        if self.shuffle_fortresskeys == 'overworld':
            itempools['overworld'].add('Small Key (Thieves Hideout)')
        if itempools['overworld']:
            overworld_itempool = [item for item in self.multiworld.itempool if item.player == self.player and item.name in itempools['overworld']]
            for item in overworld_itempool:
                self.multiworld.itempool.remove(item)
            overworld_itempool.sort(key=lambda item:
                {'GanonBossKey': 4, 'BossKey': 3, 'SmallKey': 2, 'HideoutSmallKey': 1}.get(item.type, 0))
            non_dungeon_locations = [loc for loc in self.get_locations() if
                                     not loc.item and loc not in any_dungeon_locations and
                                     (loc.type != 'Shop' or loc.name in self.shop_prices) and
                                     (loc.type != 'Song' or self.shuffle_song_items != 'song') and
                                     (loc.name not in dungeon_song_locations or self.shuffle_song_items != 'dungeon')]
            self.multiworld.random.shuffle(non_dungeon_locations)
            fill_restrictive(self.multiworld, self.multiworld.get_all_state(False), non_dungeon_locations,
                             overworld_itempool, True, True)

        # Place songs
        # 5 built-in retries because this section can fail sometimes
        if self.shuffle_song_items != 'any':
            tries = 5
            if self.shuffle_song_items == 'song':
                song_locations = list(filter(lambda location: location.type == 'Song',
                                             self.multiworld.get_unfilled_locations(player=self.player)))
            elif self.shuffle_song_items == 'dungeon':
                song_locations = list(filter(lambda location: location.name in dungeon_song_locations,
                                             self.multiworld.get_unfilled_locations(player=self.player)))
            else:
                raise Exception(f"Unknown song shuffle type: {self.shuffle_song_items}")

            songs = list(filter(lambda item: item.player == self.player and item.type == 'Song', self.multiworld.itempool))
            for song in songs:
                self.multiworld.itempool.remove(song)

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
                    self.multiworld.random.shuffle(song_locations)
                    fill_restrictive(self.multiworld, self.multiworld.get_all_state(False), song_locations[:], songs[:],
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
            shop_prog = list(filter(lambda item: item.player == self.player and item.type == 'Shop' 
                and item.advancement, self.multiworld.itempool))
            shop_junk = list(filter(lambda item: item.player == self.player and item.type == 'Shop' 
                and not item.advancement, self.multiworld.itempool))
            shop_locations = list(
                filter(lambda location: location.type == 'Shop' and location.name not in self.shop_prices,
                       self.multiworld.get_unfilled_locations(player=self.player)))
            shop_prog.sort(key=lambda item: {
                'Buy Deku Shield': 2 * int(self.open_forest == 'closed'),
                'Buy Goron Tunic': 1,
                'Buy Zora Tunic': 1,
            }.get(item.name, 0))  # place Deku Shields if needed, then tunics, then other advancement
            self.multiworld.random.shuffle(shop_locations)
            for item in shop_prog + shop_junk:
                self.multiworld.itempool.remove(item)
            fill_restrictive(self.multiworld, self.multiworld.get_all_state(False), shop_locations, shop_prog, True, True)
            fast_fill(self.multiworld, shop_junk, shop_locations)
            for loc in shop_locations:
                loc.locked = True
        set_shop_rules(self)  # sets wallet requirements on shop items, must be done after they are filled

        # If skip child zelda is active and Song from Impa is unfilled, put a local giveable item into it.
        impa = self.multiworld.get_location("Song from Impa", self.player)
        if self.skip_child_zelda:
            if impa.item is None:
                item_to_place = self.multiworld.random.choice(list(item for item in self.multiworld.itempool if
                                                                   item.player == self.player and item.name in SaveContext.giveable_items))
                impa.place_locked_item(item_to_place)
                self.multiworld.itempool.remove(item_to_place)
            # Give items to startinventory
            self.multiworld.push_precollected(impa.item)
            self.multiworld.push_precollected(self.create_item("Zeldas Letter"))

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
            junk_fill_locations = self.multiworld.random.sample(locations, round(len(locations) * ganon_junk_fill))
            exclusion_rules(self.multiworld, self.player, junk_fill_locations)

        # Locations which are not sendable must be converted to events
        # This includes all locations for which show_in_spoiler is false, and shuffled shop items.
        for loc in self.get_locations():
            if loc.address is not None and (
                    not loc.show_in_spoiler or oot_is_item_of_type(loc.item, 'Shop')
                    or (self.skip_child_zelda and loc.name in ['HC Zeldas Letter', 'Song from Impa'])):
                loc.address = None

    # Handle item-linked dungeon items and songs
    @classmethod
    def stage_pre_fill(cls, multiworld: MultiWorld):

        def gather_locations(item_type: str, players: AbstractSet[int], dungeon: str = '') -> Optional[List[OOTLocation]]:
            type_to_setting = {
                'Song': 'shuffle_song_items',
                'Map': 'shuffle_mapcompass',
                'Compass': 'shuffle_mapcompass',
                'SmallKey': 'shuffle_smallkeys',
                'BossKey': 'shuffle_bosskeys',
                'HideoutSmallKey': 'shuffle_fortresskeys',
                'GanonBossKey': 'shuffle_ganon_bosskey',
            }
            fill_opts = {p: getattr(multiworld.worlds[p], type_to_setting[item_type]) for p in players}
            locations = []
            if item_type == 'Song':
                if any(map(lambda v: v == 'any', fill_opts.values())):
                    return None
                for player, option in fill_opts.items():
                    if option == 'song':
                        condition = lambda location: location.type == 'Song'
                    elif option == 'dungeon':
                        condition = lambda location: location.name in dungeon_song_locations
                    locations += filter(condition, multiworld.get_unfilled_locations(player=player))
            else:
                if any(map(lambda v: v == 'keysanity', fill_opts.values())):
                    return None
                for player, option in fill_opts.items():
                    if option == 'dungeon':
                        condition = lambda location: getattr(location.parent_region.dungeon, 'name', None) == dungeon
                    elif option == 'overworld':
                        condition = lambda location: location.parent_region.dungeon is None
                    elif option == 'any_dungeon':
                        condition = lambda location: location.parent_region.dungeon is not None
                    locations += filter(condition, multiworld.get_unfilled_locations(player=player))

            return locations

        special_fill_types = ['Song', 'GanonBossKey', 'BossKey', 'SmallKey', 'HideoutSmallKey', 'Map', 'Compass']
        for group_id, group in multiworld.groups.items():
            if group['game'] != cls.game:
                continue
            group_items = [item for item in multiworld.itempool if item.player == group_id]
            for fill_stage in special_fill_types:
                group_stage_items = list(filter(lambda item: oot_is_item_of_type(item, fill_stage), group_items))
                if not group_stage_items:
                    continue
                if fill_stage in ['Song', 'GanonBossKey', 'HideoutSmallKey']:
                    # No need to subdivide by dungeon name
                    locations = gather_locations(fill_stage, group['players'])
                    if isinstance(locations, list):
                        for item in group_stage_items:
                            multiworld.itempool.remove(item)
                        multiworld.random.shuffle(locations)
                        fill_restrictive(multiworld, multiworld.get_all_state(False), locations, group_stage_items,
                            single_player_placement=False, lock=True)
                        if fill_stage == 'Song':
                            # We don't want song locations to contain progression unless it's a song
                            # or it was marked as priority.
                            # We do this manually because we'd otherwise have to either
                            # iterate twice or do many function calls.
                            for loc in locations:
                                if loc.progress_type == LocationProgressType.DEFAULT:
                                    loc.progress_type = LocationProgressType.EXCLUDED
                                    add_item_rule(loc, lambda i: not (i.advancement or i.useful))
                else:
                    # Perform the fill task once per dungeon
                    for dungeon_info in dungeon_table:
                        dungeon_name = dungeon_info['name']
                        locations = gather_locations(fill_stage, group['players'], dungeon=dungeon_name)
                        if isinstance(locations, list):
                            group_dungeon_items = list(filter(lambda item: dungeon_name in item.name, group_stage_items))
                            for item in group_dungeon_items:
                                multiworld.itempool.remove(item)
                            multiworld.random.shuffle(locations)
                            fill_restrictive(multiworld, multiworld.get_all_state(False), locations, group_dungeon_items,
                                single_player_placement=False, lock=True)

    def generate_output(self, output_directory: str):
        if self.hints != 'none':
            self.hint_data_available.wait()

        with i_o_limiter:
            # Make traps appear as other random items
            trap_location_ids = [loc.address for loc in self.get_locations() if loc.item.trap]
            self.trap_appearances = {}
            for loc_id in trap_location_ids:
                self.trap_appearances[loc_id] = self.create_item(self.multiworld.slot_seeds[self.player].choice(self.fake_items).name)

            # Seed hint RNG, used for ganon text lines also
            self.hint_rng = self.multiworld.slot_seeds[self.player]

            outfile_name = self.multiworld.get_out_file_name_base(self.player)
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
            all_entrances.sort(reverse=True, key=lambda x: x.name)
            all_entrances.sort(reverse=True, key=lambda x: x.type)
            if not self.decouple_entrances:
                while all_entrances:
                    loadzone = all_entrances.pop()
                    if loadzone.type != 'Overworld':
                        if loadzone.primary:
                            entrance = loadzone
                        else:
                            entrance = loadzone.reverse
                        if entrance.reverse is not None:
                            self.multiworld.spoiler.set_entrance(entrance, entrance.replaces.reverse, 'both', self.player)
                        else:
                            self.multiworld.spoiler.set_entrance(entrance, entrance.replaces, 'entrance', self.player)
                    else:
                        reverse = loadzone.replaces.reverse
                        if reverse in all_entrances:
                            all_entrances.remove(reverse)
                        self.multiworld.spoiler.set_entrance(loadzone, reverse, 'both', self.player)
            else:
                for entrance in all_entrances:
                    self.multiworld.spoiler.set_entrance(entrance, entrance.replaces, 'entrance', self.player)

    # Gathers hint data for OoT. Loops over all world locations for woth, barren, and major item locations.
    @classmethod
    def stage_generate_output(cls, multiworld: MultiWorld, output_directory: str):
        def hint_type_players(hint_type: str) -> set:
            return {autoworld.player for autoworld in multiworld.get_game_worlds("Ocarina of Time")
                    if autoworld.hints != 'none' and autoworld.hint_dist_user['distribution'][hint_type]['copies'] > 0}

        try:
            item_hint_players = hint_type_players('item')
            barren_hint_players = hint_type_players('barren')
            woth_hint_players = hint_type_players('woth')

            items_by_region = {}
            for player in barren_hint_players:
                items_by_region[player] = {}
                for r in multiworld.worlds[player].regions:
                    items_by_region[player][r.hint_text] = {'dungeon': False, 'weight': 0, 'is_barren': True}
                for d in multiworld.worlds[player].dungeons:
                    items_by_region[player][d.hint_text] = {'dungeon': True, 'weight': 0, 'is_barren': True}
                del (items_by_region[player]["Link's Pocket"])
                del (items_by_region[player][None])

            if item_hint_players:  # loop once over all locations to gather major items. Check oot locations for barren/woth if needed
                for loc in multiworld.get_locations():
                    player = loc.item.player
                    autoworld = multiworld.worlds[player]
                    if ((player in item_hint_players and (autoworld.is_major_item(loc.item) or loc.item.name in autoworld.item_added_hint_types['item']))
                                or (loc.player in item_hint_players and loc.name in multiworld.worlds[loc.player].added_hint_types['item'])):
                        autoworld.major_item_locations.append(loc)

                    if loc.game == "Ocarina of Time" and loc.item.code and (not loc.locked or
                        (oot_is_item_of_type(loc.item, 'Song') or
                            (oot_is_item_of_type(loc.item, 'SmallKey')         and multiworld.worlds[loc.player].shuffle_smallkeys     == 'any_dungeon') or
                            (oot_is_item_of_type(loc.item, 'HideoutSmallKey')  and multiworld.worlds[loc.player].shuffle_fortresskeys  == 'any_dungeon') or
                            (oot_is_item_of_type(loc.item, 'BossKey')          and multiworld.worlds[loc.player].shuffle_bosskeys      == 'any_dungeon') or
                            (oot_is_item_of_type(loc.item, 'GanonBossKey')     and multiworld.worlds[loc.player].shuffle_ganon_bosskey == 'any_dungeon'))):
                        if loc.player in barren_hint_players:
                            hint_area = get_hint_area(loc)
                            items_by_region[loc.player][hint_area]['weight'] += 1
                            if loc.item.advancement or loc.item.useful:
                                items_by_region[loc.player][hint_area]['is_barren'] = False
                        if loc.player in woth_hint_players and loc.item.advancement:
                            # Skip item at location and see if game is still beatable
                            state = CollectionState(multiworld)
                            state.locations_checked.add(loc)
                            if not multiworld.can_beat_game(state):
                                multiworld.worlds[loc.player].required_locations.append(loc)
            elif barren_hint_players or woth_hint_players:  # Check only relevant oot locations for barren/woth
                for player in (barren_hint_players | woth_hint_players):
                    for loc in multiworld.worlds[player].get_locations():
                        if loc.item.code and (not loc.locked or oot_is_item_of_type(loc.item, 'Song')):
                            if player in barren_hint_players:
                                hint_area = get_hint_area(loc)
                                items_by_region[player][hint_area]['weight'] += 1
                                if loc.item.advancement or loc.item.useful:
                                    items_by_region[player][hint_area]['is_barren'] = False
                            if player in woth_hint_players and loc.item.advancement:
                                state = CollectionState(multiworld)
                                state.locations_checked.add(loc)
                                if not multiworld.can_beat_game(state):
                                    multiworld.worlds[player].required_locations.append(loc)
            for player in barren_hint_players:
                multiworld.worlds[player].empty_areas = {region: info for (region, info) in items_by_region[player].items()
                                                    if info['is_barren']}
        except Exception as e:
            raise e
        finally:
            for autoworld in multiworld.get_game_worlds("Ocarina of Time"):
                autoworld.hint_data_available.set()

    def modify_multidata(self, multidata: dict):

        # Replace connect name
        multidata['connect_names'][self.connect_name] = multidata['connect_names'][self.multiworld.player_name[self.player]]

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
        return [entrance for entrance in self.multiworld.get_entrances() if (entrance.player == self.player and
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
        return self.multiworld.get_location(location, self.player)

    def get_region(self, region):
        return self.multiworld.get_region(region, self.player)

    def get_entrance(self, entrance):
        return self.multiworld.get_entrance(entrance, self.player)

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
        all_state = self.multiworld.get_all_state(use_cache=False)
        # Remove event progression items
        for item, player in all_state.prog_items:
            if player == self.player and (item not in item_table or (item_table[item][2] is None and item_table[item][0] != 'DungeonReward')):
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
