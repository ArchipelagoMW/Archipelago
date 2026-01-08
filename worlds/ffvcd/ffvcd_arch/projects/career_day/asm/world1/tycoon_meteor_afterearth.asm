hirom


org $C98327

db $73
db $C4, $0A                     ;Fade in Speed 0A
db $E3, $7A, $00, $A7, $10, $00 ;Inter-map cutscene? 7A 00 A7 10 00
db $F3, $27, $0F, $10           ;Set Map Tiles 27 0F 10
db $04                          ;Player move Left
db $14                          ;Player pose: face down, left hand forward
db $DB                          ;Restore Player status
db $C3, $0A                     ;Fade in Speed 0A
db $03                          ;Player Move Down
db $03                          ;Player Move Down
db $10                          ;Player pose: face up, left hand forward
db $CD, $B7, $04                ;Run event index 04B7
db $CD, $B8, $04                ;Run event index 04B8
db $CB, $33, $01                ;Clear Flag 2/3/4/5/33 01
db $CB, $34, $01                ;Clear Flag 2/3/4/5/34 01
db $CB, $F8, $00                ;Clear Flag 2/3/4/5/F8 00
db $CB, $01, $02                ;Clear Flag 2/3/4/5/01 02
db $CB, $2D, $00                ;Clear Flag 2/3/4/5/2D 00
db $CC, $29                  ;Custom destination flag
db $A2, $4F                     ;Set Event Flag 04F
db $FF                          ;End Event

padbyte $00
pad $C9842C

org $C98559
db $80, $07                     ;Sprite 080 do event: 07
db $80, $08                     ;Sprite 080 do event: 08
db $80, $5A                     ;Sprite 080 do event: 5A
db $81, $5A                     ;Sprite 081 do event: 5A
db $80, $0B                     ;Sprite 080 do event: 0B
db $81, $0B                     ;Sprite 081 do event: 0B
db $CE, $02, $08                ;Play next 08 bytes 02 times
db $81, $05                     ;Sprite 081 do event: Bounce
db $81, $00                     ;Sprite 081 do event: Hold
db $80, $05                     ;Sprite 080 do event: Bounce
db $80, $00                     ;Sprite 080 do event: Hold
db $81, $0B                     ;Sprite 081 do event: 0B
db $80, $0B                     ;Sprite 080 do event: 0B
db $CF, $02, $04                ;Play next 04 bytes simultaneously 02 times
db $81, $04                     ;Sprite 081 do event: Move Left
db $80, $04                     ;Sprite 080 do event: Move Left
db $16                          ;Player pose: face left, standing
db $81, $05                     ;Sprite 081 do event: Bounce
db $C7, $04                     ;Play next 04 bytes simultaneously
db $81, $03                     ;Sprite 081 do event: Move Down
db $80, $04                     ;Sprite 080 do event: Move Left
db $81, $0A                     ;Sprite 081 do event: Hide
db $80, $05                     ;Sprite 080 do event: Bounce
db $80, $03                     ;Sprite 080 do event: Move Down
db $80, $0A                     ;Sprite 080 do event: Hide
db $83, $0A                     ;Sprite 083 do event: Hide
db $82, $09                     ;Sprite 082 do event: Show
db $CE, $09, $02                ;Play next 02 bytes 09 times
db $82, $01                     ;Sprite 082 do event: Move Up
db $82, $0A                     ;Sprite 082 do event: Hide
db $FF                          ;End Event
pad $C9859B