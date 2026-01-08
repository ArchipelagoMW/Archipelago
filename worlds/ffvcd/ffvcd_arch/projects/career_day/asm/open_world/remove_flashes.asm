
; the below disables ALL battle screen flashing
; ; disable white screen flashing
; org $C178FA
; nop ; #EA = nop via 7EF8C7
; nop;
; nop;



; disable white screen flashing on Grand Cross
org $C1CB4B
nop ; #EA = nop via 7EF8C7
nop;
nop;



; #EA = nop via 7EF8C7
; disable omega post battle flash
org $C9F8FF
db $71				;Short pause
db $CE, $14, $04		;Play next 06 bytes 14 times
db $D0, $1A, $00		;(Music) 1A 00
db $70				;Very short pause
db $D0, $82, $80		;(Music) 82 80
db $BE, $0A			;Rumble effect of 0A magnitude
db $72				;Extremely long pause
db $BE, $00			;Rumble effect of 00 magnitude
db $FF				;End Event