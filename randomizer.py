import argparse, random, ast, sys, re
from utility import *
from generator import Generator
import mapfileio

VERSION_STRING = '{PLACEHOLDER_VERSION}'

"""
Knowledge levels:
    BASIC
    INTERMEDIATE
    ADVANCED

Difficulty levels:
    NORMAL
    HARD
    V_HARD
    STUPID
"""

KNOWLEDGE_INTERMEDIATE = 'KNOWLEDGE_INTERMEDIATE'
KNOWLEDGE_ADVANCED = 'KNOWLEDGE_ADVANCED'
DIFFICULTY_HARD = 'DIFFICULTY_HARD'
DIFFICULTY_V_HARD = 'DIFFICULTY_V_HARD'
DIFFICULTY_STUPID = 'DIFFICULTY_STUPID'

def parse_args():
    args = argparse.ArgumentParser(description='Rabi-Ribi Randomizer - %s' % VERSION_STRING)
    args.add_argument('--version', action='store_true', help='Print Randomizer Version')
    args.add_argument('-output_dir', default='generated_maps', help='Output directory for generated maps')
    args.add_argument('-config_file', default='config.txt', help='Config file to use')
    args.add_argument('-seed', default=None, type=str, help='Random seed')
    args.add_argument('--no-write', dest='write', default=True, action='store_false', help='Flag to disable map generation, and do only map analysis')
    args.add_argument('--no-fixes', dest='apply_fixes', default=True, action='store_false', help='Flag to disable randomizer-specific map fixes')
    args.add_argument('--reset', action='store_true', help='Reset maps by copying the original maps to the output directory.')
    args.add_argument('--hash', action='store_true', help='Generate a hash of the maps in the output directory.')
    args.add_argument('--check-for-updates', action='store_true', help='Check for the latest version of randomizer.')
    args.add_argument('--check-branch', action='store_true', help='Displays which branch the randomizer is currently on (D or M).')
    args.add_argument('--shuffle-music', action='store_true', help='Shuffles the music in the map.')
    args.add_argument('--shuffle-backgrounds', action='store_true', help='Shuffles the backgrounds in the map.')
    args.add_argument('--shuffle-map-transitions', action='store_true', help='Shuffles map transitions between maps.')
    args.add_argument('--no-laggy-backgrounds', action='store_true', help='Don\'t include laggy backgrounds in background shuffle.')
    args.add_argument('--no-difficult-backgrounds', action='store_true', help='Don\'t include backgrounds in background shuffle that interfere with visibility.')
    args.add_argument('--super-attack-mode', action='store_true', help='Start the game with a bunch of attack ups, so you do lots more damage.')
    args.add_argument('--hyper-attack-mode', action='store_true', help='Like Super Attack Mode, but with 35 attack ups.')
    args.add_argument('--open-mode', action='store_true', help='Removes prologue triggers that restrict exploration.')
    args.add_argument('--hide-unreachable', action='store_true', help='Hide list of unreachable items. Affects seed.')
    args.add_argument('--hide-difficulty', action='store_true', help='Hide difficulty rating. Affects seed.')
    args.add_argument('--egg-goals', action='store_true', help='Egg goals mode. Hard-to-reach items are replaced with easter eggs. All other eggs are removed from the map.')
    args.add_argument('-extra-eggs', default=0, type=int, help='Number of extra randomly-chosen eggs for egg-goals mode (in addition to the hard-to-reach eggs)')

    return args.parse_args(sys.argv[1:])


def define_setting_flags():
    d = {
        "TRUE": True,
        "FALSE": False,
        "ZIP_REQUIRED": False,
        "SEMISOLID_CLIPS_REQUIRED": False,
        "ADVANCED_TRICKS_REQUIRED": True,
        "BLOCK_CLIPS_REQUIRED": True,
        "POST_GAME_ALLOWED": True,
        "POST_IRISU_ALLOWED": True,
        "STUPID_HARD_TRICKS": False,
        "HALLOWEEN_REACHABLE": False,
        "PLURKWOOD_REACHABLE": True,
        "WARP_DESTINATION_REACHABLE": False,
        "DARKNESS_WITHOUT_LIGHT_ORB": True,
        "UNDERWATER_WITHOUT_WATER_ORB": True,
    }
    d.update(define_difficulty_flags())
    return d

def define_difficulty_flags():
    # Difficulty Flags
    return {
        KNOWLEDGE_INTERMEDIATE: False,
        KNOWLEDGE_ADVANCED: False,
        DIFFICULTY_HARD: False,
        DIFFICULTY_V_HARD: False,
        DIFFICULTY_STUPID: False,
    }

