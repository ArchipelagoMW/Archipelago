hirom


; NPC Halicarnaso sprite w/ hearts

org $C9F7AE

db $88, $03                     ;Sprite 088 do event: Move Down
db $88, $03                     ;Sprite 088 do event: Move Down
db $88, $03                     ;Sprite 088 do event: Move Down
db $F4, $00                     ;Unknown
db $3E                          ;Player pose: face up, both arms raised in
db $20                          ;Player pose: face down, left hand raised out
db $07                          ;<Unknown>
db $17                          ;Player pose: face left, down hand backward
db $01                          ;Player Move Up
db $88, $03                     ;Sprite 088 do event: Move Down
db $12                          ;Player pose: face right, standing
db $0C                          ;<Unknown>
db $C7, $03                     ;Play next 03 bytes simultaneously
db $88, $03                     ;Sprite 088 do event: Move Down
db $04                          ;Player move Left
db $0B                          ;<Unknown>
db $88, $26                     ;Sprite 088 do event: face up, right hand raised out
db $89, $09                     ;Sprite 089 do event: Show
db $89, $05                     ;Sprite 089 do event: Bounce
db $89, $00                     ;Sprite 089 do event: Hold
db $89, $05                     ;Sprite 089 do event: Bounce
db $89, $04                     ;Sprite 089 do event: Move Left
db $89, $03                     ;Sprite 089 do event: Move Down
db $89, $0A                     ;Sprite 089 do event: Hide
db $88, $13                     ;Sprite 088 do event: face right, down hand backward
db $CE, $05, $02                ;Play next 02 bytes 05 times
db $88, $01                     ;Sprite 088 do event: Move Up
db $88, $02                     ;Sprite 088 do event: Move Right
db $88, $0A                     ;Sprite 088 do event: Hide
db $12                          ;Player pose: face right, standing
db $CB, $59, $02                ;Clear Flag 2/3/4/5/59 02
db $A4, $97                     ;Set Event Flag 197

; set flag for first Halicarnaso  
db $A4, $99                     ;Set Event Flag 199 
db $FF                          ;End Event

padbyte $00
pad $C9F7ED


; $C9C3C4 → $C9C40E
; Halicarnaso minor speed ups

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