.gba

; GameSelectSeisan() case 7 - Show item text box
hook 0x8080C5C, 0x8080C6C, ResultsScreenShowItems

; GameSelectSeisan() case 8 - Let the player flip through items quickly
org 0x8080CD8
    mov r0, #15

; GameSelectSeisan() case 9 - Repeatedly show text box
.org 0x8080AB0
.word ResultsScreenMessageState


.autoregion


.align 2
; Initialize the former save tutorial, or end the level if nothing to show.
ResultsScreenShowItems:
        push {lr}

        ldr r0, =usMojiCount
        ldr r1, =1000  ; Fixed text position (?)
        strh r1, [r0]

        bl ResultsScreenShowNextItem
        cmp r0, #0
        beq @@JumpToFadeOut
        pop {pc}

    @@JumpToFadeOut:
        pop {r0}
        ldr r0, =0x8080D03
        mov pc, r0
    .pool


; Handle the 'sent item' message on the results screen.
ResultsScreenMessageState:
        ldr r0, =usTrg_KeyPress1Frame
        ldrh r1, [r0]
        mov r0, #1
        and r0, r1
        cmp r0, #0
        beq @@DefaultCase
        ldr r0, =0x125
        call_using r1, m4aSongNumStart

        bl ResultsScreenShowNextItem
        cmp r0, #0
        beq @@FadeOut

        ldr r0, =ucSeldemoSeq
        ldrb r1, [r0]
        sub r1, #1
        strb r1, [r0]

    @@DefaultCase:
        ldr r0, =0x8080D45
        mov pc, r0

    @@FadeOut:
        ldr r0, =0x8080D03
        mov pc, r0
    .pool


