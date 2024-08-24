from .decompile_common import value_text

def decompile_shops(rom):
    lines = []
    for shop_id,byte_list in enumerate(rom.shops):
        lines.append('shop(${:02X})'.format(shop_id))
        lines.append('{')
        for b in byte_list:
            if b < 0xFF:
                lines.append('    {}'.format(value_text(b, 'item')))
        lines.append('}')
        lines.append('')

    return '\n'.join(lines)
