from BaseClasses import CollectionState
from .locations import wild_name_list, wild_level_list

def level_scaling(multiworld):
    state = CollectionState(multiworld)
    locations = set(multiworld.get_filled_locations())
    spheres = []

    while locations:
        sphere = set()

        for location in locations:
            # We want areas that areaccessible earlier to have lower levels. If an important item is at a fossil
            # location but you require fossil items for the second, they may not be in logic until much later, despite
            # your ability to potentially reach them earlier. We treat them both as reachable right away for this
            # purpose
            if location.can_reach(state) or (location.parent_region.name == "Fossil" and
                                             state.can_reach("Mt Moon B2F", "Region", location.player)):
                sphere.add(location)

        if sphere:
            spheres.append(sphere)
            locations -= sphere
        else:
            spheres.append(locations)
            break

        for location in sphere:
            state.collect(location.item, True, location)

    for world in multiworld.get_game_worlds("Pokemon Red and Blue"):
        level_list_copy = wild_level_list.copy()
        for sphere in spheres:
            sphere_mons = [loc for loc in sphere if loc.player == world.player and loc.type == "Wild Encounter" and
                           loc.level is not None]
            sphere_mons.sort(key=lambda loc: wild_name_list.index(loc.name))
            for location in sphere_mons:
                location.level = level_list_copy.pop(0)
        world.finished_level_scaling.set()
