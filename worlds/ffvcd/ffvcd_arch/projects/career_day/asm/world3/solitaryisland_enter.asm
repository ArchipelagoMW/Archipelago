hirom


; $C9A2D3 → $
; Solitary Island - cutscene at beginning after Gargoyles. 2 small cutscenes

org $C9A2D3

db $BE, $05                     ;Rumble effect of 05 magnitude
db $B5, $43                     ;Play Sound Effect Gate opens
db $00
db $F3, $14, $37, $12           ;Set Map Tiles 14 37 12
db $08                          ;<Unknown>
db $09                          ;Player Show
db $0A                          ;Player Hide
db $18                          ;Player pose: face down, left hand forward
db $19                          ;Player pose: face up, left hand forward
db $1A                          ;Player pose: face left, standing
db $00
db $BE, $00                     ;Rumble effect of 00 magnitude
db $A4, $00                     ;Set Event Flag 100
db $FF                          ;End Event


db $CD, $8B, $00                ;Run event index 008B
db $CD, $8C, $00                ;Run event index 008C
; db $C8, $4F, $87                ;Display Message/Text/Dialogue 4F 87
db $CD, $BA, $00                ;Run event index 00BA
db $CD, $6E, $05                ;Run event index 056E
db $CD, $3F, $03                ;Run event index 033F
db $A4, $5F                     ;Set Event Flag 15F
db $A4, $00                     ;Set Event Flag 100
db $FF                          ;End Event


padbyte $00
pad $C9A2FE

org $C9C417
db $63, $00