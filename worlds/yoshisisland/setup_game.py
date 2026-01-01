import struct
from typing import TYPE_CHECKING

from .Options import YoshiColors, BabySound, LevelShuffle

if TYPE_CHECKING:
    from . import YoshisIslandWorld


def setup_gamevars(world: "YoshisIslandWorld") -> None:
    if world.options.luigi_pieces_in_pool < world.options.luigi_pieces_required:
        world.options.luigi_pieces_in_pool.value = world.random.randint(world.options.luigi_pieces_required.value, 100)
    world.starting_lives = struct.pack("H", world.options.starting_lives)

    world.level_colors = []
    world.color_order = []
    for i in range(72):
        world.level_colors.append(world.random.randint(0, 7))
    if world.options.yoshi_colors == YoshiColors.option_singularity:
        singularity_color = world.options.yoshi_singularity_color.value
        for i in range(len(world.level_colors)):
            world.level_colors[i] = singularity_color
    elif world.options.yoshi_colors == YoshiColors.option_random_order:
        world.leader_color = world.random.randint(0, 7)
        for i in range(7):
            world.color_order.append(world.random.randint(0, 7))

    bonus_valid = [0x00, 0x02, 0x04, 0x06, 0x08, 0x0A]

    world.world_bonus = []
    for i in range(12):
        world.world_bonus.append(world.random.choice(bonus_valid))

    safe_baby_sounds = [0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E,
                        0x0F, 0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1A,
                        0x1B, 0x1C, 0x1D, 0x1E, 0x1F, 0x20, 0x21, 0x23, 0x24, 0x25, 0x26, 0x27,
                        0x28, 0x29, 0x2A, 0x2B, 0x2C, 0x2D, 0x2E, 0x2F, 0x30, 0x31, 0x32, 0x33,
                        0x34, 0x35, 0x36, 0x37, 0x38, 0x39, 0x3A, 0x3B, 0x3C, 0x3D, 0x3E, 0x3F,
                        0x40, 0x41, 0x42, 0x43, 0x44, 0x45, 0x46, 0x47, 0x48, 0x49, 0x4A, 0x4B,
                        0x4C, 0x4D, 0x4E, 0x4F, 0x50, 0x51, 0x52, 0x52, 0x53, 0x54, 0x55, 0x56,
                        0x57, 0x58, 0x59, 0x5A, 0x5B, 0x5C, 0x5D, 0x5E, 0x5F, 0x60, 0x61, 0x62,
                        0x63, 0x64, 0x65, 0x66, 0x67, 0x68, 0x69, 0x6A, 0x6B, 0x6C, 0x6D, 0x6E,
                        0x73, 0x75, 0x76, 0x77, 0x78, 0x79, 0x7A, 0x7B, 0x7C, 0x7D, 0x7E, 0x7F,
                        0x80, 0x81, 0x82, 0x83, 0x84, 0x85, 0x86, 0x87, 0x88, 0x89, 0x8A, 0x8B,
                        0x8C, 0x8D, 0x8E, 0x8F, 0x90, 0x91, 0x92, 0x93, 0x94, 0x95, 0x96, 0x97,
                        0x98, 0x99, 0x9A, 0x9B, 0x9C, 0x9D, 0x9E, 0x9F, 0xA0, 0xA1, 0xA2]

    if world.options.baby_mario_sound == BabySound.option_random_sound_effect:
        world.baby_mario_sfx = world.random.choice(safe_baby_sounds)
    elif world.options.baby_mario_sound == BabySound.option_disabled:
        world.baby_mario_sfx = 0x42
    else:
        world.baby_mario_sfx = 0x44

    boss_list = ["Burt The Bashful's Boss Room", "Salvo The Slime's Boss Room",
                 "Bigger Boo's Boss Room", "Roger The Ghost's Boss Room",
                 "Prince Froggy's Boss Room", "Naval Piranha's Boss Room",
                 "Marching Milde's Boss Room", "Hookbill The Koopa's Boss Room",
                 "Sluggy The Unshaven's Boss Room", "Raphael The Raven's Boss Room",
                 "Tap-Tap The Red Nose's Boss Room"]

    world.boss_order = []

    if world.options.boss_shuffle:
        world.random.shuffle(boss_list)
    world.boss_order = boss_list

    burt_pointers = [0x3D, 0x05, 0x63, 0x00]
    slime_pointers = [0x70, 0x04, 0x78, 0x00]
    boo_pointers = [0x74, 0xBB, 0x7A, 0x00]
    pot_pointers = [0xCF, 0x04, 0x4D, 0x00]
    frog_pointers = [0xBF, 0x12, 0x62, 0x04]
    plant_pointers = [0x7F, 0x0D, 0x42, 0x00]
    milde_pointers = [0x82, 0x06, 0x64, 0x00]
    koop_pointers = [0x86, 0x0D, 0x78, 0x00]
    slug_pointers = [0x8A, 0x09, 0x7A, 0x00]
    raph_pointers = [0xC4, 0x03, 0x4B, 0x05]
    tap_pointers = [0xCC, 0x49, 0x64, 0x02]

    boss_data_list = [
        burt_pointers,
        slime_pointers,
        boo_pointers,
        pot_pointers,
        frog_pointers,
        plant_pointers,
        milde_pointers,
        koop_pointers,
        slug_pointers,
        raph_pointers,
        tap_pointers
    ]

    boss_levels = [0x03, 0x07, 0x0F, 0x13, 0x1B, 0x1F, 0x27, 0x2B, 0x33, 0x37, 0x3F]

    boss_room_idlist = {
        "Burt The Bashful's Boss Room": 0,
        "Salvo The Slime's Boss Room": 1,
        "Bigger Boo's Boss Room": 2,
        "Roger The Ghost's Boss Room": 3,
        "Prince Froggy's Boss Room": 4,
        "Naval Piranha's Boss Room": 5,
        "Marching Milde's Boss Room": 6,
        "Hookbill The Koopa's Boss Room": 7,
        "Sluggy The Unshaven's Boss Room": 8,
        "Raphael The Raven's Boss Room": 9,
        "Tap-Tap The Red Nose's Boss Room": 10,
    }

    boss_check_list = {
        "Burt The Bashful's Boss Room": "Burt The Bashful Defeated",
        "Salvo The Slime's Boss Room": "Salvo The Slime Defeated",
        "Bigger Boo's Boss Room": "Bigger Boo Defeated",
        "Roger The Ghost's Boss Room": "Roger The Ghost Defeated",
        "Prince Froggy's Boss Room": "Prince Froggy Defeated",
        "Naval Piranha's Boss Room": "Naval Piranha Defeated",
        "Marching Milde's Boss Room": "Marching Milde Defeated",
        "Hookbill The Koopa's Boss Room": "Hookbill The Koopa Defeated",
        "Sluggy The Unshaven's Boss Room": "Sluggy The Unshaven Defeated",
        "Raphael The Raven's Boss Room": "Raphael The Raven Defeated",
        "Tap-Tap The Red Nose's Boss Room": "Tap-Tap The Red Nose Defeated",
    }

    world.boss_room_id = [boss_room_idlist[roomnum] for roomnum in world.boss_order]
    world.tap_tap_room = boss_levels[world.boss_room_id.index(10)]
    world.boss_ap_loc = [boss_check_list[roomnum] for roomnum in world.boss_order]

    world.boss_burt_data = boss_data_list[world.boss_room_id[0]]

    world.boss_slime_data = boss_data_list[world.boss_room_id[1]]

    world.boss_boo_data = boss_data_list[world.boss_room_id[2]]

    world.boss_pot_data = boss_data_list[world.boss_room_id[3]]

    world.boss_frog_data = boss_data_list[world.boss_room_id[4]]

    world.boss_plant_data = boss_data_list[world.boss_room_id[5]]

    world.boss_milde_data = boss_data_list[world.boss_room_id[6]]

    world.boss_koop_data = boss_data_list[world.boss_room_id[7]]

    world.boss_slug_data = boss_data_list[world.boss_room_id[8]]

    world.boss_raph_data = boss_data_list[world.boss_room_id[9]]

    world.boss_tap_data = boss_data_list[world.boss_room_id[10]]

    world.global_level_list = [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
                               0x0C, 0x0D, 0x0E, 0x0F, 0x10, 0x11, 0x12, 0x13,
                               0x18, 0x19, 0x1A, 0x1B, 0x1C, 0x1D, 0x1E, 0x1F,
                               0x24, 0x25, 0x26, 0x27, 0x28, 0x29, 0x2A, 0x2B,
                               0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37,
                               0x3C, 0x3D, 0x3E, 0x3F, 0x40, 0x41, 0x42]
    level_id_list = {
                    0x00: "1-1",
                    0x01: "1-2",
                    0x02: "1-3",
                    0x03: "1-4",
                    0x04: "1-5",
                    0x05: "1-6",
                    0x06: "1-7",
                    0x07: "1-8",
                    0x0C: "2-1",
                    0x0D: "2-2",
                    0x0E: "2-3",
                    0x0F: "2-4",
                    0x10: "2-5",
                    0x11: "2-6",
                    0x12: "2-7",
                    0x13: "2-8",
                    0x18: "3-1",
                    0x19: "3-2",
                    0x1A: "3-3",
                    0x1B: "3-4",
                    0x1C: "3-5",
                    0x1D: "3-6",
                    0x1E: "3-7",
                    0x1F: "3-8",
                    0x24: "4-1",
                    0x25: "4-2",
                    0x26: "4-3",
                    0x27: "4-4",
                    0x28: "4-5",
                    0x29: "4-6",
                    0x2A: "4-7",
                    0x2B: "4-8",
                    0x30: "5-1",
                    0x31: "5-2",
                    0x32: "5-3",
                    0x33: "5-4",
                    0x34: "5-5",
                    0x35: "5-6",
                    0x36: "5-7",
                    0x37: "5-8",
                    0x3C: "6-1",
                    0x3D: "6-2",
                    0x3E: "6-3",
                    0x3F: "6-4",
                    0x40: "6-5",
                    0x41: "6-6",
                    0x42: "6-7"
                        }

    level_names = {
                    0x00: "Make Eggs, Throw Eggs",
                    0x01: "Watch Out Below!",
                    0x02: "The Cave Of Chomp Rock",
                    0x03: "Burt The Bashful's Fort",
                    0x04: "Hop! Hop! Donut Lifts",
                    0x05: "Shy-Guys On Stilts",
                    0x06: "Touch Fuzzy Get Dizzy",
                    0x07: "Salvo The Slime's Castle",
                    0x0C: "Visit Koopa And Para-Koopa",
                    0x0D: "The Baseball Boys",
                    0x0E: "What's Gusty Taste Like?",
                    0x0F: "Bigger Boo's Fort",
                    0x10: "Watch Out For Lakitu",
                    0x11: "The Cave Of The Mystery Maze",
                    0x12: "Lakitu's Wall",
                    0x13: "The Potted Ghost's Castle",
                    0x18: "Welcome To Monkey World!",
                    0x19: "Jungle Rhythm...",
                    0x1A: "Nep-Enuts' Domain",
                    0x1B: "Prince Froggy's Fort",
                    0x1C: "Jammin' Through The Trees",
                    0x1D: "The Cave Of Harry Hedgehog",
                    0x1E: "Monkeys' Favorite Lake",
                    0x1F: "Naval Piranha's Castle",
                    0x24: "GO! GO! MARIO!!",
                    0x25: "The Cave Of The Lakitus",
                    0x26: "Don't Look Back!",
                    0x27: "Marching Milde's Fort",
                    0x28: "Chomp Rock Zone",
                    0x29: "Lake Shore Paradise",
                    0x2A: "Ride Like The Wind",
                    0x2B: "Hookbill The Koopa's Castle",
                    0x30: "BLIZZARD!!!",
                    0x31: "Ride The Ski Lifts",
                    0x32: "Danger - Icy Conditions Ahead",
                    0x33: "Sluggy The Unshaven's Fort",
                    0x34: "Goonie Rides!",
                    0x35: "Welcome To Cloud World",
                    0x36: "Shifting Platforms Ahead",
                    0x37: "Raphael The Raven's Castle",
                    0x3C: "Scary Skeleton Goonies!",
                    0x3D: "The Cave Of The Bandits",
                    0x3E: "Beware The Spinning Logs",
                    0x3F: "Tap-Tap The Red Nose's Fort",
                    0x40: "The Very Loooooong Cave",
                    0x41: "The Deep, Underground Maze",
                    0x42: "KEEP MOVING!!!!"
                        }

    world_1_offsets = [0x01, 0x00, 0x00, 0x00, 0x00, 0x00]
    world_2_offsets = [0x01, 0x01, 0x00, 0x00, 0x00, 0x00]
    world_3_offsets = [0x01, 0x01, 0x01, 0x00, 0x00, 0x00]
    world_4_offsets = [0x01, 0x01, 0x01, 0x01, 0x00, 0x00]
    world_5_offsets = [0x01, 0x01, 0x01, 0x01, 0x01, 0x00]
    easy_start_lv = [0x02, 0x04, 0x06, 0x0E, 0x10, 0x18, 0x1C, 0x28,
                     0x30, 0x31, 0x35, 0x36, 0x3E, 0x40, 0x42]
    norm_start_lv = [0x00, 0x01, 0x02, 0x04, 0x06, 0x0E, 0x10, 0x12, 0x18, 0x1A,
                     0x1C, 0x1E, 0x28, 0x30, 0x31, 0x34, 0x35, 0x36, 0x3D, 0x3E, 0x40, 0x42]
    hard_start_lv = [0x00, 0x01, 0x02, 0x04, 0x06, 0x0D, 0x0E, 0x10, 0x11, 0x12, 0x18, 0x1A, 0x1C,
                     0x1E, 0x24, 0x25, 0x26, 0x28, 0x29, 0x30, 0x31, 0x34, 0x35, 0x36, 0x3D, 0x3E,
                     0x40, 0x42]
    diff_index = [easy_start_lv, norm_start_lv, hard_start_lv]
    diff_level = diff_index[world.options.stage_logic.value]
    boss_lv = [0x03, 0x07, 0x0F, 0x13, 0x1B, 0x1F, 0x27, 0x2B, 0x33, 0x37, 0x3F]
    world.world_start_lv = [0, 8, 16, 24, 32, 40]
    if not world.options.shuffle_midrings:
        easy_start_lv.extend([0x1A, 0x24, 0x34])
        norm_start_lv.extend([0x24, 0x3C])
        hard_start_lv.extend([0x1D, 0x3C])

    if world.options.level_shuffle != LevelShuffle.option_bosses_guaranteed:
        hard_start_lv.extend([0x07, 0x1B, 0x1F, 0x2B, 0x33, 0x37])
        if not world.options.shuffle_midrings:
            easy_start_lv.extend([0x1B])
            norm_start_lv.extend([0x1B, 0x2B, 0x37])

    starting_level = world.random.choice(diff_level)

    starting_level_entrance = world.world_start_lv[world.options.starting_world.value]
    if world.options.level_shuffle:
        world.global_level_list.remove(starting_level)
        world.random.shuffle(world.global_level_list)
        if world.options.level_shuffle == LevelShuffle.option_bosses_guaranteed:
            for i in range(11):
                world.global_level_list = [item for item in world.global_level_list
                                           if item not in boss_lv]
            world.random.shuffle(boss_lv)

            world.global_level_list.insert(3 - world_1_offsets[world.options.starting_world.value], boss_lv[0])  # 1 if starting world is 1, 0 otherwise
            world.global_level_list.insert(7 - world_1_offsets[world.options.starting_world.value], boss_lv[1])
            world.global_level_list.insert(11 - world_2_offsets[world.options.starting_world.value], boss_lv[2])
            world.global_level_list.insert(15 - world_2_offsets[world.options.starting_world.value], boss_lv[3])
            world.global_level_list.insert(19 - world_3_offsets[world.options.starting_world.value], boss_lv[4])
            world.global_level_list.insert(23 - world_3_offsets[world.options.starting_world.value], boss_lv[5])
            world.global_level_list.insert(27 - world_4_offsets[world.options.starting_world.value], boss_lv[6])
            world.global_level_list.insert(31 - world_4_offsets[world.options.starting_world.value], boss_lv[7])
            world.global_level_list.insert(35 - world_5_offsets[world.options.starting_world.value], boss_lv[8])
            world.global_level_list.insert(39 - world_5_offsets[world.options.starting_world.value], boss_lv[9])
            world.global_level_list.insert(43 - 1, boss_lv[10])
        world.global_level_list.insert(starting_level_entrance, starting_level)
    world.level_location_list = [level_id_list[LevelID] for LevelID in world.global_level_list]
    world.level_name_list = [level_names[LevelID] for LevelID in world.global_level_list]

    level_panel_dict = {
                    0x00: [0x04, 0x04, 0x53],
                    0x01: [0x20, 0x04, 0x53],
                    0x02: [0x3C, 0x04, 0x53],
                    0x03: [0x58, 0x04, 0x53],
                    0x04: [0x74, 0x04, 0x53],
                    0x05: [0x90, 0x04, 0x53],
                    0x06: [0xAC, 0x04, 0x53],
                    0x07: [0xC8, 0x04, 0x53],
                    0x0C: [0x04, 0x24, 0x53],
                    0x0D: [0x20, 0x24, 0x53],
                    0x0E: [0x3C, 0x24, 0x53],
                    0x0F: [0x58, 0x24, 0x53],
                    0x10: [0x74, 0x24, 0x53],
                    0x11: [0x90, 0x24, 0x53],
                    0x12: [0xAC, 0x24, 0x53],
                    0x13: [0xC8, 0x24, 0x53],
                    0x18: [0x04, 0x44, 0x53],
                    0x19: [0x20, 0x44, 0x53],
                    0x1A: [0x3C, 0x44, 0x53],
                    0x1B: [0x58, 0x44, 0x53],
                    0x1C: [0x74, 0x44, 0x53],
                    0x1D: [0x90, 0x44, 0x53],
                    0x1E: [0xAC, 0x44, 0x53],
                    0x1F: [0xC8, 0x44, 0x53],
                    0x24: [0x04, 0x64, 0x53],
                    0x25: [0x20, 0x64, 0x53],
                    0x26: [0x3C, 0x64, 0x53],
                    0x27: [0x58, 0x64, 0x53],
                    0x28: [0x74, 0x64, 0x53],
                    0x29: [0x90, 0x64, 0x53],
                    0x2A: [0xAC, 0x64, 0x53],
                    0x2B: [0xC8, 0x64, 0x53],
                    0x30: [0x04, 0x04, 0x53],
                    0x31: [0x20, 0x04, 0x53],
                    0x32: [0x3C, 0x04, 0x53],
                    0x33: [0x58, 0x04, 0x53],
                    0x34: [0x74, 0x04, 0x53],
                    0x35: [0x90, 0x04, 0x53],
                    0x36: [0xAC, 0x04, 0x53],
                    0x37: [0xC8, 0x04, 0x53],
                    0x3C: [0x04, 0x24, 0x53],
                    0x3D: [0x20, 0x24, 0x53],
                    0x3E: [0x3C, 0x24, 0x53],
                    0x3F: [0x58, 0x24, 0x53],
                    0x40: [0x74, 0x24, 0x53],
                    0x41: [0x90, 0x24, 0x53],
                    0x42: [0xAC, 0x24, 0x53],
                        }
    panel_palette_1 = [0x00, 0x03, 0x04, 0x05, 0x0C, 0x10, 0x12, 0x13, 0x19, 0x1A, 0x1B, 0x1C, 0x1D,
                       0x24, 0x26, 0x27, 0x29, 0x2A, 0x2B, 0x30, 0x32, 0x34,
                       0x35, 0x37, 0x3C, 0x3D, 0x40, 0x41]  # 000C
    panel_palette_2 = [0x01, 0x02, 0x06, 0x07, 0x0D, 0x0E, 0x0F, 0x11, 0x18, 0x1E, 0x1F, 0x25, 0x28,
                       0x31, 0x33, 0x36, 0x3E, 0x3F, 0x42]  # 0010

    stage_number = 0
    world_number = 1
    for i in range(47):
        stage_number += 1
        if stage_number >= 9:
            world_number += 1
            stage_number = 1
        for _ in range(3):
            setattr(world, f"Stage{world_number}{stage_number}StageGFX",
                    level_panel_dict[world.global_level_list[i]])

    world.level_gfx_table = []
    world.palette_panel_list = []

    for i in range(47):
        if world.global_level_list[i] >= 0x30:
            world.level_gfx_table.append(0x15)
        else:
            world.level_gfx_table.append(0x11)

        if world.global_level_list[i] in panel_palette_1:
            world.palette_panel_list.extend([0x00, 0x0C])
        elif world.global_level_list[i] in panel_palette_2:
            world.palette_panel_list.extend([0x00, 0x10])

    world.palette_panel_list[16:16] = [0x00, 0x0c, 0x00, 0x0c, 0x00, 0x18, 0x00, 0x18]
    world.palette_panel_list[40:40] = [0x00, 0x0c, 0x00, 0x0c, 0x00, 0x18, 0x00, 0x18]
    world.palette_panel_list[64:64] = [0x00, 0x0c, 0x00, 0x0c, 0x00, 0x18, 0x00, 0x18]
    world.palette_panel_list[88:88] = [0x00, 0x0c, 0x00, 0x0c, 0x00, 0x18, 0x00, 0x18]
    world.palette_panel_list[112:112] = [0x00, 0x0c, 0x00, 0x0c, 0x00, 0x18, 0x00, 0x18]

    world.level_gfx_table.insert(8, 0x15)
    world.level_gfx_table.insert(8, 0x15)
    world.level_gfx_table.insert(8, 0x15)
    world.level_gfx_table.insert(8, 0x11)

    world.level_gfx_table.insert(20, 0x15)
    world.level_gfx_table.insert(20, 0x15)
    world.level_gfx_table.insert(20, 0x15)
    world.level_gfx_table.insert(20, 0x11)

    world.level_gfx_table.insert(32, 0x15)
    world.level_gfx_table.insert(32, 0x15)
    world.level_gfx_table.insert(32, 0x15)
    world.level_gfx_table.insert(32, 0x11)

    world.level_gfx_table.insert(44, 0x15)
    world.level_gfx_table.insert(44, 0x15)
    world.level_gfx_table.insert(44, 0x15)
    world.level_gfx_table.insert(44, 0x11)

    world.level_gfx_table.insert(56, 0x15)
    world.level_gfx_table.insert(56, 0x15)
    world.level_gfx_table.insert(56, 0x15)
    world.level_gfx_table.insert(56, 0x15)

    castle_door_dict = {
        0: [0xB8, 0x05, 0x77, 0x00],
        1: [0xB8, 0x05, 0x77, 0x00],
        2: [0xC6, 0x07, 0x7A, 0x00],
        3: [0xCD, 0x05, 0x5B, 0x00],
        4: [0xD3, 0x00, 0x77, 0x06],
        5: [0xB8, 0x05, 0x77, 0x00],
    }

    world.castle_door = castle_door_dict[world.options.bowser_door_mode.value]

    world.world_1_stages = world.global_level_list[0:8]
    world.world_2_stages = world.global_level_list[8:16]
    world.world_3_stages = world.global_level_list[16:24]
    world.world_4_stages = world.global_level_list[24:32]
    world.world_5_stages = world.global_level_list[32:40]
    world.world_6_stages = world.global_level_list[40:47]

    world.world_1_stages.extend([0x08, 0x09])
    world.world_2_stages.extend([0x14, 0x15])
    world.world_3_stages.extend([0x20, 0x21])
    world.world_4_stages.extend([0x2C, 0x2D])
    world.world_5_stages.extend([0x38, 0x39])
    world.world_6_stages.extend([0x43, 0x44, 0x45])

    bowser_text_table = {
        0: [0xDE, 0xEE, 0xDC, 0xDC, 0xE5],  # Gween
        1: [0xE7, 0xE0, 0xE5, 0xE2, 0xD0],  # Pink
        3: [0xEB, 0xDF, 0xF0, 0xD8, 0xE5],  # Thyan
        2: [0xF0, 0xDC, 0xEE, 0xEE, 0xE6],  # Yewow
        4: [0xE7, 0xEC, 0xDF, 0xE7, 0xE3],  # puhpl
        5: [0xD9, 0xEE, 0xE6, 0xEE, 0xE5],  # Bwown
        6: [0xEE, 0xDC, 0xDB, 0xD0, 0xD0],  # Wed
        7: [0xD9, 0xEE, 0xEC, 0xDC, 0xD0],  # Bwue
    }

    if world.options.yoshi_colors == YoshiColors.option_random_order:
        world.bowser_text = bowser_text_table[world.leader_color]
    else:
        world.bowser_text = bowser_text_table[world.level_colors[67]]
