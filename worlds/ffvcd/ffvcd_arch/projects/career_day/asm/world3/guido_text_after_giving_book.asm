hirom



; remove long speech guido gives if you talk to him after getting the book
org $C9F347

db $C8, $20, $08	;Display Message/Text/Dialogue 20 08
db $93, $12			;Sprite 193 do event: face right, standing
db $FF				;End Event

padbyte $00
pad $C9F35B