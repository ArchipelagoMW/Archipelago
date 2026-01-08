; Handle the serial link cable
#IF HARDWARE_LINK
; FF> = Idle
; D6> = Read:  D0><[L] D1><[H] [HL]>
; D9> = Write: D8><[L] D9><[H] DA><[^DATA] DB><[DATA]
; DD> = OrW:   D8><[L] D9><[H] DA><[^DATA] DB><[DATA] (used to set flags without requiring a slow read,modify,write race condition)

handleSerialLink:
    ; Check if we got a byte from hardware
    ldh  a, [$FF01]

    cp   $D6
    jr   z, serialReadMem
    cp   $D9
    jr   z, serialWriteMem
    cp   $DD
    jr   z, serialOrMem

finishSerialLink:
    ; Do a new idle transfer.
    ld   a, $E4
    ldh  [$FF01], a
    ld   a, $81
    ldh  [$FF02], a
    ret

serialReadMem:
    ld   a, $D0
    call serialTransfer
    ld   h, a
    ld   a, $D1
    call serialTransfer
    ld   l, a
    ld   a, [hl]
    call serialTransfer
    jr   finishSerialLink

serialWriteMem:
    ld   a, $D8
    call serialTransfer
    ld   h, a
    ld   a, $D9
    call serialTransfer
    ld   l, a
    ld   a, $DA
    call serialTransfer
    cpl
    ld   c, a
    ld   a, $DB
    call serialTransfer
    cp   c
    jr   nz, finishSerialLink
    ld   [hl], a
    jr   finishSerialLink

serialOrMem:
    ld   a, $D8
    call serialTransfer
    ld   h, a
    ld   a, $D9
    call serialTransfer
    ld   l, a
    ld   a, $DA
    call serialTransfer
    cpl
    ld   c, a
    ld   a, $DB
    call serialTransfer
    cp   c
    jr   nz, finishSerialLink
    ld   c, a
    ld   a, [hl]
    or   c
    ld   [hl], a
    jr   finishSerialLink

; Transfer A to the serial link and wait for it to be done and return the result in A
serialTransfer:
    ldh  [$FF01], a
    ld   a, $81
    ldh  [$FF02], a
.loop:
    ldh  a, [$FF02]
    and  $80
    jr   nz, .loop
    ldh  a, [$FF01]
    ret

#ENDIF
