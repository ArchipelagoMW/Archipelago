from . import ff4bin
from . import ff4struct
from . import decompile_common
from .decompile_event_calls import decompile_event_call

def decompile_npcs(rom):
    lines = []
    num_npcs = len(rom.npc_sprites)

    npc_maps = {}
    for map_id,data in enumerate(rom.map_infos):
        map_info = ff4struct.map_info.decode(data)
        npc_offset = 0x100 if (map_id >= 0x100 or map_info.underground_npcs) else 0
        placements = ff4struct.npc_placement.decode_set(rom.placement_groups[map_info.placements + npc_offset])
        for p in placements:
            npc = p.npc + npc_offset
            npc_maps.setdefault(npc, []).append(map_id)

    cached_map_messages = {}

    for npc_id in range(num_npcs):
        lines.append("npc({})".format(decompile_common.value_text(npc_id, 'npc')))
        lines.append("{")
        sprite = rom.npc_sprites[npc_id]
        lines.append("    sprite {}".format(decompile_common.value_text(sprite, 'sprite')))
        active = bool(rom.npc_active_flags[int(npc_id / 8)] & (1 << (npc_id % 8)))
        lines.append("    default {}".format('active' if active else 'inactive'))

        map_messages = None
        if npc_id in npc_maps and len(npc_maps[npc_id]) == 1:
            map_id = npc_maps[npc_id][0]
            if map_id not in cached_map_messages:
                texts = ff4struct.text.decode(rom.text_bank2[map_id])
                if type(texts) is str:
                    texts = [texts]
                texts = [t.replace('\n', ' ', 1).partition('\n')[0] for t in texts]
                cached_map_messages[map_id] = texts
            map_messages = cached_map_messages[map_id]

        event_call_text = decompile_event_call(rom.npc_event_calls[npc_id], map_messages=map_messages)
        lines.extend(['    ' + l for l in event_call_text.split('\n')])
        lines.append("}")
        lines.append('')

    return "\n".join(lines)


def decompile_map_placements(rom):
    lines = []

    using_maps = {}
    for map_id,encoded_map_info in enumerate(rom.map_infos):
        map_info = ff4struct.map_info.decode(encoded_map_info)
        group_number = map_info.placements
        if map_id >= 0x100 or map_info.underground_npcs:
            group_number += 0x100

        using_maps.setdefault(group_number, []).append(map_id)

    for group_number,byte_list in enumerate(rom.placement_groups):
        placements = ff4struct.npc_placement.decode_set(byte_list)

        if group_number in using_maps:
            map_comment = ' //' + ', '.join([decompile_common.value_text(m, 'map') for m in using_maps[group_number]])
        else:
            map_comment = ''

        for placement_id,placement in enumerate(placements):
            npc_id = placement.npc | (group_number & 0x100)

            lines.append('placement({} {}) {}'.format(decompile_common.value_text(group_number), placement_id, map_comment))
            lines.append('{')
            lines.append('    npc {}'.format(decompile_common.value_text(npc_id, 'npc')))
            lines.append('    position {} {}'.format(placement.x, placement.y))
            lines.append('    walking {}'.format('on' if placement.walks else 'off'))
            lines.append('    {}'.format('intangible' if placement.intangible else 'tangible'))
            lines.append('    face {}'.format(decompile_common.value_text(placement.facing, 'direction')))
            lines.append('    palette {}'.format(placement.palette))
            lines.append('    turning {}'.format('on' if placement.turns else 'off'))
            lines.append('    marching {}'.format('on' if placement.marches else 'off'))
            lines.append('    speed {}'.format(placement.speed))
            #lines.append('    // bit13 {}'.format(placement.bit13))
            #lines.append('    // bit14 {}'.format(placement.bit14))
            #lines.append('    // bit21 {}'.format(placement.bit21))
            #lines.append('    // bit22 {}'.format(placement.bit22))
            lines.append('}')
            lines.append('')

    return '\n'.join(lines)


