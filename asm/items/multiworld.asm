.gba

; Handle the queued junk items, as well as items received through multiworld.


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
    cmp r0, #0xFE
    beq @@Return

; Reset incoming item sender
    mov r1, #0xFE
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
    ldr r1, =LastCollectedItemStatus
    mov r2, #3
    strb r2, [r1]

@@Return:
    ldr r1, =PlayerID
    ldrb r1, [r1]
    mov pc, lr
.pool


.endautoregion
