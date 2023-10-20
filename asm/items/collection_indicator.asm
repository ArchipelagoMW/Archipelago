.gba


; TKakeraIconDsp_main()
.org 0x8078E68
.word InitializeCollectionIndicator  ; case 0
.word UpdateJewelCollectionIcon  ; case 1
.word UpdateJewelCollectionIcon  ; case 2
.word UpdateJewelCollectionIcon  ; case 3
.word UpdateJewelCollectionIcon  ; case 4


; TCardIconDsp_main()
hook_branch 0x80790B6, 0x80790CC, 0x80790D8, ReadCD
hook 0x8079112, 0x8079126, UpdateCDIcon


.autoregion


; Spawn the jewel piece or CD icon when you've collected one of them.
; Parameters:
;     r0: 0 for jewel pieces, 1 for CD
;     r1: 0 if taken in the level, 1 if given permanently
SpawnCollectionIndicator:
        push {r4-r5, lr}
        mov r4, r0
        add r4, #0x41
        lsl r5, r1, #1

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

        ldr r0, =LastCollectedItemStatus
        add r1, r5, #1
        strb r1, [r0]

        pop {r4-r5, pc}
    .pool


; Replacement for the initialization function of the jewel piece collection
; indicator. This is set up to handle both jewel pieces and the progressive
; abilities.
InitializeCollectionIndicator:
        ldr r0, =LastCollectedItemStatus
        ldrb r3, [r0]
        cmp r3, #0
        bne @@CheckStatus

    ; Wait
        ldr r0, =ucTimeUp
        ldrb r0, [r0]
        cmp r0, #7
        bhi @@DoneWaiting
        b @@Return

    @@DoneWaiting:
        mov r0, #6
        b @@StoreStatus

    @@CheckStatus:
        ldr r0, =LastCollectedItemID
        ldrb r0, [r0]
        get_bit r1, r0, ItemBit_Ability
        cmp r1, #1
        beq @@Ability
        bl ReadJewelPieces
        b @@StoreStatus

    @@Ability:
        bl ReadAbility

    @@StoreStatus:
        ldr r3, =Scbuf_ucStatus
        mov r1, #0
        strb r0, [r3, #3]  ; => Scbuf_ucSeq
        strb r1, [r3, #4]  ; => Scbuf_ucWork0

    @@Return:
        ldr r0, =LastCollectedItemStatus
        ldrb r1, [r0]
        add r1, #1
        strb r1, [r0]

        ldr r0, =0x8079064
        mov pc, r0
    .pool


; Initializes the collection indicator for jewels. Unlike vanilla, this looks at
; what was just grabbed and causes it to display only that. This is done because
; we want it to reflect the item, not the level state. Since jewel pieces are
; progressive in the randomizer, it's meaningless to display anything in the
; other three parts anyway.
;
; Returns:
;     r0: Number (1-4) of the jewel collected
ReadJewelPieces:
    ; Clear indicator status
        ldr r1, =REG_DMA3SAD
        ldr r0, =EmptyJewel4Tile
        str r0, [r1]
        ldr r0, =0x6011C00
        str r0, [r1, #4]
        ldr r0, =dma_enable | dma_halfwords(2 * sizeof_tile / 2)
        str r0, [r1, #8]
        ldr r0, =EmptyJewel3Tile
        str r0, [r1]
        ldr r0, =0x6012000
        str r0, [r1, #4]
        ldr r0, =dma_enable | dma_halfwords(2 * sizeof_tile / 2)
        str r0, [r1, #8]

    ; Load collected jewel piece
        ldr r0, =LastCollectedItemID
        ldrb r3, [r0]
        get_bits r3, r3, 1, 0  ; r3 = quadrant

        add r0, r3, #1
        mov pc, lr

    .pool


ReadAbility:
        push {lr}
        bl MixTemporaryAbilities

        ; Make the top two tiles empty. The use of the empty tile address here is
        ; meaningless; that location is just known to contain the value 0.
        ldr r1, =REG_DMA3SAD
        ldr r2, =EmptyTile
        str r2, [r1]
        ldr r2, =0x6011C00
        str r2, [r1, #4]
        ldr r2, =dma_enable | dma_src_fixed | dma_halfwords(2 * sizeof_tile / 2)
        str r2, [r1, #8]

        ldr r2, =LastCollectedItemID
        ldrb r2, [r2]
        cmp r2, #ItemID_Grab
        beq @@Grab

    ; Ground Pound
        get_bit r2, r0, MoveBit_GroundPoundSuper
        cmp r2, #0
        beq @@NoGroundPound
        ldr r2, =WarioAbilities
        ldrb r2, [r2]
        get_bit r2, r2, MoveBit_GroundPound
        cmp r2, #0
        beq @@GotPoundInLevel

    ; Has ground pound
        mov r0, #2
        ldr r2, =HasGroundPound1Tile
        b @@FinishGroundPound

    @@GotPoundInLevel:
        mov r0, #2
        ldr r2, =CarryingGroundPound1Tile
        b @@FinishGroundPound

    @@NoGroundPound:
        mov r0, #3
        ldr r2, =EmptyGroundPound1Tile

    @@FinishGroundPound:
        str r2, [r1]
        ldr r2, =0x6012000
        str r2, [r1, #4]
        ldr r2, =dma_enable | dma_halfwords(sizeof_tile / 2)
        str r2, [r1, #8]

        ldr r2, =EmptyGroundPound2Tile
        b @@Return

    @@Grab:
        get_bit r2, r0, MoveBit_GrabHeavy
        cmp r2, #0
        beq @@NoGrab
        ldr r2, =WarioAbilities
        ldrb r2, [r2]
        get_bit r2, r2, MoveBit_Grab
        cmp r2, #0
        beq @@GotGrabInLevel

        ; Hack to make the blue W work with the red palette active
        ldr r0, =ObjectPalette4 + 2 * 0xF
        ldr r1, =0x50A5
        strh r1, [r0]

        mov r0, #2
        ldr r2, =HasGrab1Tile
        b @@FinishGrab

    @@GotGrabInLevel:
        mov r0, #2
        ldr r2, =CarryingGrab1Tile
        b @@FinishGrab

    @@NoGrab:
        mov r0, #3
        ldr r2, =EmptyGrab1Tile

    @@FinishGrab:
        str r2, [r1]
        ldr r2, =0x6012000
        str r2, [r1, #4]
        ldr r2, =dma_enable | dma_halfwords(sizeof_tile / 2)
        str r2, [r1, #8]

        ldr r2, =EmptyGrab2Tile

    @@Return:
        str r2, [r1]
        ldr r2, =0x6012020
        str r2, [r1, #4]
        ldr r2, =dma_enable | dma_halfwords(sizeof_tile / 2)
        str r2, [r1, #8]
        pop {pc}

    .pool


; Replacement for the update function of the jewel piece icon. Like
; ReadJewelPieces above, this uses the LastCollectedItemStatus rather than any
; of the level status variables.
UpdateJewelCollectionIcon:
        push {r4}
        mov r4, r2
        ldrb r0, [r4, #4]
        cmp r0, #0x3B
        bhi @@UpdatePosition
        cmp r0, #0x14
        bne @@DspSub
        call_using r0, TKakeraComp_SE_Set

        ldrb r0, [r4, #3]
        ldr r1, =LastCollectedItemID
        ldrb r1, [r1]
        get_bit r1, r1, ItemBit_Ability
        cmp r1, #1
        beq @@Ability
        bl SetCollectedJewelTile
        b @@DspSub

        @@Ability:
        bl SetCollectedAbilityTile

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


; Replace the appropriate tile on the collection indicator with the newly
; collected jewel piece.
; Parameters:
;     r0: Type ID for collected jewel piece
SetCollectedJewelTile:
    ; Change tile
        ldr r3, =JewelGraphicTable
        sub r0, #1
        lsl r0, #4
        add r3, r3, r0  ; r3 = entry for this jewel piece
        ldr r0, =LastCollectedItemStatus
        ldrb r0, [r0]
        cmp r0, #4
        bne @@GetJewel
        sub r0, #1
    @@GetJewel:
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

        mov pc, lr

    .pool

    .align 4
    JewelGraphicTable:
        .word EmptyJewel1Tile, 0x6011C20, CarryingJewel1Tile, HasJewel1Tile
        .word EmptyJewel2Tile, 0x6012020, CarryingJewel2Tile, HasJewel2Tile
        .word EmptyJewel3Tile, 0x6012000, CarryingJewel3Tile, HasJewel3Tile
        .word EmptyJewel4Tile, 0x6011C00, CarryingJewel4Tile, HasJewel4Tile


SetCollectedAbilityTile:
        ldr r1, =LastCollectedItemID
        ldrb r1, [r1]
        cmp r1, #ItemID_Grab
        beq @@Grab

    ; Ground Pound
        ldr r2, =CarryingGroundPound1Tile
        b @@CheckProgression

    @@Grab:
        ; Hack to make the blue W work with the red palette active
        ldr r2, =ObjectPalette4 + 2 * 0xF
        ldr r1, =0x50A5
        strh r1, [r2]
        ldr r2, =CarryingGrab1Tile

    @@CheckProgression:
        ldr r1, =0x6012000
        cmp r0, #2
        bne @@CheckStatus
        add r2, #CarryingGrab2Tile - CarryingGrab1Tile
        add r1, #sizeof_tile

    @@CheckStatus:
        ldr r0, =LastCollectedItemStatus
        ldrb r0, [r0]
        cmp r0, #4
        bne @@SetTile
        add r2, #HasGrab1Tile - CarryingGrab1Tile

    @@SetTile:
        ldr r0, =REG_DMA3SAD
        str r2, [r0]
        str r1, [r0, #4]
        ldr r1, =dma_enable | dma_halfwords(sizeof_tile / 2)
        str r1, [r0, #8]

        mov pc, lr

    .pool


; Replacement for the initialization for the CD collection indicator. The main
; difference from vanilla is that this uses the LastCollectedItemID and
; LastCollectedItemStatus.
ReadCD:
        ldr r0, =LastCollectedItemID
        ldrb r0, [r0]
        get_bit r1, r0, ItemBit_Ability
        cmp r1, #0
        beq @@CD

    ; Get address of ability tile
        get_bits r0, r0, 2, 0
        ldr r1, =NonProgressiveAbilityTileTable
        add r1, r0
        ldrb r0, [r1]
        ldr r1, =EmptySwimTile
        add r0, r1
        b @@SetTile

    @@CD:
        ldr r0, =EmptyCDTile

    @@SetTile:
        ldr r1, =REG_DMA3SAD
        str r0, [r1]
        ldr r0, =0x60114C0
        str r0, [r1, #4]
        ldr r0, =dma_enable | dma_halfwords(sizeof_tile / 2)
        str r0, [r1, #8]

    ; Load collected CD
        ldr r0, =LastCollectedItemID
        ldrb r1, [r0]

        ldr r0, =LastCollectedItemStatus
        ldrb r3, [r0]
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
        ldr r3, =Scbuf_ucStatus
        ldrb r1, [r3]
        mov pc, lr

    .pool


UpdateCDIcon:
        ldr r0, =Scbuf_ucStatus
        ldrb r0, [r0, #4]  ; Scbuf_ucWork0
        cmp r0, #0x14
        bne @@Return

        ldr r0, =LastCollectedItemID
        ldrb r0, [r0]
        get_bit r1, r0, ItemBit_Ability
        cmp r1, #0
        beq @@CD

    ; Get address of ability tile
        get_bits r0, r0, 2, 0
        ldr r1, =NonProgressiveAbilityTileTable
        add r1, r0
        ldrb r0, [r1]
        ldr r1, =HasSwimTile
        add r0, r1
        b @@SetTile

    @@CD:
        ldr r0, =HasCDTile

    @@SetTile:
        ldr r1, =REG_DMA3SAD
        str r0, [r1]
        ldr r0, =0x60114C0
        str r0, [r1, #4]
        ldr r0, =dma_enable | dma_halfwords(sizeof_tile / 2)
        str r0, [r1, #8]

    @@Return:
        mov pc, lr

    .pool


NonProgressiveAbilityTileTable:
    .byte 0  ; Ground Pound (unused)
    .byte 0 * sizeof_tile  ; Swim
    .byte 1 * sizeof_tile  ; Head Smash
    .byte 0  ; Grab (unused)
    .byte 2 * sizeof_tile  ; Dash Attack
    .byte 3 * sizeof_tile  ; Enemy Jump


.endautoregion
