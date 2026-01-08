hirom


; discovering the airship
org $C89678

db $03
db $19                          ;Player pose: face up, standing
db $D3, $83, $54, $17           ;Sprite 83 set map position 54, 17
db $D3, $84, $53, $17           ;Sprite 84 set map position 53, 17
db $CF, $08, $04                ;Play next 04 bytes simultaneously 07 times
db $83, $02                     ;Sprite 083 do event: Move Right
db $84, $02                     ;Sprite 084 do event: Move Right

db $CF, $01, $04                ;Play next 04 bytes simultaneously 07 times
db $83, $01                     ;Sprite 083 do event: Move Right
db $84, $02                     ;Sprite 084 do event: Move Right

db $CF, $08, $04                ;Play next 04 bytes simultaneously 07 times
db $83, $01                     ;Sprite 083 do event: Move Right
db $84, $01                     ;Sprite 084 do event: Move Right

; db $CF, $01, $04                ;Play next 04 bytes simultaneously 07 times
; db $83, $03                     ;Sprite 083 do event: Move Right
; db $84, $02                     ;Sprite 084 do event: Move Right

; db $CF, $01, $04                ;Play next 04 bytes simultaneously 07 times
db $83, $0A						;Sprite 084 Hide
; db $84, $03                     ;Sprite 084 do event: Move Right
db $84, $0A						;Sprite 083 Hide

db $A2, $43					;Set Event Flag 043
db $FF						;End event

padbyte $00
pad $C89715