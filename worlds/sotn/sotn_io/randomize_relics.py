import math, re, random, copy
import relics, constants, extension, util

from errors import SoftLock, PickLock


# TODO BIG ISSUE python sets are unordered while js keep insertion order


def locks_from_locations(locations: dict) -> dict:
    return {key: [iv for iv in value if iv[0] != '+'] for key, value in {key: value for key, value in
                                                                         locations.items() if key not in
                                                                         ["extension", "leakPrevention",
                                                                          "thrustSwordAbility", "placed",
                                                                          "replaced", "blocked"]}.items()}


def escapes_from_locations(locations: dict) -> dict:
    return {key: [iv[1:] for iv in value if iv[0] == '+'] for key, value in {key: value for key, value in
                                                                             locations.items() if key not in
                                                                             ["extension", "leakPrevention",
                                                                              "thrustSwordAbility", "placed",
                                                                              "replaced", "blocked"]}.items()}


def rand_idx(rng, array: list) -> int:
    return random.randint(0, math.floor(len(array)) - 1)  # floor is only need it when using rng


# Helper function to take a list of locks and replace all instances of a single ability with new locks
def replace_locks(locks: list, ability_to_replace: str, locks_to_add: list) -> list:
    new_locks = []
    for lock in locks:
        if ability_to_replace not in lock:
            # Any locks that didn't require the relic can stay the same
            new_locks.append(lock)
        else:
            # Otherwise, remove the old relic as a requirement and instead add all the locks to that relic
            for transfer_lock in locks_to_add:
                new_lock = set(lock)
                new_lock.remove(ability_to_replace)
                for requirement in transfer_lock:
                    new_lock.add(requirement)
                new_locks.append(new_lock)
    return new_locks


# Helper function to see if a set is strictly a subset of another.
def is_sub_set(first_set: set, second_set: set) -> bool:
    sub_result = True
    for element in first_set:
        sub_result = sub_result and element in second_set
    return sub_result


def pick_relic_locations(rng, pool: dict, locations: list, mapping: dict):
    if not len(pool["relics"]):
        return mapping
    mapping = mapping or {}
    for i in range(len(pool["relics"])):
        remaining_relics = pool["relics"][:]
        relic = remaining_relics.pop(i)  # js splice remove the item from the object

        # Find a location not locked by the current relic.
        def available_filter(loc: dict) -> bool:
            if len(loc["locks"]) == 0 or any(relic["ability"] not in lock for lock in loc["locks"]):
                return True
            return False

        location_available = list(filter(available_filter, pool["locations"]))
        if len(location_available):
            # Get random location.
            shuffled = util.shuffled(rng, location_available)
            location = {}
            while len(shuffled):
                location = shuffled.pop()
                if ("blocked" in pool and location["id"] in pool["blocked"] and
                        relic["ability"] in pool["blocked"]["location_id"]):
                    location = None
                else:
                    break
            if location:
                # After placing the relic in this location, anything previously locked by the relic is now locked
                # by the requirements of the new location.
                new_locations = [loc for loc in pool["locations"] if loc != location]

                def map_location(loc: dict) -> dict:
                    new_location = loc if loc else {}
                    replaced_locks = replace_locks(new_location["locks"], relic["ability"], location["locks"])
                    new_locks = list(filter(lambda lock: relic["ability"] not in lock, replaced_locks))
                    # Filter out locks that are supersets of other locks.
                    new_locks.sort(key=lambda locks: len(locks))
                    deleted = []
                    for i in range(len(new_locks) - 1):
                        lock = new_locks[i]
                        j = i + 1
                        while j < len(new_locks):
                            # If lock i is a subset of lock j, remove j from the list.
                            if is_sub_set(lock, new_locks[j]):
                                if j not in deleted:
                                    deleted.append(j)
                            j += 1
                    deleted.sort(reverse=True)
                    if len(deleted):
                        for index in deleted:
                            del new_locks[index]
                    new_location["locks"] = new_locks
                    return new_location

                new_locations = list(map(map_location, new_locations))
                # Add selection to mapping.
                new_mapping = mapping if mapping else {}
                new_mapping[relic["ability"]] = location
                # Pick from remaining pool.
                return pick_relic_locations(rng,
                                            {"locations": new_locations,
                                             "relics": remaining_relics,
                                             "blocked": pool["blocked"]},
                                            locations,
                                            new_mapping)
    raise PickLock


