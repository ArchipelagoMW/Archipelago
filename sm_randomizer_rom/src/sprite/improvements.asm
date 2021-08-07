; --- QoL improvements ---

; This bug prevents left and right morphball from being different.
; Also fixes the tilemaps
;$E508
;AFP_T31:    ;Midair morphball facing right without springball
;AFP_T32:    ;Midair morphball facing left without springball

org $92D9B2 : dw $E530
org $9292C7 : dw $071A    ; upper tilemap
org $9294C1 : dw $071A    ; lower tilemap


; The second byte here is probably supposed to be $10, just like the previous
; animation. $F0 is a terminator which is onnly ever be invoked here (besides
; there being a pose in this spot!)
;$B361
;FD_6D:    ;Falling facing right, aiming upright
;FD_6E:    ;Falling facing left, aiming upleft
;FD_6F:    ;Falling facing right, aiming downright
;FD_70:    ;Falling facing left, aiming downleft
;DB $02, $F0, $10, $FE, $01

org $91B361+1 : db $10


; The second byte here is supposed to be $00, but because it is not, the
; missile port is rendered behind Samus's left fist during elevator pose.
;$c9db
;XY_P00:    ;00:;Facing forward, ala Elevator pose (power suit)
;XY_P9B:    ;9B:;Facing forward, ala Elevator pose (Varia and/or Gravity Suit)
;DB $00, $02

org $90C9DB+1 : db $00


; --- Cannon ports ---

; Cannon port position is mostly left intact, but the set of downwards aiming
; ports are super broken.

; Redirects to new XY lists

org $90C80F : dw $CB31
org $90C839 : dw $CAC5
org $90C83B : dw $CB31


; New XY lists

org $90CAC5
    db $83, $01, $84, $01, $0B, $01, $00, $0D
org $90CB31
    db $86, $01, $85, $01, $ED, $01, $F7, $0D


; The set of the right-facing jump begin/land missile port placements is
; inconsistent across the animations and even omitted in many animations.
; We choose to make it consistent by always omitting it.

org $90CAD1 : db $00, $00
org $90CBF9 : db $00, $00
org $90CC05 : db $00, $00


; In these cases the cannon was actually placed onto the gun port backwards...
;$CBA5
;XY_P49:    ;49:;Moonwalk, facing left
;DB $02, $01
;DB $F1, $FD, $F1, $FC, $F1, $FC, $F1, $FD, $F1, $FC, $F1, $FC
;$CBB3
;XY_P4A:    ;4A:;Moonwalk, facing right
;DB $07, $01
;DB $07, $FD, $07, $FC, $07, $FC, $07, $FD, $07, $FC, $07, $FC

org $90CBA5
    db $07, $01, $ED, $FD, $ED, $FC, $ED, $FC, $ED, $FD, $ED, $FC, $ED, $FC
org $90CBB3
    db $02, $01, $0B, $FD, $0B, $FC, $0B, $FC, $0B, $FD, $0B, $FC, $0B, $FC
