hirom


org $C98445

db $CD, $B6, $04                ;Run event index 04B6
db $CD, $B7, $04                ;Run event index 04B7
db $80, $02                     ;Sprite 080 do event: Move Right
db $80, $26                     ;Sprite 080 do event: face up, right hand raised out
db $80, $11                     ;Sprite 080 do event: face up, right hand forward
db $81, $11                     ;Sprite 081 do event: face up, right hand forward
db $CA, $FC, $00                ;Set Flag 2/3/4/5/FC 00
db $A2, $26                     ;Set Event Flag 026
db $FF                          ;End Event

padbyte $00
pad $C9845C

org $C985AB

db $0C                          ;<Unknown>
db $CE, $02, $0C                ;Play next 0C bytes 02 times
db $B5, $7E                     ;Play Sound Effect ?
db $BE, $4A                     ;Rumble effect of 4A magnitude
db $3A                          ;Player pose: face down, surprised
db $05                          ;Player Bounce in Place
db $00                          ;Player Hold
db $14                          ;Player pose: face down, left hand forward
db $70                          ;Very short pause
db $BE, $40                     ;Rumble effect of 40 magnitude
db $71                          ;Short pause
db $0B                          ;<Unknown>
db $70                          ;Very short pause
db $87, $0A                     ;Sprite 087 do event: Hide
db $BD, $11, $FF                ;Start Event Battle 11
db $72                          ;Medium pause
db $B4, $29                     ;Play Background Music Fanfare 1 (short)
db $DE, $11						; set up reward
db $DF							; call text handler
db $C5, $80
db $B5, $02
db $71
db $C5, $80
db $B5, $02
db $71
db $DE, $6E ; custom reward
db $DF
db $73
db $CB, $F9, $00                ;Clear Flag 2/3/4/5/F9 00
db $CB, $FB, $00                ;Clear Flag 2/3/4/5/FB 00
db $E3, $7D, $00, $90, $12, $00 ;Inter-map cutscene? 7D 00 90 12 00
db $D3, $80, $90, $0F           ;Sprite 80 set map position 90, 0F
db $D3, $81, $90, $0F           ;Sprite 81 set map position 90, 0F
db $2E                          ;Player pose: face down, head lowered
db $C3, $10                     ;Fade in Speed 10
db $80, $10                     ;Sprite 080 do event: face up, left hand forward
db $81, $10                     ;Sprite 081 do event: face up, left hand forward
db $CD, $B7, $04                ;Run event index 04B7
db $CB, $FC, $00                ;Clear Flag 2/3/4/5/FC 00
db $CC, $2A                  ;Custom destination flag
db $A3, $BB                     ;Clear Event Flag 0BB
db $A2, $50                     ;Set Event Flag 050
db $FF                          ;End Event

pad $C9860C

