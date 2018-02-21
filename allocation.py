import random
from utility import GraphEdge, is_egg

NO_CONDITIONS = lambda v : True
INFTY = 99999

class Allocation(object):
    # Attributes:
    # 
    # list: items_to_allocate
    #
    # dict: item_at_item_location  (item location -> item at item location)
    #
    # dict: outgoing_edges  [location -> list(Edge)]
    # dict: incoming_edges  [location -> list(Edge)]
    # list: edges  [list(Edge)]   <-- indexed by edge_id
    #
    # list: walking_left_transitions  (MapTransition objects)

    def __init__(self, data, settings):
        self.items_to_allocate = list(data.items_to_allocate)
        self.walking_left_transitions = list(data.walking_left_transitions)


    def shuffle(self, data, settings):
        # Shuffle Items
        self.allocate_items(data, settings)

        # Shuffle Locations
        self.construct_graph(data, settings)


    def allocate_items(self, data, settings):
        item_slots = data.item_slots

        #if not settings.shuffle_items:
            #self.item_at_item_location = dict(zip(item_slots, item_slots))
            #return

        random.shuffle(self.items_to_allocate)

        # A map of location -> item at location
        self.item_at_item_location = dict(zip(item_slots, self.items_to_allocate))
        self.item_at_item_location.update(data.unshuffled_allocations)

        # DEBUG CODE FOR FINDING ITEMS
        #print('\n')
        #for k,v in self.item_at_item_location.items():
            #if v in ('PIKO_HAMMER','WALL_JUMP','RABI_SLIPPERS','AIR_JUMP','AIR_DASH','BUNNY_WHIRL','HAMMER_ROLL','SLIDING_POWDER','CARROT_BOMB','CARROT_SHOOTER','FIRE_ORB','WATER_ORB',):
                #print('%s @ %s' % (v, k))


    def construct_graph(self, data, settings):
        edges = list(data.initial_edges)
        originalNEdges = len(edges)
        outgoing_edges = dict((key, list(edge_ids)) for key, edge_ids in data.initial_outgoing_edges.items())
        incoming_edges = dict((key, list(edge_ids)) for key, edge_ids in data.initial_incoming_edges.items())

        # Constraints
        for constraint in data.edge_constraints:
            edges.append(GraphEdge(
                edge_id=len(edges),
                from_location=constraint.from_location,
                to_location=constraint.to_location,
                constraint=constraint.prereq_lambda,
                backtrack_cost=1,
            ))

        # Map Transitions
        if settings.shuffle_map_transitions:
            random.shuffle(self.walking_left_transitions)

        for rtr, ltr in zip(data.walking_right_transitions, self.walking_left_transitions):
            edge1 = GraphEdge(
                edge_id=len(edges),
                from_location=rtr.origin_location,
                to_location=ltr.origin_location,
                constraint=NO_CONDITIONS,
                backtrack_cost=INFTY,
            )
            edge2 = GraphEdge(
                edge_id=len(edges)+1,
                from_location=ltr.origin_location,
                to_location=rtr.origin_location,
                constraint=NO_CONDITIONS,
                backtrack_cost=INFTY,
            )
            edges.append(edge1)
            edges.append(edge2)

        for edge in edges[originalNEdges:]:
            outgoing_edges[edge.from_location].append(edge.edge_id)
            incoming_edges[edge.to_location].append(edge.edge_id)


        self.edges = edges
        self.outgoing_edges = outgoing_edges
        self.incoming_edges = incoming_edges


    def shift_eggs_to_hard_to_reach(self, data, settings, reachable_items, hard_to_reach_items):
        reachable_items = set(reachable_items)

        hard_to_reach_pairs = [(item_location, item_name)
                        for item_location, item_name in self.item_at_item_location.items()
                        if item_name in hard_to_reach_items]

        hard_to_reach_eggs = [(item_location, item_name) for item_location, item_name in hard_to_reach_pairs
                        if is_egg(item_name)]
        hard_to_reach_non_eggs = [(item_location, item_name) for item_location, item_name in hard_to_reach_pairs
                        if not is_egg(item_name)]

        non_hard_to_reach_eggs = [(item_location, item_name)
                        for item_location, item_name in self.item_at_item_location.items()
                        if is_egg(item_name) and item_name not in hard_to_reach_items and item_name in reachable_items]

        hard_to_reach_eggs.sort(key=lambda p:p[0])
        hard_to_reach_non_eggs.sort(key=lambda p:p[0])
        non_hard_to_reach_eggs.sort(key=lambda p:p[0])

        n_eggs_in_map = data.nHardToReach + settings.extra_eggs
        if len(non_hard_to_reach_eggs) + len(hard_to_reach_eggs) < n_eggs_in_map:
            # Not enough reachable eggs. Retry.
            return False
        remainingEggsToPlace = random.sample(non_hard_to_reach_eggs, n_eggs_in_map - len(hard_to_reach_eggs))
        random.shuffle(remainingEggsToPlace)

        extra_eggs = remainingEggsToPlace[:settings.extra_eggs]
        eggs_to_move = remainingEggsToPlace[settings.extra_eggs:]
        assert len(eggs_to_move) == len(hard_to_reach_non_eggs)

        for item_location, item_name in self.item_at_item_location.items():
            if is_egg(item_name):
                self.item_at_item_location[item_location] = None

        for item_location, item_name in hard_to_reach_eggs:
            self.item_at_item_location[item_location] = item_name

        for item_location, item_name in extra_eggs:
            self.item_at_item_location[item_location] = item_name

        for z1, z2 in zip(hard_to_reach_non_eggs, eggs_to_move):
            # Swap
            item_location_1, item_name_1 = z1
            item_location_2, item_name_2 = z2
            self.item_at_item_location[item_location_1] = item_name_2
            self.item_at_item_location[item_location_2] = item_name_1
        
        # Verification
        actual_n_eggs = sum(1 for item_location, item_name in self.item_at_item_location.items() if is_egg(item_name))
        assert n_eggs_in_map == actual_n_eggs

        return True




