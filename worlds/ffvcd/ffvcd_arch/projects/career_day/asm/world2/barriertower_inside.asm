hirom


; First talk with Zeza in tower 

org $C8D34E

db $80, $09                     ;Sprite 080 do event: Show
db $81, $09                     ;Sprite 081 do event: Show
db $82, $09                     ;Sprite 082 do event: Show
db $83, $10                     ;Sprite 083 do event: face up, left hand forward
db $B1, $02                     ;Set Player Sprite 02
db $C7, $06                     ;Play next 06 bytes simultaneously
db $80, $02                     ;Sprite 080 do event: Move Right
db $82, $04                     ;Sprite 082 do event: Move Left
db $81, $03                     ;Sprite 081 do event: Move Down
db $80, $24                     ;Sprite 080 do event: face down, right hand raised in
db $82, $24                     ;Sprite 082 do event: face down, right hand raised in
db $81, $4F                     ;Sprite 081 do event: garbage
db $81, $50                     ;Sprite 081 do event: 50
db $81, $24                     ;Sprite 081 do event: face down, right hand raised in
db $83, $26                     ;Sprite 083 do event: face up, right hand raised out
db $83, $24                     ;Sprite 083 do event: face down, right hand raised in
db $83, $54                     ;Sprite 083 do event: 54
db $83, $01                     ;Sprite 083 do event: Move Up
db $83, $01                     ;Sprite 083 do event: Move Up
db $81, $3E                     ;Sprite 081 do event: face up, both arms raised in
db $81, $30                     ;Sprite 081 do event: face left, head lowered
; db $C8, $7A, $05                ;Display Message/Text/Dialogue 7A 05
db $81, $24                     ;Sprite 081 do event: face down, right hand raised in
db $CE, $06, $02                ;Play next 02 bytes 06 times
db $83, $04                     ;Sprite 083 do event: Move Left
db $81, $26                     ;Sprite 081 do event: face up, right hand raised out
db $80, $26                     ;Sprite 080 do event: face up, right hand raised out
db $82, $26                     ;Sprite 082 do event: face up, right hand raised out
db $16                          ;Player pose: face left, standing
db $83, $01                     ;Sprite 083 do event: Move Up
db $83, $01                     ;Sprite 083 do event: Move Up
db $CE, $04, $02                ;Play next 02 bytes 04 times
db $83, $01                     ;Sprite 083 do event: Move Up
db $83, $04                     ;Sprite 083 do event: Move Left
db $83, $04                     ;Sprite 083 do event: Move Left
db $83, $0A                     ;Sprite 083 do event: Hide
db $C7, $06                     ;Play next 06 bytes simultaneously
db $80, $04                     ;Sprite 080 do event: Move Left
db $82, $02                     ;Sprite 082 do event: Move Right
db $81, $01                     ;Sprite 081 do event: Move Up
db $80, $0A                     ;Sprite 080 do event: Hide
db $82, $0A                     ;Sprite 082 do event: Hide
db $81, $0A                     ;Sprite 081 do event: Hide
db $DB                          ;Restore Player status
db $CB, $D9, $00                ;Clear Flag 2/3/4/5/D9 00
db $A2, $6F                     ;Set Event Flag 06F
db $A2, $A2                     ;Set Event Flag 0A2		next 3 are for flags related to zeza mid-tower cutscene. disable immediately
db $CB, $10, $03                ;Clear Flag 2/3/4/5/10 03
db $CA, $11, $03                ;Set Flag 2/3/4/5/11 03
db $FF                          ;End Event

padbyte $00
pad $C8D3CB