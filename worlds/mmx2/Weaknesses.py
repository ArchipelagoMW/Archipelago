from .Names import LocationName, ItemName, RegionName, EventName

WEAKNESS_UNCHARGED_DMG = 0x03
WEAKNESS_CHARGED_DMG = 0x05

boss_weaknesses = {
    "Wheel Gator": [
        [[ItemName.strike_chain], 0x0C, WEAKNESS_UNCHARGED_DMG],
        [[ItemName.strike_chain], 0x15, WEAKNESS_CHARGED_DMG],
    ],
    "Bubble Crab": [
        [[ItemName.spin_wheel], 0x0A, WEAKNESS_UNCHARGED_DMG],
        [[ItemName.spin_wheel], 0x13, WEAKNESS_CHARGED_DMG],
    ],
    "Flame Stag": [
        [[ItemName.bubble_splash], 0x08, WEAKNESS_UNCHARGED_DMG],
        [[ItemName.bubble_splash], 0x11, WEAKNESS_CHARGED_DMG],
    ],
    "Morph Moth": [
        [[ItemName.speed_burner], 0x0E, WEAKNESS_UNCHARGED_DMG],
        [[ItemName.speed_burner], 0x17, WEAKNESS_CHARGED_DMG],
    ],
    "Magna Centipede": [
        [[ItemName.silk_shot], 0x1B, WEAKNESS_UNCHARGED_DMG],
        [[ItemName.silk_shot], 0x20, WEAKNESS_CHARGED_DMG],
    ],
    "Crystal Snail": [
        [[ItemName.magnet_mine], 0x0D, WEAKNESS_UNCHARGED_DMG],
        [[ItemName.magnet_mine], 0x16, WEAKNESS_CHARGED_DMG],
    ],
    "Overdrive Ostrich": [
        [[ItemName.crystal_hunter], 0x07, WEAKNESS_UNCHARGED_DMG],
    ],
    "Wire Sponge": [
        [[ItemName.sonic_slicer], 0x0B, WEAKNESS_UNCHARGED_DMG],
        [[ItemName.sonic_slicer], 0x14, WEAKNESS_CHARGED_DMG],
    ],
    "Magna Quartz": [
        [None, 0x00, 0x02],
        [None, 0x01, 0x03],
        [None, 0x03, 0x04],
        [None, 0x06, 0x03],
        [None, 0x1D, 0x02],
    ],
    "Chop Register": [
        [None, 0x00, 0x02],
        [None, 0x01, 0x03],
        [None, 0x03, 0x04],
        [None, 0x06, 0x03],
        [None, 0x1D, 0x02],
    ],
    "Raider Killer": [
        [None, 0x00, 0x02],
        [None, 0x01, 0x03],
        [None, 0x03, 0x04],
        [None, 0x06, 0x03],
        [None, 0x1D, 0x02],
    ],
    "Pararoid S-38": [
        [None, 0x00, 0x02],
        [None, 0x01, 0x03],
        [None, 0x03, 0x04],
        [None, 0x06, 0x03],
        [None, 0x1D, 0x02],
    ],
    "Agile": [
        [[ItemName.magnet_mine], 0x0D, WEAKNESS_UNCHARGED_DMG],
        [[ItemName.magnet_mine], 0x16, WEAKNESS_CHARGED_DMG],
    ],
    "Serges": [
        [[ItemName.sonic_slicer], 0x0B, WEAKNESS_UNCHARGED_DMG],
        [[ItemName.sonic_slicer], 0x14, WEAKNESS_CHARGED_DMG],
    ],
    "Violen": [
        [[ItemName.bubble_splash], 0x08, WEAKNESS_UNCHARGED_DMG],
        [[ItemName.bubble_splash], 0x11, WEAKNESS_CHARGED_DMG],
    ],
    "Neo Violen": [
        [[ItemName.bubble_splash], 0x08, WEAKNESS_UNCHARGED_DMG],
        [[ItemName.bubble_splash], 0x11, WEAKNESS_CHARGED_DMG],
    ],
    "Serges Tank": [
        [[ItemName.silk_shot], 0x1B, WEAKNESS_UNCHARGED_DMG],
        [[ItemName.silk_shot], 0x20, WEAKNESS_CHARGED_DMG],
    ],
    "Agile Flyer": [
        [[ItemName.magnet_mine], 0x0D, WEAKNESS_UNCHARGED_DMG],
        [[ItemName.magnet_mine], 0x16, WEAKNESS_CHARGED_DMG],
    ],
    "Zero": [
        [[ItemName.speed_burner], 0x0E, WEAKNESS_UNCHARGED_DMG],
        [[ItemName.speed_burner], 0x17, WEAKNESS_CHARGED_DMG],
    ],
    "Sigma": [
        [[ItemName.sonic_slicer], 0x0B, WEAKNESS_UNCHARGED_DMG],
        [[ItemName.sonic_slicer], 0x14, WEAKNESS_CHARGED_DMG],
    ],
    "Sigma Virus": [
        [[ItemName.strike_chain], 0x0C, WEAKNESS_UNCHARGED_DMG],
        [[ItemName.strike_chain], 0x15, WEAKNESS_CHARGED_DMG],
    ],
}

