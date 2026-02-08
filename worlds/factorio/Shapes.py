from typing import Dict, List, Set, TYPE_CHECKING
from collections import deque

from .Options import TechTreeLayout

if TYPE_CHECKING:
    from . import Factorio, FactorioScienceLocation

funnel_layers = {TechTreeLayout.option_small_funnels: 3,
                 TechTreeLayout.option_medium_funnels: 4,
                 TechTreeLayout.option_large_funnels: 5}

funnel_slice_sizes = {TechTreeLayout.option_small_funnels: 6,
                      TechTreeLayout.option_medium_funnels: 10,
                      TechTreeLayout.option_large_funnels: 15}


def _sorter(location: "FactorioScienceLocation"):
    return location.complexity, location.rel_cost


def get_shapes(world: "Factorio") -> Dict["FactorioScienceLocation", Set["FactorioScienceLocation"]]:
    prerequisites: Dict["FactorioScienceLocation", Set["FactorioScienceLocation"]] = {}
    layout = world.options.tech_tree_layout.value
    locations: List["FactorioScienceLocation"] = sorted(world.science_locations, key=lambda loc: loc.name)
    world.random.shuffle(locations)

    if layout == TechTreeLayout.option_single:
        pass
    elif layout == TechTreeLayout.option_small_diamonds:
        slice_size = 4
        while len(locations) > slice_size:
            slice = locations[:slice_size]
            locations = locations[slice_size:]
            slice.sort(key=_sorter)
            diamond_0, diamond_1, diamond_2, diamond_3 = slice

            #   0    |
            # 1   2  |
            #   3    V
            prerequisites[diamond_3] = {diamond_1, diamond_2}
            prerequisites[diamond_2] = prerequisites[diamond_1] = {diamond_0}

    elif layout == TechTreeLayout.option_medium_diamonds:
        slice_size = 9
        while len(locations) > slice_size:
            slice = locations[:slice_size]
            locations = locations[slice_size:]
            slice.sort(key=_sorter)

            #     0     |
            #   1   2   |
            # 3   4   5 |
            #   6   7   |
            #     8     V

            prerequisites[slice[1]] = {slice[0]}
            prerequisites[slice[2]] = {slice[0]}

            prerequisites[slice[3]] = {slice[1]}
            prerequisites[slice[4]] = {slice[1], slice[2]}
            prerequisites[slice[5]] = {slice[2]}

            prerequisites[slice[6]] = {slice[3], slice[4]}
            prerequisites[slice[7]] = {slice[4], slice[5]}

            prerequisites[slice[8]] = {slice[6], slice[7]}

    elif layout == TechTreeLayout.option_large_diamonds:
        slice_size = 16
        while len(locations) > slice_size:
            slice = locations[:slice_size]
            locations = locations[slice_size:]
            slice.sort(key=_sorter)

            #       0       |
            #     1   2     |
            #   3   4   5   |
            # 6   7   8   9 |
            #   10  11  12  |
            #     13  14    |
            #       15      |

            prerequisites[slice[1]] = {slice[0]}
            prerequisites[slice[2]] = {slice[0]}

            prerequisites[slice[3]] = {slice[1]}
            prerequisites[slice[4]] = {slice[1], slice[2]}
            prerequisites[slice[5]] = {slice[2]}

            prerequisites[slice[6]] = {slice[3]}
            prerequisites[slice[7]] = {slice[3], slice[4]}
            prerequisites[slice[8]] = {slice[4], slice[5]}
            prerequisites[slice[9]] = {slice[5]}

            prerequisites[slice[10]] = {slice[6], slice[7]}
            prerequisites[slice[11]] = {slice[7], slice[8]}
            prerequisites[slice[12]] = {slice[8], slice[9]}

            prerequisites[slice[13]] = {slice[10], slice[11]}
            prerequisites[slice[14]] = {slice[11], slice[12]}

            prerequisites[slice[15]] = {slice[13], slice[14]}

    elif layout == TechTreeLayout.option_small_pyramids:
        slice_size = 6
        while len(locations) > slice_size:
            slice = locations[:slice_size]
            locations = locations[slice_size:]
            slice.sort(key=_sorter)

            #        0       |
            #      1   2     |
            #    3   4   5   |

            prerequisites[slice[1]] = {slice[0]}
            prerequisites[slice[2]] = {slice[0]}

            prerequisites[slice[3]] = {slice[1]}
            prerequisites[slice[4]] = {slice[1], slice[2]}
            prerequisites[slice[5]] = {slice[2]}

    elif layout == TechTreeLayout.option_medium_pyramids:
        slice_size = 10
        while len(locations) > slice_size:
            slice = locations[:slice_size]
            locations = locations[slice_size:]
            slice.sort(key=_sorter)

            #        0       |
            #      1   2     |
            #    3   4   5   |
            #  6   7   8   9 |


            prerequisites[slice[1]] = {slice[0]}
            prerequisites[slice[2]] = {slice[0]}

            prerequisites[slice[3]] = {slice[1]}
            prerequisites[slice[4]] = {slice[1], slice[2]}
            prerequisites[slice[5]] = {slice[2]}

            prerequisites[slice[6]] = {slice[3]}
            prerequisites[slice[7]] = {slice[3], slice[4]}
            prerequisites[slice[8]] = {slice[4], slice[5]}
            prerequisites[slice[9]] = {slice[5]}

    elif layout == TechTreeLayout.option_large_pyramids:
        slice_size = 15
        while len(locations) > slice_size:
            slice = locations[:slice_size]
            locations = locations[slice_size:]
            slice.sort(key=_sorter)

            #         0          |
            #       1   2        |
            #     3   4   5      |
            #   6   7   8   9    |
            # 10  11  12  13  14 |


            prerequisites[slice[1]] = {slice[0]}
            prerequisites[slice[2]] = {slice[0]}

            prerequisites[slice[3]] = {slice[1]}
            prerequisites[slice[4]] = {slice[1], slice[2]}
            prerequisites[slice[5]] = {slice[2]}

            prerequisites[slice[6]] = {slice[3]}
            prerequisites[slice[7]] = {slice[3], slice[4]}
            prerequisites[slice[8]] = {slice[4], slice[5]}
            prerequisites[slice[9]] = {slice[5]}

            prerequisites[slice[10]] = {slice[6]}
            prerequisites[slice[11]] = {slice[6], slice[7]}
            prerequisites[slice[12]] = {slice[7], slice[8]}
            prerequisites[slice[13]] = {slice[8], slice[9]}
            prerequisites[slice[14]] = {slice[9]}

    elif layout in funnel_layers:
        slice_size = funnel_slice_sizes[layout]
        world.random.shuffle(locations)

        while len(locations) > slice_size:
            locations = locations[slice_size:]
            current_locations = locations[:slice_size]
            layer_size = funnel_layers[layout]
            previous_slice = []
            current_locations.sort(key=_sorter)
            for layer in range(funnel_layers[layout]):
                slice = current_locations[:layer_size]
                current_locations = current_locations[layer_size:]
                if previous_slice:
                    for i, tech_name in enumerate(slice):
                        prerequisites.setdefault(tech_name, set()).update(previous_slice[i:i+2])
                previous_slice = slice
                layer_size -= 1
    elif layout == TechTreeLayout.option_trees:
        #              0              |
        #            1   2            |
        #              3              |
        #        4   5   6   7        |
        #              8              |
        #  9   10   11   12   13  14  |
        #              15             |
        #              16             |
        slice_size = 17
        while len(locations) > slice_size:
            slice = locations[:slice_size]
            locations = locations[slice_size:]
            slice.sort(key=_sorter)

            prerequisites[slice[1]] = {slice[0]}
            prerequisites[slice[2]] = {slice[0]}

            prerequisites[slice[3]] = {slice[1], slice[2]}

            prerequisites[slice[4]] = {slice[3]}
            prerequisites[slice[5]] = {slice[3]}
            prerequisites[slice[6]] = {slice[3]}
            prerequisites[slice[7]] = {slice[3]}

            prerequisites[slice[8]] = {slice[4], slice[5], slice[6], slice[7]}

            prerequisites[slice[9]] = {slice[8]}
            prerequisites[slice[10]] = {slice[8]}
            prerequisites[slice[11]] = {slice[8]}
            prerequisites[slice[12]] = {slice[8]}
            prerequisites[slice[13]] = {slice[8]}
            prerequisites[slice[14]] = {slice[8]}

            prerequisites[slice[15]] = {slice[9], slice[10], slice[11], slice[12], slice[13], slice[14]}
            prerequisites[slice[16]] = {slice[15]}
    elif layout == TechTreeLayout.option_choices:
        locations.sort(key=_sorter)
        current_choices = deque([locations[0]])
        locations = locations[1:]
        while len(locations) > 1:
            source = current_choices.pop()
            choices = locations[:2]
            locations = locations[2:]
            for choice in choices:
                prerequisites[choice] = {source}
            current_choices.extendleft(choices)
    elif layout == TechTreeLayout.option_irregular:
        
        #Made by: CosmicWolf @brattycosmicwolf
        #I am going by `sort(key=_sorter)` and then branching the tech tree out. So no issues should arrise AFAIK with getting things stuck.
        #This is the same method also used by the other tech tree methods.

        minimum_dependencies = 1 #these can be propper options and/or settings.
        maximum_dependencies = 5 + 1 #The +1 is to ensure all values are equally likely.    Long explanation; if I want a number [1,5] and I only rolled a float with [1,10] and then round. The 1 would only be rolled if the roll is [1, 1.5>. Which is only half a number compared to the random range of 2; [1.5, 2,5>. Technically it is possible that because of rounding errors the highest value becomes this max+1. Chances of this happening are so low I am going to leave it as an easter egg.
        even_distribution = False #these can be propper options and/or settings. Can/should be combined with the one below.
        weighted_distribution = 1 #these can be propper options and/or settings.
        starting_techs = 5 #setting to pick amount of techs this tree starts with.

        all_pre: Dict["FactorioScienceLocation", Set["FactorioScienceLocation"]] = {} #will be used to keep track of ALL previous dependencies. In order to ensure that A->B->C will not also get A->C. Since A is already required by B. Also the other way around A leading to both B and C and then preventing C from also getting B.
        
        locations.sort(key=_sorter, reverse=True)
        already_done = locations[-starting_techs:] # remove the first techs from my actions
        locations = locations[:-starting_techs]
        while locations: #Loop through all remaining techs
            victim = locations.pop()
            prerequisites[victim] = set()
            all_pre[victim] = set()
            current_choices = already_done.copy()
            rand_num = 0
            if even_distribution:
                rand_num = int( world.random.uniform(minimum_dependencies, maximum_dependencies))
            else:
                rand_num = int( world.random.triangular(minimum_dependencies, maximum_dependencies, weighted_distribution))

            while rand_num >=1 and len(current_choices) > 0:
                rand_num -= 1
                dependency = current_choices[world.random.randint(0, len(current_choices)-1)] #pick one of the already established techs.
                prerequisites[victim].add(dependency) #Take one of the already processed techs as its prerequisite.

                all_pre[victim].add(dependency)
                all_pre[victim].add(item for item in all_pre[victim])

                current_choices.remove(dependency)
                for item in current_choices:
                    if item in all_pre[victim]: #remove choices if it already in the victims tree: A -> dependency -> Victim remove A from choices.
                        current_choices.remove(item)
                    elif item in all_pre and dependency in all_pre[item]: #remove a choice if the victim already has a pre of a dependency. dependency -> A and dependency -> victim. Remove A from the list of choices. 
                        current_choices.remove(item)

            already_done.append(victim)
        del all_pre
    else:
        raise NotImplementedError(f"Layout {layout} is not implemented.")

    world.tech_tree_layout_prerequisites = prerequisites
    return prerequisites