# The values can be either a expression constrant, which is expressed as a string,
# or a lambda, that takes in a variables object and returns a bool.
def define_pseudo_items():
    return {
        "WALL_JUMP_LV2": "WALL_JUMP & SHOP",
        "HAMMER_ROLL_LV3": "rHAMMER_ROLL & SHOP & CHAPTER_3",
        "AIR_DASH_LV3": "rAIR_DASH & SHOP",
        "SPEED_BOOST_LV3": "SPEED_BOOST & SHOP",
        "BUNNY_AMULET_LV2": "(BUNNY_AMULET & SHOP) | CHAPTER_3",
        "BUNNY_AMULET_LV3": "(BUNNY_AMULET & SHOP) | CHAPTER_4",
        "PIKO_HAMMER_LEVELED": "PIKO_HAMMER",
        "CARROT_BOMB_ENTRY": "CARROT_BOMB",
        "CARROT_SHOOTER_ENTRY": "CARROT_SHOOTER",
        "SHOP": "TOWN_MAIN",

        "COCOA_1": "FOREST_START",
        "KOTRI_1": "PARK_MAIN",
        "ASHURI_2": "RIVERBANK_MAIN",
        "BOSS_KEKE_BUNNY": "PLURKWOOD_MAIN",
        "RIBBON": "SPECTRAL_WARP",

        "TM_COCOA": "COCOA_1 & KOTRI_1 & CAVE_COCOA",
        "TM_ASHURI": "RIVERBANK_MAIN & TOWN_MAIN & SPECTRAL_WEST",
        "TM_RITA": "SNOWLAND_EAST",
        "TM_CICINI": "SPECTRAL_CICINI_ROOM",
        "TM_SAYA": "EVERNIGHT_SAYA & EVERNIGHT_EAST_OF_WARP",
        "TM_SYARO": "SYSTEM_INTERIOR_MAIN",
        "TM_PANDORA": "PYRAMID_MAIN",
        "TM_NIEVE": "PALACE_MAIN & ICY_SUMMIT_MAIN",
        "TM_NIXIE": "PALACE_MAIN & ICY_SUMMIT_MAIN",
        "TM_ARURAUNE": "FOREST_NIGHT_WEST",
        "TM_SEANA": "TM_VANILLA & TM_CHOCOLATE & TM_CICINI & TM_SYARO & TM_NIEVE & TM_NIXIE & AQUARIUM_MAIN & PARK_MAIN",
        "TM_LILITH": "SKY_ISLAND_MAIN",
        "TM_VANILLA": "SKY_BRIDGE_EAST",
        "TM_CHOCOLATE": "CHAPTER_1 & RAVINE_CHOCOLATE",
        "TM_KOTRI": "GRAVEYARD_MAIN & VOLCANIC_MAIN",
        "TM_KEKE_BUNNY": "BOSS_KEKE_BUNNY & PLURKWOOD_MAIN",

        "2TM": lambda v: count_town_members(v) >= 2,
        "3TM": lambda v: count_town_members(v) >= 3,
        "4TM": lambda v: count_town_members(v) >= 4,
        "7TM": lambda v: count_town_members(v) >= 7,
        "10TM": lambda v: count_town_members(v) >= 10,
        "SPEEDY": "TM_CICINI & TOWN_MAIN & 3TM",

        "CHAPTER_1": "TOWN_MAIN",
        "CHAPTER_2": "TOWN_MAIN & 2TM",
        "CHAPTER_3": "TOWN_MAIN & 4TM",
        "CHAPTER_4": "TOWN_MAIN & 7TM",
        "CHAPTER_5": "TOWN_MAIN & 10TM",
    }


def define_alternate_conditions(variable_names_set, default_expressions):
    d = {
        "SPEED_BOOST": "SHOP",
        "SOUL_HEART": "SHOP",
        "BOOK_OF_CARROT": "SHOP",
        "P_HAIRPIN": "BOSS_KEKE_BUNNY & PLURKWOOD_MAIN",
        "HEALING_STAFF": "SHOP",
        "MAX_BRACELET": "SHOP",
        "BUNNY_STRIKE": "SLIDING_POWDER & SHOP",
        "STRANGE_BOX": "TM_SYARO & TOWN_MAIN",
        "BUNNY_AMULET": "CHAPTER_2",
        "RUMI_DONUT": "SHOP",
        "RUMI_CAKE": "SHOP",
        "COCOA_BOMB": "TM_COCOA & TOWN_MAIN",
    }

    for key in d.keys():
        if type(d[key]) == str:
            d[key] = parse_expression_lambda(d[key], variable_names_set, default_expressions)
    return d


