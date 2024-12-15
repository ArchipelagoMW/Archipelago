from ... import f4c

rom = f4c.ff4bin.Rom('PATH-TO-ROM')

results = []
for formation_index in range(0x200):
    formation = f4c.ff4struct.formation.decode(rom.formations[formation_index])

    relevant_indices = [0, 1, 2]
    if formation.transforming:
        relevant_indices.pop()
        if formation.calling:
            relevant_indices.pop()
    elif formation.calling:
        relevant_indices.remove(1)


    enemy_levels = []
    has_boss = False
    for i in relevant_indices:
        if formation.monster_qtys[i]:
            monster_id = formation.monster_types[i]
            monster = f4c.ff4struct.monster.decode(rom.monsters[monster_id])
            enemy_levels.extend([monster.level] * formation.monster_qtys[i])
            if monster.boss:
                has_boss = True

    if (not enemy_levels) or has_boss:
        results.append(0)
    else:
        avg_enemy_level = sum(enemy_levels) // len(enemy_levels)
        results.append(avg_enemy_level)

    if (has_boss):
        print(f'Formation {formation_index:03X} - is boss')

with open('formation_average_levels.bin', 'wb') as outfile:
    outfile.write(bytes(results))
