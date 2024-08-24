from . import decompile_common
from . import ff4struct

def decompile_map_grids(rom):
    lines = []

    grid_maps = {}
    for map_id,encoded_map_info in enumerate(rom.map_infos):
        map_info = ff4struct.map_info.decode(encoded_map_info)
        grid_maps.setdefault(map_info.grid | (map_id & 0x100), []).append(map_id)

    for i,byte_list in enumerate(rom.map_grids):
        if not byte_list:
            continue

        map_grid = ff4struct.map_grid.decode(byte_list)
        using_map_names = [decompile_common.value_text(m, 'map') for m in grid_maps.setdefault(i, [])]

        lines.append('mapgrid(${:02X}) // {}'.format(i, ' '.join(using_map_names)))
        lines.append('{')
        lines.append(' // ' + ' '.join(['{:2}'.format(x) for x in range(32)]))
        lines.append(' //' + '-' * (3 * 32))
        for y in range(32):
            lines.append('    ' + ' '.join(['{:02X}'.format(map_grid[x][y]) for x in range(32)]) + '   //| {:2}'.format(y))
        lines.append('}')
        lines.append('')

    return '\n'.join(lines)