weapon_id = {
    0x00: "Lemon",
    0x01: "Charged Shot (Level 1)",
    0x03: "Charged Shot (Level 2)",
    0x04: "Shoryuken",
    0x06: "Lemon (Dash)",
    0x07: "Uncharged Crystal Hunter",
    0x08: "Uncharged Bubble Splash",
    0x09: "Uncharged Silk Shot (Rocks)",
    0x0A: "Uncharged Spin Wheel",
    0x0B: "Uncharged Sonic Slicer",
    0x0C: "Uncharged Strike Chain",
    0x0D: "Uncharged Magnet Mine",
    0x0E: "Uncharged Speed Burner",
    0x0F: "Uncharged Giga Crush",
    0x11: "Charged Bubble Splash",
    0x12: "Charged Silk Shot (Rocks)",
    0x13: "Charged Spin Wheel",
    0x14: "Charged Sonic Slicer",
    0x15: "Charged Strike Chain",
    0x16: "Charged Magnet Mine",
    0x17: "Charged Speed Burner",
    0x18: "Uncharged Silk Shot (Black Rock)",
    0x1B: "Uncharged Silk Shot (Junk)",
    0x1C: "Uncharged Silk Shot (Leaves)",
    0x1D: "Charged Shot (Level 3)",
    0x1E: "Uncharged Silk Shot (Crystals)",
    0x1F: "Charged Silk Shot (Black Rock)",
    0x20: "Charged Silk Shot (Junk)",
    0x21: "Charged Silk Shot (Leaves)",
    0x22: "Charged Silk Shot (Crystals)",
    0x23: "Uncharged Speed Burner (Underwater)",
}

damage_templates = {
    "Allow Buster": [
        0x01, 0x01, 0x01, 0x02, 0x10, 0x01, 0x02, 0x80,
        0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x03,
        0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80,
        0x80, 0x80, 0x80, 0x80, 0x80, 0x03, 0x80, 0x80,
        0x80, 0x80, 0x80, 0x80, 0x80, 0x80,
    ],
    "Allow Upgraded Buster": [
        0x80, 0x80, 0x80, 0x80, 0x08, 0x80, 0x80, 0x80,
        0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x03,
        0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80,
        0x80, 0x80, 0x80, 0x80, 0x80, 0x03, 0x80, 0x80,
        0x80, 0x80, 0x80, 0x80, 0x80, 0x80,
    ],
    "Only Weakness": [
        0x80, 0x80, 0x80, 0x80, 0x08, 0x80, 0x80, 0x80,
        0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x03,
        0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80,
        0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80,
        0x80, 0x80, 0x80, 0x80, 0x80, 0x80,
    ],
}

