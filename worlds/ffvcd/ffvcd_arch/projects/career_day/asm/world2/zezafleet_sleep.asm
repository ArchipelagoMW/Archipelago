hirom


; Sleep at Zeza cabin. Preserved, only text box removed
; Zeza talk flag triggered instantly

org $C93725

db $CD, $F3, $04                ;Run event index 04F3
db $B4, $22                     ;Play Background Music Battle with Gilgamesh
db $BE, $4E                     ;Rumble effect of 4E magnitude
db $3A                          ;Player pose: face down, surprised
db $71
db $BE, $40                     ;Rumble effect of 40 magnitude
db $CD, $DE, $03                ;Run event index 03DE
db $A4, $FE                     ;Set Event Flag 1FE
db $CB, $01, $03                ;Clear Flag 2/3/4/5/01 03
db $CB, $02, $03                ;Clear Flag 2/3/4/5/02 03
db $CB, $03, $03                ;Clear Flag 2/3/4/5/03 03
db $A2, $6C                     ;Set Event Flag 06C

db $FF                          ;End Event

padbyte $00
pad $C9377F