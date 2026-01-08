hirom

; relocate event
org $C8420B
db $00, $03, $F9

; $C98FBE → $C99056

org $F90300
db $D0, $81, $80                ;(Music) 81 80
db $01                          ;Player Move Up
db $01                          ;Player Move Up
db $01                          ;Player Move Up
db $01                          ;Player Move Up
db $B1, $03                     ;Set Player Sprite 03
db $D8, $02, $00, $D8           ;Unknown
db $04                          ;Player move Left
db $00                          ;Player Hold
db $D8, $06, $00, $C7           ;Unknown
db $06                          ;Player Bounce in Place
db $86, $02                     ;Sprite 086 do event: Move Right
db $84, $02                     ;Sprite 084 do event: Move Right
db $82, $04                     ;Sprite 082 do event: Move Left
db $86, $02                     ;Sprite 086 do event: Move Right
db $86, $20                     ;Sprite 086 do event: face down, left hand raised out
db $84, $20                     ;Sprite 084 do event: face down, left hand raised out
db $82, $20                     ;Sprite 082 do event: face down, left hand raised out
db $B4, $24                     ;Play Background Music The Book of Sealings
db $82, $26                     ;Sprite 082 do event: face up, right hand raised out
db $86, $22                     ;Sprite 086 do event: face down, left hand on head
db $A4, $FE                     ;Set Event Flag 1FE
db $09                          ;Player Show
db $A5, $FE                     ;Clear Event Flag 1FE
db $B1, $03                     ;Set Player Sprite 03
db $84, $10                     ;Sprite 084 do event: face up, left hand forward
db $B9, $EB                     ;Toggle Subtracitve Tint by EB
db $B3, $0E                     ;Pause for 0E0 cycles
db $82, $20                     ;Sprite 082 do event: face down, left hand raised out
db $84, $22                     ;Sprite 084 do event: face down, left hand on head
db $86, $20                     ;Sprite 086 do event: face down, left hand raised out
db $84, $20                     ;Sprite 084 do event: face down, left hand raised out
db $10                          ;Player pose: face up, left hand forward
db $BD, $34, $FF                ;Start Event Battle 34
db $DE, $16				; set up reward
db $DF					; call text handler
db $B1, $03                     ;Set Player Sprite 03
db $B4, $11                     ;Play Background Music (Nothing)
db $B9, $EC                     ;Toggle Subtracitve Tint by EC
db $C7, $06                     ;Play next 06 bytes simultaneously
db $82, $02                     ;Sprite 082 do event: Move Right
db $84, $04                     ;Sprite 084 do event: Move Left
db $86, $04                     ;Sprite 086 do event: Move Left
db $82, $0A                     ;Sprite 082 do event: Hide
db $84, $0A                     ;Sprite 084 do event: Hide
db $86, $04                     ;Sprite 086 do event: Move Left
db $86, $0A                     ;Sprite 086 do event: Hide
db $14                          ;Player pose: face down, left hand forward
db $C5, $80
db $B5, $02
db $71
db $DE, $82 ; custom reward
db $DF
db $DB                          ;Restore Player status
db $B4, $29                     ;Play Background Music Fanfare 1 (short)
db $20                          ;Player pose: face down, left hand raised out



db $E4, $B4                     ;Unknown
db $2C                          ;Player pose: face right, right hand raised
db $A2, $D4                     ;Set Event Flag 0D4
db $FF                          ;End Event


org $C98FBE
padbyte $00
pad $C99056