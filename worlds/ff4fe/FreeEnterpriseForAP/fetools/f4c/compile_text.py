from . import lark
from . import compile_common
from . import consts
from . import ff4struct

def _postprocess_map_text(env, texts):
    altered_map_texts = dict()

    for map_number,message_index,text in texts:
        if map_number not in altered_map_texts:
            map_texts = ff4struct.text.decode(env.rom.text_bank2[map_number])
            if type(map_texts) is str:
                map_texts = [map_texts]
            altered_map_texts[map_number] = map_texts
        else:
            map_texts = altered_map_texts[map_number]

        if message_index < len(map_texts):
            map_texts[message_index] = text
        else:
            map_texts.insert(message_index, text)

    for map_number in altered_map_texts:
        env.rom.text_bank2[map_number] = ff4struct.text.encode(altered_map_texts[map_number])


def process_text_block(block, rom, env):
    params_tree = compile_common.parse(block['parameters'], 'text', 'text_block_parameters')

    text_type = params_tree.data
    if params_tree.children:
        message_index = params_tree.children[0]

    if text_type == 'map_text':
        map_number = params_tree.children[0]
        message_index = params_tree.children[1]

        # map text encoding is done in postprocess to avoid repeated
        # reencoding of other text on same map
        env.postprocess.register(_postprocess_map_text, [map_number, message_index, block['body']])
        
    elif text_type == 'monster_name_text':
        encoded_text = ff4struct.text.encode(block['body'], allow_dual_char=False, fixed_length=8)
        rom.text_monster_names[message_index] = encoded_text

    elif text_type == 'command_name_text':
        encoded_text = ff4struct.text.encode(block['body'], allow_dual_char=False, fixed_length=5)
        rom.text_command_names[message_index] = encoded_text

    elif text_type == 'item_name_text':
        encoded_text = ff4struct.text.encode(block['body'], allow_dual_char=False, fixed_length=9)
        rom.text_item_names[message_index] = encoded_text

    elif text_type == 'spell_name_text':
        is_player_spell = (message_index < len(rom.text_spell_names))
        encoded_text = ff4struct.text.encode(block['body'], allow_dual_char=False, fixed_length=(6 if is_player_spell else 8))
        if is_player_spell:
            rom.text_spell_names[message_index] = encoded_text
        else:
            rom.text_enemy_spell_names[message_index - len(rom.text_spell_names)] = encoded_text

    elif text_type == 'credits_text':
        rom.text_credits = ff4struct.text.encode(block['body'], allow_dual_char=False)

    elif text_type == 'alert_text':
        rom.text_alerts[message_index] = ff4struct.text.encode(block['body'], allow_dual_char=False)

    elif text_type == 'map_name_text':
        rom.text_map_names[message_index] = ff4struct.text.encode(block['body'], allow_dual_char=False)

    elif text_type == 'battle_text':
        rom.text_battle[message_index] = ff4struct.text.encode(block['body'], allow_dual_char=False)

    elif text_type == 'status_text':
        rom.text_status[message_index] = ff4struct.text.encode(block['body'], allow_dual_char=False)

    elif text_type == 'custom_text':
        rom.add_patch(params_tree.children[0], ff4struct.text.encode(block['body'], allow_dual_char=False))

    else:
        encoded_text = ff4struct.text.encode(block['body'])
        if text_type == 'bank_text':
            bank_number = params_tree.children[0]
            message_index = params_tree.children[1]
            if bank_number == 1:
                rom.text_bank1[message_index] = encoded_text
            elif bank_number == 3:
                rom.text_bank3[message_index] = encoded_text
