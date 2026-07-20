from ..roomEditor import RoomEditor, Object, ObjectWarp, ObjectHorizontal
from ..assembler import ASM
from ..locations import constants
from typing import List


# Room containing the boss
BOSS_ROOMS = [
    0x106,
    0x12b,
    0x15a,
    0x166,
    0x185,
    0x1bc,
    0x223,  # Note: unused room normally
    0x234,
    0x300,
]
BOSS_ENTITIES = [
    (3, 2, 0x59),
    (4, 2, 0x5C),
    (4, 3, 0x5B),
    None,
    (4, 3, 0x5D),
    (4, 3, 0x5A),
    None,
    (4, 3, 0x62),
    (5, 2, 0xF9),
]
MINIBOSS_ENTITIES = {
    "ROLLING_BONES":    [(8, 3, 0x81), (6, 3, 0x82)],
    "HINOX":            [(5, 2, 0x89)],
    "DODONGO":          [(3, 2, 0x60), (5, 2, 0x60)],
    "CUE_BALL":         [(1, 1, 0x8e)],
    "GHOMA":            [(2, 1, 0x5e), (2, 4, 0x5e)],
    "SMASHER":          [(5, 2, 0x92)],
    "GRIM_CREEPER":     [(4, 0, 0xbc)],
    "BLAINO":           [(5, 3, 0xbe)],
    "AVALAUNCH":        [(5, 1, 0xf4)],
    "GIANT_BUZZ_BLOB":  [(4, 2, 0xf8)],
    "MOBLIN_KING":      [(5, 5, 0xe4)],
    "ARMOS_KNIGHT":     [(4, 3, 0x88)],
}
MINIBOSS_ROOMS = {
    "0": 0x111, "1": 0x128, "2": 0x145, "3": 0x164, "4": 0x193, "5": 0x1C5, "6": 0x228, "7": 0x23F,
    "c1": 0x30C, "c2": 0x303,
    "moblin_cave": 0x2E1,
    "armos_temple": 0x27F,
}


def fixArmosKnightAsMiniboss(rom):
    # Make the armos temple room with armos knight drop a ceiling key on kill.
    # This makes the door always open, but that's fine.
    rom.patch(0x14, 0x017F, "21", "81")

    # Do not change the drop from Armos knight into a ceiling key.
    rom.patch(0x06, 0x12E8, ASM("ld [hl], $30"), "", fill_nop=True)


def getBossRoomStatusFlagLocation(dungeon_nr):
    if BOSS_ROOMS[dungeon_nr] >= 0x300:
        return 0xDDE0 - 0x300 + BOSS_ROOMS[dungeon_nr]
    return 0xD800 + BOSS_ROOMS[dungeon_nr]


def fixDungeonItem(item_chest_id, dungeon_nr):
    if item_chest_id == constants.CHEST_ITEMS[constants.MAP]:
        return constants.CHEST_ITEMS["MAP%d" % (dungeon_nr + 1)]
    if item_chest_id == constants.CHEST_ITEMS[constants.COMPASS]:
        return constants.CHEST_ITEMS["COMPASS%d" % (dungeon_nr + 1)]
    if item_chest_id == constants.CHEST_ITEMS[constants.KEY]:
        return constants.CHEST_ITEMS["KEY%d" % (dungeon_nr + 1)]
    if item_chest_id == constants.CHEST_ITEMS[constants.NIGHTMARE_KEY]:
        return constants.CHEST_ITEMS["NIGHTMARE_KEY%d" % (dungeon_nr + 1)]
    if item_chest_id == constants.CHEST_ITEMS[constants.STONE_BEAK]:
        return constants.CHEST_ITEMS["STONE_BEAK%d" % (dungeon_nr + 1)]
    return item_chest_id


