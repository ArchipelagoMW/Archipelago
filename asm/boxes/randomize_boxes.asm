.gba

; Change the boxes' opening routines to spawn their randomized item
hook 0x8029578, 0x8029592, SpawnRandomizedItemFromBox  ; 0x00 NE jewel box
hook 0x8029758, 0x8029772, SpawnRandomizedItemFromBox  ; 0x01 SE jewel box
hook 0x8029938, 0x8029952, SpawnRandomizedItemFromBox  ; 0x02 SW jewel box
hook 0x8029B18, 0x8029B32, SpawnRandomizedItemFromBox  ; 0x03 NW jewel box
hook 0x8029D06, 0x8029D24, SpawnRandomizedItemFromBox  ; 0x04 CD box
hook 0x8029F02, 0x8029F2A, SpawnRandomizedItemFromBox  ; 0x05 Full health item box


; Make the items do what they look like they do
hook 0x8029FBA, 0x802A012, CollectRandomItem  ; 0x86 NE jewel
hook 0x802A07E, 0x802A0D6, CollectRandomItem  ; 0x87 SE jewel
hook 0x802A142, 0x802A19A, CollectRandomItem  ; 0x88 SW jewel
hook 0x802A206, 0x802A25E, CollectRandomItem  ; 0x89 NW jewel
hook 0x802A2CA, 0x802A31E, CollectRandomItem  ; 0x8A CD
hook 0x802A38A, 0x802A3C4, CollectRandomItem  ; 0x8B Full health item


; Replace the items' graphics with the thing they give when collected
hook_branch 0x8029FA8, 0x8029FB8, 0x802A022, LoadRandomItemAnimation  ; 0x86 NE jewel
hook_branch 0x802A06C, 0x802A07C, 0x802A0E6, LoadRandomItemAnimation  ; 0x87 SE jewel
hook_branch 0x802A130, 0x802A140, 0x802A1AA, LoadRandomItemAnimation  ; 0x88 SW jewel
hook_branch 0x802A1F4, 0x802A204, 0x802A26E, LoadRandomItemAnimation  ; 0x89 NW jewel
hook_branch 0x802A2B8, 0x802A2C8, 0x802A32E, LoadRandomItemAnimation  ; 0x8A CD
hook_branch 0x802A378, 0x802A388, 0x802A3E6, LoadRandomItemAnimation  ; 0x8B Full health


@oam_animation_pointer equ 0x04
@y_pos equ 0x08
@x_pos equ 0x0A
@global_id equ 0x17
@room_entity_slot_id equ 0x18
@animation_id equ 0x1C
@life equ 0x1D


.autoregion


.align 2
; Check if this box has been opened before and release the item if it hasn't.
SpawnRandomizedItemFromBox:
        push r4-r7, lr
        sub sp, sp, #4
        ldr r4, =CurrentEnemyData

        ldrb r0, [r4, @global_id]

    ; Get pointer to "has item"
    ; The full health item uses a new variable so it's handled separately
        cmp r0, #0x05
        beq @@FullHealthBox

    ; For jewel pieces/CDs, the relevant locations are adjacent in memory
        ldr r1, =HasJewelPiece1
        add r5, r1, r0

    ; Change opening animation if CD
        cmp r0, #4
        beq @@CDBox

        b @@CheckLocation

    @@FullHealthBox:
        ldr r5, =HasFullHealthItem
        ldr r2, =zako_takara_box_Anm_11
        b @@SetAnimation

    @@CDBox:
        ldr r2, =zako_takara_box_Anm_02
        b @@SetAnimation

    @@SetAnimation:
        str r2, [r4, @oam_animation_pointer]

    @@CheckLocation:
        ldr r6, =Jewel1BoxContents
        ldr r7, =Jewel1BoxExtData
        add r6, r6, r0
        lsl r1, r0, #2
        add r7, r7, r1
        bl GetItemAtLocation
        strb r0, [r6]
        str r1, [r7]

    ; If it's your own junk item, always release it
        cmp r1, #0
        bne @@CheckCollectionStatus
        lsr r0, r0, #ItemBit_Junk
        cmp r0, #1
        beq @@ReleaseItem

    @@CheckCollectionStatus:
        ldrb r1, [r5]
        cmp r1, #0
        beq @@ReleaseItem

    ; Has checked: contains nothing
        ldr r1, =EntityLeftOverStateList
        ldr r0, =CurrentRoomId
        ldrb r0, [r0]
        lsl r0, r0, #6
        ldrb r4, [r4, @room_entity_slot_id]
        add r0, r0, r4
        add r0, r0, r1
        mov r1, #0x21
        strb r1, [r0]
        b @@Return

    @@ReleaseItem:
        ldrb r6, [r4, @global_id]

    ; Spawn item
        ldrb r1, [r4, @room_entity_slot_id]  ; a2
        ldrh r3, [r4, @y_pos]
        sub r3, #0x80  ; a4
        ldrh r0, [r4, @x_pos]
        str r0, [sp]  ; a5
        mov r2, #0x86
        add r0, r6, r2  ; a1, jewel piece 1 ID + box ID
        mov r2, #0  ; a3
        call_using r5, EnemyChildSet

    ; Spawn glow sprite
        ldrb r1, [r4, @room_entity_slot_id]  ; a2
        ldrh r3, [r4, @y_pos]
        sub r3, #0x80  ; a4
        ldrh r0, [r4, @x_pos]
        str r0, [sp]
        mov r2, #0x8C
        add r0, r6, r2  ; a1, jewel piece 1 glow sprite ID + box ID
        mov r2, #0  ; a3
        call_using r5, EnemyChildSet

    @@Return:
        add sp, sp, #4
        pop r4-r7, pc

    .pool


