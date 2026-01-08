hirom


org $C89A03

;db $B1, $03                     ;Set Player Sprite 03
;db $A0, $00                     ;(Message) 00
;db $80, $10                     ;Sprite 080 do event: face up, left hand forward
db $71                          ;Short pause
;db $A0, $01                     ;(Message) 01
db $80, $01                     ;Sprite 080 do event: Move Up
db $80, $04                     ;Sprite 080 do event: Move Left
db $80, $22                     ;Sprite 080 do event: face down, left hand on head
;db $A0, $02                     ;(Message) 02
db $01                          ;Player Move Up
db $01                          ;Player Move Up
db $81, $10                     ;Sprite 081 do event: face up, left hand forward
db $81, $03                     ;Sprite 081 do event: Move Down
db $81, $03                     ;Sprite 081 do event: Move Down
db $81, $0A                     ;Sprite 081 do event: Hide
db $BD, $0F, $FF                ;Start Event Battle 0F
db $C5, $80
db $B5, $02
db $71
db $DE, $6B ; custom reward
db $DF
;db $73                          ;Long pause
;db $A0, $04                     ;(Message) 04
db $80, $10                     ;Sprite 080 do event: face up, left hand forward
;db $71                          ;Short pause
db $3A                          ;Player pose: face down, surprised
db $0C                          ;<Unknown>
db $05                          ;Player Bounce in Place
db $C7, $03                     ;Play next 03 bytes simultaneously
db $02                          ;Player Move Right
db $80, $02                     ;Sprite 080 do event: Move Right
db $0B                          ;<Unknown>
db $16                          ;Player pose: face left, standing
db $CE, $07, $02                ;Play next 02 bytes 07 times
db $80, $01                     ;Sprite 080 do event: Move Up
db $F3, $17, $0D, $10           ;Set Map Tiles 17 0D 10
db $62                  ;Player or Sprite Pose
db $72                          ;Medium pause
db $04                          ;Player move Left
db $01                          ;Player Move Up
db $01                          ;Player Move Up
db $80, $01                     ;Sprite 080 do event: Move Up
db $80, $0A                     ;Sprite 080 do event: Hide
db $70                          ;Very short pause
db $F3, $17, $0D, $10, $42, $52 ;Set Map Tiles 17 0D 10 42 52
db $42                          ;Player pose: garbage
db $DB                          ;Restore Player status
db $CB, $CD, $00                ;Clear Flag 2/3/4/5/CD 00
db $CB, $CE, $00                ;Clear Flag 2/3/4/5/CE 00
db $FF                          ;End Event

padbyte $00
pad $C89A85