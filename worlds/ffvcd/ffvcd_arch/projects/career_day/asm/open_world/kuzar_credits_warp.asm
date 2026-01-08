; NPC in Kuzar gives access to credits 
org $C848AD
db $50, $F4, $C9

org $C9F450
db $B4, $11                     ;Play Background Music (Nothing)
db $B7, $0C 					; add cara over galuf for non glitchy ending...?
db $C4, $04                     ;Fade out Speed 06
db $74
db $74
db $CD, $43, $01                ;Run event index 0143
db $FF

org $E34157
;Would you like to access
db $76, $88, $8E, $85, $7D, $96, $92, $88, $8E, $96, $85, $82, $84, $7E, $96, $8D, $88, $96, $7A, $7C, $7C, $7E, $8C, $8C, $01
;the credits sequence? 
db $8D, $81, $7E, $96, $7C, $8B, $7E, $7D, $82, $8D, $8C, $96, $8C, $7E, $8A, $8E, $7E, $87, $7C, $7E, $CB, $96, $01
; This will immediately
db $73, $81, $82, $8C, $96, $90, $82, $85, $85, $96, $82, $86, $86, $7E, $7D, $82, $7A, $8D, $7E, $85, $92, $01
;end the game.
db $7E, $87, $7D, $96, $8D, $81, $7E, $96, $80, $7A, $86, $7E, $A3, $00