def getCleanBossRoom(rom, dungeon_nr):
    re = RoomEditor(rom, BOSS_ROOMS[dungeon_nr])
    new_objects = []
    for obj in re.objects:
        if isinstance(obj, ObjectWarp):
            continue
        if obj.type_id == 0xBE:  # Remove staircases
            continue
        if obj.type_id == 0x06:  # Remove lava
            continue
        if obj.type_id == 0x1c:  # Change D1 pits into normal pits
            obj.type_id = 0x01
        if obj.type_id == 0x1e:  # Change D1 pits into normal pits
            obj.type_id = 0xaf
        if obj.type_id == 0x1f:  # Change D1 pits into normal pits
            obj.type_id = 0xb0
        if obj.type_id == 0xF5:  # Change open doors into closing doors.
            obj.type_id = 0xF1
        new_objects.append(obj)


    # Make D4 room a valid fighting room by removing most content.
    if dungeon_nr == 3:
        new_objects = new_objects[:2] + [Object(1, 1, 0xAC), Object(8, 1, 0xAC), Object(1, 6, 0xAC), Object(8, 6, 0xAC)]

    # D7 has an empty room we use for most bosses, but it needs some adjustments.
    if dungeon_nr == 6:
        # Move around the unused and instrument room.
        rom.banks[0x14][0x03a0 + 6 + 1 * 8] = 0x00
        rom.banks[0x14][0x03a0 + 7 + 2 * 8] = 0x2C
        rom.banks[0x14][0x03a0 + 7 + 3 * 8] = 0x23
        rom.banks[0x14][0x03a0 + 6 + 5 * 8] = 0x00

        rom.banks[0x14][0x0520 + 7 + 2 * 8] = 0x2C
        rom.banks[0x14][0x0520 + 7 + 3 * 8] = 0x23
        rom.banks[0x14][0x0520 + 6 + 5 * 8] = 0x00

        re.floor_object &= 0x0F
        new_objects += [
            Object(4, 0, 0xF0),
            Object(1, 6, 0xBE),
            ObjectWarp(1, dungeon_nr, 0x22E, 24, 16)
        ]

        # Set the stairs towards the eagle tower top to our new room.
        r = RoomEditor(rom, 0x22E)
        r.objects[-1] = ObjectWarp(1, dungeon_nr, re.room, 24, 112)
        r.store(rom)

        # Remove the normal door to the instrument room
        r = RoomEditor(rom, 0x22e)
        r.removeObject(4, 0)
        r.store(rom)
        rom.banks[0x14][0x22e - 0x100] = 0x00

        r = RoomEditor(rom, 0x22c)
        r.changeObject(0, 7, 0x03)
        r.changeObject(2, 7, 0x03)
        r.store(rom)

    re.objects = new_objects
    re.entities = []
    return re


