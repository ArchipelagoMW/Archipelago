from . import compile_common

def process_actor_block(block, rom, env):
    params_tree = compile_common.parse(block['parameters'], 'actor', 'actor_block_params')
    tree = compile_common.parse(block['body'], 'actor', 'actor_block_body')

    actor_index = params_tree.children[0] - 1

    for node in tree.children:
        if node.data == 'name':
            rom.actor_name_ids[actor_index] = node.children[0]
        elif node.data == 'load':
            load_params = node.children[0]
            if load_params.data == 'slot':
                rom.actor_load_info[actor_index] = 0x80 | load_params.children[0]
            else:
                rom.actor_load_info[actor_index] = load_params.children[0]
        elif node.data == 'save':
            if actor_index < 20:
                rom.actor_save_info[actor_index] = node.children[0]
        elif node.data == 'discard':
            if actor_index < 20:
                rom.actor_save_info[actor_index] = 0x80
        elif node.data == 'commands':
            commands = list(node.children)
            while len(commands) < 5:
                commands.append(0xFF)
            rom.actor_commands[actor_index] = commands[:5]
        else:
            gear = list(rom.actor_gear[actor_index])
            if node.data == 'right_hand':
                gear[3] = node.children[0]
                if len(node.children) > 1:
                    gear[4] = node.children[1]
                elif node.children[0] == 0:
                    gear[4] = 0
                else:
                    gear[4] = 1
            elif node.data == 'left_hand':
                gear[5] = node.children[0]
                if len(node.children) > 1:
                    gear[6] = node.children[1]
                elif node.children[0] == 0:
                    gear[6] = 0
                else:
                    gear[6] = 1
            elif node.data == 'head':
                gear[0] = node.children[0]
            elif node.data == 'body':
                gear[1] = node.children[0]
            elif node.data == 'arms':
                gear[2] = node.children[0]

            rom.actor_gear[actor_index] = gear

