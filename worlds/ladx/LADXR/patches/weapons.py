from ..assembler import ASM
from ..roomEditor import RoomEditor


def patchSuperWeapons(rom):
    # Feather jump height
    rom.patch(0x00, 0x1508, ASM("ld a, $20"), ASM("ld a, $2C"))
    # Boots charge speed
    rom.patch(0x00, 0x1731, ASM("cp $20"), ASM("cp $01"))
    # Power bracelet pickup speed
    rom.patch(0x00, 0x2121, ASM("ld e, $08"), ASM("ld e, $01"))
    # Throwing speed (of pickups and bombs)
    rom.patch(0x14, 0x1313, "30D0000018E80000", "60A0000040C00000")
    rom.patch(0x14, 0x1323, "0000D0300000E818", "0000A0600000C040")

    # Allow as many bombs to be placed as you want!
    rom.patch(0x00, 0x135F, ASM("ret nc"), "", fill_nop=True)

    # Maximum amount of arrows in the air
    rom.patch(0x00, 0x13C5, ASM("cp $02"), ASM("cp $05"))
    # Delay between arrow shots
    rom.patch(0x00, 0x13C9, ASM("ld a, $10"), ASM("ld a, $01"))

    # Maximum amount of firerod fires
    rom.patch(0x00, 0x12E4, ASM("cp $02"), ASM("cp $05"))

    # Projectile speed (arrows, firerod)
    rom.patch(0x00, 0x13AD,
        "30D0000040C00000" "0000D0300000C040",
        "60A0000060A00000" "0000A0600000A060")

    # Hookshot shoot speed
    rom.patch(0x02, 0x024C,
        "30D00000" "0000D030",
        "60A00000" "0000A060")
    # Hookshot retract speed
    rom.patch(0x18, 0x3C41, ASM("ld a, $30"), ASM("ld a, $60"))
    # Hookshot pull speed
    rom.patch(0x18, 0x3C21, ASM("ld a, $30"), ASM("ld a, $60"))

    # Super shovel, always price!
    rom.patch(0x02, 0x0CC6, ASM("jr nz, $57"), "", fill_nop=True)

    # Unlimited boomerangs!
    rom.patch(0x00, 0x1387, ASM("ret nz"), "", fill_nop=True)

    # Increase shield push power
    rom.patch(0x03, 0x2FC5, ASM("ld a, $08"), ASM("ld a, $10"))
    rom.patch(0x03, 0x2FCA, ASM("ld a, $20"), ASM("ld a, $40"))
    # Decrease link pushback of shield
    rom.patch(0x03, 0x2FB9, ASM("ld a, $12"), ASM("ld a, $04"))
    rom.patch(0x03, 0x2F9A, ASM("ld a, $0C"), ASM("ld a, $03"))

    # Super charge the ocarina
    rom.patch(0x02, 0x0AD8, ASM("cp $38"), ASM("cp $08"))
    rom.patch(0x02, 0x0B05, ASM("cp $14"), ASM("cp $04"))

    re = RoomEditor(rom, 0x23D)
    tiles = re.getTileArray()
    tiles[11] = 0x0D
    tiles[12] = 0xA7
    tiles[22] = 0x98
    re.buildObjectList(tiles)
    re.store(rom)