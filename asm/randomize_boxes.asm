.gba

; Change the boxes' opening routine to spawn their randomized item

hook 0x8029578, 0x8029592, SpawnRandomizedItemFromBox  ; Jewel piece 1
hook 0x8029758, 0x8029772, SpawnRandomizedItemFromBox  ; Jewel piece 2
hook 0x8029938, 0x8029952, SpawnRandomizedItemFromBox  ; Jewel piece 3
hook 0x8029B18, 0x8029B32, SpawnRandomizedItemFromBox  ; Jewel piece 4
hook 0x8029D06, 0x8029D24, SpawnRandomizedItemFromBox  ; CD
hook 0x8029F02, 0x8029F2A, SpawnRandomizedItemFromBox  ; Full health item

.autoregion
@oam_animation_pointer equ 0x04
@y_pos equ 0x08
@x_pos equ 0x0A
@global_id equ 0x17
@room_entity_slot_id equ 0x18
@animation_id equ 0x1C
@life equ 0x1D


; Check if this box has been opened before and release the item if it hasn't.
; 
; In the past, this specifically changed the full health box because that one
; releases its item unconditionally in vanilla. While changing all the boxes is
; redundant for now, this opens up the possibility to apply or send native traps
; as soon as the box opens rather than hide behind an item's appearance.
SpawnRandomizedItemFromBox:
    push r4-r6, lr
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
    bl GetItemAtLocation
    lsr r0, r0, #31-6
    cmp r0, #1  ; If it's your own junk item, always release
    beq @@HasNotChecked

    ldrb r1, [r5]
    cmp r1, #0
    beq @@HasNotChecked

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

@@HasNotChecked:
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
    pop r4-r6, pc

.pool
.endautoregion


; Replace the items' graphics with the thing they give when collected

hook_branch 0x8029FA8, 0x8029FB8, 0x802A022, LoadRandomItemAnimation ;  NE jewel
hook_branch 0x802A06C, 0x802A07C, 0x802A0E6, LoadRandomItemAnimation ;  SE jewel
hook_branch 0x802A130, 0x802A140, 0x802A1AA, LoadRandomItemAnimation ;  SW jewel
hook_branch 0x802A1F4, 0x802A204, 0x802A26E, LoadRandomItemAnimation ;  NW jewel
hook_branch 0x802A2B8, 0x802A2C8, 0x802A32E, LoadRandomItemAnimation ;  CD
hook_branch 0x802A378, 0x802A388, 0x802A3E6, LoadRandomItemAnimation ;  Full health

.definelabel @ObjectPalette4, 0x5000280
.macro change_palette_entry, imm
    ldrh r2, [r0, imm * 2]
    strh r2, [r1, imm * 2]
.endmacro

.autoregion
LoadRandomItemAnimation:
    push r4-r6, lr
    ldr r4, =CurrentEnemyData

    ldrb r0, [r4, @global_id]
    sub r0, 0x86
    bl GetItemAtLocation
    mov r6, r0

; AP items
    cmp r6, #0xFE
    beq @@APItem

; Clear bit 7
    lsl r6, r6, #31-6
    lsr r6, r6, #31-6

; Junk items
    lsr r0, r6, #6
    cmp r0, #0
    bne @@JunkItem

; Jewel piece or CD

; Change the palette
; Get passage
    lsl r0, r6, #31-4
    lsr r0, r0, #31-2

; Use CD graphic for AP items until I get a custom sprite made
; This looks super disorganized, but I want to remove this later without leaving
; artifacts like unnecessary jumps or labels
    b @@LoadPalette
@@APItem:
    mov r0, #6
@@LoadPalette:

; Load palette
    ldr r1, =@@JewelPaletteTable
    lsl r2, r0, #2
    add r0, r2, r0
    lsl r0, r0, #1
    add r0, r1, r0

; Change the last five entries in object palette 4
    ldr r1, =@ObjectPalette4 + 0x296 - 0x280
    change_palette_entry #0
    change_palette_entry #1
    change_palette_entry #2
    change_palette_entry #3
    change_palette_entry #4

; Jewel/CD branch
    lsr r1, r6, #6
    cmp r1, #0 
    bne @@CD

; Jewel piece
    lsl r6, r6, #31-1
    lsr r6, r6, #31-1
    b @@SetAnimation

@@CD:
    mov r6, #0x04
    b @@SetAnimation

@@JunkItem:
    cmp r6, #0x40
    beq @@FullHealthItem

@@FullHealthItem:
    mov r6, #0x05

@@SetAnimation:
    ldr r0, =@@ItemAnimationTable
    lsl r1, r6, #2
    add r0, r1, r0
    ldr r0, [r0]
    str r0, [r4, @oam_animation_pointer]
    call_using r0, EntityAI_INITIAL_takara_kakera

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

.align 2
@@JewelPaletteTable:
    .halfword 0x7B3E, 0x723C, 0x6576, 0x58B0, 0x4C07  ; Entry passage
    .halfword 0x5793, 0x578D, 0x4B20, 0x2E40, 0x1160  ; Emerald passage
    .halfword 0x6B5F, 0x529F, 0x253F, 0x14B4, 0x14AE  ; Ruby passage
    .halfword 0x6BDF, 0x23DF, 0x139B, 0x1274, 0x0DAE  ; Topaz passage
    .halfword 0x7F5A, 0x7E94, 0x7D29, 0x50A5, 0x38A5  ; Sapphire passage
    .halfword 0x579F, 0x3B1F, 0x1A7F, 0x05DE, 0x00FB  ; Golden pyramid
    .halfword 0x7FFF, 0x72F5, 0x560E, 0x4169, 0x0000  ; Archipelago item
.endautoregion


; Make the items do what they look like they do
; FIXME If a full health item is in one of the other boxes, the icon for when
; you've collected it doesn't go away until the room is reloaded

hook 0x8029FBA, 0x8029FD6, CollectRandomItem  ; NE jewel
hook 0x802A07E, 0x802A09C, CollectRandomItem  ; SE jewel
hook 0x802A142, 0x802A160, CollectRandomItem  ; SW jewel
hook 0x802A206, 0x802A224, CollectRandomItem  ; NW jewel
hook 0x802A2CA, 0x802A2EA, CollectRandomItem  ; CD
hook 0x802A38A, 0x802A3C4, CollectRandomItem  ; Full health item

.autoregion
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
    mov r0, r5
    bl GetItemAtLocation
    mov r5, r0

; Multiplayer items
    lsr r0, r5, #7
    cmp r0, #0
    bne @@MultiplayerItem

; Junk items
    lsr r0, r5, #6
    cmp r0, #0
    bne @@JunkItem

; Jewel/CD
    lsr r1, r5, #5
    cmp r1, #0
    bne @@CD

; Jewel piece or other world's item
@@MultiplayerItem:
    ldr r0, =0x13B  ; a1
    b @@SetCheckLocation

@@CD:
    ldr r0, =0x13C  ; a1
    b @@SetCheckLocation

@@JunkItem:
    cmp r5, #0x40
    bne @@SetCheckLocation

; Full health item
    mov r0, #8
    bl GiveWarioHearts

@@SetCheckLocation:
    call_using r1, m4aSongNumStart

; Set "has X" variable
    mov r0, #1
    strb r0, [r6]
    b @@Return

@@Return:
    pop r4-r6, lr

.pool

.endautoregion
