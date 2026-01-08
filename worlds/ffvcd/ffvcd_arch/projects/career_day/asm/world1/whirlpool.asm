hirom


; whirlpool to ship graveyard, including karlabos
org $C88271

db $03							;Player Move Down
db $03							;Player Move Down
db $D0, $81, $40				;(Music) 81 40
db $B5, $3C						;Play Sound Effect Exdeath destroyed 1
db $70							;Very short pause
db $BE, $0A						;Rumble effect of 0A magnitude
db $F3, $35, $27, $22			;Set Map Tiles 35 27 22
db $C5							;<unknown>
db $C6, $C7						;Add job C7
db $D5, $D6, $D7, $E5			;(Sound) D6 D7 E5
db $E6, $E7						;Unknown
db $71							;Short pause
db $BE, $05						;Rumble effect of 05 magnitude
db $B3, $0A						;Pause for 0A0 cycles
db $D0, $82, $20				;(Music) 82 20
db $03							;Player Move Down
db $03							;Player Move Down
db $03							;Player Move Down
db $03							;Player Move Down
db $02							;Player Move Right
db $BD, $02, $FF				;Start Event Battle 02
db $C5, $80
db $B5, $02
db $71
db $DE, $62 ; custom reward
db $DF
; db $D2, $00, $54, $4F, $B5		;(Map) 00 54 4F B5
db $A4, $22						;Set Event Flag 122
db $BE, $00						;Rumble effect of 00 magnitude
db $C4, $0C						;Fade out Speed 0C
db $74							;Longish pause
db $B1, $02						;Set Player Sprite 02
db $E1, $2B, $00, $8B, $19, $00	;Return from cutscene? 2B 00 8B 19 00
db $CD, $7F, $05				;Run event index 057F ;Party Heal
db $C3, $08						;Fade in Speed 0C
db $FF

padbyte $00
pad $C88380