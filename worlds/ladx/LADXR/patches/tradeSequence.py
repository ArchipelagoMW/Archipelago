from ..assembler import ASM


def patchTradeSequence(rom, settings):
    patchTrendy(rom)
    patchPapahlsWife(rom)
    patchYipYip(rom)
    patchBananasSchule(rom)
    patchKiki(rom)
    patchTarin(rom)
    patchBear(rom)
    patchPapahl(rom)
    patchGoatMrWrite(rom)
    patchGrandmaUlrira(rom)
    patchFisherman(rom)
    patchMermaid(rom)
    patchMermaidStatue(rom)
    patchSharedCode(rom)
    patchVarious(rom, settings)
    patchInventoryMenu(rom)


def patchTrendy(rom):
    # Trendy game yoshi
    rom.patch(0x04, 0x3502, 0x350F, ASM("""
        ldh  a, [$F8] ; room status
        and  a, $20
        jp   nz, $6D7A ; clear entity
        ; Render sprite
        ld   a, $0F
        rst  8
        ; Reset the sprite variant, else the code gets confused
        xor  a
        ldh  [$F1], a ; sprite variant
    """), fill_nop=True)
    rom.patch(0x04, 0x2E80, ASM("ldh a, [$F8]"), ASM("ld a, $10"))  # Prevent marin cutscene from triggering, as that locks the game now.
    rom.patch(0x04, 0x3622, 0x3627, "", fill_nop=True)  # Dont set the trade item


def patchPapahlsWife(rom):
    # Rewrite how the first dialog is generated.
    rom.patch(0x18, 0x0E7A, 0x0EA8, ASM("""
        ldh  a, [$F8] ; room status
        and  a, $20
        jr   nz, tradeDone
        
        ld   a, [wTradeSequenceItem]
        and  $01
        jr   nz, requestTrade
        
        ld   a, $2A ; Dialog about wanting a yoshi doll
        jp   $2373  ; OpenDialogInTable1
tradeDone:
        ld   a, $2C ; Dialog about kids, after trade is done
        jp   $2373  ; OpenDialogInTable1
requestTrade:
        ld   a, $2B ; Dialog about kids, after trade is done
        call $3B12; IncrementEntityState 
        jp   $2373  ; OpenDialogInTable1
    """), fill_nop=True)
    rom.patch(0x18, 0x0EB4, 0x0EBD, ASM("ld hl, wTradeSequenceItem\nres 0, [hl]"), fill_nop=True)  # Take the trade item


def patchYipYip(rom):
    # Change how the decision is made to draw yipyip with a ribbon
    rom.patch(0x06, 0x1A2C, 0x1A36, ASM("""
        ldh  a, [$F8] ; room status
        and  $20
        jr   z, tradeNotDone
        ld   de, $59C8 ; yipyip with ribbon
tradeNotDone:
    """), fill_nop=True)
    # Check if we have the ribbon
    rom.patch(0x06, 0x1A7C, 0x1A83, ASM("""
        ld   a, [wTradeSequenceItem]
        and  $02
        jr   z, $07
    """), fill_nop=True)
    rom.patch(0x06, 0x1AAF, 0x1AB8, ASM("ld hl, wTradeSequenceItem\nres 1, [hl]"), fill_nop=True)  # Take the trade item


def patchBananasSchule(rom):
    # Change how to check if we have the right trade item
    rom.patch(0x19, 0x2D54, 0x2D5B, ASM("""
        ld   a, [wTradeSequenceItem]
        and  $04
        jr   z, $08
    """), fill_nop=True)
    rom.patch(0x19, 0x2DF0, 0x2DF9, ASM("ld hl, wTradeSequenceItem\nres 2, [hl]"), fill_nop=True)  # Take the trade item
    # Change how the decision is made to render less bananas
    rom.patch(0x19, 0x2EF1, 0x2EFA, ASM("""
        ldh  a, [$F8]
        and  $20
        jr   z, skip
        dec  c
        dec  c
skip:   """), fill_nop=True)

    # Part of the same entity code, but this is the painter, which changes the dialog depending on mermaid scale or magnifier
    rom.patch(0x19, 0x2F95, 0x2F9C, ASM("""
        ld   a, [wTradeSequenceItem2]
        and  $10 ; Check for mermaid scale
        jr   z, $04
    """))
    rom.patch(0x19, 0x2FA0, 0x2FA4, ASM("""
        and  $20 ; Check for magnifier
        jr   z, $07
    """))
    rom.patch(0x19, 0x2CE3, "9A159C15", "B41DB61D")  # Properly draw the dog food


