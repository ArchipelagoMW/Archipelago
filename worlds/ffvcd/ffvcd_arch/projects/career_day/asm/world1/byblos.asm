hirom



; Skip chat before byblos fight
org $C88562


db $D3, $80, $38, $37           ;Sprite 80 set map position 38, 37
db $D3, $81, $3C, $37           ;Sprite 81 set map position 3C, 37
db $B5, $84                     ;Play Sound Effect Exdeath destroyed 2
db $BE, $01                     ;Rumble effect of 01 magnitude
db $72
db $82, $22                     ;Sprite 082 do event: face down, left hand on head
db $83, $26                     ;Sprite 083 do event: face up, right hand raised out
db $84, $26                     ;Sprite 084 do event: face up, right hand raised out
db $80, $09                     ;Sprite 080 do event: Show
db $81, $09                     ;Sprite 081 do event: Show
db $80, $05                     ;Sprite 080 do event: Bounce
db $81, $05                     ;Sprite 081 do event: Bounce
db $C7, $04                     ;Play next 04 bytes simultaneously
db $80, $03                     ;Sprite 080 do event: Move Down
db $81, $03                     ;Sprite 081 do event: Move Down
db $BE, $00                     ;Rumble effect of 00 magnitude
db $C7, $04                     ;Play next 04 bytes simultaneously
db $80, $02                     ;Sprite 080 do event: Move Right
db $81, $04                     ;Sprite 081 do event: Move Left
db $80, $0A                     ;Sprite 080 do event: Hide
db $81, $0A                     ;Sprite 081 do event: Hide
db $BD, $09, $FF                ;Start Event Battle 09
db $B1, $02                     ;Set Player Sprite 02
db $DB                          ;Restore Player status
db $C5, $80
db $B5, $02
db $71                          ;Short pause
db $DE, $60
db $DF
db $A4, $2A                     ;Turn on bit 04 at address 0x7e0a39
db $FF                          ;End Event

padbyte $00
pad $C885CC