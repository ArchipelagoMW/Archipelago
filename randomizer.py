import random
from utility import *

START_LOCATION = 'FOREST_START'

def define_setting_flags():
    return {

    }


def define_pseudo_items():
    return {

    }



def parse_locations_and_items():
    locations = set()
    items = {}
    return locations, items



def parse_edge_constraints():
    return {
    }

def parse_map_transitions():
    return [
    ]


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
3. Pseudo Items
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
    # Preprocessed Information
    #
    # list: item_locations
    # list: graph_vertices
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

        # self.locations: dict, location_name -> location_type
        # self.items: list, Item() objects
        self.locations, self.items = parse_locations_and_items()

        self.edge_constraints = parse_edge_constraints()

        # dict, item_name -> item_id
        self.additional_items = parse_additional_items()

        self.map_transitions = parse_map_transitions()

        self.preprocess_data()

    def preprocess_data(self):
        self.item_locations = [item.name for item in data.items]
        self.graph_vertices = list(data.locations.keys()) + self.item_locations

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
        variables = dict((name, False) for name in self.graph_vertices + list(pseudo_items.values()))
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

    def shift_eggs_to_hard_to_reach(self):
        difficulty_ratings = Analyzer.analyse(self)
        pass


class Generator(object):
    def __init__(self, data, settings):
        self.data = data
        self.allocation = Allocation(data, settings)

    def shuffle(self):
        self.allocation = Allocation(data, settings)

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
    pass



def randomize():
    data = RandomizerData()
    generator = Generator(data)

