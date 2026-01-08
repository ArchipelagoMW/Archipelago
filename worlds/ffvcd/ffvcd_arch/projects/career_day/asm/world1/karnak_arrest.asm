hirom


; Arrest to Cid blowing up the wall (this actually combines two events into one)
org $C87514

db $A1, $3E							;Run Shop Karnak Weapon (pre arrest)
db $CD, $63, $07					;Run event index 0763
db $75				
db $7C								;<Unknown>
db $83, $10							;Sprite 083 do event: face up, left hand forward
db $83, $03							;Sprite 083 do event: Move Down
db $83, $03							;Sprite 083 do event: Move Down
db $83, $03							;Sprite 083 do event: Move Down
db $83, $02							;Sprite 083 do event: Move Right
db $BE, $05							;Rumble effect of 05 magnitude
db $71								;Short pause
db $C5, $E0, $71						;<unknown>
db $B5, $56							;Play Sound Effect Exploder
db $CD, $73, $07					;Run event index 0773
db $F3, $12, $36, $20				;Set Map Tiles 12 36 20
db $74								;Very long pause
db $74								;Very long pause
db $51								;Player or Sprite Pose
db $74								;Very long pause
db $BE, $00							;Rumble effect of 00 magnitude
db $83, $11							;Sprite 083 do event: face up, right hand forward
db $CC, $0B         				;Custom destination flag 0B
db $FF								;End Event

padbyte $00
pad $C8753F

; armor shop


org $C87557

db $A1, $3F			;Run Shop Karnak Armor (pre arrest)
db $CD, $63, $07	;Run event index 0763
db $75
db $7C				;<Unknown>
db $83, $10			;Sprite 083 do event: face up, left hand forward
db $83, $03			;Sprite 083 do event: Move Down
db $83, $03			;Sprite 083 do event: Move Down
db $83, $03			;Sprite 083 do event: Move Down
db $83, $02			;Sprite 083 do event: Move Right
db $BE, $05			;Rumble effect of 05 magnitude
db $71				;Short pause
db $C5, $E0, $71		;<unknown>
db $B5, $56			;Play Sound Effect Exploder
db $CD, $73, $07		;Run event index 0773
db $F3, $12, $36, $20		;Set Map Tiles 12 36 20
db $74				;Very long pause
db $74				;Very long pause
db $51			;Player or Sprite Pose
db $74				;Very long pause
db $BE, $00			;Rumble effect of 00 magnitude
db $83, $11			;Sprite 083 do event: face up, right hand forward
db $CC, $0B                  ;Custom destination flag 0B
db $FF				;End Event

pad $C875A6

org $C9FB6F

db $D0, $80, $40                	;(Music) 80 40
db $C4, $03                     	;Fade out Speed 08
db $74	
db $D0, $F0, $00                	;(Music) F0 00
db $E1, $8A, $00, $94, $38, $00 	;Return from cutscene? 8A 00 94 38 00
db $D0, $F0, $00                	;(Music) F0 00
db $32                          	;Player pose: collapsed, facing left
db $C3, $03                     	;Fade in Speed 08
db $2E                          	;Player pose: face down, head lowered
db $74                          	;Extremely long pause
db $14                          	;Player pose: face down, left hand forward
db $A4, $FF                     	;Turn on bit 80 at address 0x7e0a53
db $D1, $1E, $6A, $00           	;(Timer?) 1E 6A 00
db $B4, $0F                     	;Play Background Music Deception
db $FF                          	;End Event

pad $C9FB9B