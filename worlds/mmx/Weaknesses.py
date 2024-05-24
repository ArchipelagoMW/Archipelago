from .Names import ItemName

WEAKNESS_UNCHARGED_DMG = 0x03
WEAKNESS_CHARGED_DMG = 0x05

boss_weaknesses = {
    "Sting Chameleon": [
        [[ItemName.boomerang_cutter], 0x0D, WEAKNESS_CHARGED_DMG],
        [[ItemName.boomerang_cutter], 0x16, WEAKNESS_CHARGED_DMG],
    ],
    "Storm Eagle": [
        [[ItemName.chameleon_sting], 0x08, WEAKNESS_UNCHARGED_DMG],
    ],
    "Flame Mammoth": [
        [[ItemName.storm_tornado], 0x0B, WEAKNESS_UNCHARGED_DMG],
        [[ItemName.storm_tornado], 0x14, WEAKNESS_CHARGED_DMG],
    ],
    "Chill Penguin": [
        [[ItemName.fire_wave], 0x0A, WEAKNESS_UNCHARGED_DMG],
        [[ItemName.fire_wave], 0x13, WEAKNESS_CHARGED_DMG+3],
    ],
    "Spark Mandrill": [
        [[ItemName.shotgun_ice], 0x0E, WEAKNESS_CHARGED_DMG],
        [[ItemName.shotgun_ice], 0x17, WEAKNESS_CHARGED_DMG+3],
    ],
    "Armored Armadillo":  [
        [[ItemName.electric_spark], 0x0C, WEAKNESS_UNCHARGED_DMG],
        [[ItemName.electric_spark], 0x15, WEAKNESS_CHARGED_DMG],
    ],
    "Launch Octopus": [
        [[ItemName.rolling_shield], 0x09, WEAKNESS_UNCHARGED_DMG],
        [[ItemName.rolling_shield], 0x12, WEAKNESS_CHARGED_DMG+2],
    ],
    "Boomer Kuwanger": [
        [[ItemName.homing_torpedo], 0x07, WEAKNESS_UNCHARGED_DMG],
        [[ItemName.homing_torpedo], 0x10, WEAKNESS_CHARGED_DMG],
    ],
    "Thunder Slimer": [
        [None, 0x00, 0x02],
        [None, 0x06, 0x04],
        [None, 0x01, 0x03],
        [None, 0x03, 0x04],
        [None, 0x02, 0x05],
        [None, 0x1D, 0x02],
    ],
    "Vile": [
        [[ItemName.homing_torpedo], 0x07, WEAKNESS_UNCHARGED_DMG],
        [[ItemName.homing_torpedo], 0x10, WEAKNESS_CHARGED_DMG],
    ],
    "Bospider": [
        [[ItemName.shotgun_ice], 0x0E, WEAKNESS_CHARGED_DMG],
        [[ItemName.shotgun_ice], 0x17, WEAKNESS_CHARGED_DMG+3],
    ],
    "Rangda Bangda": [
        [[ItemName.chameleon_sting], 0x08, WEAKNESS_UNCHARGED_DMG],
    ],
    "D-Rex": [
        [[ItemName.boomerang_cutter], 0x0D, WEAKNESS_CHARGED_DMG],
        [[ItemName.boomerang_cutter], 0x16, WEAKNESS_CHARGED_DMG],
    ],
    "Velguarder": [
        [[ItemName.shotgun_ice], 0x0E, WEAKNESS_CHARGED_DMG],
        [[ItemName.shotgun_ice], 0x17, WEAKNESS_CHARGED_DMG+3],
    ],
    "Sigma":  [
        [[ItemName.electric_spark], 0x0C, WEAKNESS_UNCHARGED_DMG],
        [[ItemName.electric_spark], 0x15, WEAKNESS_CHARGED_DMG],
    ],
    "Wolf Sigma": [
        [["Check Charge 2"], 0x02, 0x05],
        [["Check Charge 2"], 0x1D, 0x02],
        [[ItemName.rolling_shield], 0x09, WEAKNESS_UNCHARGED_DMG],
        [[ItemName.rolling_shield], 0x12, WEAKNESS_CHARGED_DMG+2],
    ],
}

