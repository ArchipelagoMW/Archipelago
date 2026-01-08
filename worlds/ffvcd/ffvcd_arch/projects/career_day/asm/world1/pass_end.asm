hirom



; Removes the post earthquake cutscene
org $C956DD

db $B5, $7E							;Play Sound Effect ?
db $BE, $09							;Rumble effect of 09 magnitude
db $F3, $0A, $0C, $24				;Set Map Tiles 0A 0C 24
db $D0, $D1, $D2					;(Music) D1 D2
db $D3, $D4, $E0, $E1				;Sprite D4 set map position E0, E1
db $E2, $E3							;Unknown
db $E4, $F0							;Unknown
db $F1, $F2							;Unknown
db $F3, $F4, $06, $01				;Set Map Tiles F4 06 01
db $01								;Player Move Up
db $BE, $05							;Rumble effect of 05 magnitude
db $01								;Player Move Up
db $D0, $80, $80					;(Music) 80 80
db $C4, $02							;Fade out Speed 03
db $75              				;Wait a long time
;db $B7, $02							;Add/Remove character 02
;db $B7, $09							;Add/Remove character 09
db $A4, $E1         				;Set Event Flag 1E1
db $A2, $11							;Set Event Flag 011
db $CD, $7F, $05					;Run event index 057F
db $A4, $FF							;Set Event Flag 1FF
db $A4, $FE							;Clear Event Flag 1FE
db $BE, $00							;Rumble effect of 00 magnitude
db $E1, $00, $00, $9C, $8B, $00		;Return from cutscene? 00 00 9C 8B 00
db $C3, $02							;Fade in Speed 02
db $74
db $B4, $23         				;Play overworld music
db $FF              				;End event

padbyte $00
pad $C9588F