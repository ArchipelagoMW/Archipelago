hirom


; Catastroph Event

org $C9C1E0

db $71                ;Short pause
db $BE, $01            ;Rumble effect of 01 magnitude
db $B5, $8E            ;Play Sound Effect Treasure chest
db $F3, $3A, $29, $20, $07    ;Set Map Tiles 3A 29 20 07
db $17                ;Player pose: face left, down hand backward
db $01                ;Player Move Up
db $BE, $00            ;Rumble effect of 00 magnitude
db $80, $05            ;Sprite 080 do event: Bounce
db $80, $03            ;Sprite 080 do event: Move Down
db $12                ;Player pose: face right, standing
db $80, $16            ;Sprite 080 do event: face left, standing
db $80, $07            ;Sprite 080 do event: 07
db $80, $08            ;Sprite 080 do event: 08
db $80, $13            ;Sprite 080 do event: face right, down hand backward
db $77                ;<Unknown>
db $0C                ;<Unknown>
db $CF, $0F, $03        ;Play next 03 bytes simultaneously 0F times
db $04                ;Player move Left
db $80, $04            ;Sprite 080 do event: Move Left
db $CD, $82, $07        ;Run event index 0782
db $80, $0A            ;Sprite 080 do event: Hide
db $BD, $49, $FF        ;Start Event Battle 49
db $DE, $A3 ; custom reward
db $DF
db $CB, $86, $03        ;Turn off bit 40 at address  0x7e0ac4
db $A4, $72            ;Turn on bit 04 at address 0x7e0a42
db $76                ;<Unknown>
db $0B                ;<Unknown>
db $12                ;Player pose: face right, standing
db $FF                ;End Event