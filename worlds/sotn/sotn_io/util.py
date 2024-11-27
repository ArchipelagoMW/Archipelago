import constants, items, relics, enemies, math, json, hashlib, re, random

"""
TODO:
function checked(file, writes) Guess this a checked constructor, for {} or for a filestream
"""

# function itemFromName(name, from) can be replaced by a dict["item_name"]
get_item_from_name = {item["name"]: item for item in items.items_list}

# get_item_tiles = {ok: iv for ok, ov in items.items_dict.items() if "tiles" in ov for ik, iv in ov.items()}

def shop_item_type(item: dict):
    item_name = next(iter(item))
    item_type = items.items_dict[item_name]["type"]

    if item_type == constants.TYPE["HELMET"]:
        return 0x01
    elif item_type == constants.TYPE["ARMOR"]:
        return 0x02
    elif item_type == constants.TYPE["CLOAK"]:
        return  0x03
    elif item_type == constants.TYPE["ACCESSORY"]:
        return 0x04

    return 0x00


# Arg 1 is one tile of item dictionary from tiles
def shop_tile_filter(tile: dict):
    shop_tile = False

    if "shop" in tile:
        shop_tile = True

    return shop_tile


def drop_tile_filter(tile: dict):
    enemy_tile = False
    librarian_tile = False

    if "enemy" in tile:
        enemy_tile = True

    if "librarian" in tile:
        librarian_tile = True

    return enemy_tile or librarian_tile


def reward_tile_filter(tile: dict):
    reward_tile = False

    if "reward" in tile:
        reward_tile = tile["reward"]

    return reward_tile


# Return -1 if candle data is not present
def candle_tile_filter(tile: dict):
    candle_tile = False

    if "candle" in tile:
        candle_tile = True

    return candle_tile


def tank_tile_filter(tile: dict):
    tank_tile = False

    if "tank" in tile:
        tank_tile = True

    return tank_tile


def non_progression_filter(item: dict):
    progression = False

    if "progression" in item:
        progression = item["progression"]

    return not progression


# Looks like argument is item after randomization process
def tiles_filter(item: dict):
    item_name = next(iter(item))
    item_value = items.items_dict[item_name]
    return "tiles" in item_value


def item_tile_filter(tile_filter: list, item_name: str) -> bool:
    shop_value = None
    tank_value = None
    reward_value = None
    candle_value = None
    drop_value = None
    item_tiles = []

    try:
        item_tiles = get_item_tiles[item_name]
    except KeyError:
        pass

    for tile in item_tiles:
        if "shop" in tile_filter or "map" in tile_filter:
            shop_value = shop_tile_filter(tile)
        if "tank" in tile_filter or "map" in tile_filter:
            tank_value = tank_tile_filter(tile)
        if "reward" in tile_filter or "map" in tile_filter:
            reward_value = reward_tile_filter(tile)
        if "candle" in tile_filter or "map" in tile_filter:
            candle_value = candle_tile_filter(tile)
        if "drop" in tile_filter or "map" in tile_filter:
            drop_value = drop_tile_filter(tile)

        if shop_value or tank_value or reward_value or candle_value or drop_value:
            if "map" in tile_filter:
                continue
            else:
                return True

    if "map" in tile_filter:
        if not [value for value in (shop_value, tank_value, reward_value, candle_value, drop_value) if value is None]:
            return not shop_value and not tank_value and not reward_value and not candle_value and not drop_value
    else:
        return False


def tile_id_offset_filter(item: dict):
    return any(key == item["type"] for key in [constants.TYPE["WEAPON1"], constants.TYPE["WEAPON2"],
                                               constants.TYPE["SHIELD"], constants.TYPE["HELMET"],
                                               constants.TYPE["ARMOR"], constants.TYPE["CLOAK"],
                                               constants.TYPE["ACCESSORY"], constants.TYPE["USABLE"]])


def enemy_filter(pair) -> bool:
    enemy_id, enemy_data = pair
    enemy_data["name"] = re.sub(r'\W+', '', enemy_data["name"]).lower()
    # filter(str.isalnum, enemy_data["name"])
    return True