; Load the appropriate animation for a randomized item found in a box. The
; item used and resulting animation chosen is based on the item's entity ID.
LoadRandomItemAnimation:
        push r4-r6, lr
        ldr r4, =CurrentEnemyData
        ldrb r0, [r4, @global_id]
        sub r0, 0x86
        ldr r1, =Jewel1BoxContents
        add r0, r1, r0
        ldrb r0, [r0]
        mov r6, r0
        mov r5, #0

    ; AP items
        cmp r6, #ItemID_Archipelago
        beq @@APItem

    ; Junk items
        lsr r0, r6, #ItemBit_Junk
        cmp r0, #0
        bne @@JunkItem

    ; Jewel piece or CD

    ; Change the palette
        ; Get passage
        get_bits r0, r6, 4, 2
        bl SetTreasurePalette

    ; Jewel/CD branch
        lsr r1, r6, #ItemBit_CD
        cmp r1, #0
        bne @@CD

    ; Jewel piece
        get_bits r6, r6, 1, 0
        b @@SetAnimation

    @@CD:
        mov r6, #0x04
        b @@SetAnimation

    @@JunkItem:
        cmp r6, #ItemID_FullHealthItem
        beq @@FullHealthItem
        cmp r6, #ItemID_Heart
        beq @@Heart
        b @@GiveImmediately  ; ItemID_TransformTrap, ItemID_Lightning

    @@FullHealthItem:
        mov r6, #0x05
        b @@SetAnimation

    @@Heart:
        mov r6, #0x07
        b @@SetAnimation

    @@APItem:
        mov r0, #6
        bl SetTreasurePalette
        mov r6, #0x06
        b @@SetAnimation

    @@GiveImmediately:
        mov r5, #1
        mov r6, #0x08

    @@SetAnimation:
        ldr r0, =@@ItemAnimationTable
        lsl r1, r6, #2
        add r0, r1, r0
        ldr r0, [r0]
        str r0, [r4, @oam_animation_pointer]
        call_using r0, EntityAI_INITIAL_takara_kakera

        cmp r5, #1
        bne @@Return
        bl CollectRandomItem

    @@Return:
        pop r4-r6, pc

    .pool

    .align 4
    @@ItemAnimationTable:
        .word takara_Anm_04  ; NE jewel piece
        .word takara_Anm_05  ; SE jewel piece
        .word takara_Anm_03  ; SW jewel piece
        .word takara_Anm_02  ; NW jewel piece
        .word takara_Anm_00  ; CD
        .word takara_Anm_01  ; Full health item
        .word APLogoAnm      ; Archipelago item
        .word HeartAnm       ; Single heart
        .word EmptyAnm       ; Nothing


