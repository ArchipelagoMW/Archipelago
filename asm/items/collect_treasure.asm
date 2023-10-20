.gba

; Implement checking items.


; Give the player their progression items from what they collected in the level.


; SeisanSave() - High score recorded
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
        lsr r2, r0, #ItemBit_Junk
        cmp r2, #1
        beq @@DontGive

    @@Give:
        bl GiveItem
    @@DontGive:
.endmacro


; Look at each box variable and give its item if you've collected it. Your junk
; items would've been collected in the level, so those are never given out.
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


; Combine the current and temporary-in-level abilities to get the abilities
; Wario is currently carrying.
; Returns:
;     r0: Abilities Wario will have if and when he escapes this level
MixTemporaryAbilities:
        ldr r0, =AbilitiesInThisLevel
        ldr r1, =WarioAbilities
        ldrb r0, [r0]
        ldrb r1, [r1]
        orr r0, r1

        mov pc, lr

    .pool


.endautoregion