def patchKiki(rom):
    rom.patch(0x07, 0x18E6, 0x18ED, ASM("""
        ld   a, [wTradeSequenceItem]
        and  $08 ; check for banana
        jr   z, $08
    """))
    rom.patch(0x07, 0x19AF, 0x19B4, "", fill_nop=True)  # Do not change trading item memory
    rom.patch(0x07, 0x19CC, 0x19D5, ASM("ld hl, wTradeSequenceItem\nres 3, [hl]"), fill_nop=True)  # Take the trade item
    rom.patch(0x07, 0x194D, "9A179C17", "B81FBA1F")  # Properly draw the banana above kiki


def patchTarin(rom):
    rom.patch(0x07, 0x0EC5, 0x0ECA, ASM("""
        ld   a, [wTradeSequenceItem]
        and  $10 ; check for stick
    """))
    rom.patch(0x07, 0x0F30, 0x0F33, "", fill_nop=True)  # Take the trade item
    # Honeycomb, change how we detect that it should fall on entering the room
    rom.patch(0x07, 0x0CCC, 0x0CD3, ASM("""
        ld  a, [$D887]
        and $40
        jr  z, $14 
    """))
    # Something about tarin changing messages or not showing up depending on the trade sequence
    rom.patch(0x05, 0x0BFF, 0x0C07, "", fill_nop=True)  # Just ignore the trade sequence
    rom.patch(0x05, 0x0D20, 0x0D27, "", fill_nop=True)  # Just ignore the trade sequence
    rom.patch(0x05, 0x0DAF, 0x0DB8, "", fill_nop=True)  # Tarin giving bananas?

    rom.patch(0x07, 0x0D6D, 0x0D7A, ASM("ld hl, wTradeSequenceItem\nres 4, [hl]"), fill_nop=True)  # Take the trade item


def patchBear(rom):
    # Change the trade item check
    rom.patch(0x07, 0x0BCC, 0x0BD3, ASM("""
        ld   a, [wTradeSequenceItem]
        and  $20 ; check for honeycomb
        jr   z, $0E
    """))
    rom.patch(0x07, 0x0C21, ASM("jr nz, $22"), "", fill_nop=True)
    rom.patch(0x07, 0x0C23, 0x0C2A, ASM("""
        ld   a, [wTradeSequenceItem]
        and  $20 ; check for honeycomb
        jr   z, $08
    """))

    rom.patch(0x07, 0x0C3C, 0x0C43, ASM("""
        nop
        nop
        nop
        nop
        nop
        jr   $02
    """))
    rom.patch(0x07, 0x0C5E, 0x0C67, ASM("ld hl, wTradeSequenceItem\nres 5, [hl]"), fill_nop=True)  # Take the trade item


def patchPapahl(rom):
    rom.patch(0x07, 0x0A21, 0x0A30, ASM("call $7EA4"), fill_nop=True)  # Never show indoor papahl
    # Render the bag condition
    rom.patch(0x07, 0x0A81, 0x0A88, ASM("""
        ldh a, [$F8] ; current room status
        and $20
        nop
        jr  nz, $18
    """))
    # Check for the right item
    rom.patch(0x07, 0x0ACF, 0x0AD4, ASM("""
        ld  a, [wTradeSequenceItem]
        and $40 ; pineapple
    """))
    rom.patch(0x07, 0x0AD6, ASM("jr z, $02"), ASM("jr nz, $02"))

    rom.patch(0x07, 0x0AF9, 0x0B00, ASM("""
        ld  a, [wTradeSequenceItem]
        and $40 ; pineapple
        jr  z, $0E
    """))
    rom.patch(0x07, 0x0B2F, 0x0B38, ASM("ld hl, wTradeSequenceItem\nres 6, [hl]"), fill_nop=True)  # Take the trade item


def patchGoatMrWrite(rom): # The goat and mrwrite are the same entity
    rom.patch(0x18, 0x0BF1, 0x0BF8, ASM("""
        ldh  a, [$F8]
        and  $20
        nop
        jr   nz, $03
    """))  # Check if we made the trade with the goat
    rom.patch(0x18, 0x0C2C, 0x0C33, ASM("""
        ld   a, [wTradeSequenceItem]
        and  $80 ; hibiscus
        jr   z, $08
    """))  # Check if we have the hibiscus
    rom.patch(0x18, 0x0C3D, 0x0C41, "", fill_nop=True)
    rom.patch(0x18, 0x0C6B, 0x0C74, ASM("ld hl, wTradeSequenceItem\nres 7, [hl]"), fill_nop=True)  # Take the trade item for the goat

    rom.patch(0x18, 0x0C8B, 0x0C92, ASM("""
        ld   a, [wTradeSequenceItem2]
        and  $01 ; letter
        jr   z, $08
    """))  # Check if we have the letter
    rom.patch(0x18, 0x0C9C, 0x0CA0, "", fill_nop=True)
    rom.patch(0x18, 0x0CE2, 0x0CEB, ASM("ld hl, wTradeSequenceItem2\nres 0, [hl]"), fill_nop=True)  # Take the trade item for mrwrite


