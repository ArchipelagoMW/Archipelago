
;;; makes it so that BT will wake up only once you picked up
;;; the item he's holding, whatever it is

lorom
arch snes.cpu

!CurrentRoom = $7e079b
!BTRoom      = #$9804
!BTRoomFlag  = $7ed86c		; some free RAM for the flag
!PickedUp    = #$bbbb

;;; hijack item collection routine (different hijack point than endingtotals.asm)
org $8488a7
    jsr btflagset

org $84f840
btflagset:
    pha			; save A to perform original ORA afterwards
    ;; check if we're in BT room
    lda !CurrentRoom
    cmp !BTRoom
    bne .end
    ;; set flag "picked up BT's item"
    lda !PickedUp
    sta !BTRoomFlag
.end:
    pla
    ora $05e7 		; original hijacked code
    rts

;;; check if we picked up BT's item, zero flag set if we do
btcheck:
    lda !BTRoomFlag
    cmp !PickedUp
    rts

warnpc $84f860

;;; overwrite BT grey door PLM instruction (bomb check)
org $84ba6f
    jsr btcheck
    nop : nop : nop
    bne $03	                ; orig: BEQ $03    ; return if no bombs

;;; overwrite BT PLM pre-instruction (bomb check)
org $84d33b
    jsr btcheck
    nop : nop : nop
    bne $13			; orig: BEQ $13    ; return if no bombs