def item_from_tile_id(item_id: int) -> dict:
    for item in items.items_list:
        if not tile_id_offset_filter(item):
            continue
        temp_id = item_id
        if item_id > constants.tileIdOffset:
            temp_id = item_id - constants.tileIdOffset

        if temp_id == item["id"]:
            return item


def item_slot(item: dict) -> list:
    item_name = next(iter(item))
    item_value = items.items_dict[item_name]
    item_type = item_value["type"]

    if item_type == constants.TYPE["USABLE"]:
        return [constants.slots[constants.SLOT["LEFT_HAND"]], constants.slots[constants.SLOT["RIGHT_HAND"]]]
    elif item_type == constants.TYPE["HELMET"]:
        return [constants.slots[constants.SLOT["HEAD"]]]
    elif item_type == constants.TYPE["ARMOR"]:
        return [constants.slots[constants.SLOT["BODY"]]]
    elif item_type == constants.TYPE["CLOAK"]:
        return [constants.slots[constants.SLOT["CLOAK"]]]
    elif item_type == constants.TYPE["ACCESSORY"]:
        return [constants.slots[constants.SLOT["OTHER"]], constants.slots[constants.SLOT["OTHER2"]]]
    else:
        return []


def tile_value(item: dict, tile: dict) -> int:
    item_name = next(iter(item))
    item_value = items.items_dict[item_name]
    candle = 0

    if "noOffset" in tile:
        return item_value["id"]

    item_id = item_value["id"]
    if "candle" in tile:
        candle = tile["candle"]
        item_id = ((candle or 0x00) << 8) or item_id

    if "shop" in tile:
        if any(item_value["type"] == v for k, v in constants.TYPE.items() if k in ["HELMET", "ARMOR", "CLOAK",
                                                                                   "ACCESSORY"]):
            item_id += constants.equipIdOffset
    elif candle and item_value["id"] >= constants.tileIdOffset:
        item_id += constants.tileIdOffset
    else:
        if any(item_value["type"] == v for k, v in constants.TYPE.items() if k in ["POWERUP", "HEART", "GOLD",
                                                                                   "SUBWEAPON"]):
            pass
        else:
            item_id += constants.tileIdOffset

    return item_id


def rom_offset(zone: dict, address: int) -> int:
    return zone["pos"] + address + math.floor(address / 0x800) * 0x130


def check_address_range(address: int):
    if address < 0xffff or address > 0xffffffff or address != address:
        raise Exception(f"Bad address: {hex(address)}")


def write_char(data: dict, address: int, value:int) -> int:
    check_address_range(address)
    data[address] = {"len": 1, "val": value & 0xff}

    address += 1
    if math.floor(address % 2352) > 2071:
        address = (math.floor(address / 2352) * 2352) + 2376

    return address


def write_short(data: dict, address: int, value: int) -> int:
    check_address_range(address)
    bytes_object = [  # Guess this is only for write on file
        value & 0xff,
        (value >> 8) & 0xff
    ]

    for i in range(2):
        try:
            del data[address + i]
        except KeyError:
            pass

    data[address] = {"len": 2, "val": value & 0xffff}

    address += 2
    if math.floor(address % 2352) > 2071:
        address = (math.floor(address / 2352) * 2352) + 2376

    return address


def write_word(data: dict, address: int, value: int) -> int:
    check_address_range(address)
    bytes_object = [
        value & 0xff,
        (value >> 8) & 0xff,
        (value >> 16) & 0xff,
        (value >> 24) % 0xff
    ]

    for i in range(4):
        try:
            del data[address + i]
        except KeyError:
            pass

    data[address] = {"len": 4, "val": value & 0xffffffff}

    address += 4
    if math.floor(address % 2352) > 2071:
        address = (math.floor(address / 2352) * 2352) + 2376

    return address


def write_string(data: dict, address: int, value: [int]) -> int:
    check_address_range(address)

    for i in range(len(value)):
        try:
            del data[address + i]
        except KeyError:
            pass

    data[address] = {"len": len(value), "val": value}

    return address + len(value)


