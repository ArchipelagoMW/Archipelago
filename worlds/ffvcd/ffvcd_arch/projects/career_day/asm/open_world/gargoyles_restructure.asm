hirom


org $c83449
db $80, $04, $F9
; ramuh - solitary shrine
org $F90480
db $10                          ;Player pose: face up, left hand forward
db $0C                          ;<Unknown>
db $C5, $E0                     ;<unknown>
db $03                          ;Player Move Down
db $71                          ;Short pause
db $0B                          ;<Unknown>
db $10                          ;Player pose: face up, left hand forward
db $88, $12                     ;Sprite 088 do event: face right, standing
db $89, $12                     ;Sprite 089 do event: face right, standing
db $8A, $12                     ;Sprite 08A do event: face right, standing
db $8B, $12                     ;Sprite 08B do event: face right, standing
db $CF, $03, $08                ;Play next 08 bytes simultaneously 03 times
db $88, $01                     ;Sprite 088 do event: Move Up
db $89, $01                     ;Sprite 089 do event: Move Up
db $8A, $01                     ;Sprite 08A do event: Move Up
db $8B, $01                     ;Sprite 08B do event: Move Up
db $88, $13                     ;Sprite 088 do event: face right, down hand backward
db $89, $13                     ;Sprite 089 do event: face right, down hand backward
db $8A, $13                     ;Sprite 08A do event: face right, down hand backward
db $8B, $13                     ;Sprite 08B do event: face right, down hand backward
db $CF, $03, $08                ;Play next 08 bytes simultaneously 03 times
db $88, $03                     ;Sprite 088 do event: Move Down
db $89, $03                     ;Sprite 089 do event: Move Down
db $8A, $03                     ;Sprite 08A do event: Move Down
db $8B, $03                     ;Sprite 08B do event: Move Down
db $BE, $0A                     ;Rumble effect of 0A magnitude
db $B5, $7E                     ;Play Sound Effect ?
db $71                          ;Short pause
db $88, $0A                     ;Sprite 088 do event: Hide
db $89, $0A                     ;Sprite 089 do event: Hide
db $8A, $0A                     ;Sprite 08A do event: Hide
db $8B, $0A                     ;Sprite 08B do event: Hide
db $BD, $3D, $FF                ;Start Event Battle 2D
db $BE, $00                     ;Rumble effect of 00 magnitude
db $FF                          ;End Event


org $C8345E
db $D0, $04, $F9
; golem
org $F904D0
db $10                          ;Player pose: face up, left hand forward
db $0C                          ;<Unknown>
db $C5, $E0                     ;<unknown>
db $03                          ;Player Move Down
db $71                          ;Short pause
db $0B                          ;<Unknown>
db $10                          ;Player pose: face up, left hand forward
db $88, $12                     ;Sprite 088 do event: face right, standing
db $89, $12                     ;Sprite 089 do event: face right, standing
db $8A, $12                     ;Sprite 08A do event: face right, standing
db $8B, $12                     ;Sprite 08B do event: face right, standing
db $CF, $03, $08                ;Play next 08 bytes simultaneously 03 times
db $88, $01                     ;Sprite 088 do event: Move Up
db $89, $01                     ;Sprite 089 do event: Move Up
db $8A, $01                     ;Sprite 08A do event: Move Up
db $8B, $01                     ;Sprite 08B do event: Move Up
db $88, $13                     ;Sprite 088 do event: face right, down hand backward
db $89, $13                     ;Sprite 089 do event: face right, down hand backward
db $8A, $13                     ;Sprite 08A do event: face right, down hand backward
db $8B, $13                     ;Sprite 08B do event: face right, down hand backward
db $CF, $03, $08                ;Play next 08 bytes simultaneously 03 times
db $88, $03                     ;Sprite 088 do event: Move Down
db $89, $03                     ;Sprite 089 do event: Move Down
db $8A, $03                     ;Sprite 08A do event: Move Down
db $8B, $03                     ;Sprite 08B do event: Move Down
db $BE, $0A                     ;Rumble effect of 0A magnitude
db $B5, $7E                     ;Play Sound Effect ?
db $71                          ;Short pause
db $88, $0A                     ;Sprite 088 do event: Hide
db $89, $0A                     ;Sprite 089 do event: Hide
db $8A, $0A                     ;Sprite 08A do event: Hide
db $8B, $0A                     ;Sprite 08B do event: Hide
db $BD, $3E, $FF                ;Start Event Battle 2D
db $BE, $00                     ;Rumble effect of 00 magnitude
db $FF                          ;End Event



org $c83431
db $20, $05, $F9
; shoat
org $F90520
db $10                          ;Player pose: face up, left hand forward
db $0C                          ;<Unknown>
db $C5, $E0                     ;<unknown>
db $03                          ;Player Move Down
db $71                          ;Short pause
db $0B                          ;<Unknown>
db $10                          ;Player pose: face up, left hand forward
db $88, $12                     ;Sprite 088 do event: face right, standing
db $89, $12                     ;Sprite 089 do event: face right, standing
db $8A, $12                     ;Sprite 08A do event: face right, standing
db $8B, $12                     ;Sprite 08B do event: face right, standing
db $CF, $03, $08                ;Play next 08 bytes simultaneously 03 times
db $88, $01                     ;Sprite 088 do event: Move Up
db $89, $01                     ;Sprite 089 do event: Move Up
db $8A, $01                     ;Sprite 08A do event: Move Up
db $8B, $01                     ;Sprite 08B do event: Move Up
db $88, $13                     ;Sprite 088 do event: face right, down hand backward
db $89, $13                     ;Sprite 089 do event: face right, down hand backward
db $8A, $13                     ;Sprite 08A do event: face right, down hand backward
db $8B, $13                     ;Sprite 08B do event: face right, down hand backward
db $CF, $03, $08                ;Play next 08 bytes simultaneously 03 times
db $88, $03                     ;Sprite 088 do event: Move Down
db $89, $03                     ;Sprite 089 do event: Move Down
db $8A, $03                     ;Sprite 08A do event: Move Down
db $8B, $03                     ;Sprite 08B do event: Move Down
db $BE, $0A                     ;Rumble effect of 0A magnitude
db $B5, $7E                     ;Play Sound Effect ?
db $71                          ;Short pause
db $88, $0A                     ;Sprite 088 do event: Hide
db $89, $0A                     ;Sprite 089 do event: Hide
db $8A, $0A                     ;Sprite 08A do event: Hide
db $8B, $0A                     ;Sprite 08B do event: Hide
db $BD, $3F, $FF                ;Start Event Battle 2D
db $BE, $00                     ;Rumble effect of 00 magnitude
db $FF                          ;End Event
