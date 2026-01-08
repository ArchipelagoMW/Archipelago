hirom

org $C913A2

db $B5, $3A                     ;Play Sound Effect Quick
db $F3, $08, $32, $00, $6E, $80 ;Set Map Tiles 08 32 00 6E 80
db $09                          ;Player Show
db $0A                          ;Player Hide
db $BE, $04                     ;Rumble effect of 04 magnitude
db $72                          ;Medium pause
db $B5, $88                     ;Play Sound Effect Titan steps
db $C4, $05                     ;Fade out Speed 0C
db $72                          ;Long pause
db $CD, $BC, $01                ;Run event index 01BC
db $80, $0A                     ;Sprite 080 do event: Hide
db $CD, $BF, $01                ;Run event index 01BF
db $80, $0A                     ;Sprite 080 do event: Hide
db $D3, $80, $C9, $32           ;Sprite 80 set map position C9, 32
db $80, $09                     ;Sprite 080 do event: Show
db $BE, $00                     ;Rumble effect of 00 magnitude
db $09                          ;Player Show
db $80, $0A                     ;Sprite 080 do event: Hide
db $C3, $05                     ;Fade in Speed 0C
db $72                          ;Long pause
db $FF                          ;End Event

pad $C9140C

org $C9140D

db $B5, $3A                     ;Play Sound Effect Quick
db $F3, $08, $32, $00, $6F, $80 ;Set Map Tiles 08 32 00 6F 80
db $09                          ;Player Show
db $0A                          ;Player Hide
db $BE, $04                     ;Rumble effect of 04 magnitude
db $72                          ;Medium pause
db $B5, $88                     ;Play Sound Effect Titan steps
db $C4, $05                     ;Fade out Speed 0C
db $72                          ;Long pause
db $CD, $C2, $01                ;Run event index 01C2
db $80, $09                     ;Sprite 080 do event: Show
db $CD, $BF, $01                ;Run event index 01BF
db $80, $0A                     ;Sprite 080 do event: Hide
db $D3, $80, $C9, $32           ;Sprite 80 set map position C9, 32
db $80, $09                     ;Sprite 080 do event: Show
db $BE, $00                     ;Rumble effect of 00 magnitude
db $09                          ;Player Show
db $80, $0A                     ;Sprite 080 do event: Hide
db $C3, $05                     ;Fade in Speed 0C
db $72                          ;Long pause
db $FF                          ;End Event

pad $C91475