hirom

org $C99CAA

db $B5, $60                     ;Play Sound Effect Syldra cry
db $D0, $80, $80                ;(Music) 80 80
db $96, $09                     ;Sprite 196 do event: Show
db $B1, $02                     ;Set Player Sprite 02
db $12                          ;Player pose: face right, standing
db $CE, $06, $02                ;Play next 02 bytes 06 times
db $96, $02                     ;Sprite 196 do event: Move Right
db $96, $03                     ;Sprite 196 do event: Move Down
db $96, $02                     ;Sprite 196 do event: Move Right
db $96, $02                     ;Sprite 196 do event: Move Right
db $96, $02                     ;Sprite 196 do event: Move Right
db $96, $01                     ;Sprite 196 do event: Move Up
db $CE, $06, $01                ;Play next 01 bytes 06 times
db $02                          ;Player Move Right
db $03                          ;Player Move Down
db $02                          ;Player Move Right
db $02                          ;Player Move Right
db $02                          ;Player Move Right
db $10                          ;Player pose: face up, left hand forward
db $D3, $80, $1C, $1A           ;Sprite 80 set map position 1C, 1A
; db $80, $09                     ;Sprite 080 do event: Show
; db $97, $09                     ;Sprite 197 do event: Show
; db $C7, $04                     ;Play next 04 bytes simultaneously
; db $97, $04                     ;Sprite 197 do event: Move Left
; db $80, $02                     ;Sprite 080 do event: Move Right
; db $80, $20                     ;Sprite 080 do event: face down, left hand raised out
; db $97, $20                     ;Sprite 197 do event: face down, left hand raised out
; db $CD, $2E, $05                ;Run event index 052E
; db $96, $22                     ;Sprite 196 do event: face down, left hand on head
;db $96, $24                     ;Sprite 196 do event: face down, right hand raised in
db $B4, $10                     ;Play Background Music Nostalgia
; db $97, $01                     ;Sprite 197 do event: Move Up
db $CD, $2E, $05                ;Run event index 052E
; db $96, $26                     ;Sprite 196 do event: face up, right hand raised out
; db $97, $22                     ;Sprite 197 do event: face down, left hand on head
; db $96, $20                     ;Sprite 196 do event: face down, left hand raised out
; db $97, $20                     ;Sprite 197 do event: face down, left hand raised out
; db $CD, $2E, $05                ;Run event index 052E
; db $CD, $91, $03                ;Run event index 0391
; db $CD, $2E, $05                ;Run event index 052E
; db $CD, $91, $03                ;Run event index 0391
; db $CD, $2E, $05                ;Run event index 052E
; db $CD, $2C, $05                ;Run event index 052C
; db $CD, $8F, $03                ;Run event index 038F
db $B5, $60                     ;Play Sound Effect Syldra cry
; db $CD, $2E, $05                ;Run event index 052E
; db $CD, $8F, $03                ;Run event index 038F
; db $CD, $2E, $05                ;Run event index 052E
; db $CD, $2E, $05                ;Run event index 052E
db $C5, $E0                     ;<unknown>
db $DE, $13				; set up reward
db $DF					; call text handler
; db $96, $24                     ;Sprite 196 do event: face down, right hand raised in
; db $96, $3E                     ;Sprite 196 do event: face up, both arms raised in
; db $97, $22                     ;Sprite 197 do event: face down, left hand on head
; db $80, $01                     ;Sprite 080 do event: Move Up
; db $80, $26                     ;Sprite 080 do event: face up, right hand raised out
db $D0, $80, $80                ;(Music) 80 80
db $96, $24                     ;Sprite 196 do event: face down, right hand raised in
db $2F                          ;Player pose: face up, head lowered
db $10                          ;Player pose: face up, left hand forward
db $96, $3E                     ;Sprite 196 do event: face up, both arms raised in
db $96, $24                     ;Sprite 196 do event: face down, right hand raised in
; db $C7, $06                     ;Play next 06 bytes simultaneously
; db $97, $03                     ;Sprite 197 do event: Move Down
; db $80, $03                     ;Sprite 080 do event: Move Down
db $96, $03                     ;Sprite 196 do event: Move Down
db $96, $0A                     ;Sprite 196 do event: Hide
; db $C7, $04                     ;Play next 04 bytes simultaneously
; db $97, $02                     ;Sprite 197 do event: Move Right
; db $80, $04                     ;Sprite 080 do event: Move Left
; db $80, $0A                     ;Sprite 080 do event: Hide
; db $97, $0A                     ;Sprite 197 do event: Hide
db $DB                          ;Restore Player status
db $14                          ;Player pose: face down, left hand forward
db $A4, $4F                     ;Turn on bit 80 at address 0x7e0a3d
; db $71                          ;Short pause
db $B4, $04                     ;Play Background Music Pirates Ahoy
db $FF                          ;End Event


pad $C99DAB