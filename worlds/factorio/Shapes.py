from typing import Dict, List, Set
from collections import deque

from .Options import TechTreeLayout

funnel_layers = {TechTreeLayout.option_small_funnels: 3,
                 TechTreeLayout.option_medium_funnels: 4,
                 TechTreeLayout.option_large_funnels: 5}

funnel_slice_sizes = {TechTreeLayout.option_small_funnels: 6,
                      TechTreeLayout.option_medium_funnels: 10,
                      TechTreeLayout.option_large_funnels: 15}


def get_shapes(factorio_world) -> Dict[str, List[str]]:
    world = factorio_world.world
    player = factorio_world.player
    prerequisites: Dict[str, Set[str]] = {}
    layout = world.tech_tree_layout[player].value
    custom_technologies = factorio_world.custom_technologies
    tech_names: List[str] = list(set(custom_technologies) - world.worlds[player].static_nodes)
    tech_names.sort()
    world.random.shuffle(tech_names)

    if layout == TechTreeLayout.option_single:
        pass
    elif layout == TechTreeLayout.option_small_diamonds:
        slice_size = 4
        while len(tech_names) > slice_size:
            slice = tech_names[:slice_size]
            tech_names = tech_names[slice_size:]
            slice.sort(key=lambda tech_name: len(custom_technologies[tech_name].get_prior_technologies()))
            diamond_0, diamond_1, diamond_2, diamond_3 = slice

            #   0    |
            # 1   2  |
            #   3    V
            prerequisites[diamond_3] = {diamond_1, diamond_2}
            prerequisites[diamond_2] = prerequisites[diamond_1] = {diamond_0}

    elif layout == TechTreeLayout.option_medium_diamonds:
        slice_size = 9
        while len(tech_names) > slice_size:
            slice = tech_names[:slice_size]
            tech_names = tech_names[slice_size:]
            slice.sort(key=lambda tech_name: len(custom_technologies[tech_name].get_prior_technologies()))

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
        while len(tech_names) > slice_size:
            slice = tech_names[:slice_size]
            tech_names = tech_names[slice_size:]
            slice.sort(key=lambda tech_name: len(custom_technologies[tech_name].get_prior_technologies()))

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
        while len(tech_names) > slice_size:
            slice = tech_names[:slice_size]
            tech_names = tech_names[slice_size:]
            slice.sort(key=lambda tech_name: len(custom_technologies[tech_name].get_prior_technologies()))

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
        while len(tech_names) > slice_size:
            slice = tech_names[:slice_size]
            tech_names = tech_names[slice_size:]
            slice.sort(key=lambda tech_name: len(custom_technologies[tech_name].get_prior_technologies()))

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
        while len(tech_names) > slice_size:
            slice = tech_names[:slice_size]
            tech_names = tech_names[slice_size:]
            slice.sort(key=lambda tech_name: len(custom_technologies[tech_name].get_prior_technologies()))

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
        world.random.shuffle(tech_names)

        while len(tech_names) > slice_size:
            tech_names = tech_names[slice_size:]
            current_tech_names = tech_names[:slice_size]
            layer_size = funnel_layers[layout]
            previous_slice = []
            current_tech_names.sort(key=lambda tech_name: len(custom_technologies[tech_name].get_prior_technologies()))
            for layer in range(funnel_layers[layout]):
                slice = current_tech_names[:layer_size]
                current_tech_names = current_tech_names[layer_size:]
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
        while len(tech_names) > slice_size:
            slice = tech_names[:slice_size]
            tech_names = tech_names[slice_size:]
            slice.sort(key=lambda tech_name: len(custom_technologies[tech_name].get_prior_technologies()))

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
        tech_names.sort(key=lambda tech_name: len(custom_technologies[tech_name].get_prior_technologies()))
        current_choices = deque([tech_names[0]])
        tech_names = tech_names[1:]
        while len(tech_names) > 1:
            source = current_choices.pop()
            choices = tech_names[:2]
            tech_names = tech_names[2:]
            for choice in choices:
                prerequisites[choice] = {source}
            current_choices.extendleft(choices)
    else:
        raise NotImplementedError(f"Layout {layout} is not implemented.")

    world.tech_tree_layout_prerequisites[player] = prerequisites
    return prerequisites
