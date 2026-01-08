hirom

org $C91D7A

db $D0, $81, $80		;(Music) 81 80
db $03				;Player Move Down
db $72				;Long pause
db $B4, $34			;Play Background Music Good Night!
db $C4, $04			;Fade out Speed 04
db $B3, $0A			;Pause for 0A0 cycles
db $7D				;<Unknown>
db $CD, $7F, $05		;Run event index 057F
db $74				;Extremely long pause
db $C3, $10			;Fade in Speed 10
db $C9, $68, $0F		;Play Music 68 0F
db $DB				;Restore Player status
db $73				;Extremely long pause
db $14				;Player pose: face down, left hand forward
db $FF				;End Event

pad $C91DF2