def patchGrandmaUlrira(rom):
    rom.patch(0x18, 0x0D2C, ASM("jr z, $02"), "", fill_nop=True)  # Always show up in animal village
    rom.patch(0x18, 0x0D3C, 0x0D51, ASM("""
        ldh  a, [$F8]
        and  $20
        jp   nz, $4D58
    """), fill_nop=True)
    rom.patch(0x18, 0x0D95, 0x0D9A, "", fill_nop=True)
    rom.patch(0x18, 0x0D9C, 0x0DA0, "", fill_nop=True)
    rom.patch(0x18, 0x0DA3, 0x0DAA, ASM("""
        ld   a, [wTradeSequenceItem2]
        and  $02 ; broom
        jr   z, $0B
    """))
    rom.patch(0x18, 0x0DC4, 0x0DC7, "", fill_nop=True)
    rom.patch(0x18, 0x0DE2, 0x0DEB, ASM("ld hl, wTradeSequenceItem2\nres 1, [hl]"), fill_nop=True)  # Take the trade item
    rom.patch(0x18, 0x0E1D, 0x0E20, "", fill_nop=True)
    rom.patch(0x18, 0x0D13, "9A149C14", "D01CD21C")


def patchFisherman(rom):
    # Not sure what this first check is for
    rom.patch(0x07, 0x02F8, 0x0300, ASM("""
    """), fill_nop=True)
    # Check for the hook
    rom.patch(0x07, 0x04BF, 0x04C6, ASM("""
        ld   a, [wTradeSequenceItem2]
        and  $04 ; hook
        jr   z, $08
    """))
    rom.patch(0x07, 0x04F3, 0x04F6, "", fill_nop=True)
    rom.patch(0x07, 0x057D, 0x0586, ASM("ld hl, wTradeSequenceItem2\nres 2, [hl]"), fill_nop=True)  # Take the trade item
    rom.patch(0x04, 0x1F88, 0x1F8B, "", fill_nop=True)


def patchMermaid(rom):
    # Check for the right trade item
    rom.patch(0x07, 0x0797, 0x079E, ASM("""
        ld   a, [wTradeSequenceItem2]
        and  $08 ; necklace
        jr   z, $0B
    """))
    rom.patch(0x07, 0x0854, 0x085B, ASM("ld hl, wTradeSequenceItem2\nres 3, [hl]"), fill_nop=True)  # Take the trade item


def patchMermaidStatue(rom):
    rom.patch(0x18, 0x095D, 0x0962, "", fill_nop=True)
    rom.patch(0x18, 0x0966, 0x097A, ASM("""
        ld   a, [wTradeSequenceItem2]
        and  $10 ; scale
        ret  z
        ldh  a, [$F8]
        and  $20 ; ROOM_STATUS_EVENT_2
        ret  nz

        ld hl, wTradeSequenceItem2
        res 4, [hl] ; take the trade item
    """), fill_nop=True)


def patchSharedCode(rom):
    # Trade item render code override.
    rom.patch(0x07, 0x1535, 0x1575, ASM("""
        ldh  a, [$F9] 
        and  a
        jr   z, notSideScroll
        
        ldh  a, [$EC]; hActiveEntityVisualPosY
        add  a, $02
        ldh  [$EC], a 
notSideScroll:
        ; Render sprite
        ld   a, $0F
        rst  8
    """), fill_nop=True)
    # Trade item message code
    # rom.patch(0x07, 0x159F, 0x15B9, ASM("""
    #     ld   a, $09 ; give message and item (from alt item table)
    #     rst  8
    # """), fill_nop=True)
    rom.patch(0x07, 0x159F, 0x15B9, ASM("""
        ldh  a, [$F6] ; map room
        cp $B2
        jr nz, NotYipYip
        add a, 2 ; Add 2 to room to set room pointer to an empty room for trade items
        ldh [$F6], a
        ld   a, $0e ; giveItemMultiworld
        rst  8
        ldh  a, [$F6] ; map room
        sub a, 2 ; ...and undo it
        ldh [$F6], a
        jr Done
    NotYipYip:
        ld   a, $0e ; giveItemMultiworld
        rst  8
    Done:
    """), fill_nop=True)


    # Prevent changing the 2nd trade item memory
    rom.patch(0x07, 0x15BD, 0x15C1, ASM("""
        call $7F7F
        xor  a ; we need to exit with A=00    
    """), fill_nop=True)
    rom.patch(0x07, 0x3F7F, "00" * 7, ASM("ldh a, [$F8]\nor $20\nldh [$F8], a\nret"))


