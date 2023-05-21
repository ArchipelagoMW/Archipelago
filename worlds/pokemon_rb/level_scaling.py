from BaseClasses import CollectionState, Location
from .locations import level_name_list, level_list

def level_scaling(multiworld):
    try:
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
        print([len([item for item in sphere if item.type == "Item"]) for sphere in spheres])
        for world in multiworld.get_game_worlds("Pokemon Red and Blue"):
            level_list_copy = level_list.copy()
            for sphere in spheres:
                sphere_objects = {loc.name: loc for loc in sphere if loc.player == world.player and loc.type == "Wild Encounter" and
                                  loc.level is not None}
                party_objects = [loc for loc in sphere if loc.player == world.player and loc.type == "Trainer Parties"]
                for parties in party_objects:
                    for party in parties.party_data:
                        if isinstance(party["level"], int):
                            sphere_objects[(party["party_address"], 0)] = parties
                        else:
                            for i, level in enumerate(party["level"]):
                                sphere_objects[(party["party_address"], i)] = parties
                ordered_sphere_objects = list(sphere_objects.keys())
                ordered_sphere_objects.sort(key=lambda obj: level_name_list.index(obj))
                for object in ordered_sphere_objects:
                    if sphere_objects[object].type == "Wild Encounter":
                        sphere_objects[object].level = level_list_copy.pop(0)
                    else:
                        for party in sphere_objects[object].party_data:
                            if party["party_address"] == object[0]:
                                if isinstance(party["level"], int):
                                    party["level"] = level_list_copy.pop(0)
                                else:
                                    party["level"][object[1]] = level_list_copy.pop(0)
                                break
                        else:
                            breakpoint()
    except Exception as e:
        breakpoint()

    world.finished_level_scaling.set()