# Guess this is a wrapper function to write results on a main file
def apply_write(data: dict, result: dict) -> None:
    for k, v in result.items():
        if isinstance(v["val"], list):
            write_string(data, k, v["val"])
        else:
            length = v["len"]
            if length == 1:
                write_char(data, k, v["val"])
            elif length == 2:
                write_short(data, k, v["val"])
            elif length == 4:
                write_word(data, k, v["val"])
            elif length == 8:
                raise Exception("write_long missing")


def sha256(crypto_input: bytes) -> str:
    a_hash = hashlib.sha256(crypto_input).hexdigest()

    # Hash already on function bufToHex format

    return a_hash


def buf_to_hex(buf: str) -> str:
    hex_result = ""
    for char in buf:
        hex_result += str(int(char, 16))
    return hex_result


def checksum(data: dict):
    state = bytes(map(ord, list(json.dumps(data, separators=(',', ":")))))
    a_hash = sha256(state)

    zeros = 0
    while len(a_hash) > 3 and a_hash[zeros] == '0':
        zeros += 1

    return int(a_hash[zeros:zeros+3], 16)


def options_from_string(randomize: str) -> dict:
    i = 0
    options = {}
    while i < len(randomize):
        c = randomize[i]
        i += 1
        negate = False
        if c == '~':
            if len(randomize) == i:
                raise Exception("Expected randomization argument to negate")
            negate = True
            c = randomize[i]
            i += 1
        if c == 'p':
            if negate:
                raise Exception("Cannot negate preset option")
            if randomize[i] != ':':
                raise Exception("Expected argument")
            arg: str
            start: int
            start = i + 1
            # Maybe this should be indexof + slice
            while i < len(randomize) and randomize[i] != ',':
                i += 1
            arg = randomize[start:i]
            if not len(arg):
                raise Exception("Expected argument")
            options["preset"] = arg
            try:
                if randomize[i] == ',':
                    i += 1
            except IndexError:
                pass

    # TODO: Understand and port function
    return options








# Just calling this will change on zone "not boss zone"
def replace_boss_relic_with_item(opts: dict, data: dict, relic: dict, item: dict, index: int) -> None:
    boss = constants.zones[opts["boss"]]
    item_id = items.items_dict[next(iter(item))]["id"]
    zone = constants.zones[relic["entity"]["zones"][0]]
    slots = item_slot(item)
    offset = rom_offset(zone, zone["items"] + 0x02 * index)
    write_short(data, offset, item_id + constants.tileIdOffset)

    for addr in relic["entity"]["entities"]:
        if "asItem" in relic:
            as_item = relic["asItem"]
            if 'x' in as_item:
                offset = rom_offset(zone, addr + 0x00)
                write_short(data, offset, as_item['x'])
            if 'y' in as_item:
                offset = rom_offset(zone, addr + 0x02)
                write_short(data, offset, as_item['y'])
            offset = rom_offset(zone, addr + 0x04)
            write_short(data, offset, 0x000c)
            offset = rom_offset(zone, addr + 0x08)
            write_short(data, offset, index)

    write_word(data, relic["erase"]["instructions"][0]["addresses"][0],
               relic["erase"]["instructions"][0]["instruction"])
    write_short(data, rom_offset(boss, boss["rewards"]), item_id + constants.tileIdOffset)
    offset = rom_offset(zone, opts["entry"])
    offset = write_word(data, offset, 0x08060000 + (opts["inj"] >> 2))
    offset = write_word(data, offset, 0x00041400)
    offset = rom_offset(zone, opts["inj"])
    offset = write_word(data, offset, 0x34090000 + item_id + constants.equipIdOffset)
    for slot in slots:
        offset = write_word(data, offset, 0x3c080000 + (slot >> 16))
        offset = write_word(data, offset, 0x91080000 + (slot & 0xffff))
        offset = write_word(data, offset, 0x00000000)
        next_slot = 5 + 5 * (len(slots) - index - 1)
        offset = write_word(data, offset, 0x11090000 + next_slot)
        offset = write_word(data, offset, 0x00000000)
    offset = write_word(data, offset, 0x3c088009)
    offset = write_word(data, offset, 0x91080000 + item_id + constants.equipmentInvIdOffset)
    offset = write_word(data, offset, 0x00000000)
    offset = write_word(data, offset, 0x11000004)
    offset = write_word(data, offset, 0x3409000f)
    offset = write_word(data, offset, 0x3c088018)
    for addr in relic["entity"]["entities"]:
        offset = write_word(data, offset, 0xa5090000 + addr + 0x04)
    offset = write_word(data, offset, 0x03e00008)
    offset = write_word(data, offset, 0x00000000)


