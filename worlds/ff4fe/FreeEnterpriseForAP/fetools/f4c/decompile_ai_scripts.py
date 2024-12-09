from .decompile_common import value_text
from . import ff4struct
from . import ai_common

def _decompile_ai_script(script, rom):
    script = list(script)
    script_lines = []
    chain_starting = False
    in_chain = False
    last_command_was_action = False

    while script:        
        b = script.pop(0)
        if b in ai_common.COMMANDS:
            cmd_data = ai_common.COMMANDS[b]
            cmd = cmd_data[0]
            if len(cmd_data) > 1:
                param_types = cmd_data[1:]
                num_params = len(param_types)
                raw_params = [script.pop(0) for i in range(num_params)]
                params = [decomp(param_types[i], raw_params[i]) for i in range(num_params)]
                cmd = cmd.format(*params)
                if cmd.startswith('message $'):
                    msg = ff4struct.text.decode(rom.text_battle[raw_params[0]])
                    cmd += '   // "{}"'.format(msg)
        elif b <= 0x30:
            cmd = 'use {}'.format(value_text(b, 'spell'))
        elif b <= 0x5E:
            cmd = 'use {} on group'.format(value_text(b - 0x30, 'spell'))
        elif b <= 0xBF:
            cmd = 'use {}'.format(value_text(b, 'spell'))
        elif b <= 0xE7:
            cmd = 'use command {}'.format(value_text(b - 0xC0, 'command'))
        elif b == 0xFB:
            if last_command_was_action:
                cmd = '' #compiler automatically handles these 'chain-into' things
            else:
                cmd = 'chain into'
        elif b == 0xFC:
            in_chain = False
            cmd = '}'
        elif b == 0xFE:
            if last_command_was_action:
                cmd = '' #compiler automatically inserts wait commands
            else:
                cmd = 'wait'
        elif b == 0xFF:
            break
        else:
            cmd = 'unknown command ${:02X}'.format(b)

        if b == 0xFD:
            in_chain = True
            script_lines.append('chain {')
        elif cmd is not None:
            if in_chain:
                cmd = '    ' + cmd
            script_lines.append(cmd)

        if b <= 0xE7 or b == 0xFC:
            last_command_was_action = True
        else:
            last_command_was_action = False

    return '\n'.join(script_lines)

def decompile_ai_scripts(rom, script_id=None, moon=False):
    lines = []

    if script_id is not None:
        script_ids = [script_id] if not moon else []
        moon_script_ids = [script_id] if moon else []
    else:
        script_ids = range(len(rom.monster_scripts))
        moon_script_ids = range(len(rom.moon_monster_scripts))

    for script_id in script_ids:
        script = rom.monster_scripts[script_id]
        lines.append('ai_script(${:02X})'.format(script_id))
        lines.append('{')
        compiled_script = _decompile_ai_script(script, rom)
        lines.extend(['    ' + x for x in compiled_script.split('\n')])
        lines.append('}')
        lines.append('')

    for script_id in moon_script_ids:
        script = rom.moon_monster_scripts[script_id]
        lines.append('ai_script(moon ${:02X})'.format(script_id))
        lines.append('{')
        compiled_script = _decompile_ai_script(script, rom)
        lines.extend(['    ' + x for x in compiled_script.split('\n')])
        lines.append('}')
        lines.append('')

    return '\n'.join(lines)

def decomp(value_type, value):
    try:
        decomp_func = globals()['decomp_{}'.format(value_type)]
    except KeyError:
        return decomp_hex(value)

    return decomp_func(value)        

def decomp_hex(b):
    return '${:02X}'.format(b)

def decomp_decimal(b):
    return str(b)

def decomp_races(b):
    return ' '.join([value_text(i, 'race', hex=False) for i in range(8) if (b & (1 << i))])

def decomp_speed_delta(b):
    if b & 0x80:
        return '- {}'.format(b & 0x7F)
    else:
        return '+ {}'.format(b)

def decomp_elements(b):
    return ' '.join([value_text(i, 'element', hex=False) for i in range(8) if (b & (1 << i))])

def decomp_music(b):
    return value_text(b, 'music')

def decomp_condition_delta(b):
    if b == 1:
        return '+ 1'
    elif b & 0x80:
        return str(b & 0x7F)
    else:
        return '? ${:02X}'.format(b)

def decomp_reaction(b):
    if b & 0x80:
        return decomp_hex(b & 0x7F)
    else:
        return '? ' + decomp_hex(b)

def decomp_target(b):
    if b <= 0x15:
        return value_text(b, 'actor')
    elif b in ai_common.TARGETS:
        return ai_common.TARGETS[b]
    else:
        return '? ' + decomp_hex(b)
