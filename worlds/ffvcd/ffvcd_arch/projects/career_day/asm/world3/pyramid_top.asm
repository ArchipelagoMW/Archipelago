hirom


; $C9B0CA → $C9B2A8

org $C9B0CA

db $01                          ;Player Move Up
db $72                          ;Medium pause
db $26                          ;Player pose: face up, right hand raised out
db $72                          ;Medium pause
db $82, $0A                     ;Sprite 082 do event: Hide
db $01                          ;Player Move Up
db $B4, $24                     ;Play Background Music The Book of Sealings
db $73                          ;Long pause
db $14                          ;Player pose: face down, left hand forward
db $D0, $81, $40                ;(Music) 81 40
db $DE, $41
db $DF
db $73
db $BD, $2B, $FF                ;Start Event Battle 2B
db $71
db $C5, $80
db $B5, $02
db $71
db $DE, $7A ; custom reward
db $DF
db $73
; db $C5                          ;<unknown>
; db $E0, $75                     ;Unknown
db $E3, $7A, $01, $A0, $14, $00 ;Inter-map cutscene? 7A 01 A0 14 00
db $0A                          ;Player Hide
db $D8, $47, $90, $87           ;Unknown
db $09                          ;Player Show
db $74
db $C3, $02
db $CE, $07, $01                ;Play next 01 bytes 07 times
db $04                          ;Player move Left
db $12                          ;Player pose: face right, standing
db $87, $0A                     ;Sprite 087 do event: Hide
db $09                          ;Player Show
db $72                          ;Medium pause
db $03                          ;Player Move Down
db $A5, $FE                     ;Clear Event Flag 1FE
db $A4, $F3                     ;Turn on bit 08 at address 0x7e0a52
db $CB, $08, $00                ;Turn off bit 01 at address  0x7e0a55
; db $A2, $83                     ;Turn on bit 08 at address 0x7e0a24
db $A2, $78			; new custom flag for pyramid tablet
db $CC, $27                  ;Custom destination flag 27
db $FF                          ;End Event

padbyte $00
pad $C9B2A8