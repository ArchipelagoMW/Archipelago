from .enemy_attributes import excluded_enemies


class EnemyStatCopy:
    def __init__(self, hp, exp, money, speed, offense, defense, level, guts, luck):
        self.hp = hp
        self.exp = exp
        self.money = money
        self.speed = speed
        self.offense = offense
        self.defense = defense
        self.level = level
        self.guts = guts
        self.luck = luck


def randomize_enemy_stats(world, rom) -> None:
    stat_copies = {}
    for enemy in world.enemies:
        if enemy not in excluded_enemies:
            stat_copies[enemy] = EnemyStatCopy(
                hp=world.enemies[enemy].hp,
                exp=world.enemies[enemy].exp,
                money=world.enemies[enemy].money,
                speed=world.enemies[enemy].speed,
                offense=world.enemies[enemy].offense,
                defense=world.enemies[enemy].defense,
                level=world.enemies[enemy].level,
                guts=world.enemies[enemy].guts,
                luck=world.enemies[enemy].luck
            )

    for enemy in world.enemies:
        if enemy not in excluded_enemies:
            copied_stat_base = world.random.choice(list(stat_copies))
            world.enemies[enemy].hp = stat_copies[copied_stat_base].hp
            if world.random.randint(1, 100) < 20:
                world.enemies[enemy].pp = int(world.random.randint(10, 500) / 2)
            else:
                world.enemies[enemy].pp = 0
            world.enemies[enemy].offense = stat_copies[copied_stat_base].offense
            world.enemies[enemy].defense = stat_copies[copied_stat_base].defense
            world.enemies[enemy].speed = stat_copies[copied_stat_base].speed
            world.enemies[enemy].level = stat_copies[copied_stat_base].level
            world.enemies[enemy].exp = stat_copies[copied_stat_base].exp
            world.enemies[enemy].money = stat_copies[copied_stat_base].money
            world.enemies[enemy].guts = stat_copies[copied_stat_base].guts
            world.enemies[enemy].luck = stat_copies[copied_stat_base].luck
            rom.write_bytes(world.enemies[enemy].address + 0x3D, bytearray([world.enemies[enemy].guts]))
            rom.write_bytes(world.enemies[enemy].address + 0x3E, bytearray([world.enemies[enemy].luck]))
            if world.enemies[enemy].attack_extensions > 0:
                world.enemies[f"{enemy} (2)"].hp = world.enemies[enemy].hp
                world.enemies[f"{enemy} (2)"].pp = world.enemies[enemy].pp
                world.enemies[f"{enemy} (2)"].offense = world.enemies[enemy].offense
                world.enemies[f"{enemy} (2)"].defense = world.enemies[enemy].defense
                world.enemies[f"{enemy} (2)"].speed = world.enemies[enemy].speed
                world.enemies[f"{enemy} (2)"].level = world.enemies[enemy].level
                world.enemies[f"{enemy} (2)"].exp = world.enemies[enemy].exp
                world.enemies[f"{enemy} (2)"].money = world.enemies[enemy].money
                rom.write_bytes(world.enemies[f"{enemy} (2)"].address + 0x3D, bytearray([world.enemies[enemy].guts]))
                rom.write_bytes(world.enemies[f"{enemy} (2)"].address + 0x3E, bytearray([world.enemies[enemy].luck]))
                