def get_locations() -> list:
    locations = [loc for loc in relics.relics_list if "extension" not in loc and
                 loc["ability"] != constants.RELIC["THRUST_SWORD"]]

    for loc in extension.location_list:
        locations.append(loc)

    item_id = ""
    for loc in locations:
        if "ability" in loc:
            item_id = loc["ability"]
        elif "name" in loc:
            item_id = loc["name"]

        if "itemId" in loc:
            item_id_offset = loc["itemId"] + constants.tileIdOffset
            item = util.item_from_tile_id(item_id_offset)
            loc["item"] = item
            if "tileIndex" in loc:
                loc["tile"] = item["tiles"][loc["tileIndex"]]

        loc["id"] = item_id
    return locations


def graph(mapping: dict) -> list:
    graph_list = []
    locks_list = []
    for k, v in mapping.items():
        for lock in v["locks"]:
            locks_list.append(list(lock))
        if any(locks_list):
            graph_list.append({"item": k, "locks": locks_list})
        else:
            graph_list.append({"item": k})
        locks_list = []

    backup_graph = copy.deepcopy(graph_list)
    # Build lock graph.
    for node in graph_list:
        new_locks = []
        if "locks" in node:
            for outer in node["locks"]:
                inner_locks = []
                for item in outer:
                    for graph in graph_list:
                        if graph["item"] == item:
                            inner_locks.append(graph)
                            break
                new_locks.append(inner_locks)
        node["locks"] = new_locks
        # Clean locks.
        if not len(node["locks"]):
            del node["locks"]
    return graph_list


def solve(graph: list, requirements: set):
    abilities = []
    for lock in requirements:
        for node in graph:
            if node["item"] == lock:
                abilities.append(node)
    return abilities


def lock_depth(outer_node: list, visited: list, min_value: int) -> int:
    cache = {}

    if any(node["item"] in vis["item"] for vis in visited for node in outer_node):
        return min_value
    curr = 0
    for inner_max, node in enumerate(outer_node):
        if node["item"] in cache:
            curr = max(cache[node["item"]], inner_max)
            break
        inner_curr = 1
        if "locks" in node:
            visited.append(node)
            for inner_lock in node["locks"]:
                inner_curr += lock_depth(inner_lock, visited, inner_curr)
            visited.remove(node)
        cache[node["item"]] = inner_curr
        curr = max(inner_curr, inner_max)
        continue
    if min_value == 0:
        return curr
    return min(curr, min_value)


def complexity(solutions: list) -> int:
    result = 0
    for nodes in solutions:
        result += lock_depth(nodes, [], result)
    return result


