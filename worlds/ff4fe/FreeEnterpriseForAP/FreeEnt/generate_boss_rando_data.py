import sys
import os
import f4c

formations = [
    0xDE, 0xED, 0xDF, 0xE0, 0xEF, 0xE1, 0xF7, 0xF8, 0xF9,
    0xE2, 0xE3, 0xF6, 0xFA, 0xF2, 0xE4, 0xE5, 0xE7, 0xE8, 0xEA,
    0x1A7, 0x1B6, 0x1A9, 0x1B5, 0x100, 0xFE, 0xFF, 0x1AF,
    0x1B0, 0x1AD, 0x1AC, 0x1AE, 0xDC, 0xDD, 0x1FB, 0x1FC,
    0x1FE, 0x1FD, 0x1FA
    ]

rom = f4c.ff4bin.Rom('PATH-TO-ROM')
print('# This file is auto-generated, do not make manual edits')
print('FORMATION_DATA = {')
for fid in formations:
    print('    0x{:X} : {{'.format(fid))
    f = f4c.ff4struct.formation.decode(rom.formations[fid])

    monster_counts = {}
    for i,monster_type in enumerate(f.monster_types):
        if f.monster_qtys[i]:
            monster_counts.setdefault(monster_type, 0)
            monster_counts[monster_type] += f.monster_qtys[i]

    for monster_type in monster_counts:
        monster_qty = monster_counts[monster_type]
        monster_name = f4c.ff4struct.text.decode(rom.text_monster_names[monster_type])
        m = f4c.ff4struct.monster.decode(rom.monsters[monster_type])
        info = [
            ('name', f"'{monster_name.strip()}'"),
            ('qty', monster_qty),
            ('hp', m.hp),
            ('level', m.level),
            ('attack', rom.monster_stats[m.attack_index]),
            ('defense', rom.monster_stats[m.defense_index]),
            ('magic defense', rom.monster_stats[m.magic_defense_index]),
            ('speed', rom.monster_speeds[m.speed_index]),
            ('spell power', m.spell_power),
            ('xp', rom.monster_xp[monster_type]),
            ('gp', rom.monster_gp[monster_type]),
            ]

        info_string = ', '.join(["'{}' : {}".format(item[0], item[1]) for item in info])
        print("        0x{:X} : {{ {} }},  # {}".format(monster_type, info_string, monster_name))
    print("    },")
print('}')
print('')

print('STATS_TABLE = [')
for stat in rom.monster_stats:
    print('    {},'.format(stat))
print(']')
print('')

print('SPEED_TABLE = [')
for stat in rom.monster_speeds:
    print('    {},'.format(stat))
print(']')
print('')