weapon_id = {
    0x00: "Lemon",
    0x01: "Charged Shot (Level 1)",
    0x02: "Charged Shot (Level 3, Bullet Stream)",
    0x03: "Charged Shot (Level 2)",
    0x04: "Hadouken",
    0x06: "Lemon (Dash)",
    0x07: "Uncharged Homing Torpedo",
    0x08: "Uncharged Chameleon Sting",
    0x09: "Uncharged Rolling Shield",
    0x0A: "Uncharged Fire Wave",
    0x0B: "Uncharged Storm Tornado",
    0x0C: "Uncharged Electric Spark",
    0x0D: "Uncharged Boomerang Cutter",
    0x0E: "Uncharged Shotgun Ice",
    0x10: "Charged Homing Torpedo",
    0x12: "Charged Rolling Shield",
    0x13: "Charged Fire Wave",
    0x14: "Charged Storm Tornado",
    0x15: "Charged Electric Spark",
    0x16: "Charged Boomerang Cutter",
    0x17: "Charged Shotgun Ice",
    0x1D: "Charged Shot (Level 3, Shockwave)",
}

damage_templates = {
    "Allow Buster": [
        0x01,0x02,0x03,0x03,0x20,0x00,0x02,0x80,
        0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,
        0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,
        0x80,0x80,0x80,0x7F,0x80,0x01
    ],
    "Allow Upgraded Buster": [
        0x80,0x80,0x80,0x03,0x20,0x00,0x80,0x80,
        0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,
        0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,
        0x80,0x80,0x80,0x7F,0x80,0x01
    ],
    "Only Weakness": [
        0x80,0x80,0x80,0x80,0x20,0x00,0x80,0x80,
        0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,
        0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,
        0x80,0x80,0x80,0x7F,0x80,0x80
    ],
}

boss_weakness_data = {
    "Sting Chameleon": [
        0x01,0x01,0x02,0x02,0x20,0x02,0x02,0x01,
        0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,
        0x02,0x00,0x02,0x02,0x02,0x02,0x02,0x02,
        0x01,0x01,0x01,0x7F,0x01,0x01
    ],
    "Storm Eagle": [
        0x01,0x01,0x02,0x02,0x20,0x02,0x02,0x01,
        0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,
        0x02,0x00,0x02,0x02,0x02,0x02,0x02,0x02,
        0x01,0x01,0x01,0x7F,0x01,0x01
    ],
    "Flame Mammoth": [
        0x01,0x01,0x02,0x02,0x20,0x02,0x02,0x01,
        0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,
        0x02,0x00,0x02,0x02,0x02,0x02,0x02,0x02,
        0x01,0x01,0x01,0x7F,0x01,0x01
    ],
    "Chill Penguin": [
        0x01,0x02,0x03,0x03,0x20,0x02,0x02,0x01,
        0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,
        0x02,0x00,0x02,0x02,0x02,0x02,0x02,0x02,
        0x01,0x01,0x01,0x7F,0x01,0x01
    ],
    "Spark Mandrill": [
        0x01,0x02,0x03,0x03,0x20,0x02,0x02,0x01,
        0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,
        0x02,0x00,0x02,0x02,0x02,0x02,0x02,0x02,
        0x01,0x01,0x01,0x7F,0x01,0x01
    ],
    "Armored Armadillo": [
        0x01,0x01,0x01,0x01,0x20,0x02,0x02,0x01,
        0x01,0x01,0x00,0x00,0x01,0x01,0x01,0x01,
        0x02,0x02,0x02,0x02,0x02,0x02,0x02,0x02,
        0x01,0x01,0x01,0x7F,0x01,0x01
    ],
    "Launch Octopus": [
        0x01,0x02,0x03,0x03,0x20,0x02,0x02,0x01,
        0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,
        0x02,0x02,0x02,0x02,0x02,0x02,0x02,0x02,
        0x01,0x01,0x01,0x7F,0x01,0x01
    ],
    "Boomer Kuwanger": [
        0x01,0x02,0x03,0x03,0x20,0x02,0x02,0x01,
        0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,
        0x02,0x02,0x02,0x02,0x02,0x02,0x02,0x02,
        0x01,0x01,0x01,0x7F,0x01,0x01
    ],
    "Thunder Slimer": [
        0x01,0x02,0x04,0x04,0x20,0x04,0x02,0x02,
        0x02,0x02,0x01,0x01,0x02,0x02,0x02,0x02,
        0x03,0x00,0x04,0x01,0x04,0x06,0x06,0x04,
        0x04,0x05,0x0A,0x7F,0x10,0x01
    ],
    "Vile": [
        0x01,0x02,0x04,0x04,0x20,0x04,0x02,0x02,
        0x02,0x02,0x01,0x01,0x02,0x02,0x02,0x02,
        0x03,0x00,0x04,0x01,0x04,0x06,0x06,0x06,
        0x04,0x05,0x0A,0x7F,0x10,0x01
    ],
    "Bospider": [
        0x01,0x02,0x03,0x03,0x20,0x02,0x02,0x01,
        0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,
        0x02,0x00,0x02,0x02,0x02,0x02,0x02,0x02,
        0x01,0x01,0x01,0x7F,0x01,0x01
    ],
    "Rangda Bangda": [
        0x01,0x01,0x02,0x02,0x20,0x02,0x02,0x01,
        0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,
        0x02,0x00,0x02,0x02,0x02,0x02,0x02,0x02,
        0x01,0x01,0x01,0x7F,0x01,0x01
    ],
    "D-Rex": [
        0x01,0x01,0x02,0x02,0x20,0x02,0x02,0x01,
        0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,
        0x02,0x00,0x02,0x02,0x02,0x02,0x02,0x02,
        0x01,0x01,0x01,0x7F,0x01,0x01
    ],
    "Velguarder": [
        0x01,0x02,0x03,0x03,0x20,0x02,0x02,0x01,
        0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,
        0x02,0x00,0x02,0x02,0x02,0x02,0x02,0x02,
        0x01,0x01,0x01,0x7F,0x01,0x01
    ],
    "Sigma": [
        0x01,0x01,0x01,0x01,0x20,0x01,0x01,0x01,
        0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,
        0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,
        0x01,0x01,0x01,0x01,0x01,0x01
    ],
    "Wolf Sigma": [
        0x80,0x80,0x01,0x80,0x80,0x80,0x80,0x80,
        0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,
        0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,
        0x80,0x80,0x80,0x80,0x80,0x01
    ],
}

