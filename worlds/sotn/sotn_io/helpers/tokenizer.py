import math

def read_extension():
    lines_read = []
    reading = False

    with open("extension.js") as fstream:
        file = fstream.read()

    for line in file.splitlines():
        if not line.strip():
            continue

        if "const locations = [{" in line:
            reading = True
            continue

        if reading:
            if '}, {' in line or "const exports" in line:
                result_str = ""
                inner_value = False
                for i, l in enumerate(lines_read):
                    if inner_value:
                        if '},' in l:
                            inner_value = False
                            print(result_str + '}')
                            lines_read = []
                            continue

                        if 'x' in line or 'y' in l:
                            split_line = l.split(':')
                            lvalue = '"' + split_line[0].strip() + '"'
                            rvalue = split_line[1].replace(',', '').strip()
                            result_str += f"{lvalue}: " + rvalue + ","
                            continue

                    if "}, {" in l:
                        print("}, {")
                        continue

                    split_line = l.split(':')
                    lvalue = '"' + split_line[0].strip() + '"'
                    rvalue = ""
                    if len(split_line) > 1:
                        rvalue = split_line[1].replace(',', '').strip()

                    if "LOCATION" in rvalue:
                        temp_str = rvalue.split('.')
                        rvalue = "constants.LOCATION[\"" + temp_str[1] + "\"]"
                    elif "EXTENSION" in rvalue:
                        temp_str = rvalue.split('.')
                        rvalue = "constants.EXTENSION[\"" + temp_str[1] + "\"]"
                    elif "ZONE" in rvalue:
                        temp_str = rvalue.split('.')
                        rvalue = "constants.ZONE[\"" + temp_str[1] + "\"]"
                        if lvalue == '\"zone\"':
                            rvalue = rvalue.replace("[ ", '').replace(" ]", '')
                        else:
                            rvalue = '[' + rvalue.replace("[ ", '').replace(" ]", '') + ']'

                    if "asRelic" in lvalue:
                        result_str = "\"asRelic\": {"
                        inner_value = True
                        continue
                    elif "entities" in lvalue:
                        temp_str = rvalue.split()
                        rvalue = "["
                        for part in temp_str:
                            if "0x" in part:
                                rvalue += part + ", "
                        rvalue += ']'
                    elif "addresses" in lvalue:
                        rvalue = '[' + rvalue.replace("[ ", '').replace(" ]", '') + ']'

                    print(f"{lvalue}: {rvalue},")

            lines_read.append(line)

            if "const exports" in line:
                break


def read_stats():
    result_list = []
    key_id = 1
    inner_dict = {}
    reading = False

    with open("stats.js") as fstream:
        file = fstream.read()

    for line in file.splitlines():
        if not line.strip():
            continue

        if "const equipment = [{" in line:
            reading = True
            continue

        if not reading:
            continue

        if "}, {" in line:
            result_list.append(inner_dict.copy())

        if "}]" in line:
            result_list.append(inner_dict.copy())
            break

        if all(char in line for char in [':', ',']):
            split_line = line.split(':')
            lvalue = '"' + split_line[0].strip() + '"'
            rvalue = split_line[1].replace(',', '').strip()
            if rvalue[0] == '\'' and rvalue[-1] == '\'':
                rvalue = '\"' + rvalue[1:-1] + '\"'

            if "HAND_TYPE" in rvalue:
                rvalue = rvalue.split('.')[1]
                rvalue = "constants.HAND_TYPE[\"" + rvalue + "\"]"
            elif "TYPE" in rvalue:
                rvalue = rvalue.split('.')[1]
                rvalue = "constants.TYPE[\"" + rvalue + "\"]"

            inner_dict[lvalue] = rvalue

    for items in result_list:
        print('{')
        for k, v in items.items():
            print(f"{k}: {v},")
        print("},")


