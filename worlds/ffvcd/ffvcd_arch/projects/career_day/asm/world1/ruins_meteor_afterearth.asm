hirom


org $C984A7

db $CD, $B6, $04                ;Run event index 04B6
db $14                          ;Player pose: face down, left hand forward
db $3F                          ;Player pose: face down, looking left, eyes lowered
db $40                          ;Player pose: face down, looking right, eyes lowered
db $14                          ;Player pose: face down, left hand forward
db $10                          ;Player pose: face up, left hand forward
db $CB, $35, $01                ;Clear Flag 2/3/4/5/35 01
db $CB, $37, $01                ;Clear Flag 2/3/4/5/37 01
db $CA, $36, $01                ;Set Flag 2/3/4/5/36 01
db $A2, $28                     ;Set Event Flag 028
db $FF                          ;End Event

padbyte $00
pad $C984C2


org $C98513
db $CA, $35, $01                ;Turn on bit 20 at address  0x7e0a7a
db $CA, $37, $01                ;Turn on bit 80 at address  0x7e0a7a
db $CD, $12, $01                ;Run event index 0112
db $FF                          ;End Event
org $C9852C

org $C9866A


db $3A                          ;Player pose: face down, surprised
db $0C                          ;<Unknown>
db $05                          ;Player Bounce in Place
db $00                          ;Player Hold
db $05                          ;Player Bounce in Place
db $00                          ;Player Hold
db $0B                          ;<Unknown>
db $03                          ;Player Move Down
db $03                          ;Player Move Down
db $C7, $04                     ;Play next 04 bytes simultaneously
db $80, $01                     ;Sprite 080 do event: Move Up
db $81, $01                     ;Sprite 081 do event: Move Up
db $70                          ;Very short pause
db $40                          ;Player pose: face down, looking right, eyes lowered
db $71                          ;Short pause
db $3F                          ;Player pose: face down, looking left, eyes lowered
db $71                          ;Short pause
db $14                          ;Player pose: face down, left hand forward
db $70                          ;Very short pause
db $C7, $04                     ;Play next 04 bytes simultaneously
db $80, $02                     ;Sprite 080 do event: Move Right
db $81, $04                     ;Sprite 081 do event: Move Left
db $80, $0A                     ;Sprite 080 do event: Hide
db $81, $0A                     ;Sprite 081 do event: Hide

db $84, $0A                     ;Sprite 084 do event: Hide
db $85, $09                     ;Sprite 085 do event: Show
db $82, $0A                     ;Sprite 082 do event: Hide
db $83, $09                     ;Sprite 083 do event: Show
db $83, $20                     ;Sprite 083 do event: face down, left hand raised out
db $85, $20                     ;Sprite 085 do event: face down, left hand raised out
db $BD, $10, $FF                ;Start Event Battle 10
db $C5, $80
db $B5, $02
db $71
db $DE, $6C ; custom reward
db $DF
db $C4, $04
db $73
db $E1, $80, $00, $90, $10, $00 ;Return from cutscene? 80 00 90 10 00
db $C3, $03                     ;Fade in Speed 10
db $03                          ;Player Move Down
db $03                          ;Player Move Down
db $D3, $80, $90, $0F           ;Sprite 80 set map position 90, 0F
db $D3, $81, $90, $0F           ;Sprite 81 set map position 90, 0F
db $80, $10                     ;Sprite 080 do event: face up, left hand forward
db $81, $10                     ;Sprite 081 do event: face up, left hand forward
db $CD, $B7, $04                ;Run event index 04B7
db $CB, $36, $01                ;Clear Flag 2/3/4/5/36 01
db $A2, $54                     ;Set Event Flag 054
db $A3, $BC                     ;Clear Event Flag 0BC
db $CC, $17                  ;Custom destination flag 17
db $FF                          ;End Event

pad $C986E7

; manually override any flag set for world map 4 meteors pointing
org $C94B88
db $00,$00, $07, $07, $07

org $C8DD65

db $2F                          ;Player pose: face up, head lowered
db $71                          ;Short pause
db $10                          ;Player pose: face up, left hand forward
db $72                          ;Medium pause
db $03                          ;Player Move Down
db $03                          ;Player Move Down
db $80, $12                     ;Sprite 080 do event: face right, standing
db $81, $12                     ;Sprite 081 do event: face right, standing
db $83, $12                     ;Sprite 083 do event: face right, standing
; db $A4, $EF                     ;Turn on bit 80 at address 0x7e0a51. Disabled for world locking
db $FF                          ;End Event

pad $C8DD84

; overwrite event after 4 meteors to only update flags, no cutscene

org $C984DF
db $CA, $F9, $00                ;Turn on bit 02 at address  0x7e0a73
db $CA, $FB, $00                ;Turn on bit 08 at address  0x7e0a73
db $FF
pad $C984F8