boss_excluded_weapons = {
    "Sting Chameleon": [
    ],
    "Storm Eagle": [
    ],
    "Flame Mammoth": [
    ],
    "Chill Penguin": [
    ],
    "Spark Mandrill": [
    ],
    "Armored Armadillo": [
    ],
    "Launch Octopus": [
        "Fire Wave",
    ],
    "Boomer Kuwanger": [
    ],
    "Thunder Slimer": [
    ],
    "Vile": [
    ],
    "Bospider": [
    ],
    "Rangda Bangda": [
    ],
    "D-Rex": [
    ],
    "Velguarder": [
    ],
    "Sigma": [
        "Charged Rolling Shield",
    ],
    "Wolf Sigma": [
    ],
}

weapons = {
    "Buster": [
        [None, 0x00, 0x02],
        [None, 0x06, 0x04],
        [None, 0x01, 0x03],
        [None, 0x03, 0x04],
        [None, 0x02, 0x05],
        [None, 0x1D, 0x02],
    ],
    "Homing Torpedo": [
        [[ItemName.homing_torpedo], 0x07, WEAKNESS_UNCHARGED_DMG],
        [[ItemName.homing_torpedo], 0x10, WEAKNESS_CHARGED_DMG],
    ],
    "Chameleon Sting": [
        [[ItemName.chameleon_sting], 0x08, WEAKNESS_UNCHARGED_DMG],
    ],
    "Rolling Shield": [
        [[ItemName.rolling_shield], 0x09, WEAKNESS_UNCHARGED_DMG],
        [[ItemName.rolling_shield], 0x12, WEAKNESS_CHARGED_DMG+2],
    ],
    "Fire Wave": [
        [[ItemName.fire_wave], 0x0A, WEAKNESS_UNCHARGED_DMG],
        [[ItemName.fire_wave], 0x13, WEAKNESS_CHARGED_DMG+3],
    ],
    "Storm Tornado": [
        [[ItemName.storm_tornado], 0x0B, WEAKNESS_UNCHARGED_DMG],
        [[ItemName.storm_tornado], 0x14, WEAKNESS_CHARGED_DMG],
    ],
    "Electric Spark": [
        [[ItemName.electric_spark], 0x0C, WEAKNESS_UNCHARGED_DMG],
        [[ItemName.electric_spark], 0x15, WEAKNESS_CHARGED_DMG],
    ],
    "Boomerang Cutter": [
        [[ItemName.boomerang_cutter], 0x0D, WEAKNESS_CHARGED_DMG],
        [[ItemName.boomerang_cutter], 0x16, WEAKNESS_CHARGED_DMG],
    ],
    "Shotgun Ice": [
        [[ItemName.shotgun_ice], 0x0E, WEAKNESS_CHARGED_DMG],
        [[ItemName.shotgun_ice], 0x17, WEAKNESS_CHARGED_DMG+3],
    ],
}

