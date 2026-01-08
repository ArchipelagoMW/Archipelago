hirom


org $c96ef4

; Moogle first meet in forest 

db $80, $13                     ;Sprite 080 do event face right, down hand backward
db $80, $5B                     ;Sprite 080 do event 5B
db $80, $0B                     ;Sprite 080 do event 0B
db $80, $05                     ;Sprite 080 do event Bounce
db $80, $00                     ;Sprite 080 do event Hold
db $80, $05                     ;Sprite 080 do event Bounce
db $80, $00                     ;Sprite 080 do event Hold
db $80, $0B                     ;Sprite 080 do event 0B
db $80, $05                     ;Sprite 080 do event Bounce
db $80, $02                     ;Sprite 080 do event Move Right
db $80, $02                     ;Sprite 080 do event Move Right
db $80, $03                     ;Sprite 080 do event Move Down
db $12                          ;Player pose: face right, standing
db $CE, $05, $02                ;Play next 02 bytes 05 times
db $80, $02                     ;Sprite 080 do event Move Right
db $BE, $05                     ;Rumble effect of 05 magnitude
db $B5, $7E                     ;Play Sound Effect ?
db $F3, $19, $14, $01           ;Set Map Tiles 19 14 01
db $15                          ;Player pose: face down, right hand forward
db $16                          ;Player pose: face left, standing
db $BE, $00                     ;Rumble effect of 00 magnitude
db $80, $5B                     ;Sprite 080 do event 5B
db $80, $0B                     ;Sprite 080 do event 0B
db $80, $05                     ;Sprite 080 do event Bounce
db $80, $00                     ;Sprite 080 do event Hold
db $80, $0A                     ;Sprite 080 do event Hide
db $CE, $06, $01                ;Play next 01 bytes 06 times
db $02                          ;Player Move Right
db $DB                          ;Restore Player status
db $CB, $50, $02                ;Clear Flag 2/3/4/5/50 02
db $A2, $5D                     ;Set Event Flag 05D
db $FF                          ;End Event

padbyte $00
pad $C96F8A