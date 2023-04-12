.gba


hook 0x8000728, 0x8000738, PreGamePrep
.autoregion
PreGamePrep:
; Copy deathlink option from ROM
    ldr r0, =DeathLinkFlag
    ldrb r0, [r0]
    ldr r4, =DeathlinkEnabled
    strb r0, [r4]

; Reset incoming item sender
    ldr r4, =IncomingItemSender
    mov r0, #0xFF
    strb r0, [r4]

; Replaced code
    ldr r0, =KeyPressContinuous
    strh r7, [r0]
    ldr r0, =KeyPressPrevious
    strh r7, [r0]
    ldr r4, =usTrg_KeyPress1Frame
    strh r7, [r4]
    ldr r0, =sGameSeq
    strh r7, [r0]

    mov pc, lr
.pool
.endautoregion
