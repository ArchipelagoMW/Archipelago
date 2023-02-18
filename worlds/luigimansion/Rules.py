from BaseClasses import Location, MultiWorld
from worlds.generic.Rules import set_rule, CollectionRule
from .Locations import ghost_affected_locations

#Assign ghost_type to region subcless statically, access that attribute to set rules using function below
def set_ghost_type(multiworld: MultiWorld, player: int, location: Location, region: LMRegion) -> CollectionRule:
    if multiworld.Enemizer == True:
        result = multiworld.random.choice(["Fire", "Water", "Ice", "No Element"])
        room_to_ghost_table.update{location.name: result}

    for location_name, ghost_type in room_to_ghost_table:
        if ghost_type == "Fire":
            room_to_ghost_table.update{location.name: "Fire"}
            return lambda state: state.has("Water Element Medal", player)
        elif ghost_type == "Water":
            room_to_ghost_table.update{location.name: "Water"}
            return lambda state: state.has("Ice Element Medal", player)
        elif ghost_type == "Ice":
            room_to_ghost_table.update{location.name: "Ice"}
            return lambda state: state.has("Fire Element Medal", player)
        else:
            room_to_ghost_table.update{location.name: "No Element"}
            return lambda state: False


def set_ghost_rules(multiworld: MultiWorld, player: int, locations: [Location]):
    for location in locations:
        for location_name in ghost_affected_locations:
            if location_name == location.name:
                ghost_state = set_ghost_type(multiworld, player)
                if ghost_state:
                    set_rule(location, ghost_state)
