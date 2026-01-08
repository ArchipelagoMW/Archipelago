hirom


; going near the ruined city and the city flying into the air
org $C89B54

db $BE, $45						;Rumble effect of 45 magnitude
db $71
db $C4, $03
db $73
db $CD, $A4, $04				;Run event index 04A4
db $CD, $5E, $01				;Run event index 015E
db $E1, $00, $20, $41, $A0, $D8	;Return from cutscene? 00 20 41 A0 D8
db $09							;Player Show
db $C3, $02						;Fade in Speed 02
db $A5, $FE						;Clear Event Flag 1FE

db $CC, $14                  ;Custom destination flag 14
db $FF							;End event

padbyte $00
pad $C89B79

; disable the meat of this cutscene. Has to happen here because calling
; the "city fly" event raw on the map causes bad sprites to show
org $C907C7

db $D5, $84, $04, $00			;(Sound) 84 04 00
db $73							;Sort of long pause
db $A4, $E6						;Set Event Flag 1E6
db $BE, $00						;Cancel rumble
db $FF							;End Event

padbyte $00
pad $C907EE

org $C982C4

db $B1, $02                     ;Set Player Sprite 02
db $80, $09                     ;Sprite 080 do event: Show
db $81, $09                     ;Sprite 081 do event: Show
db $82, $09                     ;Sprite 082 do event: Show
db $D8, $80, $DF
db $D8, $81, $E0                     ;Sprite 081 do event: E0
db $D8, $82, $1F
db $FF