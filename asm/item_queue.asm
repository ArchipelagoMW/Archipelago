.gba

; Handle the queued junk items, as well as items received through multiworld.

; Level select: GameSelect case 2
.org 0x80799E0
.word ReceiveItemsInPyramid

; In level: GameMain case 2
.org 0x801B8EC
.word ReceiveItemsInLevel

.autoregion
.align 2


ItemReceivedFeedbackSound:
    push {lr}

    lsl r0, r4, #31-6
    lsr r0, r0, #32-2
    cmp r0, #1
    bgt @@Return
    beq @@CDSound    

@@MultiplayerItem:
    ldr r0, =0x13B  ; a1
    b @@PlaySound

@@CDSound:
    ldr r0, =0x13C  ; a1

@@PlaySound:
    call_using r1, m4aSongNumStart
    mov r0, #1
    call_using r1, WarioVoiceSet

@@Return:
    pop {pc}
.pool


; Get the next incoming item and return it in r0, and return this game's player
; ID in r1.
; If nothing was received, return 0xFF
ReceiveNextItem:
    ldr r2, =IncomingItemSender
    ldrb r0, [r2]
    cmp r0, #0xFF
    beq @@Return

; Reset incoming item sender
    mov r1, #0xFF
    strb r1, [r2]

; Increment received item counter
    ldr r1, =ReceivedItemCount
    ldrh r2, [r1]
    add r2, r2, #1
    strh r2, [r1]

; Set last collected item (if jewel or CD)
    ldr r2, =IncomingItemID
    ldrb r0, [r2]
    lsr r1, r0, #5
    cmp r1, #2
    bge @@Return
    ldr r1, =LastCollectedItemID
    strb r0, [r1]

@@Return:
    ldr r1, =PlayerID
    ldrb r1, [r1]
    mov pc, lr
.pool


; Game mode 1 (pyramid)
ReceiveItemsInPyramid:
    push {r4}
    bl ReceiveNextItem
    mov r4, r0
    bl GiveItem
    mov r0, r4
    bl ItemReceivedFeedbackSound
    pop {r4}
    ldr r0, =0x8079AE0
    mov pc, r0
.pool


; Game mode 2 (level)
ReceiveItemsInLevel:
    push {r4}

; If Wario isn't in a playable state, don't bother yet
    ldr r0, =usWarStopFlg
    ldrh r0, [r0]
    cmp r0, #0
    bne @@Return

    bl ReceiveNextItem
    mov r4, r0
    bl GiveItem
    mov r0, r4
    bl ItemReceivedFeedbackSound

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
    lsl r2, r3, #32-5
    lsr r2, r2, #32-5
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

@@Return:
    pop {r4}
    ldr r0, =0x801B950
    mov pc, r0
.pool

.endautoregion
