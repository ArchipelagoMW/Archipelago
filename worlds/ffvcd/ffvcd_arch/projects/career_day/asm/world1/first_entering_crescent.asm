hirom


; First time entering crescent and steamship sinking
; This just instantly cuts to the ship sinking and doesn't
; allow exploring crescent during the earthquake.

; I changed it so the event that usually happens when you leave crescent
; while the earthquake is happening actually just plays when you
; enter crescent.
org $C889D9

db $B4, $17						;Play Background Music Danger!
db $BE, $4A						;Rumble effect of 4A magnitude
db $73
db $7C							;<Unknown>
db $A4, $FE						;Set Event Flag 1FE
db $E3, $00, $00, $D8, $C9, $00	;Inter-map cutscene? 00 00 D8 C9 00
db $0A							;Player Hide
db $D2, $00, $CD, $CA, $B5		;(Map) 00 CD CA B5
db $C3, $10						;Fade in Speed 10
db $BE, $45						;Rumble effect of 45 magnitude
db $CE, $0A, $01				;Play next 01 bytes 0A times
db $04							;Player move Left
db $C1, $05						;<Unknown>
db $BF, $15						;Sprite effect 15
db $C1, $00						;<Unknown>
db $C4, $04						;Fade out Speed 04
db $D0, $82, $80				;(Music) 82 80
db $D0, $81, $80				;(Music) 81 80
db $B3, $14						;Pause for 140 cycles
db $D0, $F2, $00				;(Music) F2 00
db $BE, $40						;Rumble effect of 40 magnitude
db $CA, $75, $03				;Set Flag 2/3/4/5/75 03
db $CA, $76, $03				;Set Flag 2/3/4/5/76 03
db $CA, $77, $03				;Set Flag 2/3/4/5/77 03
db $CA, $E9, $01				;Set Flag 2/3/4/5/E9 01
db $CA, $EA, $01				;Set Flag 2/3/4/5/EA 01
db $CB, $EC, $01				;Clear Flag 2/3/4/5/EC 01
db $CB, $EE, $01				;Clear Flag 2/3/4/5/EE 01
db $CA, $FD, $01				;Set Flag 2/3/4/5/FD 01
db $E1, $00, $00, $D8, $C9, $00	;Return from cutscene? 00 00 D8 C9 00
db $A5, $FE						;Clear Event Flag 1FE
db $E1, $B8, $40, $18, $2A, $00	;Return from cutscene? B8 40 18 2A 00
db $09							;Player Show
db $C3, $0A						;Fade in Speed 0A
db $C2, $05						;Map 05
db $A2, $39						;Set Event Flag 039
db $FF							;End Event

db $FF							;End Event

padbyte $00
pad $C88A39