def changeBosses(rom, mapping: List[int]):
    # Fix the color dungeon not properly warping to room 0 with the boss.
    for addr in range(0x04E0, 0x04E0 + 64):
        if rom.banks[0x14][addr] == 0x00 and addr not in {0x04E0 + 1 + 3 * 8, 0x04E0 + 2 + 6 * 8}:
            rom.banks[0x14][addr] = 0xFF
    # Fix the genie death not really liking pits/water.
    rom.patch(0x04, 0x0521, ASM("ld [hl], $81"), ASM("ld [hl], $91"))

    # For the sidescroll bosses, we need to update this check to be the evil eagle dungeon.
    # But if evil eagle is not there we still need to remove this check to make angler fish work in D7
    dungeon_nr = mapping.index(6) if 6 in mapping else 0xFE
    rom.patch(0x02, 0x1FC8, ASM("cp $06"), ASM("cp $%02x" % (dungeon_nr if dungeon_nr < 8 else 0xff)))

    for dungeon_nr in range(9):
        target = mapping[dungeon_nr]
        if target == dungeon_nr:
            continue

        if target == 3:  # D4 fish boss
            # If dungeon_nr == 6: use normal eagle door towards fish.
            if dungeon_nr == 6:
                # Add the staircase to the boss, and fix the warp back.
                re = RoomEditor(rom, 0x22E)
                for obj in re.objects:
                    if isinstance(obj, ObjectWarp):
                        obj.type_id = 2
                        obj.map_nr = 3
                        obj.room = 0x1EF
                        obj.target_x = 24
                        obj.target_y = 16
                re.store(rom)
                re = RoomEditor(rom, 0x1EF)
                re.objects[-1] = ObjectWarp(1, dungeon_nr if dungeon_nr < 8 else 0xff, 0x22E, 24, 16)
                re.store(rom)
            else:
                # Set the proper room event flags
                rom.banks[0x14][BOSS_ROOMS[dungeon_nr] - 0x100] = 0x2A

                # Add the staircase to the boss, and fix the warp back.
                re = getCleanBossRoom(rom, dungeon_nr)
                re.objects += [Object(4, 4, 0xBE), ObjectWarp(2, 3, 0x1EF, 24, 16)]
                re.store(rom)
                re = RoomEditor(rom, 0x1EF)
                re.objects[-1] = ObjectWarp(1, dungeon_nr if dungeon_nr < 8 else 0xff, BOSS_ROOMS[dungeon_nr], 72, 80)
                re.store(rom)

            # Patch the fish heart container to open up the right room.
            if dungeon_nr == 6:
                rom.patch(0x03, 0x1A0F, ASM("ld hl, $D966"), ASM("ld hl, $%04x" % (0xD800 + 0x22E)))
            else:
                rom.patch(0x03, 0x1A0F, ASM("ld hl, $D966"), ASM("ld hl, $%04x" % (getBossRoomStatusFlagLocation(dungeon_nr))))

            # Patch the proper item towards the D4 boss
            rom.banks[0x3E][0x3800 + 0x01ff] = fixDungeonItem(rom.banks[0x3E][0x3800 + BOSS_ROOMS[dungeon_nr]], dungeon_nr)
            rom.banks[0x3E][0x3300 + 0x01ff] = fixDungeonItem(rom.banks[0x3E][0x3300 + BOSS_ROOMS[dungeon_nr]], dungeon_nr)
        elif target == 6:  # Evil eagle
            rom.banks[0x14][BOSS_ROOMS[dungeon_nr] - 0x100] = 0x2A

            # Patch the eagle heart container to open up the right room.
            rom.patch(0x03, 0x1A04, ASM("ld hl, $DA2E"), ASM("ld hl, $%04x" % (getBossRoomStatusFlagLocation(dungeon_nr))))

            # Add the staircase to the boss, and fix the warp back.
            re = getCleanBossRoom(rom, dungeon_nr)
            re.objects += [Object(4, 4, 0xBE), ObjectWarp(2, 6, 0x2F8, 72, 80)]
            re.store(rom)
            re = RoomEditor(rom, 0x2F8)
            re.objects[-1] = ObjectWarp(1, dungeon_nr if dungeon_nr < 8 else 0xff, BOSS_ROOMS[dungeon_nr], 72, 80)
            re.store(rom)

            # Patch the proper item towards the D7 boss
            rom.banks[0x3E][0x3800 + 0x02E8] = fixDungeonItem(rom.banks[0x3E][0x3800 + BOSS_ROOMS[dungeon_nr]], dungeon_nr)
            rom.banks[0x3E][0x3300 + 0x02E8] = fixDungeonItem(rom.banks[0x3E][0x3300 + BOSS_ROOMS[dungeon_nr]], dungeon_nr)
        else:
            rom.banks[0x14][BOSS_ROOMS[dungeon_nr] - 0x100] = 0x21
            re = getCleanBossRoom(rom, dungeon_nr)
            re.entities = [BOSS_ENTITIES[target]]

            if target == 4:
                # For slime eel, we need to setup the right wall tiles.
                rom.banks[0x20][0x2EB3 + BOSS_ROOMS[dungeon_nr] - 0x100] = 0x06
            if target == 5:
                # Patch facade so he doesn't use the spinning tiles, which is a problem for the sprites.
                rom.patch(0x04, 0x121D, ASM("cp $14"), ASM("cp $00"))
                rom.patch(0x04, 0x1226, ASM("cp $04"), ASM("cp $00"))
                rom.patch(0x04, 0x127F, ASM("cp $14"), ASM("cp $00"))
            if target == 7:
                pass
                # For hot head, add some lava (causes graphical glitches)
                # re.animation_id = 0x06
                # re.objects += [
                #     ObjectHorizontal(3, 2, 0x06, 4),
                #     ObjectHorizontal(2, 3, 0x06, 6),
                #     ObjectHorizontal(2, 4, 0x06, 6),
                #     ObjectHorizontal(3, 5, 0x06, 4),
                # ]

            re.store(rom)


def readBossMapping(rom):
    mapping = []
    for dungeon_nr in range(9):
        r = RoomEditor(rom, BOSS_ROOMS[dungeon_nr])
        if r.entities:
            mapping.append(BOSS_ENTITIES.index(r.entities[0]))
        elif isinstance(r.objects[-1], ObjectWarp) and r.objects[-1].room == 0x1ef:
            mapping.append(3)
        elif isinstance(r.objects[-1], ObjectWarp) and r.objects[-1].room == 0x2f8:
            mapping.append(6)
        else:
            mapping.append(dungeon_nr)
    return mapping


