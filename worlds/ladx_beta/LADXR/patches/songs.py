from ..assembler import ASM


def upgradeMarin(rom):
    # Show marin outside, even without a sword.
    rom.patch(0x05, 0x0E78, ASM("ld a, [$DB4E]"), ASM("ld a, $01"), fill_nop=True)
    # Make marin ignore the fact that you did not save the tarin yet, and allowing getting her song
    rom.patch(0x05, 0x0E87, ASM("ld a, [$D808]"), ASM("ld a, $10"), fill_nop=True)
    rom.patch(0x05, 0x0F73, ASM("ld a, [$D808]"), ASM("ld a, $10"), fill_nop=True)
    rom.patch(0x05, 0x0FB0, ASM("ld a, [$DB48]"), ASM("ld a, $01"), fill_nop=True)
    # Show marin in the animal village
    rom.patch(0x03, 0x0A86, ASM("ld a, [$DB74]"), ASM("ld a, $01"), fill_nop=True)
    rom.patch(0x05, 0x3F2E, ASM("ld a, [$DB74]"), ASM("ld a, $01"), fill_nop=True)  # animal d0
    rom.patch(0x15, 0x3F96, ASM("ld a, [$DB74]"), ASM("ld a, $01"), fill_nop=True)  # animal d1
    rom.patch(0x18, 0x11B0, ASM("ld a, [$DB74]"), ASM("ld a, $01"), fill_nop=True)  # animal d2

    # Instead of checking if we have the ballad, check if we have a specific room flag set
    rom.patch(0x05, 0x0F89, ASM("""
        ld   a, [$DB49]
        and  $04
    """), ASM("""
        ld   a, [$D892]
        and  $10
    """), fill_nop=True)
    rom.patch(0x05, 0x0FDF, ASM("""
        ld   a, [$DB49]
        and  $04
    """), ASM("""
        ld   a, [$D892]
        and  $10
    """), fill_nop=True)
    rom.patch(0x05, 0x1042, ASM("""
        ld   a, [$DB49]
        and  $04
    """), ASM("""
        ld   a, [$D892]
        and  $10
    """), fill_nop=True)

    # Patch that we call our specific handler instead of giving the song
    rom.patch(0x05, 0x1170, ASM("""
        ld   hl, $DB49
        set  2, [hl]
        xor  a
        ld   [$DB4A], a
    """), ASM("""
        ; Mark Marin as done.
        ld   a, [$D892]
        or   $10
        ld   [$D892], a
    """), fill_nop=True)


    # Show the right item instead of the ocerina
    rom.patch(0x05, 0x11B3, ASM("""
        ld   de, $515F
        xor  a
        ldh  [$FFF1], a
        jp   $3C77
    """), ASM("""
        ld   a, $0C
        rst  8
        ret
    """), fill_nop=True)

    # Patch the message that tells we got the song, to give the item and show the right message
    rom.patch(0x05, 0x119C, ASM("""
        ld   a, $13
        call $2385
    """), ASM("""
        ld   a, $0E
        rst  8
    """), fill_nop=True)

    # Load marin singing even if you have the marin date
    rom.patch(0x03, 0x0A91, ASM("jp nz, $3F8D"), "", fill_nop=True)
    rom.patch(0x05, 0x0E6E, ASM("jp nz, $7B4B"), "", fill_nop=True)


def upgradeManbo(rom):
    # Instead of checking if we have the song, check if we have a specific room flag set
    rom.patch(0x18, 0x0536, ASM("""
        ld   a, [$DB49]
        and  $02
    """), ASM("""
        ld   a, [$DAFD]
        and  $20
    """), fill_nop=True)

    # Show the right item instead of the ocerina
    rom.patch(0x18, 0x0786, ASM("""
        ld   de, $474D
        xor  a
        ldh  [$FFF1], a
        jp   $3C77
    """), ASM("""
        ld   a, $0C
        rst  8
        ret
    """), fill_nop=True)

    # Patch to replace song giving to give the right item
    rom.patch(0x18, 0x0757, ASM("""
        ld   a, $01
        ld   [$DB4A], a
        ld   hl, $DB49
        set  1, [hl]
    """), ASM("""
        ; Mark Manbo as done.
        ld   hl, $DAFD
        set  5, [hl]
        ; Show item message and give item
        ld   a, $0E
        rst  8
    """), fill_nop=True)
    # Remove the normal "got song message")
    rom.patch(0x18, 0x076F, 0x0774, "", fill_nop=True)

def upgradeMamu(rom):
    # Always allow the sign maze instead of only allowing the sign maze if you do not have song3
    rom.patch(0x00, 0x2057, ASM("ld a, [$DB49]"), ASM("ld a, $00"), fill_nop=True)

    # Patch the condition at which Mamu gives you the option to listen to him
    rom.patch(0x18, 0x0031, ASM("""
        ld   a, [$DB49]
        and  $01
    """), ASM("""
        ld   a, [$DAFB] ; load room flag of the Mamu room
        and  $10
    """), fill_nop=True)

    # Show the right item instead of the ocerina
    rom.patch(0x18, 0x0299, ASM("""
        ld   de, $474D
        xor  a
        ldh  [$FFF1], a
        call $3C77
    """), ASM("""
        ld   a, $0C
        rst  8
    """), fill_nop=True)

    # Patch given an item
    rom.patch(0x18, 0x0270, ASM("""
        ld   a, $02
        ld   [$DB4A], a
        ld   hl, $DB49
        set  0, [hl]
    """), ASM("""
        ; Set the room complete flag.
        ld   hl, $DAFB
        set  4, [hl]
    """), fill_nop=True)

    # Patch to show the right message for the item
    rom.patch(0x18, 0x0282, ASM("""
        ld   a, $DF
        call $4087
    """), ASM("""
        ; Give item and message for room.
        ld   a, $0E
        rst  8
    """), fill_nop=True)
