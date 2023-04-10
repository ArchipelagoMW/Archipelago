.gba

; Functions for applying junk items and traps to Wario's status

.autoregion

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