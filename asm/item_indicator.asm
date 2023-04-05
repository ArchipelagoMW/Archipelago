.gba

@room_entity_slot_id equ 0x18

.autoregion

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
.endautoregion


.definelabel REG_DMA3SAD, 0x40000D4
.definelabel @EmptyJewel1Tile, 0x8401708
.definelabel @EmptyJewel2Tile, 0x8401B08
.definelabel @EmptyJewel3Tile, 0x8401AE8
.definelabel @EmptyJewel4Tile, 0x84016E8
.definelabel @EmptyCDTile, 0x8400FA8

.macro set_tile, TileId, RomId
    ldr r0, =RomId
    str r0, [r1]
    ldr r0, =TileId
    str r0, [r1, #4]
    ldr r0, =0x80000010
    str r0, [r1, #8]
    ldr r0, [r1, #8]
.endmacro

.org 0x8078E68
.word ReadJewelPieces

.autoregion
ReadJewelPieces:
    push {r7}

; Clear indicator status
    ldr r1, =REG_DMA3SAD
    set_tile 0x6011C20, @EmptyJewel1Tile
    set_tile 0x6012020, @EmptyJewel2Tile
    set_tile 0x6012000, @EmptyJewel3Tile
    set_tile 0x6011C00, @EmptyJewel4Tile

; Load collected jewel piece
    ldr r0, =LastCollectedItemID
    ldrb r7, [r0]
    lsr r3, r7, #7  ; r3 = 1 if collected this frame, 0 otherwise
    lsl r0, r7, #31-4
    lsr r0, r0, #31-2  ; r0 = passage ID
    lsl r7, r7, #31-1
    lsr r7, r7, #31-1  ; r7 = quadrant

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
    lsl r3, 31-6
    lsr r3, 31-6
    strb r3, [r0]

    pop {r7}
    ldr r0, =0x8079064
    mov pc, r0
.pool
.endautoregion


hook_branch 0x80790B6, 0x80790CC, 0x80790D8, ReadCD
.autoregion
ReadCD:
    push {r7}

; clear indicator
    ldr r1, =REG_DMA3SAD
    set_tile 0x60114C0, @EmptyCDTile
    
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
    lsl r3, 31-6
    lsr r3, 31-6
    strb r3, [r0]

    ldr r3, =Scbuf_ucStatus
    ldrb r1, [r3]
    pop {r7}
    mov pc, lr

.pool
.endautoregion
