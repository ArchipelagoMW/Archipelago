from BaseClasses import Location, MultiWorld
from worlds.generic.Rules import set_rule


# Assign ghost_type to region list, access that attribute to set rules using function below
def set_ghost_type(multiworld: MultiWorld, ghost_list: dict) -> dict:
    ghost_type = multiworld.random.choice(["Fire", "Water", "Ice", "No Element"])

    for region_name in ghost_list:
        ghost_list.update({region_name: ghost_type})


def set_ghost_rules(multiworld: MultiWorld, player: int, locations: [Location]):
    for location in locations:
        for location_name in ghost_affected_locations:
            if location_name == location.name:
                ghost_state = set_ghost_type(multiworld, player)
                if ghost_state:
                    set_rule(location, ghost_state)
