from ..assembler import ASM
from ..roomEditor import RoomEditor, Object, ObjectVertical, ObjectHorizontal, ObjectWarp
from ..utils import formatText


def setRequiredInstrumentCount(rom, count):
    rom.texts[0x1A3] = formatText("You need %d instruments" % (count))
    if count >= 8:
        return
    if count < 0:
        rom.patch(0x00, 0x31f5, ASM("ld a, [$D806]\nand $10\njr z, $25"), ASM(""), fill_nop=True)
        rom.patch(0x20, 0x2dea, ASM("ld a, [$D806]\nand $10\njr z, $29"), ASM(""), fill_nop=True)
        count = 0

    # TODO: Music bugs out at the end, unless you have all instruments.
    rom.patch(0x19, 0x0B79, None, "0000")  # always spawn all instruments, we need the last one as that handles opening the egg.
    rom.patch(0x19, 0x0BF4, ASM("jp $3BC0"), ASM("jp $7FE0")) # instead of rendering the instrument, jump to the code below.
    rom.patch(0x19, 0x0BFE, ASM("""
        ; Normal check fo all instruments
        ld   e, $08
        ld   hl, $DB65
    loop:
        ldi  a, [hl]
        and  $02
        jr   z, $12
        dec  e
        jr   nz, loop
    """), ASM("""
        jp   $7F2B ; jump to the end of the bank, where there is some space for code.
    """), fill_nop=True)
    # Add some code at the end of the bank, as we do not have enough space to do this "in place"
    rom.patch(0x19, 0x3F2B, "0000000000000000000000000000000000000000000000000000", ASM("""
        ld   d, $00
        ld   e, $08
        ld   hl, $DB65 ; start of has instrument memory
loop:
        ld   a, [hl]
        and  $02
        jr   z, noinc
        inc  d
noinc:
        inc  hl
        dec  e
        jr   nz, loop
        ld   a, d
        cp   $%02x    ; check if we have a minimal of this amount of instruments.
        jp   c, $4C1A ; not enough instruments
        jp   $4C0B    ; enough instruments
    """ % (count)), fill_nop=True)
    rom.patch(0x19, 0x3FE0, "0000000000000000000000000000000000000000000000000000", ASM("""
    ; Entry point of render code
        ld   hl, $DB65  ; table of having instruments
        push bc
        ldh  a, [$FFF1]
        ld   c, a
        add  hl, bc
        pop  bc
        ld   a, [hl]
        and  $02        ; check if we have this instrument
        ret  z
        jp   $3BC0 ; jump to render code
    """), fill_nop=True)


def setSpecificInstruments(rom, instruments):
    rom.texts[0x1A3] = formatText("You need:\n" + "\n".join(["{INSTRUMENT%s}" % (c) for c in instruments]))
    instruments.sort()
    rom.patch(0x19, 0x0BF9, ASM("cp 7"), ASM("cp %d" % (instruments[0] - 1)))
    if len(instruments) > 1:
        code = f"ld hl, $DB65 + {instruments[1] - 1}\nld a, [hl]\n"
        for n in range(2, len(instruments)):
            if instruments[n] == instruments[n-1] + 1:
                code += "inc l\nand[hl]\n"
            else:
                code += f"ld l, $65 + {instruments[n] - 1}\nand [hl]\n"
        code += "and $02\njp z, $4C1A\njp $4C0B"
    else:
        code = "jp $4C0B"
    rom.patch(0x19, 0x3F2B, "00" * 26, ASM(code), fill_nop=True)
    rom.patch(0x19, 0x0BFE, 0x0C0B, ASM("jp $7F2B"), fill_nop=True)


