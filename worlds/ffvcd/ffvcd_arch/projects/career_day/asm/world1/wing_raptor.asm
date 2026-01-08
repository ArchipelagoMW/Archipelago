hirom

org $C85BF6

db $0C                          ;<Unknown>
db $CE, $03, $16                ;Play next 16 bytes 03 times
db $80, $05                     ;Sprite 080 do event: Bounce
db $81, $05                     ;Sprite 081 do event: Bounce
db $82, $05                     ;Sprite 082 do event: Bounce
db $C7, $07                     ;Play next 07 bytes simultaneously
db $80, $03                     ;Sprite 080 do event: Move Down
db $81, $03                     ;Sprite 081 do event: Move Down
db $82, $03                     ;Sprite 082 do event: Move Down
db $03                          ;Player Move Down
db $BE, $04                     ;Rumble effect of 04 magnitude
db $B5, $88                     ;Play Sound Effect Titan steps
db $71                          ;Short pause
db $BE, $00                     ;Rumble effect of 00 magnitude
db $0B                          ;<Unknown>
db $00, $00, $00
db $71                          ;Short pause
db $80, $0A                     ;Sprite 080 do event: Hide
db $81, $0A                     ;Sprite 081 do event: Hide
db $82, $0A                     ;Sprite 082 do event: Hide
db $BD, $01, $FF                ;Start Event Battle 01
db $10                          ;Player pose: face up, left hand forward
db $CB, $4A, $00                ;Turn off bit 04 at address  0x7e0a5d
db $A4, $20                     ;Turn on bit 01 at address 0x7e0a38
db $CA, $4B, $00                ;Turn on bit 08 at address  0x7e0a5d
db $CA, $4C, $00                ;Turn on bit 10 at address  0x7e0a5d
db $C5, $80
db $B5, $02
db $71
db $DE, $61 ; custom reward
db $DF
db $FF                          ;End Event

pad $C85C1E