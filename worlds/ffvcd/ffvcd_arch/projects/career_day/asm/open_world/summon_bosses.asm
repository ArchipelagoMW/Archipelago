hirom

; corresponds to SHOAT GOLEM RAMUH

; disable groups for 3 summons
; Ramuh
org $D068B8 ; world map 1 
db $6E, $00, $6E, $00
org $D06BC6 ; rift
db $6E, $00
; org $D07010  ; very unsure about this one, don't think its necessary
; db $6E, $00

; Shoat
org $d069a8
db $CD

; Golem
org $D06EB8
db $B2, $00
org $D06EB0
db $B2, $00


; write formation flags to not run away
org $D034C1
db $FF
org $D03BB1
db $FF
org $D03A51
db $FF

; give them boss music
org $D034CE
db $08
org $D03BBE
db $08
org $D03A5E
db $08