def read_relics():
    reading_relics = False
    brackets = []
    line_tokens = []
    result = ""

    with open("relics.js") as fstream:
        file = fstream.read()

    for line in file.splitlines():
        if not line.strip():
            continue

        if "const relics = [{" in line:
            reading_relics = True
            result = "relics = {\n"
            continue

        if not reading_relics:
            continue

        if "[{" in line:
            list_copy = line_tokens[:]
            for token in list_copy:
                result += f"\"{token[0]}\": {token[1]}"
                line_tokens.remove(token)

            lvalue = line.split(':')[0].strip()
            if lvalue == "instructions":
                result += f"\"{lvalue}\": " + '[ {'
                brackets.append("I[{")
            else:
                result += f"\"{lvalue}\": " + '{'
                brackets.append("[{")
            continue

        if "}]" in line:
            if len(brackets) == 0:
                for token in line_tokens:
                    result += f"\"{token[0]}\": {token[1]}\n"
                result += "}}"
                print("END")
                print("--------------------------")
                print(result)
                break
            else:
                end = "},\n"
                if brackets[-1] == "I[{":
                    end = "}],"
                if brackets[-1] == "[{" or brackets[-1] == "I[{":
                    brackets.pop()
                    list_copy = line_tokens[:]
                    for token in list_copy:
                        result += f"\"{token[0]}\": {token[1]} "
                        line_tokens.remove(token)
                    result += end

            continue

        if "}, {" in line:
            for token in line_tokens:
                result += f"\"{token[0]}\": {token[1]}\n"
            line_tokens = []
            result += '},\n'
            continue

        if '{' in line:
            brackets.append('{')
            list_copy = line_tokens[:]
            for token in list_copy:
                result += f"\"{token[0]}\": {token[1]}\n"
                line_tokens.remove(token)

            lvalue = line.split(':')[0].strip()
            result += f"\"{lvalue}\": " + '{'
            continue

        if '}' in line:
            if brackets[-1] == '{':
                list_copy = line_tokens[:]
                for token in list_copy:
                    result += f"\"{token[0]}\": {token[1]} "
                    line_tokens.remove(token)
                k = 0
                if result[-1] == ',' or result[-1] == ' ':
                    k -= 1
                if result[-2] == ',' or result[-2] == ' ':
                    k -= 1
                if k == 0:
                    result += '}\n'
                else:
                    result = result[:k] + '},\n'
                brackets.pop()

                if len(line_tokens) != 0:
                    print(f"Unplaced tokens {line_tokens}")
                    break

                continue

        read_line = line.split(':')
        try:
            lvalue = read_line[0].strip()
            rvalue = read_line[1].strip()
        except IndexError:
            print(f"Error at {line}")
            print(brackets)
            break

        if "RELIC." in rvalue:
            ability = rvalue.split('.')[1].replace(',', '').strip()
            rvalue = f"RELIC[\"{ability}\"],"

        if "ZONE." in rvalue:
            zone_value = rvalue[:-1].replace('[', '').replace(']', '').strip()
            if zone_value.count(',') > 0:
                zones = zone_value.split(',')
                rvalue = "["
                for zone in zones:
                    z = zone.replace("ZONE.", '').strip()
                    rvalue += f"ZONE[\"{z}\"], "
                rvalue = rvalue[:-2] + '],'
            else:
                zones = zone_value.replace("ZONE.", '')
                rvalue = f"[ZONE[\"{zones}\"]],"

        if "EXTENSION." in rvalue:
            rvalue = rvalue.replace("EXTENSION.", '')
            rvalue = f"EXTENSION[\"{rvalue}\"],"

        if "entities" in lvalue:
            rvalue = '[' + rvalue[:-1].replace('[', '').replace(']', '').lstrip().rstrip() + '],'

        if "addresses" in lvalue:
            if rvalue[-1] == ',':
                rvalue = rvalue[:-1]

            rvalue = rvalue.replace('[', '').replace(']', '').strip()
            rvalue = '[' + rvalue + '],'

        if lvalue == "name":
            name = rvalue.replace('\'', '\"').replace(',', '')
            result += f"{name}: " + "{\n"
        else:
            if lvalue == "erase":
                if rvalue == "false,":
                    rvalue = "False,"

            if lvalue == "replaceWithRelic":
                rvalue = f"\"{rvalue[:-1]}\","

            if lvalue == "replaceWithItem":
                rvalue = f"\"{rvalue[:-1]}\","

            if lvalue == "consumesItem":
                if rvalue == "false,":
                    rvalue = "False,"

            if lvalue == "instructions":
                print(lvalue)

            line_tokens.append([lvalue, rvalue])


