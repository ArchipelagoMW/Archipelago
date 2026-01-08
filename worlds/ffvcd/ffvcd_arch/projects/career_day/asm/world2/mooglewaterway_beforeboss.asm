hirom


org $C90E7C

; Moogle dialogue before boss
; Sets flag, immediately ends. Player won't notice

; db $A2, $5E                     ;Set Event Flag 05E
db $FF                                 ;End Event

padbyte $00
pad $C90E94