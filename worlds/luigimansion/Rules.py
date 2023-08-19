from BaseClasses import Location, MultiWorld
from worlds.generic.Rules import add_rule


# Assign ghost_type to region list, access that attribute to set rules during connect function
def set_ghost_type(multiworld: MultiWorld, ghost_list: dict):
    for region_name in ghost_list:
        ghost_type = multiworld.random.choice(["Fire", "Water", "Ice", "No Element"])
        ghost_list.update({region_name: ghost_type})
