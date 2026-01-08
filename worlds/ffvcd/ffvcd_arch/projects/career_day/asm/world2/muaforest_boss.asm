hirom


; Frankly this one's a mess but it does work and I left in the old code in case something needs to be added in later. 
; This handles from starting Guardians boss to going back to world map, skipping a lot in between
; However, for the key item cutscene, Cara has 1 text box, then the world map is given 


; Boss → Waiting for Cara

org $C95FFC



db $CE, $03, $01                ;Play next 01 bytes 03 times
db $01                          ;Player Move Up
db $BE, $05                     ;Rumble effect of 05 magnitude
db $71                          ;Short pause
db $B5, $43                     ;Play Sound Effect Gate opens
db $F3, $10, $16, $72           ;Set Map Tiles 10 16 72
db $79                          ;'The Crash Event'
db $79                          ;'The Crash Event'
db $79                          ;'The Crash Event'
db $11                          ;Player pose: face up, right hand forward
db $11                          ;Player pose: face up, right hand forward
db $11                          ;Player pose: face up, right hand forward
db $11                          ;Player pose: face up, right hand forward
db $11                          ;Player pose: face up, right hand forward
db $11                          ;Player pose: face up, right hand forward
db $11                          ;Player pose: face up, right hand forward
db $11                          ;Player pose: face up, right hand forward
db $11                          ;Player pose: face up, right hand forward
db $11                          ;Player pose: face up, right hand forward
db $11                          ;Player pose: face up, right hand forward
db $11                          ;Player pose: face up, right hand forward
db $11                          ;Player pose: face up, right hand forward
db $11                          ;Player pose: face up, right hand forward
db $11                          ;Player pose: face up, right hand forward
db $11                          ;Player pose: face up, right hand forward
db $11                          ;Player pose: face up, right hand forward
db $11                          ;Player pose: face up, right hand forward
db $11                          ;Player pose: face up, right hand forward
db $11                          ;Player pose: face up, right hand forward
db $11                          ;Player pose: face up, right hand forward
db $71                          ;Short pause
db $BE, $00                     ;Rumble effect of 00 magnitude
db $14                          ;Player pose: face down, left hand forward
db $73                          ;Long pause
db $CE, $05, $01                ;Play next 01 bytes 05 times
db $01                          ;Player Move Up
db $71                          ;Short pause
db $92, $09                     ;Sprite 192 do event: Show
db $0A                          ;Player Hide
db $94, $09                     ;Sprite 194 do event: Show
db $93, $09                     ;Sprite 193 do event: Show
db $95, $09                     ;Sprite 195 do event: Show
db $C7, $06                     ;Play next 06 bytes simultaneously
db $94, $02                     ;Sprite 194 do event: Move Right
db $95, $04                     ;Sprite 195 do event: Move Left
db $93, $03                     ;Sprite 193 do event: Move Down
db $94, $20                     ;Sprite 194 do event: face down, left hand raised out
db $95, $20                     ;Sprite 195 do event: face down, left hand raised out
db $93, $20                     ;Sprite 193 do event: face down, left hand raised out
db $8D, $11                     ;Sprite 08D do event: face up, right hand forward
db $8E, $11                     ;Sprite 08E do event: face up, right hand forward
db $8F, $11                     ;Sprite 08F do event: face up, right hand forward
db $90, $11                     ;Sprite 190 do event: face up, right hand forward
db $C5                          ;<unknown>
db $20                          ;Player pose: face down, left hand raised out
db $C7, $08                     ;Play next 08 bytes simultaneously
db $8D, $03                     ;Sprite 08D do event: Move Down
db $8E, $03                     ;Sprite 08E do event: Move Down
db $8F, $03                     ;Sprite 08F do event: Move Down
db $90, $03                     ;Sprite 190 do event: Move Down
db $C5                          ;<unknown>
db $20                          ;Player pose: face down, left hand raised out
db $C7, $08                     ;Play next 08 bytes simultaneously
db $8D, $03                     ;Sprite 08D do event: Move Down
db $8E, $03                     ;Sprite 08E do event: Move Down
db $8F, $03                     ;Sprite 08F do event: Move Down
db $90, $03                     ;Sprite 190 do event: Move Down
db $C5                          ;<unknown>
db $20                          ;Player pose: face down, left hand raised out
db $C5                          ;<unknown>
db $20                          ;Player pose: face down, left hand raised out
db $C5                          ;<unknown>
db $20                          ;Player pose: face down, left hand raised out
db $8D, $13                     ;Sprite 08D do event: face right, down hand backward
db $8E, $13                     ;Sprite 08E do event: face right, down hand backward
db $8F, $13                     ;Sprite 08F do event: face right, down hand backward
db $90, $13                     ;Sprite 190 do event: face right, down hand backward
db $CF, $02, $08                ;Play next 08 bytes simultaneously 02 times
db $8D, $03                     ;Sprite 08D do event: Move Down
db $8E, $04                     ;Sprite 08E do event: Move Left
db $8F, $02                     ;Sprite 08F do event: Move Right
db $90, $03                     ;Sprite 190 do event: Move Down
db $CF, $02, $08                ;Play next 08 bytes simultaneously 02 times
db $8D, $03                     ;Sprite 08D do event: Move Down
db $8E, $03                     ;Sprite 08E do event: Move Down
db $8F, $03                     ;Sprite 08F do event: Move Down
db $90, $03                     ;Sprite 190 do event: Move Down
db $C7, $04                     ;Play next 04 bytes simultaneously
db $8E, $03                     ;Sprite 08E do event: Move Down
db $8F, $03                     ;Sprite 08F do event: Move Down
db $95, $26                     ;Sprite 195 do event: face up, right hand raised out
db $92, $26                     ;Sprite 192 do event: face up, right hand raised out
db $94, $22                     ;Sprite 194 do event: face down, left hand on head
db $93, $22                     ;Sprite 193 do event: face down, left hand on head
db $CF, $02, $08                ;Play next 08 bytes simultaneously 02 times
db $8D, $02                     ;Sprite 08D do event: Move Right
db $8E, $02                     ;Sprite 08E do event: Move Right
db $8F, $04                     ;Sprite 08F do event: Move Left
db $90, $04                     ;Sprite 190 do event: Move Left
db $93, $20                     ;Sprite 193 do event: face down, left hand raised out
db $94, $20                     ;Sprite 194 do event: face down, left hand raised out
db $95, $20                     ;Sprite 195 do event: face down, left hand raised out
db $92, $20                     ;Sprite 192 do event: face down, left hand raised out
db $8D, $0A                     ;Sprite 08D do event: Hide
db $8E, $0A                     ;Sprite 08E do event: Hide
db $8F, $0A                     ;Sprite 08F do event: Hide
db $90, $0A                     ;Sprite 190 do event: Hide
db $BD, $21, $FF                ;Start Event Battle 21
db $C5, $80
db $B5, $02
db $71
db $DE, $76 ; custom reward
db $DF
db $71
db $C4, $02
db $A2, $75                     ;Turn on bit 20 at address 0x7e0a22
db $E3, $67, $01, $93, $12, $00 ;Inter-map cutscene? 67 01 93 12 00
db $CD, $40, $04                ;Run event index 0440
db $88, $09                     ;Sprite 088 do event: Show
db $88, $24                     ;Sprite 088 do event: face down, right hand raised in
db $0A                          ;Player Hide
db $B4, $30                     ;Play Background Music The Day Will Come
; db $D3, $82, $93, $0F           ;Sprite 82 set map position 93, 0F
; db $D3, $83, $93, $11           ;Sprite 83 set map position 93, 11
; db $D3, $85, $93, $11           ;Sprite 85 set map position 93, 11
db $C3, $02                     ;Fade in Speed 08
db $74
; db $B3, $10                     ;Pause for 100 cycles
; db $CD, $73, $07                ;Run event index 0773
; db $88, $02                     ;Sprite 088 do event: Move Right
; db $88, $04                     ;Sprite 088 do event: Move Left
; db $88, $04                     ;Sprite 088 do event: Move Left
; db $CD, $73, $07                ;Run event index 0773
; db $88, $20                     ;Sprite 088 do event: face down, left hand raised out
; db $B4, $30                     ;Play Background Music The Day Will Come
; db $CD, $88, $07                ;Run event index 0788
; db $CD, $73, $07                ;Run event index 0773
; db $88, $03                     ;Sprite 088 do event: Move Down
; db $88, $03                     ;Sprite 088 do event: Move Down
; db $88, $3E                     ;Sprite 088 do event: face up, both arms raised in
; db $88, $24                     ;Sprite 088 do event: face down, right hand raised in
; db $86, $01                     ;Sprite 086 do event: Move Up
; db $C5                          ;<unknown>
; db $40                          ;Player pose: face down, looking right, eyes lowered
; db $86, $0A                     ;Sprite 086 do event: Hide
; db $C5                          ;<unknown>
; db $40                          ;Player pose: face down, looking right, eyes lowered
; db $C5                          ;<unknown>
; db $40                          ;Player pose: face down, looking right, eyes lowered
db $C8, $E2, $05                ;Display Message/Text/Dialogue E2 05
db $C4, $02
db $75
db $A5, $FE                     ;Clear Event Flag 1FE
db $E1, $01, $20, $38, $79, $6C ;Return from cutscene? 01 20 38 79 6C
db $B7, $0C                     ;Add/Remove character 0C
db $76                          ;<Unknown>
; db $A4, $25                     ;Turn on bit 20 at address 0x7e0a38
db $CB, $0E, $00                ;Turn off bit 40 at address  0x7e0a55
db $CA, $0F, $00                ;Turn on bit 80 at address  0x7e0a55
db $CB, $1A, $03                ;Turn off bit 04 at address  0x7e0ab7
db $CB, $44, $02                ;Turn off bit 10 at address  0x7e0a9c
db $CB, $45, $02                ;Turn off bit 20 at address  0x7e0a9c
db $CB, $46, $02                ;Turn off bit 40 at address  0x7e0a9c
db $CB, $47, $02                ;Turn off bit 80 at address  0x7e0a9c
db $CB, $48, $02                ;Turn off bit 01 at address  0x7e0a9d
db $CB, $7B, $02                ;Turn off bit 08 at address  0x7e0aa3
db $CA, $49, $02                ;Turn on bit 02 at address  0x7e0a9d
db $CA, $4A, $02                ;Turn on bit 04 at address  0x7e0a9d
db $CA, $4B, $02                ;Turn on bit 08 at address  0x7e0a9d
db $CA, $4C, $02                ;Turn on bit 10 at address  0x7e0a9d
db $CA, $4D, $02                ;Turn on bit 20 at address  0x7e0a9d

; arch - reset forest status for re-entry
db $A5, $EC                     
db $A3, $74                     


; new flag for cara joining
db $A2, $C6            ; set address 000A2C bit ON 40

db $09                          ;Player Show
db $C3, $02
db $14                          ;Player pose: face down, left hand forward
db $CC, $23                  ;Custom destination flag 23
db $A4, $45					; Trigger for Exdeath cutscene
db $E1, $01, $00, $2E, $8B, $00 ;Return from cutscene? 00 00 9C 96 00
db $D2, $01, $2E, $8A, $D8


; db $EB, $FF                     ;DISABLED FOR NOW - believed to reset Cara's state to Freelancer
db $FF

padbyte $00
pad $C96861
