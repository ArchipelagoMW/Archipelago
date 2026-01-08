hirom


; Zeza talk in sub to get into tower

org $C93F24

db $84, $24                     ;Sprite 084 do event: face down, right hand raised in
db $E0, $03                     ;Unknown
db $20                          ;Player pose: face down, left hand raised out
db $B3, $A3, $91
db $03                          ;Player Move Down
db $03                          ;Player Move Down
db $03                          ;Player Move Down
db $04                          ;Player move Left
db $04                          ;Player move Left
db $E3, $57, $01, $8D, $0F, $00 ;Inter-map cutscene? 57 01 8D 0F 00
db $40                          ;Player pose: face down, looking right, eyes lowered
db $3F                          ;Player pose: face down, looking left, eyes lowered
db $14                          ;Player pose: face down, left hand forward

db $CD, $D9, $03                ;Run event index 03D9
db $CC, $20                  ;Custom destination flag 20
db $FF                          ;End Event


padbyte $00
pad $C93F49


org $C94CAE

db $C3, $0a					  ; Fade in
db $84, $10                     ;Sprite 084 do event: face up, left hand forward
db $84, $02                     ;Sprite 084 do event: Move Right
db $84, $01                     ;Sprite 084 do event: Move Up
db $84, $01                     ;Sprite 084 do event: Move Up
db $84, $04                     ;Sprite 084 do event: Move Left
db $84, $01                     ;Sprite 084 do event: Move Up
db $10                          ;Player pose: face up, left hand forward
db $84, $24                     ;Sprite 084 do event: face down, right hand raised in
db $84, $58                     ;Sprite 084 do event: 58
db $84, $20                     ;Sprite 084 do event: face down, left hand raised out
db $B5, $8E                     ;Play Sound Effect Treasure chest
db $F3, $0D, $0B, $10           ;Set Map Tiles 0D 0B 10
db $04                          ;Player move Left
db $14                          ;Player pose: face down, left hand forward
db $85, $0A                     ;Sprite 085 do event: Hide
db $84, $01                     ;Sprite 084 do event: Move Up
db $84, $0A                     ;Sprite 084 do event: Hide
db $B5, $8E                     ;Play Sound Effect Treasure chest
db $F3, $0D, $0B, $10           ;Set Map Tiles 0D 0B 10
db $03                          ;Player Move Down
db $13                          ;Player pose: face right, down hand backward
db $A2, $6E                     ;Set Event Flag 06E. This sets Zeza's bombing cutscene immediately
db $CB, $D8, $00                ;Clear Flag 2/3/4/5/D8 00
db $CB, $DA, $00                ;Clear Flag 2/3/4/5/DA 00
db $CB, $DB, $00                ;Clear Flag 2/3/4/5/DB 00
db $FF                          ;End Event


padbyte $00
pad $C94CFA