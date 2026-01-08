hirom


; $C8CD0B → $C8CE7E
; Dialogue before & after Hiryuu Plant boss fight


org $C8CD0B



db $03                          ;Player Move Down
db $03                          ;Player Move Down
db $03                          ;Player Move Down
db $70                          ;Very short pause
db $86, $0A                     ;Sprite 086 do event: Hide
db $BD, $1E, $FF                ;Start Event Battle 1E
db $C5, $80
db $B5, $02
db $71
db $DE, $73 ; custom reward
db $DF
db $24                          ;Sprite 080 do event: face down, right hand raised in
db $82, $0A                     ;Sprite 082 do event: Hide
db $80, $0A                     ;Sprite 080 do event: Hide
db $81, $0A                     ;Sprite 081 do event: Hide
db $DB                          ;Restore Player status
db $B4, $2C                     ;Play Background Music Walking the Snowy Mountains
db $CB, $D3, $02                ;Clear Flag 2/3/4/5/D3 02
db $A2, $66                     ;Set Event Flag 066
db $A4, $1D                     ;Set Event Flag 11D
db $CC, $1C                  ;Custom destination flag 1C
db $FF                          ;End Event













; db $03                          ;Player Move Down
; db $B1, $02                     ;Set Player Sprite 02
; db $D3, $80, $93, $16           ;Sprite 80 set map position 93, 16
; db $D3, $81, $93, $16           ;Sprite 81 set map position 93, 16
; db $D3, $82, $93, $16           ;Sprite 82 set map position 93, 16
; db $C7, $06                     ;Play next 06 bytes simultaneously
; db $80, $03                     ;Sprite 080 do event: Move Down
; db $81, $02                     ;Sprite 081 do event: Move Right
; db $82, $04                     ;Sprite 082 do event: Move Left
; db $81, $24                     ;Sprite 081 do event: face down, right hand raised in
; db $82, $24                     ;Sprite 082 do event: face down, right hand raised in
; db $C8, $DD, $04                ;Display Message/Text/Dialogue DD 04
; db $C7, $04                     ;Play next 04 bytes simultaneously
; db $80, $02                     ;Sprite 080 do event: Move Right
; db $82, $03                     ;Sprite 082 do event: Move Down
; db $CF, $02, $04                ;Play next 04 bytes simultaneously 02 times
; db $80, $03                     ;Sprite 080 do event: Move Down
; db $82, $03                     ;Sprite 082 do event: Move Down
; db $80, $3B                     ;Sprite 080 do event: nothing
; db $82, $3D                     ;Sprite 082 do event: face up, both arms raised out
; db $BE, $45                     ;Rumble effect of 45 magnitude
; db $83, $09                     ;Sprite 083 do event: Show
; db $84, $09                     ;Sprite 084 do event: Show
; db $85, $09                     ;Sprite 085 do event: Show
; db $86, $0A                     ;Sprite 086 do event: Hide
; db $83, $01                     ;Sprite 083 do event: Move Up
; db $C7, $04                     ;Play next 04 bytes simultaneously
; db $83, $01                     ;Sprite 083 do event: Move Up
; db $84, $01                     ;Sprite 084 do event: Move Up
; db $83, $10                     ;Sprite 083 do event: face up, left hand forward
; db $84, $10                     ;Sprite 084 do event: face up, left hand forward
; db $85, $10                     ;Sprite 085 do event: face up, left hand forward
; db $BE, $40                     ;Rumble effect of 40 magnitude
; db $80, $4A                     ;Sprite 080 do event: garbage
; db $82, $4A                     ;Sprite 082 do event: garbage
; db $80, $0B                     ;Sprite 080 do event: 0B
; db $82, $0B                     ;Sprite 082 do event: 0B
; db $80, $05                     ;Sprite 080 do event: Bounce
; db $82, $05                     ;Sprite 082 do event: Bounce
; db $C7, $04                     ;Play next 04 bytes simultaneously
; db $80, $00                     ;Sprite 080 do event: Hold
; db $82, $00                     ;Sprite 082 do event: Hold
; db $83, $10                     ;Sprite 083 do event: face up, left hand forward
; db $84, $10                     ;Sprite 084 do event: face up, left hand forward
; db $85, $10                     ;Sprite 085 do event: face up, left hand forward
; db $C8, $DE, $04                ;Display Message/Text/Dialogue DE 04
; db $CE, $14, $0C                ;Play next 0C bytes 14 times
; db $80, $50                     ;Sprite 080 do event: 50
; db $82, $4F                     ;Sprite 082 do event: garbage
; db $B2, $03                     ;Pause for 03 cycles
; db $80, $4F                     ;Sprite 080 do event: garbage
; db $82, $50                     ;Sprite 082 do event: 50
; db $B2, $03                     ;Pause for 03 cycles
; db $80, $05                     ;Sprite 080 do event: Bounce
; db $82, $05                     ;Sprite 082 do event: Bounce
; db $C7, $04                     ;Play next 04 bytes simultaneously
; db $80, $00                     ;Sprite 080 do event: Hold
; db $82, $00                     ;Sprite 082 do event: Hold
; db $80, $43                     ;Sprite 080 do event: face down, looking right, pointing finger right
; db $82, $42                     ;Sprite 082 do event: garbage
; db $70                          ;Very short pause
; db $81, $4A                     ;Sprite 081 do event: garbage
; db $3A                          ;Player pose: face down, surprised
; db $81, $0B                     ;Sprite 081 do event: 0B
; db $0C                          ;<Unknown>
; db $81, $05                     ;Sprite 081 do event: Bounce
; db $05                          ;Player Bounce in Place
; db $C7, $03                     ;Play next 03 bytes simultaneously
; db $81, $00                     ;Sprite 081 do event: Hold
; db $00                          ;Player Hold
; db $81, $0B                     ;Sprite 081 do event: 0B
; db $0B                          ;<Unknown>
; db $C7, $03                     ;Play next 03 bytes simultaneously
; db $81, $02                     ;Sprite 081 do event: Move Right
; db $04                          ;Player move Left
; db $CF, $02, $03                ;Play next 03 bytes simultaneously 02 times
; db $81, $03                     ;Sprite 081 do event: Move Down
; db $03                          ;Player Move Down
; db $81, $03                     ;Sprite 081 do event: Move Down
; db $81, $26                     ;Sprite 081 do event: face up, right hand raised out
; db $81, $3B                     ;Sprite 081 do event: nothing
; db $38                          ;Player pose: face down, squatting
; db $81, $0B                     ;Sprite 081 do event: 0B
; db $0C                          ;<Unknown>
; db $71                          ;Short pause
; db $C7, $04                     ;Play next 04 bytes simultaneously
; db $81, $04                     ;Sprite 081 do event: Move Left
; db $80, $01                     ;Sprite 080 do event: Move Up
; db $81, $3A                     ;Sprite 081 do event: face down, surprised
; db $C7, $03                     ;Play next 03 bytes simultaneously
; db $03                          ;Player Move Down
; db $82, $01                     ;Sprite 082 do event: Move Up
; db $39                          ;Player pose: face down, both arms raised
; db $70                          ;Very short pause
; db $2A                          ;Player pose: face left, left hand raised
; db $81, $3C                     ;Sprite 081 do event: face down, mouth open, shrugging
; db $71                          ;Short pause
; db $80, $05                     ;Sprite 080 do event: Bounce
; db $82, $05                     ;Sprite 082 do event: Bounce
; db $81, $05                     ;Sprite 081 do event: Bounce
; db $05                          ;Player Bounce in Place
; db $C7, $07                     ;Play next 07 bytes simultaneously
; db $04                          ;Player move Left
; db $80, $02                     ;Sprite 080 do event: Move Right
; db $82, $04                     ;Sprite 082 do event: Move Left
; db $81, $02                     ;Sprite 081 do event: Move Right
; db $80, $0B                     ;Sprite 080 do event: 0B
; db $81, $0B                     ;Sprite 081 do event: 0B
; db $82, $0B                     ;Sprite 082 do event: 0B
; db $0B                          ;<Unknown>
; db $71                          ;Short pause
; db $81, $3D                     ;Sprite 081 do event: face up, both arms raised out
; db $D3, $80, $D6, $19           ;Sprite 80 set map position D6, 19
; db $80, $40                     ;Sprite 080 do event: face down, looking right, eyes lowered
; db $70                          ;Very short pause
; db $2B                          ;Player pose: face left, left hand out
; db $D3, $82, $50, $19           ;Sprite 82 set map position 50, 19
; db $82, $41                     ;Sprite 082 do event: face up, sprite becomes symmetrical (maybe shrugging?)
; db $73                          ;Long pause
; db $CE, $08, $0C                ;Play next 0C bytes 08 times
; db $80, $50                     ;Sprite 080 do event: 50
; db $82, $4F                     ;Sprite 082 do event: garbage
; db $B2, $03                     ;Pause for 03 cycles
; db $80, $4F                     ;Sprite 080 do event: garbage
; db $82, $50                     ;Sprite 082 do event: 50
; db $B2, $03                     ;Pause for 03 cycles
; db $80, $24                     ;Sprite 080 do event: face down, right hand raised in
; db $82, $24                     ;Sprite 082 do event: face down, right hand raised in
; db $72                          ;Medium pause
; db $80, $26                     ;Sprite 080 do event: face up, right hand raised out
; db $82, $22                     ;Sprite 082 do event: face down, left hand on head
; db $73                          ;Long pause
; db $C7, $07                     ;Play next 07 bytes simultaneously
; db $03                          ;Player Move Down
; db $82, $02                     ;Sprite 082 do event: Move Right
; db $81, $03                     ;Sprite 081 do event: Move Down
; db $80, $04                     ;Sprite 080 do event: Move Left
; db $12                          ;Player pose: face right, standing
; db $81, $26                     ;Sprite 081 do event: face up, right hand raised out
; db $C8, $DF, $84                ;Display Message/Text/Dialogue DF 84
; db $70                          ;Very short pause
; db $BD, $1E, $FF                ;Start Event Battle 1E
; db $B1, $02                     ;Set Player Sprite 02
; db $C8, $E0, $04                ;Display Message/Text/Dialogue E0 04
; db $C5                          ;<unknown>
; db $E0, $B2                     ;Unknown
; db $04                          ;Player move Left
; db $CE, $14, $14                ;Play next 14 bytes 14 times
; db $83, $09                     ;Sprite 083 do event: Show
; db $84, $09                     ;Sprite 084 do event: Show
; db $85, $09                     ;Sprite 085 do event: Show
; db $86, $0A                     ;Sprite 086 do event: Hide
; db $B2, $02                     ;Pause for 02 cycles
; db $83, $0A                     ;Sprite 083 do event: Hide
; db $84, $0A                     ;Sprite 084 do event: Hide
; db $85, $0A                     ;Sprite 085 do event: Hide
; db $86, $09                     ;Sprite 086 do event: Show
; db $B2, $02                     ;Pause for 02 cycles
; db $72                          ;Medium pause
; db $80, $04                     ;Sprite 080 do event: Move Left
; db $C8, $E1, $04                ;Display Message/Text/Dialogue E1 04
; db $C7, $05                     ;Play next 05 bytes simultaneously
; db $82, $01                     ;Sprite 082 do event: Move Up
; db $01                          ;Player Move Up
; db $81, $04                     ;Sprite 081 do event: Move Left
; db $C7, $05                     ;Play next 05 bytes simultaneously
; db $02                          ;Player Move Right
; db $82, $02                     ;Sprite 082 do event: Move Right
; db $81, $04                     ;Sprite 081 do event: Move Left
; db $81, $20                     ;Sprite 081 do event: face down, left hand raised out
; db $82, $02                     ;Sprite 082 do event: Move Right
; db $82, $24                     ;Sprite 082 do event: face down, right hand raised in
; db $C8, $E2, $04                ;Display Message/Text/Dialogue E2 04
; db $80, $3B                     ;Sprite 080 do event: nothing
; db $73                          ;Long pause
; db $80, $04                     ;Sprite 080 do event: Move Left
; db $86, $0A                     ;Sprite 086 do event: Hide
; db $80, $24                     ;Sprite 080 do event: face down, right hand raised in
; db $B4, $29                     ;Play Background Music Fanfare 1 (short)
; db $C8, $E3, $04                ;Display Message/Text/Dialogue E3 04
; db $E4, $C7                     ;Unknown
; db $05                          ;Player Bounce in Place
; db $82, $03                     ;Sprite 082 do event: Move Down
; db $02                          ;Player Move Right
; db $81, $01                     ;Sprite 081 do event: Move Up
; db $82, $0A                     ;Sprite 082 do event: Hide
; db $80, $0A                     ;Sprite 080 do event: Hide
; db $81, $0A                     ;Sprite 081 do event: Hide
; db $DB                          ;Restore Player status
; db $B4, $2C                     ;Play Background Music Walking the Snowy Mountains
; db $CB, $D3, $02                ;Clear Flag 2/3/4/5/D3 02
; db $A2, $66                     ;Set Event Flag 066
; db $FF                          ;End Event


padbyte $00
pad $C8CE7F