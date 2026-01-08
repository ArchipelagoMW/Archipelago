hirom


; Pre dialogue, Atomos, post

org $C8D4C9

db $D0, $81, $F0                ;(Music) 81 F0
db $CD, $09, $01                ;Run event index 0109
db $83, $0A                     ;Sprite 083 do event: Hide
db $86, $0A                     ;Sprite 086 do event: Hide
db $89, $0A                     ;Sprite 089 do event: Hide
db $8C, $0A                     ;Sprite 08C do event: Hide
db $8F, $0A                     ;Sprite 08F do event: Hide
db $CD, $09, $01                ;Run event index 0109
db $82, $0A                     ;Sprite 082 do event: Hide
db $85, $0A                     ;Sprite 085 do event: Hide
db $88, $0A                     ;Sprite 088 do event: Hide
db $8B, $0A                     ;Sprite 08B do event: Hide
db $8E, $0A                     ;Sprite 08E do event: Hide
db $CD, $09, $01                ;Run event index 0109
db $BD, $20, $FF          ;Start Event Battle 20
db $C5, $80
db $B5, $02
db $71
db $DE, $75 ; custom reward
db $DF
db $C4, $02                     ;Fade out
db $75
db $75
; db $A4, $EA                     ;Turn on bit 04 at address 0x7e0a51. This sets the tile on the world map to inactive 
db $A2, $77                     ;Turn on bit 80 at address 0x7e0a22
; db $A4, $EB                     ;Turn on bit 08 at address 0x7e0a51
; db $D2, $01, $CE, $C8, $6C      ;(Map) 01 AD 9F 6C
; db $CA, $DB, $02                ;Turn on bit 08 at address  0x7e0aaf
db $CA, $DC, $02                ;Turn on bit 10 at address  0x7e0aaf
db $CA, $DD, $02                ;Turn on bit 20 at address  0x7e0aaf
db $CA, $DE, $02                ;Turn on bit 40 at address  0x7e0aaf
db $CA, $DF, $02                ;Turn on bit 80 at address  0x7e0aaf
db $CB, $E3, $02                ;Turn off bit 08 at address  0x7e0ab0
db $CB, $E4, $02                ;Turn off bit 10 at address  0x7e0ab0
db $CB, $E5, $02                ;Turn off bit 20 at address  0x7e0ab0
db $CB, $11, $03                ;Turn off bit 02 at address  0x7e0ab6
db $CB, $0E, $00                ;Turn off bit 40 at address  0x7e0a55

; CAREER DAY
; Disable submarine bit flags
db $A3, $C1            ; set address 000A2C bit OFF 02
db $A3, $C0            ; set address 000A2C bit OFF 01

; below skips sub cutscene with Galuf waiting. No timer is ever set, Galuf never removed from party

db $A5, $FE                     ;Turn off bit 40 at address 0x7e0a53
db $E1, $03, $20, $A9, $A5, $91 ;Return from cutscene? 03 20 A9 A5 91
db $DB                          ;Restore Player status
db $C3, $02                     ;Fade in Speed 02
db $73                          ;Long pause
db $CA, $0E, $00                ;Turn on bit 40 at address  0x7e0a55
db $A3, $C1                     ;Turn off bit 02 at address 0x7e0a2c
db $CC                          ;Noop
db $21                          ;Player pose: face down, left hand raised in
db $FF                          ;End Event

padbyte $00
pad $C8D9AA