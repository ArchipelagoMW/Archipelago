import argparse
import random
from utility import *

START_LOCATION = 'FOREST_START'

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
    return args.parse_args(sys.argv[1:])


def define_setting_flags():
    return {
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
    }

def define_difficulty_flags():
    # Difficulty Flags
    d.update({
        KNOWLEDGE_INTERMEDIATE: False,
        KNOWLEDGE_ADVANCED: False,
        DIFFICULTY_HARD: False,
        DIFFICULTY_V_HARD: False,
        DIFFICULTY_STUPID: False,
    })

# The values can be either a expression constrant, which is expressed as a string,
# or a lambda, that takes in a variables object and returns a bool.
def define_pseudo_items():
    return {
        "WALL_JUMP_LV2": "WALL_JUMP & SHOP",
        "HAMMER_ROLL_LV3": "rHAMMER_ROLL & SHOP & CHAPTER_3",
        "AIR_DASH_LV3": "rAIR_DASH & SHOP",
        "SPEED_BOOST_LV3": "SPEED_BOOST & SHOP",
        "BUNNY_AMULET_LV2": "(BUNNY_AMULET & SHOP) | CHAPTER_3"
        "BUNNY_AMULET_LV3": "(BUNNY_AMULET & SHOP) | CHAPTER_4"
        "PIKO_HAMMER_LEVELED": "PIKO_HAMMER",
        "SHOP": "TOWN_MAIN",

        "COCOA_1": "FOREST_START",
        "KOTRI_1": "PARK_MAIN",

        "COCOA": "COCOA_1 & KOTRI_1 & CAVE_COCOA",
        "ASHURI": "RIVERBANK_MAIN & TOWN_MAIN & SPECTRAL_WEST",
        "RITA": "SNOWLAND_EAST",
        "RIBBON": "SPECTRAL_WARP",
        "CICINI": "SPECTRAL_CICINI_ROOM",
        "SAYA": "EVERNIGHT_SAYA & EVERNIGHT_EAST_OF_WARP",
        "SYARO": "SYSTEM_INTERIOR_MAIN",
        "PANDORA": "PYRAMID_MAIN",
        "NIEVE": "PALACE_MAIN & ICY_SUMMIT_MAIN",
        "NIXIE": "PALACE_MAIN & ICY_SUMMIT_MAIN",
        "ARURAUNE": "FOREST_NIGHT_WEST",
        "SEANA": "VANILLA & CHOCOLATE & CICINI & SYARO & NIEVE & NIXIE & AQUARIUM_MAIN & PARK_MAIN",
        "LILITH": "SKY_ISLAND_MAIN",
        "VANILLA": "SKY_BRIDGE_EAST",
        "CHOCOLATE": "RAVINE_CHOCOLATE",
        "KOTRI": "GRAVEYARD_MAIN & VOLCANIC_MAIN",
        "KEKE_BUNNY": "PLURKWOOD_MAIN",

        "2TM": lambda v: count_town_members(v) >= 2,
        "3TM": lambda v: count_town_members(v) >= 3,
        "4TM": lambda v: count_town_members(v) >= 4,
        "7TM": lambda v: count_town_members(v) >= 7,
        "SPEEDY": "CICINI & TOWN_MAIN & 3TM",

        "CHAPTER_1": "TOWN_MAIN",
        "CHAPTER_2": "TOWN_MAIN & 2TM",
        "CHAPTER_3": "TOWN_MAIN & 4TM",
        "CHAPTER_4": "TOWN_MAIN & 7TM",
    }

def define_alternate_conditions(variable_names_set, default_expressions):
    d = {
        "SPEED_BOOST": "SHOP",
        "SOUL_HEART": "SHOP",
        "BOOK_OF_CARROT": "SHOP",
        "P_HAIRPIN": "KEKE_BUNNY & PLURKWOOD_MAIN",
        "HEALING_STAFF": "SHOP",
        "MAX_BRACELET": "SHOP",
        "BUNNY_STRIKE": "SLIDING_POWDER & SHOP",
        "STRANGE_BOX": "SYARO & TOWN_MAIN",
        "BUNNY_AMULET": "CHAPTER_2",
        "RUMI_DONUT": "SHOP",
        "RUMI_CAKE": "SHOP",
        "COCOA_BOMB": "COCOA & TOWN_MAIN",
    }

    for key in d.keys():
        if type(d[key]) == str:
            d[key] = parse_expression_lambda(d[key], variable_names_set, default_expressions)
    return d