boss_weakness_data = {
    "Wheel Gator": [
        0x01, 0x01, 0x01, 0x02, 0x10, 0x02, 0x02, 0x80,
        0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x03,
        0x80, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02,
        0x01, 0x01, 0x01, 0x01, 0x01, 0x03, 0x01, 0x01,
        0x01, 0x01, 0x01, 0x01, 0x01, 0x01,
    ],
    "Bubble Crab": [
        0x01, 0x01, 0x01, 0x02, 0x10, 0x02, 0x02, 0x80,
        0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x03,
        0x80, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02,
        0x01, 0x01, 0x01, 0x01, 0x01, 0x03, 0x01, 0x01,
        0x01, 0x01, 0x01, 0x01, 0x01, 0x01,
    ],
    "Flame Stag": [
        0x01, 0x01, 0x01, 0x02, 0x10, 0x02, 0x02, 0x80,
        0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x03,
        0x80, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02,
        0x01, 0x01, 0x01, 0x01, 0x01, 0x03, 0x01, 0x01,
        0x01, 0x01, 0x01, 0x01, 0x01, 0x01,
    ],
    "Morph Moth": [
        0x01, 0x01, 0x01, 0x02, 0x10, 0x02, 0x02, 0x80,
        0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x03,
        0x80, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02,
        0x01, 0x01, 0x01, 0x01, 0x01, 0x03, 0x01, 0x01,
        0x01, 0x01, 0x01, 0x01, 0x01, 0x01,
    ],
    "Magna Centipede": [
        0x01, 0x01, 0x01, 0x02, 0x10, 0x02, 0x02, 0x80,
        0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x03,
        0x80, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02,
        0x01, 0x01, 0x01, 0x01, 0x01, 0x03, 0x01, 0x01,
        0x01, 0x01, 0x01, 0x01, 0x01, 0x01,
    ],
    "Crystal Snail": [
        0x01, 0x01, 0x01, 0x02, 0x10, 0x02, 0x02, 0x80,
        0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x03,
        0x80, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02,
        0x01, 0x01, 0x01, 0x01, 0x01, 0x03, 0x01, 0x01,
        0x01, 0x01, 0x01, 0x01, 0x01, 0x01,
    ],
    "Overdrive Ostrich": [
        0x01, 0x01, 0x01, 0x02, 0x10, 0x02, 0x02, 0x80,
        0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x03,
        0x80, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02,
        0x01, 0x01, 0x01, 0x01, 0x01, 0x03, 0x01, 0x01,
        0x01, 0x01, 0x01, 0x01, 0x01, 0x01,
    ],
    "Wire Sponge": [
        0x01, 0x01, 0x01, 0x02, 0x10, 0x02, 0x02, 0x80,
        0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x03,
        0x80, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02,
        0x01, 0x01, 0x01, 0x01, 0x01, 0x03, 0x01, 0x01,
        0x01, 0x01, 0x01, 0x01, 0x01, 0x01,
    ],
    "Magna Quartz": [
        0x01, 0x01, 0x01, 0x02, 0x10, 0x02, 0x02, 0x80,
        0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x03,
        0x80, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02,
        0x01, 0x01, 0x01, 0x01, 0x01, 0x03, 0x01, 0x01,
        0x01, 0x01, 0x01, 0x01, 0x01, 0x01,
    ],
    "Chop Register": [
        0x01, 0x01, 0x01, 0x02, 0x10, 0x02, 0x02, 0x80,
        0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x03,
        0x80, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02,
        0x01, 0x01, 0x01, 0x01, 0x01, 0x03, 0x01, 0x01,
        0x01, 0x01, 0x01, 0x01, 0x01, 0x01,
    ],
    "Raider Killer": [
        0x01, 0x01, 0x01, 0x02, 0x10, 0x02, 0x02, 0x80,
        0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x03,
        0x80, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02,
        0x01, 0x01, 0x01, 0x01, 0x01, 0x03, 0x01, 0x01,
        0x01, 0x01, 0x01, 0x01, 0x01, 0x01,
    ],
    "Pararoid S-38": [
        0x01, 0x01, 0x01, 0x02, 0x10, 0x02, 0x02, 0x80,
        0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x03,
        0x80, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02,
        0x01, 0x01, 0x01, 0x01, 0x01, 0x03, 0x01, 0x01,
        0x01, 0x01, 0x01, 0x01, 0x01, 0x01,
    ],
    "Agile": [
        0x01, 0x01, 0x01, 0x02, 0x10, 0x02, 0x02, 0x80,
        0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x03,
        0x80, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02,
        0x01, 0x01, 0x01, 0x01, 0x01, 0x03, 0x01, 0x01,
        0x01, 0x01, 0x01, 0x01, 0x01, 0x01,
    ],
    "Serges": [
        0x01, 0x01, 0x01, 0x02, 0x10, 0x02, 0x02, 0x80,
        0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x03,
        0x80, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02,
        0x01, 0x01, 0x01, 0x01, 0x01, 0x03, 0x01, 0x01,
        0x01, 0x01, 0x01, 0x01, 0x01, 0x01,
    ],
    "Violen": [
        0x01, 0x01, 0x01, 0x02, 0x10, 0x02, 0x02, 0x80,
        0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x03,
        0x80, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02,
        0x01, 0x01, 0x01, 0x01, 0x01, 0x03, 0x01, 0x01,
        0x01, 0x01, 0x01, 0x01, 0x01, 0x01,
    ],
    "Neo Violen": [
        0x01, 0x01, 0x01, 0x02, 0x10, 0x02, 0x02, 0x80,
        0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x03,
        0x80, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02,
        0x01, 0x01, 0x01, 0x01, 0x01, 0x03, 0x01, 0x01,
        0x01, 0x01, 0x01, 0x01, 0x01, 0x01,
    ],
    "Serges Tank": [
        0x01, 0x01, 0x01, 0x02, 0x10, 0x02, 0x02, 0x80,
        0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x03,
        0x80, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02,
        0x01, 0x01, 0x01, 0x01, 0x01, 0x03, 0x01, 0x01,
        0x01, 0x01, 0x01, 0x01, 0x01, 0x01,
    ],
    "Agile Flyer": [
        0x01, 0x01, 0x01, 0x02, 0x10, 0x02, 0x02, 0x80,
        0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x03,
        0x80, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02,
        0x01, 0x01, 0x01, 0x01, 0x01, 0x03, 0x01, 0x01,
        0x01, 0x01, 0x01, 0x01, 0x01, 0x01,
    ],
    "Zero": [
        0x01, 0x01, 0x01, 0x02, 0x10, 0x02, 0x02, 0x80,
        0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x03,
        0x80, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02,
        0x01, 0x01, 0x01, 0x01, 0x01, 0x03, 0x01, 0x01,
        0x01, 0x01, 0x01, 0x01, 0x01, 0x01,
    ],
    "Sigma": [
        0x01, 0x01, 0x01, 0x02, 0x10, 0x02, 0x02, 0x80,
        0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x03,
        0x80, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02,
        0x01, 0x01, 0x01, 0x01, 0x01, 0x03, 0x01, 0x01,
        0x01, 0x01, 0x01, 0x01, 0x01, 0x01,
    ],
    "Sigma Virus": [
        0x01, 0x01, 0x01, 0x02, 0x10, 0x02, 0x02, 0x80,
        0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x03,
        0x80, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02,
        0x01, 0x01, 0x01, 0x01, 0x01, 0x03, 0x01, 0x01,
        0x01, 0x01, 0x01, 0x01, 0x01, 0x01,
    ],
}

