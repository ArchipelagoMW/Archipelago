from . import ff4struct

def decompile_formations(rom):
    lines = []
    for formation_id,encoded_formation in enumerate(rom.formations):
        formation = ff4struct.formation.decode(encoded_formation)

        lines.append('formation(${:02X})'.format(formation_id))
        lines.append('{')

        lines.append('    monsters {')
        for i in range(3):
            if formation.monster_types[i] == 0xFF:
                for later_type in formation.monster_types[i+1:]:
                    if later_type != 0xFF:
                        lines.append('        none')
                        break
            else:
                monster_name = ff4struct.text.decode(rom.text_monster_names[formation.monster_types[i]])
                lines.append('        ${:02X} x {}   // {}'.format(
                    formation.monster_types[i],
                    formation.monster_qtys[i],
                    monster_name
                    ))
        lines.append('    }')

        if formation.calling:
            lines.append("    calling")

        if formation.transforming:
            lines.append("    transforming")

        lines.append('    arrangement ${:02X}'.format(formation.arrangement))

        if formation.back_attack:
            lines.append("    back attack")

        if formation.boss_death:
            lines.append("    boss death")

        if True in formation.eggs:
            eggs_str = ' '.join(['yes' if b else 'no' for b in formation.eggs])
            lines.append("    eggs ({})".format(eggs_str))

        if formation.no_flee:
            lines.append("    can't run")
        if formation.no_gameover:
            lines.append("    no gameover")

        if formation.music == ff4struct.formation.BOSS_MUSIC:
            lines.append("    boss music")
        elif formation.music == ff4struct.formation.FIEND_MUSIC:
            lines.append("    fiend music")
        elif formation.music == ff4struct.formation.CONTINUE_MUSIC:
            lines.append("    continue music")
        
        if formation.character_battle:
            lines.append("    character battle")

        if formation.auto_battle:
            lines.append("    auto battle")

        if formation.floating_enemies:
            lines.append("    floating enemies")

        if formation.transparent:
            lines.append("    transparent")

        lines.append("    gfx bits {}".format(formation.gfx_bits))
        
        lines.append("    cursor graph ${:02X}".format(formation.cursor_graph_index))

        lines.append("}")
        lines.append("")

    return '\n'.join(lines)
