hirom



; short text to boko after fighting the antlion
org $C91D35

db $C4, $10						;Fade out Speed 10
db $70							;Very short pause
db $77							;<Unknown>
db $03							;Player Move Down
db $76							;<Unknown>
db $E1, $2A, $41, $20, $20, $00	;Return from cutscene? 2A 41 20 20 00
db $B1, $07						;Set Player Sprite 07
db $C3, $0A						;Fade in Speed 0A
db $01							;Player Move Up
db $01							;Player Move Up
db $83, $09						;Sprite 083 do event: Show
db $B1, $02						;Set Player Sprite 02
db $06							;Player Bounce in Place
db $01							;Player Move Up
db $CE, $06, $02				;Play next 02 bytes 06 times
db $83, $03						;Sprite 083 do event: Move Down
db $83, $0A						;Sprite 083 do event: Hide
db $D2, $02, $6F, $66, $24		;(Map) 02 6F 66 24
db $FF							;End Event

padbyte $00
pad $C91D5E