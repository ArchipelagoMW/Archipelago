hirom


org $C9860D

db $CD, $B6, $04                ;Run event index 04B6
db $CD, $B7, $04                ;Run event index 04B7
db $84, $09                     ;Sprite 084 do event: Show
db $84, $03                     ;Sprite 084 do event: Move Down
db $84, $02                     ;Sprite 084 do event: Move Right
db $84, $02                     ;Sprite 084 do event: Move Right
db $84, $07                     ;Sprite 084 do event: 07
db $84, $08                     ;Sprite 084 do event: 08
db $80, $07                     ;Sprite 080 do event: 07
db $80, $08                     ;Sprite 080 do event: 08
db $CF, $03, $02                ;Play next 02 bytes simultaneously 03 times
db $84, $03                     ;Sprite 084 do event: Move Down
db $80, $5B                     ;Sprite 080 do event: 5B
db $81, $5B                     ;Sprite 081 do event: 5B
db $80, $0B                     ;Sprite 080 do event: 0B
db $81, $0B                     ;Sprite 081 do event: 0B
db $80, $05                     ;Sprite 080 do event: Bounce
db $81, $05                     ;Sprite 081 do event: Bounce
db $C7, $04                     ;Play next 04 bytes simultaneously
db $80, $00                     ;Sprite 080 do event: Hold
db $81, $00                     ;Sprite 081 do event: Hold
db $81, $20                     ;Sprite 081 do event: face down, left hand raised out
db $80, $02                     ;Sprite 080 do event: Move Right
db $80, $20                     ;Sprite 080 do event: face down, left hand raised out
db $81, $0B                     ;Sprite 081 do event: 0B
db $80, $0B                     ;Sprite 080 do event: 0B
db $84, $06                     ;Sprite 084 do event: Bounce
db $84, $03                     ;Sprite 084 do event: Move Down
db $81, $22                     ;Sprite 081 do event: face down, left hand on head
db $80, $26                     ;Sprite 080 do event: face up, right hand raised out
db $80, $07                     ;Sprite 080 do event: 07
db $80, $08                     ;Sprite 080 do event: 08
db $84, $0A                     ;Sprite 084 do event: Hide
db $BD, $12, $FF                ;Start Event Battle 12
db $C5, $80
db $B5, $02
db $71
db $DE, $6D ; custom reward
db $DF
db $80, $04                     ;Sprite 080 do event: Move Left
db $80, $24                     ;Sprite 080 do event: face down, right hand raised in
db $81, $24                     ;Sprite 081 do event: face down, right hand raised in
db $A3, $BA                     ;Clear Event Flag 0BA
db $A2, $53                     ;Set Event Flag 053
db $CC, $2B                  ;Custom destination flag
db $FF                          ;End Event

padbyte $00
pad $C98669