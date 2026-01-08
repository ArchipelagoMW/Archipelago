hirom

; Talk with Guido

org $C8DA2B


db $01                          ;Player Move Up
db $01                          ;Player Move Up
db $01                          ;Player Move Up
db $01                          ;Player Move Up
db $01                          ;Player Move Up
db $01                          ;Player Move Up
db $01                          ;Player Move Up
db $92, $01                     ;Sprite 192 do event: Move Up
db $92, $01                     ;Sprite 192 do event: Move Up
db $CD, $81, $04                ;Run event index 0481
db $92, $24                     ;Sprite 192 do event: face down, right hand raised in
db $71                          ;Short pause
db $01                          ;Player Move Up
db $26                          ;Player pose: face up, right hand raised out
db $73                          ;Long pause
db $10                          ;Player pose: face up, left hand forward
db $71                          ;Short pause
db $16                          ;Player pose: face left, standing
db $74                          ;Very long pause
db $03                          ;Player Move Down
db $2E                          ;Player pose: face down, head lowered
db $71                          ;Short pause
db $20                          ;Player pose: face down, left hand raised out
db $D8, $06, $0F, $B4           ;Unknown
db $29                          ;Player pose: face up, right hand raised in
db $C8, $A8, $05                ;Display Message/Text/Dialogue A8 05

db $E4, $C9                     ;Unknown
db $48                          ;Player pose: garbage
db $0F                          ;<Unknown>
db $71                          ;Short pause
db $86, $0A                     ;Sprite 086 do event: Hide
db $DB                          ;Restore Player status
; db $A2, $71                     ;Set Event Flag 071
db $CC, $22                  ;Custom destination flag 22
db $FF                          ;End Event


padbyte $00
pad $C8DB7C