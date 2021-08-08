;;; Opens Maridia Tube for Watering Hole start to have more varied seed starts
;;;
;;; compile with asar (https://www.smwcentral.net/?a=details&id=14560&p=section),
;;; or a variant of xkas that supports arch directive

arch snes.cpu
lorom

;;; door ASM ptr for door associated to save starting point
org $83a4a2
    dw open_tube

org $8ff400
open_tube:
    lda #$000b : jsl $8081fa
    rts

warnpc $8ff40f

