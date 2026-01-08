hirom


; First dialogue, remove text boxes
; There's a ton of events during the char switching, which was not changed

org $C99F7D

db $01                          ;Player Move Up
db $01                          ;Player Move Up
db $01                          ;Player Move Up
db $01                          ;Player Move Up
db $B1, $02                     ;Set Player Sprite 02
db $D3, $80, $2F, $0A           ;Sprite 80 set map position 2F, 0A
db $D3, $82, $2F, $0A           ;Sprite 82 set map position 2F, 0A
db $80, $09                     ;Sprite 080 do event: Show
db $81, $09                     ;Sprite 081 do event: Show
db $82, $09                     ;Sprite 082 do event: Show
db $C7, $05                     ;Play next 05 bytes simultaneously
db $01                          ;Player Move Up
db $80, $04                     ;Sprite 080 do event: Move Left
db $82, $02                     ;Sprite 082 do event: Move Right
db $14                          ;Player pose: face down, left hand forward
db $80, $20                     ;Sprite 080 do event: face down, left hand raised out
db $81, $20                     ;Sprite 081 do event: face down, left hand raised out
db $82, $20                     ;Sprite 082 do event: face down, left hand raised out
db $2E                          ;Player pose: face down, head lowered
db $14                          ;Player pose: face down, left hand forward
db $82, $3F                     ;Sprite 082 do event: face down, looking left, eyes lowered
db $80, $3F                     ;Sprite 080 do event: face down, looking left, eyes lowered
db $81, $3F                     ;Sprite 081 do event: face down, looking left, eyes lowered
db $80, $20                     ;Sprite 080 do event: face down, left hand raised out
db $81, $20                     ;Sprite 081 do event: face down, left hand raised out
db $82, $20                     ;Sprite 082 do event: face down, left hand raised out
db $C8, $2F, $07                ;Display Message/Text/Dialogue 2F 07
db $A4, $5E                     ;Set Event Flag 15E
db $A4, $60                     ;Set Event Flag 160
db $CD, $42, $07                ;Run event index 0742
db $B7, $00                     ;Add/Remove character 00
db $B7, $89                     ;Add/Remove character 89
db $B7, $8B                     ;Add/Remove character 8B
db $B7, $8C                     ;Add/Remove character 8C
db $FF                          ;End Event


padbyte $00
pad $C99FCC

org $C99F3A

; db $F3, $B1, $0E, $20, $C1      ;Set Map Tiles B1 0E 20 C1
; db $D1, $F1, $B2, $01           ;(Timer?) F1 B2 01
db $F3, $AE, $0E, $20, $C1      ;Set Map Tiles AE 0E 20 C1
db $D1, $F1, $B2, $01           ;(Timer?) F1 B2 01
db $F3, $B0, $0E, $20, $C1      ;Set Map Tiles B0 0E 20 C1
db $D1, $F1, $B2, $01           ;(Timer?) F1 B2 01
db $F3, $AF, $0E, $20, $C1      ;Set Map Tiles AF 0E 20 C1
db $D1, $F1, $B2, $01           ;(Timer?) F1 B2 01
db $CD, $74, $07                ;Run event index 0774
db $3A                          ;Player pose: face down, surprised
db $0C                          ;<Unknown>
db $05                          ;Player Bounce in Place
db $03                          ;Player Move Down
db $0B                          ;<Unknown>
db $10                          ;Player pose: face up, left hand forward
db $C8, $2F, $00                ;Display Message/Text/Dialogue 2F 07
db $FF

pad $C99F70

org $E10CE4
db $62, $7A, $8B, $7A, $96, $8B, $7E, $8A, $8E, $82, $8B, $7E, $7D, $96, $7F, $88, $8B, $96, $65, $88, $8B, $84, $96, $73, $88, $90, $7E, $8B, $A3, $01
db $72, $7E, $7E, $84, $96, $88, $8E, $8D, $96, $8D, $81, $7E, $96, $64, $85, $7D, $7E, $8B, $96, $61, $8B, $7A, $87, $7C, $81, $01
db $7A, $87, $7D, $96, $6C, $8E, $7A, $96, $65, $88, $8B, $7E, $8C, $8D, $A3, $00

