.gba

; Handle the queued junk items, as well as items received through multiworld.


.autoregion
.align 2


ItemReceivedFeedbackSound:
        push {lr}

        get_bits r0, r4, 6, 5
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


; Get the next incoming item. If nothing was received, return 0xFF.
;
; Returns:
;   r0: Item ID received
ReceiveNextItem:
        ldr r2, =MultiworldState
        ldrb r0, [r2]
        cmp r0, #1
        beq @@GotItem
        mov r0, #0xFF
        b @@Return

    @@GotItem:
    ; Set multiworld state
        mov r1, #0x02
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
        mov pc, lr
    .pool

LoadReceivedText:
        push {lr}

        ldr r0, =StrItemReceived
        ldr r1, =TilesReceived8
        mov r2, #8
        bl LoadSpriteString
        ldr r0, =StrItemFrom
        ldr r1, =TilesFrom4
        mov r2, #4
        bl LoadSpriteString

        ldr r0, =IncomingItemSender
        ldr r1, =TilesSenderA8
        mov r2, #8
        bl LoadSpriteString
        ldr r1, =TilesSenderB8
        mov r2, #8
        bl LoadSpriteString

        pop {pc}
    .pool

.endautoregion