def num_to_hex(num: int, width: int = None) -> str:
    sign = 1
    if num < 0:
        sign = -1
        num *= -1
    if width is None:
        width = 2 * math.ceil(len(hex(num).replace("0x", '')) / 2)
    zeros = "".zfill(width)
    hex_number = (zeros + hex(num).replace("0x", ''))[-width:]
    if sign < 0:
        return "-0x" + hex_number
    else:
        return "0x" + hex_number


def filter_pool(pair):
    item_name, value = pair
    item_tiles = []
    try:
        item_tiles = get_item_tiles[item_name]
    except KeyError:
        pass

    if item_name == "Sword Familiar":
        return False

    if not non_progression_filter(items.items_dict[item_name]):
        return False

    if "food" in items.items_dict[item_name]:
        return True

    if True:
        if item_tile_filter(["map"], item_name) or item_tile_filter(["shop", "candle", "tank"], item_name):
            return True

    if True and item_tile_filter(["drop"], item_name):
        enemy_global = False
        for tile in item_tiles:
            if "enemy" in tile:
                if tile["enemy"] == constants.GLOBAL_DROP:
                    enemy_global = True
        if not enemy_global:
            return True

    if True and 4 <= items.items_dict[item_name]["type"] <= 10:
        return True

    if True and item_tile_filter(["reward"], item_name):
        return True

    return False


def shuffled(rng, array):
    copy = array[:]
    shuffled_array = []
    while len(copy):
        rand = random.randint(0, len(copy) - 1)
        shuffled_array.append(copy[rand])
        del copy[rand]
    return shuffled_array


def randomize_relics(version: str, applied: dict, options: dict, seed: int, new_names: list, workers=0, nonce=4, url=""):
    pass


def has_non_circular_path(node: dict, visited: list) -> bool:
    return_value = True

    if "locks" not in node:
        return True
    for lock in node["locks"]:
        for inner_lock in lock:
            if any(inner_lock == vis for vis in visited):
                return False
            visited.append(inner_lock)
            return_value = has_non_circular_path(inner_lock, visited)
            visited.remove(inner_lock)
            if not return_value:
                return False
    return return_value


def new_info() -> [list]:
    MAX_VERBOSITY = 5
    return_list = []
    for _ in range(MAX_VERBOSITY):
        return_list.append({})
    return return_list


def minify_solutions(visited: [dict], outer_lock: [dict], node_tracker: [dict], parent: int):
    if parent == 0:
        if 0 not in node_tracker:
            node_tracker[0] = {"parent": 0, "node": outer_lock, "depth": 0}
    solution = []
    for outer_node in outer_lock:
        for node in outer_node:
            inner_solution = []
            node_id = id(node)
            try:
                current_node = node_tracker[node_id]
            except KeyError:
                current_node = {"parent": parent, "node": node, "depth": node_tracker[parent]["depth"] + 1}
                node_tracker[node_id] = current_node
            if "locks" in node:
                visited.append(node)
                for lock in node["locks"]:
                    if any(l == v for l, v in zip(lock, visited)):
                        continue
                    res = has_non_circular_path(lock, visited)
                    if res:
                        inner_node = id(node["locks"])
                        try:
                            current_node = node_tracker[inner_node]
                        except KeyError:
                            current_node = {"parent": node_id, "node": lock,
                                            "depth": node_tracker[node_id]["depth"] + 1}
                            node_tracker[inner_node] = current_node
                        inner_solution.append({"depth": node_tracker[current_node["parent"]]["depth"], "lock": lock})
            solution.append({"node": node_id, "solution": inner_solution, "depth": 0, "weight": 0, "parent": 0})

    print("a")