; Load the text for the next item received message.
PyramidScreenShowReceivedItem:
        push {r6, lr}
        ldr r6, =0x9000  ; Next tile

        ; "Received "
        mov r2, #9  ; a3 String length
        lsl r3, r2, #6
        mov r1, r6  ; a2
        add r6, r3  ; Set next tile
        ldr r0, =StrItemReceived  ; a1
        call_using r3, MojiCreate

        ; "from "
        mov r2, #5  ; a3 String length
        lsl r3, r2, #6
        mov r1, r6  ; a2
        add r6, r3  ; Set next tile
        ldr r0, =StrItemFrom  ; a1
        call_using r3, MojiCreate

        ; Player name
        ldr r0, =IncomingItemSender
        bl StrLen
        mov r2, r0  ; a3 String length
        lsl r3, r2, #6
        mov r1, r6  ; a2 Current tile
        add r6, r3  ; Set next tile
        ldr r0, =IncomingItemSender  ; a1
        call_using r3, MojiCreate

        ; Space filler
        ldr r2, =0xA180
        sub r2, r6
        lsr r2, r2, #6  ; a3 String length
        mov r1, r6  ; a2 Current tile
        ldr r0, =StrScreenFiller  ; a1
        call_using r3, MojiCreate

    ; Sprite

        ; Decode
        ldr r3, =REG_DMA3SAD
        ldr r0, =IncomingItemID
        ldrb r0, [r0]

        get_bit r1, r0, ItemBit_Junk
        cmp r1, #1
        beq @@JunkItem

        get_bit r1, r0, ItemBit_Ability
        cmp r1, #1
        beq @@Ability

        ; Major item
        get_bits r2, r0, 4, 2  ; Passage
        lsl r2, r2, #5  ; r2: Passage * 32
        get_bit r1, r0, ItemBit_CD
        cmp r1, #1
        beq @@CD

    ; Jewel piece

        ; DMA in the palette
        ldr r1, =PortalPaletteDTable  ; Palette set
        add r1, r1, r2  ; Passage palette
        str r1, [r3]
        ldr r1, =ObjectPaletteF
        str r1, [r3, #4]
        ldr r1, =dma_enable | dma_halfwords(16)
        str r1, [r3, #8]
        ldr r1, [r3, #8]

        ; DMA in the tiles
        get_bits r1, r0, 1, 0
        lsl r1, #1  ; Quadrant * 2
        ldr r0, =@@JewelPieceNEOffset  ; Table
        add r0, r0, r1  ; Entry
        ldrh r1, [r0]  ; Tile offset
        ldr r2, =PortalOBJTileset
        add r1, r2, r1  ; Tile address
        str r1, [r3]
        ldr r1, =0x6014000
        str r1, [r3, #4]
        ldr r1, =dma_enable | dma_words(8 * 34)
        str r1, [r3, #8]
        ldr r1, [r3, #8]

        b @@Return

    @@CD:
        ldr r1, =PortalPaletteETable
        sub r1, #0x20  ; Palette set
        add r1, r1, r2  ; Passage palette
        str r1, [r3]
        ldr r1, =ObjectPaletteF
        str r1, [r3, #4]
        ldr r1, =dma_enable | dma_halfwords(16)
        str r1, [r3, #8]
        ldr r1, [r3, #8]

        ldr r1, =PortalOBJTileset + tile_no_4b(0x4A)  ; Tile address
        str r1, [r3]
        ldr r1, =0x6014000
        str r1, [r3, #4]
        ldr r1, =dma_enable | dma_words(8 * 100)
        str r1, [r3, #8]
        ldr r1, [r3, #8]

        b @@Return

    @@Ability:
        cmp r0, #ItemID_GroundPound
        beq @@GroundPound
        cmp r0, #ItemID_Grab
        beq @@Grab
        b @@OtherAbility

    @@GroundPound:
        ldr r1, =WarioAbilities
        ldrb r1, [r1]
        get_bit r1, r1, MoveBit_GroundPoundSuper
        cmp r1, #0
        beq @@OtherAbility
        mov r0, MoveBit_GroundPoundSuper
        b @@OtherAbility

    @@Grab:
        ldr r1, =WarioAbilities
        ldrb r1, [r1]
        get_bit r1, r1, MoveBit_GrabHeavy
        cmp r1, #0
        beq @@OtherAbility
        mov r0, MoveBit_GrabHeavy
        b @@OtherAbility

    @@OtherAbility:
        get_bits r0, r0, 2, 0

        ; Palette
        ldr r1, =@@AbilityPaletteTable
        lsl r2, r0, #2
        add r1, r2
        ldr r1, [r1]
        str r1, [r3]  ; REG_DMA3SAD
        ldr r1, =ObjectPaletteF
        str r1, [r3, #4]  ; REG_DMA3DAD
        ldr r1, =dma_enable | dma_halfwords(16)
        str r1, [r3, #8]  ; REG_DMA3CNT

        ; Graphic
        ldr r1, =AbilityIconTilesTop
        lsl r2, r0, #6
        add r1, r2
        str r1, [r3]  ; REG_DMA3SAD
        ldr r2, =0x6014000
        str r2, [r3, #4]  ; REG_DMA3DAD
        ldr r2, =dma_enable | dma_halfwords(2 * sizeof_tile / 2)
        str r2, [r3, #8]  ; REG_DMA3CNT
        ldr r2, =sizeof_tile * 16
        add r1, r2
        str r1, [r3]  ; REG_DMA3SAD
        ldr r2, =0x6014000 + tile_coord_4b(0, 1)
        str r2, [r3, #4]  ; REG_DMA3DAD
        ldr r2, =dma_enable | dma_halfwords(2 * sizeof_tile / 2)
        str r2, [r3, #8]  ; REG_DMA3CNT

        b @@Return

    @@JunkItem:
        get_bits r1, r0, 3, 0
        lsl r1, #2
        ldr r2, =@@JunkJumpTable
        add r1, r2
        ldr r6, [r1]
        mov pc, r6

    .align 4
    @@JunkJumpTable:
        .word @@FullHealthItem
        .word @@BigBoardTrap  ; Wario transform
        .word @@Heart
        .word @@BigBoardTrap  ; Lightning damage

    @@FullHealthItem:
        ldr r1, =CommonRoomEntityPalettes4 + 0x40  ; 3rd palette (normally OBP6)
        str r1, [r3]
        ldr r1, =ObjectPaletteF
        str r1, [r3, #4]
        ldr r1, =dma_enable | dma_halfwords(16)
        str r1, [r3, #8]
        ldr r1, [r3, #8]

        ; Heart graphic
        ldr r1, =BasicElementTiles + tile_coord_4b(24, 7)
        str r1, [r3]
        ldr r2, =0x6014000
        str r2, [r3, #4]
        ldr r0, =dma_enable | dma_words(8 * 34)
        str r0, [r3, #8]
        ldr r6, [r3, #8]

        ; Crown graphic
        ldr r1, =BasicElementTiles + tile_coord_4b(4, 1)
        str r1, [r3]
        add r2, #0x40
        str r2, [r3, #4]
        ldr r0, =dma_enable | dma_words(8 * 2)
        str r0, [r3, #8]
        ldr r0, [r3, #8]

        b @@Return

    @@Heart:
        ldr r1, =CommonRoomEntityPalettes4 + 0x60  ; 4th palette (normally OBP7)
        str r1, [r3]
        ldr r1, =ObjectPaletteF
        str r1, [r3, #4]
        ldr r1, =dma_enable | dma_halfwords(16)
        str r1, [r3, #8]
        ldr r1, [r3, #8]

        ldr r1, =BasicElementTiles + tile_coord_4b(10, 3)
        str r1, [r3]
        ldr r2, =0x6014000
        str r2, [r3, #4]
        ldr r0, =dma_enable | dma_words(8 * 34)
        str r0, [r3, #8]
        ldr r6, [r3, #8]

        b @@Return

    @@BigBoardTrap:
        ldr r1, =BigBoardEntityPalettes + 0x20  ; Second palette of list
        str r1, [r3]
        ldr r1, =ObjectPaletteF
        str r1, [r3, #4]
        ldr r1, =dma_enable | dma_halfwords(16)
        str r1, [r3, #8]
        ldr r1, [r3, #8]

        ; Get trap types
        ldr r6, =@@WarioFormTrapOffsets
        cmp r0, #ItemID_Lightning
        bne @@Upper3x2
        add r6, #4

    @@Upper3x2:
        ldr r1, =BigBoardEntityTiles
        ldrh r2, [r6]
        add r2, r1
        str r2, [r3]
        ldr r0, =0x6014000
        str r0, [r3, #4]
        ldr r2, =dma_enable | dma_words(8 * 35)
        str r2, [r3, #8]
        ldr r2, [r3, #8]

        ; Lower 4x1
        ldrh r2, [r6, #2]
        add r2, r1
        str r2, [r3]
        add r0, #0x60
        str r0, [r3, #4]
        ldr r2, =dma_enable | dma_words(8 * 4)
        str r2, [r3, #8]
        ldr r2, [r3, #8]

    @@Return:
        pop {r6, lr}
    .pool

    .align 2
    ; Offsets from PortalOBJTileset
    @@JewelPieceNEOffset:   .halfword tile_no_4b(0x31)
    @@JewelPieceSEOffset:   .halfword tile_no_4b(0x35)
    @@JewelPieceSWOffset:   .halfword tile_no_4b(0x39)
    @@JewelPieceNWOffset:   .halfword tile_no_4b(0x3D)
    @@CDOffset:             .halfword tile_no_4b(0x4A)

    .align 4
    @@AbilityPaletteTable:
        .word PassageTreasurePalettes             ; Ground Pound
        .word PassageTreasurePalettes + 4 * 0x20  ; Swim
        .word ExtraAbilityPalettes + 0x20         ; Head Smash
        .word PassageTreasurePalettes + 4 * 0x20  ; Grab
        .word ExtraAbilityPalettes                ; Dash Attack
        .word PassageTreasurePalettes + 0x20      ; Enemy Jump
        .word PassageTreasurePalettes             ; Super Ground Pound
        .word PassageTreasurePalettes + 2 * 0x20  ; Heavy Grab

    ; 3x2 top offset, 4x1 bottom offset
    @@WarioFormTrapOffsets: .halfword tile_coord_4b(22, 4), tile_coord_4b(28, 5)
    @@DamageTrapOffsets:    .halfword tile_coord_4b(12, 4), tile_coord_4b(25, 4)


; Load the text for the next item collection message. If no items are left to
; show, start fading the results screen.
; Returns:
;  a0: 1 if a new message was loaded, 0 if nothing left to display
ResultsScreenShowNextItem:
        push {r4-r6, lr}

        ldr r0, =HasJewelPiece1
        mov r2, #3
        ldr r3, =Jewel1BoxExtData

    ; Jewel 1
        ldrb r1, [r0]
        cmp r1, #1
        bne @@Jewel2
        strb r2, [r0]
        ldr r4, [r3]
        cmp r4, #0
        beq @@Jewel2
        b @@SetText

    @@Jewel2:
        ldrb r1, [r0, #1]
        cmp r1, #1
        bne @@Jewel3
        strb r2, [r0, #1]
        ldr r4, [r3, #4]
        cmp r4, #0
        beq @@Jewel3
        b @@SetText

    @@Jewel3:
        ldrb r1, [r0, #2]
        cmp r1, #1
        bne @@Jewel4
        strb r2, [r0, #2]
        ldr r4, [r3, #8]
        cmp r4, #0
        beq @@Jewel4
        b @@SetText

    @@Jewel4:
        ldrb r1, [r0, #3]
        cmp r1, #1
        bne @@CD
        strb r2, [r0, #3]
        ldr r4, [r3, #12]
        cmp r4, #0
        beq @@CD
        b @@SetText

    @@CD:
        ldrb r1, [r0, #4]
        cmp r1, #1
        bne @@FullHealth
        strb r2, [r0, #4]
        ldr r4, [r3, #16]
        beq @@FullHealth
        b @@SetText

    @@FullHealth:
        ldr r0, =HasFullHealthItem
        ldrb r1, [r0]
        cmp r1, #1
        bne @@NoMore
        strb r2, [r0]
        ldr r4, [r3, #20]
        cmp r4, #0
        beq @@NoMore

    @@SetText:
        ldr r5, [r4]  ; Item name
        ldr r4, [r4, #4]  ; Item receiver
        ldr r6, =0x9000  ; Next tile

        ; "Sent "
        mov r2, #5  ; a3 String length
        lsl r3, r2, #6
        mov r1, r6  ; a2
        add r6, r3  ; Set next tile
        ldr r0, =StrItemSent  ; a1
        call_using r3, MojiCreate

        ; Item name
        ; Really long item names could lead to the text box being over-filled, but
        ; the background 2 tileset has tons of unused tiles (due in part to vanilla
        ; allocating tiles for both Japanese and English text), so I don't think any
        ; item will have a long enough name to cause any visual glitches in practice.
        mov r0, r4
        bl StrLen
        mov r2, r0  ; a3 String length
        lsl r3, r2, #6
        mov r1, r6  ; a2 Current tile
        add r6, r3  ; Set next tile
        mov r0, r4  ; a1
        call_using r3, MojiCreate

        ; " to "
        mov r2, #4  ; a3 String length
        lsl r3, r2, #6
        mov r1, r6  ; a2
        add r6, r3  ; Set next tile
        ldr r0, =StrItemTo  ; a1
        call_using r3, MojiCreate

        ; Receiver name
        mov r0, r5
        bl StrLen
        mov r2, r0  ; a3 String length
        lsl r3, r2, #6
        mov r1, r6  ; a2 Current tile
        add r6, r3  ; Set next tile
        mov r0, r5  ; a1
        call_using r3, MojiCreate

        ; Space filler
        ; The above being said, I would rather not tempt fate by filling almost 140
        ; extra tiles for no reason
        ldr r2, =0xA180
        cmp r6, r2
        bge @@Return
        sub r2, r6
        lsr r2, r2, #6  ; a3 String length
        mov r1, r6  ; a2 Current tile
        ldr r0, =StrScreenFiller  ; a1
        call_using r3, MojiCreate

        mov r0, #1
        b @@Return

    @@NoMore:
        mov r0, #0

    @@Return:
        pop {r4-r6, pc}
    .pool


.endautoregion
