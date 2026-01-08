hirom


org $C89B8C

db $A4, $FE                     ;Set Event Flag 1FE
db $D3, $84, $2F, $2A           ;Sprite 84 set map position 2F, 2A
db $01                          ;Player Move Up
db $01                          ;Player Move Up
db $01                          ;Player Move Up
db $84, $24                     ;Sprite 097 do event: Move Down
db $D0, $81, $40                ;(Music) 81 40
db $70
db $C4, $03
db $75
db $A4, $DE                     ;Set Event Flag 1DE
db $E1, $00, $00, $95, $51, $00 ;Return from cutscene? 00 00 95 51 00
db $E1, $FE, $00, $2F, $2C, $00 ;Return from cutscene? FE 00 2F 2C 00

;music related...?
db $D8, $00, $00, $0A           ;Unknown
db $D8, $01, $00, $D8           ;Unknown
db $03                          ;Player Move Down
db $00                          ;Player Hold
db $D8, $02, $00, $B4           ;Unknown
db $0F                          ;<Unknown>
; end of music


db $03
db $03
db $03
db $09                          ;Player Show
db $D3, $8B, $2E, $2F           ;Sprite 8D set map position 00, 00
db $D3, $89, $30, $2F           ;Sprite 8D set map position 00, 00
db $D3, $8A, $2F, $2E           ;Sprite 8D set map position 00, 00
db $D3, $8C, $2F, $30           ;Sprite 8D set map position 00, 00
db $10
db $80, $0A                     ;Sprite 08C do event: Hide
db $81, $0A                     ;Sprite 08A do event: Hide
db $82, $0A                     ;Sprite 08B do event: Hide
db $83, $0A
db $84, $0A
db $85, $0A
db $97, $0A
db $C3, $03                    ;Fade in Speed 0A
db $73

db $DE, $0C				; set up reward
db $DF					; call text handler
db $DE, $0D				; set up reward
db $DF					; call text handler
db $DE, $0E				; set up reward
db $DF					; call text handler
db $DE, $0F				; set up reward
db $DF					; call text handler




db $C7, $08                     ;Play next 06 bytes simultaneously
db $89, $04                     ;Sprite 08B do event: Move Left
db $8A, $03                     ;Sprite 08B do event: Move Left
db $8B, $02                     ;Sprite 08B do event: Move Left
db $8C, $01                     ;Sprite 08B do event: Move Left

db $89, $0A                     ;Sprite 08C do event: Hide
db $8A, $0A                     ;Sprite 08A do event: Hide
db $8B, $0A                     ;Sprite 08B do event: Hide
db $8C, $0A                     ;Sprite 08C do event: Hide

db $B5, $02                     ;Play Sound Effect Void, Image
db $C5, $E0, $71                ;<unknown>

db $D0, $81, $F0                ;(Music) 81 F0
db $75                          ;Extremely long pause
db $BE, $44                     ;Rumble effect of 44 magnitude
db $72
db $C4, $02
db $75
db $BE, $00                     ;Rumble effect of 44 magnitude
db $A5, $FE                     ;Clear Event Flag 1FE
db $A2, $B0                     ;Set Event Flag 0B0
db $A3, $B2                     ;Clear Event Flag 0B2
db $A3, $B1                     ;Clear Event Flag 0B1
; db $A4, $E7                     ;Set Event Flag 1E7
db $C2, $02                     ;Map 02


db $E1, $C3, $00, $14, $2A, $00 ;Return from cutscene? 00 00 40 A2 D8



; ORIGINAL WARP, CHANGED TO GENERIC WARP AREA FOR SAFETY
; db $C8, $AF, $01 ; CUSTOM MESSAGE FOR WARPZONE
; db $E1, $FE, $01, $03, $13, $00 ;Return from cutscene? 00 00 9C 96 00


; db $CD, $7F, $05                ;Run event index 057F
; db $CD, $42, $07                ;Run event index 0742
; db $B7, $82                     ;Add/Remove character 82
db $14
db $DB                          ;Restore Player status
db $09                          ;Player Show
db $C3, $10                     ;Fade in Speed 10
; db $7B                          ;*YOU DIDNT MEAN TO USE THIS*
db $CB, $0E, $00                ;Clear Flag 2/3/4/5/0E 00
db $CB, $01, $02                ;Clear Flag 2/3/4/5/01 02
db $CB, $FD, $01                ;Clear Flag 2/3/4/5/FD 01
db $CA, $01, $01                ;Set Flag 2/3/4/5/01 01
db $CB, $0A, $01                ;Clear Flag 2/3/4/5/0A 01
db $CA, $2D, $00                ;Set Flag 2/3/4/5/2D 00
db $CB, $DD, $00                ;Clear Flag 2/3/4/5/DD 00
db $CB, $DE, $00                ;Clear Flag 2/3/4/5/DE 00
db $CA, $33, $01                ;Set Flag 2/3/4/5/33 01
db $CA, $34, $01                ;Set Flag 2/3/4/5/34 01
db $CA, $F8, $00                ;Set Flag 2/3/4/5/F8 00

; db $A3, $B8                     ;Clear Event Flag 0B8

; CAREERDAY
; Remove event flag disabling free access back to Lonka
; db $A5, $FA                     ;Clear Event Flag 1FA

; set flags for airship scene after leaving and landing
db $A5, $FE                     ;Clear Event Flag 1FE
db $A2, $4D                     ;Set Event Flag 04D
db $CC, $13                  ;Custom destination flag 13 (Tycoon)

db $FF                          ;End Event

padbyte $00
pad $C8A664