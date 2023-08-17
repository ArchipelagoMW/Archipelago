.gba

; Implement checking items.


; Give the player their progression items from what they collected in the level.


; SeisanSave() - High score recorded
hook 0x808134C, 0x808135C, CheckLocations


; TKakeraIconDsp_main()
.org 0x8078E68
.word ReadJewelPieces  ; case 0
.word UpdateJewelIcon  ; case 1
.word UpdateJewelIcon  ; case 2
.word UpdateJewelIcon  ; case 3
.word UpdateJewelIcon  ; case 4


; TCardIconDsp_main()
hook_branch 0x80790B6, 0x80790CC, 0x80790D8, ReadCD


.autoregion


.align 2
; If Wario has the item specified in HasLocation, check level r4's entry in
; LocationTable. If that item is your own junk item, don't do anything because
; you would've gotten it in the level already
.macro check_has_item, HasLocation, LocationTable
        ldr r0, =HasLocation
        ldrb r0, [r0]
        cmp r0, #0
        beq @@DontGive

    ; Get the item and multiworld pointer
        ldr r0, =LocationTable
        add r1, r0, r4  ; get entry for this level
        ldrb r0, [r1]  ; a1
        ldr r1, =ItemExtDataTable + 4 * (LocationTable - ItemLocationTable)
        lsl r2, r4, #2
        add r1, r1, r2
        ldr r1, [r1]  ; a2

    ; Skip your junk items
        cmp r1, #0
        bne @@Give
        lsr r2, r0, #6
        cmp r2, #1
        beq @@DontGive

    @@Give:
        bl GiveItem
    @@DontGive:
.endmacro


CheckLocations:
        push lr
        push r2, r4

    ; Calculate level ID as [PassageID] * 4 + [InPassageLevelID] and store in r4
        ldr r0, =PassageID
        ldr r1, =InPassageLevelID
        ldrb r0, [r0]
        ldrb r1, [r1]
        lsl r0, r0, #2
        add r4, r0, r1

        check_has_item HasJewelPiece1, Jewel1LocationTable
        check_has_item HasJewelPiece2, Jewel2LocationTable
        check_has_item HasJewelPiece3, Jewel3LocationTable
        check_has_item HasJewelPiece4, Jewel4LocationTable
        check_has_item HasCD, CDLocationTable
        check_has_item HasFullHealthItem, HealthLocationTable

    ; Return
        pop r2, r4

    ; Replaced code
        ldrb r0, [r6]
        lsl r0, r0, #2
        ldrb r1, [r5]
        lsl r1, r1, #4
        add r0, r0, r1
        add r0, r9
        ldr r0, [r0]
        cmp r0, r2

        pop pc

    .pool


@room_entity_slot_id equ 0x18

