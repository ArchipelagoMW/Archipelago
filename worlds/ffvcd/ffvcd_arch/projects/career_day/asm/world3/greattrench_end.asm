hirom


; Boss of great trench

org $C9C8B7

db $3A                          ;Player pose: face down, surprised
db $0C                          ;<Unknown>
db $06                          ;Player Bounce in Place
db $03                          ;Player Move Down
db $0B                          ;<Unknown>
db $10                          ;Player pose: face up, left hand forward
db $B5, $96                     ;Play Sound Effect Evil disappears
db $83, $09                     ;Sprite 083 do event: Show
db $B5, $96                     ;Play Sound Effect Evil disappears
db $84, $09                     ;Sprite 084 do event: Show
db $B5, $96                     ;Play Sound Effect Evil disappears
db $85, $09                     ;Sprite 085 do event: Show
db $71
db $C7, $06                     ;Play next 06 bytes simultaneously
db $83, $03                     ;Sprite 083 do event: Move Down
db $84, $03                     ;Sprite 084 do event: Move Down
db $85, $03                     ;Sprite 085 do event: Move Down
db $83, $0A                     ;Sprite 083 do event: Hide
db $84, $0A                     ;Sprite 084 do event: Hide
db $85, $0A                     ;Sprite 085 do event: Hide
db $BD, $32, $FF                ;Start Event Battle 32
db $01                          ;Player Move Up
db $01                          ;Player Move Up
db $26                          ;Player pose: face up, right hand raised out
db $82, $0A                     ;Sprite 082 do event: Hide
; db $C8, $54, $07                ;Display Message/Text/Dialogue 54 07
db $71                          ;Short pause
db $14                          ;Player pose: face down, left hand forward
db $20                          ;Player pose: face down, left hand raised out
db $B4, $29                     ;Play Background Music Fanfare 1 (short)
db $DE, $21				; set up reward
db $DF					; call text handler
db $C5, $80
db $B5, $02
db $71
db $DE, $7C ; custom reward
db $DF
db $E4, $B4                     ;Unknown
db $24                          ;Player pose: face down, right hand raised in
; db $A2, $91                     ;Turn on bit 02 at address 0x7e0a26
db $A2, $0E                     ;Turn on bit 40 at address 0x7e0a15
db $CB, $20, $00                ;Turn off bit 01 at address  0x7e0a58
db $CB, $5C, $02                ;Turn off bit 10 at address  0x7e0a9f
db $FF                          ;End Event

padbyte $00
pad $C9C917