def read_enemies():
    result = ""
    reading_drops = False
    reading_stats = False
    line_tokens = []
    last_token = False

    with open("enemies.js") as fstream:
        file = fstream.read()

    for line in file.splitlines():
        if not line.strip():
            continue

        if "enemiesDrops = [{" in line:
            #reading_drops = True
            result = "enemiesDrops = {\n"
            continue

        if "enemyStats = [" in line:
            reading_stats = True
            result = "enemyStats = {\n"
            continue

        if reading_drops:
            if "id: " in line:
                id_num = int(line.split(':')[1].replace(',', '').strip())
                result_str = f"\"id\": {id_num}" + ', '
                token_tuple = ("id", result_str)
                line_tokens.append(token_tuple)
                continue
            elif "name: " in line:
                name = line.split(':')[1].replace('\'', '\"').replace(',', '').strip()
                result_str = '{' + f"\"name\": {name}, "
                token_tuple = ("name", result_str)
                line_tokens.append(token_tuple)
                continue
            elif "level: " in line:
                level = int(line.split(':')[1].replace(',', '').strip())
                result_str = f"\"level\": {level}, "
                token_tuple = ("level", result_str)
                line_tokens.append(token_tuple)
                continue
            elif "dropAddresses: " in line:
                addresses = line.split(':')[1].replace('[', '')
                if addresses[-1] == ',':
                    addresses = addresses[:-2].strip()

                result_str = f"\"dropAdresses\": [{addresses}]"
                token_tuple = ("address", result_str)
                line_tokens.append(token_tuple)
            elif "}]" in line:
                last_token = True
            elif "}, {" in line or last_token:
                if last_token:
                    reading_drops = False

                def get_value(att_name: str):
                    for token in line_tokens:
                        if token[0] == att_name:
                            return token[1]
                    return "empty"

                token_place = 0
                while len(line_tokens) != token_place:
                    value = get_value("name")
                    result += value
                    token_place += 1
                    value = get_value("id")
                    result += value
                    token_place += 1
                    value = get_value("level")
                    if value != "empty":
                        result += value
                        token_place += 1
                    value = get_value("address")
                    result += value
                    token_place += 1

                result += "},\n"
                line_tokens = []
            else:
                print(f"No token found {line}")

        if reading_stats:
            if "const exports = {" in line:
                break

            lvalue = line.split(':')[0].strip()
            # if any(int_str in line for int_str in ["index", "hpValue", "atkValue", "defValue"]):
            if False:
                pass
                # rvalue = int(line.split(':')[1].replace(',', '').strip())
                # rvalue = rvalue
                # line_tokens.append([lvalue, rvalue])
            else:
                if "}, {" in line:
                    name_value = {token[0]: token[1] for token in line_tokens}
                    add_order = ["index", "name", "nameOffset", "newNameReference", "newNameText", "hpOffset",
                                 "hpValue", "atkOffset", "atkValue", "atkTypeOffset", "defOffset", "defValue",
                                 "weakOffset", "resistOffset", "guardOffset", "absorbOffset"]

                    for attr in add_order:
                        if attr == "index":
                            result += "{\n" + f"\"id\": {name_value[attr][:-1]}, \n"
                            continue

                        lvalue = '\"' + f"{attr}" + "\": "
                        rvalue = name_value[attr]
                        result += f"{lvalue}{rvalue}" + "\n"
                    result += "},\n"
                elif line == "  ]":
                    print("end")
                elif line == "    {":
                    print("a")
                elif line == "    }":
                    print("list end")
                else:
                    rvalue = line.split(':')[1].strip()
                    line_tokens.append([lvalue, rvalue])


    print("---------------------END---------------------")
    print(result)


