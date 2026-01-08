
class EntranceInfo:
    def __init__(self, room, alt_room=None, *, type=None, dungeon=None, index=None, instrument_room=None, target=None, x=None, y=None):
        if type is None and dungeon is not None:
            type = "dungeon"
        assert type is not None, "Missing entrance type"
        self.type = type
        self.room = room
        self.alt_room = alt_room
        self.dungeon = dungeon
        self.index = index
        self.instrument_room = instrument_room
        self.target = target
        self.x = x
        self.y = y


ENTRANCE_INFO = {
    # Row0-1
    "d8":                           EntranceInfo(0x10, target=0x25d, dungeon=8, instrument_room=0x230),
    "phone_d8":                     EntranceInfo(0x11, target=0x299, type="dummy"),
    "fire_cave_exit":               EntranceInfo(0x03, target=0x1ee, type="connector"),
    "fire_cave_entrance":           EntranceInfo(0x13, target=0x1fe, type="connector"),
    "madbatter_taltal":             EntranceInfo(0x04, target=0x1e2, type="single"),
    "left_taltal_entrance":         EntranceInfo(0x15, target=0x2ea, type="connector"),
    "obstacle_cave_entrance":       EntranceInfo(0x17, target=0x2b6, type="connector"),
    "left_to_right_taltalentrance": EntranceInfo(0x07, target=0x2ee, type="connector"),
    "obstacle_cave_outside_chest":  EntranceInfo(0x18, target=0x2bb, type="connector", index=0, x=104, y=18),
    "obstacle_cave_exit":           EntranceInfo(0x18, target=0x2bc, type="connector", index=1, x=136, y=18),
    "papahl_entrance":              EntranceInfo(0x19, target=0x289, type="connector"),
    "papahl_exit":                  EntranceInfo(0x0A, target=0x28b, type="connector", index=0, x=24, y=112),
    "rooster_house":                EntranceInfo(0x0A, target=0x29f, type="dummy", index=2, x=72, y=34),
    "bird_cave":                    EntranceInfo(0x0A, target=0x27e, type="single", index=1, x=120, y=112),
    "multichest_left":              EntranceInfo(0x1D, target=0x2f9, type="connector", index=0, x=24, y=48),
    "multichest_right":             EntranceInfo(0x1D, target=0x2fa, type="connector", index=1, x=120, y=80),
    "multichest_top":               EntranceInfo(0x0D, target=0x2f2, type="connector"),
    "right_taltal_connector1":      EntranceInfo(0x1E, target=0x280, type="connector", index=0, x=56, y=16),
    "right_taltal_connector2":      EntranceInfo(0x1F, target=0x282, type="connector", index=0, x=40, y=16),
    "right_taltal_connector3":      EntranceInfo(0x1E, target=0x283, type="connector", index=1, x=120, y=16),
    "right_taltal_connector4":      EntranceInfo(0x1F, target=0x287, type="connector", index=2, x=88, y=64),
    "right_taltal_connector5":      EntranceInfo(0x1F, target=0x28c, type="connector", index=1, x=120, y=16),
    "right_taltal_connector6":      EntranceInfo(0x0F, target=0x28e, type="connector"),
    "right_fairy":                  EntranceInfo(0x1F, target=0x1fb, type="dummy", index=3, x=56, y=80),
    "d7":                           EntranceInfo(0x0E, "Alt0E", target=0x20e, dungeon=7, instrument_room=0x22C),
    # Row 2-3
    "writes_cave_left":             EntranceInfo(0x20, target=0x2ae, type="connector"),
    "writes_cave_right":            EntranceInfo(0x21, target=0x2af, type="connector"),
    "writes_house":                 EntranceInfo(0x30, target=0x2a8, type="trade"),
    "writes_phone":                 EntranceInfo(0x31, target=0x29b, type="dummy"),
    "d2":                           EntranceInfo(0x24, target=0x136, dungeon=2, instrument_room=0x12A),
    "moblin_cave":                  EntranceInfo(0x35, target=0x2f0, type="single"),
    "photo_house":                  EntranceInfo(0x37, target=0x2b5, type="dummy"),
    "mambo":                        EntranceInfo(0x2A, target=0x2fd, type="water"),
    "d4":                           EntranceInfo(0x2B, "Alt2B", target=0x17a, dungeon=4, index=0, x=72, y=34, instrument_room=0x162),
    # TODO
    #  "d4_connector":                 EntranceInfo(0x2B, "Alt2B", index=1),
    #  "d4_connector_exit":            EntranceInfo(0x2D),
    "heartpiece_swim_cave":         EntranceInfo(0x2E, target=0x1f2, type="water"),
    "raft_return_exit":             EntranceInfo(0x2F, target=0x1e7, type="connector"),
    "raft_house":                   EntranceInfo(0x3F, target=0x2b0, type="insanity"),
    "raft_return_enter":            EntranceInfo(0x8F, target=0x1f7, type="connector"),
    # Forest and everything right of it
    "hookshot_cave":                EntranceInfo(0x42, target=0x2b3, type="single"),
    "toadstool_exit":               EntranceInfo(0x50, target=0x2ab, type="connector"),
    "forest_madbatter":             EntranceInfo(0x52, target=0x1e1, type="single"),
    "toadstool_entrance":           EntranceInfo(0x62, target=0x2bd, type="connector"),
    "crazy_tracy":                  EntranceInfo(0x45, target=0x2ad, type="dummy"),
    "witch":                        EntranceInfo(0x65, target=0x2a2, type="single"),
    "graveyard_cave_left":          EntranceInfo(0x75, target=0x2de, type="connector"),
    "graveyard_cave_right":         EntranceInfo(0x76, target=0x2df, type="connector"),
    "d0":                           EntranceInfo(0x77, target=0x312, dungeon=9, index="all", instrument_room=0x301),
    # Castle
    "castle_jump_cave":             EntranceInfo(0x78, target=0x1fd, type="single"),
    "castle_main_entrance":         EntranceInfo(0x69, target=0x2d3, type="connector"),
    "castle_upper_left":            EntranceInfo(0x59, target=0x2d5, type="connector", index=0, x=24, y=48),
    "castle_upper_right":           EntranceInfo(0x59, target=0x2d6, type="single", index=1, x=88, y=64),
    "castle_secret_exit":           EntranceInfo(0x49, target=0x1eb, type="connector"),
    "castle_secret_entrance":       EntranceInfo(0x4A, target=0x1ec, type="connector"),
    "castle_phone":                 EntranceInfo(0x4B, target=0x2cc, type="dummy"),
    # Mabe village
    "papahl_house_left":            EntranceInfo(0x82, target=0x2a5, type="connector", index=0, x=88, y=82),
    "papahl_house_right":           EntranceInfo(0x82, target=0x2a6, type="connector", index=1, x=120, y=82),
    "dream_hut":                    EntranceInfo(0x83, target=0x2aa, type="single"),
    "rooster_grave":                EntranceInfo(0x92, target=0x1f4, type="single"),
    "shop":                         EntranceInfo(0x93, target=0x2a1, type="single"),
    "madambowwow":                  EntranceInfo(0xA1, target=0x2a7, type="dummy", index=1, x=56, y=66),
    "kennel":                       EntranceInfo(0xA1, target=0x2b2, type="single", index=0, x=88, y=66),
    "start_house":                  EntranceInfo(0xA2, target=0x2a3, type="start"),
    "library":                      EntranceInfo(0xB0, target=0x1fa, type="dummy"),
    "ulrira":                       EntranceInfo(0xB1, target=0x2a9, type="dummy"),
    "mabe_phone":                   EntranceInfo(0xB2, target=0x2cb, type="dummy"),
    "trendy_shop":                  EntranceInfo(0xB3, target=0x2a0, type="trade"),
    # Ukuku Prairie
    "prairie_left_phone":           EntranceInfo(0xA4, target=0x2b4, type="dummy"),
    "prairie_left_cave1":           EntranceInfo(0x84, target=0x2cd, type="single"),
    "prairie_left_cave2":           EntranceInfo(0x86, target=0x2f4, type="single"),
    "prairie_left_fairy":           EntranceInfo(0x87, target=0x1f3, type="dummy"),
    "mamu":                         EntranceInfo(0xD4, target=0x2fb, type="insanity"),
    "d3":                           EntranceInfo(0xB5, target=0x152, dungeon=3, instrument_room=0x159),
    "prairie_right_phone":          EntranceInfo(0x88, target=0x29c, type="dummy"),
    "seashell_mansion":             EntranceInfo(0x8A, target=0x2e9, type="single"),
    "prairie_right_cave_top":       EntranceInfo(0xB8, target=0x292, type="connector", index=1, x=120, y=96),
    "prairie_right_cave_bottom":    EntranceInfo(0xC8, target=0x293, type="connector"),
    "prairie_right_cave_high":      EntranceInfo(0xB8, target=0x295, type="connector", index=0, x=88, y=48),
    "prairie_to_animal_connector":  EntranceInfo(0xAA, target=0x2d0, type="connector"),
    "animal_to_prairie_connector":  EntranceInfo(0xAB, target=0x2d1, type="connector"),
    
    "d6":                           EntranceInfo(0x8C, "Alt8C", target=0x1d4, dungeon=6, instrument_room=0x1B5),
    "d6_connector_exit":            EntranceInfo(0x9C, target=0x1f0, type="connector"),
    "d6_connector_entrance":        EntranceInfo(0x9D, target=0x1f1, type="connector"),
    "armos_fairy":                  EntranceInfo(0x8D, target=0x1ac, type="dummy"),
    "armos_maze_cave":              EntranceInfo(0xAE, target=0x2fc, type="single"),
    "armos_temple":                 EntranceInfo(0xAC, target=0x28f, type="single"),
    # Beach area
    "d1":                           EntranceInfo(0xD3, target=0x117, dungeon=1, instrument_room=0x102),
    "boomerang_cave":               EntranceInfo(0xF4, target=0x1f5, type="single", instrument_room="Alt1F5"),  # instrument_room is to configure the exit on the alt room layout
    "banana_seller":                EntranceInfo(0xE3, target=0x2fe, type="trade"),
    "ghost_house":                  EntranceInfo(0xF6, target=0x1e3, type="single"),

    # Lower prairie
    "richard_house":                EntranceInfo(0xD6, target=0x2c7, type="connector"),
    "richard_maze":                 EntranceInfo(0xC6, target=0x2c9, type="connector"),
    "prairie_low_phone":            EntranceInfo(0xE8, target=0x29d, type="dummy"),
    "prairie_madbatter_connector_entrance": EntranceInfo(0xF9, target=0x1f6, type="connector"),
    "prairie_madbatter_connector_exit": EntranceInfo(0xE7, target=0x1e5, type="connector"),
    "prairie_madbatter":            EntranceInfo(0xE6, target=0x1e0, type="single"),

    "d5":                           EntranceInfo(0xD9, target=0x1a1, dungeon=5, instrument_room=0x182),
    # Animal village
    "animal_phone":                 EntranceInfo(0xDB, target=0x2e3, type="dummy"),
    "animal_house1":                EntranceInfo(0xCC, target=0x2db, type="dummy", index=0, x=40, y=80),
    "animal_house2":                EntranceInfo(0xCC, target=0x2dd, type="dummy", index=1, x=120, y=80),
    "animal_house3":                EntranceInfo(0xCD, target=0x2d9, type="trade", index=1, x=40, y=80),
    "animal_house4":                EntranceInfo(0xCD, target=0x2da, type="dummy", index=2, x=88, y=80),
    "animal_house5":                EntranceInfo(0xDD, target=0x2d7, type="trade"),
    "animal_cave":                  EntranceInfo(0xCD, target=0x2f7, type="single", index=0, x=136, y=32),
    "desert_cave":                  EntranceInfo(0xCF, target=0x1f9, type="single"),
}
