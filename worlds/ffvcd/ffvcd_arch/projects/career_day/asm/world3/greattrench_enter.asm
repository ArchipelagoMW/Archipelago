hirom


; Gargoyles at Great Trench

org $C9AEDC

db $88, $0A                     ;Sprite 088 do event: Hide
db $89, $0A                     ;Sprite 089 do event: Hide
db $8A, $0A                     ;Sprite 08A do event: Hide
db $8B, $0A                     ;Sprite 08B do event: Hide
db $CD, $8B, $00                ;Run event index 008B
db $CD, $8C, $00                ;Run event index 008C
db $CD, $BA, $00                ;Run event index 00BA
db $F4, $00                     ;Unknown
db $FD                          ;Noop
db $10                          ;Player pose: face up, left hand forward
db $04                          ;Player move Left
db $14                          ;Player pose: face down, left hand forward
db $CD, $3F, $03                ;Run event index 033F
db $CB, $21, $00                ;Clear Flag 2/3/4/5/21 00
db $A2, $A1                     ;Set Event Flag 0A1
db $FF                          ;End Event

padbyte $00
pad $C9AEFF

org $c9aedA
db $6A, $00