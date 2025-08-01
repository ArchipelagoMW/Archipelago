# Preprocessor to convert Blasphemous Randomizer logic into a StringWorldDefinition for use with APHKLogicExtractor
# https://github.com/BrandenEK/Blasphemous.Randomizer
# https://github.com/ArchipelagoMW-HollowKnight/APHKLogicExtractor


import json, requests, argparse
from typing import List, Dict, Any


def load_resource_local(file: str) -> List[Dict[str, Any]]:
    print(f"Reading from {file}")
    loaded = []
    with open(file, encoding="utf-8") as f:
        loaded = read_json(f.readlines())
        f.close()

    return loaded


def load_resource_from_web(url: str) -> List[Dict[str, Any]]:
    req = requests.get(url, timeout=1)
    print(f"Reading from {url}")
    req.encoding = "utf-8"
    lines: List[str] = []
    for line in req.text.splitlines():
        while "\t" in line:
            line = line[1::]
        if line != "":
            lines.append(line)
    return read_json(lines)


def read_json(lines: List[str]) -> List[Dict[str, Any]]:
    loaded = []
    creating_object: bool = False
    obj: str = ""
    for line in lines:
        stripped = line.strip()
        if "{" in stripped:
            creating_object = True
            obj += stripped
            continue
        elif "}," in stripped or "}" in stripped and "]" in lines[lines.index(line)+1]:
            creating_object = False
            obj += "}"
            #print(f"obj = {obj}")
            loaded.append(json.loads(obj))
            obj = ""
            continue

        if not creating_object:
            continue
        else:
            try:
                if "}," in lines[lines.index(line)+1] and stripped[-1] == ",":
                    obj += stripped[:-1]
                else:
                    obj += stripped
            except IndexError:
                obj += stripped

    return loaded


def get_room_from_door(door: str) -> str:
    return door[:door.find("[")]


def preprocess_logic(is_door: bool, id: str, logic: str) -> str:
    if id in logic and not is_door:
        index: int = logic.find(id)
        logic = logic[:index] + logic[index+len(id)+4:]

    while ">=" in logic:
        index: int = logic.find(">=")
        logic = logic[:index-1] + logic[index+3:]

    while ">" in logic:
        index: int = logic.find(">")
        count = int(logic[index+2])
        count += 1
        logic = logic[:index-1] + str(count) + logic[index+3:]

    while "<=" in logic:
        index: int = logic.find("<=")
        logic = logic[:index-1] + logic[index+3:]
    
    while "<" in logic:
        index: int = logic.find("<")
        count = int(logic[index+2])
        count += 1
        logic = logic[:index-1] + str(count) + logic[index+3:]

    #print(logic)
    return logic


