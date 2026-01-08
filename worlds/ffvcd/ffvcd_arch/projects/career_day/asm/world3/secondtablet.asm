hirom


; $C9A4AD → $C9A5B1
; Before fight, then after fight, show fork tower fast (gives player direction)

org $C9A4AD


db $B5, $93                     ;Play Sound Effect Evil appears
db $CE, $08, $08                ;Play next 08 bytes 14 times
db $86, $0A                     ;Sprite 086 do event: Hide
db $B2, $04                     ;Pause for 04 cycles
db $86, $09                     ;Sprite 086 do event: Show
db $B2, $04                     ;Pause for 04 cycles
db $86, $16                     ;Sprite 086 do event: face left, standing
db $14                          ;Player pose: face down, left hand forward
db $86, $01                     ;Sprite 086 do event: Move Up
db $86, $01                     ;Sprite 086 do event: Move Up
db $86, $01                     ;Sprite 086 do event: Move Up
db $86, $0A                     ;Sprite 086 do event: Hide
db $BD, $2E, $FF                ;Start Event Battle 2E
db $C5, $80
db $B5, $02
db $71
db $DE, $80 ; custom reward
db $DF
db $10                          ;Player pose: face up, left hand forward
db $71                          ;Short pause
db $82, $03                     ;Sprite 082 do event: Move Down
db $82, $0A                     ;Sprite 082 do event: Hide
db $12                          ;Player pose: face right, standing
db $B2, $03                     ;Pause for 03 cycles
db $14                          ;Player pose: face down, left hand forward
db $39                          ;Player pose: face down, both arms raised
db $B4, $29                     ;Play Background Music Fanfare 1 (short)
; db $C8, $50, $07                ;Display Message/Text/Dialogue 50 07
db $E4, $C4                     ;Unknown
db $06                          ;Player Bounce in Place
db $73                          ;Long pause
db $0A
db $E1, $02, $00, $CE, $C9, $00 ;Return from cutscene? 02 00 CE C9 00
db $D0, $80, $00                ;(Music) 80 00
db $B4, $11                     ;Play Background Music (Nothing)
db $A4, $FE                     ;Set Event Flag 1FE
db $0A                          ;Player Hide
db $C3, $08                     ;Fade in Speed 08
db $75                          ;Extremely long pause
db $E3, $89, $01, $2F, $10, $00 ;Inter-map cutscene? 89 01 2F 10 00
db $F3, $AD, $0E, $20           ;Set Map Tiles AD 0E 20
db $F3, $AD, $0E, $24           ;Set Map Tiles AD 0E 24
db $CB, $43, $02                ;Clear Flag 2/3/4/5/43 02
db $E1, $88, $01, $8F, $05, $00 ;Return from cutscene? 88 01 8F 05 00
db $09                          ;Player Show
db $B1, $02                     ;Set Player Sprite 02
db $14                          ;Player pose: face down, left hand forward
db $D3, $82, $0F, $06           ;Sprite 82 set map position 0F, 06
db $03                          ;Player Move Down
db $03                          ;Player Move Down
db $C3, $04                     ;Fade in Speed 08
db $73                          ;Extremely long pause
db $14                          ;Player pose: face down, left hand forward
db $DB                          ;Restore Player status
db $B4, $24                     ;Play Background Music The Book of Sealings
db $A5, $FE                     ;Clear Event Flag 1FE
; db $A2, $8E                     ;Turn on bit 40 at address 0x7e0a25
db $A4, $53                     ;Turn on bit 08 at address 0x7e0a3e
db $CB, $43, $02                ;Turn off bit 08 at address  0x7e0a9c
db $CB, $5A, $02                ;Turn off bit 04 at address  0x7e0a9f
db $FF                          ;End Event



padbyte $00
pad $C9A5B1