hirom


; Siren encounter
org $C866DE

db $8A, $09				;Sprite 08A do event: Show
db $8B, $09             ;Sprite 08B do event: Show
db $06					;Player Bounce in Place
db $01					;Player Move Up
db $01					;Player Move Up
db $01					;Player Move Up
db $01					;Player Move Up
db $01					;Player Move Up
db $01					;Player Move Up
db $01					;Player Move Up
db $01					;Player Move Up
db $73					;Medium wait
db $8A, $0A				;Sprite 08A do event: Hide
db $8B, $0A             ;Sprite 08B do event: Hide
db $BD, $03, $06		;Start Event Battle 03
db $C5, $80
db $B5, $02
db $71
db $DE, $63 ; custom reward
db $DF
db $A2, $21				;Set Event Flag 021
db $CC, $06                  ;Custom destination flag 06

; CAREERDAY
; Set airship outside
db $D2, $00, $D6, $2D, $D8


db $FF					;End Event

padbyte $00
pad $C869A9