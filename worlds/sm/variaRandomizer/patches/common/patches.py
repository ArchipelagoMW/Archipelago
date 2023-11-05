patches = {
    "Removes_Gravity_Suit_heat_protection": {
        0x06e37d: [0x01],
        0x0869dd: [0x01]},
    "Mother_Brain_Cutscene_Edits": {
        0x148824: [0x01,0x00],
        0x148848: [0x01,0x00],
        0x148867: [0x01,0x00],
        0x14887f: [0x01,0x00],
        0x148bdb: [0x04,0x00],
        0x14897d: [0x10,0x00],
        0x1489af: [0x10,0x00],
        0x1489e1: [0x10,0x00],
        0x148a09: [0x10,0x00],
        0x148a31: [0x10,0x00],
        0x148a63: [0x10,0x00],
        0x148a95: [0x10,0x00],
        0x148b33: [0x10,0x00],
        0x148dc6: [0xb0],
        0x148b8d: [0x12,0x00],
        0x148d74: [0x00,0x00],
        0x148d86: [0x00,0x00],
        0x148daf: [0x00,0x01],
        0x148e51: [0x01,0x00],
        0x14b93a: [0x00,0x01],
        0x148eef: [0x0a,0x00],
        0x148f0f: [0x60,0x00],
        0x14af4e: [0x0a,0x00],
        0x14af0d: [0x0a,0x00],
        0x14b00d: [0x00,0x00],
        0x14b132: [0x40,0x00],
        0x14b16d: [0x00,0x00],
        0x14b19f: [0x20,0x00],
        0x14b1b2: [0x30,0x00],
        0x14b20c: [0x03,0x00]},
    "No_Music":{
        0x278413: [0x6f]},
    "Escape_Rando_Enable_Enemies":{
        0x10F000: [0x0, 0x0]},
    "Escape_Rando_Disable_Enemies":{
        0x10F000: [0x1]},
    "Escape_Animals_Open_Brinstar": {
        0x784BD: [0x10]
    },
    "Escape_Animals_Open_Norfair": {
        0x78B0B: [0x10]
    },
    "Escape_Animals_Open_Maridia": {
        0x7C54C: [0x10]
    },
    "Enable_Backup_Saves": {
        0xef20: [0x1]
    },
    'Escape_Trigger' : {
        0x10F5FE: [0x1]
    },
    'Escape_Trigger_Disable' : {
        0x10F5FE: [0x0]
    },
    # actually a bitmask:
    # high bit is for sfx play on obj completion, low bit for trigger escape
    # only in crateria (standard in rando, default in the patch) for nothing objectives.
    # we want to play sfx on objective completion only with non-standard objectives
    'Objectives_sfx' : {
        0x10F5FF: [0x81]
    },
    # see above, used in plandos so trigger escape whatever the start loc is
    # with nothing objective. With this, we'll play sfx even in plandos
    # with standard objectives, but it'll prevent to handle these patches
    # as anything else that just bytes.
    'Escape_Trigger_Nothing_Objective_Anywhere' : {
        0x10F5FF: [0x80]
    },
    # for development/quickmet: disable clear save files on 1st boot
    "Disable_Clear_Save_Boot": {
        0x7E39: [0x4c, 0x7c, 0xfe]
    },
    # vanilla data to restore setup asm for plandos
    "Escape_Animals_Disable": {
        0x79867: [0xb2, 0x91],
        0x798dc: [0xbb, 0x91]
    },
    # with animals suprise make the bomb blocks at alcatraz disapear with event "Zebes timebomb set" instead of "critters escaped"
    "Escape_Animals_Change_Event": {
        0x023B0A: [0x0E]
    },
    "LN_Chozo_SpaceJump_Check_Disable": {
        0x2518f: [0xea, 0xea, 0xea, 0xea, 0xea, 0xea, 0xea, 0xea]
    },
    "LN_PB_Heat_Disable": {
        0x18878: [0x80, 0x00]
    },
    "LN_Firefleas_Remove_Fune": {
        0x10ABC2: [0xff, 0x7f, 0xff, 0x7f],
    },
    "WS_Main_Open_Grey": {
        0x10BE92: [0x0]
    },
    "WS_Save_Active": {
        0x7ceb0: [0xC9]
    },
    "WS_Etank": {
        0x7cc4d: [0x37, 0xc3],
        0x7cbfb: [0x23, 0xc3]
    },
    "Phantoon_Eye_Door":{
        0x7CCAF: [0x91, 0xC2]
    },
    # has to be applied along with WS_Main_Open_Grey
    "Sponge_Bath_Blinking_Door": {
        0x7C276: [0x0C],
        0x10CE69: [0x00]
    },
    "Infinite_Space_Jump": {
        0x82493: [0x80, 0x0D]
    },
    "SpriteSomething_Disable_Spin_Attack": {
        0xD93FE: [0x0, 0x0]
    },
    "Ship_Takeoff_Disable_Hide_Samus": {
        0x112B13: [0x6B]
    },
    # custom load points for non standard start APs
    "Save_G4": {
        # load point entry
        0x4527: [0xED, 0xA5, 0x16, 0x92, 0x00, 0x00, 0x00, 0x03, 0x00, 0x00, 0xA8, 0x00, 0x60, 0x00],
        # map icon X/Y
        0x1486f: [0x78, 0x00, 0x48, 0x00]
    },
    "Save_Gauntlet": {
        # load point entry
        0x4519: [0xBD, 0x99, 0x1A, 0x8B, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x88, 0x00, 0x50, 0x00],
        # music in room state header
        0x799ce: [0x09],
        # map icon X/Y
        0x1486b: [0x58, 0x00, 0x18, 0x00]
    },
    "Save_Watering_Hole": {
        # load point entry
        0x4979: [0x3B, 0xD1, 0x98, 0xA4, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x88, 0x00, 0xD0, 0xFF],
        # music in room state header
        0x7d14c: [0x1b, 0x06],
        # map icon X/Y
        0x14a0f: [0x68, 0x00, 0x28, 0x00]
    },
    "Save_Mama": {
        # load point entry
        0x496B: [0x55, 0xD0, 0xE4, 0xA3, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x98, 0x00, 0xF0, 0xFF],
        # music in room state header
        0x7d066: [0x1b, 0x06],
        # map icon X/Y
        0x14a0b: [0x97, 0x00, 0x67, 0x00]
    },
    "Save_Aqueduct": {
        # load point entry
        0x495D: [0xA7, 0xD5, 0xD4, 0xA7, 0x00, 0x00, 0x00, 0x05, 0x00, 0x00, 0x78, 0x00, 0x20, 0x00],
        # map icon X/Y
        0x14a07: [0xc4, 0x00, 0x50, 0x00]
    },
    "Save_Etecoons": {
        # load point entry
        0x4631: [0x51, 0xA0, 0x3A, 0x8F, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x98, 0x00, 0xD0, 0xFF],
        # music in room state header
        0x7a062: [0x0f, 0x05],
        # map icon X/Y
        0x148d9: [0x28, 0x00, 0x58, 0x00]
    },
    "Save_Firefleas": {
        # load point entry
        0x473b: [0x5A, 0xB5, 0x9E, 0x9A, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x78, 0x00, 0x00, 0x00],
        # music in room state header
        0x7b56b: [0x18, 0x05],
        # map icon X/Y
        0x1493f: [0x28, 0x01, 0x38, 0x00]
    },
    # custom load points for west maridia additional saves in area rando
    "Save_Crab_Shaft": {
        # load point entry
        0x4995: [0xa3, 0xd1, 0x68, 0xa4, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x78, 0x00, 0x60, 0x00],
        # map icon X/Y
        0x14a17: [0x90, 0x00, 0x50, 0x00]
    },
    "Save_Main_Street": {
        0x49a3: [0xC9, 0xCF, 0xD8, 0xA3, 0x00, 0x00, 0x00, 0x01, 0x00, 0x05, 0x78, 0x00, 0x10, 0x00],
        # map icon X/Y
        0x14a1b: [0x58, 0x00, 0x78, 0x00]
    },
    # blinking doors for area APs
    'Blinking[Keyhunter Room Bottom]': {
        0x78228: [0x4e, 0xc8, 0x16, 0x2d, 0x0e, 0x8c],
        0x108F7B: [0x0]
    },
    'Blinking[Moat Right]': {
        0x1085E0: [0x0]
    },
    'Blinking[Morph Ball Room Left]': {
        0x78746: [0x48, 0xc8, 0x01, 0x26, 0x31, 0x8c],
        0x1093A8: [0x0]
    },
    'Blinking[Green Pirates Shaft Bottom Right]': {
        0x78470: [0x42, 0xc8, 0x0e, 0x66, 0x63, 0x8c],
        0x108572: [0x0]
    },
    'Blinking[Lower Mushrooms Left]': {
        0x108C0C: [0x0]
    },
    'Blinking[Golden Four]': {
        0x109F60: [0x0]
    },
    'Blinking[Green Brinstar Elevator]': {
        0x108585: [0x0]
    },
    'Blinking[Green Hill Zone Top Right]': {
        0x78670: [0x42, 0xc8, 0x1e, 0x06, 0x63, 0x8c],
        0x109D5B: [0x0]
    },
    'Blinking[Noob Bridge Right]': {
        0x787A6: [0x42, 0xc8, 0x5e, 0x06, 0x63, 0x8c],
        0x109325: [0x0]
    },
    'Blinking[Warehouse Zeela Room Left]': {
        0x109451: [0x0]
    },
    'Blinking[KraidRoomOut]': {
        # removes gadora by ending PLM list
        0x78A1A: [0x42, 0xc8, 0x1e, 0x16, 0x63, 0x8c, 0x00, 0x00],
        0x10A056: [0x0]
    },
    'Blinking[Warehouse Entrance Right]': {
        0x1098F6: [0x0]
    },
    'Blinking[Warehouse Entrance Left]': {
        0x1098F6: [0x0]
    },
    'Blinking[Single Chamber Top Right]': {
        0x10B88E: [0x0]
    },
    'Blinking[Kronic Boost Room Bottom Left]': {
        0x78D4E: [0x48, 0xc8, 0x11, 0x26, 0x58, 0x8c],
        0x10B9D7: [0x0]
    },
    'Blinking[Three Muskateers Room Left]': {
        0x10BB0D: [0x0]
    },
    'Blinking[Lava Dive Right]': {
        0x10AD6B: [0x0]
    },
    'Blinking[RidleyRoomOut]': {
        # removes gadora by ending PLM list
        0x78EA6: [0x48, 0xc8, 0x01, 0x06, 0x63, 0x8c, 0x00, 0x00],
        0x10B81B: [0x0]
    },
    'Blinking[West Ocean Left]': {
        0x1086F6: [0x0]
    },
    'Blinking[PhantoonRoomOut]': {
        # removes gadora by ending PLM list
        0x7C29D: [0x42, 0xc8, 0x4e, 0x06, 0x63, 0x8c, 0x00, 0x00],
        # zero needed enemy count for both room states
        0x10C3E5: [0x0],
        0x10C19B: [0x0]
    },
    'Blinking[Crab Maze Left]': {
        0x108B3A: [0x0]
    },
    'Blinking[Crab Hole Bottom Left]': {
        0x10DE59: [0x0]
    },
    'Blinking[Main Street Bottom]': {
        0x10DF2F: [0x0]
    },
    'Blinking[Red Fish Room Left]': {
        0x10D3EC: [0x0]
    },
    'Blinking[Le Coude Right]': {
        0x7823E: [0x42, 0xc8, 0x0e, 0x06, 0x63, 0x8c],
        0x1085DD: [0x0]
    },
    'Blinking[DraygonRoomOut]': {
        # overwrites a gadoras PLMs and replace the rest with useless arrow PLMs
        # (we cannot end the list because the item is after in the list)
        0x7C73B: [0x48, 0xc8, 0x01, 0x26, 0x63, 0x8c] + [0x3b, 0xb6, 0x31, 0x26, 0x00, 0x00]*2,
        0x10D111: [0x0]
    },
    'Blinking[East Tunnel Top Right]': {
        0x10D5E1: [0x0]
    },
    'Blinking[East Tunnel Right]': {
        0x10D5E1: [0x0]
    },
    'Blinking[Glass Tunnel Top]': {
        0x10D53B: [0x0]
    },
    'Blinking[Red Tower Top Left]': {
        0x109504: [0x0]
    },
    'Blinking[Caterpillar Room Top Right]': {
        0x10A0B9: [0x0]
    },
    'Blinking[Red Brinstar Elevator]': {
        0x78256: [0x54, 0xc8, 0x06, 0x02, 0x10, 0x8c],
        0x1089F1: [0x0]
    },
    'Blinking[Crocomire Speedway Bottom]': {
        0x78B96: [0x4e, 0xc8, 0xc6, 0x2d, 0x4e, 0x8c],
        0x10AA8C: [0x0]
    },
    'Blinking[Crocomire Room Top]': {
        0x78B9E: [0x54, 0xc8, 0x36, 0x02, 0x4f, 0x8c],
        0x10BB30: [0x0]
    },
    'Blinking[Below Botwoon Energy Tank Right]': {
        0x10DD9A: [0x0]
    },
    'Blinking[West Sand Hall Left]': {
        0x10DACF: [0x0]
    },
    'Blinking[Aqueduct Top Left]': {
        0x10D3A9: [0x0]
    },
    'Blinking[Crab Shaft Right]': {
        0x7C4FB: [0x42, 0xc8, 0x1e, 0x36, 0x8f, 0x8c],
        0x10D005: [0x0]
    },
    'Blinking[RidleyRoomIn]': {
        0x78E98: [0x42, 0xc8, 0x0e, 0x06, 0x5a, 0x8c],
        0x10A638: [0x0]
    },
    'Blinking[DraygonRoomIn]': {
        0x7C7BB: [0x42, 0xc8, 0x1e, 0x06, 0x9e, 0x8c],
        0x10D356: [0x0]
    },
    'Blinking[PhantoonRoomIn]': {
        0x7C2B3: [0x48, 0xc8, 0x01, 0x06, 0x86, 0x8c],
        0x10CD16: [0x0]
    },
    'Blinking[KraidRoomIn]': {
        0x78A34: [0x48, 0xc8, 0x01, 0x16, 0x47, 0x8c],
        0x109F37: [0x0]
    },
    # only set blinking in "zebes asleep" room state to avoid having
    # the door blink when not needed
    # (only needed for escape peek in Crateria-less minimizer with disabled Tourian)
    'Blinking[Climb Bottom Left]': {
        0x782FE: [0x48, 0xc8, 0x01, 0x86, 0x12, 0x8c],
        0x108683: [0x0]
    },
    # Climb always in "zebes asleep" state, except during escape
    # (for escape peek in Crateria-less minimizer with disabled Tourian)
    'Climb_Asleep': {
        # replace "zebes awake" event ID with an unused event
        0x796CC: [0x7F],
        # put "Statues Hall" tension music
        0x796D6: [0x04]
    },
    # Indicator PLM IDs set to ffff because they're set dynamically
    'Indicator[KihunterBottom]': {
        0x78256: [0xff, 0xff, 0x06, 0x02, 0x0e, 0x00]
    },
    'Indicator[GreenHillZoneTopRight]': {
        0x78746: [0xff, 0xff, 0x01, 0x26, 0x30, 0x00]
    },
    # cancels the gamestate change by new_game.asm
    "Restore_Intro": {
        0x16EDA: [0x1E]
    }
}

