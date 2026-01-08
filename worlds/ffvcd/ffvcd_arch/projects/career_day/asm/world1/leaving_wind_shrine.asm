hirom


; speed up the warp and skip Boko's tutorial prompt
org $C85B90

db $CD, $5B, $05				;Run event index 055B
db $73							;Medium pause
db $E3, $1B, $00, $13, $15, $00	;Inter-map cutscene? 00 00 B6 35 00
db $09							;Player Show
db $03
db $D3, $80, $40, $07			;Sprite 80 set map position 40, 07
db $C3, $02						;Fade in Speed 02
db $CC, $03                  ;Custom destination flag 03
db $FF							;End Event

padbyte $00
pad $C85BD8

; world 3 version
org $C9F861
db $14                          ;Player pose: face down, left hand forward
db $71                          ;Short pause
db $CD, $73, $07                ;Run event index 0773
db $CD, $5B, $05                ;Run event index 055B
db $75                          ;Extremely long pause
db $CD, $59, $05                ;Run event index 0559
db $E1, $1B, $00, $13, $15, $00	;Inter-map cutscene? 00 00 B6 35 00
db $14                          ;Player pose: face down, left hand forward
db $C3, $0C                     ;Fade in Speed 0C
db $73                          ;Long pause
db $FF                          ;End Event