boss_excluded_weapons = {
    "Wheel Gator": [
        "Speed Burner (Underwater)",
    ],
    "Bubble Crab": [
        "Speed Burner",
        "Charged Speed Burner",
    ],
    "Flame Stag": [
        "Speed Burner (Underwater)",
    ],
    "Morph Moth": [
        "Speed Burner (Underwater)",
    ],
    "Magna Centipede": [
        "Speed Burner (Underwater)",
    ],
    "Crystal Snail": [
        "Speed Burner (Underwater)",
    ],
    "Overdrive Ostrich": [
        "Speed Burner (Underwater)",
    ],
    "Wire Sponge": [
        "Speed Burner (Underwater)",
    ],
    "Magna Quartz": [
        "Speed Burner (Underwater)",
    ],
    "Chop Register": [
        "Speed Burner (Underwater)",
    ],
    "Raider Killer": [
        "Speed Burner (Underwater)",
    ],
    "Pararoid S-38": [
        "Speed Burner (Underwater)",
    ],
    "Agile": [
        "Speed Burner (Underwater)",
    ],
    "Serges": [
        "Silk Shot (Leaves)",
        "Charged Silk Shot (Leaves)",
        "Charged Speed Burner",
        "Charged Bubble Splash",
        "Uncharged Speed Burner (Underwater)",
    ],
    "Violen": [
        "Speed Burner (Underwater)",
    ],
    "Neo Violen": [
        "Speed Burner (Underwater)",
    ],
    "Serges Tank": [
        "Charged Speed Burner",
        "Speed Burner (Underwater)",
    ],
    "Agile Flyer": [
        "Speed Burner (Underwater)",
    ],
    "Zero": [
        "Speed Burner (Underwater)",
    ],
    "Sigma": [
        "Speed Burner (Underwater)",
    ],
    "Sigma Virus": [
        "Speed Burner (Underwater)",
    ],
}

