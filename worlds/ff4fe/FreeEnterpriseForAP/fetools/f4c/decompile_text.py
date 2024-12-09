from. import ff4struct
from. import consts
from .decompile_common import value_text

def decompile_text(rom):
    lines = []

    for i,encoded_text in enumerate(rom.text_bank1):
        lines.append("--- bank 1 message ${:02X} ---".format(i))
        lines.append(ff4struct.text.decode(encoded_text, consts))
        lines.append('')

    for i,encoded_texts in enumerate(rom.text_bank2):
        map_name = consts.get_name(i, 'map')
        map_name = '#{}'.format(map_name) if map_name else '${:02X}'.format(i)
        texts = ff4struct.text.decode(encoded_texts, consts)
        if type(texts) is str:
            texts = [texts]

        for j,t in enumerate(texts):
            lines.append("--- map {} message ${:02X} ---".format(map_name, j))
            lines.append(t)
            lines.append('')

    for i,encoded_text in enumerate(rom.text_bank3):
        lines.append("--- bank 3 message ${:02X} ---".format(i))
        lines.append(ff4struct.text.decode(encoded_text, consts))
        lines.append('')

    for i,encoded_text in enumerate(rom.text_battle):
        lines.append("--- battle message ${:02X} ---".format(i))
        lines.append(ff4struct.text.decode(encoded_text, consts))
        lines.append('')

    for i,encoded_text in enumerate(rom.text_alerts):
        lines.append("--- alert message ${:02X} ---".format(i))
        lines.append(ff4struct.text.decode(encoded_text, consts))
        lines.append('')

    for i,encoded_text in enumerate(rom.text_status):
        lines.append("--- status ${:02X} ---".format(i))
        lines.append(ff4struct.text.decode(encoded_text, consts))
        lines.append('')

    for i,encoded_text in enumerate(rom.text_monster_names):
        lines.append("--- monster name ${:02X} ---".format(i))
        lines.append(ff4struct.text.decode(encoded_text, consts))
        lines.append('')

    for i,encoded_text in enumerate(rom.text_command_names):
        lines.append("--- command name ${:02X} ---".format(i))
        lines.append(ff4struct.text.decode(encoded_text, consts))
        lines.append('')

    for i,encoded_text in enumerate(rom.text_map_names):
        lines.append("--- map name ${:02X} ---".format(i))
        lines.append(ff4struct.text.decode(encoded_text, consts))
        lines.append('')

    for i,encoded_text in enumerate(rom.text_item_names):
        lines.append("--- item name {} ---".format(value_text(i, 'item')))
        lines.append(ff4struct.text.decode(encoded_text, consts))
        lines.append('')

    for i,encoded_text in enumerate(rom.text_spell_names):
        lines.append("--- spell name {} ---".format(value_text(i, 'spell')))
        lines.append(ff4struct.text.decode(encoded_text, consts))
        lines.append('')

    for i,encoded_text in enumerate(rom.text_enemy_spell_names):
        lines.append("--- spell name {} ---".format(value_text(i + len(rom.text_spell_names), 'spell')))
        lines.append(ff4struct.text.decode(encoded_text, consts))
        lines.append('')

    lines.append("--- credits ---")
    lines.append(ff4struct.text.decode(rom.text_credits))
    lines.append('')

    return '\n'.join(lines)
