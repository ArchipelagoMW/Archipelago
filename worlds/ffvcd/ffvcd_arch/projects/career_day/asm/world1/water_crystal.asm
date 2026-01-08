hirom


; Walse Meteor Event
org $C870C9

db $D0, $81, $20                ;(Music) 81 20
db $01                          ;Player Move Up
db $F3, $08, $02, $10, $8C, $9C ;Set Map Tiles 08 02 10 8C 9C
db $B4, $0F                     ;Play Background Music Deception
db $80, $09                     ;Sprite 080 do event: Show
db $0A                          ;Player Hide
db $01                          ;Player Move Up
db $01                          ;Player Move Up
db $01                          ;Player Move Up
db $8F, $09                     ;Sprite 08F do event: Show
db $8F, $0A                     ;Sprite 08F do event: Hide
db $84, $10                     ;Sprite 084 do event: face up, left hand forward
db $85, $10                     ;Sprite 085 do event: face up, left hand forward
db $85, $5A                     ;Sprite 085 do event: 5A
db $D8, $86, $E0, $85           ;Unknown
db $5B                  ;Player or Sprite Pose
db $85, $0B                     ;Sprite 085 do event: 0B
db $B5, $59                     ;Play Sound Effect Specialty (monster)
db $85, $06                     ;Sprite 085 do event: Bounce
db $C7, $04                     ;Play next 04 bytes simultaneously
db $84, $01                     ;Sprite 084 do event: Move Up
db $85, $04                     ;Sprite 085 do event: Move Left
db $85, $0B                     ;Sprite 085 do event: 0B
db $86, $09                     ;Sprite 086 do event: Show
db $85, $0A                     ;Sprite 085 do event: Hide
db $84, $24                     ;Sprite 084 do event: face down, right hand raised in
db $84, $03                     ;Sprite 084 do event: Move Down
db $84, $03                     ;Sprite 084 do event: Move Down
db $84, $0A                     ;Sprite 084 do event: Hide

db $D8, $86, $04
db $BD, $06, $FF                ;Start Event Battle 06

db $C5, $80
db $B5, $02
db $71
db $DE, $65 ; custom reward
db $DF


