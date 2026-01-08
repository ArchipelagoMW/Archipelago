hirom


; Mid and Cid waking up after fixing the ship
org $C8884A
db $C4, $04                     ;Fade out Speed 04
db $75                          ;Extremely long pause
db $E1, $00, $00, $54, $4F, $B5 ;Return from cutscene? 00 00 54 4F B5
db $14                          ;Player pose: face down, left hand forward
db $C3, $04                     ;Fade in Speed 04
db $75                          ;Extremely long pause
db $A2, $38						;Set Event Flag 038
db $CA, $7A, $01				;Set Flag 2/3/4/5/7A 01
db $CA, $7B, $01				;Set Flag 2/3/4/5/7B 01
db $CB, $89, $01				;Clear Flag 2/3/4/5/89 01
db $CB, $8A, $01				;Clear Flag 2/3/4/5/8A 01
db $CB, $8B, $01				;Clear Flag 2/3/4/5/8B 01
db $CB, $8C, $01				;Clear Flag 2/3/4/5/8C 01
db $CA, $7C, $01				;Set Flag 2/3/4/5/7C 01
db $CA, $7D, $01				;Set Flag 2/3/4/5/7D 01
db $CA, $7E, $01				;Set Flag 2/3/4/5/7E 01
db $CA, $7F, $01				;Set Flag 2/3/4/5/7F 01
db $CC, $0F                  ;Custom destination flag 0F
db $FF							;End Event

padbyte $00
pad $C88954