import re

from . import ff4bin
from . import ff4struct
from . import consts
from . import hints
from . import event_common
from . import decompile_common

def decompile_events(rom, event_id=None):
    if event_id is None:
        event_ids = range(len(rom.event_scripts))
    elif type(event_id) in [list, tuple]:
        event_ids = event_id
    else:
        event_ids = [event_id]

    output_lines = []

    for event_id in event_ids:
        event_script = rom.event_scripts[event_id]

        sections = []
        current_section = None

        if event_script:
            num_actions_left_in_block = 0
            indent = ''
            has_else_clause = False
            else_source_section = None

            while True:
                cmd_code = event_script[0]
                event_script = event_script[1:]

                if current_section is None or cmd_code == 0xFE or (cmd_code == 0xFF and has_else_clause):
                    current_section = {
                        'commands' : [], 
                        'else' : False,
                        'activations' : set(),
                        'placements' : set(),
                        'map_messages' : set(),
                        'map' : None
                    }
                    sections.append(current_section)

                if cmd_code == 0xFF:
                    if has_else_clause:
                        current_section['else'] = True
                        current_section['else_source'] = else_source_section
                        has_else_clause = False
                    else:
                        break

                if cmd_code == 0xEB:
                    num_iterations, num_actions_left_in_block = event_script[:2]
                    event_script = event_script[2:]
                    current_section['commands'].append('batch {} {{'.format(num_iterations))
                    if num_actions_left_in_block == 0:
                        current_section['commands'].append('}')
                    else:
                        indent = '    '
                else:
                    if event_common.is_placement_command_code(cmd_code):
                        placement = (cmd_code & 0xF0) >> 4
                        current_section['placements'].add(placement)
                        sub_cmd = cmd_code & 0xF
                        if sub_cmd in event_common.PLACEMENT_COMMANDS:
                            current_section['commands'].append(indent + 'p {} {}'.format(placement, event_common.PLACEMENT_COMMANDS[sub_cmd]))
                    elif cmd_code in event_common.COMMANDS:
                        cmd_data = event_common.COMMANDS[cmd_code]
                        
                        param_data = cmd_data[1:]
                        num_params = len(param_data)
                        raw_params = list(event_script[:num_params])
                        event_script = event_script[num_params:]

                        if cmd_code == 0xFE:
                            # load map command
                            raw_params[0] += ((raw_params[3] & 0x80) << 1)
                            # extract facing from X coordinate and jam into flags param
                            if raw_params[0] < 0xFB or raw_params[0] > 0xFF:
                                raw_params[3] = (raw_params[3], ((raw_params[1] & 0xC0) >> 6))
                                raw_params[1] = raw_params[1] & 0x3F
                            else:
                                # no facing direction on overworld/underworld/moon map params
                                raw_params[3] = (raw_params[3], 0)
                            current_section['map'] = raw_params[0]
                        elif cmd_code == 0xEF:
                            # map message command
                            current_section['map_messages'].add(raw_params[0])
                        elif cmd_code == 0xF1 or cmd_code == 0xF8:
                            # high bank message or confirm message
                            raw_params[0] += 0x100

                        if cmd_code == 0xDE and raw_params[0] == 0xFE:
                            decomp_command = 'restore hp'
                        elif cmd_code == 0xDF and raw_params[0] == 0xFE:
                            decomp_command = 'restore mp'
                        else:
                            decomp_params = [decomp(param_data[i], raw_params[i]) for i in range(len(raw_params))]
                            decomp_command = indent + cmd_data[0].format(*decomp_params)

                        if cmd_code == 0xE3 and raw_params[0] != 0:
                            decomp_command = decomp_command.replace('clear status', 'clear status except')


                        comment = None
                        if cmd_code == 0xF0 or cmd_code == 0xF1:
                            comment = make_comment_from_text(rom.text_bank1[raw_params[0]])
                        elif cmd_code == 0xF6:
                            comment = make_comment_from_text(rom.text_bank3[raw_params[0]])

                        if comment:
                            comment = comment.partition('\n')[0]
                            decomp_command += '   // ' + comment

                        current_section['commands'].append(decomp_command)

                        if cmd_code == 0xF8:
                            has_else_clause = True
                            else_source_section = current_section

                        if cmd_code == 0xF4 or cmd_code == 0xF5:
                            current_section['activations'].add(raw_params[0])

                    if num_actions_left_in_block > 0:
                        num_actions_left_in_block -= 1
                        if num_actions_left_in_block == 0:
                            current_section['commands'].append('}')
                            indent = ''

            # annotate code sections if we need info from the map
            for section in sections:
                if section['placements'] or section['map_messages'] or section['activations']:
                    build_metadata(rom)

                    if section['else']:
                        section['map'] = section['else_source']['map']

                    if section['map'] is None:
                        hint = hints.get_event_map(event_id)
                        if hint is not None:
                            section['map'] = hint
                            map_method = 'hinted'
                        else:
                            section['map'] = lookup_map(rom, event_id)
                            map_method = 'autodetected'

                        if section['map']:
                            map_name = consts.get_name(section['map'], 'map')
                            if map_name is None:
                                map_name = ('${:02X}'.format(section['map']))
                            else:
                                map_name = '#' + map_name
                            section['commands'].insert(0, '// {} map {}'.format(map_method, map_name))

                    if section['map'] is None: #previous lookup may fail
                        section['commands'].insert(0, '// could not auto-detect map')
                        continue

                    if section['placements']:
                        placement_names = generate_placement_names(section['map'], section['placements'])

                        const_lines = []
                        const_lines.append('consts(placement) {')
                        for p in placement_names:
                            const_lines.append('    {}   {}'.format(p, placement_names[p]))
                        const_lines.append('}')

                        for i,cmd in enumerate(section['commands']):
                            m = re.search(r'^(?P<indent>\s*)p (?P<placement>\d+)', cmd)
                            if m:
                                p = int(m.group('placement'))
                                if p in placement_names:
                                    placement_name = placement_names[p]
                                    if placement_name:
                                        section['commands'][i] = '{}p #{}'.format(m.group('indent'), placement_name) + cmd[len(m.group(0)):]

                        section['commands'] = const_lines + section['commands']

                    map_message_comments = generate_map_message_comments(section['map'], section['map_messages'])
                    for i,cmd in enumerate(section['commands']):
                        m = re.search(r'map message (?P<message>\d+)', cmd)
                        if m:
                            section['commands'][i] = cmd + '  // ' + map_message_comments[int(m.group('message'))]
                            continue

                        m = re.search(r'activate (?P<npc>\$[0-9A-Fa-f]+)', cmd)
                        if m:
                            npc_number = int(m.group('npc')[1:], 16)
                            if section['map'] >= 0x100 or _MAP_INFOS[section['map']].underground_npcs:
                                npc_number += 0x100
                            npc_name = consts.get_name(npc_number, 'npc')
                            if npc_name:
                                section['commands'][i] = section['commands'][i].replace(m.group('npc'), '#{}'.format(npc_name))


            output_lines.append('event(${:02X})  //{}'.format(event_id, event_common.DEFAULT_EVENT_DESCRIPTIONS[event_id]))
            output_lines.append('{')
            for section in sections:
                if section['else']:
                    output_lines.append('cancel:')
                for cmd in section['commands']:
                    output_lines.append('    ' + cmd)
            output_lines.append('}')
            output_lines.append('')

    return '\n'.join(output_lines)