def non_circular_back(visited: list, path: dict) -> bool:
    cache = {}
    count = 0

    for index, locks in enumerate(visited[-1]["locks"]):
        if any(vis["item"] == lock["item"] for vis in visited for lock in locks):
            return False
        result = True
        nodes = []
        for i in range(len(locks)):
            node = locks[i]
            nodes.append({})
            if "locks" in node:
                if node["item"] in cache:
                    nodes[i] = {"index": 0,
                                "locks": cache[node["item"]]["locks"],
                                "nodes": cache[node["item"]]["nodes"]}
                else:
                    visited.append(node)
                    nodes[i] = {"index": 0}
                    # nodes[i]["locks"] = []
                    for inner_lock in node["locks"]:
                        if non_circular(visited, nodes[i]):
                            if "locks" not in nodes[i]:
                                nodes[i]["locks"] = [inner_lock]
                            else:
                                nodes[i]["locks"].append(inner_lock)
                    visited.remove(node)
                    cache[node["item"]] = {
                        "locks": nodes[i]["locks"] if "locks" in nodes[i] else [],
                        "nodes": nodes[i]["nodes"] if "nodes" in nodes[i] else []
                    }
                if "locks" in nodes[i] and not len(nodes[i]["locks"]):
                    result = False
                    break
                if "locks" in nodes[i] and len(nodes[i]["locks"]):
                    """if "locks" not in path:
                        path["locks"] = []"""
                    path["locks"] = nodes[i]["locks"]

        if result:
            if path["index"] == count:
                path["nodes"] = nodes
            count += 1
        return result


def non_circular(visited: list, path: dict, return_locks: dict) -> bool:
    cache = {}
    count = 0
    visited_id = id(visited[-1]["locks"])
    if not return_locks[0]:
        return_locks[0] = visited_id

    for index, locks in enumerate(visited[-1]["locks"]):
        if any(vis["item"] == lock["item"] for vis in visited for lock in locks):
            return False
        result = True
        nodes = []
        for i in range(len(locks)):
            node = locks[i]
            nodes.append({})
            if "locks" in node:
                if node["item"] in cache:
                    nodes[i] = {"index": 0,
                                "locks": cache[node["item"]]["locks"],
                                "nodes": cache[node["item"]]["nodes"]}
                else:
                    visited.append(node)
                    nodes[i] = {"index": 0}
                    node_id = id(node)
                    for inner_lock in node["locks"]:
                        if non_circular(visited, nodes[i], return_locks):
                            if node_id in return_locks:
                                return_locks[node_id].append(inner_lock)
                            else:
                                return_locks[node_id] = [inner_lock]
                    if node_id in return_locks:
                        nodes[i]["locks"] = return_locks[node_id]
                    else:
                        nodes[i]["locks"] = []
                    visited.remove(node)
                    cache[node["item"]] = {
                        "locks": nodes[i]["locks"] if "locks" in nodes[i] else [],
                        "nodes": nodes[i]["nodes"] if "nodes" in nodes[i] else []
                    }
                if not len(nodes[i]["locks"]):
                    result = False
                    break
        if result:
            if path["index"] == count:
                path["nodes"] = nodes
            count += 1
            if visited_id == return_locks[0]:
                return_locks[visited_id] = []
                if len(return_locks) > 2:
                    for k, v in return_locks.items():
                        if k == visited_id or k == 0:
                            continue
                        for inner_value in v:
                            if inner_value not in return_locks[visited_id]:
                                return_locks[visited_id].append(inner_value)
        return result


def build_path(visited: list, path: dict, chain: set, advance: bool) -> bool:
    lock = []
    try:
        lock = path["locks"][path["index"]]
    except:
        pass

    for i in range(len(lock)):
        node = lock[i]
        if "nodes" not in path:
            path["nodes"] = []
        try:
            path["nodes"][i] = path["nodes"][i]
        except IndexError:
            path["nodes"].append({"index": 0})
        if "locks" in node:
            locks = None
            try:
                locks = path["nodes"][i]["locks"]
            except:
                pass
            if not locks:
                visited.append(node)
                locks = {0: "build_path"}
                non_circular(visited, path["nodes"][i], locks)
                visited.remove(node)
            if len(locks) > 1:
                visited.append(node)
                advance = build_path(visited, path["nodes"][i], chain, advance)
                visited.remove(node)
    for node in lock:
        chain.add(node["item"])
    if advance:
        if "locks" in path and len(path["locks"]) > 1:
            path["nodes"] = []
            path["index"] = (path["index"] + 1) % len(path["locks"])
            if path["index"] == 0:
                return True
        else:
            return True
    return False


