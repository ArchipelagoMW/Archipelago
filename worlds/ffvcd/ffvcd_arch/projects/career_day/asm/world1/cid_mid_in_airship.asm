hirom


; discovering the airship to the point that you're flying, before crayclaw
org $C89611

db $C4, $10						;Fade out speed 10
db $A4, $E5						;Set Event Flag 1E5
db $A4, $FE						;Set Event Flag 1FE
db $CD, $15, $00				;Run event index 0015
db $A5, $FE						;Clear Event Flag 1FE
db $CB, $F2, $00				;Clear Flag 2/3/4/5/F2 00
db $CB, $F3, $00				;Clear Flag 2/3/4/5/F3 00
db $A3, $B0						;Clear Event Flag 0B0
db $A2, $B1						;Set Event Flag 0B1
db $A3, $B2						;Clear Event Flag 0B2
db $A4, $00						;Set Event Flag 100
db $E0, $BE, $00, $9E, $16, $00	;Unknown  (related to cutscene)
db $A4, $00						;Set Event Flag 100
db $FF							;End event

padbyte $00
pad $C8967A