weapons = {
    "Buster": [
        [None, 0x00, 0x02],
        [None, 0x01, 0x03],
        [None, 0x03, 0x04],
        [None, 0x06, 0x03],
        [None, 0x1D, 0x02],
    ],
    "Strike Chain": [
        [[ItemName.strike_chain], 0x0C, WEAKNESS_UNCHARGED_DMG],
        [[ItemName.strike_chain], 0x15, WEAKNESS_CHARGED_DMG],
    ],
    "Spin Wheel": [
        [[ItemName.spin_wheel], 0x0A, WEAKNESS_UNCHARGED_DMG],
        [[ItemName.spin_wheel], 0x13, WEAKNESS_CHARGED_DMG],
    ],
    "Bubble Splash": [
        [[ItemName.bubble_splash], 0x08, WEAKNESS_UNCHARGED_DMG],
        [[ItemName.bubble_splash], 0x11, WEAKNESS_CHARGED_DMG],
    ],
    "Speed Burner": [
        [[ItemName.speed_burner], 0x0E, WEAKNESS_UNCHARGED_DMG],
        [[ItemName.speed_burner], 0x17, WEAKNESS_CHARGED_DMG],
    ],
    "Speed Burner (Underwater)": [
        [[ItemName.speed_burner], 0x23, WEAKNESS_UNCHARGED_DMG],
    ],
    "Silk Shot (Rocks)": [
        [[ItemName.silk_shot], 0x09, WEAKNESS_UNCHARGED_DMG],
        [[ItemName.silk_shot], 0x12, WEAKNESS_CHARGED_DMG],
    ],
    "Silk Shot (Junk)": [
        [[ItemName.silk_shot], 0x1B, WEAKNESS_UNCHARGED_DMG],
        [[ItemName.silk_shot], 0x20, WEAKNESS_CHARGED_DMG],
    ],
    "Silk Shot (Leaves)": [
        [[ItemName.silk_shot], 0x1C, WEAKNESS_UNCHARGED_DMG],
        [[ItemName.silk_shot], 0x21, WEAKNESS_CHARGED_DMG],
    ],
    "Silk Shot (Crystals)": [
        [[ItemName.silk_shot], 0x1E, WEAKNESS_UNCHARGED_DMG],
        [[ItemName.silk_shot], 0x22, WEAKNESS_CHARGED_DMG],
    ],
    "Silk Shot (Black Rock)": [
        [[ItemName.silk_shot], 0x18, WEAKNESS_UNCHARGED_DMG],
        [[ItemName.silk_shot], 0x1F, WEAKNESS_CHARGED_DMG],
    ],
    "Magnet Mine": [
        [[ItemName.magnet_mine], 0x0D, WEAKNESS_UNCHARGED_DMG],
        [[ItemName.magnet_mine], 0x16, WEAKNESS_CHARGED_DMG],
    ],
    #"Crystal Hunter": [  <- removed because it crashes the game
    #    [[ItemName.crystal_hunter], 0x07, WEAKNESS_UNCHARGED_DMG],
    #],
    "Sonic Slicer": [
        [[ItemName.sonic_slicer], 0x0B, WEAKNESS_UNCHARGED_DMG],
        [[ItemName.sonic_slicer], 0x14, WEAKNESS_CHARGED_DMG],
    ],
}