def define_default_expressions(variable_names_set):
    # Default expressions take priority over actual variables.
    # so if we parse an expression that has AIR_DASH, the default expression AIR_DASH will be used instead of the variable AIR_DASH.
    # however, the expressions parsed in define_default_expressions (just below) cannot use default expressions in their expressions.
    expr = lambda s : parse_expression(s, variables)
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
        "UNDERWATER": expr("TRUE"),
        "BOOST": expr("TRUE"),
        #"RIBBON": expr("TRUE"),
        #"WARP": expr("TRUE"),
        "TRUE": expr("TRUE"),
        "FALSE": expr("FALSE"),
        "NONE": expr("TRUE"),
        "IMPOSSIBLE": expr("FALSE"),
    }
    expr = lambda s : parse_expression(s, variables, def1)
    def2 = {
        "HAMMER_ROLL_ZIP": expr("ZIP & HAMMER_ROLL_LV3"),
        "SLIDE_ZIP": expr("ZIP & SLIDING_POWDER"),
        "EXPLOSIVES": expr("CARROT_BOMB | (CARROT_SHOOTER & BOOST)"),
        "EXPLOSIVES_ENEMY": expr("CARROT_BOMB | CARROT_SHOOTER"),
        "SPEED": expr("SPEED_BOOST | SPEEDY"),
        "SUPER_SPEED": expr("SPEED_BOOST_LV3 & SPEEDY"),
    }

    def1.update(def2)
    return def1

def get_default_areaids():
    return list(range(10))

TOWN_MEMBERS = []
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

    lines = read_file_and_strip_comments('locations_items.txt')

    type_map = {
        "WARP" : LOCATION_WARP,
        "MAJOR" : LOCATION_MAJOR,
        "MINOR" : LOCATION_MINOR,
    }

    READING_NOTHING = 0
    READING_LOCATIONS = 1
    READING_ADDITIONAL_ITEMS = 2
    READING_ITEMS = 3

    currently_reading = READING_NOTHING

    for line in lines:
        if line.startswith('===Locations==='):
            currently_reading = READING_LOCATIONS
        elif line.startswith('===AdditionalItems==='):
            currently_reading = READING_ADDITIONAL_ITEMS
        elif line.startswith('===Items==='):
            currently_reading = READING_ITEMS
        elif currently_reading == READING_LOCATIONS:
            if len(line) > 0:
                location, location_type = (x.strip() for x in line.split(':'))
                location_type = type_map[location_type]
                if location in locations:
                    fail('Location %s already defined!' % location)
                locations[location] = location_type
        elif currently_reading == READING_ADDITIONAL_ITEMS:
            if len(line) > 0:
                item, item_id = (x.strip() for x in line.split(':'))
                item_id = int(item_id)
                if item in items:
                    fail('Additional Item %s already defined!' % item)
                items[item] = item_id
        elif currently_reading == READING_ITEMS:
            if len(line) > 0:
                items.append(itemreader.parse_item_from_string(line))

    return locations, items, additional_items

# throws errors for invalid formats.
def parse_edge_constraints(graph_vertices_set, variable_names_set, default_expressions):
    lines = read_file_and_strip_comments('constraints.txt')
    jsondata = ' '.join(lines)
    jsondata = re.sub(',\s*}', '}', jsondata)
    jsondata = '},{'.join(re.split('}\s*{', jsondata))
    jsondata = '[' + jsondata + ']'
    cdicts = parse_json(jsondata)

    constraints = []

    for cdict in cdicts:
        from_location, to_location = (x.strip() for x in cdict['edge'].split('->'))
        if from_location not in graph_vertices_set: fail('Unknown location: %s' % from_location)
        if to_location not in graph_vertices_set: fail('Unknown location: %s' % to_location)
        prereq = parse_expression(cdict['prereq'], variable_names_set, default_expressions)
        constraints.append(EdgeConstraint(from_location, to_location, prereq))

    return constraints


def parse_map_transitions(graph_vertices_set):
    return [
    ]


