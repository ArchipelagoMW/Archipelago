hirom


; pre-cannon

org $C98247

db $CA, $FD, $00                ;Set Flag 2/3/4/5/FD 00
db $E3, $DD, $20, $07, $09, $D8 ;Inter-map cutscene? DD 20 07 09 D8
db $A5, $FE                     ;Clear Event Flag 1FE
db $CD, $A9, $00                ;Run event index 00A9
db $CD, $A7, $04                ;Run event index 04A7
db $D9, $0C, $05, $D9           ;Unknown
db $0A                          ;Player Hide
db $03                          ;Player Move Down
db $C1, $01                     ;<Unknown>
db $C3, $10                     ;Fade in Speed 10
db $A2, $B7                     ;Set Event Flag 0B7
db $D0, $F2, $00                ;(Music) F2 00
db $FF                          ;End Event

padbyte $00
pad $C982C3

; post-cannon
org $C89ABD
db $C5, $80
db $B5, $02
db $71
db $DE, $6A ; custom reward
db $DF
db $CB, $FD, $00                ;Clear Flag 2/3/4/5/FD 00
db $A2, $4B                     ;Set Event Flag 04B
db $FF                          ;End Event