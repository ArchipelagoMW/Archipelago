hirom


; Calofisteri text remove

org $C9C611

db $B5, $93                     ;Play Sound Effect Evil appears
db $3A                          ;Player pose: face down, surprised
db $0C                          ;<Unknown>
db $06                          ;Player Bounce in Place
db $03                          ;Player Move Down
db $0B                          ;<Unknown>
db $10                          ;Player pose: face up, left hand forward
db $81, $09                     ;Sprite 081 do event: Show
db $81, $03                     ;Sprite 081 do event: Move Down
db $81, $0A                     ;Sprite 081 do event: Hide
db $BD, $47, $FF                ;Start Event Battle 47
db $DE, $A0 ; custom reward
db $DF
db $0B                          ;<Unknown>
db $10                          ;Player pose: face up, left hand forward
db $A4, $79                     ;Set Event Flag 179
db $FF                          ;End Event

padbyte $00
pad $C9C62B