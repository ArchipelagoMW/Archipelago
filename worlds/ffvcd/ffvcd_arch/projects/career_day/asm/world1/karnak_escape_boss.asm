hirom

; rewrite location of event

org $C83476
db $80, $80, $C8

; in new freed area, write event
org $C88080
db $BD, $08, $FF                ;Start Event Battle 08
db $A2, $31                     ;Turn on bit 02 at address 0x7e0a1a
db $C5, $80
db $B5, $02
db $71
db $DE, $67 ; custom reward
db $DF
db $A2, $30
db $FF                          ;End Event


org $F04BF3
db $FD, $31, $FC, $DB