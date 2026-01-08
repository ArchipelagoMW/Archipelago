hirom


; This cutscene is a real doozy, I'll do my best to explain it here.
; The first section of this patch removes the whole "pre-falling down"
; portion of the event. The second part of this patch is what retains
; the state of the room when you walk back UP into the crystal room
; from the downstairs room.

; This is where all the important flags are set, these are largely the fires
; in the castle proper, but also relocks many doors and sets some chests. This
; event is largely "normal" as far as strategy to hack an event is concerened.
; In fact, as long as this hack is run before the second one, you don't even have
; to be as precise with the padding as I have been (the second patch will overwrite the 00s)
org $C878DA
db $01				;Player Move Up
db $01				;Player Move Up
db $F3, $1A, $0E, $22, $8B, $D4 ;Set Map Tiles 1A 0E 22 8B D4
db $8D, $E3                     ;Sprite 08D do event: E3
db $E4, $E5                     ;Unknown
db $F3, $F4, $F5, $73, $BE, $00 ;Set Map Tiles F4 F5 73 BE 00
db $C4, $03						;Fade out at speed 0C
db $73
db $CD, $76, $07				;Run event index 0776
db $A4, $FE						;Set Event Flag 1FE
db $CB, $6B, $01				;Clear Flag 2/3/4/5/6B 01
db $CA, $6C, $01				;Set Flag 2/3/4/5/6C 01
db $CB, $58, $01				;Clear Flag 2/3/4/5/58 01
db $CB, $59, $01				;Clear Flag 2/3/4/5/59 01
db $CB, $5A, $01				;Clear Flag 2/3/4/5/5A 01
db $CB, $5B, $01				;Clear Flag 2/3/4/5/5B 01
db $CB, $5C, $01				;Clear Flag 2/3/4/5/5C 01
db $CB, $5D, $01				;Clear Flag 2/3/4/5/5D 01
db $CB, $5E, $01				;Clear Flag 2/3/4/5/5E 01
db $CB, $5F, $01				;Clear Flag 2/3/4/5/5F 01
db $CB, $60, $01				;Clear Flag 2/3/4/5/60 01
db $CB, $61, $01				;Clear Flag 2/3/4/5/61 01
db $CB, $62, $01				;Clear Flag 2/3/4/5/62 01
db $CB, $63, $01				;Clear Flag 2/3/4/5/63 01
db $CB, $64, $01				;Clear Flag 2/3/4/5/64 01
db $CB, $65, $01				;Clear Flag 2/3/4/5/65 01
db $CB, $66, $01				;Clear Flag 2/3/4/5/66 01
db $CB, $67, $01				;Clear Flag 2/3/4/5/67 01
db $CB, $68, $01				;Clear Flag 2/3/4/5/68 01
db $CB, $69, $01				;Clear Flag 2/3/4/5/69 01
db $CB, $57, $01				;Clear Flag 2/3/4/5/57 01
db $CB, $6B, $01				;Clear Flag 2/3/4/5/6B 01
db $CA, $6C, $01				;Set Flag 2/3/4/5/6C 01
db $CA, $6D, $01				;Set Flag 2/3/4/5/6D 01
db $CA, $6E, $01				;Set Flag 2/3/4/5/6E 01
db $CA, $6F, $01				;Set Flag 2/3/4/5/6F 01
db $CA, $70, $01				;Set Flag 2/3/4/5/70 01
db $CA, $71, $01				;Set Flag 2/3/4/5/71 01
; db $A2, $30						;Set Event Flag 030 	move this to karnak escape boss
db $CB, $52, $01				;Clear Flag 2/3/4/5/52 01
db $CA, $54, $01				;Set Flag 2/3/4/5/54 01
db $CB, $73, $01				;Clear Flag 2/3/4/5/73 01
db $CB, $74, $01				;Clear Flag 2/3/4/5/74 01
db $CB, $75, $01				;Clear Flag 2/3/4/5/75 01
db $CB, $76, $01				;Clear Flag 2/3/4/5/76 01
db $D7, $96, $20, $05			;(Timer?) 96 20 05
db $A4, $DB						;Set Event Flag 1DB
db $E1, $92, $00, $B9, $3C, $00	;Return from cutscene? 92 00 B9 3C 00
db $B4, $31						;Play Background Music Hurry! Hurry!
db $B9, $C1						;Toggle Subtracitve Tint by C1
db $C3, $03						;Fade in at speed $0C
db $74							;Medium-long pause
db $FF

