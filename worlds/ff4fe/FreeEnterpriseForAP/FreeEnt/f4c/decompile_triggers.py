from . import ff4struct
from . import decompile_common

def _decompile_trigger(trigger, map_index, trigger_index):
    lines = []

    lines.append("trigger({} {})".format(decompile_common.value_text(map_index, 'map'), trigger_index))

    lines.append("{")
    lines.append("    position {} {}".format(trigger.x, trigger.y))
    if trigger.type == ff4struct.trigger.EVENT:
        lines.append("    event call {}".format(decompile_common.value_text(trigger.event_call)))
    elif trigger.type == ff4struct.trigger.TREASURE:
        if trigger.item is not None:
            contents = decompile_common.value_text(trigger.item, 'item')
        else:
            contents = '{} gp'.format(trigger.gp)

        if trigger.is_miab:
            fight = ' fight ${:02X}'.format(trigger.formation)
        else:
            fight = ''
        lines.append("    treasure {}{}".format(contents, fight))
    elif trigger.type == ff4struct.trigger.TELEPORT:
        target_map = trigger.map
        if map_index >= 0x80 and map_index != 251:
            # Underworld
            if target_map < 0x80:
                target_map += 0x100                

        facing = ''
        if trigger.target_facing is not None:
            facing = 'facing {}'.format(decompile_common.value_text(trigger.target_facing, 'direction'))

        lines.append("    teleport {} at {} {} {}".format(
            decompile_common.value_text(target_map, 'map'),
            trigger.target_x, trigger.target_y, 
            facing
            ))

    lines.append("}")
    return "\n".join(lines)

def decompile_triggers(rom):
    results = []

    for map_index,encoded_trigger_set in enumerate(rom.map_trigger_sets):
        if map_index in (251, 252, 253):
            # these are world map sets
            encoded_trigger_set = rom.world_trigger_sets[map_index - 251]

        triggers = ff4struct.trigger.decode_set(encoded_trigger_set)
        for trigger_index,trigger in enumerate(triggers):
            results.append(_decompile_trigger(trigger, map_index, trigger_index))
            results.append("")

    return "\n".join(results)
