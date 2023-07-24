.gba

.org 0x8080C5C

; Hook into GameSelectSeisan() case 7
hook 0x8080C5C, 0x8080C6C, ResultsScreenShowItems

; GameSelectSeisan() jump table case 9
.org 0x8080AB0
.word ResultsScreenMessageState

.autoregion
.align 2

ResultsScreenShowItems:
    push {lr}

    ldr r0, =usMojiCount
    ldr r1, =1000  ; Fixed text position (?)
    strh r1, [r0]

    bl ResultsScreenShowNextItem
    cmp r0, #0
    beq @@JumpToFadeOut
    pop {pc}

@@JumpToFadeOut:
    pop {r0}
    ldr r0, =0x8080D03
    mov pc, r0
.pool


ResultsScreenMessageState:
    ldr r0, =usTrg_KeyPress1Frame
    ldrh r1, [r0]
    mov r0, #1
    and r0, r1
    cmp r0, #0
    beq @@DefaultCase
    ldr r0, =0x125
    call_using r1, m4aSongNumStart
    
    bl ResultsScreenShowNextItem
    cmp r0, #0
    beq @@FadeOut
    
    ldr r0, =ucSeldemoSeq
    ldrb r1, [r0]
    sub r1, #1
    strb r1, [r0]
    
@@DefaultCase:
    ldr r0, =0x8080D45
    mov pc, r0

@@FadeOut:
    ldr r0, =0x8080D03
    mov pc, r0
.pool


; Load the text for the next item collection message. If no items are left to
; show, start fading the results screen.
; Returns:
;  a0: 1 if a new message was loaded, 0 if nothing left to display
ResultsScreenShowNextItem:
    push {r4-r6, lr}
    
    ldr r0, =HasJewelPiece1
    mov r2, #3
    ldr r3, =Jewel1BoxExtData

; Jewel 1
    ldrb r1, [r0]
    cmp r1, #1
    bne @@Jewel2
    strb r2, [r0]
    ldr r4, [r3]
    cmp r4, #0
    beq @@Jewel2
    b @@SetText
    
@@Jewel2:
    ldrb r1, [r0, #1]
    cmp r1, #1
    bne @@Jewel3
    strb r2, [r0, #1]
    ldr r4, [r3, #4]
    cmp r4, #0
    beq @@Jewel3
    b @@SetText

@@Jewel3:
    ldrb r1, [r0, #2]
    cmp r1, #1
    bne @@Jewel4
    strb r2, [r0, #2]
    ldr r4, [r3, #8]
    cmp r4, #0
    beq @@Jewel4
    b @@SetText

@@Jewel4:
    ldrb r1, [r0, #3]
    cmp r1, #1
    bne @@CD
    strb r2, [r0, #3]
    ldr r4, [r3, #12]
    cmp r4, #0
    beq @@CD
    b @@SetText

@@CD:
    ldrb r1, [r0, #4]
    cmp r1, #1
    bne @@FullHealth
    strb r2, [r0, #4]
    ldr r4, [r3, #16]
    beq @@FullHealth
    b @@SetText

@@FullHealth:
    ldr r0, =HasFullHealthItem
    ldrb r1, [r0]
    cmp r1, #1
    bne @@NoMore
    strb r2, [r0]
    ldr r4, [r3, #20]
    cmp r4, #0
    beq @@NoMore

@@SetText:
    ldr r5, [r4]  ; Item name
    ldr r4, [r4, #4]  ; Item receiver
    ldr r6, =0x9000  ; Next tile

    ; "Sent "
    mov r2, #5  ; a3 String length
    lsl r3, r2, #6
    mov r1, r6  ; a2
    add r6, r3  ; Set next tile
    ldr r0, =StrItemSent  ; a1
    call_using r3, MojiCreate
    
    ; Item name
    ; Really long item names could lead to the text box being over-filled, but
    ; the background 2 tileset has tons of unused tiles (due in part to vanilla
    ; allocating tiles for both Japanese and English text), so I don't think any
    ; item will have a long enough name to cause any visual glitches in practice.
    mov r0, r4
    bl StrLen
    mov r2, r0  ; a3 String length
    lsl r3, r2, #6
    mov r1, r6  ; a2 Current tile
    add r6, r3  ; Set next tile
    mov r0, r4  ; a1
    call_using r3, MojiCreate
    
    ; " to "
    mov r2, #4  ; a3 String length
    lsl r3, r2, #6
    mov r1, r6  ; a2
    add r6, r3  ; Set next tile
    ldr r0, =StrItemTo  ; a1
    call_using r3, MojiCreate

    ; Receiver name
    mov r0, r5
    bl StrLen
    mov r2, r0  ; a3 String length
    lsl r3, r2, #6
    mov r1, r6  ; a2 Current tile
    add r6, r3  ; Set next tile
    mov r0, r5  ; a1
    call_using r3, MojiCreate
    
    ; Space filler
    ; The above being said, I would rather not tempt fate by filling almost 140
    ; extra tiles for no reason
    ldr r2, =0xA180
    cmp r6, r2
    bge @@Return
    sub r2, r6
    lsr r2, r2, #6  ; a3 String length
    mov r1, r6  ; a2 Current tile
    ldr r0, =StrScreenFiller  ; a1
    call_using r3, MojiCreate

    mov r0, #1
    b @@Return

@@NoMore:
    mov r0, #0

@@Return:
    pop {r4-r6, pc}
.pool

.endautoregion