def read_config(variable_names_list, item_locations_set, setting_flags_set, predefined_additional_items_set):
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
    difficulty = config_dict['difficulty']

    # Knowledge
    if knowledge == 'BASIC':
        variables[KNOWLEDGE_INTERMEDIATE] = False
        variables[KNOWLEDGE_ADVANCED] = False
    elif knowledge == 'INTERMEDIATE':
        variables[KNOWLEDGE_INTERMEDIATE] = True
        variables[KNOWLEDGE_ADVANCED] = False
    elif knowledge == 'ADVANCED':
        variables[KNOWLEDGE_INTERMEDIATE] = True
        variables[KNOWLEDGE_ADVANCED] = True
    else:
        fail('Unknown knowledge level: %s. Either BASIC, INTERMEDIATE or ADVANCED.' % knowledge)

    # Difficulty
    if difficulty == 'NORMAL':
        variables[DIFFICULTY_HARD] = False
        variables[DIFFICULTY_V_HARD] = False
        variables[DIFFICULTY_STUPID] = False
    elif difficulty == 'HARD':
        variables[DIFFICULTY_HARD] = True
        variables[DIFFICULTY_V_HARD] = False
        variables[DIFFICULTY_STUPID] = False
    elif difficulty == 'V_HARD':
        variables[DIFFICULTY_HARD] = True
        variables[DIFFICULTY_V_HARD] = True
        variables[DIFFICULTY_STUPID] = False
    elif difficulty == 'STUPID':
        variables[DIFFICULTY_HARD] = True
        variables[DIFFICULTY_V_HARD] = True
        variables[DIFFICULTY_STUPID] = True
    else:
        fail('Unknown difficulty level: %s. Either NORMAL, HARD, V_HARD or STUPID.' % difficulty)



    # Settings
    variables = dict((name, False) for name in variable_names_list)
    for key, value in settings.items():
        if key not in setting_flags_set:
            fail('Undefined flag: %s' % key)
        if not type(value) is bool:
            fail('Flag %s does not map to a boolean variable in config.txt' % key)
        variables[key] = value

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

    return variables, to_shuffle, must_be_reachable, included_additional_items


### Enums
LOCATION_WARP = 0
LOCATION_MAJOR = 1
LOCATION_MINOR = 2

NO_CONDITIONS = lambda v : True

"""
Variable types:
1. Locations
    - Warp locations - locations with a warp stone
    - Major locations - must have unconstrained path to warp stone
    - Minor locations - cannot have autosave or save points within
2. Items (Item Locations)
3. Additional Items (Items without locations)
4. Pseudo Items
"""

"""




"""

"""
Settings:
- shuffle_items
- shuffle_map_transitions
"""

class MapTransition(object):
    def __init__(self, origin_location, area_current, entry_current, area_target, entry_target, walking_right):
        self.origin_location = origin_location
        self.area_current = area_current
        self.entry_current = entry_current
        self.area_target = area_target
        self.entry_target = entry_target
        self.walking_right = walking_right


class EdgeConstraint(object):
    def __init__(self, from_location, to_location, prereq_expression):
        self.from_location = from_location
        self.to_location = to_location
        #self.prereq_expression = prereq_expression
        self.prereq_lambda = lambda v : prereq_expression.evaluate(v)

    def __str__(self):
        return '\n'.join([
            'From: %s' % self.from_location,
            'To: %s' % self.to_location,
            'Prereq: %s' % self.prereq_expression,
        ])


class RandomizerData(object):
    # Attributes:
    #
    # Raw Information
    #
    # dict: setting_flags   (setting_name -> bool)
    # dict: pseudo_items   (condition -> psuedo_item_name)
    # dict: locations   (location -> location_type)
    # list: items   (Item objects)
    # list: edge_constraints   (Constraint objects)
    # dict: additional_items   (item_name -> item_id)
    # list: map_transitions   (MapTransition objects)
    #
    # Intermediate Information
    #
    # list: item_locations
    # list: graph_vertices
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


    def __init__(self):
        self.setting_flags = define_setting_flags()
        self.pseudo_items = define_pseudo_items()
        self.additional_item_conditions = define_additional_item_conditions()
        self.locations, self.items, self_additional_items = parse_locations_and_items()

        # Do some preprocessing of variable names        
        self.item_locations = [item.name for item in data.items]
        self.graph_vertices = list(data.locations.keys()) + self.item_locations
        variable_names_list = list(self.locations.keys()) + \
                              self.item_locations + \
                              list(self.additional_items.keys()) + \
                              list(self.pseudo_items.values()) + \
                              list(self.setting_flags.keys())
        variable_names_list.sort()

        variable_names_set = set(variable_names_list)
        if len(variable_names_set) < len(variable_names_list):
            # Repeats detected! Fail.
            repeat_names = [x for x in variable_names_set if variable_names_list.count(x) > 1]
            fail('Repeat names detected: %s' % ','.join(repeat_names))
        
        graph_vertices_set = set(self.graph_vertices)


        # More config loading
        self.variables, self.to_shuffle, self.must_be_reachable, self_included_additional_items = \
            read_config(variable_names_list, set(self.item_locations), set(self.setting_flags.keys()), set(self.additional_item_conditions.keys()))

        default_expressions = define_default_expressions(variable_names_set)
        evaluate_pseudo_item_constraints(self.pseudo_items, variable_names_set, default_expressions)
        self.alternate_conditions = define_alternate_conditions(variable_names_set, default_expressions)
        self.edge_constraints = parse_edge_constraints(graph_vertices_set, variable_names_set, default_expressions)

        self.map_transitions = parse_map_transitions(graph_vertices_set)

        self.preprocess_data()

    def preprocess_data(self):

        ### For item shuffle
        normal_items = [item.name for item in data.items if not is_egg(item.name)]
        additional_items = list(data.additional_items.keys())
        eggs = [item.name for item in data.items if is_egg(item.name)]

        self.nLocations = len(item_locations)
        self.nNormalItems = len(items)
        self.nAdditionalItems = len(additional_items)
        self.originalNEggs = len(eggs)

        # Remove eggs so that number of items to allocate == number of locations
        self.nEggs = se.originalNEggs - self.nAdditionalItems
        self.items_to_allocate = normal_items + additional_items + eggs[:self.nEggs]

        # map_transitions
        walking_right_transitions = [tr for tr in self.map_transitions if tr.walking_right]
        walking_right_transitions.sort(key=lambda tr : tr.origin_location)
        walking_left_transitions = []

        left_transition_dict = dict(( (tr.area_current, tr.entry_current), tr )
            for tr in self.map_transitions if not tr.walking_right)

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
        variables = dict((name, False) for name in self.variables)
        variables.update(setting_flags)
        return variables

    def pseudo_item_conditions(self):
        return self.pseudo_items


