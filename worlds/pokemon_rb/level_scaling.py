from BaseClasses import CollectionState, Location
from .locations import level_name_list, level_list


def level_scaling(multiworld):
    try:
        state = CollectionState(multiworld)
        locations = set(multiworld.get_filled_locations())
        spheres = []

        while locations:
            sphere = set()
            for world in multiworld.get_game_worlds("Pokemon Red and Blue"):
                if multiworld.level_scaling[world.player] != "by_spheres_and_distance":
                    continue
                regions = {multiworld.get_region("Menu", world.player)}
                checked_regions = set()
                distance = 0
                while regions:
                    next_regions = set()
                    for region in regions:
                        if not getattr(region, "distance"):
                            region.distance = distance
                        next_regions.update({e.connected_region for e in region.exits if e.connected_region not in
                                             checked_regions and e.access_rule(state)})
                    checked_regions.update(regions)
                    regions = next_regions
                    distance += 1

            distances = {}

            for location in locations:
                # We want areas that are accessible earlier to have lower levels. If an important item is at a fossil
                # location, but you require fossil items for the second, they may not be in logic until much later,
                # despite your ability to potentially reach them earlier. We treat them both as reachable right away for
                # this purpose
                if location.can_reach(state) or (location.parent_region.name == "Fossil" and
                                                 state.can_reach("Mt Moon B2F", "Region", location.player)):
                    sphere.add(location)
                    parent_region = location.parent_region
                    if parent_region.name == "Fossil":
                        parent_region = multiworld.get_region("Mt Moon B2F", location.player)
                    if getattr(parent_region, "distance", None) is None:
                        distance = 0
                    else:
                        distance = parent_region.distance
                    if distance not in distances:
                        distances[distance] = {location}
                    else:
                        distances[distance].add(location)

            if sphere:
                for distance in sorted(distances.keys()):
                    spheres.append(distances[distance])
                # spheres.append(sphere)
                    locations -= distances[distance]
            else:
                spheres.append(locations)
                break

            for location in sphere:
                state.collect(location.item, True, location)
        #print([len([item for item in sphere if item.type == "Item"]) for sphere in spheres])
        for world in multiworld.get_game_worlds("Pokemon Red and Blue"):
            if multiworld.level_scaling[world.player] == "off":
                continue
            level_list_copy = level_list.copy()
            for sphere in spheres:
                sphere_objects = {loc.name: loc for loc in sphere if loc.player == world.player
                                  and (loc.type == "Wild Encounter" or "Pokemon" in loc.type) and loc.level is not None}
                party_objects = [loc for loc in sphere if loc.player == world.player and loc.type == "Trainer Parties"]
                for parties in party_objects:
                    for party in parties.party_data:
                        if isinstance(party["level"], int):
                            sphere_objects[(party["party_address"][0] if isinstance(party["party_address"], list)
                                           else party["party_address"], 0)] = parties
                        else:
                            for i, level in enumerate(party["level"]):
                                sphere_objects[(party["party_address"][0] if isinstance(party["party_address"], list)
                                                else party["party_address"], i)] = parties
                ordered_sphere_objects = list(sphere_objects.keys())
                ordered_sphere_objects.sort(key=lambda obj: level_name_list.index(obj))
                for object in ordered_sphere_objects:
                    if sphere_objects[object].type == "Trainer Parties":
                        for party in sphere_objects[object].party_data:
                            if (isinstance(party["party_address"], list) and party["party_address"][0] == object[0]) or party["party_address"] == object[0]:
                                if isinstance(party["level"], int):
                                    party["level"] = level_list_copy.pop(0)
                                    #print(f"{party['party_address']} - {party['level']}")
                                else:
                                    party["level"][object[1]] = level_list_copy.pop(0)
                                    #print(f"{party['party_address']} - {party['level'][object[1]]}")
                                break
                    else:
                        sphere_objects[object].level = level_list_copy.pop(0)
                        #print(f"{sphere_objects[object]} - {sphere_objects[object].level}")
            world.finished_level_scaling.set()

            print([len([item for item in sphere if item.player == world.player and item.type == "Item"]) for sphere in multiworld.get_spheres()])


    except Exception as e:
        breakpoint()