def define_default_expressions(variable_names_set):
    # Default expressions take priority over actual variables.
    # so if we parse an expression that has AIR_DASH, the default expression AIR_DASH will be used instead of the variable AIR_DASH.
    # however, the expressions parsed in define_default_expressions (just below) cannot use default expressions in their expressions.
    expr = lambda s : parse_expression(s, variable_names_set)
    def1 = {
        "INTERMEDIATE": expr("KNOWLEDGE_INTERMEDIATE"),
        "ADVANCED": expr("KNOWLEDGE_ADVANCED"),
        "HARD": expr("DIFFICULTY_HARD"),
        "V_HARD": expr("DIFFICULTY_V_HARD"),
        "STUPID": expr("DIFFICULTY_STUPID"),

        "ZIP": expr("ZIP_REQUIRED"),
        "SEMISOLID_CLIP": expr("SEMISOLID_CLIPS_REQUIRED"),
        "BLOCK_CLIP": expr("BLOCK_CLIPS_REQUIRED"),
        "POST_GAME": expr("POST_GAME_ALLOWED"),
        "POST_IRISU": expr("POST_IRISU_ALLOWED"),
        "HALLOWEEN": expr("HALLOWEEN_REACHABLE"),
        "PLURKWOOD": expr("PLURKWOOD_REACHABLE"),
        "WARP_DESTINATION": expr("WARP_DESTINATION_REACHABLE"),
        "BUNNY_STRIKE": expr("BUNNY_STRIKE & PIKO_HAMMER"),
        "BUNNY_WHIRL": expr("BUNNY_WHIRL & PIKO_HAMMER"),
        "AIR_DASH": expr("AIR_DASH & PIKO_HAMMER"),
        "AIR_DASH_LV3": expr("AIR_DASH_LV3 & PIKO_HAMMER"),
        "HAMMER_ROLL": expr("HAMMER_ROLL & BUNNY_WHIRL & PIKO_HAMMER"),
        "HAMMER_ROLL_LV3": expr("HAMMER_ROLL_LV3 & BUNNY_WHIRL & PIKO_HAMMER"),
        "DARKNESS": expr("DARKNESS_WITHOUT_LIGHT_ORB | LIGHT_ORB"),
        "UNDERWATER": expr("UNDERWATER_WITHOUT_WATER_ORB | WATER_ORB"),
        "UNDERWATER": expr("TRUE"),
        "BOOST": expr("TRUE"),
        #"RIBBON": expr("TRUE"),
        #"WARP": expr("TRUE"),
        "TRUE": expr("TRUE"),
        "FALSE": expr("FALSE"),
        "NONE": expr("TRUE"),
        "IMPOSSIBLE": expr("FALSE"),
    }

    expr = lambda s : parse_expression(s, variable_names_set, def1)
    def2 = {
        "ITM": expr("INTERMEDIATE"),
        "ITM_HARD": expr("INTERMEDIATE & HARD"),
        "ITM_VHARD": expr("INTERMEDIATE & HARD"),
        "ADV": expr("ADVANCED"),
        "ADV_HARD": expr("ADVANCED & HARD"),
        "ADV_VHARD": expr("ADVANCED & V_HARD"),
        "ADV_STUPID": expr("ADVANCED & STUPID"),
    }
    def1.update(def2)

    expr = lambda s : parse_expression(s, variable_names_set, def1)
    def3 = {
        "HAMMER_ROLL_ZIP": expr("ZIP & HAMMER_ROLL_LV3"),
        "SLIDE_ZIP": expr("ZIP & SLIDING_POWDER"),
        "WHIRL_BONK": expr("BUNNY_WHIRL & ITM_HARD"),
        "WHIRL_BONK_CANCEL": expr("BUNNY_WHIRL & BUNNY_AMULET & ITM_HARD"),
        "SLIDE_JUMP_BUNSTRIKE": expr("BUNNY_STRIKE & INTERMEDIATE"),
        "SLIDE_JUMP_BUNSTRIKE_CANCEL": expr("BUNNY_STRIKE & BUNNY_AMULET & ITM_HARD"),
        "DOWNDRILL_SEMISOLID_CLIP": expr("PIKO_HAMMER_LEVELED & SEMISOLID_CLIP"),

        "EXPLOSIVES": expr("CARROT_BOMB | (CARROT_SHOOTER & BOOST)"),
        "EXPLOSIVES_ENEMY": expr("CARROT_BOMB | CARROT_SHOOTER"),

        "SPEED1": expr("SPEED_BOOST | SPEEDY"),
        "SPEED2": expr("SPEED_BOOST_LV3 | SPEEDY"),
        "SPEED3": expr("SPEED_BOOST_LV3 | (SPEED_BOOST & SPEEDY)"),
        "SPEED5": expr("SPEED_BOOST_LV3 & SPEEDY"),

        "AMULET_FOOD": expr("BUNNY_AMULET | (TOWN_MAIN & (RUMI_DONUT | RUMI_CAKE | COCOA_BOMB | GOLD_CARROT))"),
    }
    def1.update(def3)
    return def1

def get_default_areaids():
    return list(range(10))

TOWN_MEMBERS = ('TM_COCOA','TM_ASHURI','TM_RITA','TM_CICINI','TM_SAYA','TM_SYARO','TM_PANDORA','TM_NIEVE','TM_NIXIE','TM_ARURAUNE','TM_SEANA','TM_LILITH','TM_VANILLA','TM_CHOCOLATE','TM_KOTRI','TM_KEKE_BUNNY',)
def count_town_members(variables):
    return sum([1 for tm in TOWN_MEMBERS if variables[tm]])


