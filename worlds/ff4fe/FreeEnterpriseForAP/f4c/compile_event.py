from . import lark
from . import event_common
from . import compile_common
from . import consts

_EVENT_COMMAND_CODES = {}
_PLACEMENT_COMMAND_CODES = {}
_VEHICLE_CODES = {}

class EventCodeTransformer(lark.Transformer):
    def __init__(self, *args, **kwargs):
        lark.Transformer.__init__(self, *args, **kwargs)
        self._placement_consts = {}

    def statuses(self, statuses):
        status_byte = 0
        for v in statuses:
            status_byte |= (1 << v)
        return status_byte

    def placement_const_definition(self, n):
        value,name = n
        self._placement_consts[name] = value
        return None

    def evcmd_placement(self, n):
        placement,command = n
        try:
            if placement.data == 'placement_const':
                placement_number = self._placement_consts[str(placement.children[0])]
        except AttributeError:
            placement_number = placement

        command_text = ''.join([str(x) for x in command.children if type(x) is not int])
        if type(command.children[-1]) is int:
            # directional command
            command_code = _PLACEMENT_COMMAND_CODES[command_text + "up"]
            command_code += command.children[-1]
        else:
            command_code = _PLACEMENT_COMMAND_CODES[command_text]

        return [((placement_number << 4) | command_code)]

    def evcmd_player(self, n):
        player_keyword,command = n
        command_text = ''.join([str(x) for x in command.children if type(x) is not int])
        if type(command.children[-1]) is int:
            # directional command
            command_code = _EVENT_COMMAND_CODES["player{}up".format(command_text)]
            command_code += command.children[-1]
        else:
            command_code = _EVENT_COMMAND_CODES["player{}".format(command_text)]

        return [command_code]

    def evcmd_message(self, elements):
        number = elements[1]
        if len(elements) > 2 and elements[2].data == 'message_bank3_specifier':            
            return [0xF6, number]
        elif number >= 0x100:
            return [0xF1, number - 0x100]
        else:
            return [0xF0, number]

    def evcmd_confirm(self, elements):
        return [0xF8, elements[2] - 0x100]

    def evcmd_give_hp(self, elements):
        return [0xDE, int(elements[2] / 10)]

    def evcmd_give_mp(self, elements):
        return [0xDF, int(elements[2] / 10)]

    def evcmd_restore_hp(self, elements):
        return [0xDE, 0xFE]

    def evcmd_restore_mp(self, elements):
        return [0xDF, 0xFE]

    def evcmd_clear_status(self, elements):
        status_byte = 0
        if len(elements) > 2:
            status_byte = elements[3]

        return [0xE3, status_byte]

    def evcmd_npc(self, elements):
        result = self.event_command(elements)
        result[1] &= 0xFF
        return result

    def evcmd_music(self, elements):
        if len(elements) > 2:
            return [0xEA, elements[1]]
        else:
            return [0xFA, elements[1]]

    def evcmd_load_map(self, elements):
        # command is "load map M at X Y facing D [flags]"
        map_number = elements[2]
        x = elements[4]
        y = elements[5]
        x_and_direction = x
        flags = 0

        if map_number & 0x100:
            flags |= 0x80
            map_number &= 0xFF

        for flag_node in elements[6:]:
            if flag_node.data == 'facing_specifier':
                direction = flag_node.children[0]
                x_and_direction = ((x & 0x3F) | ((direction & 0x03) << 6))
            elif flag_node.data == 'no_transition_specifier':
                flags |= 0x20
            elif flag_node.data == 'vehicle_specifier':
                if type(flag_node.children[1]) is int:
                    flags |= (flag_node.children[1] & 0x1f)
                else:
                    slug = ''.join([str(t) for t in flag_node.children])
                    flags |= _VEHICLE_CODES[slug]
            elif flag_node.data == 'no_launch_specifier':
                flags |= 0x40

        return [0xFE, map_number, x_and_direction, y, flags]

    def event_command(self, elements):
        slug = ''
        for e in elements:
            if type(e) is lark.Tree or type(e) is int:
                break
            else:
                slug += str(e)

        result = []
        if slug in _EVENT_COMMAND_CODES:
            cmd_code = _EVENT_COMMAND_CODES[slug]
            result.append(cmd_code)
            param_elems = filter(lambda e: type(e) is int, elements)
            result.extend(param_elems)
        return result

    def ev_cancel(self, elements):
        return [0xFF]

    def batch_block(self, elements):
        if type(elements[0]) is int:
            iterations = elements[0]
            length = len(elements) - 1
            subelements = elements[1:]
        else:
            iterations = 1
            length = len(elements)
            subelements = elements

        batch_body = []
        for byte_list in subelements:
            if batch_body and (byte_list[0] >= 0xD0 or batch_body[0] >= 0xD0):
                raise ValueError("A batch block may only contain either (a) a single non-player/placement command, or (b) any number of only player/placement commands")
            batch_body.extend(byte_list)
        result = [event_common.BATCH_COMMAND_CODE, iterations, len(batch_body)] + batch_body
        return result

    def extension_command(self, elements):
        result = list([n & 0xFF for n in elements[0].children])
        if len(elements) > 1:
            block_bytes = []
            for byte_list in elements[1].children:
                block_bytes.extend(byte_list)
            if len(block_bytes) > 254:
                raise compile_common.CompileError("Event sub-block is longer than 254 bytes -- {}".format(str(elements)))
            result.append(len(block_bytes))
            result.extend(block_bytes)
        return result


def build_lookup_tables():
    if _EVENT_COMMAND_CODES:
        return

    for cmd_code in event_common.COMMANDS:
        cmd_data = event_common.COMMANDS[cmd_code]
        slug = cmd_data[0].replace('{}', '').replace(' ', '').lower()
        _EVENT_COMMAND_CODES[slug] = cmd_code

    for cmd_code in event_common.PLACEMENT_COMMANDS:
        slug = event_common.PLACEMENT_COMMANDS[cmd_code].replace(' ', '').lower()
        _PLACEMENT_COMMAND_CODES[slug] = cmd_code

    for code in event_common.VEHICLES:
        slug = event_common.VEHICLES[code].replace(' ', '').lower()
        _VEHICLE_CODES[slug] = code



def process_event_block(block, rom, env):
    params_tree = compile_common.parse(block['parameters'], 'event', 'event_block_parameters')
    event_id = params_tree.children[0]

    bytecode = None
    if env.cache:
        cache_name = env.cache.get_block_cache_name(block)
        if not env.options.force_recompile:
            bytecode = env.cache.load(cache_name)

    if bytecode is None:
        bytecode = compile_event_script(block['body'])
        if env.cache:
            env.cache.save(cache_name, bytecode)
    
    #print(' '.join(['{:02X}'.format(x) for x in bytecode]))

    rom.event_scripts[event_id] = bytecode

def compile_event_script(script):
    build_lookup_tables()

    tree = compile_common.parse(script, 'event', 'event_block_body')
    tree = EventCodeTransformer().transform(tree)

    bytecode = []
    for elem in tree.children:
        if type(elem) is list:
            bytecode.extend(elem)
    bytecode.append(0xFF)

    return bytecode