class Allocation(object):
    # Attributes:
    # 
    # list: items_to_allocate
    #
    # dict: item_at_location  (location -> item at location)
    #
    # dict: outgoing_conditions  item_location -> list(condition -> item_location)
    # dict: incoming_conditions  item_location -> list(condition -> item_location)

    def __init__(self, data, settings):
        self.items_to_allocate = list(data.items_to_allocate)
        self.walking_left_transitions = list(data.walking_left_transitions)


    def shuffle(self, data, settings):
        # Shuffle Items
        self.allocate_items(data, settings)

        # Shuffle Locations
        self.construct_graph(data, settings)


    def allocate_items(self, data, settings):
        item_locations = data.item_locations

        if not settings.shuffle_items:
            self.item_at_location = dict(zip(item_locations, item_locations))
            return

        random.shuffle(items_to_allocate)

        # A map of location -> item at location
        self.item_at_location = dict(zip(item_locations, items_to_allocate))


    def construct_graph(self, data, settings):
        outgoing_conditions = dict((loc, []) for loc in data.graph_vertices)
        incoming_conditions = dict((loc, []) for loc in data.graph_vertices)

        # Constraints
        for constraint in data.edge_constraints:
            outgoing_conditions[constraint.from_location].append((constraint.prereq_lambda, constraint.to_location))
            incoming_conditions[constraint.to_location].append((constraint.prereq_lambda, constraint.from_location))

        # Map Transitions
        if settings.shuffle_map_transitions:
            random.shuffle(self.walking_left_transitions)

        for rtr, ltr in zip(data.walking_right_transitions, self.walking_left_transitions):
            outgoing_conditions[rtr.origin_location].append((NO_CONDITIONS, ltr.origin_location]))
            incoming_conditions[rtr.origin_location].append((NO_CONDITIONS, ltr.origin_location]))
            outgoing_conditions[ltr.origin_location].append((NO_CONDITIONS, rtr.origin_location]))
            incoming_conditions[ltr.origin_location].append((NO_CONDITIONS, rtr.origin_location]))

        self.outgoing_conditions = outgoing_conditions
        self.incoming_conditions = incoming_conditions

    def shift_eggs_to_hard_to_reach(self, data, settings):
        analyzer = Analyzer(self, data, settings)
        difficulty_ratings = analyzer.compute_difficulty_ratings()
        pass


