hirom


; teleporter and explosion beneath ruined city
org $C8916E

db $A4, $FE						;Set Event Flag 1FE
db $A6, $1B						;Set Flag 1B
db $70
db $14
db $71
db $E3, $C0, $00, $A6, $1E, $00	;Inter-map cutscene? C0 00 A6 1E 00
db $A5, $FE						;Clear Event Flag 1FE
db $D4, $3D, $48, $0F			;(Music) 3D 48 0F
db $C3, $04						;Fade in Speed 02
db $73
db $FF							;End event

padbyte $00
pad $C895BE