; Spawn the jewel piece or CD icon.
; 0 = jewel pieces
; 1 = CD
SpawnCollectionIndicator:
        push {r4, lr}
        mov r4, r0
        add r4, #0x41

        ldr r3, =CurrentEnemyData
        ldr r1, =EntityLeftOverStateList
        ldr r0, =CurrentRoomId
        ldrb r0, [r0]
        lsl r0, r0, #6
        ldrb r3, [r3, @room_entity_slot_id]
        add r0, r0, r3
        add r0, r0, r1
        mov r1, #0x21
        strb r1, [r0]

        ldr r2, =Wario_ucReact
        ldrh r1, [r2, #14]
        mov r0, #0x20
        and r0, r1
        cmp r0, #0
        beq @@Zero

        ldrh r0, [r2, #20]
        sub r0, #0xA0  ; a1
        ldrh r1, [r2, #18]
        sub r1, #0xC8  ; a2
        b @@Spawn

    @@Zero:
        ldrh r0, [r2, #20]
        sub r0, #0xA0  ; a1
        ldrh r1, [r2, #18]
        sub r1, #0x48  ; a2

    @@Spawn:
        mov r2, r4  ; a3
        call_using r3, TOptObjSet

        ldr r0, =LastCollectedItemID
        ldrb r1, [r0]
        mov r3, 0x80
        orr r1, r3
        strb r1, [r0]

        pop {r4, lr}
    .pool


.macro set_tile, TileId, RomId
        ldr r0, =RomId
        str r0, [r1]
        ldr r0, =TileId
        str r0, [r1, #4]
        ldr r0, =dma_enable | dma_halfwords(0x10)
        str r0, [r1, #8]
        ldr r0, [r1, #8]
.endmacro

ReadJewelPieces:
        push {r7}

    ; Clear indicator status
        ldr r1, =REG_DMA3SAD
        set_tile 0x6011C20, EmptyJewel1Tile
        set_tile 0x6012020, EmptyJewel2Tile
        set_tile 0x6012000, EmptyJewel3Tile
        set_tile 0x6011C00, EmptyJewel4Tile

    ; Load collected jewel piece
        ldr r0, =LastCollectedItemID
        ldrb r7, [r0]
        lsr r3, r7, #7  ; r3 = 1 if collected this frame, 0 otherwise
        get_bits r0, r7, 4, 2  ; r0 = passage ID
        get_bits r7, r7, 1, 0  ; r7 = quadrant

    ; Piece 1
        cmp r3, #0
        beq @@Piece2
        cmp r7, #0
        bne @@Piece2
        mov r0, #0
        mov r1, #1
        strb r1, [r2, #3]
        strb r0, [r2, #4]
        b @@Return

    @@Piece2:
        cmp r3, #0
        beq @@Piece3
        cmp r7, #1
        bne @@Piece3
        mov r1, #0
        mov r0, #2
        b @@StoreStatus

    @@Piece3:
        cmp r3, #0
        beq @@Piece4
        cmp r7, #2
        bne @@Piece4
        mov r1, #0
        mov r0, #3
        b @@StoreStatus

    @@Piece4:
        cmp r3, #0
        beq @@Timeout
        cmp r7, #3
        bne @@Timeout
        mov r1, #0
        mov r0, #4
        b @@StoreStatus

    @@Timeout:
        ldr r0, =ucTimeUp
        ldrb r0, [r0]
        cmp r0, #7
        bhi @@DoneWaiting
        b @@Return

    @@DoneWaiting:
    @@HasPieces:
        mov r1, #0
        mov r0, #6

    @@StoreStatus:
        strb r0, [r2, #3]
        strb r1, [r2, #4]

    @@Return:
        ldr r0, =LastCollectedItemID
        ldrb r3, [r0]
        get_bits r3, r3, 6, 0
        strb r3, [r0]

        pop {r7}
        ldr r0, =0x8079064
        mov pc, r0
    .pool


UpdateJewelIcon:
        push {r4}
        mov r4, r2
        ldrb r0, [r4, #4]
        cmp r0, #0x3B
        bhi @@UpdatePosition
        cmp r0, #0x14
        bne @@DspSub
        call_using r0, TKakeraComp_SE_Set

    ; Change tile
        ldr r3, =JewelGraphicTable
        ldrb r0, [r4, #3]
        sub r0, #1
        lsl r0, #4
        add r3, r3, r0  ; r3 = entry for this jewel piece
        ldr r0, =LastCollectedItemStatus
        ldrb r0, [r0]
        lsl r0, #2
        add r2, r3, r0  ; r2 = selected graphic

        ldr r1, =REG_DMA3SAD
        ldr r0, [r2]  ; Source (selected graphic)
        str r0, [r1]
        ldr r0, [r3, #4]  ; Destination (tilemap position)
        str r0, [r1, #4]
        ldr r0, =dma_enable | dma_halfwords(0x10)
        str r0, [r1, #8]
        ldr r0, [r1, #8]

    @@DspSub:
        call_using r0, TKakeraIconDsp_sub

    @@Return:
        pop {r4}
        ldr r0, =0x8079064
        mov pc, r0

    @@UpdatePosition:
        pop {r4}
        ldr r3, =0x8078F86
        mov pc, r3

    .pool

.align 4
JewelGraphicTable:
    .word EmptyJewel1Tile, 0x6011C20, CarryingJewel1Tile, HasJewel1Tile
    .word EmptyJewel2Tile, 0x6012020, CarryingJewel2Tile, HasJewel2Tile
    .word EmptyJewel3Tile, 0x6012000, CarryingJewel3Tile, HasJewel3Tile
    .word EmptyJewel4Tile, 0x6011C00, CarryingJewel4Tile, HasJewel4Tile


ReadCD:
        push {r7}

    ; clear indicator
        ldr r1, =REG_DMA3SAD
        set_tile 0x60114C0, EmptyCDTile

    ; Load collected CD
        ldr r0, =LastCollectedItemID
        ldrb r7, [r0]
        lsr r3, r7, #7  ; r3 = 1 if collected this frame, 0 otherwise

        cmp r3, #0
        beq @@Timeout
        mov r2, #1
        mov r0, #2
        b @@Return

    @@Timeout:
        mov r2, #2
        ldr r0, =0x80790CC
        mov lr, r0

    @@Return:
        ldr r0, =LastCollectedItemID
        ldrb r3, [r0]
        get_bits r3, r3, 6, 0
        strb r3, [r0]

        ldr r3, =Scbuf_ucStatus
        ldrb r1, [r3]
        pop {r7}
        mov pc, lr

    .pool


.endautoregion