def evaluate_pseudo_item_constraints(pseudo_items, variable_names_set, default_expressions):
    for key in pseudo_items.keys():
        if type(pseudo_items[key]) == str:
            pseudo_items[key] = parse_expression_lambda(pseudo_items[key], variable_names_set, default_expressions)


def parse_locations_and_items():
    locations = {}
    items = []
    additional_items = {}
    map_transitions = []

    lines = read_file_and_strip_comments('locations_items.txt')

    type_map = {
        "WARP" : LOCATION_WARP,
        "MAJOR" : LOCATION_MAJOR,
        "MINOR" : LOCATION_MINOR,
    }

    READING_NOTHING = 0
    READING_LOCATIONS = 1
    READING_MAP_TRANSITIONS = 2
    READING_ADDITIONAL_ITEMS = 3
    READING_ITEMS = 4

    currently_reading = READING_NOTHING

    for line in lines:
        if line.startswith('===Locations==='):
            currently_reading = READING_LOCATIONS
        elif line.startswith('===MapTransitions==='):
            currently_reading = READING_MAP_TRANSITIONS
        elif line.startswith('===AdditionalItems==='):
            currently_reading = READING_ADDITIONAL_ITEMS
        elif line.startswith('===Items==='):
            currently_reading = READING_ITEMS
        elif currently_reading == READING_LOCATIONS:
            if len(line) <= 0: continue
            location, location_type = (x.strip() for x in line.split(':'))
            location_type = type_map[location_type]
            if location in locations:
                fail('Location %s already defined!' % location)
            locations[location] = location_type
        elif currently_reading == READING_ADDITIONAL_ITEMS:
            if len(line) <= 0: continue
            item_name, item_id = (x.strip() for x in line.split(':'))
            item_id = int(item_id)
            if item_name in items:
                fail('Additional Item %s already defined!' % item)
            additional_items[item_name] = item_id
        elif currently_reading == READING_ITEMS:
            if len(line) <= 0: continue
            items.append(parse_item_from_string(line))
        elif currently_reading == READING_MAP_TRANSITIONS:
            if len(line) <= 0: continue
            # Line format:
            # area : (x, y, w, h) : origin_location : direction : map_event : trigger_id : entrance_id
            area_current, rect, origin_location, walking_direction, area_target_ev, entry_target_ev, entry_current_ev = [x.strip() for x in line.split(':')]

            if walking_direction == 'MovingRight': walking_right = True
            elif walking_direction == 'MovingLeft': walking_right = False
            else: fail('Undefined map transition direction: %s' % walking_direction)
            area_target = int(area_target_ev) - 161
            entry_target = int(entry_target_ev) - 200
            entry_current = (int(entry_current_ev)-227 if int(entry_current_ev) >= 227 else int(entry_current_ev)-176+6)

            map_transitions.append(MapTransition(
                origin_location = origin_location,
                area_current = int(area_current),
                entry_current = entry_current,
                area_target = area_target,
                entry_target = entry_target,
                walking_right = walking_right,
                rect = rect,
             ))


    # Validate map transition locations
    if set(mt.origin_location for mt in map_transitions) - set(locations.keys()):
        print('Unknown locations: %s' % '\n'.join(
            set(mt.origin_location for mt in map_transitions) - set(locations.keys())
        ))

    return locations, map_transitions, items, additional_items

# throws errors for invalid formats.
def parse_edge_constraints(locations_set, variable_names_set, default_expressions):
    lines = read_file_and_strip_comments('constraints_graph.txt')
    jsondata = ' '.join(lines)
    jsondata = re.sub(',\s*}', '}', jsondata)
    jsondata = '},{'.join(re.split('}\s*{', jsondata))
    jsondata = '[' + jsondata + ']'
    cdicts = parse_json(jsondata)

    constraints = []

    for cdict in cdicts:
        from_location, to_location = (x.strip() for x in cdict['edge'].split('->'))
        if from_location not in locations_set: fail('Unknown location: %s' % from_location)
        if to_location not in locations_set: fail('Unknown location: %s' % to_location)
        prereq = parse_expression(cdict['prereq'], variable_names_set, default_expressions)
        constraints.append(EdgeConstraintData(from_location, to_location, prereq))

    # Validate that there are no duplicate edges defined
    if len(constraints) != len(set(cdict['edge'] for cdict in cdicts)):
        # Error: duplicate edge. Find the duplicate edge.
        edge_names = [cdict['edge'] for cdict in cdicts]
        duplicates = [edge for edge in set(edge_names) if edge_names.count(edge) > 1]
        fail('Duplicate edge definition(s) in constraints!\n%s' % '\n'.join(duplicates))

    return constraints