def setSeashellGoal(rom, count):
    rom.texts[0x1A3] = formatText("You need %d {SEASHELL}s" % (count))

    # Remove the seashell mansion handler (as it will take your seashells) but put a heartpiece instead
    re = RoomEditor(rom, 0x2E9)
    re.entities = [(4, 4, 0x35)]
    re.store(rom)

    rom.patch(0x19, 0x0ACB, 0x0C21, ASM("""
        ldh  a, [$FFF8] ; room status
        and  $10
        ret  nz
        ldh  a, [$FFF0] ; active entity state
        rst  0
        dw   state0, state1, state2, state3, state4

state0:
        ld   a, [$C124] ; room transition state
        and  a
        ret  nz
        ldh  a, [$FF99]  ; link position Y
        cp   $70
        ret  nc
        jp   $3B12  ; increase entity state

state1:
        call $0C05 ; get entity transition countdown
        jr   nz, renderShells
        ld   [hl], $10
        call renderShells

        ld   hl, $C2B0 ; private state 1 table
        add  hl, bc
        ld   a, [wSeashellsCount]
        cp   [hl]
        jp   z, $3B12  ; increase entity state
        ld   a, [hl]   ; increase the amount of compared shells
        inc  a
        daa
        ld   [hl], a
        ld   hl, $C2C0 ; private state 2 table
        add  hl, bc
        inc  [hl] ; increase amount of displayed shells
        ld   a, $2B
        ldh  [$FFF4], a ; SFX
        ret

state2:
        ld   a, [wSeashellsCount]
        cp   $%02d
        jr   c, renderShells
        ; got enough shells
        call $3B12 ; increase entity state
        call $0C05 ; get entity transition countdown
        ld   [hl], $40
        jp   renderShells

state3:
        ld   a, $23
        ldh  [$FFF2], a ; SFX: Dungeon opened
        ld   hl, $D806 ; egg room status
        set  4, [hl]
        ld   a, [hl]
        ldh  [$FFF8], a ; current room status
        call $3B12 ; increase entity state

        ld   a, $00
        jp   $4C2E

state4:
        ret

renderShells:
        ld   hl, $C2C0 ; private state 2 table
        add  hl, bc
        ld   a, [hl]
        cp   $14
        jr   c, .noMax
        ld   a, $14
.noMax:
        and  a
        ret  z
        ld   c, a
        ld   hl, spriteRect
        call $3CE6 ; RenderActiveEntitySpritesRect
        ret

spriteRect:
        db $10, $1E, $1E, $0C
        db $10, $2A, $1E, $0C
        db $10, $36, $1E, $0C
        db $10, $42, $1E, $0C
        db $10, $4E, $1E, $0C

        db $10, $5A, $1E, $0C
        db $10, $66, $1E, $0C
        db $10, $72, $1E, $0C
        db $10, $7E, $1E, $0C
        db $10, $8A, $1E, $0C

        db $24, $1E, $1E, $0C
        db $24, $2A, $1E, $0C
        db $24, $36, $1E, $0C
        db $24, $42, $1E, $0C
        db $24, $4E, $1E, $0C

        db $24, $5A, $1E, $0C
        db $24, $66, $1E, $0C
        db $24, $72, $1E, $0C
        db $24, $7E, $1E, $0C
        db $24, $8A, $1E, $0C
    """ % (count), 0x4ACB), fill_nop=True)


