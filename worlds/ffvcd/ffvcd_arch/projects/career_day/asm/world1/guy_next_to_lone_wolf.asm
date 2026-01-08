hirom


; Speed up guy next to lone wolf
org $C930CC

db $81, $02			;Sprite 081 do event: Move Right
db $81, $03			;Sprite 081 do event: Move Down
db $81, $03			;Sprite 081 do event: Move Down
db $81, $03			;Sprite 081 do event: Move Down
db $F0, $9D, $01	;Yes/No Dialogue box (message is 9D 01)
db $CD, $BE, $02	;Run event index 02BE
db $FF				;End Event
db $00, $00, $00	;Display Message/Text/Dialogue A1 81
db $81, $01			;Sprite 081 do event: Move Up
db $81, $01			;Sprite 081 do event: Move Up
db $81, $01			;Sprite 081 do event: Move Up
db $81, $04			;Sprite 081 do event: Move Left
db $81, $24			;Sprite 081 do event: face down, right hand raised in
db $14				;Player pose: face down, left hand forward
db $FF				;End Event
db $81, $01			;Sprite 081 do event: Move Up
db $81, $01			;Sprite 081 do event: Move Up
db $81, $01			;Sprite 081 do event: Move Up
db $81, $01			;Sprite 081 do event: Move Up
db $81, $04			;Sprite 081 do event: Move Left
db $BE, $4F			;Rumble effect of 4F magnitude
db $81, $5B			;Sprite 081 do event: 5B
db $81, $05			;Sprite 081 do event: Bounce
db $81, $03			;Sprite 081 do event: Move Down
db $BE, $40			;Rumble effect of 40 magnitude
db $81, $24			;Sprite 081 do event: face down, right hand raised in
db $14				;Player pose: face down, left hand forward
db $FF				;End Event

padbyte $00
pad $C9312E