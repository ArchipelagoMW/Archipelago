hirom


; After picking up final crystal
org $C8729A

db $B4, $31			;Play Background Music Run!
db $B5, $84			;Play Sound Effect Exdeath destroyed 2
db $BE, $49			;Rumble effect of 49 magnitude
db $F3, $08, $02, $10		;Set Map Tiles 08 02 10
db $7E				;<Unknown>
db $8E, $BE			;Sprite 08E do event: BE
db $FF

padbyte $00
pad $C872D2

; Walse tower sink cutscene
org $C88B26



db $C4, $04
db $75
db $BE, $00						;Rumble effect of 4F magnitude
; db $A4, $E3						;Set Event Flag 1E3 (disabled for arch)
db $E1, $00, $00, $CB, $57, $00	;Return from cutscene? 00 00 CB 57 00
db $D2, $00, $CA, $57, $D8
; db $D2, $00, $CD, $56, $6C		;(Map) 00 CD 56 6C
db $DB							;Restore Player status
db $C3, $04						;Fade in Speed 04
db $CA, $C4, $00				;Set Flag 2/3/4/5/C4 00
db $CA, $D0, $00				;Set Flag 2/3/4/5/D0 00
db $CA, $D1, $00				;Set Flag 2/3/4/5/D1 00
db $CA, $B5, $00				;Set Flag 2/3/4/5/B5 00
db $CA, $C6, $00				;Set Flag 2/3/4/5/C6 00
db $CB, $E9, $00				;Clear Flag 2/3/4/5/E9 00
db $CB, $9F, $00				;Clear Flag 2/3/4/5/9F 00
db $CB, $A0, $00				;Clear Flag 2/3/4/5/A0 00

db $FF

padbyte $00
pad $C88CF3