weapons_chaotic = {
    "Lemon": [
        [None, 0x00, 0x02],
    ],
    "Lemon (Dash)": [
        [["Check Dash"], 0x06, 0x03],
    ],
    "Charged Shot (Level 1)": [
        [["Check Charge 1"], 0x01, 0x03],
    ],
    "Charged Shot (Level 2)": [
        [["Check Charge 1"], 0x03, 0x04],
    ],
    "Charged Shot (Level 3)": [
        [["Check Charge 2"], 0x02, 0x05],
        [["Check Charge 2"], 0x1D, 0x02],
    ],
    "Homing Torpedo": [
        [[ItemName.homing_torpedo], 0x07, WEAKNESS_UNCHARGED_DMG],
    ],
    "Charged Homing Torpedo": [
        [["Check Charge 2", ItemName.homing_torpedo], 0x10, WEAKNESS_CHARGED_DMG],
    ],
    "Chameleon Sting": [
        [[ItemName.chameleon_sting], 0x08, WEAKNESS_UNCHARGED_DMG],
    ],
    "Rolling Shield": [
        [[ItemName.rolling_shield], 0x09, WEAKNESS_UNCHARGED_DMG+1],
    ],
    "Charged Rolling Shield": [
        [["Check Charge 2", ItemName.rolling_shield], 0x12, WEAKNESS_CHARGED_DMG+2],
    ],
    "Fire Wave": [
        [[ItemName.fire_wave], 0x0A, WEAKNESS_UNCHARGED_DMG],
        [[ItemName.fire_wave], 0x13, WEAKNESS_CHARGED_DMG+3],
    ],
    "Storm Tornado": [
        [[ItemName.storm_tornado], 0x0B, WEAKNESS_UNCHARGED_DMG],
    ],
    "Charged Storm Tornado": [
        [["Check Charge 2", ItemName.storm_tornado], 0x14, WEAKNESS_CHARGED_DMG],
    ],
    "Electric Spark": [
        [[ItemName.electric_spark], 0x0C, WEAKNESS_UNCHARGED_DMG],
    ],
    "Charged Electric Spark": [
        [["Check Charge 2", ItemName.electric_spark], 0x15, WEAKNESS_CHARGED_DMG],
    ],
    "Boomerang Cutter": [
        [[ItemName.boomerang_cutter], 0x0D, WEAKNESS_UNCHARGED_DMG],
    ],
    "Charged Boomerang Cutter": [
        [["Check Charge 2", ItemName.boomerang_cutter], 0x16, WEAKNESS_CHARGED_DMG],
    ],
    "Shotgun Ice": [
        [[ItemName.shotgun_ice], 0x0E, WEAKNESS_UNCHARGED_DMG],
    ],
    "Charged Shotgun Ice": [
        [["Check Charge 2", ItemName.shotgun_ice], 0x17, WEAKNESS_CHARGED_DMG+3],
    ],
}


def handle_weaknesses(world):
    shuffle_type = world.options.boss_weakness_rando.value
    strictness_type = world.options.boss_weakness_strictness.value

    if shuffle_type != "vanilla":
        weapon_list = weapons.keys()
        if shuffle_type == 2 or shuffle_type == 3:
            weapon_list = weapons_chaotic.keys()
        weapon_list = list(weapon_list)
    
    for boss in boss_weaknesses.keys():
        world.boss_weaknesses[boss] = []

        if strictness_type == 0:
            damage_table = boss_weakness_data[boss].copy()
        elif strictness_type == 1:
            damage_table = damage_templates["Allow Buster"].copy()
        elif strictness_type == 2:
            damage_table = damage_templates["Allow Upgraded Buster"].copy()
        else:
            damage_table = damage_templates["Only Weakness"].copy()

        if shuffle_type != "vanilla":
            copied_weapon_list = weapon_list.copy()
            for weapon in boss_excluded_weapons[boss]:
                if weapon in copied_weapon_list:
                    copied_weapon_list.remove(weapon)

        if shuffle_type == 1:
            chosen_weapon = world.random.choice(copied_weapon_list)
            data = weapons[chosen_weapon]
            for entry in data:
                world.boss_weaknesses[boss].append(entry)
                damage = entry[2]
                damage_table[entry[1]] = damage
            world.boss_weakness_data[boss] = damage_table.copy()

        elif shuffle_type == 2:
            for _ in range(2):
                chosen_weapon = world.random.choice(copied_weapon_list)
                data = weapons_chaotic[chosen_weapon].copy()
                copied_weapon_list.remove(chosen_weapon)
                for entry in data:
                    world.boss_weaknesses[boss].append(entry)
                    damage = entry[2]
                    damage_table[entry[1]] = damage
            world.boss_weakness_data[boss] = damage_table.copy()

        elif shuffle_type == 3:
            chosen_weapon = world.random.choice(copied_weapon_list)
            data = weapons_chaotic[chosen_weapon].copy()
            for entry in data:
                world.boss_weaknesses[boss].append(entry)
                damage = entry[2]
                damage_table[entry[1]] = damage
            world.boss_weakness_data[boss] = damage_table.copy()

        else:
            for entry in boss_weaknesses[boss]:
                world.boss_weaknesses[boss].append(entry)
                damage = entry[2]
                damage_table[entry[1]] = damage