def parse_item_constraints(items_set, locations_set, variable_names_set, default_expressions):
    lines = read_file_and_strip_comments('constraints.txt')
    jsondata = ' '.join(lines)
    jsondata = re.sub(',\s*}', '}', jsondata)
    jsondata = '},{'.join(re.split('}\s*{', jsondata))
    jsondata = '[' + jsondata + ']'
    cdicts = parse_json(jsondata)

    def parse_alternates(alts):
        if alts == None: return {}
        return dict((name, parse_expression_lambda(constraint, variable_names_set, default_expressions))
            for name, constraint in alts.items())

    item_constraints = []

    valid_keys = set(('item','from_location','to_location','entry_prereq','exit_prereq','alternate_entries','alternate_exits'))
    for cdict in cdicts:
        if not valid_keys.issuperset(cdict.keys()): fail('Unknown keys in item constraint: \n' + str(cdict))
        item, from_location = cdict['item'], cdict['from_location']
        if item not in items_set: fail('Unknown item: %s' % item)
        if from_location not in locations_set: fail('Unknown location: %s' % from_location)

        item_constraints.append(ItemConstraintData(
            item = item,
            from_location = from_location,
            entry_prereq = parse_expression_lambda(cdict['entry_prereq'], variable_names_set, default_expressions),
            exit_prereq = parse_expression_lambda(cdict['exit_prereq'], variable_names_set, default_expressions),
            alternate_entries = parse_alternates(cdict.get('alternate_entries')),
            alternate_exits = parse_alternates(cdict.get('alternate_exits')),
        ))

    # Validate that there are no duplicate items defined
    if len(item_constraints) != len(set(cdict['item'] for cdict in cdicts)):
        # Error: duplicate item. Find the duplicate item.
        item_names = [cdict['item'] for cdict in cdicts]
        duplicates = [item for item in set(item_names) if item_names.count(item) > 1]
        fail('Duplicate item definition(s) in constraints!\n%s' % '\n'.join(duplicates))

    return item_constraints

def read_config(setting_flags, item_locations_set, setting_flags_set, predefined_additional_items_set, settings):
    lines = read_file_and_strip_comments(settings.config_file)
    jsondata = ' '.join(lines)
    jsondata = re.sub(',\s*]', ']', jsondata)
    jsondata = re.sub(',\s*}', '}', jsondata)
    config_dict = parse_json('{' + jsondata + '}')

    to_shuffle = config_dict['to_shuffle']
    must_be_reachable = set(config_dict['must_be_reachable'])
    included_additional_items = config_dict['additional_items']
    settings = config_dict['settings']
    knowledge = config_dict['knowledge']
    difficulty = config_dict['trick_difficulty']

    # Settings
    setting_flags = dict(setting_flags)
    for key, value in settings.items():
        if key not in setting_flags_set:
            fail('Undefined flag: %s' % key)
        if not type(value) is bool:
            fail('Flag %s does not map to a boolean variable in config.txt' % key)
        setting_flags[key] = value


    # Knowledge
    if knowledge == 'BASIC':
        setting_flags[KNOWLEDGE_INTERMEDIATE] = False
        setting_flags[KNOWLEDGE_ADVANCED] = False
    elif knowledge == 'INTERMEDIATE':
        setting_flags[KNOWLEDGE_INTERMEDIATE] = True
        setting_flags[KNOWLEDGE_ADVANCED] = False
    elif knowledge == 'ADVANCED':
        setting_flags[KNOWLEDGE_INTERMEDIATE] = True
        setting_flags[KNOWLEDGE_ADVANCED] = True
    else:
        fail('Unknown knowledge level: %s. Either BASIC, INTERMEDIATE or ADVANCED.' % knowledge)

    # Difficulty
    if difficulty == 'NORMAL':
        setting_flags[DIFFICULTY_HARD] = False
        setting_flags[DIFFICULTY_V_HARD] = False
        setting_flags[DIFFICULTY_STUPID] = False
    elif difficulty == 'HARD':
        setting_flags[DIFFICULTY_HARD] = True
        setting_flags[DIFFICULTY_V_HARD] = False
        setting_flags[DIFFICULTY_STUPID] = False
    elif difficulty == 'V_HARD':
        setting_flags[DIFFICULTY_HARD] = True
        setting_flags[DIFFICULTY_V_HARD] = True
        setting_flags[DIFFICULTY_STUPID] = False
    elif difficulty == 'STUPID':
        setting_flags[DIFFICULTY_HARD] = True
        setting_flags[DIFFICULTY_V_HARD] = True
        setting_flags[DIFFICULTY_STUPID] = True
    else:
        fail('Unknown difficulty level: %s. Either NORMAL, HARD, V_HARD or STUPID.' % difficulty)

    if set(included_additional_items) - predefined_additional_items_set:
        fail('\n'.join[
            'Unknown additional items defined:',
            '\n'.join(map(str, set(included_additional_items) - predefined_additional_items_set)),
        ])

    if set(to_shuffle) - item_locations_set:
        fail('\n'.join[
            'Unknown items defined in config:',
            '\n'.join(map(str, set(to_shuffle) - item_locations_set)),
        ])

    if set(must_be_reachable) - item_locations_set:
        fail('\n'.join[
            'Unknown items defined in config:',
            '\n'.join(map(str, set(must_be_reachable) - item_locations_set)),
        ])

    return setting_flags, to_shuffle, must_be_reachable, included_additional_items


