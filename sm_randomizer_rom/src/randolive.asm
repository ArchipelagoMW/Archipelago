; Randomizer.live - communication library
; Used here for multiworld messaging

!MESSAGEBASE = $703000
!MESSAGETMP = $c1

!MESSAGES_IN = !MESSAGEBASE
!MESSAGES_OUT = !MESSAGEBASE+$0100
!SNES_WRITEPTR = !MESSAGEBASE+$184
!REMOTE_READPTR = !MESSAGEBASE+$186
!REMOTE_WRITEPTR = !MESSAGEBASE+$180
!SNES_READPTR = !MESSAGEBASE+$182

; Write simple message
; A = message type, X = param 1, Y = param 2 (all 16-bit)
write_message:
    phx : pha
    lda.l !SNES_WRITEPTR
    asl #4
    tax
    pla
    sta.l !MESSAGES_OUT, x
    pla
    sta.l !MESSAGES_OUT+$2, x
    tya
    sta.l !MESSAGES_OUT+$4, x
    lda.l !SNES_WRITEPTR
    inc a
    cmp #$0008
    bne +
    lda #$0000
+   sta.l !SNES_WRITEPTR
    rtl

; Write long mesage
; A = message type, X = length, Y = ptr (loram)
write_long_message:
    pha : phx
    lda.l !SNES_WRITEPTR
    asl #4
    tax
    pla
    sta.l !MESSAGES_OUT, x
    
    ; Write end pointer to tmp
    pla
    asl
    sta !MESSAGETMP
    txa
    clc
    adc !MESSAGETMP
    sta !MESSAGETMP

-   lda $0000, y
    sta.l !MESSAGES_OUT+$2, x
    iny #2
    inx #2
    cpx !MESSAGETMP
    bne -

    lda.l !SNES_WRITEPTR
    inc a
    cmp #$0008
    bne +
    lda #$0000
+   sta.l !SNES_WRITEPTR
    rtl

read_messages:
    pha : phx : phy : php
    rep #$30

-
    lda.l !SNES_READPTR
    cmp.l !REMOTE_WRITEPTR
    beq .end

    asl #4
    tax
    lda.l !MESSAGES_IN, x
    jsr handle_message

    lda.l !SNES_READPTR
    inc a
    cmp #$0010
    bne +
    lda #$0000
+   sta.l !SNES_READPTR
    bra -

.end
    plp : ply : plx : pla
    rtl

; Message type in A, X = pointer to message block
handle_message:
    jmp .unknownMessage

.unknownMessage
    jmp .end        ; Do nothing here for now

.end
    rts


init_randolive:
    pha : phx : phy : php
    %ai16()
    lda #$0000
    ldx #$0000

-    
    sta.l !MESSAGEBASE, x
    inx : inx
    cpx #$0190
    bne -

    plp : ply : plx : pla
    rtl

nmi_read_messages:
    rep #$30
    lda config_multiworld
    beq +
    lda.l !MESSAGEBASE+$18E
    bne +
    jsl read_messages
+
    inc $05b8
    rtl