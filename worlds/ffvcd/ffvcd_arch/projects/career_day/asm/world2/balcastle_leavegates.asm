hirom


; Leave Castle Bal through gates
; $C8C7DF → $C8C80E is the first event called, which then branches (after saying yes to dialogue) to:

; The flag is set in bigbridge_endofbigbridge to completely bypass the Cara cutscene with Hiryuu at $C8C71D, so the guards let you leave right away upon entering Bal

org $C8C7DF

; db $B1, $01                     ;Set Player Sprite 04
; db $D3, $84, $94, $24           ;Sprite 84 set map position 94, 24
; db $D3, $85, $94, $24           ;Sprite 85 set map position 94, 24
; db $D3, $87, $94, $24           ;Sprite 87 set map position 94, 24
; db $84, $09                     ;Sprite 084 do event Show
; db $85, $09                     ;Sprite 085 do event Show
; db $87, $09                     ;Sprite 087 do event Show
; db $C7, $06                     ;Play next 06 bytes simultaneously
; db $84, $01                     ;Sprite 084 do event Move Up
; db $85, $01                     ;Sprite 085 do event Move Up
; db $87, $01                     ;Sprite 087 do event Move Up
; db $C7, $04                     ;Play next 04 bytes simultaneously
; db $85, $02                     ;Sprite 085 do event Move Right
; db $87, $04                     ;Sprite 087 do event Move Left
; db $84, $24                     ;Sprite 084 do event face down, right hand raised in
; db $85, $24                     ;Sprite 085 do event face down, right hand raised in
; db $87, $24                     ;Sprite 087 do event face down, right hand raised in
db $F0, $B7, $04              ;Conditional yes/no dialogue at 04B7
db $CD, $08, $04                ;Run event index 0408
db $FF                          ;End Event
db $CD, $09, $04                ;Run event index 0409
db $FF                          ;End Event
db $FF                          ;End Event

padbyte $00
pad $C8C80E


org $C952B7


db $A4, $00                     ;Set Event Flag 100
db $2E                          ;Player pose: face down, head lowered
db $14                          ;Player pose: face down, left hand forward
db $C7, $04                     ;Play next 04 bytes simultaneously
db $85, $04                     ;Sprite 085 do event: Move Left
db $87, $02                     ;Sprite 087 do event: Move Right
db $C7, $06                     ;Play next 06 bytes simultaneously
db $84, $03                     ;Sprite 084 do event: Move Down
db $85, $03                     ;Sprite 085 do event: Move Down
db $87, $03                     ;Sprite 087 do event: Move Down
db $84, $0A                     ;Sprite 084 do event: Hide
db $85, $0A                     ;Sprite 085 do event: Hide
db $87, $0A                     ;Sprite 087 do event: Hide
db $0C                          ;<Unknown>
db $01                          ;Player Move Up
db $0B                          ;<Unknown>
db $89, $24                     ;Sprite 089 do event: face down, right hand raised in
db $88, $02                     ;Sprite 088 do event: Move Right
db $8A, $26                     ;Sprite 08A do event: face up, right hand raised out
db $89, $0A                     ;Sprite 089 do event: Hide
db $88, $03                     ;Sprite 088 do event: Move Down
db $8A, $04                     ;Sprite 08A do event: Move Left
db $88, $0A                     ;Sprite 088 do event: Hide
db $8A, $03                     ;Sprite 08A do event: Move Down
db $8A, $0A                     ;Sprite 08A do event: Hide

db $CE, $05, $01                ;Play next 01 bytes 05 times
db $03                          ;Player Move Down
db $D3, $88, $94, $2A           ;Sprite 88 set map position 94, 2A
db $D3, $89, $94, $2A           ;Sprite 89 set map position 94, 2A
db $D3, $8A, $94, $2A           ;Sprite 8A set map position 94, 2A

