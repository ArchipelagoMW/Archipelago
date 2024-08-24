from . import compile_common
from .compile_event_call import compile_event_call

def process_npc_block(block, rom, env):
    parse_tree = compile_common.parse(block['parameters'], 'npc', 'npc_block_params')
    npc_id = parse_tree.children[0]

    tree = compile_common.parse(block['body'], 'npc', 'npc_block_body')

    for node in tree.children:
        if node.data == 'sprite':
            rom.npc_sprites[npc_id] = node.children[0]
        elif node.data == 'active' or node.data == 'inactive':
            flag_index = npc_id >> 3
            flag_bit = 1 << (npc_id % 8)
            if node.data == 'active':
                rom.npc_active_flags[flag_index] |= flag_bit
            else:
                rom.npc_active_flags[flag_index] &= (~flag_bit)
        elif node.data == 'eventcall':
            body = ' '.join([str(x) for x in node.children])
            rom.npc_event_calls[npc_id] = compile_event_call(body)
