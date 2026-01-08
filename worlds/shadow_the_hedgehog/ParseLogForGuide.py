import re
import sys

#file = "C:\\ProgramData\\Archipelago\\logs\\" + "Shadow The Hedgehog Client_2025_06_23_16_10_11.txt"
file = "C:\\Users\\Alex\\Downloads\\Archipelago\\code\\Archipelago\\logs\\Guides\\" +"Space Gadget.txt"
data = open(file).readlines()

checks_spawned = []
checks_gotten = []
checks_gotten_result = []

#[FileLog at 2025-06-23 20:08:48,290]: ChoatixShadow: Take rocket

checkpoint_pattern = r'^\[.*?\]:\s*(?P<name>\w+)\s+found\s+their\s+(?P<found_item>[^(]+)\s+\((?P<in_brackets>Checkpointsanity[^)]+)\)'
spawn_pattern = r'^\[.*?\]:\s*(.*?)\s*has spawned$'
get_pattern  = r'^\[.*?\]:\s*(?P<name>\w+)\s+found\s+their\s+(?P<found_item>[^(]+)\s+\((?P<in_brackets>[^)]+)\)'
text_pattern = r'^\[.*?\]:\s*(?P<name>\w+)\s*:\s*(?P<message>[^(]+)'

for line in data:
    match = re.match(text_pattern, line)
    if match:
        if match.group("name") == "ChoatixShadow":
            message = match.group("message")
            print("M",message)
            checks_gotten.append(message)


    match = re.match(checkpoint_pattern, line)
    if match:
        location_name = match.group('in_brackets')
        print("Check", location_name)
        checks_gotten.append(location_name)
        continue

    match = re.match(spawn_pattern, line)
    if match:
        location_name = match.group(1)
        checks_spawned.append(location_name)
        #print("Spawned:", location_name)

    match = re.match(get_pattern, line)
    if match:
        location_name = match.group('in_brackets')
        ##if location_name not in checks_spawned:
        #    #print("Had not spawned beforehand", location_name)
        #else:
        #    print("Spawned and defeated", location_name)
        checks_gotten.append(location_name)


for line in data:
    match = re.match(text_pattern, line)
    if match:
        if match.group("name") == "ChoatixShadow":
            message = match.group("message")
            print("M", message)
            checks_gotten_result.append((3,message))

    match = re.match(checkpoint_pattern, line)
    if match:
        location_name = match.group('in_brackets')
        #print("Check", location_name)
        checks_gotten_result.append((0,location_name))
        continue

    match = re.match(spawn_pattern, line)
    if match:
        location_name = match.group(1)
        if location_name not in checks_gotten:
            checks_gotten_result.append((2,location_name))

    match = re.match(get_pattern, line)
    if match:
        location_name = match.group('in_brackets')
        checks_gotten_result.append((1,location_name))

checkpoint_template = "== {name} =="

item_template = "\
'''{caption}'''\
\n{{| class=\"wikitable\n\
|-\n\
|-\n\
| [[File:shadow-placeholder.webp|thumb|none|50px]]\n\
| style=\"width:70%\" | {snippet}\n\
|}}\n"

item_template = "{caption}{snippet}"
#item_template = "[[File:{file}.png|left|thumb|500px|{caption}]]\
#    <pre>{snippet}</pre>"

lines = []
for check in checks_gotten_result:

    type = check[0]
    name = check[1]

    if len(lines) == 0 and type != 0:
        check_line = checkpoint_template.format(name="Start")
        lines.append(check_line)

    if type == 0:
        check_line = checkpoint_template.format(name=name)
        lines.append(check_line)
    elif type == 1:
        t_line = item_template.format(file=name, caption=name, snippet="")
        lines.append(t_line)
    elif type == 2:
        t_line = item_template.format(file=name, caption=name, snippet="Missed")
        lines.append(t_line)
    elif type == 3:
        t_line = item_template.format(file="", caption=name, snippet=name)
        lines.append(t_line)


data = "\n".join(lines)
print(data)

print("==For Debugging, marking as hard, failing, etc.==")
for i in [ x for x in checks_spawned if x not in checks_gotten ]:
    print("Spawned, never defeated", i)

