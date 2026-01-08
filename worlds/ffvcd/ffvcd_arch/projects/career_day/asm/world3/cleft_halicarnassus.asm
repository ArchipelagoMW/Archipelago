hirom


; Halicarnassus minor speed ups

org $C9C3C4

db $0B                          ;<Unknown>
db $82, $09                     ;Sprite 082 do event: Show
db $82, $01                     ;Sprite 082 do event: Move Up
db $82, $01                     ;Sprite 082 do event: Move Up
db $82, $01                     ;Sprite 082 do event: Move Up
db $82, $01                     ;Sprite 082 do event: Move Up
db $81, $09                     ;Sprite 081 do event: Show
db $81, $05                     ;Sprite 081 do event: Bounce
db $81, $00                     ;Sprite 081 do event: Hold
db $82, $22                     ;Sprite 082 do event: face down, left hand on head
db $B2, $04                     ;Pause for 04 cycles
db $82, $24                     ;Sprite 082 do event: face down, right hand raised in
db $73
db $81, $0A                     ;Sprite 081 do event: Hide
db $B5, $93                     ;Play Sound Effect Evil appears
db $CE, $0F, $06                ;Play next 0C bytes 0F times
db $80, $0A                     ;Sprite 080 do event: Hide
db $82, $09                     ;Sprite 082 do event: Show
db $80, $09                     ;Sprite 080 do event: Show
db $C5                          ;<unknown>
db $E0, $73                     ;Unknown
db $82, $0A                     ;Sprite 082 do event: Hide
db $80, $16                     ;Sprite 080 do event: face left, standing
db $80, $01                     ;Sprite 080 do event: Move Up
db $80, $01                     ;Sprite 080 do event: Move Up
db $80, $0A                     ;Sprite 080 do event: Hide
db $BD, $38, $FF                ;Start Event Battle 38
db $DE, $A4 ; custom reward
db $DF
db $7D                          ;<Unknown>
db $CB, $90, $03                ;Clear Flag 2/3/4/5/90 03
db $A4, $75                     ;Set Event Flag 175
db $FF                          ;End Event


padbyte $00
pad $C9C40E