def can_escape(graph: list, ability: str, requirements: list) -> bool:
    solutions = [solve(graph, {ability})]
    if not len(solutions) or not len(solutions[0]):
        return False
    root = solutions[0][0]
    path = {"index": 0}
    root_id = id(root)
    if "locks" in root:
        locks = {0: None}
        non_circular([root], path, locks)
        if 0 in locks and locks[0] in locks and len(locks[locks[0]]) > 0:
            path["locks"] = locks[locks[0]]
    if "locks" not in path or ("locks" in path and not len(path["locks"])):
        return False
    # TODO: Convert requirements to an array, not sure is need it
    chain = set()
    if len(root["item"]) == 1:
        chain.update(root["item"])
    # TODO: Visited to a WeakSet, guess is to handle all the circular references or to make a copy of root. Is it deep?
    visited = [root]
    count = 0
    advance = None
    while not advance and len(requirements):
        count += 1
        if count > (1 << 11):
            return False
        new_chain = set(chain)
        if "locks" in path:
            advance = build_path(visited, path, new_chain, True)
        i = 0
        while i < len(requirements):
            if not all(req in new_chain for req in requirements[i]):
                del requirements[i]
            else:
                i += 1
    return len(requirements) > 0


def randomize(rng, placed, blocked, relics: list, locations: list, goal: set, target: dict):
    pool = {
        "relics": util.shuffled("", relics),
        "locations": locations[:],
        "blocked": blocked
    }
    while len(pool["locations"]) > len(relics):
        index = rand_idx("", pool["locations"])
        pool["locations"].pop(index)
    # Place relics. TODO
    # Pick random relic locations.
    mapping = {}
    result = mapping  # ???????
    if len(pool["locations"]):
        result = pick_relic_locations("", pool, locations, "")
    # Restore original location locks in mapping.
    mapping = {}
    location_by_id = {loc["id"]: loc for loc in locations}
    for k, v in result.items():
        mapping[k] = location_by_id[v["id"]]
    # Make an inverse mapping of location => ability.
    inv = {}
    for k in mapping.keys():
        inv[result[k]["id"]] = k
    # Add placeholders for locations that are not in logic.
    for loc in locations:
        if not loc["id"] in inv:
            mapping['(' + loc["id"] + ')'] = loc
    # Build node graph.
    graphed = graph(mapping)
    if len(target):
        # Solve for completion goals.
        solutions = [solve(graphed, goal)]
        if not len(solutions):
            raise SoftLock
        depth = complexity(solutions)
        # TODO: There are some depth check and throw a ComplexityError here
    # Collect locations with escape requirements.
    escapes = []
    for key, value in mapping.items():
        if len(value["escapes"]):
            escapes.append(key)
    for escape in escapes:
        if not can_escape(graphed, escape, mapping[escape]["escapes"]):
            raise SoftLock
    return {
        "mapping": mapping,
        "solutions": solutions,
        "depth": depth
    }


