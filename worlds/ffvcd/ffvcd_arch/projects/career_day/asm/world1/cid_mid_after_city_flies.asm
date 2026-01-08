hirom


; telling cid and mid about the flying city
org $C897A3

db $CD, $5F, $01				;Run event index 015F
db $C4, $0C						;Fade out speed 0C
db $A2, $46						;Set Event Flag 046
db $72							;Shortish pause
db $84, $0A						;Sprite 084 Hide
db $83, $0A						;Sprite 083 Hide
db $C3, $0C						;Fade in speed 0C

db $CC, $13                 	;Custom destination flag 13
db $FF							;End event

padbyte $00
pad $C89895