additional_PLMs = {
    # for escape rando seeds
    "WS_Map_Grey_Door": {
        'room': 0Xcc6f,
        'plm_bytes_list': [
            [0x48, 0xc8, 0x1, 0x6, 0x61, 0x90]
        ]
    },
    "WS_Map_Grey_Door_Openable": {
        'room': 0Xcc6f,
        'plm_bytes_list': [
            [0x48, 0xc8, 0x1, 0x6, 0x61, 0x10]
        ]
    },
    # area/boss seeds
    # has to be applied along with WS_Main_Open_Grey
    "WS_Save_Blinking_Door": {
        'room': 0xcaf6,
        'state': 0xcb08,
        'plm_bytes_list': [
            [0x42, 0xC8, 0x4E, 0x36, 0x62, 0x0C]
        ]
    },
    # non standard start AP seeds (morph item is not in vanilla PLM list w/ zebes awake)
    "Morph_Zebes_Awake": {
        'room': 0x9e9f,
        'state': 0x9ecb,
        'plm_bytes_list': [
            [0xff, 0xff, 0x45, 0x29, 0x1A, 0x00]
        ],
        'locations': [("Morphing Ball", 0)]
    },
    # seal west/east maridia connection in area rando
    'Maridia Sand Hall Seal': {
        'room': 0xd252,
        'plm_bytes_list': [
            [0x42, 0xc8, 0x0e, 0x06, 0x63, 0x90]
        ]
    },
    # custom save points for non standard start APs
    "Save_G4": {
        "room": 0xa5ed,
        'plm_bytes_list': [
            [0x6F, 0xB7, 0x3D, 0x0C, 0x07, 0x00]
        ]
    },
    "Save_Gauntlet": {
        "room": 0x99bd,
        'plm_bytes_list': [
            [0x6F, 0xB7, 0x0C, 0x0A, 0x06, 0x00]
        ]
    },
    "Save_Watering_Hole": {
        "room": 0xd13b,
        'plm_bytes_list': [
            [0x6F, 0xB7, 0x14, 0x0A, 0x07, 0x00]
        ]
    },
    "Save_Mama": {
        "room": 0xd055,
        'plm_bytes_list': [
            [0x6F, 0xB7, 0x26, 0x0B, 0x06, 0x00]
        ]
    },
    "Save_Aqueduct": {
        "room": 0xd5a7,
        'plm_bytes_list': [
            [0x6F, 0xB7, 0x59, 0x09, 0x05, 0x00]
        ]
    },
    "Save_Etecoons": {
        "room": 0xa051,
        'plm_bytes_list': [
            [0x6F, 0xB7, 0x04, 0x0B, 0x07, 0x00]
        ]
    },
    "Save_Firefleas": {
        "room": 0xb55a,
        'plm_bytes_list': [
            [0x6F, 0xB7, 0x07, 0x09, 0x07, 0x00]
        ]
    },
    # additional saves in west maridia for area rando
    "Save_Crab_Shaft": {
        "room": 0xd1a3,
        'plm_bytes_list': [
            [0x6F, 0xB7, 0x0D, 0x29, 0x09, 0x00]
        ]
    },
    "Save_Main_Street": {
        "room": 0xcfc9,
        'plm_bytes_list': [
            [0x6F, 0xB7, 0x18, 0x59, 0x0A, 0x00]
        ]
    },
    # blinking doors for area APs
    'Blinking[Moat Right]': {
        'room': 0x95ff,
        'plm_bytes_list': [
            [0x42, 0xc8, 0x1e, 0x06, 0x63, 0x8c]
        ]
    },
    'Blinking[Lower Mushrooms Left]': {
        'room': 0x9969,
        'plm_bytes_list': [
            [0x48, 0xc8, 0x01, 0x06, 0x63, 0x8c]
        ]
    },
    'Blinking[Golden Four]': {
        'room': 0xa5ed,
        'plm_bytes_list': [
            [0x48, 0xc8, 0x01, 0x06, 0x63, 0x8c]
        ]
    },
    'Blinking[Green Brinstar Elevator]': {
        'room': 0x9938,
        'plm_bytes_list': [
            [0x42, 0xc8, 0x0e, 0x06, 0x63, 0x8c]
        ]
    },
    'Blinking[Warehouse Zeela Room Left]': {
        'room': 0xa471,
        'plm_bytes_list': [
            [0x48, 0xc8, 0x01, 0x06, 0x63, 0x8c]
        ]
    },
    'Blinking[Warehouse Entrance Right]': {
        'room': 0xa6a1,
        'plm_bytes_list': [
            [0x48, 0xc8, 0x01, 0x06, 0x63, 0x8c]
        ]
    },
    'Blinking[Warehouse Entrance Left]': {
        'room': 0xa6a1,
        'plm_bytes_list': [
            [0x42, 0xc8, 0x2e, 0x06, 0x63, 0x8c]
        ]
    },
    'Blinking[Single Chamber Top Right]': {
        'room': 0xad5e,
        'plm_bytes_list': [
            [0x42, 0xc8, 0x5e, 0x06, 0x63, 0x8c]
        ]
    },
    'Blinking[Three Muskateers Room Left]': {
        'room': 0xb656,
        'plm_bytes_list': [
            [0x48, 0xc8, 0x11, 0x06, 0x63, 0x8c]
        ]
    },
    'Blinking[Lava Dive Right]': {
        'room': 0xaf14,
        'plm_bytes_list': [
            [0x42, 0xc8, 0x3e, 0x06, 0x63, 0x8c]
        ]
    },
    'Blinking[West Ocean Left]': {
        'room': 0x93fe,
        'plm_bytes_list': [
            [0x48, 0xc8, 0x01, 0x46, 0x63, 0x8c]
        ]
    },
    'Blinking[Crab Maze Left]': {
        'room': 0x957d,
        'plm_bytes_list': [
            [0x48, 0xc8, 0x01, 0x16, 0x63, 0x8c]
        ]
    },
    'Blinking[Crab Hole Bottom Left]': {
        'room': 0xd21c,
        'plm_bytes_list': [
            [0x48, 0xc8, 0x01, 0x16, 0x63, 0x8c]
        ]
    },
    'Blinking[Main Street Bottom]': {
        'room': 0xcfc9,
        'plm_bytes_list': [
            [0x4e, 0xc8, 0x16, 0x7d, 0x63, 0x8c]
        ]
    },
    'Blinking[Red Fish Room Left]': {
        'room': 0xd104,
        'plm_bytes_list': [
            [0x48, 0xc8, 0x01, 0x06, 0x63, 0x8c]
        ]
    },
    'Blinking[East Tunnel Top Right]': {
        'room': 0xcf80,
        'plm_bytes_list': [
            [0x42, 0xc8, 0x3e, 0x06, 0x63, 0x8c]
        ]
    },
    'Blinking[East Tunnel Right]': {
        'room': 0xcf80,
        'plm_bytes_list': [
            [0x42, 0xc8, 0x0e, 0x16, 0x63, 0x8c]
        ]
    },
    'Blinking[Glass Tunnel Top]': {
        'room': 0xcefb,
        'plm_bytes_list': [
            [0x54, 0xc8, 0x06, 0x02, 0x63, 0x8c]
        ]
    },
    'Blinking[Red Tower Top Left]': {
        'room': 0xa253,
        'plm_bytes_list': [
            [0x48, 0xc8, 0x01, 0x46, 0x63, 0x8c]
        ]
    },
    'Blinking[Caterpillar Room Top Right]': {
        'room': 0xa322,
        'plm_bytes_list': [
            [0x42, 0xc8, 0x2e, 0x36, 0x63, 0x8c]
        ]
    },
    'Blinking[Below Botwoon Energy Tank Right]': {
        'room': 0xd6fd,
        'plm_bytes_list': [
            [0x42, 0xc8, 0x3e, 0x06, 0x63, 0x8c]
        ]
    },
    'Blinking[West Sand Hall Left]': {
        'room': 0xd461,
        'plm_bytes_list': [
            [0x48, 0xc8, 0x01, 0x06, 0x63, 0x8c]
        ]
    },
    'Blinking[Aqueduct Top Left]': {
        'room': 0xd5a7,
        'plm_bytes_list': [
            [0x48, 0xc8, 0x01, 0x16, 0x63, 0x8c]
        ]
    },
    # Indicator PLM IDs set to ffff because they're set dynamically
    'Indicator[LandingSiteRight]': {
        'room': 0x948c,
        'plm_bytes_list': [
            [0xff, 0xff, 0x01, 0x06, 0x00, 0x00]
        ]
    },
    'Indicator[KihunterRight]': {
        'room': 0x95ff,
        'plm_bytes_list': [
            [0xff, 0xff, 0x01, 0x06, 0x0d, 0x00]
        ]
    },
    'Indicator[NoobBridgeRight]': {
        'room': 0xa253,
        'plm_bytes_list': [
            [0xff, 0xff, 0x01, 0x46, 0x33, 0x00]
        ]
    },
    'Indicator[MainShaftBottomRight]': {
        'room': 0x9cb3,
        'plm_bytes_list': [
            [0xff, 0xff, 0x01, 0x06, 0x22, 0x00]
        ]
    },
    'Indicator[BigPinkBottomRight]': {
        'room': 0x9e52,
        'plm_bytes_list': [
            [0xff, 0xff, 0x01, 0x06, 0x29, 0x00]
        ]
    },
    'Indicator[RedTowerElevatorLeft]': {
        'room': 0xa2f7,
        'plm_bytes_list': [
            [0xff, 0xff, 0x2e, 0x06, 0x3c, 0x00]
        ]
    },
    'Indicator[WestOceanRight]': {
        'room': 0xca08,
        'plm_bytes_list': [
            [0xff, 0xff, 0x01, 0x06, 0x0c, 0x00]
        ]
    },
    'Indicator[LeCoudeBottom]': {
        'room': 0x94cc,
        'plm_bytes_list': [
            [0xff, 0xff, 0x06, 0x02, 0x0f, 0x00]
        ]
    },
    'Indicator[WreckedShipMainShaftBottom]': {
        'room': 0xcc6f,
        'plm_bytes_list': [
            [0xff, 0xff, 0x26, 0x02, 0x84, 0x00]
        ]
    },
    'Indicator[CathedralEntranceRight]': {
        'room': 0xa788,
        'plm_bytes_list': [
            [0xff, 0xff, 0x01, 0x06, 0x4a, 0x00]
        ]
    },
    'Indicator[CathedralRight]': {
        'room': 0xafa3,
        'plm_bytes_list': [
            [0xff, 0xff, 0x01, 0x06, 0x49, 0x00]
        ]
    },
    'Indicator[RedKihunterShaftBottom]': {
        'room': 0xb5d5,
        'plm_bytes_list': [
            [0xff, 0xff, 0x56, 0x02, 0x5e, 0x00]
        ]
    },
    'Indicator[WastelandLeft]': {
        'room': 0xb62b,
        'plm_bytes_list': [
            [0xff, 0xff, 0x2e, 0x06, 0x5f, 0x00]
        ]
    },
    'Indicator[MainStreetBottomRight]': {
        'room': 0xd08a,
        'plm_bytes_list': [
            [0xff, 0xff, 0x01, 0x06, 0x8d, 0x00]
        ]
    },
    'Indicator[CrabShaftRight]': {
        'room': 0xd5a7,
        'plm_bytes_list': [
            [0xff, 0xff, 0x01, 0x16, 0x8f, 0x00]
        ]
    },
    'Indicator[ColosseumBottomRight]': {
        'room': 0xd78f,
        'plm_bytes_list': [
            [0xff, 0xff, 0x01, 0x06, 0x9a, 0x00]
        ]
    }
}
