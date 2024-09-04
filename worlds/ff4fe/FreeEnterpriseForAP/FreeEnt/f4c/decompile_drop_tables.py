from . import ff4struct
from .decompile_common import value_text

def decompile_drop_tables(rom):
    lines = []
    for drop_table_id,byte_list in enumerate(rom.drop_tables):
        dt = ff4struct.drop_table.decode(byte_list)

        lines.append('droptable(${:02X}) {{'.format(drop_table_id))
        for rarity in ['common', 'uncommon', 'rare', 'mythic']:
            item = getattr(dt, rarity)
            if item is None:
                lines.append('    {} none'.format(rarity))
            else:
                lines.append('    {} {}'.format(rarity, value_text(item, 'item')))
        lines.append('}')
        lines.append('')

    return '\n'.join(lines)
