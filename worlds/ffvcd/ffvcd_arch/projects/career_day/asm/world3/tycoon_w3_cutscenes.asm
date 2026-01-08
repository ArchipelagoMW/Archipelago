hirom


; $C8DE22 → $C8E127

org $C8DE22

db $CD, $90, $03                ;Run event index 0390
db $CA, $40, $01                ;Set Flag 2/3/4/5/40 01
db $CA, $10, $01                ;Set Flag 2/3/4/5/10 01
db $CA, $11, $01                ;Set Flag 2/3/4/5/11 01
db $CA, $12, $01                ;Set Flag 2/3/4/5/12 01
db $CA, $13, $01                ;Set Flag 2/3/4/5/13 01
db $CA, $14, $01                ;Set Flag 2/3/4/5/14 01
db $CA, $19, $01                ;Set Flag 2/3/4/5/19 01
db $CA, $1A, $01                ;Set Flag 2/3/4/5/1A 01
db $CA, $1B, $01                ;Set Flag 2/3/4/5/1B 01
db $CA, $17, $01                ;Set Flag 2/3/4/5/17 01
db $CA, $18, $01                ;Set Flag 2/3/4/5/18 01
db $CB, $0E, $01                ;Clear Flag 2/3/4/5/0E 01
db $CA, $0E, $01                ;Set Flag 2/3/4/5/0E 01
; db $B7, $89                     ;Add/Remove character 89
; db $B7, $8B                     ;Add/Remove character 8B
; db $B7, $8C                     ;Add/Remove character 8C
db $CB, $0C, $00                ;Clear Flag 2/3/4/5/0C 00
db $CB, $0D, $00                ;Clear Flag 2/3/4/5/0D 00
db $CB, $CF, $02                ;Clear Flag 2/3/4/5/CF 02
db $CB, $CE, $02                ;Clear Flag 2/3/4/5/CE 02
db $CB, $CD, $02                ;Clear Flag 2/3/4/5/CD 02
db $CB, $CC, $02                ;Clear Flag 2/3/4/5/CC 02
db $CB, $DE, $02                ;Clear Flag 2/3/4/5/DE 02
db $CB, $CB, $02                ;Clear Flag 2/3/4/5/CB 02
db $CB, $DB, $02                ;Clear Flag 2/3/4/5/DB 02
db $CB, $DC, $02                ;Clear Flag 2/3/4/5/DC 02
db $CB, $DD, $02                ;Clear Flag 2/3/4/5/DD 02
db $CA, $1F, $00                ;Set Flag 2/3/4/5/1F 00
db $CB, $C9, $02                ;Clear Flag 2/3/4/5/C9 02
db $CB, $06, $01                ;Clear Flag 2/3/4/5/06 01
db $CB, $07, $01                ;Clear Flag 2/3/4/5/07 01
db $CB, $08, $01                ;Clear Flag 2/3/4/5/08 01
db $CB, $82, $00                ;Clear Flag 2/3/4/5/82 00
db $CB, $3E, $01                ;Clear Flag 2/3/4/5/3E 01
db $CB, $CA, $02                ;Clear Flag 2/3/4/5/CA 02
db $CB, $13, $00                ;Clear Flag 2/3/4/5/13 00
db $A2, $2C                     ;Set Event Flag 02C
db $A2, $98                     ;Set Event Flag 098
db $A4, $FE                     ;Set Event Flag 1FE
db $E3, $4C, $00, $23, $13, $00 ;Inter-map cutscene? 4C 00 23 13 00
db $02                          ;Player Move Right
db $02                          ;Player Move Right
db $02                          ;Player Move Right
db $02                          ;Player Move Right
db $02                          ;Player Move Right
db $02                          ;Player Move Right
db $14
db $C3, $03
db $73
db $FF                          ;End Event

padbyte $00
pad $C8E127

; $C8E128 → C8E157
; Cara on the balcony

org $C8E128

db $02                          ;Player Move Right
db $92, $0A                     ;Sprite 192 do event: Hide
db $DB                          ;Restore Player status
db $CB, $0E, $01                ;Clear Flag 2/3/4/5/0E 01
; db $B7, $0C                     ;Add/Remove character 0C
db $A2, $7A                     ;Set Event Flag 07A
db $CA, $0D, $01                ;Set Flag 2/3/4/5/0D 01

; future cutscenes in Tycoon, Cara at leaving ballroom, leaving with guard 

db $A2, $7B                     ;Set Event Flag 07B
db $A4, $F0                     ;Set Event Flag 1F0
db $A4, $FC                     ;Set Event Flag 1FC
db $CC, $25                  ;Custom destination flag 25
db $FF                          ;End Event
padbyte $00
pad $C8E157

