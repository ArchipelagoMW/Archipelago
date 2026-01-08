hirom



org $C99537

; Gilgamesh before Exdeath cutscene

db $80, $09                     ;Sprite 080 do event: Show
db $80, $03                     ;Sprite 080 do event: Move Down
db $80, $03                     ;Sprite 080 do event: Move Down
db $80, $20                     ;Sprite 080 do event: face down, left hand raised out
db $F3, $32, $1F, $00           ;Set Map Tiles 32 1F 00
db $12                          ;Player pose: face right, standing
db $03                          ;Player Move Down
db $03                          ;Player Move Down
db $03                          ;Player Move Down
db $03                          ;Player Move Down
db $71                          ;Short pause
db $80, $26                     ;Sprite 080 do event: face up, right hand raised out
db $71                          ;Short pause
db $80, $20                     ;Sprite 080 do event: face down, left hand raised out
db $0C                          ;<Unknown>
db $80, $0B                     ;Sprite 080 do event: 0B
db $77                          ;<Unknown>
db $80, $13                     ;Sprite 080 do event: face right, down hand backward
db $04                          ;Player move Left
db $80, $06                     ;Sprite 080 do event: Bounce
db $C7, $03                     ;Play next 03 bytes simultaneously
db $04                          ;Player move Left
db $80, $04                     ;Sprite 080 do event: Move Left
db $CF, $06, $03                ;Play next 03 bytes simultaneously 06 times
db $04                          ;Player move Left
db $80, $04                     ;Sprite 080 do event: Move Left
db $0B                          ;<Unknown>
db $80, $0B                     ;Sprite 080 do event: 0B
db $CF, $02, $03                ;Play next 03 bytes simultaneously 02 times
db $03                          ;Player Move Down
db $80, $01                     ;Sprite 080 do event: Move Up
db $80, $0A                     ;Sprite 080 do event: Hide
db $BD, $23, $FF                ;Start Event Battle 23
db $C5, $80
db $B5, $02
db $71
db $DE, $78 ; custom reward
db $DF
db $76                          ;<Unknown>
db $A4, $4B                     ;Set Event Flag 14B
db $CA, $61, $02                ;Set Flag 2/3/4/5/61 02
db $FF                          ;End Event

padbyte $00
pad $C99592