def parse_item_from_string(line):
    pos, areaid, itemid, name = (s.strip() for s in line.split(':', 3))
    import ast
    item = Item(ast.literal_eval(pos), int(areaid), int(itemid))
    if len(name) > 0 and name != 'None':
        item.name = name
    return item

class RandomizerData(object):
    # Attributes:
    #
    # Raw Information
    #
    # dict: setting_flags   (setting_name -> bool)
    # dict: pseudo_items   (psuedo_item_name -> condition)
    # dict: additional_items   (item_name -> item_id)
    # dict: locations   (location -> location_type)
    # list: items   (Item objects)
    # dict: alternate_conditions   (item_name -> constraint lambda)
    # list: edge_constraints   (EdgeConstraintData objects)
    # list: item_constraints   (ItemConstraintData objects)
    # list: map_transitions   (MapTransition objects)
    #
    # Intermediate Information
    #
    # list: item_names
    # list: location_list
    # set: locations_set
    #
    #
    # Preprocessed - Graph
    #
    # list: graph_vertices           (list(node_name))
    # dict: item_locations_in_node   (node_name -> list(item_name))
    # list: initial_edges             (edge_id -> GraphEdge)
    # dict: initial_outgoing_edges     (node_name -> list(edge_id))
    # dict: initial_incoming_edges     (node_name -> list(edge_id))
    #
    #
    # Preprocessed Information
    #
    # list: items_to_allocate
    #
    # list: walking_left_transitions 
    # list: walking_right_transitions 
    #
    # int: nLocations
    # int: nNormalItems
    # int: nAdditionalItems
    # int: originalNEggs
    # int: nEggs


    def __init__(self, settings):
        self.setting_flags = define_setting_flags()
        self.pseudo_items = define_pseudo_items()
        self.locations, self.map_transitions, self.items, self.additional_items = parse_locations_and_items()

        self.nHardToReach = 5

        # Do some preprocessing of variable names        
        self.item_names = [item.name for item in self.items]
        self.location_list = sorted(list(self.locations.keys()))
        self.variable_names_list = self.location_list + \
                                   self.item_names + \
                                   list(self.additional_items.keys()) + \
                                   list(self.pseudo_items.keys()) + \
                                   list(self.setting_flags.keys())
        self.variable_names_list.sort()

        variable_names_set = set(self.variable_names_list)
        if len(variable_names_set) < len(self.variable_names_list):
            # Repeats detected! Fail.
            repeat_names = [x for x in variable_names_set if self.variable_names_list.count(x) > 1]
            fail('Repeat names detected: %s' % ','.join(repeat_names))
        
        self.locations_set = set(self.location_list)
        items_set = set(self.item_names)

        # More config loading
        self.setting_flags, self.to_shuffle, self.must_be_reachable, self.included_additional_items = \
            read_config(self.setting_flags, items_set, set(self.setting_flags.keys()), set(self.additional_items.keys()), settings)

        default_expressions = define_default_expressions(variable_names_set)
        evaluate_pseudo_item_constraints(self.pseudo_items, variable_names_set, default_expressions)
        self.alternate_conditions = define_alternate_conditions(variable_names_set, default_expressions)
        self.edge_constraints = parse_edge_constraints(self.locations_set, variable_names_set, default_expressions)
        self.item_constraints = parse_item_constraints(items_set, self.locations_set, variable_names_set, default_expressions)

        self.preprocess_data(settings)
        self.preprocess_variables(settings)
        self.preprocess_graph(settings)

    def preprocess_variables(self, settings):
        # Mark all unconstrained pseudo-items
        variables = dict((name, False) for name in self.variable_names_list)
        variables.update(self.setting_flags)

        to_remove = set()
        unreached_pseudo_items = dict()
        has_changes = True
        while has_changes:
            has_changes = False
            to_remove.clear()
            for condition, target in unreached_pseudo_items.items():
                if condition(variables):
                    variables[target] = True
                    to_remove.append(target)
                    has_changes = True

            for target in to_remove:
                del unreached_pseudo_items[target]

        self.default_variables = variables

    def preprocess_graph(self, settings):
        default_variables = self.default_variables

        # Partial Graph Construction
        graph_vertices = list(self.location_list)
        item_locations_in_node = dict((node, []) for node in graph_vertices)
        edges = []
        for item_constraint in self.item_constraints:
            if item_constraint.no_alternate_paths and \
                    item_constraint.entry_prereq(default_variables) and \
                    item_constraint.exit_prereq(default_variables):
                # Unconstrained - Merge directly into from_location
                item_locations_in_node[item_constraint.from_location].append(item_constraint.item)
            else:
                # Constrained - Create new node
                item_node_name = 'ITEM_%s' % item_constraint.item
                graph_vertices.append(item_node_name)
                item_locations_in_node[item_node_name] = [item_constraint.item]

                edges.append(GraphEdge(
                    edge_id=len(edges),
                    from_location=item_constraint.from_location,
                    to_location=item_node_name,
                    constraint=item_constraint.entry_prereq,
                    backtrack_cost=0,
                ))

                edges.append(GraphEdge(
                    edge_id=len(edges),
                    from_location=item_node_name,
                    to_location=item_constraint.from_location,
                    constraint=item_constraint.exit_prereq,
                    backtrack_cost=0,
                ))

                for entry_node, prereq in item_constraint.alternate_entries.items():
                    edges.append(GraphEdge(
                        edge_id=len(edges),
                        from_location=entry_node,
                        to_location=item_node_name,
                        constraint=prereq,
                        backtrack_cost=1,
                    ))

                for exit_node, prereq in item_constraint.alternate_exits.items():
                    edges.append(GraphEdge(
                        edge_id=len(edges),
                        from_location=item_node_name,
                        to_location=exit_node,
                        constraint=prereq,
                        backtrack_cost=1,
                    ))

        initial_outgoing_edges = dict((node, []) for node in graph_vertices)
        initial_incoming_edges = dict((node, []) for node in graph_vertices)

        for edge in edges:
            initial_outgoing_edges[edge.from_location].append(edge.edge_id)
            initial_incoming_edges[edge.to_location].append(edge.edge_id)

        self.graph_vertices = graph_vertices
        self.item_locations_in_node = item_locations_in_node
        self.initial_edges = edges
        self.initial_outgoing_edges = initial_outgoing_edges
        self.initial_incoming_edges = initial_incoming_edges


    def preprocess_data(self, settings):
        ### For item shuffle
        to_shuffle_set = set(self.to_shuffle)
        do_not_shuffle = [item.name for item in self.items if not item.name in to_shuffle_set]

        items_to_shuffle = [item_name for item_name in self.to_shuffle if not is_egg(item_name)]
        unshuffled_items = [item_name for item_name in do_not_shuffle if not is_egg(item_name)]

        eggs_to_shuffle = [item_name for item_name in self.to_shuffle if is_egg(item_name)]
        unshuffled_eggs = [item_name for item_name in do_not_shuffle if is_egg(item_name)]

        self.nItemSpots = len(self.to_shuffle)
        self.nNormalItems = len(items_to_shuffle)
        self.nAdditionalItems = len(self.included_additional_items)
        self.nOriginalEggs = len(eggs_to_shuffle)


        # Remove eggs so that number of items to allocate == number of locations
        self.nEggs = self.nOriginalEggs - self.nAdditionalItems
        if self.nEggs < 0:
            fail('Too few eggs to remove to make room for additional items.')

        self.items_to_allocate = items_to_shuffle + self.included_additional_items + eggs_to_shuffle[:self.nEggs]
        self.item_slots = items_to_shuffle + eggs_to_shuffle
        self.unshuffled_allocations = list(zip(unshuffled_items, unshuffled_items))
        if settings.egg_goals:
            minShuffledEggs = self.nHardToReach + settings.extra_eggs
            if self.nEggs < minShuffledEggs:
                fail('Not enough shuffled eggs for egg goals. Needs at least %d.' % minShuffledEggs)
            self.unshuffled_allocations += [(egg_loc, None) for egg_loc in unshuffled_eggs]
        else:
            self.unshuffled_allocations += list(zip(unshuffled_eggs, unshuffled_eggs))

        # map_transitions
        walking_right_transitions = [tr for tr in self.map_transitions if tr.walking_right]
        walking_right_transitions.sort(key=lambda tr : (tr.origin_location, tr.rect))
        walking_left_transitions = []

        left_transition_dict = dict(( (tr.area_current, tr.entry_current), tr )
            for tr in self.map_transitions if not tr.walking_right)
        print(len(walking_right_transitions), len(left_transition_dict))
        for rtr in walking_right_transitions:
            key = (rtr.area_target, rtr.entry_target)
            ltr = left_transition_dict.get(key)
            if ltr == None:
                fail('Matching map transition not found for %s' % rtr.origin_location)
            if rtr.area_current != ltr.area_target or rtr.entry_current != ltr.entry_target:
                fail("Map transitions don't match! %s vs %s" % (rtr.origin_location, ltr.origin_location))
            walking_left_transitions.append(ltr)
            del left_transition_dict[key]

        for ltr in left_transition_dict.values():
            fail('Matching map transition not found for %s' % ltr.origin_location)

        self.walking_right_transitions = walking_right_transitions
        self.walking_left_transitions = walking_left_transitions


    def generate_variables(self):
        return dict(self.default_variables)



