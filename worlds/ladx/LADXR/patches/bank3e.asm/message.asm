MessageCopyString:
.loop:
    ldi  a, [hl]
    ld   [de], a
    cp   $ff
    ret  z
    inc  de
    jr   .loop

MessageAddSpace:
    ld   a, $20
    ld   [de], a
    inc  de
    ld   a, $ff
    ld   [de], a
    ret
