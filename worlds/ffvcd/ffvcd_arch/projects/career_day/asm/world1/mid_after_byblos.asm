hirom



; Skip chat with mid after byblos
org $C885CD

db $C4, $03						;Fade in speed 0C
db $73

; ORIGINAL WARP, CHANGED TO GENERIC WARP AREA FOR SAFETY
db $E1, $A9, $00, $94, $28, $00	;Inter-map cutscene? A9 00 94 28 00


db $CB, $A0, $01				;Clear Flag 2/3/4/5/A0 01
db $A2, $35						;Set Event Flag 035
db $CB, $54, $01				;Clear Flag 2/3/4/5/54 01
db $CA, $51, $01				;Set Flag 2/3/4/5/51 01
db $A2, $32						;Set Event Flag 032
db $A2, $33						;Set Event Flag 033
db $CC, $0D                  ;Custom destination flag 0D
db $C3, $03						;Fade in speed 0C
db $73
db $FF							;End Event

padbyte $00
pad $C88849