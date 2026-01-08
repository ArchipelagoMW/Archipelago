hirom


; Guard outside of tycoon (simply disables messages)
org $C88D0C

db $E3, $A4, $00, $16, $15, $00	;Inter-map cutscene? A4 00 16 15 00
db $D3, $88, $96, $0D			;Sprite 88 set map position 96, 0D
db $D3, $89, $96, $0C			;Sprite 89 set map position 96, 0C
db $88, $09						;Sprite 088 do event: Show
db $89, $09						;Sprite 089 do event: Show
db $C3, $0C						;Fade in Speed 0C
db $01							;Player move up
db $01							;Player move up
db $88, $10
db $89, $10
db $CF, $05, $04				;Play next 04 bytes simultaneously 05 times
db $88, $03						;Sprite 088 do event: Move Down
db $89, $03						;Sprite 089 do event: Move Down
db $75
db $E3, $00, $00, $4F, $78, $00	;Inter-map cutscene? 00 00 4F 78 00
db $DB							;Restore Player status
db $14							;Player pose: face down, left hand forward
db $C3, $08						;Fade in Speed 08
db $74							;Very long pause
db $A2, $3B						;Set Event Flag 03B
db $CC, $11                  ;Custom destination flag 11
db $FF							;End Event

padbyte $00
pad $C88DDF 