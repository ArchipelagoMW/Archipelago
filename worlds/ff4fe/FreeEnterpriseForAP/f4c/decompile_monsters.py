from .decompile_common import value_text
from . import ff4struct

def _get_elements_string(elements):
    items = []
    for i in range(8):
        if i in elements:
            items.append(value_text(i, 'element'))

    return ' '.join(items)

def _get_statuses_string(statuses):
    items = []
    for i in range(16):
        if i in statuses:
            items.append(value_text(i, 'status'))

    return ' '.join(items)

def _get_races_string(races):
    items = []
    for i in range(8):
        if i in races:
            items.append(value_text(i, 'race'))

    return ' '.join(items)

def decompile_monsters(rom):
    lines = []
    for monster_id,encoded_monster in enumerate(rom.monsters):
        monster = ff4struct.monster.decode(encoded_monster)

        monster_name = ff4struct.text.decode(rom.text_monster_names[monster_id])

        lines.append('monster(${:02X})   // {}'.format(monster_id, monster_name))
        lines.append('{')
        if monster.boss:
            lines.append("    boss")
        lines.append("    level {}".format(monster.level))
        lines.append("    hp {}".format(monster.hp))
        lines.append("    gp {}".format(rom.monster_gp[monster_id]))
        lines.append("    xp {}".format(rom.monster_xp[monster_id]))
        lines.append("    attack index ${:02X}         // {}".format(monster.attack_index, rom.monster_stats[monster.attack_index]))
        lines.append("    defense index ${:02X}        // {}".format(monster.defense_index, rom.monster_stats[monster.defense_index]))
        lines.append("    magic defense index ${:02X}  // {}".format(monster.magic_defense_index, rom.monster_stats[monster.magic_defense_index]))
        lines.append("    speed index ${:02X}          // {}".format(monster.speed_index, rom.monster_speeds[monster.speed_index]))
        lines.append("    drop index ${:02X}".format(monster.drop_index))
        lines.append("    drop rate ${:02X}".format(monster.drop_rate))
        lines.append("    attack sequence ${:02X}".format(monster.attack_sequence))

        if monster.attack_elements:
            lines.append("    attack element {}".format(_get_elements_string(monster.attack_elements)))
        if monster.attack_statuses:
            lines.append("    attack status {}".format(_get_statuses_string(monster.attack_statuses)))
        if monster.resist_elements:
            lines.append("    resist element {}".format(_get_elements_string(monster.resist_elements)))
        if monster.resist_statuses:
            lines.append("    resist status {}".format(_get_statuses_string(monster.resist_statuses)))
        if monster.weak_elements:
            lines.append("    weak element {}".format(_get_elements_string(monster.weak_elements)))
        if monster.spell_power is not None:
            lines.append("    spell power {}".format(monster.spell_power))
        if monster.races:
            lines.append("    race {}".format(_get_races_string(monster.races)))
        if monster.reaction_sequence is not None:
            lines.append("    reaction sequence ${:02X}".format(monster.reaction_sequence))

        gfx = ff4struct.monster_gfx.decode(rom.monster_gfx[monster_id])
        lines.append("    gfx {")
        lines.append("        size ${:02X}".format(gfx.size))
        lines.append("        palette ${:02X}".format(gfx.palette))
        lines.append("        pointer ${:04X}".format(gfx.pointer))
        lines.append("    }")
        lines.append("}")
        lines.append('')

    return '\n'.join(lines)

def decompile_monster_stats(rom):
    lines = []

    for i,encoded in enumerate(rom.monster_stats):
        lines.append('monster_stat({}) {{ {:3}x {:3}% {:3} }}'.format(
            value_text(i), encoded[0], encoded[1], encoded[2]
            ))

    lines.append('')
    for i,encoded in enumerate(rom.monster_speeds):
        lines.append('monster_speed({}) {{ {:3} - {:3} }}'.format(
            value_text(i), encoded[0], encoded[1]
            ))

    return '\n'.join(lines)

