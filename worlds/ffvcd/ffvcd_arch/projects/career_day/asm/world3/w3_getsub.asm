hirom


; $C9C9B2 → $C9CBEF
; Cutscene from finding Mid in the wheel → overworld map 

org $C9C9B2

db $3A                          ;Player pose: face down, surprised
db $0C                          ;<Unknown>
db $05                          ;Player Bounce in Place
db $00                          ;Player Hold
db $05                          ;Player Bounce in Place
db $00                          ;Player Hold
db $0B                          ;<Unknown>

; db $C4, $03                   ; Fade out, although nice, was causing problems with a blip 
; db $73


; cid during wheel turn, just for effect
db $CE, $03, $10                ;Play next 10 bytes 03 times
db $80, $03                     ;Sprite 080 do event: Move Down
db $80, $03                     ;Sprite 080 do event: Move Down
db $80, $07                     ;Sprite 080 do event: 07
db $80, $08                     ;Sprite 080 do event: 08
db $80, $01                     ;Sprite 080 do event: Move Up
db $80, $01                     ;Sprite 080 do event: Move Up
db $80, $07                     ;Sprite 080 do event: 07
db $80, $08                     ;Sprite 080 do event: 08

db $C4, $03                   ; Fade out, although nice, was causing problems with a blip 
db $73
db $E1, $D2, $00, $9C, $14, $00 ;Return from cutscene? D2 00 9C 14 00
db $01
db $01
db $01
db $01
db $01
db $01
db $01
db $02
db $01
db $01
db $02
db $01
db $14
db $C3, $03                   ; Fade out, although nice, was causing problems with a blip 
db $73
db $C8, $72, $07                ;Display Message/Text/Dialogue 72 07

db $E3, $02, $00, $CE, $C8, $D8 ;Inter-map cutscene? 02 00 CE C8 D8
db $BE, $40                     ;Rumble effect of 40 magnitude
db $09                          ;Player Show
db $C3, $0A                     ;Fade in Speed 0A
db $71                          ;Short pause
db $B5, $69                     ;Play Sound Effect Airship
db $7B                          ;*YOU DIDNT MEAN TO USE THIS*
db $A5, $FE                     ;Clear Event Flag 1FE
db $A2, $8F                     ;Set Event Flag 08F
db $A4, $F9                     ;Set Event Flag 1F9
db $CA, $DE, $00                ;Set Flag 2/3/4/5/DE 00
db $CA, $DD, $00                ;Set Flag 2/3/4/5/DD 00
db $CB, $1F, $00                ;Clear Flag 2/3/4/5/1F 00
db $CB, $FA, $01                ;Clear Flag 2/3/4/5/FA 01
db $FF                          ;End Event

padbyte $00
pad $C9CBEF