.gba

; Implement checking items.


.autoregion

.align 2
; Gives the player the item in r0.
; See Items.py
GiveItem:
    push {r4-r5, lr}

    ; TODO signal something's wrong if it encounters 0xFF
    cmp r0, #0xFF
    beq @@Return

    ; TODO Archipelago items

    lsr r1, r0, #7
    cmp r1, #0
    bne @@JunkItem

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

    ; Check bit 6 to determine CD/Jewel piece
    lsr r3, r0, #6
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
    mov r3, #0x20
    orr r2, r3
    str r2, [r1]

    b @@Return

@@JunkItem:

@@Return:
    pop r4-r5, pc

.pool
.endautoregion


; Give the player their progression items from what they collected in the level.

; Hook into SeisanSave() where the high score is recorded
hook 0x808134C, 0x808135C, CheckLocations

.autoregion
.align 2

; Get the item at level r4's position in LocationTable and give it
.macro check, LocationTable
    ldr r0, =LocationTable
    add r0, r0, r4  ; get entry for this level
    ldrb r0, [r0]  ; a1
    bl GiveItem
.endmacro

CheckLocations:
    push r2, r4, lr

; Calculate level ID as [PassageID] * 4 + [InPassageLevelID] and store in r4
    ldr r0, =PassageID
    ldr r1, =InPassageLevelID
    ldrb r0, [r0]
    ldrb r1, [r1]
    lsl r0, r0, #2
    add r4, r0, r1

; If Wario has the item specified in HasLocation, check level r4's entry in LocationTable
.macro check_has_item, HasLocation, LocationTable
    ldr r0, =HasLocation
    ldrb r0, [r0]
    cmp r0, #0
    beq @@DoesNotHave
    check LocationTable
@@DoesNotHave:
.endmacro

    check_has_item HasJewelPiece1, Jewel1LocationTable
    check_has_item HasJewelPiece2, Jewel2LocationTable
    check_has_item HasJewelPiece3, Jewel3LocationTable
    check_has_item HasJewelPiece4, Jewel4LocationTable
    check_has_item HasCD, CDLocationTable
    check_has_item HasFullHealthItem, HealthLocationTable

; Replaced code
    ldrb r0, [r6]
    lsl r0, r0, #2
    ldrb r1, [r5] 
    lsl r1, r1, #4
    add r0, r0, r1
    add r0, r9
    ldr r0, [r0]
    cmp r0, r2
; Return
    pop r2, r4, pc

.pool
.endautoregion