class Analyzer(object):
    def __init__(self, allocation, data, settings):
        self.allocation = allocation
        self.data = data
        self.settings = settings

    def compute_difficulty_ratings(self):
        pass



def run_item_randomizer(data, settings):
    generator = Generator(data, settings)

    attempts = 0
    while True:
        attempts += 1
        generator.shuffle()
        if generator.verify():
            if settings.egg_goals:
                generator.shift_eggs_to_hard_to_reach()
                if generator.verify():
                    break
            else:
                break

    log('Computed after %d attempts' % attempts)
    return generator.allocation


def generate_randomized_maps(settings):
    if write_to_map_files and not os.path.isdir(output_dir):
        fail('Output directory %s does not exist' % output_dir)

    data = RandomizerData()
    allocation = run_item_randomizer(data, settings)
    analyzer = Analysis(allocation, data, settings)

    areaids = get_default_areaids()
    assert len(set(item.areaid for item in data.items) - set(areaids)) == 0

    generate_analysis_file(allocation, analyzer, settings)
    log('Analysis Generated.')

    if not write_to_map_files:
        log('No maps generated as no-write flag is on.')
        return

    if not itemreader.exists_map_files(areaids, source_dir):
        fail('Maps not found in the directory %s! Place the original Rabi-Ribi maps '
             'in this directory for the randomizer to work.' % source_dir)

    itemreader.grab_original_maps(source_dir, output_dir)
    log('Maps copied...')
    mod = itemreader.ItemModifier(areaids, settings)
    pre_modify_map_data(mod, settings)

    mod.clear_items()
    for item in items:
        mod.add_item(item)
    mod.save(output_dir)
    log('Maps saved successfully to %s.' % output_dir)

    hash_digest = hash_map_files(areaids, output_dir)
    log('Hash: %s' % hash_digest)

