from ..assembler import ASM
from ..entranceInfo import ENTRANCE_INFO
from ..roomEditor import RoomEditor, ObjectWarp, ObjectHorizontal
from ..backgroundEditor import BackgroundEditor
from .. import utils


def bugfixWrittingWrongRoomStatus(rom):
    # The normal rom contains a pretty nasty bug where door closing triggers in D7/D8 can effect doors in
    # dungeons D1-D6. This fix should prevent this.
    rom.patch(0x02, 0x1D21, 0x1D3C, ASM("call $5B9F"), fill_nop=True)

def fixEggDeathClearingItems(rom):
    rom.patch(0x01, 0x1E79, ASM("cp $0A"), ASM("cp $08"))

def fixWrongWarp(rom):
    rom.patch(0x00, 0x18CE, ASM("cp $04"), ASM("cp $03"))
    re = RoomEditor(rom, 0x2b)
    for x in range(10):
        re.removeObject(x, 7)
    re.objects.append(ObjectHorizontal(0, 7, 0x2C, 10))
    while len(re.getWarps()) < 4:
        re.objects.append(ObjectWarp(1, 3, 0x7a, 80, 124))
    re.store(rom)

def bugfixBossroomTopPush(rom):
    rom.patch(0x14, 0x14D9, ASM("""
        ldh  a, [$99]
        dec  a
        ldh  [$99], a
    """), ASM("""
        jp   $7F80
    """), fill_nop=True)
    rom.patch(0x14, 0x3F80, "00" * 0x80, ASM("""
        ldh  a, [$99]
        cp   $50
        jr   nc, up
down:
        inc  a
        ldh  [$99], a
        jp   $54DE
up:
        dec  a
        ldh  [$99], a
        jp   $54DE
    """), fill_nop=True)

def bugfixPowderBagSprite(rom):
    rom.patch(0x03, 0x2055, "8E16", "0E1E")

def easyColorDungeonAccess(rom):
    re = RoomEditor(rom, 0x312)
    re.entities = [(3, 1, 246), (6, 1, 247)]
    re.store(rom)

def removeGhost(rom):
    ## Ghost patch
    # Do not have the ghost follow you after dungeon 4
    rom.patch(0x03, 0x1E1B, ASM("LD [$DB79], A"), "", fill_nop=True)

def alwaysAllowSecretBook(rom):
    rom.patch(0x15, 0x3F23, ASM("ld a, [$DB0E]\ncp $0E"), ASM("xor a\ncp $00"), fill_nop=True)
    rom.patch(0x15, 0x3F2A, 0x3F30, "", fill_nop=True)

def cleanup(rom):
    # Remove unused rooms to make some space in the rom
    re = RoomEditor(rom, 0x2C4)
    re.objects = []
    re.entities = []
    re.store(rom, 0x2C4)
    re.store(rom, 0x2D4)
    re.store(rom, 0x277)
    re.store(rom, 0x278)
    re.store(rom, 0x279)
    re.store(rom, 0x1ED)
    re.store(rom, 0x1FC)  # Beta room

    rom.texts[0x02B] = b'' # unused text


def disablePhotoPrint(rom):
    rom.patch(0x28, 0x07CC, ASM("ldh [$01], a\nldh [$02], a"), "", fill_nop=True) # do not reset the serial link
    rom.patch(0x28, 0x0483, ASM("ld a, $13"), ASM("jr $EA", 0x4483)) # Do not print on A press, but jump to cancel
    rom.patch(0x28, 0x0492, ASM("ld hl, $4439"), ASM("ret"), fill_nop=True) # Do not show the print/cancel overlay

def fixMarinFollower(rom):
    # Allow opening of D0 with marin
    rom.patch(0x02, 0x3402, ASM("ld a, [$DB73]"), ASM("xor a"), fill_nop=True)
    # Instead of uselessly checking for sidescroller rooms for follower spawns, check for color dungeon instead
    rom.patch(0x01, 0x1FCB, 0x1FD3, ASM("cp $FF\nret z"), fill_nop=True)
    # Do not load marin graphics in color dungeon
    rom.patch(0x00, 0x2EA6, 0x2EB0, ASM("cp $FF\njp $2ED3"), fill_nop=True)
    # Fix marin on taltal bridge causing a lockup if you have marin with you
    # This changes the location where the index to the marin entity is stored from it's normal location
    # To the memory normal reserved for progress on the egg maze (which is reset to 0 on a warp)
    rom.patch(0x18, 0x1EF7, ASM("ld [$C50F], a"), ASM("ld [$C5AA], a"))
    rom.patch(0x18, 0x2126, ASM("ld a, [$C50F]"), ASM("ld a, [$C5AA]"))
    rom.patch(0x18, 0x2139, ASM("ld a, [$C50F]"), ASM("ld a, [$C5AA]"))
    rom.patch(0x18, 0x214F, ASM("ld a, [$C50F]"), ASM("ld a, [$C5AA]"))
    rom.patch(0x18, 0x2166, ASM("ld a, [$C50F]"), ASM("ld a, [$C5AA]"))

