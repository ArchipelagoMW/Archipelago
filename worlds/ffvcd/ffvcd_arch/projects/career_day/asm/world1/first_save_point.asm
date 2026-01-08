hirom


; disable the text box from the first save point
org $C95F18

db $A4, $FD			;Set Event Flag 1FD
db $A4, $21			;Set Event Flag 121
db $FF				;End Event

padbyte $00
pad $C95F22