class Generator(object):
    def __init__(self, data, settings):
        self.data = data
        self.settings = settings
        self.allocation = Allocation(data, settings)

    def shuffle(self):
        self.allocation.shuffle(self.data, self.settings)

    def shuft_eggs_to_hard_to_reach(self):
        self.allocation.shift_eggs_to_hard_to_reach(self, data, settings)

    def verify(self):
        if not self.verify_warps_reachable():
            return False
        if not self.verify_reachable_items():
            return False

    def verify_warps_reachable(self):
        variables = self.data.generate_variables()

        dfs_stack = [location for location, loc_type in self.data.locations.items() if loc_type == LOCATION_WARP]
        visited = set(dfs_stack)

        while len(dfs_stack) > 0:
            current = dfs_stack.pop()
            for condition, target in allocation.incoming_conditions(target):
                if target in visited: continue
                if condition(variables):
                    visited.add(target)
                    dfs_stack.append(target)

        major_locations = set(location for location, loc_type in self.data.locations.items() if loc_type == LOCATION_MAJOR)

        return len(major_locations - visited) == 0


    def verify_reachable_items(self):
        data = self.data
        allocation = self.allocation

        variables = self.data.generate_variables()

        enterable_nodes = set()
        exitable_nodes = set()

        # the frontier stores edges
        entry_frontier = {NO_CONDITION : START_LOCATION}
        exit_frontier = dict((NO_CONDITION, location)
            for location, loc_type in data.locations.items() if loc_type != LOCATION_MINOR)

        unreached_pseudo_items = dict(data.pseudo_item_conditions())

        to_remove = []
        items_to_remove = set()
        exit_check_item_locations = set()

        items_exiting_to_target = dict((item_location, set()) for item_location in data.item_locations)

        # Alternate between graph and pseudo items
        has_variable_changes = True
        while has_variable_changes:
            has_variable_changes = False

            # Graph loop
            has_frontier_changes = True
            while has_frontier_changes:
                has_frontier_changes = False

                to_remove.clear()
                for condition, target in entry_frontier.items():
                    if target in enterable_nodes:
                        to_remove.append(condition)
                    elif condition(variables):
                        # Note: This block is only run once per location.
                        to_remove.append(condition)
                        enterable_nodes.add(target)
                        entry_frontier.update(allocation.outgoing_conditions[target])

                        item = allocation.item_at_location.get(target)
                        if item != None:
                            exit_check_item_locations[target] = item, {NO_CONDITION : target}, set()

                        has_frontier_changes = True

                for c in to_remove: del entry_frontier[c]

                to_remove.clear()
                for condition, target in exit_frontier.items():
                    if target in exitable_nodes:
                        to_remove.append(condition)
                    elif condition(variables):
                        # Note: This block is only run once per location.
                        to_remove.append(condition)
                        exitable_nodes.add(target)
                        exit_frontier.update(allocation.incoming_conditions[target])

                        for item_location in items_exiting_to_target[target]:
                            if item_location in exit_check_item_locations:
                                # Can obtain item: When exitable_nodes meets Item Exit Loop
                                del exit_check_item_locations[item_location]
                                item = allocation.item_at_location.get(target)
                                assert item != None
                                variables[item] = True

                        has_frontier_changes = True

                for c in to_remove: del exit_frontier[c]

            # Pseudo Item Loop
            # TODO: Test whether removing this loop is faster!
            has_frontier_changes = True
            while has_frontier_changes:
                has_frontier_changes = False

                to_remove.clear()
                for condition, target in unreached_pseudo_items.items():
                    if condition(variables):
                        to_remove.append(condition)
                        variables[target] = True
                        has_frontier_changes, has_variable_changes = True, True

                for c in to_remove: del unreached_pseudo_items[c]


            items_to_remove.clear()
            # Item Exit Loops. For items that are enterable but not exitable.
            for item_location, item_data in exit_check_item_locations.items():
                item, item_frontier, item_reachable = item_data

                assert not variables[item]:

                item_reached = False
                # Set variables[item] to True temporarily
                variables[item] = True

                has_frontier_changes = True
                while has_frontier_changes:
                    has_frontier_changes = False

                    to_remove.clear()
                    for condition, target in item_frontier.items():
                        if target in item_reachable:
                            to_remove.append(condition)
                        elif condition(variables):
                            # Note: This block is only run once per location per item.
                            to_remove.append(condition)

                            # visit target.
                            if target in exitable_nodes:
                                # Can obtain item: When Item Exit Loop meets exitable_nodes
                                item_reached = True
                                has_frontier_changes = False
                                break
                            else:
                                items_exiting_to_target[target].add(item_location)

                            item_reachable.add(target)
                            exit_frontier.update(allocation.incoming_conditions(target))

                            has_frontier_changes = True

                    for c in to_remove: del item_frontier[c]

                if item_reached:
                    items_to_remove.add(item)
                    #variables[item] = True # Already set
                else:
                    variables[item] = False

            for item_location in items_to_remove: del exit_check_item_locations[item_location]


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

if __name__ == '__main__':
    args = parse_args()
    source_dir='original_maps'

    if args.seed == None:
        seed = None
    else:
        seed = string_to_integer_seed('%s_ha:%s_hd:%s' % (args.seed, args.hide_unreachable, args.hide_difficulty))
    
    pass