def build_logic_conditions(logic: str) -> List[List[str]]:
    all_conditions: List[List[str]] = []

    parts = logic.split()
    sub_part: str = ""
    current_index: int = 0
    parens: int = -1
    current_condition: List[str] = []
    parens_conditions: List[List[List[str]]] = []

    for index, part in enumerate(parts):
        #print(current_index, index, parens, part)

        # skip parts that have already been handled
        if index < current_index:
            continue

        # break loop if reached final part
        try:
            parts[index+1]
        except IndexError:
            #print("INDEXERROR", part)
            if parens < 0:
                current_condition.append(part)
                if len(parens_conditions) > 0:
                    for i in parens_conditions:
                        for j in i:
                            all_conditions.append(j + current_condition)
                else:
                    all_conditions.append(current_condition)
                break

        #print(current_condition, parens, sub_part)

        # prepare for subcondition
        if "(" in part:
            # keep track of nested parentheses
            if parens == -1:
                parens = 0
            for char in part:
                if char == "(":
                    parens += 1
            
            # add to sub part
            if sub_part == "":
                sub_part = part
            else:
                sub_part += f" {part}"
            #if not ")" in part:
            continue

        # end of subcondition
        if ")" in part:
            # read every character in case of multiple closing parentheses
            for char in part:
                if char == ")":
                    parens -= 1

            sub_part += f" {part}"

            # if reached end of parentheses, handle subcondition
            if parens == 0:
                #print(current_condition, sub_part)
                parens = -1

                try:
                    parts[index+1]
                except IndexError:
                    #print("END OF LOGIC")
                    if len(parens_conditions) > 0:
                        parens_conditions.append(build_logic_subconditions(current_condition, sub_part))
                        #print("PARENS:", parens_conditions)

                        temp_conditions: List[List[str]] = []

                        for i in parens_conditions[0]:
                            for j in parens_conditions[1]:
                                temp_conditions.append(i + j)

                        parens_conditions.pop(0)
                        parens_conditions.pop(0)

                        while len(parens_conditions) > 0:
                            temp_conditions2 = temp_conditions
                            temp_conditions = []
                            for k in temp_conditions2:
                                for l in parens_conditions[0]:
                                    temp_conditions.append(k + l)
                            
                            parens_conditions.pop(0)

                        #print("TEMP:", remove_duplicates(temp_conditions))
                        all_conditions += temp_conditions
                    else:
                        all_conditions += build_logic_subconditions(current_condition, sub_part)
                else:
                    #print("NEXT PARTS:", parts[index+1], parts[index+2])
                    if parts[index+1] == "&&":
                        parens_conditions.append(build_logic_subconditions(current_condition, sub_part))
                        #print("PARENS:", parens_conditions)
                    else:
                        if len(parens_conditions) > 0:
                            parens_conditions.append(build_logic_subconditions(current_condition, sub_part))
                            #print("PARENS:", parens_conditions)

                            temp_conditions: List[List[str]] = []

                            for i in parens_conditions[0]:
                                for j in parens_conditions[1]:
                                    temp_conditions.append(i + j)

                            parens_conditions.pop(0)
                            parens_conditions.pop(0)

                            while len(parens_conditions) > 0:
                                temp_conditions2 = temp_conditions
                                temp_conditions = []
                                for k in temp_conditions2:
                                    for l in parens_conditions[0]:
                                        temp_conditions.append(k + l)
                                
                                parens_conditions.pop(0)

                            #print("TEMP:", remove_duplicates(temp_conditions))
                            all_conditions += temp_conditions
                        else:
                            all_conditions += build_logic_subconditions(current_condition, sub_part)

                    current_index = index+2
                    
                    current_condition = []
                    sub_part = ""
                    
            continue

        # collect all parts until reaching end of parentheses
        if parens > 0:
            sub_part += f" {part}"
            continue

        current_condition.append(part)

        # continue with current condition
        if parts[index+1] == "&&":
            current_index = index+2
            continue
        
        # add condition to list and start new one
        elif parts[index+1] == "||":
            if len(parens_conditions) > 0:
                for i in parens_conditions:
                    for j in i:
                        all_conditions.append(j + current_condition)
                parens_conditions = []
            else:    
                all_conditions.append(current_condition)
            current_condition = []
            current_index = index+2
            continue
        
    return remove_duplicates(all_conditions)


def build_logic_subconditions(current_condition: List[str], subcondition: str) -> List[List[str]]:
    #print("STARTED SUBCONDITION", current_condition, subcondition)
    subconditions = build_logic_conditions(subcondition[1:-1])
    final_conditions = []

    for condition in subconditions:
        final_condition = current_condition + condition
        final_conditions.append(final_condition)

    #print("ENDED SUBCONDITION")
    #print(final_conditions)
    return final_conditions


def remove_duplicates(conditions: List[List[str]]) -> List[List[str]]:
    final_conditions: List[List[str]] = []
    for condition in conditions:
        final_conditions.append(list(dict.fromkeys(condition)))

    return final_conditions


