hirom


; party trying to steal faris' ship
org $C96869

db $C4, $04			;Fade out Speed 04
db $75				;Extremely long pause
db $CD, $7F, $05		;Run event index 057F
db $A5, $FE			;Clear Event Flag 1FE
db $E1, $00, $00, $A1, $70, $B4	;Return from cutscene? 00 00 A1 70 B4
db $09				;Player Show
db $01				;Player Move Up
db $71				;Short pause
db $C3, $08			;Fade in Speed 08
db $75				;Extremely long pause
;db $B7, $0B			;Add/Remove character 0B
db $CB, $34, $00		;Clear Flag 2/3/4/5/34 00
db $CB, $36, $00		;Clear Flag 2/3/4/5/36 00
db $CB, $37, $00		;Clear Flag 2/3/4/5/37 00
db $CA, $38, $00		;Set Flag 2/3/4/5/38 00
db $CA, $39, $00		;Set Flag 2/3/4/5/39 00
db $CA, $3A, $00		;Set Flag 2/3/4/5/3A 00
db $A2, $15			;Set Event Flag 015
db $CC, $02                  ;Custom destination flag 02
db $FF				;End Event

padbyte $00
pad $C96E50