def quickswap(rom, button):
    rom.patch(0x00, 0x1094, ASM("jr c, $49"), ASM("jr nz, $49"))  # prevent agressive key repeat
    rom.patch(0x00, 0x10BC,  # Patch the open minimap code to swap the your items instead
        ASM("xor a\nld [$C16B], a\nld [$C16C], a\nld [$DB96], a\nld a, $07\nld [$DB95], a"), ASM("""
        ld a, [$DB%02X]
        ld e, a
        ld a, [$DB%02X]
        ld [$DB%02X], a
        ld a, e
        ld [$DB%02X], a
        ret
    """ % (button, button + 2, button, button + 2)))

def injectMainLoop(rom):
    rom.patch(0x00, 0x0346, ASM("""
        ldh  a, [$FE]
        and  a
        jr   z, $08
    """), ASM("""
        ; Call the mainloop handler
        xor  a
        rst  8
    """), fill_nop=True)

def warpHome(rom):
    # Patch the S&Q menu to allow 3 options
    rom.patch(0x01, 0x012A, 0x0150, ASM("""
        ld   hl, $C13F
        call $6BA8 ; make sound on keypress
        ldh  a, [$CC] ; load joystick status
        and  $04      ; if up
        jr   z, noUp
        dec  [hl]
noUp:
        ldh  a, [$CC] ; load joystick status
        and  $08      ; if down
        jr   z, noDown
        inc  [hl]
noDown:

        ld   a, [hl]
        cp   $ff
        jr   nz, noWrapUp
        ld   a, $02
noWrapUp:
        cp   $03
        jr   nz, noWrapDown
        xor  a
noWrapDown:
        ld   [hl], a
        jp   $7E02
    """), fill_nop=True)
    rom.patch(0x01, 0x3E02, 0x3E20, ASM("""
        swap a
        add  a, $48
        ld   hl, $C018
        ldi  [hl], a
        ld   a, $24
        ldi  [hl], a
        ld   a, $BE
        ldi  [hl], a
        ld   [hl], $00
        ret
    """), fill_nop=True)

    rom.patch(0x01, 0x00B7, ASM("""
        ld   a, [$C13F]
        cp   $01
        jr   z, $3B
    """), ASM("""
        ld   a, [$C13F]
        jp $7E20
    """), fill_nop=True)

    re = RoomEditor(rom, 0x2a3)
    warp = re.getWarps()[0]

    type = 0x00
    map = 0x00
    room = warp.room
    x = warp.target_x
    y = warp.target_y

    one_way = [
        'd0',
        'd1',
        'd3',
        'd4',
        'd6',
        'd8',
        'animal_cave',
        'right_fairy',
        'rooster_grave',
        'prairie_left_cave2',
        'prairie_left_fairy',
        'armos_fairy',
        'boomerang_cave',
        'madbatter_taltal',
        'forest_madbatter',
    ]

    one_way = {ENTRANCE_INFO[x].room for x in one_way}

    if warp.room in one_way:
        # we're starting at a one way exit room
        # warp indoors to avoid soft locks
        type = 0x01
        map = 0x10
        room = 0xa3
        x = 0x50
        y = 0x7f

    rom.patch(0x01, 0x3E20, 0x3E6B, ASM("""
        ; First, handle save & quit
        cp   $01
        jp   z, $40F9
        and  a
        jp   z, $40BE ; return to normal "return to game" handling

        ld   a, [$C509] ; Check if we have an item in the shop
        and  a
        jp   nz, $40BE ; return to normal "return to game" handling

        ld   a, $0B
        ld   [$DB95], a
        call $0C7D

        ; Replace warp0 tile data, and put link on that tile.
        ld   a, $%02x ; Type
        ld   [$D401], a
        ld   a, $%02x ; Map
        ld   [$D402], a
        ld   a, $%02x ; Room
        ld   [$D403], a
        ld   a, $%02x ; X
        ld   [$D404], a
        ld   a, $%02x ; Y
        ld   [$D405], a

        ldh  a, [$98]
        swap a
        and  $0F
        ld   e, a
        ldh  a, [$99]
        sub  $08
        and  $F0
        or   e
        ld   [$D416], a

        ld   a, $07
        ld   [$DB96], a
        ret
        jp   $40BE  ; return to normal "return to game" handling
    """ % (type, map, room, x, y)), fill_nop=True)

   # Patch the RAM clear not to delete our custom dialog when we screen transition
    rom.patch(0x01, 0x042C, "C629", "6B7E")
    rom.patch(0x01, 0x3E6B, 0x3FFF, ASM("""
        ld bc, $A0
        call $29DC
        ld bc, $1200
        ld hl, $C100
        call $29DF
        ret
    """), fill_nop=True)
    # Patch the S&Q screen to have 3 options.
    be = BackgroundEditor(rom, 0x0D)
    for n in range(2, 18):
        be.tiles[0x99C0 + n] = be.tiles[0x9980 + n]
        be.tiles[0x99A0 + n] = be.tiles[0x9960 + n]
        be.tiles[0x9980 + n] = be.tiles[0x9940 + n]
        be.tiles[0x9960 + n] = be.tiles[0x98e0 + n]
    be.tiles[0x9960 + 10] = 0xCE
    be.tiles[0x9960 + 11] = 0xCF
    be.tiles[0x9960 + 12] = 0xC4
    be.tiles[0x9960 + 13] = 0x7F
    be.tiles[0x9960 + 14] = 0x7F
    be.store(rom)

    sprite_data = [
        0b00000000,
        0b01000100,
        0b01000101,
        0b01000101,
        0b01111101,
        0b01000101,
        0b01000101,
        0b01000100,

        0b00000000,
        0b11100100,
        0b00010110,
        0b00010101,
        0b00010100,
        0b00010100,
        0b00010100,
        0b11100100,
    ]
    for n in range(32):
        rom.banks[0x0F][0x08E0 + n] = sprite_data[n // 2]


def addFrameCounter(rom, check_count):
    # Patch marin giving the start the game to jump to a custom handler
    rom.patch(0x05, 0x1299, ASM("ld a, $01\ncall $2385"), ASM("push hl\nld a, $0D\nrst 8\npop hl"), fill_nop=True)

    # Add code that needs to be called every frame to tick our ingame time counter.
    rom.patch(0x00, 0x0091, "00" * (0x100 - 0x91), ASM("""
        ld   a, [$DB95] ;Get the gameplay type
        dec  a          ; and if it was 1
        ret  z          ; we are at the credits and the counter should stop.

        ; Check if the timer expired
        ld   hl, $FF0F
        bit  2, [hl]
        ret  z
        res  2, [hl]

        ; Increase the "subsecond" counter, and continue if it "overflows"
        call $27D0 ; Enable SRAM
        ld   hl, $B000
        ld   a, [hl]
        inc  a
        cp   $20
        ld   [hl], a
        ret  nz
        xor  a
        ldi  [hl], a

        ; Increase the seconds counter/minutes/hours counter
increaseSecMinHours:
        ld   a, [hl]
        inc  a
        daa
        ld   [hl], a
        cp   $60
        ret  nz
        xor  a
        ldi  [hl], a
        jr   increaseSecMinHours
    """), fill_nop=True)
    # Replace a cgb check with the call to our counter code.
    rom.patch(0x00, 0x0367, ASM("ld a, $0C\ncall $0B0B"), ASM("call $0091\nld a, $2C"))

    # Do not switch to 8x8 sprite mode
    rom.patch(0x17, 0x2E9E, ASM("res 2, [hl]"), "", fill_nop=True)
    # We need to completely reorder link sitting on the raft to work with 16x8 sprites.
    sprites = rom.banks[0x38][0x1600:0x1800]
    sprites[0x1F0:0x200] = b'\x00' * 16
    for index, position in enumerate(
            (0, 0x1F,
             1, 0x1F, 2, 0x1F,
             7, 8,
             3, 9, 4, 10, 5, 11, 6, 12,
             3, 13, 4, 14, 5, 15, 6, 16,
             3, 17, 4, 18, 5, 19, 6, 20,
        )):
        rom.banks[0x38][0x1600+index*0x10:0x1610+index*0x10] = sprites[position*0x10:0x10+position*0x10]
    rom.patch(0x27, 0x376E, 0x3776, "00046601", fill_nop=True)
    rom.patch(0x27, 0x384E, ASM("ld c, $08"), ASM("ld c, $04"))
    rom.patch(0x27, 0x3776, 0x3826,
          "FA046002"
          "0208640402006204"
          "0A106E030A086C030A006A030AF86803"

          "FA046002"
          "0208640402006204"
          "0A1076030A0874030A0072030AF87003"

          "FA046002"
          "0208640402006204"
          "0A107E030A087C030A007A030AF87803"
    , fill_nop=True)
    rom.patch(0x27, 0x382E, ASM("ld a, $6C"), ASM("ld a, $80")) # OAM start position
    rom.patch(0x27, 0x384E, ASM("ld c, $08"), ASM("ld c, $04")) # Amount of overlay OAM data
    rom.patch(0x27, 0x3826, 0x382E, ASM("dw $7776, $7792, $77AE, $7792")) # pointers to animation
    rom.patch(0x27, 0x3846, ASM("ld c, $2C"), ASM("ld c, $1C")) # Amount of OAM data

    # TODO: fix flying windfish
    # Upper line of credits roll into "TIME"
    rom.patch(0x17, 0x069D, 0x0713, ASM("""
        ld   hl, OAMData
        ld   de, $C000 ; OAM Buffer
        ld   bc, $0048
        call $2914
        ret
OAMData:
        db  $20, $18, $34, $00 ;T
        db  $20, $20, $20, $00 ;I
        db  $20, $28, $28, $00 ;M
        db  $20, $30, $18, $00 ;E
        
        db  $20, $70, $16, $00 ;D
        db  $20, $78, $18, $00 ;E
        db  $20, $80, $10, $00 ;A
        db  $20, $88, $34, $00 ;T
        db  $20, $90, $1E, $00 ;H

        db  $50, $18, $14, $00 ;C
        db  $50, $20, $1E, $00 ;H
        db  $50, $28, $18, $00 ;E
        db  $50, $30, $14, $00 ;C
        db  $50, $38, $24, $00 ;K
        db  $50, $40, $32, $00 ;S

        db  $68, $38, $%02x, $00 ;0
        db  $68, $40, $%02x, $00 ;0
        db  $68, $48, $%02x, $00 ;0
        
    """ % ((((check_count // 100) % 10) * 2) | 0x40, (((check_count // 10) % 10) * 2) | 0x40, ((check_count % 10) * 2) | 0x40), 0x469D), fill_nop=True)
    # Lower line of credits roll into XX XX XX
    rom.patch(0x17, 0x0784, 0x082D, ASM("""
        ld   hl, OAMData
        ld   de, $C048 ; OAM Buffer
        ld   bc, $0038
        call $2914

        call $27D0 ; Enable SRAM
        ld   hl, $C04A
        ld   a, [$B003] ; hours
        call updateOAM
        ld   a, [$B002] ; minutes
        call updateOAM
        ld   a, [$B001] ; seconds
        call updateOAM
        
        ld   a, [$DB58] ; death count high
        call updateOAM
        ld   a, [$DB57] ; death count low
        call updateOAM

        ld   a, [$B011] ; check count high
        call updateOAM
        ld   a, [$B010] ; check count low
        call updateOAM
        ret

updateOAM:
        ld   de, $0004
        ld   b, a
        swap a
        and  $0F
        add  a, a
        or   $40
        ld   [hl], a
        add  hl, de

        ld   a, b
        and  $0F
        add  a, a
        or   $40
        ld   [hl], a
        add  hl, de
        ret
OAMData:
        db  $38, $18, $40, $00 ;0 (10 hours)
        db  $38, $20, $40, $00 ;0 (1 hours)
        db  $38, $30, $40, $00 ;0 (10 minutes)
        db  $38, $38, $40, $00 ;0 (1 minutes)
        db  $38, $48, $40, $00 ;0 (10 seconds)
        db  $38, $50, $40, $00 ;0 (1 seconds)

        db  $00, $00, $40, $00 ;0 (1000 death)
        db  $38, $80, $40, $00 ;0 (100 death)

        db  $38, $88, $40, $00 ;0 (10 death)
        db  $38, $90, $40, $00 ;0 (1 death)

        ; checks
        db  $00, $00, $40, $00 ;0
        db  $68, $18, $40, $00 ;0
        db  $68, $20, $40, $00 ;0
        db  $68, $28, $40, $00 ;0
        
    """, 0x4784), fill_nop=True)

    # Grab the "mostly" complete A-Z font
    sprites = rom.banks[0x38][0x1100:0x1400]
    for index, position in enumerate((
            0x10, 0x20,  # A
            0x11, 0x21,  # B
            0x12, 0x12 | 0x100,  # C
            0x13, 0x23,  # D
            0x14, 0x24,  # E
            0x14, 0x25,  # F
            0x12, 0x22,  # G
            0x20 | 0x100, 0x26,  # H
            0x17, 0x17 | 0x100,  # I
            0x28, 0x28,  # J
            0x19, 0x29,  # K
            0x06, 0x07,  # L
            0x1A, 0x2A,  # M
            0x1B, 0x2B,  # N
            0x00, 0x00,  # O?
            0x00, 0x00,  # P?
            #0x00, 0x00,  # Q?
            0x11, 0x18,  # R
            0x1C, 0x2C,  # S
            0x1D, 0x2D,  # T
            0x26, 0x10,  # U
            0x00, 0x00,  # V?
            0x1E, 0x2E,  # W
            #0x00, 0x00,  # X?
            #0x00, 0x00,  # Y?
            0x27, 0x27,  # Z
    )):
        sprite = sprites[(position&0xFF)*0x10:0x10+(position&0xFF)*0x10]
        if position & 0x100:
            for n in range(4):
                sprite[n * 2], sprite[14 - n * 2] = sprite[14 - n * 2], sprite[n * 2]
                sprite[n * 2 + 1], sprite[15 - n * 2] = sprite[15 - n * 2], sprite[n * 2 + 1]
        rom.banks[0x38][0x1100+index*0x10:0x1110+index*0x10] = sprite


    # Number graphics change for the end
    tile_graphics = """
........ ........ ........ ........ ........ ........ ........ ........ ........ ........
.111111. ..1111.. .111111. .111111. ..11111. 11111111 .111111. 11111111 .111111. .111111.
11333311 .11331.. 11333311 11333311 .113331. 13333331 11333311 13333331 11333311 11333311
13311331 113331.. 13311331 13311331 1133331. 13311111 13311331 11111331 13311331 13311331
13311331 133331.. 13311331 11111331 1331331. 1331.... 13311331 ...11331 13311331 13311331
13311331 133331.. 11111331 ....1331 1331331. 1331.... 13311111 ...13311 13311331 13311331
13311331 111331.. ...13311 .1111331 1331331. 1331111. 1331.... ..11331. 13311331 13311331
13311331 ..1331.. ..11331. .1333331 13313311 13333311 1331111. ..13311. 11333311 11333331
13311331 ..1331.. ..13311. .1111331 13333331 13311331 13333311 .11331.. 13311331 .1111331
13311331 ..1331.. .11331.. ....1331 11113311 11111331 13311331 .13311.. 13311331 ....1331
13311331 ..1331.. .13311.. ....1331 ...1331. ....1331 13311331 11331... 13311331 ....1331
13311331 ..1331.. 11331... 11111331 ...1331. 11111331 13311331 13311... 13311331 11111331
13311331 ..1331.. 13311111 13311331 ...1331. 13311331 13311331 1331.... 13311331 13311331
11333311 ..1331.. 13333331 11333311 ...1331. 11333311 11333311 1331.... 11333311 11333311
.111111. ..1111.. 11111111 .111111. ...1111. .111111. .111111. 1111.... .111111. .111111.
........ ........ ........ ........ ........ ........ ........ ........ ........ ........
""".strip()
    for n in range(10):
        gfx_high = "\n".join([line.split(" ")[n] for line in tile_graphics.split("\n")[:8]])
        gfx_low = "\n".join([line.split(" ")[n] for line in tile_graphics.split("\n")[8:]])
        rom.banks[0x38][0x1400+n*0x20:0x1410+n*0x20] = utils.createTileData(gfx_high)
        rom.banks[0x38][0x1410+n*0x20:0x1420+n*0x20] = utils.createTileData(gfx_low)
