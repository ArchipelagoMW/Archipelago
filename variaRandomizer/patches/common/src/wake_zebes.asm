arch snes.cpu
lorom

;;; Door ASM pointer (Door into small corridor before construction zone)
org $838eb4
    db $00, $ff

;;; Door ASM to force Zebes awake event.
;;; With the new nothing item plm we can really have no item collected at morph ball location,
;;; so always wake zebes when we traverse the door.
org $8fff00
    lda $7ed820                 ; load Event bit array.
    ora.w #$0001                ; 1:   Event 0 - Zebes is awake
    sta $7ed820                 ; update RAM
    rts
