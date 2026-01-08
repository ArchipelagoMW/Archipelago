hirom


; even where the party sees the pirates and hides behind the rock
org $C85406

db $A4, $1C			;Set Event Flag 11C
db $FF				;End Event

padbyte $00
pad $C854AC