hirom


; remove the cutscene speaking to the chancellor in the wind shrine
org $C855A0

db $A4, $1F			;Set Event Flag 11F
db $FF				;End Event

padbyte $00
pad $C8563A