def setRaftGoal(rom):
    rom.texts[0x1A3] = formatText("Just sail away.")

    # Remove the egg and egg event handler.
    re = RoomEditor(rom, 0x006)
    for x in range(4, 7):
        for y in range(0, 4):
            re.removeObject(x, y)
    re.objects.append(ObjectHorizontal(4, 1, 0x4d, 3))
    re.objects.append(ObjectHorizontal(4, 2, 0x03, 3))
    re.objects.append(ObjectHorizontal(4, 3, 0x03, 3))
    re.entities = []
    re.updateOverlay()
    re.store(rom)

    re = RoomEditor(rom, 0x08D)
    re.objects[6].count = 4
    re.objects[7].x += 2
    re.objects[7].type_id = 0x2B
    re.objects[8].x += 2
    re.objects[8].count = 2
    re.objects[9].x += 1
    re.objects[11] = ObjectVertical(7, 5, 0x37, 2)
    re.objects[12].x -= 1
    re.objects[13].x -= 1
    re.objects[14].x -= 1
    re.objects[14].type_id = 0x34
    re.objects[17].x += 3
    re.objects[17].count -= 3
    re.updateOverlay()
    re.overlay[7 + 60] = 0x33
    re.store(rom)

    re = RoomEditor(rom, 0x0E9)
    re.objects[30].count = 1
    re.objects[30].x += 2
    re.overlay[7 + 70] = 0x0E
    re.overlay[8 + 70] = 0x0E
    re.store(rom)
    re = RoomEditor(rom, 0x0F9)
    re.objects = [
        ObjectHorizontal(4, 0, 0x0E, 6),
        ObjectVertical(9, 0, 0xCA, 8),
        ObjectVertical(8, 0, 0x0E, 8),

        Object(3, 0, 0x38),
        Object(3, 1, 0x32),
        ObjectHorizontal(4, 1, 0x2C, 3),
        Object(7, 1, 0x2D),
        ObjectVertical(7, 2, 0x38, 5),
        Object(7, 7, 0x34),
        ObjectHorizontal(0, 7, 0x2F, 7),

        ObjectVertical(2, 3, 0xE8, 4),
        ObjectVertical(3, 2, 0xE8, 5),
        ObjectVertical(4, 2, 0xE8, 2),

        ObjectVertical(4, 4, 0x5C, 3),
        ObjectVertical(5, 2, 0x5C, 5),
        ObjectVertical(6, 2, 0x5C, 5),

        Object(6, 4, 0xC6),
        ObjectWarp(1, 0x1F, 0xF6, 136, 112)
    ]
    re.updateOverlay(True)
    re.entities.append((0, 0, 0x41))
    re.store(rom)
    re = RoomEditor(rom, 0x1F6)
    re.objects[-1].target_x -= 16
    re.store(rom)

    # Fix the raft graphics (this overrides some unused graphic tiles)
    rom.banks[0x31][0x21C0:0x2200] = rom.banks[0x2E][0x07C0:0x0800]

    # Patch the owl entity to run our custom end handling.
    rom.patch(0x06, 0x27F5, 0x2A77, ASM("""
        ld  a, [$DB95]
        cp  $0B
        ret nz
        ; If map is not fully loaded, return
        ld  a, [$C124]
        and a
        ret nz
        ; Check if we are moving off the bottom of the map
        ldh a, [$FF99]
        cp  $7D
        ret c
        ; Move link back so it does not move off the map
        ld  a, $7D
        ldh [$FF99], a
        
        xor a
        ld  e, a
        ld  d, a

raftSearchLoop:
        ld  hl, $C280
        add hl, de
        ld  a, [hl]
        and a
        jr  z, .skipEntity
        
        ld  hl, $C3A0
        add hl, de
        ld  a, [hl]
        cp  $6A
        jr  nz, .skipEntity

        ; Raft found, check if near the bottom of the screen.
        ld  hl, $C210
        add hl, de
        ld  a, [hl]
        cp  $70
        jr  nc, raftOffWorld

.skipEntity:
        inc e
        ld  a, e
        cp  $10
        jr  nz, raftSearchLoop
        ret

raftOffWorld:
        ; Switch to the end credits
        ld  a, $01
        ld  [$DB95], a
        ld  a, $00
        ld  [$DB96], a
        ret
    """), fill_nop=True)

    # We need to run quickly trough part of the credits, or else it bugs out
    # Skip the whole windfish part.
    rom.patch(0x17, 0x0D39, None, ASM("ld a, $18\nld [$D00E], a\nret"))
    # And skip the zoomed out laying on the log
    rom.patch(0x17, 0x20ED, None, ASM("ld a, $00"))
    # Finally skip some waking up on the log.
    rom.patch(0x17, 0x23BC, None, ASM("jp $4CD9"))
    rom.patch(0x17, 0x2476, None, ASM("jp $4CD9"))
