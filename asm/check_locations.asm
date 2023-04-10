.gba

; Implement checking items.


.autoregion

.align 2
; Collect the item in r0. If the item is this player's junk, it will be stored
; and given to Wario later.
;
; See Items.py
GiveItem:
    push {r4-r5, lr}

; 0xFF means no item, so immediately return
    cmp r0, #0xFF
    beq @@Return

; If another world's item, it'll be handled outside the game
    ldr r2, =PlayerID
    ldr r2, [r2]
    cmp r1, r2
    bne @@Return

    lsr r1, r0, #6
    cmp r1, #0
    bne @@Junk

; Progression item
    ldr r4, =LevelStatusTable

    ; Get passage ID * 24 into r1
    lsl r1, r0, #31-4  ; we want the passage ID in bits 4:2
    lsr r1, r1, #31-2  ; r1 = passage ID
    lsl r3, r1, #1  ; passage*2
    add r3, r3, r1  ; passage*3  
    lsl r1, r3, #3  ; passage*24

    ; Get bits 1:0 into r2
    lsl r2, r0, #31-1
    lsr r2, r2, #31-1

    ; Check bit 5 to determine CD/Jewel piece
    lsr r3, r0, #5
    cmp r3, #0
    bne @@CD

; Jewel piece
    add r1, r1, r4
    mov r5, #4

    ; r2 is the piece we have; bit to set in level status is 1 << r2 -> r3
    mov r3, #1
    lsl r3, r2

    ; Loop through level statuses to find the first one with this piece's bit
    ; unset. If all four are set, break out since this one's an extra.
    @@CheckJewel:
        ldr r2, [r1]
        mov r0, r2
        and r2, r3
        cmp r2, #0
        beq @@FoundJewel

    ; Next
        add r1, r1, #4
        add r5, r5, #-1
        cmp r5, #0
        beq @@Return
        b @@CheckJewel

@@FoundJewel:
    orr r0, r3
    str r0, [r1]
    b @@Return

@@CD:
    ; Load and update level's entry in level status table
    lsl r2, r2, #2
    add r1, r1, r2
    add r1, r1, r4
    ldr r2, [r1]
    mov r3, #0x10
    orr r2, r3
    str r2, [r1]

    b @@Return

@@Junk:
; Queue your junk item by incrementing the appropriate variable
    lsl r1, r0, #31-3
    lsr r1, r1, #31-3
    ldr r2, =QueuedJunk
    add r1, r1, r2
    ldrb r2, [r1]
    add r2, r2, #1
    strb r2, [r1]

@@Return:
    pop r4-r5, pc

.pool

.endautoregion


; Give the player their progression items from what they collected in the level.

; Hook into SeisanSave() where the high score is recorded
hook 0x808134C, 0x808135C, CheckLocations

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

; Get the item and player ID
    ldr r0, =LocationTable
    add r1, r0, r4  ; get entry for this level
    ldrb r0, [r1]  ; a1
    ldr r1, =ItemDestinationTable + (LocationTable - ItemLocationTable)
    add r1, r1, r4
    ldrb r1, [r1]  ; a2

; Skip your junk items
    ldr r2, =PlayerID
    ldrb r2, [r2]
    cmp r1, r2
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
.endautoregion
