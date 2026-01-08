hirom


; Just fade out and come back with the door open and Cid gone
org $C875CA

db $C4, $03				;Fade out speed 02
db $73					;Wait a bit
db $83, $0A
db $B5, $8E				;Play Sound Effect Treasure chest
db $F3, $18, $37, $20	;Set Map Tiles 18 37 20
db $07					;<Unknown>
db $17					;Player pose: face left, down hand backward
db $01					;Player Move Up
db $BE, $00				;Rumble effect of 00 magnitude
db $A4, $01				;Set Event Flag 101
db $B5, $8E				;Play Sound Effect Treasure chest
db $F3, $14, $3B, $20	;Set Map Tiles 14 3B 20
db $07					;<Unknown>
db $17					;Player pose: face left, down hand backward
db $01					;Player Move Up
db $BE, $00				;Rumble effect of 00 magnitude
db $A4, $06				;Set Event Flag 106
db $B4, $33				;Play Background Music Royal Palace
db $A2, $2D				;Set Event Flag 02D
db $CB, $69, $01		;Clear Flag 2/3/4/5/69 01
db $CB, $53, $01		;Clear Flag 2/3/4/5/53 01
db $CB, $72, $01		;Clear Flag 2/3/4/5/72 01
db $CA, $73, $01		;Set Flag 2/3/4/5/73 01
db $CA, $74, $01		;Set Flag 2/3/4/5/74 01
db $CA, $75, $01		;Set Flag 2/3/4/5/75 01
db $CA, $76, $01		;Set Flag 2/3/4/5/76 01
db $CB, $56, $01		;Clear Flag 2/3/4/5/56 01
db $CA, $52, $01			;Set Flag 2/3/4/5/52 01
db $A2, $2E					;Set Event Flag 02E
db $C3, $03				;Fade in speed 02
db $73					;Wait a bit
db $FF					;End Event

padbyte $00
pad $C878B0