def changeMiniBosses(rom, mapping):
    # Fix avalaunch not working when entering a room from the left or right
    rom.patch(0x03, 0x0BE0, ASM("""
        ld  [hl], $50
        ld  hl, $C2D0
        add hl, bc
        ld  [hl], $00
        jp  $4B56
    """), ASM("""
        ld  a, [hl]
        sub $08
        ld  [hl], a    
        ld  hl, $C2D0
        add hl, bc
        ld  [hl], b ; b is always zero here
        ret
    """), fill_nop=True)
    # Fix avalaunch waiting until the room event is done (and not all rooms have a room event on enter)
    rom.patch(0x36, 0x1C14, ASM("ret z"), "", fill_nop=True)
    # Fix giant buzz blob waiting until the room event is done (and not all rooms have a room event on enter)
    rom.patch(0x36, 0x153B, ASM("ret z"), "", fill_nop=True)

    # Remove the powder fairy from giant buzz blob
    rom.patch(0x36, 0x14F7, ASM("jr nz, $05"), ASM("jr $05"))

    # Do not allow the force barrier in D3 dodongo room
    rom.patch(0x14, 0x14AC, 0x14B5, ASM("jp $7FE0"), fill_nop=True)
    rom.patch(0x14, 0x3FE0, "00" * 0x20, ASM("""
        ld  a, [$C124] ; room transition
        ld  hl, $C17B
        or  [hl]
        ret nz
        ldh a, [$F6] ; room
        cp  $45 ; check for D3 dodogo room
        ret z
        cp  $7F ; check for armos temple room
        ret z
        jp  $54B5
    """), fill_nop=True)

    # Patch smasher to spawn the ball closer, so it doesn't spawn on the wall in the armos temple
    rom.patch(0x06, 0x0533, ASM("add a, $30"), ASM("add a, $20"))

    for target, name in mapping.items():
        re = RoomEditor(rom, MINIBOSS_ROOMS[target])
        re.entities = [e for e in re.entities if e[2] == 0x61]  # Only keep warp, if available
        re.entities += MINIBOSS_ENTITIES[name]

        if re.room == 0x228 and name != "GRIM_CREEPER":
            for x in range(3, 7):
                for y in range(0, 3):
                    re.removeObject(x, y)

        if name == "CUE_BALL":
            re.objects += [
                Object(3, 3, 0x2c),
                ObjectHorizontal(4, 3, 0x22, 2),
                Object(6, 3, 0x2b),
                Object(3, 4, 0x2a),
                ObjectHorizontal(4, 4, 0x21, 2),
                Object(6, 4, 0x29),
            ]
        if name == "BLAINO":
            # BLAINO needs a warp object to hit you to the entrance of the dungeon.
            if len(re.getWarps()) < 1:
                # Default to start house.
                target = (0x10, 0x2A3, 0x50, 0x7c)
                if 0x100 <= re.room < 0x11D: #D1
                    target = (0, 0x117, 80, 80)
                elif 0x11D <= re.room < 0x140: #D2
                    target = (1, 0x136, 80, 80)
                elif 0x140 <= re.room < 0x15D: #D3
                    target = (2, 0x152, 80, 80)
                elif 0x15D <= re.room < 0x180: #D4
                    target = (3, 0x174, 80, 80)
                elif 0x180 <= re.room < 0x1AC: #D5
                    target = (4, 0x1A1, 80, 80)
                elif 0x1B0 <= re.room < 0x1DE: #D6
                    target = (5, 0x1D4, 80, 80)
                elif 0x200 <= re.room < 0x22D: #D7
                    target = (6, 0x20E, 80, 80)
                elif 0x22D <= re.room < 0x26C: #D8
                    target = (7, 0x25D, 80, 80)
                elif re.room >= 0x300: #D0
                    target = (0xFF, 0x312, 80, 80)
                elif re.room == 0x2E1: #Moblin cave
                    target = (0x15, 0x2F0, 0x50, 0x7C)
                elif re.room == 0x27F: #Armos temple
                    target = (0x16, 0x28F, 0x50, 0x7C)
                re.objects.append(ObjectWarp(1, *target))
        if name == "DODONGO":
            # Remove breaking floor tiles from the room.
            re.objects = [obj for obj in re.objects if obj.type_id != 0xDF]
        if name == "ROLLING_BONES" and target == 2:
            # Make rolling bones pass trough walls so it does not get stuck here.
            rom.patch(0x03, 0x02F1 + 0x81, "84", "95")
        re.store(rom)


def readMiniBossMapping(rom):
    mapping = {}
    for key, room in MINIBOSS_ROOMS.items():
        r = RoomEditor(rom, room)
        for me_key, me_data in MINIBOSS_ENTITIES.items():
            if me_data[-1][2] == r.entities[-1][2]:
                mapping[key] = me_key
    return mapping