#-----------------------------------------------------------------------------

def make_comment_from_text(encoded_text):
    if type(encoded_text) is str:
        t = encoded_text
    else:
        t = ff4struct.text.decode(encoded_text)

    t = t.replace('\n', ' ', 1).partition('\n')[0]
    return '"{}"'.format(t)


_EVENT_SOURCE_MAPS = {}
_MAP_PLACEMENTS = {}
_MAP_MESSAGES = {}
_MAP_INFOS = {}
_EVENT_MESSAGES = {}

def build_metadata(rom):
    if _EVENT_SOURCE_MAPS:
        return

    for map_id,data in enumerate(rom.map_infos):
        map_info = ff4struct.map_info.decode(data)
        _MAP_INFOS[map_id] = map_info

        event_calls = []
        triggers = ff4struct.trigger.decode_set(rom.map_trigger_sets[map_id])
        for t in triggers:
            if t.type == ff4struct.trigger.EVENT:
                event_call = ff4struct.event_call.decode(rom.event_calls[t.event_call])
                if event_call:
                    event_calls.append(event_call)

        npc_offset = 0x100 if (map_id >= 0x100 or map_info.underground_npcs) else 0

        placements = ff4struct.npc_placement.decode_set(rom.placement_groups[map_info.placements + npc_offset])
        for p in placements:
            npc = p.npc + npc_offset
            event_call = ff4struct.event_call.decode(rom.npc_event_calls[npc])
            if event_call is not None:
                event_calls.append(event_call)
        _MAP_PLACEMENTS[map_id] = placements

        for event_call in event_calls:
            for case in event_call.cases:
                _EVENT_SOURCE_MAPS.setdefault(case.event, set()).add(map_id)
                if event_call.parameters:
                    if case.event in _EVENT_MESSAGES:
                        _EVENT_MESSAGES[case.event] = None
                    else:
                        _EVENT_MESSAGES[case.event] = event_call.parameters

        _MAP_MESSAGES[map_id] = ff4struct.text.decode(rom.text_bank2[map_id])

    for i in _EVENT_SOURCE_MAPS:
        _EVENT_SOURCE_MAPS[i] = list(_EVENT_SOURCE_MAPS[i])