def minify_solutions_copy(visited: list, lock: list, minified: dict):
    requirements = []
    for node in lock:
        if "locks" in node:
            visited.append(node)
            solution = []
            inner_solution = []
            for lock in node["locks"]:
                if any(inner_node in visited for inner_node in lock):
                    continue
                for inner_lock in lock:
                    visited.append(inner_lock)
                    res = has_non_circular_path(inner_lock, visited)
                    visited.remove(inner_lock)
                    if res:
                        inner_solution.append(inner_lock)
                solution.append(inner_solution)
            for s in solution:
                minified = {"depth": 0, "weight": 0, "avg": 0, "requirements": []}
                minify_solutions(visited, s, minified)
            visited.remove(node)
            requirements.append({"item": node["item"], "depth": 1 + solution["depth"], "solution": solution})
        requirements.append({"item": node["item"], "depth": 1})
    depth = sorted(requirements, key=lambda x: x["depth"])[0]["depth"]
    weight = 0
    for req in requirements:
        weight += req["depth"]
    avg = weight / len(requirements)
    solution = {
        "depth": depth,
        "weight": weight,
        "avg": avg,
        "requirements": requirements
    }
    if minified["depth"] == 0 or solution["depth"] < minified["depth"] or (solution["depth"] == minified["depth"] and solution["weigth"] < minified["weight"]) or (solution["depth"] == minified["depth"] and solution["weigth"] == minified["weigth"] and solution["avg"] < minified["avg"]):
        minified["depth"] = solution["depth"]
        minified["weight"] = solution["weight"]
        minified["avg"] = solution["avg"]
        minified["requirements"] = solution["requirements"]


def render_solutions(solutions, relics, new_names, thrust_sword):
    tracker = {}
    minify_solutions([], solutions, tracker, 0)


def apply_results(checked: dict, original_bin):
    for addr, data in checked.items():
        size = data["len"]
        if size == 1:
            original_bin[addr] = data["val"] & 0xff
        elif size == 2:
            bytes_object = [
                data["val"] & 0xff,
                (data["val"] >> 8) & 0xff
            ]
            for i in range(2):
                original_bin[addr + i] = bytes_object[i]
        elif size == 4:
            bytes_object = [
                data["val"] & 0xff,
                (data["val"] >> 8) & 0xff,
                (data["val"] >> 16) & 0xff,
                (data["val"] >> 24) & 0xff,
            ]
            for i in range(4):
                pass
                original_bin[addr + i] = bytes_object[i]
        # TODO: Case 8
        else:
            print(f"{size} no function for {data}")

"""item_test = item_from_tile_id(369)
relic_test = relics.relics_dict["Heart of Vlad"]
data_test = {}

write_string(data_test, 885869, [39, 82, 65, 86, 73, 84, 89, 0, 34, 79, 79, 84, 83, 255, 0, 0,])
print(data_test)

options_test = relic_test["replaceWithItem"]

print(item_test)
print(relic_test)
replace_boss_relic_with_item(options_test, data_test, relic_test, item_test, 11)

for dt, vdt in data_test.items():
    print(f"{dt}: {vdt}")

result_test = checksum(data_test)
print(result_test)

print(options_from_string("p:safe"))"""






"""with open("o.bin", "rb") as in_file:
    original_bin = list(in_file.read())


for addr, data in data_test.items():
    size = data["len"]
    if size == 2:
        bytes_object = [
            data["val"] & 0xff,
            (data["val"] >> 8) & 0xff
        ]
        for i in range(2):
            original_bin[addr + i] = bytes_object[i]
            print(f"{addr + i} = {bytes_object[i]}")

with open("Castlevania - Symphony of the Night (USA) (Track 1).bin", "wb") as out_file:
    out_file.write(bytearray(original_bin))"""




"""for k, v in filtered_result.items():
    if "tiles" in v:
        del filtered_result[k]["tiles"]
    print(f"{k}: {v}")
    count += 1

print(count)
print(len(items.items_dict))
print(filtered_result)
print(tile_id_offset_filter(items.items_dict["Leather shield"]))"""






"""if __name__ == "__main__":
    filter_dict = {k: mapTileData(v) for k, v in items.items.items()}
    filtered = filter(tilesFilter, items.items)

    itemTileFilter("mapTileFilter")
    #print(items.items)
    #print(filter_dict)"""

