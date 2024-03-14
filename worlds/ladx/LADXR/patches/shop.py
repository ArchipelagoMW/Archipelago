from ..assembler import ASM

# Patches the max rupee count to be 9999
# works, but (1) needs testing at 9999
# (2) needs GUI rendering support code
def patchMaxRupees(rom):
    rom.patch(0x02, 0x6296 - 0x4000, "09", "63")
    
    rom.patch(0x02, 0x6292 - 0x4000, "0A", "64")
    # noop out the cp to 0x10, we want to instead just check the daa overflow
    rom.patch(0x02, 0x625C - 0x4000, "FE1038", "000030")
    rom.patch(0x02, 0x6261 - 0x4000, "09", "99")
        
def fixShop(rom):
    # Move shield visuals to the 2nd slot, and arrow to 3th slot
    rom.patch(0x04, 0x3732 + 22, "986A027FB2B098AC01BAB1", "9867027FB2B098A801BAB1")
    rom.patch(0x04, 0x3732 + 55, "986302B1B07F98A4010A09", "986B02B1B07F98AC010A09")

    # Just use a fixed location in memory to store which inventory we give.
    rom.patch(0x04, 0x37C5, "0708", "0802")

    # Patch the code that decides which shop to show.
    rom.patch(0x04, 0x3839, 0x388E, ASM("""
        push bc
        jr skipSubRoutine

checkInventory:
        ld hl, $DB00 ; inventory
        ld c, INV_SIZE
loop:
        cp [hl]
        ret z
        inc hl
        dec c
        jr nz, loop
        and a
        ret

skipSubRoutine:
        ; Set the shop table to all nothing.
        ld   hl, $C505
        xor  a
        ldi  [hl], a
        ldi  [hl], a
        ldi  [hl], a
        ldi  [hl], a
        ld   de, $C505
        
        ; Check if we want to load a key item into the shop.
        ldh  a, [$F8]
        bit  4, a
        jr   nz, checkForSecondKeyItem
        ld   a, $01
        ld   [de], a
        jr   checkForShield
checkForSecondKeyItem:
        bit  5, a
        jr   nz, checkForShield
        ld   a, $05
        ld   [de], a

checkForShield:
        inc  de
        ; Check if we have the shield or the bow to see if we need to remove certain entries from the shop
        ld   a, [$DB44]
        and  a
        jr   z, hasNoShieldLevel
        ld   a, $03
        ld   [de], a ; Add shield buy option
hasNoShieldLevel:

        inc  de
        ld   a, $05
        call checkInventory
        jr   nz, hasNoBow
        ld   a, $06
        ld   [de], a ; Add arrow buy option
hasNoBow:

        inc  de
        ld   a, $02
        call checkInventory
        jr   nz, hasNoBombs
        ld   a, $04
        ld   [de], a ; Add bomb buy option
hasNoBombs:

        pop  bc
        call $3B12 ; increase entity state
    """, 0x7839), fill_nop=True)

    # We do not have enough room at the shovel/bow buy entry to handle this
    # So jump to a bit where we have some more space to work, as there is some dead code in the shop.
    rom.patch(0x04, 0x3AA9, 0x3AAE, ASM("jp $7AC3"), fill_nop=True)

    # Patch over the "you stole it" dialog
    rom.patch(0x00, 0x1A1C, 0x1A21, ASM("""ld   a, $C9
       call   $2385"""), fill_nop=True)
    rom.patch(0x04, 0x3AC3, 0x3AD8, ASM("""
        ; No room override needed, we're in the proper room
        ; Call our chest item giving code.
        ld   a, $0E
        rst  8
        ; Update the room status to mark first item as bought
        ld   hl, $DAA1
        ld   a, [hl]
        or   $10
        ld   [hl], a
        ret
    """), fill_nop=True)
    rom.patch(0x04, 0x3A73, 0x3A7E, ASM("jp $7A91"), fill_nop=True)
    rom.patch(0x04, 0x3A91, 0x3AA9, ASM("""
        ; Override the room - luckily nothing will go wrong here if we leave it as is
        ld a, $A7
        ldh  [$F6], a
        ; Call our chest item giving code.
        ld   a, $0E
        rst  8
        ; Update the room status to mark second item as bought
        ld   hl, $DAA1
        ld   a, [hl]
        or   $20
        ld   [hl], a
        ret
    """), fill_nop=True)

    # Patch shop item graphics rendering to use some new code at the end of the bank.
    rom.patch(0x04, 0x3B91, 0x3BAC, ASM("""
        call $7FD0
    """), fill_nop=True)
    rom.patch(0x04, 0x3BD3, 0x3BE3, ASM("""
        jp   $7FD0
    """), fill_nop=True)
    rom.patch(0x04, 0x3FD0, "00" * 42, ASM("""
        ; Check if first key item
        and  a
        jr   nz, notShovel
        ld   a, [$77C5]
        ldh  [$F1], a
        ld   a, $01
        rst  8
        ret
notShovel:
        cp   $04
        jr   nz, notBow
        ld   a, [$77C6]
        ldh  [$F1], a
        ld   a, $01
        rst  8
        ret
notBow:
        cp   $05
        jr   nz, notArrows
        ; Load arrow graphics and render then as a dual sprite
        ld   de, $7B58
        call $3BC0
        ret
notArrows:
        ; Load the normal graphics
        ld   de, $7B5A
        jp   $3C77
    """), fill_nop=True)