def lookup_map(rom, event_id):
    if event_id not in _EVENT_SOURCE_MAPS:
        return None

    map_set = _EVENT_SOURCE_MAPS[event_id]
    if len(map_set) == 1:
        return map_set[0]
    else:
        return None

def generate_placement_names(map_id, placements):
    npc_offset = 0x100 if (map_id >= 0x100 or _MAP_INFOS[map_id].underground_npcs) else 0
    npcs = {}
    for p in range(len(_MAP_PLACEMENTS[map_id])):
        npc_name = consts.get_name(npc_offset + _MAP_PLACEMENTS[map_id][p].npc, 'npc')
        npcs.setdefault(npc_name, []).append(p)

    result = {}
    for npc_name in npcs:
        placement_list = sorted(npcs[npc_name])
        if len(placement_list) == 1:
            result[placement_list[0]] = npc_name
        else:
            for i,p in enumerate(placement_list):
                result[p] = '{}_{}'.format(npc_name, chr(ord('A') + i))

    return {x : result[x] for x in result if x in placements}


def generate_map_message_comments(map_id, messages):
    if map_id not in _MAP_MESSAGES:
        return {}
        
    map_messages = _MAP_MESSAGES[map_id]
    if type(map_messages) is str:
        map_messages = [map_messages]

    return {x: make_comment_from_text(map_messages[x]) for x in messages}


#-----------------------------------------------------------------------------

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

def decomp_const(family):
    def func(b):
        identifier = consts.get_name(b, family)
        if identifier:
            return '#{}'.format(identifier)
        else:
            return decomp_hex(b)

    return func

def decomp_status(b):
    fields = [decomp_const('status')(i) for i in range(8) if (b & (1 << i))]
    return ' '.join(fields)

decomp_actor = decomp_const('actor')

def decomp_hpmp(b):
    return str(b * 10)

decomp_item = decomp_const('item')
decomp_spell = decomp_const('spell')
decomp_spellset = decomp_const('spellset')

def decomp_gp(b):
    return str(b * 100)

decomp_music = decomp_const('music')
decomp_formation = decomp_hex
decomp_shop = decomp_hex
decomp_message = decomp_hex
decomp_flag = decomp_const('flag')
decomp_npc = decomp_hex
decomp_sound = decomp_const('sound')
decomp_vfx = decomp_const('vfx')
decomp_map = decomp_const('map')

def decomp_mapflags(flags):
    (b, facing) = flags
    
    params = []

    if facing != 0:
        params.append('facing ' + decompile_common.value_text(facing, 'direction'))

    if b & 0x20:
        params.append('no transition')

    vehicle = b & 0b00011111

    if vehicle in event_common.VEHICLES:
        params.append(event_common.VEHICLES[vehicle])
    
    if (b & 0x40):
        params.append('no launch')

    return ' '.join(params)