padbyte $00
pad $C87EEF


; This is the weird part. This patch MUST have the "Inter Map Cutscene" (db $E3, $91, $00, $8F, $10, $00)
; written at $C87EEF. This is because when you walk back up from the room
; with the healing pot in it, you aren't actually travelling rooms. There's an event
; right in the stairwell and it points to that address, $C87EEF. I left this entire
; portion in tact, as it's a bit unclear to me why all the sprite movement is ocurring.
; The map tile calls are all setting the room back up like you'd expect after the crystal exploded.

;To reiterate, if you change this, LEAVE db $E3, $91, $00, $8F, $10, $00 AT $C87EEF
org $C87EEF

db $E3, $91, $00, $8F, $10, $00	;Inter-map cutscene? 91 00 8F 10 00
db $F3, $80, $00, $32		;Set Map Tiles 80 00 32
db $01				;Player Move Up
db $01				;Player Move Up
db $01				;Player Move Up
db $01				;Player Move Up
db $01				;Player Move Up
db $01				;Player Move Up
db $01				;Player Move Up
db $01				;Player Move Up
db $01				;Player Move Up
db $01				;Player Move Up
db $01				;Player Move Up
db $01				;Player Move Up
db $F3, $1A, $0E, $22		;Set Map Tiles 1A 0E 22
db $8B, $D4			;Sprite 08B do event: D4
db $8D, $E3			;Sprite 08D do event: E3
db $E4, $E5			;Unknown
db $F3, $F4, $F5, $F3		;Set Map Tiles F4 F5 F3
db $15				;Player pose: face down, right hand forward
db $0E				;<Unknown>
db $00				;Player Hold
db $73				;Long pause
db $F3, $18, $15, $12		;Set Map Tiles 18 15 12
db $BE, $BE			;Rumble effect of BE magnitude
db $BE, $DE			;Rumble effect of DE magnitude
db $DE, $DE, $F3, $10		;Noop
db $15				;Player pose: face down, right hand forward
db $12				;Player pose: face right, standing
db $BE, $BE			;Rumble effect of BE magnitude
db $BE, $DE			;Rumble effect of DE magnitude
db $DE, $DE, $F3, $15		;Noop
db $19				;Player pose: face up, left hand forward
db $20				;Player pose: face down, left hand raised out
db $BF, $BF			;Sprite effect BF
db $BF, $F3			;Sprite effect F3
db $10				;Player pose: face up, left hand forward
db $17				;Player pose: face left, down hand backward
db $12				;Player pose: face right, standing
db $D6, $E6, $D6, $71		;(Map) E6 D6 71
db $F6				;Noop
db $E6, $F3			;Unknown
db $18				;Player pose: face down, left hand forward
db $17				;Player pose: face left, down hand backward
db $12				;Player pose: face right, standing
db $D6, $E6, $F6, $71		;(Map) E6 F6 71
db $F6				;Noop
db $71				;Short pause
db $F3, $18, $12, $23		;Set Map Tiles 18 12 23
db $71				;Short pause
db $D6, $D6, $71, $D6		;(Map) D6 71 D6
db $E6, $E6			;Unknown
db $F6				;Noop
db $E6, $F6			;Unknown
db $F6				;Noop
db $71				;Short pause
db $F3, $10, $11, $34		;Set Map Tiles 10 11 34
db $A1, $DA			;Run Shop DA
db $D6, $D6, $71, $71		;(Map) D6 71 71
db $D6, $E6, $E6, $F6		;(Map) E6 E6 F6
db $D6, $E6, $E6, $84		;(Map) E6 E6 84
db $85, $F6			;Sprite 085 do event: F6
db $F6				;Noop
db $93, $94			;Sprite 193 do event: 94
db $95, $14			;Sprite 195 do event: face down, left hand forward
db $C3, $0C			;Fade in Speed 0C
db $73				;Long pause
db $FF				;End Event

;padbyte $00
;pad 