def apply_map_transition_shuffle(mod, data, settings, allocation):
    events_2d_dict = {}
    for areaid, tiledata in mod.stored_datas.items():
        tiledata_event = tiledata.tiledata_event
        events_2d_dict[areaid] = [tiledata_event[i:i+200] for i in range(0,len(tiledata_event),200)]

    def set_target_in_map(transition, area_target, entry_target):
        events_2d = events_2d_dict[transition.area_current]
        tiledata_event = mod.stored_datas[transition.area_current].tiledata_event
        x1,y1,w,h = transition.rect
        events_cropped = [x for row in events_2d[x1:x1+w] for x in row[y1:y1+h]]

        original_map_event = transition.area_target + 161
        original_entry_event = transition.entry_target + 200
        new_map_event = area_target + 161
        new_entry_event = entry_target + 200

        for i in (i for i,ev in enumerate(events_cropped) if ev == original_map_event):
            tiledata_event[xy_to_index(x1+i//h, y1+i%h)] = new_map_event

        for i in (i for i,ev in enumerate(events_cropped) if ev == original_entry_event):
            tiledata_event[xy_to_index(x1+i//h, y1+i%h)] = new_entry_event

    for rtr, ltr in zip(data.walking_right_transitions, allocation.walking_left_transitions):
        set_target_in_map(rtr, ltr.area_current, ltr.entry_current)
        set_target_in_map(ltr, rtr.area_current, rtr.entry_current)


def insert_items_into_map(mod, data, settings, allocation):
    name_to_id = dict((item.name, item.itemid) for item in data.items)
    name_to_id.update(data.additional_items)

    mod.clear_items()
    for original_item in data.items:
        item = original_item.copy()
        item_at_location = allocation.item_at_item_location[item.name]
        if item_at_location != None:
            #item.name = item_at_location
            item.itemid = name_to_id[item_at_location]
            mod.add_item(item)


def get_default_areaids():
    return list(range(10))


def run_randomizer(seed, source_dir, settings):
    if seed != None: random.seed(seed)
    randomizer_data = RandomizerData(settings)
    generator = Generator(randomizer_data, settings)
    allocation, analyzer = generator.generate_seed()
    print('done')

    areaids = get_default_areaids()
    if not mapfileio.exists_map_files(areaids, source_dir):
        fail('Maps not found in the directory %s! Place the original Rabi-Ribi maps '
             'in this directory for the randomizer to work.' % source_dir)

    mapfileio.grab_original_maps(source_dir, settings.output_dir)
    print('Maps copied...')
    mod = mapfileio.ItemModifier(areaids, source_dir=source_dir, no_load=True)
    #pre_modify_map_data(mod, apply_fixes=apply_fixes, open_mode=open_mode, shuffle_music=shuffle_music, shuffle_backgrounds=shuffle_backgrounds, no_laggy_backgrounds=no_laggy_backgrounds, no_difficult_backgrounds=no_difficult_backgrounds, super_attack_mode=super_attack_mode, hyper_attack_mode=hyper_attack_mode)
    #apply_item_specific_fixes(mod, assigned_locations)
    apply_map_transition_shuffle(mod, randomizer_data, settings, allocation)
    insert_items_into_map(mod, randomizer_data, settings, allocation)

    mod.save(settings.output_dir)
    print('Maps saved successfully to %s.' % settings.output_dir)

    hash_digest = hash_map_files(areaids, settings.output_dir)
    print('Hash: %s' % hash_digest)


if __name__ == '__main__':
    args = parse_args()
    source_dir='original_maps'

    if args.seed == None:
        seed = None
    else:
        seed = string_to_integer_seed('%s_ha:%s_hd:%s' % (args.seed, args.hide_unreachable, args.hide_difficulty))

    run_randomizer(seed, source_dir, args)