db $BE, $01                     ;Rumble effect of 01 magnitude
db $B5, $66                     ;Play Sound Effect Fire beast
db $F3, $13, $2A, $12           ;Set Map Tiles 13 2A 12
db $2D                          ;Player pose: face right, right hand out
db $2E                          ;Player pose: face down, head lowered
db $2F                          ;Player pose: face up, head lowered
db $3D                          ;Player pose: face up, both arms raised out
db $3E                          ;Player pose: face up, both arms raised in
db $3F                          ;Player pose: face down, looking left, eyes lowered
db $70                          ;Short pause
db $BE, $00                     ;Rumble effect of 00 magnitude
db $70                          ;Short pause
db $89, $09                     ;Sprite 089 do event: Show
db $89, $03                     ;Sprite 089 do event: Move Down
db $8A, $09                     ;Sprite 08A do event: Show
db $C7, $04                     ;Play next 04 bytes simultaneously
db $89, $03                     ;Sprite 089 do event: Move Down
db $8A, $03                     ;Sprite 08A do event: Move Down
db $C7, $04                     ;Play next 04 bytes simultaneously
db $89, $04                     ;Sprite 089 do event: Move Left
db $8A, $03                     ;Sprite 08A do event: Move Down
db $8A, $02                     ;Sprite 08A do event: Move Right
db $70                          ;Very short pause
db $89, $22                     ;Sprite 089 do event: face down, left hand on head
db $8A, $26                     ;Sprite 08A do event: face up, right hand raised out
db $88, $09                     ;Sprite 088 do event: Show
db $CE, $03, $02                ;Play next 02 bytes 03 times
db $88, $03                     ;Sprite 088 do event: Move Down
db $88, $02                     ;Sprite 088 do event: Move Right
db $88, $26                     ;Sprite 088 do event: face up, right hand raised out
db $CE, $06, $01                ;Play next 01 bytes 06 times
db $03                          ;Player Move Down
db $70                          ;Short pause
db $10                          ;Player pose: face up, left hand forward
db $88, $04                     ;Sprite 088 do event: Move Left
db $88, $24                     ;Sprite 088 do event: face down, right hand raised in
db $89, $24                     ;Sprite 089 do event: face down, right hand raised in
db $8A, $24                     ;Sprite 08A do event: face down, right hand raised in
db $70                          ;Short pause
db $2F                          ;Player pose: face up, head lowered
db $70                          ;Very short pause
db $10                          ;Player pose: face up, left hand forward
db $89, $02                     ;Sprite 089 do event: Move Right
db $C7, $04                     ;Play next 04 bytes simultaneously
db $89, $01                     ;Sprite 089 do event: Move Up
db $8A, $04                     ;Sprite 08A do event: Move Left
db $C7, $06                     ;Play next 06 bytes simultaneously
db $89, $01                     ;Sprite 089 do event: Move Up
db $8A, $01                     ;Sprite 08A do event: Move Up
db $88, $01                     ;Sprite 088 do event: Move Up
db $89, $0A                     ;Sprite 089 do event: Hide
db $C7, $04                     ;Play next 04 bytes simultaneously
db $8A, $01                     ;Sprite 08A do event: Move Up
db $88, $01                     ;Sprite 088 do event: Move Up
db $8A, $0A                     ;Sprite 08A do event: Hide
db $88, $01                     ;Sprite 088 do event: Move Up
db $88, $0A                     ;Sprite 088 do event: Hide
db $70                          ;Short pause
db $BE, $01                     ;Rumble effect of 01 magnitude
db $B5, $66                     ;Play Sound Effect Fire beast
db $F3, $13, $2A, $12           ;Set Map Tiles 13 2A 12
db $0D                          ;<Unknown>
db $0E                          ;<Unknown>
db $0F                          ;<Unknown>
db $1D                          ;Player pose: face up, walking, right hand forward
db $1E                          ;Player pose: face right, standing
db $1F                          ;Player pose: face right, walking, right hand forward
db $70                          ;Short pause
db $BE, $00                     ;Rumble effect of 00 magnitude
db $A5, $00                     ;Clear Event Flag 100
db $14                          ;Player pose: face down, left hand forward
db $70                          ;Short pause
; db $D3, $84, $94, $2E           ;Sprite 84 set map position 94, 2E
; db $D3, $85, $94, $2E           ;Sprite 85 set map position 94, 2E
; db $D3, $87, $94, $2E           ;Sprite 87 set map position 94, 2E
; db $84, $09                     ;Sprite 084 do event: Show
; db $85, $09                     ;Sprite 085 do event: Show
; db $87, $09                     ;Sprite 087 do event: Show
; db $C7, $06                     ;Play next 06 bytes simultaneously
; db $84, $01                     ;Sprite 084 do event: Move Up
; db $85, $01                     ;Sprite 085 do event: Move Up
; db $87, $01                     ;Sprite 087 do event: Move Up
; db $C7, $04                     ;Play next 04 bytes simultaneously
; db $85, $02                     ;Sprite 085 do event: Move Right
; db $87, $04                     ;Sprite 087 do event: Move Left
; db $84, $24                     ;Sprite 084 do event: face down, right hand raised in
; db $85, $24                     ;Sprite 085 do event: face down, right hand raised in
; db $87, $24                     ;Sprite 087 do event: face down, right hand raised in
db $BE, $01                     ;Rumble effect of 01 magnitude
db $70                          ;Short pause
; db $90, $09                     ;Sprite 190 do event: Show
db $91, $09                     ;Sprite 191 do event: Show
; db $92, $09                     ;Sprite 192 do event: Show
db $CF, $06, $06                ;Play next 06 bytes simultaneously 06 times
db $90, $01                     ;Sprite 190 do event: Move Up
db $91, $01                     ;Sprite 191 do event: Move Up
db $92, $01                     ;Sprite 192 do event: Move Up
db $C7, $04                     ;Play next 04 bytes simultaneously
db $90, $01                     ;Sprite 190 do event: Move Up
db $92, $01                     ;Sprite 192 do event: Move Up
db $70                          ;Very short pause
db $BE, $00                     ;Rumble effect of 00 magnitude
db $90, $0A                     ;Sprite 190 do event: Hide
db $91, $0A                     ;Sprite 191 do event: Hide
db $92, $0A                     ;Sprite 192 do event: Hide
db $84, $0A                     ;Sprite 084 do event: Hide
db $85, $0A                     ;Sprite 085 do event: Hide
db $87, $0A                     ;Sprite 087 do event: Hide
db $BD, $1D, $FF                ;Start Event Battle 1D
db $C5, $80
db $B5, $02
db $71
db $DE, $72 ; custom reward
db $DF
db $A2, $61                     ;Set Event Flag 061
; db $CB, $6B, $02                ;Clear Flag 2/3/4/5/6B 02
db $FF



padbyte $00
pad $C953D7


; disable door locking 
; org $D8EBEF
org $F04B6F
db $fe, $66, $fb, $1d, $ff, $36, $04, $fb, $00, $ff, $50, $03


; custom text
org $E24ffC
db $72, $8D, $7A, $87, $7D, $96, $7B, $7E, $8D, $90, $7E, $7E, $87, $96, $8E, $8C, $96, $7A, $87, $7D, $96, $8D, $7A, $85, $84, $96, $8D, $88, $01
db $96, $96, $8E, $8C, $96, $8D, $88, $96, $7D, $7E, $7F, $7E, $87, $7D, $96, $8D, $81, $7E, $96, $80, $7A, $8D, $7E, $8C, $96, $7F, $8B, $88, $86, $96, $01
db $96, $96, $8D, $81, $7E, $96, $7E, $87, $7E, $86, $92, $A1, $00