hirom


; Lev cutscene with minion destroyed

org $C99EC2

db $B4, $17                     ;Play Background Music Danger!
db $8A, $09                     ;Sprite 08A do event: Show
db $0A                          ;Player Hide
db $77                          ;<Unknown>
db $CE, $07, $01                ;Play next 01 bytes 07 times
db $01                          ;Player Move Up
db $CD, $5B, $06                ;Run event index 065B
db $CE, $07, $01                ;Play next 01 bytes 07 times
db $03                          ;Player Move Down
db $76                          ;<Unknown>
db $10                          ;Player pose: face up, left hand forward
db $09                          ;Player Show
db $8A, $0A                     ;Sprite 08A do event: Hide
db $B5, $4A                     ;Play Sound Effect Tsunami
db $BE, $0A                     ;Rumble effect of 0A magnitude
db $BE, $00                     ;Rumble effect of 00 magnitude
db $A4, $7B                     ;Set Event Flag 17B
db $CB, $5C, $02                ;Clear Flag 2/3/4/5/5C 02
db $FF                          ;End Event


padbyte $00
pad $C99F1D


; Leviathan fight

org $C9BBF8


db $BD, $31, $FF                ;Start Event Battle 31
db $DE, $10				; set up reward
db $DF					; call text handler
db $C5, $80
db $B5, $02
db $71
db $DE, $7F ; custom reward
db $DF
db $CE, $0A, $1C                ;Play next 1C bytes 0A times
db $83, $09                     ;Sprite 083 do event: Show
db $84, $09                     ;Sprite 084 do event: Show
db $85, $09                     ;Sprite 085 do event: Show
db $86, $09                     ;Sprite 086 do event: Show
db $87, $09                     ;Sprite 087 do event: Show
db $88, $09                     ;Sprite 088 do event: Show
db $B2, $02                     ;Pause for 02 cycles
db $83, $0A                     ;Sprite 083 do event: Hide
db $84, $0A                     ;Sprite 084 do event: Hide
db $85, $0A                     ;Sprite 085 do event: Hide
db $86, $0A                     ;Sprite 086 do event: Hide
db $87, $0A                     ;Sprite 087 do event: Hide
db $88, $0A                     ;Sprite 088 do event: Hide
db $B2, $02                     ;Pause for 02 cycles
db $C5                          ;<unknown>
db $80, $BE                     ;Sprite 080 do event: BE
db $00                          ;Player Hold
db $89, $09                     ;Sprite 089 do event: Show
db $C5                          ;<unknown>
db $80, $71                     ;Sprite 080 do event: 71
db $89, $03                     ;Sprite 089 do event: Move Down
db $89, $03                     ;Sprite 089 do event: Move Down
db $89, $0A                     ;Sprite 089 do event: Hide
db $C5                          ;<unknown>
db $80, $39                     ;Sprite 080 do event: face down, both arms raised
db $24                          ;Player pose: face down, right hand raised in
db $A2, $92                     ;Set Event Flag 092
db $FF                          ;End Event


padbyte $00
pad $C9BC3F

org $C9BBDB
db $71                          ;Short pause
db $82, $03                     ;Sprite 082 do event: Move Down
db $82, $0A                     ;Sprite 082 do event: Hide
db $71                          ;Short pause
db $14                          ;Player pose: face down, left hand forward
db $71                          ;Short pause
db $39                          ;Player pose: face down, both arms raised
db $71                          ;Short pause
db $B4, $29                     ;Play Background Music Fanfare 1 (short)
db $E4, $C9                     ;Unknown
db $48                          ;Player pose: garbage
db $0F                          ;<Unknown>
db $A4, $54                     ;Turn on bit 10 at address 0x7e0a3e 
db $CB, $7F, $02                ;Turn off bit 80 at address  0x7e0aa3
; db $A4, $CA                     ;Turn on bit 04 at address 0x7e0a4d (key item)
db $FF                          ;End Event

pad $C9BBF7