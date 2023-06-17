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
                def reachable():
                    if location.can_reach(state):
                        return True
                    if location.parent_region.name == "Fossil" and state.can_reach("Mt Moon B2F", "Region",
                                                                                   location.player):
                        # We want areas that are accessible earlier to have lower levels. If an important item is at a
                        # fossil location, it may not be in logic until much later, despite your ability to potentially
                        # reach them earlier. We treat them both as reachable right away for this purpose
                        return True
                    if (location.name == "Route 25 - Item" and state.can_reach("Route 25", "Region", location.player)
                            and multiworld.blind_trainers[location.player].value < 100):
                        # Assume they will take their one chance to get the trainer to walk out of the way to reach
                        # the item behind them
                        return True
                    return False
                if reachable():
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
                if not location.item:
                    continue
                if (location.item.game == "Pokemon Red and Blue" and (location.item.name.startswith("Missable ") or
                        location.item.name.startswith("Static ")) and location.name !=
                        "Pokemon Tower 6F - Restless Soul"):
                    # Normally, missable Pokemon (starters, the dojo rewards) are not considered in logic static Pokemon
                    # are not considered for moves or evolutions, as you could release them and potentially soft lock
                    # the game. However, for level scaling purposes, we will treat them as not missable or static.
                    # We would not want someone playing a minimal accessibility Dexsanity game to get what would be
                    # technically an "out of logic" Mansion Key from selecting Bulbasaur at the beginning of the game
                    # and end up in the Mansion early and encountering level 67 Pokémon
                    state.collect(multiworld.worlds[location.item.player].create_item(
                        location.item.name.split("Missable ")[-1].split("Static ")[-1]), True, location)
                else:
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
        for world in multiworld.get_game_worlds("Pokemon Red and Blue"):
            world.finished_level_scaling.set()

            print([len([item for item in sphere if item.player == world.player and item.type == "Item"]) for sphere in multiworld.get_spheres()])


    except Exception as err:
        breakpoint()
