import re
import os
import sys
sys.path.insert(0, '../..')

import f4c
import databases

def ff4strlen(text):
    shrunken_text = re.sub(r'\[.*?\]', '*', text)
    return len(shrunken_text)

def load_custom_descriptions(description_filename):
    descriptions = {}
    with open(description_filename, 'r') as infile:
        current_description = []
        for line in infile:
            line = line.strip()
            m = re.search(r'^\<(?P<item_id>[0-9A-Fa-f]+)\>', line)
            if m:
                current_description = list()
                descriptions[int(m['item_id'], 16)] = current_description
            elif line:
                current_description.append(line)
    
    return descriptions

def generate_item_description_data(name, description,
    is_weapon=False, 
    is_armor=False,
    strength=0, percent=0, magic_strength=0, magic_percent=0,
    metallic=False, throwable=False, long_range=False
):
    if is_weapon or is_armor:
        header_left_text = name

        if is_weapon:
            header_right_text = f'[$31]{strength}/{percent}%'
        elif is_armor:
            header_right_text = f'[$3B]{strength}/{percent}% [$41]{magic_strength}/{magic_percent}%'

        icons = []
        if metallic:
            icons.append(0x8A)
        if throwable:
            icons.append(0x32)
        if long_range:
            icons.append(0x38)

        if icons:
            header_left_text += '[$cc]' + ''.join([f'[${b:02X}]' for b in icons]) + '[$cd]'

        header_filler = ' ' * (27 - ff4strlen(header_left_text) - ff4strlen(header_right_text))
        header_text = f'[$00][$fa]{header_left_text}{header_filler}{header_right_text}[$fb][$00][$00]'
    else:
        header_left_text = name
        if header_left_text.startswith('[$15]'):
            header_left_text = header_left_text[len('[$15]'):]
        header_filler = ' ' * (27 - ff4strlen(header_left_text))
        header_text = f'[$00][$fa]{header_left_text}{header_filler}[$fb][$00][$00]'

    description_lines = [header_text]
    if description is None:
        description = []
    if len(description) == 1:
        # insert blank line so description text is vertically centered
        description_lines.append('[$00][$fa]                           [$fb][$00][$00]')
    for line in description:
        line = line.replace('+', '[$cb]')
        line = line.replace('(', '[$cc]')
        line = line.replace(')', '[$cd]')
        filler = ' ' * (27 - ff4strlen(line))
        description_lines.append(f'[$00][$fa]{line}{filler}[$fb][$00][$00]')
    while len(description_lines) < 4:
        description_lines.append('[$00][$fa]                           [$fb][$00][$00]')

    output_bytes = []
    for line in description_lines:
        if ff4strlen(line) != 32:
            raise Exception(f"Unexpected line length {ff4strlen(line)} : {line}")
        
        output_bytes.extend(f4c.encode_text(line))

    return output_bytes


with open('item_names.txt', 'r') as infile:
    FE_ITEM_NAMES = [l.strip() for l in infile]

with open('vanilla_item_names.txt', 'r') as infile:
    VANILLA_ITEM_NAMES = [l.strip() for l in infile]

FE_DESCRIPTIONS = load_custom_descriptions('custom_descriptions.txt')
VANILLA_DESCRIPTIONS = load_custom_descriptions('vanilla_descriptions.txt')
CUSTOM_WEAPON_DESCRIPTIONS =  load_custom_descriptions('gba_descriptions.txt')

fe_item_data = []
vanilla_item_data = []

with open('PATH-TO-ROM', 'rb') as romfile:
    for item_id in range(0xFD):
        is_weapon = (item_id < 0x60)
        is_armor = (item_id >= 0x60 and item_id < 0xB0)

        if is_weapon or is_armor:
            # read gear data
            romfile.seek(0x79100 + item_id * 8)
            gear_data = romfile.read(8)

            strength = gear_data[1]
            percent = gear_data[2] & 0x7F
            magic_strength = (gear_data[3]) if is_armor else None
            magic_percent = (gear_data[0] & 0x7F) if is_armor else None

            metallic = bool(gear_data[0] & 0x80)
            throwable = (is_weapon and bool(gear_data[0] & 0x40))
            long_range = (is_weapon and bool(gear_data[0] & 0x20))

            fe_item_data.extend(generate_item_description_data(FE_ITEM_NAMES[item_id], FE_DESCRIPTIONS.get(item_id, None),
                is_weapon=is_weapon, is_armor=is_armor,
                strength=strength, percent=percent, magic_strength=magic_strength, magic_percent=magic_percent,
                metallic=metallic, throwable=throwable, long_range=long_range
                ))

            vanilla_item_data.extend(generate_item_description_data(VANILLA_ITEM_NAMES[item_id], VANILLA_DESCRIPTIONS.get(item_id, None),
                is_weapon=is_weapon, is_armor=is_armor,
                strength=strength, percent=percent, magic_strength=magic_strength, magic_percent=magic_percent,
                metallic=metallic, throwable=throwable, long_range=long_range
                ))
        else:
            fe_item_data.extend(generate_item_description_data(FE_ITEM_NAMES[item_id], FE_DESCRIPTIONS.get(item_id, None)))
            vanilla_item_data.extend(generate_item_description_data(VANILLA_ITEM_NAMES[item_id], VANILLA_DESCRIPTIONS.get(item_id, None)))

with open('item_descriptions.bin', 'wb') as outfile:
    outfile.write(bytes(fe_item_data))

with open('vanilla_item_descriptions.bin', 'wb') as outfile:
    outfile.write(bytes(vanilla_item_data))

custom_weapons_dbview = databases.get_custom_weapons_dbview()
for custom_weapon in custom_weapons_dbview:
    data = generate_item_description_data(
        custom_weapon.name,
        CUSTOM_WEAPON_DESCRIPTIONS.get(custom_weapon.id, None),
        is_weapon=True,
        strength=custom_weapon.attack,
        percent=custom_weapon.accuracy,
        metallic=custom_weapon.metallic,
        throwable=custom_weapon.throwable,
        long_range=custom_weapon.longrange
        )
    with open(f'custom_weapon_{custom_weapon.id:X}_description.bin', 'wb') as outfile:
        outfile.write(bytes(data))
