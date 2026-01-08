hirom


; disable event where butz points out the healing spring
org $C852E7

db $A4, $33			;Set Event Flag 133
db $FF				;End Event

padbyte $00
pad $C852FA
