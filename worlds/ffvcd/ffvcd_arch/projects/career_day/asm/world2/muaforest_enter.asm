hirom


; Enter Mua forest. Theoretically could set flag $72 instead elsewhere, but decided it was simple enough to remove text boxes on first run

org $C8DB7D

db $CD, $79, $03                ;Run event index 0379
db $CD, $7A, $03                ;Run event index 037A
db $CD, $7B, $03                ;Run event index 037B
db $A2, $72                     ;Set Event Flag 072
db $FF                          ;End Event

padbyte $00
pad $C8DB8E