def read_items():
    result = ""
    inner_loop = False
    adding_items = False
    read_values = []
    count = 0

    with open("items.js") as fstream:
        file = fstream.read()

    for line in file.splitlines():
        if not line.strip():
            continue

        if "items = [{" in line:
            result += "items = {"
            adding_items = True
            continue
        elif not adding_items:
            continue

        if not inner_loop:
            if "}, {" in line:
                if inner_result == "":
                    if read_values:
                        for value in read_values:
                            result += value + ", \n"
                    read_values = []
                    if result[-1] == '{':
                        result = result[:-1]
                continue
            elif "name:" in line:
                name = line.split(': ')[1].replace('\'', '\"').replace(',', '').strip()
                result += '},'
                result += f"\n{name}: "
                result += '{\n'
            elif "type:" in line:
                item_type = line.split()[1].split('.')[1].replace(',', '')
                read_values.append("\"type\": TYPE[\"" + item_type + "\"]")
            elif "id" in line:
                id = int(line.split()[1].replace(',', ''))
                read_values.append(f"\"id\": {id}")
            elif "blacklist:" in line:
                rvalue = line.split(':')[1].strip()[2:-2]
                read_values.append(f"\"blacklist\": [{rvalue}]")
            elif "food:" in line:
                rvalue = line.split(':')[1].replace(',', '').strip()
                if rvalue == "true":
                    read_values.append(f"\"food\": True")
                elif rvalue == "false":
                    read_values.append(f"\"food\": False")
            elif "thrustSword:" in line:
                rvalue = line.split(':')[1].replace(',', '').strip()
                if rvalue == "true":
                    read_values.append(f"\"thrustSword\": True")
                elif rvalue == "false":
                    read_values.append(f"\"thrustSword\": False")
            elif "progression:" in line:
                rvalue = line.split(':')[1].replace(',', '').strip()
                if rvalue == "true":
                    read_values.append(f"\"progression\": True")
                elif rvalue == "false":
                    read_values.append(f"\"progression\": False")
            elif "salable:" in line:
                rvalue = line.split(':')[1].replace(',', '').strip()
                if rvalue == "true":
                    read_values.append(f"\"salable\": True")
                elif rvalue == "false":
                    read_values.append(f"\"salable\": False")
            elif "tiles:" in line:
                inner_loop = True
                inner_result = "\"tiles\": [\n{"
                if read_values:
                    for value in read_values:
                        result += value + ", \n"
                read_values = []
                continue
            elif "}]" in line:
                if not inner_loop:
                    print(f"END: {line}")
                    with open("result.txt", 'w') as fd:
                        fd.write(result)
                    break
            else:
                if not inner_loop:
                    print(f"Last: {line}")
                    break

        if inner_loop:
            if "zones:" in line:
                zone = line.split(':')[1].replace('[', '').replace(']', '')[:-1]
                if ',' in zone:
                    inner_zone = zone.replace("ZONE.", '').split(',')
                    zone_result = f"\"zones\": [ZONE[\"{inner_zone[0].strip()}\"], ZONE[\"{inner_zone[1].strip()}\"]], "
                else:
                    inner_zone = zone.split('.')[1].strip()
                    zone_result = f"\"zones\": ZONE[\"{inner_zone}\"], "

                inner_result += zone_result
            elif "index: " in line:
                index = line.split(':')[1].replace(',', '').strip()
                inner_result += f"\"index\": {int(index)}, "
            elif "entities:" in line:
                entity = line.split(':')[1][:-1].replace('[', '').replace(']', '').strip()
                inner_result += f"\"entities\": [{entity}], "
            elif "candle:" in line:
                candle = line.split(':')[1][:-1].strip()
                inner_result += f"\"candle\": {candle}, "
            elif "addresses:" in line:
                addresses = line.split(':')[1].strip()
                addresses = '[' + addresses[2:-3] + ']'
                inner_result += f"\"addresses\": {addresses}, "
            elif "enemy:" in line:
                enemy = line.split(':')[1].replace(',', '').strip()
                if enemy == "GLOBAL_DROP":
                    inner_result += f"\"enemy\": {enemy}, "
                elif enemy.isnumeric():
                    inner_result += f"\"enemy\": {int(enemy)}, "
                else:
                    print(f"ERROR: {line}")
            elif "noOffset:" in line:
                rvalue = line.split(':')[1].replace(',', '').strip()
                if rvalue == "true":
                    inner_result += f"\"noOffset\": True, "
                elif rvalue == "false":
                    inner_result += f"\"noOffset\": False, "
            elif "tank:" in line:
                rvalue = line.split(':')[1].replace(',', '').strip()
                if rvalue == "true":
                    inner_result += f"\"tank\": True, "
                elif rvalue == "false":
                    inner_result += f"\"tank\": False, "
            elif "librarian:" in line:
                rvalue = line.split(':')[1].replace(',', '').strip()
                if rvalue == "true":
                    inner_result += f"\"librarian\": True, "
                elif rvalue == "false":
                    inner_result += f"\"librarian\": False, "
            elif "shop:" in line:
                rvalue = line.split(':')[1].replace(',', '').strip()
                if rvalue == "true":
                    inner_result += f"\"shop\": True, "
                elif rvalue == "false":
                    inner_result += f"\"shop\": False, "
            elif "despawn:" in line:
                rvalue = line.split(':')[1].replace(',', '').strip()
                if rvalue == "true":
                    inner_result += f"\"despawn\": True, "
                elif rvalue == "false":
                    inner_result += f"\"despawn\": False, "
            elif "reward:" in line:
                rvalue = line.split(':')[1].replace(',', '').strip()
                if rvalue == "true":
                    inner_result += f"\"reward\": True, "
                elif rvalue == "false":
                    inner_result += f"\"reward\": False, "
            elif "}, {" in line:
                result += inner_result + "},\n{"
                inner_result = ""
            elif "}]," in line:
                #result += inner_result + "},\n{"
                result += inner_result + "}]"
                inner_result = ""
                inner_loop = False
            else:
                print(f"Inner last: {line}")
                break


