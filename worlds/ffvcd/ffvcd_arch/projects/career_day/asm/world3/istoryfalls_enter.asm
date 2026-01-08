hirom


org $C9BBAE

db $CD, $8B, $00                ;Run event index 008B
db $CD, $8C, $00                ;Run event index 008C
db $00, $00, $00
db $CD, $BA, $00                ;Run event index 00BA
db $CD, $58, $06                ;Run event index 0658
db $CD, $3F, $03                ;Run event index 033F
db $A4, $6A                     ;Set Event Flag 16A
db $A4, $00                     ;Set Event Flag 100
db $FF                          ;End Event
db $BE, $06                     ;Rumble effect of 06 magnitude
db $B5, $43                     ;Play Sound Effect Gate opens
db $F3, $15, $24, $10           ;Set Map Tiles 15 24 10
db $04                          ;Player move Left
db $14                          ;Player pose: face down, left hand forward
db $BE, $00                     ;Rumble effect of 00 magnitude
db $A4, $00                     ;Set Event Flag 100
db $8C, $0A                     ;Sprite 08C do event: Hide
db $CB, $71, $03                ;Clear Flag 2/3/4/5/71 03
db $FF                          ;End Event


padbyte $00
pad $C9BBDA

org $C9C420
db $5B, $00