def doubleTrouble(rom):
    for n in range(0x316):
        if n == 0x2FF:
            continue
        re = RoomEditor(rom, n)
        # Bosses
        if re.hasEntity(0x59):  # Moldorm (TODO; double heart container drop)
            re.removeEntities(0x59)
            re.entities += [(3, 2, 0x59), (4, 2, 0x59)]
            re.store(rom)
        if re.hasEntity(0x5C):  # Ghini
            re.removeEntities(0x5C)
            re.entities += [(3, 2, 0x5C), (4, 2, 0x5C)]
            re.store(rom)
        if re.hasEntity(0x5B):  # slime eye
            re.removeEntities(0x5B)
            re.entities += [(3, 2, 0x5B), (6, 2, 0x5B)]
            re.store(rom)
        if re.hasEntity(0x65):  # angler fish
            re.removeEntities(0x65)
            re.entities += [(6, 2, 0x65), (6, 5, 0x65)]
            re.store(rom)
        # Slime eel bugs out on death if duplicated.
        # if re.hasEntity(0x5D):  # slime eel
        #     re.removeEntities(0x5D)
        #     re.entities += [(6, 2, 0x5D), (6, 5, 0x5D)]
        #     re.store(rom)
        if re.hasEntity(0x5A):  # facade (TODO: Drops two hearts, shared health?)
            re.removeEntities(0x5A)
            re.entities += [(2, 3, 0x5A), (6, 3, 0x5A)]
            re.store(rom)
        # Evil eagle causes a crash, and messes up the intro sequence and generally is just a mess if I spawn multiple
        # if re.hasEntity(0x63):  # evil eagle
        #     re.removeEntities(0x63)
        #     re.entities += [(3, 4, 0x63), (2, 4, 0x63)]
        #     re.store(rom)
        #     # Remove that links movement is blocked
        #     rom.patch(0x05, 0x2258, ASM("ldh [$A1], a"), "0000")
        #     rom.patch(0x05, 0x1AE3, ASM("ldh [$A1], a"), "0000")
        #     rom.patch(0x05, 0x1C5D, ASM("ldh [$A1], a"), "0000")
        #     rom.patch(0x05, 0x1C8D, ASM("ldh [$A1], a"), "0000")
        #     rom.patch(0x05, 0x1CAF, ASM("ldh [$A1], a"), "0000")
        if re.hasEntity(0x62):  # hot head (TODO: Drops thwo hearts)
            re.removeEntities(0x62)
            re.entities += [(2, 2, 0x62), (4, 4, 0x62)]
            re.store(rom)
        if re.hasEntity(0xF9):  # hardhit beetle
            re.removeEntities(0xF9)
            re.entities += [(2, 2, 0xF9), (5, 4, 0xF9)]
            re.store(rom)
        # Minibosses
        if re.hasEntity(0x89):
            re.removeEntities(0x89)
            re.entities += [(2, 3, 0x89), (6, 3, 0x89)]
            re.store(rom)
        if re.hasEntity(0x81):
            re.removeEntities(0x81)
            re.entities += [(2, 3, 0x81), (6, 3, 0x81)]
            re.store(rom)
        if re.hasEntity(0x60):
            dodongo = [e for e in re.entities if e[2] == 0x60]
            x = (dodongo[0][0] + dodongo[1][0]) // 2
            y = (dodongo[0][1] + dodongo[1][1]) // 2
            re.entities += [(x, y, 0x60)]
            re.store(rom)
        if re.hasEntity(0x8e):
            re.removeEntities(0x8e)
            re.entities += [(1, 1, 0x8e), (7, 1, 0x8e)]
            re.store(rom)
        if re.hasEntity(0x92):
            re.removeEntities(0x92)
            re.entities += [(2, 3, 0x92), (4, 3, 0x92)]
            re.store(rom)
        if re.hasEntity(0xf4):
            re.removeEntities(0xf4)
            re.entities += [(2, 1, 0xf4), (6, 1, 0xf4)]
            re.store(rom)
        if re.hasEntity(0xf8):
            re.removeEntities(0xf8)
            re.entities += [(2, 2, 0xf8), (6, 2, 0xf8)]
            re.store(rom)
        if re.hasEntity(0xe4):
            re.removeEntities(0xe4)
            re.entities += [(5, 2, 0xe4), (5, 5, 0xe4)]
            re.store(rom)

        if re.hasEntity(0x88): # Armos knight (TODO: double item drop)
            re.removeEntities(0x88)
            re.entities += [(3, 3, 0x88), (6, 3, 0x88)]
            re.store(rom)
        if re.hasEntity(0x87): # Lanmola (TODO: killing one drops the item, and marks as done)
            re.removeEntities(0x87)
            re.entities += [(2, 2, 0x87), (1, 1, 0x87)]
            re.store(rom)
