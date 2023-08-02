.gba

; Functions for applying junk items and traps to Wario's status

.autoregion
.align 2

CollectJunkItems:
        push {lr}

    ; Check full health items
        ldr r3, =QueuedFullHealthItem
        ldrb r2, [r3]
        mov r1, #0
        cmp r2, r1
        beq @@EndCheckFullHealth
        strb r1, [r3]
        mov r0, #8
        bl GiveWarioHearts
    @@EndCheckFullHealth:

    ; Check hearts
    ; Only every 32 frames so as to not spam them too hard
        ldr r3, =GlobalTimer
        ldr r3, [r3]
        get_bits r2, r3, 4, 0
        cmp r2, #0
        bne @@EndCheckHearts

        ldr r3, =QueuedHearts
        ldrb r2, [r3]
        cmp r2, #0
        beq @@EndCheckHearts
        sub r2, r2, #1
        strb r2, [r3]
        mov r0, #1
        bl GiveWarioHearts
    @@EndCheckHearts:

    ; Wario needs to not be invincible to be transformed or damaged
        ldr r3, =Wario_ucMiss
        ldrb r3, [r3]
        cmp r3, #0
        bne @@EndCheckTraps

    ; Wario also needs to be in normal form
        ldr r3, =Wario_ucReact
        ldrb r3, [r3]
        cmp r3, #1
        bgt @@EndCheckTraps

    ; For transformations, he needs to also not be swimming
    ; TODO Maybe also on solid ground for balance reasons
        beq @@EndTransformTraps

        ldr r3, =QueuedFormTraps
        ldrb r2, [r3]
        cmp r2, #0
        beq @@EndTransformTraps
        sub r2, r2, #1
        strb r2, [r3]
        bl GiveTransformTrap
    @@EndTransformTraps:

    ; Check lightning traps
        ldr r3, =QueuedLightningTraps
        ldrb r2, [r3]
        cmp r2, #0
        beq @@EndLightningTraps
        sub r2, r2, #1
        strb r2, [r3]
        bl GiveLightningTrap
    @@EndLightningTraps:

    @@EndCheckTraps:
        pop {pc}
    .pool


; Refil Wario's health, by the amount in r0
GiveWarioHearts:
        push lr
        push r4
        mov r4, r0

        ldr r1, =WarioHeart
        ldrb r0, [r1, #1]
        add r0, r4
        strb r0, [r1, #1]
        ldrb r2, [r1]
        ldrb r0, [r1, #1]
        add r0, r2, r0
        cmp r0, #8
        ble @@FinishFilling
        mov r0, #8
        sub r0, r0, r2
        strb r0, [r1, #1]

    @@FinishFilling:
        ldrb r0, [r1, #1]
        lsl r0, r0, #3
        strb r0, [r1, #2]
        mov r0, #0
        strb r0, [r1, #3]

        ; a1
        ldr r0, =0x140
        cmp r4, #8
        bne @@PlaySound
        add r0, r0, 3

    @@PlaySound:
        call_using r1, m4aSongNumStart

        pop r4
        pop r0
        bx r0
    .pool


; Randomly transform Wario. For compatibility with all levels, only Flaming,
; Fat and Frozen Wario are allowed right now.
GiveTransformTrap:
        push lr

        call_using r2, MiniRandomCreate
        mov r1, #3
        call_using r2, modsi3
        ldr r1, =@@ReactionList
        lsl r0, r0, #2
        add r0, r1, r0
        ldr r0, [r0]

        ldr r1, =@@Return | 1
        mov lr, r1
        mov pc, r0

    @@Return:
        pop pc

    .pool
    @@ReactionList:
        .word ChangeWarioReact_Fire
        .word ChangeWarioReact_Fat
        .word ChangeWarioReact_Frozen


; Summon lightning to damage Wario. Same effect as on The Big Board.
GiveLightningTrap:
        push lr

        ldr r1, =ucFlashLoop
        mov r0, #5
        strb r0, [r1]
        ldr r1, =WarioChng_React
        ldr r0, =Wario_ucReact
        ldrb r0, [r0]
        lsl r0, r0, #2
        add r0, r0, r1
        ldr r1, [r0]  ; a2
        mov r0, #0x13  ; a1

        ldr r2, =@@RemoveCoins | 1
        mov lr, r2
        bx r1

    @@RemoveCoins:
        mov r0, #0x28
        neg r0, r0
        call_using r1, WarioCoinSet

        pop pc
    .pool

.endautoregion