weapons_chaotic = {
    "Lemon": [
        [None, 0x00, 0x02],
    ],
    "Lemon (Dash)": [
        [None, 0x06, 0x03],
    ],
    "Charged Shot (Level 1)": [
        [["Check Charge 1"], 0x01, 0x03],
    ],
    "Charged Shot (Level 2)": [
        [["Check Charge 1"], 0x03, 0x04],
    ],
    "Charged Shot (Level 3)": [
        [["Check Charge 2"], 0x1D, 0x02],
    ],
    "Strike Chain": [
        [[ItemName.strike_chain], 0x0C, WEAKNESS_UNCHARGED_DMG],
    ],
    "Charged Strike Chain": [
        [["Check Charge 2", ItemName.strike_chain], 0x15, WEAKNESS_CHARGED_DMG],
    ],
    "Spin Wheel": [
        [[ItemName.spin_wheel], 0x0A, WEAKNESS_UNCHARGED_DMG],
    ],
    "Charged Spin Wheel": [
        [["Check Charge 2", ItemName.spin_wheel], 0x13, WEAKNESS_CHARGED_DMG],
    ],
    "Bubble Splash": [
        [[ItemName.bubble_splash], 0x08, WEAKNESS_UNCHARGED_DMG],
    ],
    "Charged Bubble Splash": [
        [["Check Charge 2", ItemName.bubble_splash], 0x11, WEAKNESS_CHARGED_DMG],
    ],
    "Speed Burner": [
        [[ItemName.speed_burner], 0x0E, WEAKNESS_UNCHARGED_DMG],
    ],
    "Speed Burner (Underwater)": [
        [[ItemName.speed_burner], 0x23, WEAKNESS_UNCHARGED_DMG],
    ],
    "Charged Speed Burner": [
        [["Check Charge 2", ItemName.speed_burner], 0x17, WEAKNESS_CHARGED_DMG],
    ],
    "Silk Shot (Rocks)": [
        [[ItemName.silk_shot], 0x09, WEAKNESS_UNCHARGED_DMG],
    ],
    "Charged Silk Shot (Rocks)": [
        [["Check Charge 2", ItemName.silk_shot], 0x12, WEAKNESS_CHARGED_DMG],
    ],
    "Silk Shot (Junk)": [
        [[ItemName.silk_shot], 0x1B, WEAKNESS_UNCHARGED_DMG],
    ],
    "Charged Silk Shot (Junk)": [
        [["Check Charge 2", ItemName.silk_shot], 0x20, WEAKNESS_CHARGED_DMG],
    ],
    "Silk Shot (Leaves)": [
        [[ItemName.silk_shot], 0x1C, WEAKNESS_UNCHARGED_DMG],
    ],
    "Charged Silk Shot (Leaves)": [
        [["Check Charge 2", ItemName.silk_shot], 0x21, WEAKNESS_CHARGED_DMG],
    ],
    "Silk Shot (Crystals)": [
        [[ItemName.silk_shot], 0x1E, WEAKNESS_UNCHARGED_DMG],
    ],
    "Charged Silk Shot (Crystals)": [
        [["Check Charge 2", ItemName.silk_shot], 0x22, WEAKNESS_CHARGED_DMG],
    ],
    "Silk Shot (Black Rock)": [
        [[ItemName.silk_shot], 0x18, WEAKNESS_UNCHARGED_DMG],
    ],
    "Charged Silk Shot (Black Rock)": [
        [["Check Charge 2", ItemName.silk_shot], 0x1F, WEAKNESS_CHARGED_DMG],
    ],
    "Magnet Mine": [
        [[ItemName.magnet_mine], 0x0D, WEAKNESS_UNCHARGED_DMG],
    ],
    "Charged Magnet Mine": [
        [["Check Charge 2", ItemName.magnet_mine], 0x16, WEAKNESS_CHARGED_DMG],
    ],
    #"Crystal Hunter": [   <- removed because it crashes the game
    #    [[ItemName.crystal_hunter], 0x07, WEAKNESS_UNCHARGED_DMG],
    #],
    "Sonic Slicer": [
        [[ItemName.sonic_slicer], 0x0B, WEAKNESS_UNCHARGED_DMG],
    ],
    "Charged Sonic Slicer": [
        [["Check Charge 2", ItemName.sonic_slicer], 0x14, WEAKNESS_CHARGED_DMG],
    ],
}

