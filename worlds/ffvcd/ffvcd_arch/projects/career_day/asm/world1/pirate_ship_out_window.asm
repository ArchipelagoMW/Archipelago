hirom


; event where party witnesses the syldra pulled ship
; disable the event and set the flags.
org $C853A2

db $A2, $14			;Set Event Flag 014
db $FF

padbyte $00
pad $C85405