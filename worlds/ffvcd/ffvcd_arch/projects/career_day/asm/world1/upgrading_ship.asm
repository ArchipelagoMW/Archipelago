hirom


; giving adamantium to cid/mid to upgrade ship
org $C89896

db $E3, $D2, $00, $9E, $0A, $00		;Inter-map cutscene? D2 00 9E 0A 00
db $75								;Extremely long pause
db $C3, $0A							;Fade in Speed 0A
db $75								;Extremely long pause
db $20								;Player pose: face down, left hand raised out
db $71								;Short pause
db $C8, $53, $00					;Display Message/Text/Dialogue 53 00
db $B4, $28							;Play Background Music The Airship
db $14								;Player pose: face down, left hand forward
db $CD, $A0, $00					;Run event index 00A0
db $A5, $FE							;Clear Event Flag 1FE
db $A2, $4A							;Set Event Flag 04A
db $A4, $FA							;Set Event Flag 1FA

db $CC, $12                 		;Custom destination flag 12
db $FF								;End event

padbyte $00
pad $C899F7