silk_shot_family = {
    "Silk Shot (Rocks)",
    "Silk Shot (Junk)",
    "Silk Shot (Leaves)",
    "Silk Shot (Crystals)",
    "Silk Shot (Black Rock)",
    "Charged Silk Shot (Rocks)",
    "Charged Silk Shot (Junk)",
    "Charged Silk Shot (Leaves)",
    "Charged Silk Shot (Crystals)",
    "Charged Silk Shot (Black Rock)",
}

def handle_weaknesses(world):
    shuffle_type = world.options.boss_weakness_rando.value
    strictness_type = world.options.boss_weakness_strictness.value
    boss_weakness_plando = world.options.boss_weakness_plando.value

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
            world.boss_weaknesses[boss].append(weapons_chaotic["Charged Shot (Level 3)"][0])
        else:
            damage_table = damage_templates["Only Weakness"].copy()

        if boss in boss_weakness_plando.keys():
            if shuffle_type != "vanilla":
                chosen_weapon = boss_weakness_plando[boss]
                if chosen_weapon not in boss_excluded_weapons[boss]:
                    data = weapons_chaotic[chosen_weapon].copy()
                    for entry in data:
                        world.boss_weaknesses[boss].append(entry)
                        damage = entry[2]
                        damage_table[entry[1]] = damage
                    world.boss_weakness_data[boss] = damage_table.copy()
                    continue

                print (f"[{world.multiworld.player_name[world.player]}] Weakness plando failed for {boss}, contains an excluded weapon. Choosing an alternate weapon...")

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

        elif shuffle_type >= 2:
            for _ in range(shuffle_type - 1):
                chosen_weapon = world.random.choice(copied_weapon_list)
                data = weapons_chaotic[chosen_weapon].copy()
                if chosen_weapon in silk_shot_family:
                    for silk_shot in silk_shot_family:
                        if silk_shot in copied_weapon_list:
                            copied_weapon_list.remove(silk_shot)
                else:
                    copied_weapon_list.remove(chosen_weapon)
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