db $B4, $0F                     ;Play Background Music Deception
db $80, $01                     ;Sprite 080 do event: Move Up
db $80, $01                     ;Sprite 080 do event: Move Up
db $80, $01                     ;Sprite 080 do event: Move Up
db $01                          ;Player Move Up
db $01                          ;Player Move Up
db $C7, $06                     ;Play next 06 bytes simultaneously
db $81, $01                     ;Sprite 081 do event: Move Up
db $82, $04                     ;Sprite 082 do event: Move Left
db $83, $02                     ;Sprite 083 do event: Move Right
db $82, $20                     ;Sprite 082 do event: face down, left hand raised out
db $83, $20                     ;Sprite 083 do event: face down, left hand raised out
db $CD, $66, $03                ;Run event index 0366
db $CD, $66, $03                ;Run event index 0366
db $CD, $1F, $02                ;Run event index 021F
db $C5, $E0                     ;<unknown>
db $D8, $10, $0C, $D8           ;Unknown
db $11                          ;Player pose: face up, right hand forward
db $FD                          ;Noop
db $D8, $12, $0E, $D8           ;Unknown
db $13                          ;Player pose: face right, down hand backward
db $1D                          ;Player pose: face up, walking, right hand forward
db $C7, $08                     ;Play next 08 bytes simultaneously
db $90, $04                     ;Sprite 190 do event: Move Left
db $91, $03                     ;Sprite 191 do event: Move Down
db $92, $02                     ;Sprite 192 do event: Move Right
db $93, $01                     ;Sprite 193 do event: Move Up
db $C7, $08                     ;Play next 08 bytes simultaneously
db $90, $03                     ;Sprite 190 do event: Move Down
db $91, $02                     ;Sprite 191 do event: Move Right
db $92, $01                     ;Sprite 192 do event: Move Up
db $93, $04                     ;Sprite 193 do event: Move Left
db $C5, $E0                     ;<unknown>
db $CD, $66, $03                ;Run event index 0366
db $CD, $66, $03                ;Run event index 0366
db $CE, $04, $03                ;Play next 03 bytes 04 times
db $CD, $66, $03                ;Run event index 0366
db $C7, $08                     ;Play next 08 bytes simultaneously
db $90, $02                     ;Sprite 190 do event: Move Right
db $91, $01                     ;Sprite 191 do event: Move Up
db $92, $04                     ;Sprite 192 do event: Move Left
db $93, $03                     ;Sprite 193 do event: Move Down
db $D3, $90, $30, $30           ;Sprite 90 set map position 30, 30
db $D3, $91, $30, $30           ;Sprite 91 set map position 30, 30
db $D3, $92, $30, $30           ;Sprite 92 set map position 30, 30
db $D3, $93, $30, $30           ;Sprite 93 set map position 30, 30
db $B9, $67                     ;Toggle Subtracitve Tint by 67
db $01                          ;Player Move Up
db $01                          ;Player Move Up
db $87, $0A                     ;Sprite 087 do event: Hide
db $88, $0A                     ;Sprite 088 do event: Hide
db $B2, $01                     ;Pause for 01 cycles
db $C1, $02                     ;<Unknown>
db $D9, $0A, $04, $B5           ;Unknown
db $81, $BF                     ;Sprite 081 do event: BF
db $02                          ;Player Move Right
db $B9, $78                     ;Toggle Subtracitve Tint by 78
db $C1, $00                     ;<Unknown>
db $B1, $02                     ;Set Player Sprite 02
db $CD, $8D, $03                ;Run event index 038D
db $B4, $08                     ;Play Background Music The Prelude
db $03                          ;Player Move Down
db $03                          ;Player Move Down
db $03                          ;Player Move Down
db $03                          ;Player Move Down
; db $85, $54                     ;Sprite 085 do event: 54
; db $D3, $86, $00, $00           ;Sprite 86 set map position 00, 00
; db $85, $09                     ;Sprite 085 do event: Show
; db $85, $11                     ;Sprite 085 do event: face up, right hand forward
; db $81, $26                     ;Sprite 081 do event: face up, right hand raised out
; db $80, $26                     ;Sprite 080 do event: face up, right hand raised out
; db $83, $26                     ;Sprite 083 do event: face up, right hand raised out
; db $82, $26                     ;Sprite 082 do event: face up, right hand raised out
; db $CE, $03, $02                ;Play next 02 bytes 03 times
; db $85, $11                     ;Sprite 080 do event face right, down hand backward
; db $85, $03                     ;Sprite 085 do event: Move Down
; db $81, $24                     ;Sprite 081 do event: face down, right hand raised in
; db $80, $24                     ;Sprite 080 do event: face down, right hand raised in
; db $83, $24                     ;Sprite 083 do event: face down, right hand raised in
; db $82, $24                     ;Sprite 082 do event: face down, right hand raised in
; db $85, $02                     ;Sprite 085 do event: Move Right
; db $85, $02                     ;Sprite 085 do event: Move Right
; db $85, $03                     ;Sprite 085 do event: Move Down

db $85, $0A                          
db $09                          ;Player Show
db $80, $0A                     ;Sprite 080 do event: Hide
db $DB                          ;Restore Player status
db $D3, $92, $00, $00           ;Sprite 92 set map position 00, 00
db $D3, $90, $00, $00           ;Sprite 90 set map position 00, 00
db $14                          ;Player pose: face down, left hand forward
db $CA, $E1, $00                ;Turn on bit 02 at address  0x7e0a70
db $CB, $DF, $00                ;Turn off bit 80 at address  0x7e0a6f
db $CB, $E0, $00                ;Turn off bit 01 at address  0x7e0a70
db $CB, $E7, $00                ;Turn off bit 80 at address  0x7e0a70
db $CB, $E8, $00                ;Turn off bit 01 at address  0x7e0a71
db $A2, $27                     ;Turn on bit 80 at address 0x7e0a18
db $A4, $DD                     ;Turn on bit 20 at address 0x7e0a4f
db $FF						;End event

padbyte $00
pad $C87299