def handle_door_visibility(door: Dict[str, Any]) -> Dict[str, Any]:
    if door.get("visibilityFlags") == None:
        return door
    else:
        flags: List[str] = str(door.get("visibilityFlags")).split(", ")
        #print(flags)
        temp_flags: List[str] = []
        this_door: bool = False
        #required_doors: str = ""

        if "ThisDoor" in flags:
            this_door = True

        #if "requiredDoors" in flags:
        #    required_doors: str = " || ".join(door.get("requiredDoors"))

        if "DoubleJump" in flags:
            temp_flags.append("DoubleJump")

        if "NormalLogic" in flags:
            temp_flags.append("NormalLogic")

        if "NormalLogicAndDoubleJump" in flags:
            temp_flags.append("NormalLogicAndDoubleJump")

        if "HardLogic" in flags:
            temp_flags.append("HardLogic")

        if "HardLogicAndDoubleJump" in flags:
            temp_flags.append("HardLogicAndDoubleJump")

        if "EnemySkips" in flags:
            temp_flags.append("EnemySkips")

        if "EnemySkipsAndDoubleJump" in flags:
            temp_flags.append("EnemySkipsAndDoubleJump")

        # remove duplicates
        temp_flags = list(dict.fromkeys(temp_flags))

        original_logic: str = door.get("logic")
        temp_logic: str = ""

        if this_door:
            temp_logic = door.get("id")

        if temp_flags != []:
            if temp_logic != "":
                temp_logic += " || "
            temp_logic += ' && '.join(temp_flags)

        if temp_logic != "" and original_logic != None:
            if len(original_logic.split()) == 1:
                if len(temp_logic.split()) == 1:
                    door["logic"] = f"{temp_logic} && {original_logic}"
                else:
                    door["logic"] = f"({temp_logic}) && {original_logic}"
            else:
                if len(temp_logic.split()) == 1:
                    door["logic"] = f"{temp_logic} && ({original_logic})"
                else:
                    door["logic"] = f"({temp_logic}) && ({original_logic})"
        elif temp_logic != "" and original_logic == None:
            door["logic"] = temp_logic
        
        return door


def get_state_provider_for_condition(condition: List[str]) -> str:
    for item in condition:
        if (item[0] == "D" and item[3] == "Z" and item[6] == "S")\
        or (item[0] == "D" and item[3] == "B" and item[4] == "Z" and item[7] == "S"):
            return item
    return None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--local', action="store_true", help="Use local files in the same directory instead of reading resource files from the BrandenEK/Blasphemous-Randomizer repository.")
    args = parser.parse_args()
    return args


