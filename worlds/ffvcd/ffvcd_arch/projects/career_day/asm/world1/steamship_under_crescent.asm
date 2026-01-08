hirom


; discovering the steamship
org $C895D8

db $CD, $94, $00				;Run event index 0094
db $02							;Player Move Right
db $02							;Player Move Right
db $02							;Player Move Right
db $A2, $B0						;Set Event Flag 0B0
db $A3, $B1						;Clear Event Flag 0B1
db $A3, $B2						;Clear Event Flag 0B2
db $FF							;End event

padbyte $00
pad $C895E7