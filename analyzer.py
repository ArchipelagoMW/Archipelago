import random
from utility import *

START_LOCATION = 'FOREST_START'

class Analyzer(object):
    # -- Results --
    #
    # success: bool (True if verification success, False otherwise)
    # error_message: string (error message if success == False)
    #
    # -- The following attributes will only be assigned if success == True. --
    # reachable
    # unreachable
    # levels
    # hard_to_reach_items

    def __init__(self, data, allocation, visualize=False):
        self.data = data
        self.allocation = allocation
        self.visualize = visualize

        self.error_message = ''
        self.success = self.run_verifier()

    def run_verifier(self):
        result, backward_exitable = self.verify_warps_reachable()
        if not result:
            self.error_message = 'Not all warps reachable.'
            return False
        reachable, unreachable, levels = self.verify_reachable_items(backward_exitable)

        # ensure all must_be_reachable items are reachable.
        if not set(self.data.must_be_reachable).issubset(reachable):
            self.error_message = 'Not all must_be_reachable items are reachable.'
            return False

        error = self.process_verification_results(reachable, unreachable, levels)
        if error:
            self.error_message = error
            return False

        return True

    def process_verification_results(self, reachable, unreachable, levels):
        #all_levels = [x for x in levels for x in x]
        #print(set(reachable) - set(all_levels))
        #print(len(all_levels), len(set(all_levels)), len(reachable), len(unreachable))
        #print(set(all_levels) - set(reachable))
        
        allocated_items_set = set(self.data.items_to_allocate)
        nHardToReach = self.data.nHardToReach
        minHardToReachPoolSize = nHardToReach * 3

        hard_to_reach_all = []
        for level in reversed(levels):
            # sort to make it deterministic
            hard_to_reach_all += sorted(allocated_items_set.intersection(level))
            if len(hard_to_reach_all) >= minHardToReachPoolSize:
                break

        if len(hard_to_reach_all) < nHardToReach:
            return 'Not enough reachable items (%d) for hard to reach (%d)...?' % (len(hard_to_reach_all), nHardToReach)

        self.hard_to_reach_items = random.sample(hard_to_reach_all, nHardToReach)
        self.reachable = reachable
        self.unreachable = unreachable
        self.levels = levels

        return None


    def verify_warps_reachable(self):
        # verify that every major location has an unconstrained path to the goal.
        variables = self.data.generate_variables()
        allocation = self.allocation
        edges = allocation.edges

        dfs_stack = [location for location, loc_type in self.data.locations.items() if loc_type == LOCATION_WARP]
        visited = set(dfs_stack)

        while len(dfs_stack) > 0:
            current_dest = dfs_stack.pop()
            for edge_id in allocation.incoming_edges[current_dest]:
                target_src = edges[edge_id].from_location
                if target_src in visited: continue
                if edges[edge_id].satisfied(variables):
                    visited.add(target_src)
                    dfs_stack.append(target_src)

        major_locations = set(location for location, loc_type in self.data.locations.items() if loc_type == LOCATION_MAJOR)

        return (len(major_locations - visited) == 0, visited)


    def verify_reachable_items(self, backward_exitable):
        if self.visualize:
            from visualizer import Visualization
            vis = Visualization()
            vis.load_graph(self.data, self.allocation)

        data = self.data
        allocation = self.allocation

        # Should not be modified:
        edges = allocation.edges
        outgoing_edges = allocation.outgoing_edges
        incoming_edges = allocation.incoming_edges
        locations_set = data.locations_set

        # Persistent variables
        variables = data.generate_variables()
        untraversable_edges = set(edge.edge_id for edge in edges)
        unreached_pseudo_items = dict(data.pseudo_items)
        unsatisfied_item_conditions = dict(data.alternate_conditions)

        forward_enterable = set((START_LOCATION,))
        backward_exitable = set(backward_exitable)
        pending_exit_locations = set()
        locally_exitable_locations = {}

        levels = []

        # Temp Variables that are reset every time
        to_remove = []
        forward_frontier = set()
        backward_frontier = set()
        new_reachable_locations = set()
        newly_traversable_edges = set()
        temp_variable_storage = {}


        variables['IS_BACKTRACKING'] = False
        variables['BACKTRACK_DATA'] = untraversable_edges, outgoing_edges, edges
        variables['BACKTRACK_GOALS'] = None, None

        first_loop = True
        while True:
            new_reachable_locations.clear()
            if first_loop: new_reachable_locations = forward_enterable.intersection(backward_exitable)
            current_level_part1 = []
            current_level_part2 = []
            first_loop = False

            # STEP 0: Mark Pseudo-Items
            has_changes = True
            while has_changes:
                has_changes = False

                # 0 Part A: Handle pseudo-items
                to_remove.clear()
                for target, condition in unreached_pseudo_items.items():
                    if condition(variables):
                        current_level_part1.append(target)
                        to_remove.append(target)
                        has_changes = True

                for target in to_remove:
                    variables[target] = True
                    del unreached_pseudo_items[target]

                # 0 Part B: Handle alternate constraints for items
                to_remove.clear()
                for target, condition in unsatisfied_item_conditions.items():
                    if condition(variables):
                        if not variables[target]:
                            current_level_part1.append(target)
                            has_changes = True
                        to_remove.append(target)

                for target in to_remove:
                    variables[target] = True
                    del unsatisfied_item_conditions[target]


            # STEP 1: Loop Edge List
            forward_frontier.clear()
            backward_frontier.clear()
            newly_traversable_edges.clear()
            for edge_id in untraversable_edges:
                edge = edges[edge_id]
                if edge.satisfied(variables):
                    newly_traversable_edges.add(edge_id)
                    if edge.from_location in forward_enterable:
                        forward_frontier.add(edge.from_location)
                    if edge.to_location in backward_exitable:
                        backward_frontier.add(edge.to_location)
            untraversable_edges -= newly_traversable_edges

            # STEP 2: Find Forward Reachable Nodes
            new_forward_enterable = set()
            while len(forward_frontier) > 0:
                for node in forward_frontier:
                    for edge_id in outgoing_edges[node]:
                        if edge_id not in untraversable_edges:
                            target_location = edges[edge_id].to_location
                            if target_location not in forward_enterable:
                                new_forward_enterable.add(target_location)
                                forward_enterable.add(target_location)

                                if target_location in backward_exitable:
                                    new_reachable_locations.add(target_location)
                                else:
                                    pending_exit_locations.add(target_location)
                forward_frontier.clear()
                forward_frontier, new_forward_enterable = new_forward_enterable, forward_frontier


            # STEP 3: Find Exitable Nodes
            new_backward_exitable = set()
            while len(backward_frontier) > 0:
                for node in backward_frontier:
                    for edge_id in incoming_edges[node]:
                        if edge_id not in untraversable_edges:
                            target_location = edges[edge_id].from_location
                            if target_location not in backward_exitable:
                                new_backward_exitable.add(target_location)
                                backward_exitable.add(target_location)

                                if target_location in forward_enterable:
                                    new_reachable_locations.add(target_location)
                                    pending_exit_locations.remove(target_location)
                backward_frontier.clear()
                backward_frontier, new_backward_exitable = new_backward_exitable, backward_frontier


            # STEP 4: Mark New Reachable Locations
            for location in new_reachable_locations:
                if location in locations_set:
                    if not variables[location]:
                        current_level_part2.append(location)
                        #variables[location] = True
                for item_location in data.item_locations_in_node[location]:
                    item_name = allocation.item_at_item_location[item_location]
                    if item_name == None: continue
                    if not variables[item_name]:
                        current_level_part2.append(item_name)
                        #variables[item_name] = True

            new_reachable_locations.clear()


            # STEP 5: Handle Pending Exit Locations
            for base_location in pending_exit_locations:
                # Temporarily Mark Variables
                variables['IS_BACKTRACKING'] = True
                temp_variable_storage.clear()
                if base_location in locations_set:
                    temp_variable_storage[base_location] = variables[base_location]
                    variables[base_location] = True
                for item_location in data.item_locations_in_node[base_location]:
                    item_name = allocation.item_at_item_location[item_location]
                    if item_name == None: continue
                    temp_variable_storage[item_name] = variables[item_name]
                    variables[item_name] = True

                if base_location not in locally_exitable_locations:
                    locally_exitable_locations[base_location] = set((base_location,))
                locally_exitable = locally_exitable_locations[base_location]

                can_exit = False
                local_backward_frontier = set(locally_exitable)
                new_locally_backward_exitable = set()
                while len(local_backward_frontier) > 0 and not can_exit:
                    for node in local_backward_frontier:
                        if can_exit or node in backward_exitable:
                            can_exit = True
                            break
                        for edge_id in outgoing_edges[node]:
                            edge = edges[edge_id]
                            if edge.to_location in locally_exitable: continue
                            variables['BACKTRACK_GOALS'] = edge.to_location, base_location
                            if edge.edge_id not in untraversable_edges or edge.satisfied(variables):
                                locally_exitable.add(edge.to_location)
                                new_locally_backward_exitable.add(edge.to_location)
                    
                    local_backward_frontier.clear()
                    local_backward_frontier, new_locally_backward_exitable = new_locally_backward_exitable, local_backward_frontier

                # Restore Previous Variables Status
                for name, value in temp_variable_storage.items():
                    variables[name] = value
                temp_variable_storage.clear()
                variables['IS_BACKTRACKING'] = False
                variables['BACKTRACK_GOALS'] = None, None

                # If we can exit, set the corresponding variables to true.
                if can_exit:
                    if base_location in locations_set:
                        if not variables[base_location]:
                            current_level_part2.append(base_location)
                            variables[base_location] = True
                    for item_location in data.item_locations_in_node[base_location]:
                        item_name = allocation.item_at_item_location[item_location]
                        if item_name == None: continue
                        if not variables[item_name]:
                            current_level_part2.append(item_name)
                            variables[item_name] = True

            for node in current_level_part2:
                variables[node] = True

            if len(current_level_part1) == 0 and len(current_level_part2) == 0:
                break
            levels.append(current_level_part1)
            levels.append(current_level_part2)

        if self.visualize:
            for edge_id in untraversable_edges:
                edge = edges[edge_id]
                vis.set_edge_color(edge.from_location, edge.to_location, color=(191,32,32))
            for loc in forward_enterable.intersection(backward_exitable):
                vis.set_node_color(loc, (255,191,0))
            vis.render()

        reachable = sorted(name for name, value in variables.items() if value)
        unreachable = sorted(name for name, value in variables.items() if not value)

        #if self.visualize:
            #for en, level in enumerate(levels):
                #print('LEVEL %d' % en)
                #print(level)

        return reachable, unreachable, levels



