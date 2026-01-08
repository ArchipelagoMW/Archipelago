hirom


org $C8D157
db $CD, $FD, $02                ;Run event index 02FD

; if you wanna move goblins around, use these three 
db $D3, $86, $14, $1A           ;Sprite 86 set map position 14, 1A
db $D3, $8F, $14, $1E           ;Sprite 8F set map position 14, 1E
db $D3, $90, $D6, $18           ;Sprite 90 set map position D6, 18

db $88, $10                     ;Sprite 088 do event: face up, left hand forward
db $89, $10                     ;Sprite 089 do event: face up, left hand forward
db $CD, $80, $04                ;Run event index 0480
db $8A, $0A                     ;Sprite 193 do event: Hide
db $94, $09                     ;Sprite 194 do event: Show
db $8F, $09                     ;Sprite 08F do event: Show
db $90, $09                     ;Sprite 190 do event: Show
db $87, $09                     ;Sprite 087 do event: Show
db $91, $09                     ;Sprite 191 do event: Show
db $92, $09                     ;Sprite 192 do event: Show
db $93, $09                     ;Sprite 193 do event: Show
; place player in reasonable spot
db $03
db $03
db $03
db $03
db $03
db $03
db $03
db $03
db $03
db $C3, $03                     ;Fade in Speed 10
db $73

db $CB, $F2, $02                ;Clear Flag 2/3/4/5/F2 02
db $CA, $F5, $02                ;Set Flag 2/3/4/5/F5 02
db $CA, $F6, $02                ;Set Flag 2/3/4/5/F6 02
db $CA, $F7, $02                ;Set Flag 2/3/4/5/F7 02
db $CA, $F8, $02                ;Set Flag 2/3/4/5/F8 02
db $CA, $F9, $02                ;Set Flag 2/3/4/5/F9 02
db $CA, $05, $03                ;Set Flag 2/3/4/5/05 03
db $CA, $06, $03                ;Set Flag 2/3/4/5/06 03
db $CA, $07, $03                ;Set Flag 2/3/4/5/07 03
db $A2, $AA                     ;Set Event Flag 0AA
db $FF                          ;End Event


padbyte $00
pad $C8D283

org $C93952

db $93, $0A                     ;Sprite 193 do event: Hide
db $BD, $29, $FF                ;Start Event Battle 29
db $CB, $F6, $02                ;Clear Flag 2/3/4/5/F6 02
db $CB, $00, $03                ;Clear Flag 2/3/4/5/00 03

db $FF                          ;End Event


padbyte $00
pad $C3A2B

; gilgamesh 3

org $C93428

db $8F, $0A                     ;Sprite 08F do event: Hide
db $91, $0A                     ;Sprite 191 do event: Hide
db $92, $0A                     ;Sprite 192 do event: Hide
db $93, $0A                     ;Sprite 193 do event: Hide
db $86, $0A                     ;Sprite 086 do event: Hide
db $BD, $1F, $FF                ;Start Event Battle 1F
db $C5, $80
db $B5, $02
db $71
db $DE, $74 ; custom reward
db $DF
db $A5, $FE                     ;Clear Event Flag 1FE
db $94, $0A                     ;Sprite 194 do event: Hide
db $87, $0A                     ;Sprite 087 do event: Hide
db $84, $0A                     ;Sprite 084 do event: Hide
db $86, $0A                     ;Sprite 086 do event: Hide
db $D3, $81, $00, $00           ;Sprite 81 set map position 00, 00
db $01
db $01
db $01
db $01
db $01
db $01
; db $A2, $6D                     ;Turn on bit 20 at address 0x7e0a21
db $A2, $AA                     ;Turn on bit 04 at address 0x7e0a29
db $CA, $01, $03                ;Turn on bit 02 at address  0x7e0ab4
db $CB, $07, $03                ;Turn off bit 80 at address  0x7e0ab4
db $CB, $06, $03                ;Turn off bit 40 at address  0x7e0ab4
db $CB, $00, $03                ;Turn off bit 01 at address  0x7e0ab4
; db $CA, $08, $03                ;Turn on bit 01 at address  0x7e0ab5
db $CB, $F5, $02                ;Turn off bit 20 at address  0x7e0ab2
db $CB, $F6, $02                ;Turn off bit 40 at address  0x7e0ab2
db $CB, $F7, $02                ;Turn off bit 80 at address  0x7e0ab2
db $CB, $F8, $02                ;Turn off bit 01 at address  0x7e0ab3
db $CB, $F9, $02                ;Turn off bit 02 at address  0x7e0ab3
db $CC, $1F                  ;Custom destination flag 1F
db $A2, $69                     ;Set Event Flag 069
db $FF                          ;End Event

padbyte $00
pad $C9356F