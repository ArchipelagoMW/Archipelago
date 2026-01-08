hirom


org $C90E96


; Moogle boss & post dialogue

db $82, $10                      ;Sprite 082 do event face up, left hand forward
db $81, $10                      ;Sprite 081 do event face up, left hand forward
db $82, $04                      ;Sprite 082 do event Move Left
db $82, $24                      ;Sprite 082 do event face down, right hand raised in
db $82, $05                      ;Sprite 082 do event Bounce
db $82, $00                      ;Sprite 082 do event Hold
db $82, $0A                      ;Sprite 082 do event Hide
db $BD, $1C, $06                        ;Start Event Battle 1C
db $C5, $80
db $B5, $02
db $71
db $DE, $71 ; custom reward
db $DF
db $B4, $07                     ;Play Background Music Critter Tripper Fritter!
db $01                                 ;Player Move Up
db $16                          ;Player pose: face left, standing
db $2B                          ;Player pose: face left, left hand out
db $70
db $C4, $03                     ;Fade in Speed 02
db $74
db $81, $0A                      ;Sprite 081 do event Hide
db $14                          ;Player pose: face down, left hand forward
db $CB, $3E, $02                        ;Clear Flag 2/3/4/5/3E 02
db $CB, $3F, $02                        ;Clear Flag 2/3/4/5/3F 02
db $A4, $3C                     ;Set Event Flag 13C

; set event flags for Moogle searching in Village 
db $A4, $2C                     ;Set Event Flag 12C
db $CB, $E6, $01                ;Clear Flag 2/3/4/5/E6 01
db $CB, $E7, $01                ;Clear Flag 2/3/4/5/E7 01
db $CB, $DF, $01                ;Clear Flag 2/3/4/5/DF 01
db $CA, $E0, $01                ;Set Flag 2/3/4/5/E0 01
db $CA, $E1, $01                ;Set Flag 2/3/4/5/E1 01
db $CA, $E2, $01                ;Set Flag 2/3/4/5/E2 01
db $CA, $E3, $01                ;Set Flag 2/3/4/5/E3 01
db $CA, $E4, $01                ;Set Flag 2/3/4/5/E4 01
db $CA, $E5, $01                ;Set Flag 2/3/4/5/E5 01
db $A4, $2D                     ;Set Event Flag 12D
db $CC, $1A                  ;Custom destination flag 1A
db $74
db $C3, $03                     ;Fade in Speed 02
db $73
db $FF                                 ;End Event

padbyte $00
pad $C91021