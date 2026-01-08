hirom


; disable aspis
org $C9B04D

;db $80, $05                     ;Sprite 080 do event: Bounce
;db $80, $03                     ;Sprite 080 do event: Move Down
;db $D3, $80, $00, $00           ;Sprite 80 set map position 00, 00
db $80, $0A                     ;Sprite 081 do event: Show
db $81, $0A                     ;Sprite 081 do event: Show
db $82, $0A                     ;Sprite 082 do event: Show
;db $81, $0C                     ;Sprite 081 do event: 0C
;db $82, $0C                     ;Sprite 082 do event: 0C
db $A4, $F1                     ;Turn on bit 02 at address 0x7e0a52
db $FF                          ;End Event

pad $C9B05F


; disable npcs for machinehead/mummy

org $CE93A7

pad $CE941E


; disable timer events

org $C8EC83
db $01                          ;Player Move Up
db $A4, $F1                     ;Turn on bit 02 at address 0x7e0a52
db $FF                          ;End Event
pad $C8EC8A
org $C8EC8B
db $A4, $F1                     ;Turn on bit 02 at address 0x7e0a52
db $FF                          ;End Event