def patchVarious(rom, settings):
    # Make the zora photo work with the magnifier
    rom.patch(0x18, 0x09F3, 0x0A02, ASM("""
        ld   a, [wTradeSequenceItem2]
        and  $20 ; MAGNIFYING_GLASS
        jp   z, $7F08 ; ClearEntityStatusBank18 
    """), fill_nop=True)
    rom.patch(0x03, 0x0B6D, 0x0B75, ASM("""
        ld   a, [wTradeSequenceItem2]
        and  $20 ; MAGNIFYING_GLASS
        jp   z, $3F8D ; UnloadEntity 
    """), fill_nop=True)
    # Mimic invisibility
    rom.patch(0x19, 0x2AC0, ASM("""
        cp   $97
        jr   z, mermaidStatueCave
        cp   $98
        jr   nz, visible
    mermaidStatueCave:
        ld   a, [$DB7F]
        and  a
        jr   nz, 6
    visible:
    """), ASM("""
        dec  a ; save one byte by only doing one cp
        or   $01
        cp   $97
        jr   nz, visible
    mermaidStatueCave:
        ld   a, [wTradeSequenceItem2]
        and  $20 ; MAGNIFYING_GLASS
        jr   z, 6
    visible:
    """))
    # Zol invisibility
    rom.patch(0x06, 0x3BE9, ASM("""
        cp   $97
        jr   z, mermaidStatueCave
        cp   $98
        ret  nz ; visible
    mermaidStatueCave:
        ld   a, [$DB7F]
        and  a
        ret  z
    """), ASM("""
        dec  a ; save one byte by only doing one cp
        or   $01
        cp   $97
        ret  nz ; visible
    mermaidStatueCave:
        ld   a, [wTradeSequenceItem2]
        and  $20 ; MAGNIFYING_GLASS
        ret  nz
    """))
    # Ignore trade quest state for marin at beach
    rom.patch(0x18, 0x219E, 0x21A6, "", fill_nop=True)
    # Shift the magnifier 8 pixels
    rom.patch(0x03, 0x0F68, 0x0F6F, ASM("""
        ldh a, [$F6] ; map room
        cp  $97 ; check if we are in the magnifier room
        jp  z, $4F83
    """), fill_nop=True)
    # Something with the photographer
    rom.patch(0x36, 0x0948, 0x0950, "", fill_nop=True)

    # Boomerang trade guy
    # if settings.boomerang not in {'trade', 'gift'} or settings.overworld in {'normal', 'nodungeons'}:
    if settings.tradequest:
        # Update magnifier checks
        rom.patch(0x19, 0x05EC, ASM("ld a, [wTradeSequenceItem]\ncp $0E\njp nz, $7E61"), ASM("ld a, [wTradeSequenceItem2]\nand $20\njp z, $7E61"))  # show the guy
        rom.patch(0x00, 0x3199, ASM("ld a, [wTradeSequenceItem]\ncp $0E\njr nz, $06"), ASM("ld a, [wTradeSequenceItem2]\nand $20\njr z, $06"))  # load the proper room layout
    else:
        # Monkey bridge patch, always have the bridge there.
        rom.patch(0x00, 0x333D, ASM("bit 4, e\njr Z, $05"), b"", fill_nop=True)
        # Always have the boomerang trade guy enabled (magnifier not needed)
        rom.patch(0x19, 0x05EC, ASM("ld a, [wTradeSequenceItem]\ncp $0E"), ASM("ld a, $0E\ncp $0E"), fill_nop=True)  # show the guy
        rom.patch(0x00, 0x3199, ASM("ld a, [wTradeSequenceItem]\ncp $0E"), ASM("ld a, $0E\ncp $0E"), fill_nop=True)  # load the proper room layout
    rom.patch(0x19, 0x05F4, ASM("ld a, [wTradeSequenceItem2]\nand a"), ASM("xor a"), fill_nop=True)


def patchInventoryMenu(rom):
    # Never draw the trade item the normal way
    rom.patch(0x20, 0x1A2E, ASM("ld a, [wTradeSequenceItem2]\nand  a\njr nz, $23"), ASM("jp $5A57"), fill_nop=True)

    rom.patch(0x20, 0x1EB5, ASM("ldh a, [$FE]\nand a\njr z, $34"), ASM("ld a, $10\nrst 8"), fill_nop=True)
