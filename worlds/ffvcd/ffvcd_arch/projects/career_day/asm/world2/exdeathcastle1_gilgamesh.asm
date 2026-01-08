hirom


org $C93C1E

; Gilgamesh first fight, getting back companions
; Keeps some animations but cuts out dialogue & waiting

db $83, $24                     ;Sprite 083 do event face down, right hand raised in
db $D3, $86, $32, $0A           ;Sprite 86 set map position 32, 0A
db $00                          ;Player Hold

db $83, $13                     ;Sprite 083 do event face right, down hand backward
db $83, $04                     ;Sprite 083 do event Move Left
db $CE, $03, $02                ;Play next 02 bytes 03 times
db $83, $03                     ;Sprite 083 do event Move Down
db $BD, $94, $FF                ;Start Event Battle 94
db $83, $0A                     ;Sprite 083 do event Hide
db $C3, $03
db $73
db $C5, $80
db $B5, $02
db $71
db $DE, $6F ; custom reward
db $DF
; db $0A                          ;Player Hide
db $CB, $18, $03                ;Clear Flag 2/3/4/5/18 03
; db $E1, $E2, $00, $33, $0D, $00 ;Return from cutscene? E2 00 33 0D 00
; db $D3, $89, $33, $10           ;Sprite 89 set map position 33, 10
; db $C3, $10                     ;Fade in Speed 10
; db $89, $07                     ;Sprite 089 do event 07
; db $CE, $03, $02                ;Play next 02 bytes 03 times
; db $89, $01                     ;Sprite 089 do event Move Up
; db $B5, $8E                     ;Play Sound Effect Treasure chest
; db $BE, $45                     ;Rumble effect of 45 magnitude
; db $F3, $33, $0B, $20           ;Set Map Tiles 33 0B 20
; db $07                          ;<Unknown>
; db $17                          ;Player pose: face left, down hand backward
; db $01                          ;Player Move Up
; db $BE, $40                     ;Rumble effect of 40 magnitude
; db $80, $10                     ;Sprite 080 do event face up, left hand forward
; db $81, $10                     ;Sprite 081 do event face up, left hand forward
; db $82, $10                     ;Sprite 082 do event face up, left hand forward
; db $C7, $06                     ;Play next 06 bytes simultaneously
; db $89, $03                     ;Sprite 089 do event Move Down
; db $80, $03                     ;Sprite 080 do event Move Down
; db $81, $02                     ;Sprite 081 do event Move Right
; db $C7, $08                     ;Play next 08 bytes simultaneously
; db $89, $04                     ;Sprite 089 do event Move Left
; db $80, $03                     ;Sprite 080 do event Move Down
; db $81, $03                     ;Sprite 081 do event Move Down
; db $82, $04                     ;Sprite 082 do event Move Left
; db $89, $22                     ;Sprite 089 do event face down, left hand on head
; db $CF, $04, $06                ;Play next 06 bytes simultaneously 04 times
; db $80, $03                     ;Sprite 080 do event Move Down
; db $81, $03                     ;Sprite 081 do event Move Down
; db $82, $03                     ;Sprite 082 do event Move Down
; db $80, $26                     ;Sprite 080 do event face up, right hand raised out
; db $81, $26                     ;Sprite 081 do event face up, right hand raised out
; db $16                          ;Player pose: face left, standing
; db $B1, $05                     ;Set Player Sprite 05
; db $82, $0A                     ;Sprite 082 do event Hide
; db $09                          ;Player Show
; db $CE, $04, $24                ;Play next 24 bytes 04 times
; db $80, $26                     ;Sprite 080 do event face up, right hand raised out
; db $81, $26                     ;Sprite 081 do event face up, right hand raised out
; db $89, $26                     ;Sprite 089 do event face up, right hand raised out
; db $16                          ;Player pose: face left, standing
; db $B2, $03                     ;Pause for 03 cycles
; db $80, $20                     ;Sprite 080 do event face down, left hand raised out
; db $81, $20                     ;Sprite 081 do event face down, left hand raised out
; db $89, $20                     ;Sprite 089 do event face down, left hand raised out
; db $10                          ;Player pose: face up, left hand forward
; db $B2, $03                     ;Pause for 03 cycles
; db $80, $22                     ;Sprite 080 do event face down, left hand on head
; db $81, $22                     ;Sprite 081 do event face down, left hand on head
; db $89, $22                     ;Sprite 089 do event face down, left hand on head
; db $12                          ;Player pose: face right, standing
; db $B2, $03                     ;Pause for 03 cycles
; db $80, $24                     ;Sprite 080 do event face down, right hand raised in
; db $81, $24                     ;Sprite 081 do event face down, right hand raised in
; db $89, $24                     ;Sprite 089 do event face down, right hand raised in
; db $14                          ;Player pose: face down, left hand forward
; db $B2, $03                     ;Pause for 03 cycles
; db $80, $48                     ;Sprite 080 do event garbage
; db $81, $48                     ;Sprite 081 do event garbage
; db $89, $48                     ;Sprite 089 do event garbage
; db $38                          ;Player pose: face down, squatting
; db $71                          ;Timing
; db $81, $30                     ;Sprite 081 do event face left, head lowered
; db $80, $30                     ;Sprite 080 do event face left, head lowered
; db $89, $30                     ;Sprite 089 do event face left, head lowered
; db $20                          ;Player pose: face down, left hand raised out
; db $81, $0B                     ;Sprite 081 do event 0B
; db $80, $0B                     ;Sprite 080 do event 0B
; db $89, $0B                     ;Sprite 089 do event 0B
; db $0C                          ;<Unknown>
; db $81, $05                     ;Sprite 081 do event Bounce
; db $80, $05                     ;Sprite 080 do event Bounce
; db $89, $05                     ;Sprite 089 do event Bounce
; db $05                          ;Player Bounce in Place
; db $C7, $07                     ;Play next 07 bytes simultaneously
; db $81, $00                     ;Sprite 081 do event Hold
; db $80, $00                     ;Sprite 080 do event Hold
; db $89, $00                     ;Sprite 089 do event Hold
; db $00                          ;Player Hold
; db $70                          ;Timing
; db $81, $0B                     ;Sprite 081 do event 0B
; db $80, $0B                     ;Sprite 080 do event 0B
; db $89, $0B                     ;Sprite 089 do event 0B
; db $0B                          ;<Unknown>
; db $C7, $05                     ;Play next 05 bytes simultaneously
; db $03                          ;Player Move Down
; db $89, $02                     ;Sprite 089 do event Move Right
; db $80, $01                     ;Sprite 080 do event Move Up
; db $81, $0A                     ;Sprite 081 do event Hide
; db $89, $0A                     ;Sprite 089 do event Hide
; db $80, $0A                     ;Sprite 080 do event Hide
; ;db $B7, $00                     ;Add/Remove character 00
; ;db $B7, $09                     ;Add/Remove character 09
; ;db $B7, $0B                     ;Add/Remove character 0B



