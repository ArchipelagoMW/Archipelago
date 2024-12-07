from .decompile_common import value_text

def decompile_actors(rom):
    lines = []
    for i in range(0, len(rom.actor_name_ids)):
        lines.append('actor({})'.format(value_text(i+1, 'actor')))
        lines.append('{')
        lines.append('    name ${:02X}'.format(rom.actor_name_ids[i]))

        if rom.actor_load_info[i] & 0x80:
            lines.append('    load from slot {}'.format(rom.actor_load_info[i] & 0x7F))
        else:
            lines.append('    load from stats ${:02X}'.format(rom.actor_load_info[i]))

        if rom.actor_save_info[i] & 0x80:
            lines.append('    discard')
        else:
            lines.append('    save to slot {}'.format(rom.actor_save_info[i]))

        lines.append('    commands {')
        commands = list(rom.actor_commands[i])
        while commands and commands[-1] == 0xFF:
            commands.pop()
        for c in commands:
            lines.append('        {}'.format(value_text(c, 'command')))
        lines.append('    }')

        gear = rom.actor_gear[i]
        lines.append('    right hand {} {}'.format(value_text(gear[3], 'item'), (gear[4] if (gear[4] > 1) else '')))
        lines.append('    left hand {} {}'.format(value_text(gear[5], 'item'), (gear[6] if (gear[6] > 1) else '')))
        lines.append('    head {}'.format(value_text(gear[0], 'item')))
        lines.append('    body {}'.format(value_text(gear[1], 'item')))
        lines.append('    arms {}'.format(value_text(gear[2], 'item')))
        lines.append('}')
        lines.append('')

    return '\n'.join(lines)