def read_constants():
    with open('constants.js', 'r') as f:
        text = f.read()
        output = []
        object_depth = 0
        object_type = ""

        for line in text.splitlines():
            if not line.strip() or line.lstrip().startswith("//"):
                continue

            if "const exports = {" in line:
                break

            if all(char in line for char in ['=', '{', '}']):
                temp_list = []
                var_name = line.split()[1]
                lvalue = line.split()[4].replace(':', '')
                rvalue = line.split()[5].replace(',', '')
                temp_list.append([lvalue, rvalue])
                lvalue = line.split()[6].replace(':', '')
                rvalue = line.split()[7].replace(',', '')
                temp_list.append([lvalue, rvalue])
                output.append(["Multi-single", [var_name, temp_list]])
                continue

            if all(char in line for char in ['=', '[', '{']):
                outer_list = []
                inner_list = []
                object_depth = 2
                var_name = line.split()[1]
                object_type = "Multi-long"
                continue

            if all(char in line for char in ['=', '{']):
                inner_list = []
                object_depth = 1
                var_name = line.split()[1]
                object_type = "Multi-short"
                continue

            if object_depth == -1:
                if ']' in line:
                    output.append([object_type, [var_name, inner_list]])
                    object_depth = 0
                    continue

            if object_depth == 1 and '}' in line and "\'}\'" not in line:
                output.append([object_type, [var_name, inner_list]])
                object_depth = 0
                continue

            if object_depth == 2 and "}, {" in line:
                outer_list.append(inner_list)
                inner_list = []
                continue

            if object_depth == 2 and "}]" in line:
                output.append([object_type, [var_name, outer_list]])
                object_depth = 0
                continue

            if object_depth == -1:
                inner_list.append(line.replace('\'', '').replace(',', '').lstrip())
                continue

            if object_depth == 1:
                if all(char in line for char in ['[', ']']):
                    lvalue = line.split()[0][1]
                    rvalue = [line.split()[2].replace(',', ''), line.split()[3]]
                else:
                    if line.count(':') > 1:
                        line_list = line.replace('\'', '').replace(',', '').lstrip().split(':')
                        lvalue = (line_list[0] + ':' + line_list[1]).lstrip()
                        rvalue = (line_list[2] + ':' + line_list[3]).lstrip()
                    else:
                        lvalue = line.split(':')[0].replace('\'', '').lstrip()
                        rvalue = line.split(':')[1].replace('\'', '').lstrip().replace('\'', '').replace(',', '')
                inner_list.append([lvalue, rvalue])
                continue

            if object_depth == 2:
                lvalue = line.split(':')[0].lstrip()
                rvalue = line.split(':')[1].replace(',', '').lstrip()
                inner_list.append([lvalue, rvalue])
                continue

            if '[' in line:
                object_depth = -1
                var_name = line.split()[1]
                inner_list = []
                object_type = "Enum"
                continue

            if '=' in line and object_depth == 0:
                lvalue = line.split()[1]
                rvalue = line.split()[3].replace('\'', '')
                output.append(["Single", [lvalue, rvalue]])

        print(output)

    for o in output:
        if o[0] == "Single":
            if o[1][1].isnumeric():
                print(f"{o[1][0]} = {o[1][1]}")
            else:
                if "0x" in o[1][1]:
                    print(f"{o[1][0]} = {o[1][1]}")
                else:
                    print(f"{o[1][0]} = \"{o[1][1]}\"")

        if o[0] == "Multi-single":
            result = f"{o[1][0]} = " + "{ " + f"{o[1][1][0][0]}: {o[1][1][0][1]}, {o[1][1][1][0]}: {o[1][1][1][1]}" + "}"
            print(result)

        if o[0] == "Multi-short":
            result = f"{o[1][0]} = " + "{"
            print(result)
            for inner in o[1][1]:
                rvalue = f"\"{inner[1]}\""
                if isinstance(inner[1], list):
                    rvalue = f"[{inner[1][0]}, {inner[1][1]}]"
                elif inner[1].isnumeric():
                    rvalue = inner[1]
                elif "0x" in inner[1]:
                    rvalue = inner[1]
                print(f"    \"{inner[0]}\": {rvalue},")
            print("}")

        if o[0] == "Multi-long":
            result = f"{o[1][0]} = ["
            result += "{"
            for inner in o[1][1]:
                result += f"{inner[0][1]}: [{inner[1][1]}, {inner[2][1]}], "
            print(result)

        if o[0] == "Enum":
            print(f"{o[1][0]} = [")
            index = 0
            for inner in o[1][1]:
                print(f"    {inner},")
                index += 1
            print("]")


