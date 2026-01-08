hirom


; skip cutscene whre faris complains about getting wet
org $C86489

db $A2, $1F			;Set Event Flag 01F
db $FF              ;End Event

padbyte $00
pad $C864C2