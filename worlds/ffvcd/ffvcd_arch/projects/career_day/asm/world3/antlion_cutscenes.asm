hirom


; Fall → antlion

org $C8BD45

db $03                          ;Player Move Down
db $B5, $84                     ;Play Sound Effect Exdeath destroyed 2
db $BE, $05                     ;Rumble effect of 05 magnitude
db $12                          ;Player pose: face right, standing
db $16                          ;Player pose: face left, standing
db $BE, $0A                     ;Rumble effect of 0A magnitude
db $14                          ;Player pose: face down, left hand forward
db $B5, $7E                     ;Play Sound Effect ?
db $F3, $09, $1F, $24           ;Set Map Tiles 09 1F 24
db $D0, $D1, $D2                ;(Music) D1 D2
db $D3, $D4, $E0, $E1           ;Sprite D4 set map position E0, E1
db $E2, $E3                     ;Unknown
db $E4, $F0                     ;Unknown
db $F1, $F2                     ;Unknown
db $F3, $F4, $05, $00           ;Set Map Tiles F4 05 00
db $0A                          ;Player Hide
; db $70                          ;Very short pause
db $D0, $F0, $00                ;(Music) F0 00
db $E3, $73, $01, $20, $17, $00 ;Inter-map cutscene? 73 01 20 17 00
db $BE, $00                     ;Rumble effect of 00 magnitude
db $D0, $80, $00                ;(Music) 80 00
db $0A                          ;Player Hide
db $B1, $02                     ;Set Player Sprite 02
db $8E, $09                     ;Sprite 08E do event: Show
db $8E, $4A                     ;Sprite 08E do event: garbage
db $81, $09                     ;Sprite 081 do event: Show
db $81, $4A                     ;Sprite 081 do event: garbage
db $80, $09                     ;Sprite 080 do event: Show
db $80, $5B                     ;Sprite 080 do event: 5B
db $81, $0B                     ;Sprite 081 do event: 0B
db $80, $0B                     ;Sprite 080 do event: 0B
db $8E, $0B                     ;Sprite 08E do event: 0B
db $8E, $13                     ;Sprite 08E do event: face right, down hand backward
db $81, $13                     ;Sprite 081 do event: face right, down hand backward
db $80, $13                     ;Sprite 080 do event: face right, down hand backward
; db $77                          ;<Unknown>
db $C3, $08                     ;Fade in Speed 08
db $B5, $85                     ;Play Sound Effect Falling
db $CF, $0A, $07                ;Play next 07 bytes simultaneously 0A times
db $03                          ;Player Move Down
db $8E, $03                     ;Sprite 08E do event: Move Down
db $80, $03                     ;Sprite 080 do event: Move Down
db $81, $03                     ;Sprite 081 do event: Move Down
db $BE, $0A                     ;Rumble effect of 0A magnitude
db $3A                          ;Player pose: face down, surprised
db $09                          ;Player Show
db $8E, $0A                     ;Sprite 08E do event: Hide
; db $76                          ;<Unknown>
db $81, $10                     ;Sprite 081 do event: face up, left hand forward
db $80, $10                     ;Sprite 080 do event: face up, left hand forward
db $05                          ;Player Bounce in Place
db $81, $05                     ;Sprite 081 do event: Bounce
db $80, $05                     ;Sprite 080 do event: Bounce
db $C7, $05                     ;Play next 05 bytes simultaneously
db $03                          ;Player Move Down
db $80, $04                     ;Sprite 080 do event: Move Left
db $81, $04                     ;Sprite 081 do event: Move Left
db $34                          ;Player pose: face down, splayed, looking left
db $81, $44                     ;Sprite 081 do event: face down, head lowered, left hand forward
db $0B                          ;<Unknown>
db $81, $0B                     ;Sprite 081 do event: 0B
db $80, $0B                     ;Sprite 080 do event: 0B
db $80, $22                     ;Sprite 080 do event: face down, left hand on head
db $BE, $00                     ;Rumble effect of 00 magnitude
; db $73                          ;Long pause
db $81, $22                     ;Sprite 081 do event: face down, left hand on head
db $14                          ;Player pose: face down, left hand forward
db $81, $03                     ;Sprite 081 do event: Move Down
db $81, $22                     ;Sprite 081 do event: face down, left hand on head
db $16                          ;Player pose: face left, standing
; db $73                          ;Long pause
db $30                          ;Player pose: face left, head lowered
; db $74                          ;Very long pause
db $04                          ;Player move Left
db $2A                          ;Player pose: face left, left hand raised
; db $73                          ;Long pause
db $80, $5B                     ;Sprite 080 do event: 5B
db $80, $0B                     ;Sprite 080 do event: 0B
db $80, $05                     ;Sprite 080 do event: Bounce
db $80, $00                     ;Sprite 080 do event: Hold
db $80, $05                     ;Sprite 080 do event: Bounce
db $80, $00                     ;Sprite 080 do event: Hold
db $80, $0B                     ;Sprite 080 do event: 0B
db $80, $22                     ;Sprite 080 do event: face down, left hand on head
db $81, $04                     ;Sprite 081 do event: Move Left
db $81, $03                     ;Sprite 081 do event: Move Down
db $81, $03                     ;Sprite 081 do event: Move Down
db $81, $02                     ;Sprite 081 do event: Move Right
db $81, $02                     ;Sprite 081 do event: Move Right
db $81, $20                     ;Sprite 081 do event: face down, left hand raised out
db $14                          ;Player pose: face down, left hand forward
; db $72                          ;Medium pause
db $2E                          ;Player pose: face down, head lowered
; db $74                          ;Very long pause
db $B5, $84                     ;Play Sound Effect Exdeath destroyed 2
db $BE, $05                     ;Rumble effect of 05 magnitude
db $83, $09                     ;Sprite 083 do event: Show
db $81, $02                     ;Sprite 081 do event: Move Right
db $80, $22                     ;Sprite 080 do event: face down, left hand on head
db $81, $01                     ;Sprite 081 do event: Move Up
db $81, $26                     ;Sprite 081 do event: face up, right hand raised out
db $81, $22                     ;Sprite 081 do event: face down, left hand on head
db $81, $3D                     ;Sprite 081 do event: face up, both arms raised out
db $14                          ;Player pose: face down, left hand forward
; db $70                          ;Very short pause
db $12                          ;Player pose: face right, standing
; db $73                          ;Long pause
db $BE, $0A                     ;Rumble effect of 0A magnitude
db $82, $09                     ;Sprite 082 do event: Show
db $80, $5B                     ;Sprite 080 do event: 5B
db $80, $0B                     ;Sprite 080 do event: 0B
db $80, $05                     ;Sprite 080 do event: Bounce
db $80, $01                     ;Sprite 080 do event: Move Up
db $80, $05                     ;Sprite 080 do event: Bounce
db $80, $01                     ;Sprite 080 do event: Move Up
db $80, $0B                     ;Sprite 080 do event: 0B
db $80, $26                     ;Sprite 080 do event: face up, right hand raised out
; db $73                          ;Long pause
db $BE, $05                     ;Rumble effect of 05 magnitude
db $16                          ;Player pose: face left, standing
db $CF, $02, $04                ;Play next 04 bytes simultaneously 02 times
db $82, $02                     ;Sprite 082 do event: Move Right
db $83, $04                     ;Sprite 083 do event: Move Left
db $80, $24                     ;Sprite 080 do event: face down, right hand raised in
db $BE, $0A                     ;Rumble effect of 0A magnitude
; db $73                          ;Long pause
db $C5                          ;<unknown>
db $20                          ;Player pose: face down, left hand raised out
db $82, $10                     ;Sprite 082 do event: face up, left hand forward
db $83, $10                     ;Sprite 083 do event: face up, left hand forward
db $C7, $04                     ;Play next 04 bytes simultaneously
db $82, $02                     ;Sprite 082 do event: Move Right
db $83, $04                     ;Sprite 083 do event: Move Left
db $BE, $00                     ;Rumble effect of 00 magnitude
db $82, $0A                     ;Sprite 082 do event: Hide
db $83, $0A                     ;Sprite 083 do event: Hide
; db $70                          ;Very short pause
db $BD, $25, $FF                ;Start Event Battle 25
db $C5, $80
db $B5, $02
; db $71
db $DE, $79 ; custom reward
db $DF
db $E3, $02, $00, $79, $59, $24 ;Inter-map cutscene? 02 00 79 59 24
db $09                          ;Player Show
db $14                          ;Player pose: face down, left hand forward
db $C3, $0C                     ;Fade in Speed 0C
; db $73                          ;Long pause
db $A2, $7F                     ;Set Event Flag 07F
db $CB, $18, $01                ;Clear Flag 2/3/4/5/18 01
db $CA, $0D, $00                ;Set Flag 2/3/4/5/0D 00
;db $B7, $0B                     ;Add/Remove character 0B
db $FF                          ;End Event

padbyte $00
pad $C8BE7C