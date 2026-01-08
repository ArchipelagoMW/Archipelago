from ..assembler import ASM


def oracleMode(rom):
    # Reduce iframes
    rom.patch(0x03, 0x2DB2, ASM("ld a, $50"), ASM("ld a, $20"))

    # Make bomb explosions damage you.
    rom.patch(0x03, 0x2618, ASM("""
        ld   hl, $C440
        add  hl, bc
        ld   a, [hl]
        and  a
        jr   nz, $05
    """), ASM("""
        call $6625
    """), fill_nop=True)
    # Reduce bomb blast push back on link
    rom.patch(0x03, 0x2643, ASM("sla [hl]"), ASM("sra [hl]"), fill_nop=True)
    rom.patch(0x03, 0x2648, ASM("sla [hl]"), ASM("sra [hl]"), fill_nop=True)

    # Never spawn a piece of power or acorn
    rom.patch(0x03, 0x1608, ASM("jr nz, $05"), ASM("jr $05"))
    rom.patch(0x03, 0x1642, ASM("jr nz, $04"), ASM("jr $04"))

    # Let hearts only recover half a container instead of a full one.
    rom.patch(0x03, 0x24B7, ASM("ld a, $08"), ASM("ld a, $04"))
    # Don't randomly drop fairies from enemies, drop a rupee instead
    rom.patch(0x03, 0x15C7, "2E2D382F2E2D3837", "2E2D382E2E2D3837")

    # Make dropping in water without flippers damage you.
    rom.patch(0x02, 0x3722, ASM("ldh a, [$FFAF]"), ASM("ld a, $06"))


def heroMode(rom):
    # Don't randomly drop fairies and hearts from enemies, drop a rupee instead
    rom.patch(0x03, 0x159D,
                "2E2E2D2D372DFFFF2F37382E2F2F",
                "2E2EFFFF37FFFFFFFF37382EFFFF")
    rom.patch(0x03, 0x15C7,
              "2E2D382F2E2D3837",
              "2E2E382E2E2E3837")
    rom.patch(0x00, 0x168F, ASM("ld a, $2D"), "", fill_nop=True)
    rom.patch(0x02, 0x0CDB, ASM("ld a, $2D"), "", fill_nop=True)
    # Double damage
    rom.patch(0x03, 0x2DAB,
              ASM("ld a, [$DB94]\nadd a, e\nld [$DB94], a"),
              ASM("ld hl, $DB94\nld a, [hl]\nadd a, e\nadd a, e\nld [hl], a"))
    rom.patch(0x02, 0x11B2, ASM("add a, $04"), ASM("add a, $08"))
    rom.patch(0x02, 0x127E, ASM("add a, $04"), ASM("add a, $08"))
    rom.patch(0x02, 0x291C, ASM("add a, $04"), ASM("add a, $08"))
    rom.patch(0x02, 0x362B, ASM("add a, $04"), ASM("add a, $08"))
    rom.patch(0x06, 0x041C, ASM("ld a, $02"), ASM("ld a, $04"))
    rom.patch(0x15, 0x09B8, ASM("add a, $08"), ASM("add a, $10"))
    rom.patch(0x15, 0x32FD, ASM("ld a, $08"), ASM("ld a, $10"))
    rom.patch(0x18, 0x370E, ASM("ld a, $08"), ASM("ld a, $10"))
    rom.patch(0x07, 0x3103, ASM("ld a, $08"), ASM("ld a, $10"))
    rom.patch(0x06, 0x1166, ASM("ld a, $08"), ASM("ld a, $10"))




def oneHitKO(rom):
    rom.patch(0x02, 0x238C, ASM("ld [$DB94], a"), "", fill_nop=True)
