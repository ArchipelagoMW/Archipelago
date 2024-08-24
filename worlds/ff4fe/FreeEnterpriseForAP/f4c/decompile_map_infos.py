from . import decompile_common
from . import ff4struct



def decompile_map_infos(rom):
    lines = []
    for map_id,byte_list in enumerate(rom.map_infos):
        map_info = ff4struct.map_info.decode(byte_list)
        lines.append('map({})'.format(decompile_common.value_text(map_id, 'map')))
        lines.append('{')
        lines.append('    battle background ${:02X} {}'.format(
            map_info.battle_background,
            'alternate' if map_info.battle_background_alt_palette else ''
            ))
        lines.append('    warp {}'.format('enabled' if map_info.can_warp else 'disabled'))
        lines.append('    exit {}'.format('enabled' if map_info.can_exit else 'disabled'))
        lines.append('    magnetic {}'.format('enabled' if map_info.magnetic else 'disabled'))
        lines.append('    grid ${:02X}'.format(map_info.grid))
        if (map_info.grid | (map_id & 0x100)) != map_id:
            lines.append('    // ! this map\'s grid ID does not match its map ID')
        lines.append('    tileset ${:02X}'.format(map_info.tileset))
        lines.append('    placement group ${:02X}'.format(map_info.placements))
        lines.append('    border tile ${:02X}'.format(map_info.border_tile))
        lines.append('    palette ${:02X}'.format(map_info.palette))
        lines.append('    npc palettes ${:02X} ${:02X}'.format(map_info.npc_palette_0, map_info.npc_palette_1))
        lines.append('    music {}'.format(decompile_common.value_text(map_info.music, 'music')))

        bg_grid = map_info.bg_grid
        if bg_grid > 0:
            bg_grid |= (map_id & 0x100)

        background_props = ['grid ${:02X}'.format(bg_grid)]
        if map_info.bg_translucent:
            background_props.append('translucent')
        if map_info.bg_scroll_horizontal or map_info.bg_scroll_vertical:
            background_props.append('scroll')
            if map_info.bg_scroll_vertical and map_info.bg_scroll_horizontal:
                background_props.append('both')
            elif map_info.bg_scroll_vertical:
                background_props.append('vertical')
            elif map_info.bg_scroll_horizontal:
                background_props.append('horizontal')
        background_props.append('direction {}'.format(decompile_common.value_text(map_info.bg_direction, 'direction')))
        background_props.append('speed {}'.format(map_info.bg_speed))

        lines.append('    background {}'.format(' '.join(background_props)))

        if map_info.underground_npcs:
            lines.append('    underground npcs')

        if map_info.underground_map_grid:
            lines.append('    underground map grid')            

        name_comment = ''
        if map_info.name < len(rom.text_map_names):
            name_comment = '   // ' + ff4struct.text.decode(rom.text_map_names[map_info.name])
        lines.append('    name index ${:02X}{}'.format(map_info.name, name_comment))
        
        # treasure index is autocalculated; too fragile to manually adjust
        lines.append('    // treasure index {}'.format(map_info.treasure_index))

        if map_info.bit75:
            lines.append('    // bit75 true')

        if map_info.bits81to86:
            lines.append('    // bits81to86 ${:02X}'.format(map_info.bits81to86))

        lines.append('}')
        lines.append('')

    return "\n".join(lines)