def randomize_relics(rng, options: dict, new_names: list) -> dict:
    if "relicLocations" not in options:
        return {}
    # Initialize location locks.
    relic_locations = {}
    if isinstance(options["relicLocations"], dict):
        relic_locations = options["relicLocations"]
    else:
        pass
        # TODO Load from preset
    # If only an extension is specified, inherit safe logic.
    if "extension" in relic_locations:
        has_locks = False
        extension = relic_locations["extension"]
        for relic in relic_locations.keys():
            if relic != "extension" and not re.search("^[0-9](-[0-9])*", relic):
                has_locks = True
        if not has_locks:
            pass
            # TODO: Object assign
    locks_map = locks_from_locations(relic_locations)
    escapes_map = escapes_from_locations(relic_locations)
    # Get the goal and complexity target.
    target = {}
    goal = {}
    for name in list(locks_map.keys()):
        if re.search("^[0-9](-[0-9])*", name):
            parts = name.split('-')
            target["min"] = int(parts[0])
            if len(parts) == 2:
                target["max"] = int(parts[1])
            goal = {lock for locks in locks_map[name] for lock in locks}
            del locks_map[name]
    # Create relics and locations collections.
    locations = get_locations()
    extensions = []
    if options["relicLocations"]["extension"] == constants.EXTENSION["WANDERER"]:
        # This is a smaller distribution than Equipment
        # but includes all tourist checks + Spread + some Equipment - eldri7ch
        extensions.append(constants.EXTENSION["WANDERER"])
        extensions.append(constants.EXTENSION["SPREAD"])
        extensions.append(constants.EXTENSION["GUARDED"])
    elif options["relicLocations"]["extension"] == constants.EXTENSION["TOURIST"]:
        extensions.append(constants.EXTENSION["TOURIST"])
        extensions.append(constants.EXTENSION["EQUIPMENT"])
        extensions.append(constants.EXTENSION["SPREAD"])
        extensions.append(constants.EXTENSION["GUARDED"])
    elif options["relicLocations"]["extension"] == constants.EXTENSION["EQUIPMENT"]:
        extensions.append(constants.EXTENSION["EQUIPMENT"])
        extensions.append(constants.EXTENSION["SPREAD"])
        extensions.append(constants.EXTENSION["GUARDED"])
    elif options["relicLocations"]["extension"] == constants.EXTENSION["SPREAD"]:
        extensions.append(constants.EXTENSION["SPREAD"])
        extensions.append(constants.EXTENSION["GUARDED"])
    elif options["relicLocations"]["extension"] == constants.EXTENSION["GUARDED"]:
        extensions.append(constants.EXTENSION["GUARDED"])
    locations = [loc for loc in locations if "extension" not in loc or loc["extension"] in extensions]

    def relic_filter(relic: dict) -> bool:
        if "thrustSwordAbility" not in options["relicLocations"] and relic["ability"] == constants.RELIC["THRUST_SWORD"]:
            return False
        return "extension" not in relic or relic["extension"] in extensions
    enabled_relics = list(filter(relic_filter, relics.relics_list))
    # Get random thrust sword. TODO
    # Replace relics with items. TODO
    # Initialize location locks.
    for loc in locations:
        loc_id = loc["id"]
        if loc_id in locks_map:
            loc["locks"] = list(map(lambda lock: {c for c in lock}, locks_map[loc_id]))
        if loc_id in escapes_map:
            loc["escapes"] = list(map(lambda escape: {c for c in escape}, escapes_map[loc_id]))
        if "locks" not in loc or not len(loc["locks"]):
            loc["locks"] = list()
        if "escapes" not in loc:
            loc["escapes"] = list()
    # Attempt to place all relics.
    result = randomize("", {}, {}, enabled_relics, locations, goal, target)
    # Write spoilers.
    info = util.new_info()
    if "tournamentMode" not in options:
        spoilers = []
        get_new_item_by_id = {item["id"]: item for item in new_names}
        for relic in enabled_relics:
            relic_name = relic["name"]
            if "itemId" in relic:
                try:
                    item = get_new_item_by_id[relic["itemId"]]
                except KeyError:
                    item = None
                if item:
                    relic_name = item["name"]
            location = result["mapping"][relic["ability"]]
            if location:
                spoilers.append(relic_name + " at " + location["name"])
        info[3]["Relic locations"] = spoilers
        if "solutions" in result:
            # TODO: Thrust_sword
            info[4]["solutions"] = 5 # TODO: RenderSolutions
            info[4]["Complexity"] = result["depth"]
    return {
        "mapping": result["mapping"],
        "solutions": result["solutions"],
        "locations": locations,
        "relics": enabled_relics,
        "thrustSword": None,
        "info": info
    }


def write_relics(rng, options: dict, result: dict, new_names: list):
    pass
