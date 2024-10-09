from .decompile_common import value_text
from . import ff4struct

def _unit_name(i):
    prefix = ''
    if i & 0x80:
        i &= 0x7f
        prefix = 'all '

    if i <= 0x15:
        return prefix + 'actor {}'.format(value_text(i, 'actor'))

    target_table = {
        'self' : [0x17],
        'character' : [0x18, 0x19],
        'type 0 monster' : [0x1A, 0x25],
        'type 1 monster' : [0x1B, 0x26],
        'type 2 monster' : [0x1C, 0x27],
        'anyone' : [0x1D],
        'other' : [0x1E],
        'monster' : [0x1F, 0x24, 0x2F],
        'other monster' : [0x20, 0x23],
        'front row' : [0x21, 0x28],
        'back row' : [0x22, 0x29]
        }

    for target in target_table:
        if i in target_table[target]:
            return prefix + target

    return prefix + 'unit {}'.format(value_text(i))

def _condition_description(condition_bytes, rom):
    condition = condition_bytes[0]
    if condition == 0:
        unit = condition_bytes[1]
        status_byte = condition_bytes[2]
        status_list = [i for i in range(8) if (condition_bytes[3] & (1 << i))]
        return '{} status {}'.format(_unit_name(unit), ' '.join([value_text(x + status_byte * 8, 'status') for x in status_list]))

    if condition == 1:
        unit = condition_bytes[1]
        hp_index = condition_bytes[3]
        return '{} hp below index {} /* {} */'.format(_unit_name(unit), value_text(hp_index), rom.ai_hp_thresholds[hp_index])

    if condition == 2:
        flag_type = ('reaction' if condition_bytes[2] else 'condition')
        flag_value = condition_bytes[3]
        return '{} flag {}'.format(flag_type, flag_value)

    if condition == 3:
        if condition_bytes[2] == 0:
            alive_or_dead = 'alive'
        elif condition_bytes[2] == 1:
            alive_or_dead = 'dead'
        else:
            alive_or_dead = 'alivedeadmysterious {}'.format(condition_bytes[2])
        return '{} {}'.format(_unit_name(condition_bytes[1]), alive_or_dead)

    if condition == 4:
        if condition_bytes[2] == 0:
            alive_or_dead = 'alive but not only type alive'
        elif condition_bytes[2] == 1:
            alive_or_dead = 'dead'
        elif condition_bytes[2] == 2:
            alive_or_dead = 'only type alive'
        else:
            alive_or_dead = 'alivedeadmysterious {}'.format(condition_bytes[2])
        monster_name = ff4struct.text.decode(rom.text_monster_names[condition_bytes[3]])
        return 'monster {} {}  // {}'.format(value_text(condition_bytes[3]), alive_or_dead, monster_name)

    if condition == 5:
        return 'formation ${:2X}'.format((condition_bytes[2] << 8) | condition_bytes[3])

    if condition == 6:
        return 'all monsters same type as self'

    if condition == 8 or condition == 7:
        unit_name = _unit_name(condition_bytes[1])
        if condition == 7:
            unit_name = 'anyone ({})'.format(unit_name)
        elements = ''
        if condition_bytes[3]:
            elements = ' '.join([value_text(i, 'element') for i in range(8) if (condition_bytes[3] & (1 << i))]) + ' '

        if condition_bytes[2] == 194:
            command = 'magic'
        elif condition_bytes[2] == 222:
            command = 'jump'
        elif condition_bytes[2] >= 192 and condition_bytes[2] < 192 + 0x19:
            command = value_text(condition_bytes[2] - 192, 'command')
        else:
            command = value_text(condition_bytes[2])

        return '{} uses {}{}'.format(unit_name, elements, command)

    if condition == 10:
        return 'damaged'

    if condition == 11:
        return 'alone'

    return ' '.join([value_text(b) for b in condition_bytes])

def decompile_ai(rom):
    lines = []

    for i,encoded in enumerate(rom.ai_conditions):
        lines.append('ai_condition({}) {{ {} }}'.format(value_text(i), _condition_description(encoded, rom)))

    lines.append('')        

    cached_set_descriptions = {}
    for i,encoded in enumerate(rom.ai_condition_sets):
        if encoded[-1] == 0xFF:
            encoded = encoded[:-1]
        lines.append('ai_condition_set({}) {{'.format(value_text(i)))
        descriptions = []
        for c in encoded:
            d = _condition_description(rom.ai_conditions[c], rom)
            descriptions.append(d)
            lines.append('    {}  // {}'.format(value_text(c), d))
        cached_set_descriptions[i] = ', '.join(descriptions)
        lines.append('}')
        lines.append('')

    # cache which monsters use what AI so that we can annotate
    using_monsters = {}
    for i,encoded in enumerate(rom.monsters):
        m = ff4struct.monster.decode(encoded)
        if m.attack_sequence is not None:
            using_monsters.setdefault(m.attack_sequence, []).append(ff4struct.text.decode(rom.text_monster_names[i]))
        if m.reaction_sequence is not None:
            using_monsters.setdefault(m.reaction_sequence, []).append(ff4struct.text.decode(rom.text_monster_names[i]))

    for i,encoded in enumerate(rom.ai_groups):
        if encoded[-1] == 0xFF:
            encoded = encoded[:-1]
        if i in using_monsters:
            lines.append('// used by: {}'.format(', '.join(using_monsters[i])))
        lines.append('aigroup({}) {{'.format(value_text(i)))
        for j in range(0, len(encoded), 2):
            if j + 1 >= len(encoded):
                lines.append('    script {}'.format(value_text(encoded[j])))
            else:
                lines.append('    condition set {} : script {}  // {}'.format(
                    value_text(encoded[j]), value_text(encoded[j+1]), 
                    cached_set_descriptions[encoded[j]])
                )
        lines.append('}')
        lines.append('')

    return '\n'.join(lines)