db $DB                          ;Restore Player status
db $CB, $15, $03                ;Turn off bit 20 at address  0x7e0ab6
db $CB, $16, $03                ;Turn off bit 40 at address  0x7e0ab6
db $CB, $17, $03                ;Turn off bit 80 at address  0x7e0ab6
db $CB, $1B, $03                ;Turn off bit 08 at address  0x7e0ab7
db $CA, $0E, $00                ;Turn on bit 40 at address  0x7e0a55
db $A2, $58                     ;Turn on bit 01 at address 0x7e0a1f
db $A2, $59                     ;Turn on bit 02 at address 0x7e0a1f
db $FF                          ;End Event


padbyte $00
pad $C93D11


; enemy gates right side
org $c98722
db $B1, $02                     ;Set Player Sprite 02
db $04                          ;Player move Left
db $3F                          ;Player pose: face down, looking left, eyes lowered
db $32                          ;Player pose: collapsed, facing left
db $0C                          ;<Unknown>
db $FF                          ;End Event

pad $C9872D



org $C98716
db $B1, $02                     ;Set Player Sprite 02
db $02                          ;Player Move Right
db $40                          ;Player pose: face down, looking right, eyes lowered
db $33                          ;Player pose: collapsed, facing right
db $0C                          ;<Unknown>
db $FF                          ;End Event

pad $C98721