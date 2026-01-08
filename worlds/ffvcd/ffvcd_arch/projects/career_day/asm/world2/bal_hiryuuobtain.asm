hirom


org $C95C60

db $E3, $09, $01, $A4, $11, $00 ;Inter-map cutscene? 09 01 A4 11 00
db $80, $0C                     ;Sprite 080 do event: 0C
db $80, $0B                     ;Sprite 080 do event: 0B
db $80, $2F                     ;Sprite 080 do event: face up, head lowered
db $76							; Wait
db $C3, $0a					   ; Fade in
db $03                          ;Player Move Down
db $03                          ;Player Move Down
db $03                          ;Player Move Down
db $03                          ;Player Move Down
db $03                          ;Player Move Down
db $17
db $71
db $CD, $B6, $01                ;Run event index 01B6
db $71
db $05                          ;Player Bounce in Place
db $04                          ;Player move Left
db $71
db $01
db $14
db $72
db $C4, $03					   ; Fade out
db $E3, $01, $20, $55, $B0, $6C ;Inter-map cutscene? 01 20 55 B0 6C
db $09                          ;Player Show
db $14                          ;Player pose: face down, left hand forward
db $A2, $68                     ;Set Event Flag 068
db $CB, $73, $02                ;Clear Flag 2/3/4/5/73 02
db $CB, $7C, $02                ;Clear Flag 2/3/4/5/7C 02
db $CB, $6A, $02                ;Clear Flag 2/3/4/5/6A 02
db $CB, $6C, $02                ;Clear Flag 2/3/4/5/6C 02

db $A2, $6A 						; Set event flag for playing Surgate cutscene 
db $CC, $1D                  ;Custom destination flag 1D
db $C3, $03					   ; Fade out	
db $74							; Wait
db $DB                          ;Restore Player status
db $FF                          ;End Event

padbyte $00
pad $C95EF5