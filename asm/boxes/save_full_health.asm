.gba


; ItemGetFlgSet_LoadSavestateInfo2RAM() - Before checking anything else
hook 0x8075F10, 0x8075F20, ItemGetFlags


; SeisanSave() - Just before Keyzer check
hook 0x8081262, 0x8081284, SeisanSaveFullHealthItem


.autoregion
.align 2


; Check the appropriate bit in the level save to determine whether the full
; health item box has been collected already.
ItemGetFlags:
    ; Load level state flags into r1
        add r1, r4, r6
        lsl r1, r1, #3
        add r1, r3, r1
        add r1, r12
        ldrb r1, [r1, #1]  ; chest flags are in [r1+1] so treasures can stay in [r1]

    ; Check full health first so that we can load Keyzer's status to follow the
    ; original branch when this returns.
    ; Some other code gets to one of those branches, which is why we can't replace
    ; it here.
        get_bit r2, r1, 6
        cmp r2, #0
        beq @@NoFullHealth

    ; Already got the full-health check
        ldr r2, =HasFullHealthItem
        mov r1, #2
        strb r1, [r2]
        b @@FullHealth2

    @@NoFullhealth:
        ldr r1, =HasFullHealthItem
        strb r2, [r1]

    @@FullHealth2:
        get_bit r2, r1, 7
        cmp r2, #0
        beq @@NoFullHealth2

        ldr r2, =HasFullHealthItem2
        mov r1, #2
        strb r1, [r2]
        b @@CheckKeyzer

    @@NoFullHealth2:
        ldr r1, =HasFullHealthItem2
        strb r2, [r1]

    ; Reset the abilities that have been marked as found in the level
        ldr r0, =AbilitiesInThisLevel
        mov r1, #0
        strb r1, [r0]

    @@CheckKeyzer:
        add r1, r4, r6
        lsl r1, r1, #3
        add r1, r3, r1
        add r1, r12
        ldrb r1, [r1]
        get_bit r2, r1, 5

    @@Return:
        cmp r2, #0  ; Next instruction is beq
        mov pc, lr

    .pool


; Save the appropriate item data flag for the full health item box.
SeisanSaveFullHealthItem:
        ldr r3, =LevelStatusTable
        ldrb r1, [r6]
        lsl r1, r1, #2
        ldrb r2, [r5]
        lsl r0, r2, #1
        add r0, r0, r2
        lsl r0, r0, #3
        add r1, r1, r0
        add r1, r1, r3

    ; Handle Keyzer
        ldr r0, =HasKeyzer
        ldrb r0, [r0]
        cmp r0, #0
        beq @@FullHealthItem
        ldrb r0, [r1]
        mov r2, #1 << 5
        orr r0, r2
        strb r0, [r1]

    @@FullHealthItem:
        ldr r0, =HasFullHealthItem
        ldrb r0, [r0]
        cmp r0, #0
        beq @@FullHealth2
        ldrb r0, [r1, #1]
        mov r2, #1 << 6
        orr r0, r2
        strb r0, [r1, #1]

    @@FullHealth2:
        ldr r0, =HasFullHealthItem2
        ldrb r0, [r0]
        cmp r0, #0
        beq @@Return
        ldrb r0, [r1, #1]
        mov r2, #1 << 7
        orr r0, r2
        strb r0, [r1, #1]

    @@Return:
        mov pc, lr

    .pool


.endautoregion
