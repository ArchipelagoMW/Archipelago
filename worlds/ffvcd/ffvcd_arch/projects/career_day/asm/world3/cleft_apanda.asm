hirom


; Apanda text box

org $C9C24D

db $81, $16                     ;Sprite 081 do event: face left, standing
db $B5, $3A                     ;Play Sound Effect Quick
db $B9, $63                     ;Toggle Subtracitve Tint by 63
db $B5, $93                     ;Play Sound Effect Evil appears
db $CE, $14, $08                ;Play next 08 bytes 14 times
db $80, $0A                     ;Sprite 080 do event: Hide
db $80, $09                     ;Sprite 080 do event: Show
db $73                          ;Long pause
db $80, $0A                     ;Sprite 080 do event: Hide
db $BD, $36, $FF                ;Start Event Battle 36
db $DE, $A1 ; custom reward
db $DF
db $7D                          ;<Unknown>
db $A4, $71                     ;Set Event Flag 171
db $A4, $74                     ;Set Event Flag 174
db $71                          ;Short pause
db $C5                          ;<unknown>
db $80, $B5                     ;Sprite 080 do event: B5
db $7F                          ;*YOU DIDNT MEAN TO USE THIS*
db $FF                          ;End Event

padbyte $00
pad $C9C275