; Collect this item. If it's your own junk item, it gets immediately given.
; Otherwise, this marks the item as collected so that it can be properly given
; to you or another player when you escape the level.
CollectRandomItem:
        push r4-r6, lr

        ldr r4, =CurrentEnemyData
        ldrb r5, [r4, @global_id]
        sub r5, 0x86

    ; Get pointer to "has item"
    ; The full health item uses a new variable so it's handled separately
        cmp r5, #0x05
        beq @@FullHealthCheck

    ; For jewel pieces/CDs, the relevant locations are adjacent in memory
        ldr r6, =HasJewelPiece1
        add r6, r6, r5
        b @@GetItem

    @@FullHealthCheck:
        ldr r6, =HasFullHealthItem

    @@GetItem:
    ; Kill the item entity
        ldr r3, =EntityLeftOverStateList
        ldr r0, =CurrentRoomId
        ldrb r0, [r0]
        lsl r0, r0, #6
        ldrb r4, [r4, @room_entity_slot_id]
        add r0, r0, r4
        add r0, r0, r3
        mov r3, 0x21
        strb r3, [r0]

    ; Get and decode
        ldr r1, =Jewel1BoxContents
        ldr r2, =Jewel1BoxExtData
        add r1, r5, r1
        lsl r0, r5, #2
        add r2, r0, r2
        ldrb r5, [r1]
        ldr r1, [r2]

    ; Multiplayer items
        cmp r1, #0
        bne @@MultiplayerItem

    ; Junk items
        lsr r0, r5, #ItemBit_Junk
        cmp r0, #0
        bne @@JunkItem

    ; Jewel/CD
        ldr r0, =LastCollectedItemID
        strb r5, [r0]
        ldr r0, =LastCollectedItemStatus
        mov r1, #2
        strb r1, [r0]

        lsr r1, r5, #ItemBit_CD
        cmp r1, #0
        bne @@CD
        mov r0, #0  ; a1
        bl SpawnCollectionIndicator
        b @@JewelPiece

    @@MultiplayerItem:
        ldr r0, [r1, #4]
        ldr r1, =TilesItemA12
        mov r2, #12
        bl LoadSpriteString
        ldr r1, =TilesItemB8
        mov r2, #8
        bl LoadSpriteString
        ldr r1, =TilesItemC8
        mov r2, #8
        bl LoadSpriteString

        ldr r0, =MultiworldState
        mov r1, #3
        strb r1, [r0]
        ldr r0, =TextTimer
        mov r1, #120
        strb r1, [r0]

    @@JewelPiece:
        ldr r0, =0x13B  ; a1
        b @@PlayCollectionSound

    @@CD:
        mov r0, #1  ; a1
        bl SpawnCollectionIndicator
        ldr r0, =0x13C  ; a1

    @@PlayCollectionSound:
        call_using r1, m4aSongNumStart
        b @@SetCheckLocation

    @@JunkItem:
        cmp r5, #ItemID_FullHealthItem
        beq @@FullHealthItem
        cmp r5, #ItemID_TransformTrap
        beq @@Transform
        cmp r5, #ItemID_Heart
        beq @@Heart
        cmp r5, #ItemID_Lightning
        beq @@Damage

    @@FullHealthItem:
        mov r0, #8
        bl GiveWarioHearts
        b @@SetCheckLocation

    @@Transform:
        bl GiveTransformTrap
        b @@SetCheckLocation

    @@Heart:
        mov r0, #1
        bl GiveWarioHearts
        b @@SetCheckLocation

    @@Damage:
        bl GiveLightningTrap

    @@SetCheckLocation:
        mov r0, #1
        strb r0, [r6]
        b @@Return

    @@Return:
        pop r4-r6, lr

    .pool


; Spawn the jewel piece or CD icon when you've collected one of them.
; Parameters:
;     r0: 0 for jewel pieces, 1 for CD
IndicateCollectedBoxItem:
        push {lr}

        ldr r3, =CurrentEnemyData
        ldr r1, =EntityLeftOverStateList
        ldr r2, =CurrentRoomId
        ldrb r2, [r2]
        lsl r2, r2, #6
        ldrb r3, [r3, @room_entity_slot_id]
        add r2, r2, r3
        add r2, r2, r1
        mov r1, #0x21
        strb r1, [r2]

        ; r0 contains argument passed through
        bl SpawnCollectionIndicator

        pop {pc}
    .pool


.endautoregion
