hirom


org $C8B64F
db $CD, $F5, $03                ;Run event index 03F5
db $D3, $82, $AC, $27           ;Sprite 82 set map position AC, 27
db $D3, $83, $AC, $27           ;Sprite 83 set map position AC, 27
db $D3, $84, $B2, $27           ;Sprite 84 set map position B2, 27
db $82, $05                     ;Sprite 082 do event: Bounce
db $82, $02                     ;Sprite 082 do event: Move Right
db $82, $05                     ;Sprite 082 do event: Bounce
db $83, $05                     ;Sprite 083 do event: Bounce
db $84, $05                     ;Sprite 084 do event: Bounce
db $CF, $02, $06                ;Play next 06 bytes simultaneously 02 times
db $82, $02                     ;Sprite 082 do event: Move Right
db $83, $02                     ;Sprite 083 do event: Move Right
db $84, $04                     ;Sprite 084 do event: Move Left
db $82, $24                     ;Sprite 082 do event: face down, right hand raised in
db $83, $24                     ;Sprite 083 do event: face down, right hand raised in
db $84, $24                     ;Sprite 084 do event: face down, right hand raised in

db $01                          ;Player Move Up
db $C7, $06                     ;Play next 06 bytes simultaneously
db $82, $03                     ;Sprite 082 do event: Move Down
db $83, $03                     ;Sprite 083 do event: Move Down
db $84, $03                     ;Sprite 084 do event: Move Down
db $CD, $F6, $03                ;Run event index 03F6
db $BD, $16, $FF                ;Start Event Battle 16
db $FF                          ;End Event

padbyte $00
pad $C8B68B
org $C9872E

; Gilgamesh at Big Bridge
; $c9872e → $C9875D


db $F3, $1E, $09, $10           ;Set Map Tiles 1E 09 10
db $04                          ;Player move Left
db $14                          ;Player pose: face down, left hand forward
db $80, $09                     ;Sprite 080 do event: Show
db $3A                          ;Player pose: face down, surprised
db $0C                          ;<Unknown>
db $06                          ;Player Bounce in Place
db $03                          ;Player Move Down
db $80, $03                     ;Sprite 080 do event: Move Down
db $0B                          ;<Unknown>
db $10                          ;Player pose: face up, left hand forward
db $80, $03                     ;Sprite 080 do event Move Down
db $80, $0A                     ;Sprite 080 do event Hide
db $BD, $1B, $FF                ;Start Event Battle 1B
db $C5, $80
db $B5, $02
db $71
db $DE, $70 ; custom reward
db $DF
db $A2, $45                     ;Set Event Flag 045
db $00                          ;Player Hold
db $FF                          ;End Event


padbyte $00
pad $C9875D