hirom


; first cutscene at Kuzar where Galuf talks about tablets within chamber
org $C8EA48

db $A2, $5C
db $FF

pad $C8EAB2

; second Void cutscene

org $C93DDD

db $E1, $41, $01, $B0, $09, $00 ;Return from cutscene? 41 01 B0 09 00
db $09                          ;Player Show
db $A2, $0D                     ;Turn on bit 20 at address 0x7e0a15
db $FF                          ;End Event

pad $C93DED