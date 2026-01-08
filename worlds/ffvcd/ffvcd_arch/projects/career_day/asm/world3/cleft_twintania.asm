hirom


; Twin Tania text box

org $C9C4D4

db $80, $03                     ;Sprite 080 do event: Move Down
db $80, $03                     ;Sprite 080 do event: Move Down
db $80, $03                     ;Sprite 080 do event: Move Down
db $BD, $4A, $FF                ;Start Event Battle 4A
db $DE, $A5 ; custom reward
db $DF
db $80, $12                     ;Sprite 080 do event: face right, standing
db $CE, $05, $02                ;Play next 02 bytes 05 times
db $80, $01                     ;Sprite 080 do event: Move Up
db $BE, $0A                     ;Rumble effect of 0A magnitude
db $B5, $36                     ;Play Sound Effect Fire3
db $CD, $73, $07                ;Run event index 0773
db $80, $0A                     ;Sprite 080 do event: Hide
db $CD, $73, $07                ;Run event index 0773
db $CD, $A1, $06                ;Run event index 06A1
db $BE, $05                     ;Rumble effect of 05 magnitude
db $BE, $00                     ;Rumble effect of 00 magnitude
db $CB, $92, $03                ;Clear Flag 2/3/4/5/92 03
db $A4, $77                     ;Set Event Flag 177
db $FF                          ;End Event


padbyte $00
pad $C9C504