def read_graphed():
    result = ""
    with open("graphed.txt") as fstream:
        file = fstream.read()

    for line in file.splitlines():
        line = line.strip()
        print(line)


def read_graph():
    result = ""
    with open("graph.txt") as fstream:
        file = fstream.read()

        for line in file.splitlines():
            line = line.strip()
            if ':' in line:
                lvalue = line.split(':')[0].strip()
                rvalue = line.split(':')[1].strip()
                result += "\"" + lvalue + "\": " + rvalue
            elif "}," in line:
                result += line + '\n'
            else:
                result += line
        print(result)


def read_mapping():
    with open("mapping.txt") as fstream:
        file = fstream.read()

    skip = False
    result = ""
    for line in file.splitlines():
        if "id:" in line:
            rvalue = line.split(':')[1].replace(',', '').strip()
            if rvalue.isnumeric():
                result += line.strip()
            else:
                second = result.rfind('\"')
                first = result.rfind('\"', 0, second)
                result = result[:first] + '\n' + result[first:second] + result[second:]
        if "replaceWithItem" in line:
            skip = True
        elif "replaceWithRelic" in line and "function" in line:
            skip = True
        elif ':' in line and not skip:
            split_line = line.split(':')
            key = split_line[0].strip()
            value = split_line[1].strip()
            if '\"' not in key:
                key = '\"' + key + '\"'
            if "true" in value:
                value = value.replace("true", "True")
            if "false" in value:
                value = value.replace("false", "False")
            result += key + ": " + value
        else:
            if not skip:
                result += line.strip()

        if skip:
            if "}," in line:
                skip = False

    print(result)

if __name__ == "__main__":
    #read_graphed()
    def rom_offset(zone_pos: int, address: int) -> int:
        return zone_pos + address + math.floor(address / 0x800) * 0x130


    # print(hex(rom_offset(0x057df998, 0x1c80)))
    print(hex(rom_offset(0x059bb0d8, 0x3640)))
    print(hex(rom_offset(0x04e31458, 0x0d2c + 0x02 * 0)))
    print(hex(rom_offset(0x067422a8, 0x12a8)))
