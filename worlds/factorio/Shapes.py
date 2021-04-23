from typing import Dict, List, Set

from BaseClasses import MultiWorld
from Options import TechTreeLayout
from worlds.factorio.Technologies import technology_table

def get_shapes(world: MultiWorld, player: int) -> Dict[str, List[str]]:
    prerequisites: Dict[str, Set[str]] = {}
    layout = world.tech_tree_layout[player].value
    custom_technologies = world.custom_data[player]["custom_technologies"]
    if layout == TechTreeLayout.option_small_diamonds:
        slice_size = 4
        tech_names: List[str] = list(set(custom_technologies) - world._static_nodes)
        tech_names.sort()
        world.random.shuffle(tech_names)
        while len(tech_names) > slice_size:
            slice = tech_names[:slice_size]
            tech_names = tech_names[slice_size:]
            slice.sort(key=lambda tech_name: len(custom_technologies[tech_name].ingredients))
            diamond_0, diamond_1, diamond_2, diamond_3 = slice

            #   0    |
            # 1   2  |
            #   3    V
            prerequisites[diamond_3] = {diamond_1, diamond_2}
            prerequisites[diamond_2] = prerequisites[diamond_1] = {diamond_0}
    elif layout == TechTreeLayout.option_medium_diamonds:
        slice_size = 9
        tech_names: List[str] = list(set(custom_technologies) - world._static_nodes)
        tech_names.sort()
        world.random.shuffle(tech_names)
        while len(tech_names) > slice_size:
            slice = tech_names[:slice_size]
            tech_names = tech_names[slice_size:]
            slice.sort(key=lambda tech_name: len(custom_technologies[tech_name].ingredients))

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

    elif layout == TechTreeLayout.option_pyramid:
        slice_size = 1
        tech_names: List[str] = list(set(custom_technologies) - world._static_nodes)
        tech_names.sort()
        world.random.shuffle(tech_names)
        tech_names.sort(key=lambda tech_name: len(custom_technologies[tech_name].ingredients))
        previous_slice = []
        while len(tech_names) > slice_size:
            slice = tech_names[:slice_size]
            world.random.shuffle(slice)
            tech_names = tech_names[slice_size:]
            for i, tech_name in enumerate(previous_slice):
                prerequisites.setdefault(slice[i], set()).add(tech_name)
                prerequisites.setdefault(slice[i + 1], set()).add(tech_name)
            previous_slice = slice
            slice_size += 1

    elif layout == TechTreeLayout.option_funnel:


        tech_names: List[str] = list(set(custom_technologies) - world._static_nodes)
        # find largest inverse pyramid
        # https://www.wolframalpha.com/input/?i=x+=+1/2+(n++++1)+(2++++n)+solve+for+n
        import math
        slice_size = int(0.5*(math.sqrt(8*len(tech_names)+1)-3))
        tech_names.sort()
        world.random.shuffle(tech_names)
        tech_names.sort(key=lambda tech_name: len(custom_technologies[tech_name].ingredients))
        previous_slice = []
        while slice_size:
            slice = tech_names[:slice_size]
            world.random.shuffle(slice)
            tech_names = tech_names[slice_size:]
            if previous_slice:
                for i, tech_name in enumerate(slice):
                    prerequisites.setdefault(tech_name, set()).update(previous_slice[i:i+2])
            previous_slice = slice
            slice_size -= 1

    world.tech_tree_layout_prerequisites[player] = prerequisites
    return prerequisites