def main(args: argparse.Namespace):
    doors = []
    locations = []

    if (args.local):
        doors = load_resource_local("doors.json")
        locations = load_resource_local("locations_items.json")
    
    else:
        doors = load_resource_from_web("https://raw.githubusercontent.com/BrandenEK/Blasphemous-Randomizer/main/resources/data/Randomizer/doors.json")
        locations = load_resource_from_web("https://raw.githubusercontent.com/BrandenEK/Blasphemous-Randomizer/main/resources/data/Randomizer/locations_items.json")

    original_connections: Dict[str, str] = {}
    rooms: Dict[str, List[str]] = {}
    output: Dict[str, Any] = {}
    logic_objects: List[Dict[str, Any]] = []

    for door in doors:
         if door.get("originalDoor") != None:
            if not door.get("id") in original_connections:
                original_connections[door.get("id")] = door.get("originalDoor")
                original_connections[door.get("originalDoor")] = door.get("id")

            room: str = get_room_from_door(door.get("originalDoor"))
            if not room in rooms.keys():
                rooms[room] = [door.get("id")]
            else:
                rooms[room].append(door.get("id"))

    def flip_doors_in_condition(condition: List[str]) -> List[str]:
        new_condition = []
        for item in condition:
            if item in original_connections:
                new_condition.append(original_connections[item])
            else:
                new_condition.append(item)

        return new_condition
    
    for room in rooms.keys():
        obj = {
            "Name": room,
            "Logic": [],
            "Handling": "Default"
        }

        for door in rooms[room]:
            logic = {
                "StateProvider": door,
                "Conditions": [],
                "StateModifiers": []
            }
            obj["Logic"].append(logic)
        
        logic_objects.append(obj)

    for door in doors:
        if door.get("direction") == 5:
            continue

        handling: str = "Transition"
        if "Cell" in door.get("id"):
            handling = "Default"
        obj = {
            "Name": door.get("id"),
            "Logic": [],
            "Handling": handling
        }

        visibility_flags: List[str] = []
        if door.get("visibilityFlags") != None:
            visibility_flags = str(door.get("visibilityFlags")).split(", ")
            if "1" in visibility_flags:
                visibility_flags.remove("1")
                visibility_flags.append("ThisDoor")

        required_doors: List[str] = []
        if door.get("requiredDoors"):
            required_doors = door.get("requiredDoors")

        if len(visibility_flags) > 0:
            for flag in visibility_flags:
                if flag == "RequiredDoors":
                    continue

                if flag == "ThisDoor":
                    flag = original_connections[door.get("id")]
                
                if door.get("logic") != None:
                    logic: str = door.get("logic")
                    logic = f"{flag} && ({logic})"
                    logic = preprocess_logic(True, door.get("id"), logic)
                    conditions = build_logic_conditions(logic)
                    for condition in conditions:
                        condition = flip_doors_in_condition(condition)
                        state_provider: str = get_room_from_door(door.get("id"))

                        if get_state_provider_for_condition(condition) != None:
                            state_provider = get_state_provider_for_condition(condition)
                            condition.remove(state_provider)

                        logic = {
                            "StateProvider": state_provider,
                            "Conditions": condition,
                            "StateModifiers": []
                        }
                        obj["Logic"].append(logic)
                else:
                    logic = {
                        "StateProvider": get_room_from_door(door.get("id")),
                        "Conditions": [flag],
                        "StateModifiers": []
                    }
                    obj["Logic"].append(logic)
            
            if "RequiredDoors" in visibility_flags:
                for d in required_doors:
                    flipped = original_connections[d]
                    if door.get("logic") != None:
                        logic: str = preprocess_logic(True, door.get("id"), door.get("logic"))
                        conditions = build_logic_conditions(logic)
                        for condition in conditions:
                            condition = flip_doors_in_condition(condition)
                            state_provider: str = flipped

                            if flipped in condition:
                                condition.remove(flipped)

                            logic = {
                                "StateProvider": state_provider,
                                "Conditions": condition,
                                "StateModifiers": []
                            }
                            obj["Logic"].append(logic)
                    else:
                        logic = {
                            "StateProvider": flipped,
                            "Conditions": [],
                            "StateModifiers": []
                        }
                        obj["Logic"].append(logic)

        else:
            if door.get("logic") != None:
                logic: str = preprocess_logic(True, door.get("id"), door.get("logic"))
                conditions = build_logic_conditions(logic)
                for condition in conditions:
                    condition = flip_doors_in_condition(condition)
                    stateProvider: str = get_room_from_door(door.get("id"))

                    if get_state_provider_for_condition(condition) != None:
                        stateProvider = get_state_provider_for_condition(condition)
                        condition.remove(stateProvider)

                    logic = {
                        "StateProvider": stateProvider,
                        "Conditions": condition,
                        "StateModifiers": []
                    }
                    obj["Logic"].append(logic)
            else:
                logic = {
                    "StateProvider": get_room_from_door(door.get("id")),
                    "Conditions": [],
                    "StateModifiers": []
                }
                obj["Logic"].append(logic)

        logic_objects.append(obj)

    for location in locations:
        obj = {
            "Name": location.get("id"),
            "Logic": [],
            "Handling": "Location"
        }

        if location.get("logic") != None:
            for condition in build_logic_conditions(preprocess_logic(False, location.get("id"), location.get("logic"))):
                condition = flip_doors_in_condition(condition)
                stateProvider: str = location.get("room")

                if get_state_provider_for_condition(condition) != None:
                    stateProvider = get_state_provider_for_condition(condition)
                    condition.remove(stateProvider)

                if stateProvider == "Initial":
                    stateProvider = None

                logic = {
                    "StateProvider": stateProvider,
                    "Conditions": condition,
                    "StateModifiers": []
                }
                obj["Logic"].append(logic)
        else:
            stateProvider: str = location.get("room")
            if stateProvider == "Initial":
                stateProvider = None
            logic = {
                "StateProvider": stateProvider,
                "Conditions": [],
                "StateModifiers": []
            }
            obj["Logic"].append(logic)

        logic_objects.append(obj)

    output["LogicObjects"] = logic_objects
        
    with open("StringWorldDefinition.json", "w") as file:
        print("Writing to StringWorldDefinition.json")
        file.write(json.dumps(output, indent=4))


if __name__ == "__main__":
    main(parse_args())
