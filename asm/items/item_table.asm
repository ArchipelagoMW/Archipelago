.gba

.autoregion

; 24 available level IDs, not all of which are used.
@levels equ 6 * 4

invalid_item equ 0xFF

; Maps locations to the 8-bit IDs of the items they contain.
; After Archipelago patches the ROM, the "invalid" value should only be in
; locations that don't exist
.align 4
ItemLocationTable:
    Jewel1LocationTable: .fill @levels, invalid_item
    Jewel2LocationTable: .fill @levels, invalid_item
    Jewel3LocationTable: .fill @levels, invalid_item
    Jewel4LocationTable: .fill @levels, invalid_item
    CDLocationTable:     .fill @levels, invalid_item
    HealthLocationTable: .fill @levels, invalid_item

; Maps locations to pointers toward the item's multiworld data.
.align 4
ItemExtDataTable:
    Jewel1ExtDataTable: .fill @levels * 4, 0
    Jewel2ExtDataTable: .fill @levels * 4, 0
    Jewel3ExtDataTable: .fill @levels * 4, 0
    Jewel4ExtDataTable: .fill @levels * 4, 0
    CDExtDataTable:     .fill @levels * 4, 0
    HealthExtDataTable: .fill @levels * 4, 0


.align 2
; Retrieve the item and multiworld pointer at the location specified in r0 in this level.
; Return the encoded ID in r0 and the multiworld pointer in r1
GetItemAtLocation:
    ; r1 = boxtype * 6
    lsl r1, r0, #1
    add r1, r1, r0
    lsl r1, r1, #1
    
    ; r1 = (boxtype * 6 + passageID) * 4
    ldr r0, =PassageID
    ldrb r0, [r0]
    add r1, r1, r0
    lsl r1, r1, #2

    ; r3 = locationID = (boxtype * 6 + passageID) * 4 + levelID
    ldr r0, =InPassageLevelID
    ldrb r0, [r0]
    add r3, r1, r0

    ; r0 = item ID
    ldr r1, =ItemLocationTable
    add r2, r1, r3
    ldrb r0, [r2]

    ; r3 = locationID * 4
    lsl r3, r3, #2

    ; r1 = multiworld pointer
    ldr r1, =ItemExtDataTable
    add r2, r1, r3
    ldr r1, [r2]

    mov pc, lr
.pool

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
    ldrb r2, [r2]
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
