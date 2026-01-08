hirom


; skip cutscene where the boys discover faris is a girl
org $C864C3

db $A2, $20			;Set Event Flag 020
db $FF				;Event End

padbyte $00
pad $C866DD