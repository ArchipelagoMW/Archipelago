hirom


; $C9B456 → $C9B48D
; Place tablet

org $C9B456

db $CD, $E2, $05                ;Run event index 05E2
db $A2, $97                     ;Set Event Flag 097
db $FF                          ;End Event


padbyte $00
pad $C9B467

; Remove "One of the 12 legendary weapons..."

org $C84A14
db $00, $00, $00





; the below hacks are postponed
; there's weirdness with these needing to be in the exact position, where even padding messes them up big time





; If you want to replace these you need to:
; 1) Hack the text dynamically for 12 Kuzar in bank $E1 for these randomized items
; 2) Put the standard $DE, $xx code in
; 3) You can possibly ignore the $DF command because the player already knows the item from above, which will give you perfect space. Otherwise youll bleed too many commands 
; 4) If you do want it all, then you can cut out the $C7, $03 simultaneous. 


; db $DE, $00
; db $DF

org $C9B750
db $3D                          ;Player pose: face up, both arms raised out
db $86, $07                     ;Sprite 086 do event: 07
db $86, $08                     ;Sprite 086 do event: 08
db $0C                          ;<Unknown>
db $C7, $03                     ;Play next 03 bytes simultaneously
db $03                          ;Player Move Down
db $86, $03                     ;Sprite 086 do event: Move Down
db $39                          ;Player pose: face down, both arms raised
db $70                          ;Very short pause
db $86, $01                     ;Sprite 086 do event: Move Up
db $CD, $B1, $06                ;Run event index 06B1
db $86, $13                     ;Sprite 086 do event: face right, down hand backward
db $05                          ;Player Bounce in Place
db $C7, $03                     ;Play next 03 bytes simultaneously
db $00                          ;Player Hold
db $86, $03                     ;Sprite 086 do event: Move Down
db $86, $0A                     ;Sprite 086 do event: Hide
db $CD, $B2, $06                ;Run event index 06B2
db $DE, $2B				; set up reward


db $CB, $24, $01                ;Clear Flag 2/3/4/5/24 01
db $FF                          ;End Event

pad $C9B774

org $C9B775
db $3D                          ;Player pose: face up, both arms raised out
db $87, $07                     ;Sprite 087 do event: 07
db $87, $08                     ;Sprite 087 do event: 08
db $0C                          ;<Unknown>
db $C7, $03                     ;Play next 03 bytes simultaneously
db $03                          ;Player Move Down
db $87, $03                     ;Sprite 087 do event: Move Down
db $2A                          ;Player pose: face left, left hand raised
db $B2, $05                     ;Pause for 05 cycles
db $39                          ;Player pose: face down, both arms raised
db $70                          ;Very short pause
db $87, $01                     ;Sprite 087 do event: Move Up
db $CD, $B1, $06                ;Run event index 06B1
db $87, $13                     ;Sprite 087 do event: face right, down hand backward
db $05                          ;Player Bounce in Place
db $C7, $03                     ;Play next 03 bytes simultaneously
db $00                          ;Player Hold
db $87, $03                     ;Sprite 087 do event: Move Down
db $87, $0A                     ;Sprite 087 do event: Hide
db $CD, $B2, $06                ;Run event index 06B2
db $DE, $29                     ;Add Item Assassin Dagger
db $CB, $25, $01                ;Clear Flag 2/3/4/5/25 01
db $FF                          ;End Event

pad $C9B79C
org $C9B79D
db $3D                          ;Player pose: face up, both arms raised out
db $88, $07                     ;Sprite 088 do event: 07
db $88, $08                     ;Sprite 088 do event: 08
db $0C                          ;<Unknown>
db $C7, $03                     ;Play next 03 bytes simultaneously
db $03                          ;Player Move Down
db $88, $03                     ;Sprite 088 do event: Move Down
db $2A                          ;Player pose: face left, left hand raised
db $B2, $05                     ;Pause for 05 cycles
db $39                          ;Player pose: face down, both arms raised
db $70                          ;Very short pause
db $88, $01                     ;Sprite 088 do event: Move Up
db $CD, $B1, $06                ;Run event index 06B1
db $88, $13                     ;Sprite 088 do event: face right, down hand backward
db $05                          ;Player Bounce in Place
db $C7, $03                     ;Play next 03 bytes simultaneously
db $00                          ;Player Hold
db $88, $03                     ;Sprite 088 do event: Move Down
db $88, $0A                     ;Sprite 088 do event: Hide
db $CD, $B2, $06                ;Run event index 06B2
db $DE, $33				; set up reward
db $CB, $26, $01                ;Clear Flag 2/3/4/5/26 01
db $FF                          ;End Event

pad $C9B7C4
org $C9B7C5
db $3D                          ;Player pose: face up, both arms raised out
db $89, $07                     ;Sprite 089 do event: 07
db $89, $08                     ;Sprite 089 do event: 08
db $0C                          ;<Unknown>
db $C7, $03                     ;Play next 03 bytes simultaneously
db $03                          ;Player Move Down
db $89, $03                     ;Sprite 089 do event: Move Down
db $2A                          ;Player pose: face left, left hand raised
db $B2, $05                     ;Pause for 05 cycles
db $39                          ;Player pose: face down, both arms raised
db $70                          ;Very short pause
db $89, $01                     ;Sprite 089 do event: Move Up
db $CD, $B1, $06                ;Run event index 06B1
db $89, $13                     ;Sprite 089 do event: face right, down hand backward
db $05                          ;Player Bounce in Place
db $C7, $03                     ;Play next 03 bytes simultaneously
db $00                          ;Player Hold
db $89, $03                     ;Sprite 089 do event: Move Down
db $89, $0A                     ;Sprite 089 do event: Hide
db $CD, $B2, $06                ;Run event index 06B2
db $DE, $2E				; set up reward
db $CB, $27, $01                ;Clear Flag 2/3/4/5/27 01
db $FF                          ;End Event

pad $C9B7EC
org $C9B7ED
db $3D                          ;Player pose: face up, both arms raised out
db $8A, $07                     ;Sprite 08A do event: 07
db $8A, $08                     ;Sprite 08A do event: 08
db $0C                          ;<Unknown>
db $C7, $03                     ;Play next 03 bytes simultaneously
db $03                          ;Player Move Down
db $8A, $03                     ;Sprite 08A do event: Move Down
db $2A                          ;Player pose: face left, left hand raised
db $B2, $05                     ;Pause for 05 cycles
db $39                          ;Player pose: face down, both arms raised
db $70                          ;Very short pause
db $8A, $01                     ;Sprite 08A do event: Move Up
db $CD, $B1, $06                ;Run event index 06B1
db $8A, $13                     ;Sprite 08A do event: face right, down hand backward
db $05                          ;Player Bounce in Place
db $C7, $03                     ;Play next 03 bytes simultaneously
db $00                          ;Player Hold
db $8A, $03                     ;Sprite 08A do event: Move Down
db $8A, $0A                     ;Sprite 08A do event: Hide
db $CD, $B2, $06                ;Run event index 06B2
db $DE, $31				; set up reward
db $CB, $28, $01                ;Clear Flag 2/3/4/5/28 01
db $FF                          ;End Event

pad $C9B814
org $C9B815
db $3D                          ;Player pose: face up, both arms raised out
db $8B, $07                     ;Sprite 08B do event: 07
db $8B, $08                     ;Sprite 08B do event: 08
db $0C                          ;<Unknown>
db $C7, $03                     ;Play next 03 bytes simultaneously
db $03                          ;Player Move Down
db $8B, $03                     ;Sprite 08B do event: Move Down
db $2A                          ;Player pose: face left, left hand raised
db $B2, $05                     ;Pause for 05 cycles
db $39                          ;Player pose: face down, both arms raised
db $70                          ;Very short pause
db $8B, $01                     ;Sprite 08B do event: Move Up
db $CD, $B1, $06                ;Run event index 06B1
db $8B, $13                     ;Sprite 08B do event: face right, down hand backward
db $05                          ;Player Bounce in Place
db $C7, $03                     ;Play next 03 bytes simultaneously
db $00                          ;Player Hold
db $8B, $03                     ;Sprite 08B do event: Move Down
db $8B, $0A                     ;Sprite 08B do event: Hide
db $CD, $B2, $06                ;Run event index 06B2
db $DE, $2F 			; set up reward
db $CB, $29, $01                ;Clear Flag 2/3/4/5/29 01
db $FF                          ;End Event

pad $C9B83C
org $C9B83D
db $3D                          ;Player pose: face up, both arms raised out
db $8C, $07                     ;Sprite 08C do event: 07
db $8C, $08                     ;Sprite 08C do event: 08
db $0C                          ;<Unknown>
db $C7, $03                     ;Play next 03 bytes simultaneously
db $03                          ;Player Move Down
db $8C, $03                     ;Sprite 08C do event: Move Down
db $2A                          ;Player pose: face left, left hand raised
db $B2, $05                     ;Pause for 05 cycles
db $39                          ;Player pose: face down, both arms raised
db $70                          ;Very short pause
db $8C, $01                     ;Sprite 08C do event: Move Up
db $CD, $B1, $06                ;Run event index 06B1
db $8C, $13                     ;Sprite 08C do event: face right, down hand backward
db $05                          ;Player Bounce in Place
db $C7, $03                     ;Play next 03 bytes simultaneously
db $00                          ;Player Hold
db $8C, $03                     ;Sprite 08C do event: Move Down
db $8C, $0A                     ;Sprite 08C do event: Hide
db $CD, $B2, $06                ;Run event index 06B2
db $DE, $34				; set up reward
db $CB, $2A, $01                ;Clear Flag 2/3/4/5/2A 01
db $FF                          ;End Event

pad $C9B864
org $C9B865
db $3D                          ;Player pose: face up, both arms raised out
db $8D, $07                     ;Sprite 08D do event: 07
db $8D, $08                     ;Sprite 08D do event: 08
db $0C                          ;<Unknown>
db $C7, $03                     ;Play next 03 bytes simultaneously
db $03                          ;Player Move Down
db $8D, $03                     ;Sprite 08D do event: Move Down
db $2A                          ;Player pose: face left, left hand raised
db $B2, $05                     ;Pause for 05 cycles
db $39                          ;Player pose: face down, both arms raised
db $70                          ;Very short pause
db $8D, $01                     ;Sprite 08D do event: Move Up
db $CD, $B1, $06                ;Run event index 06B1
db $8D, $13                     ;Sprite 08D do event: face right, down hand backward
db $05                          ;Player Bounce in Place
db $C7, $03                     ;Play next 03 bytes simultaneously
db $00                          ;Player Hold
db $8D, $03                     ;Sprite 08D do event: Move Down
db $8D, $0A                     ;Sprite 08D do event: Hide
db $CD, $B2, $06                ;Run event index 06B2
db $DE, $2C				; set up reward
db $CB, $2B, $01                ;Clear Flag 2/3/4/5/2B 01
db $FF                          ;End Event

pad $C9B88C
org $C9B88D
db $3D                          ;Player pose: face up, both arms raised out
db $8E, $07                     ;Sprite 08E do event: 07
db $8E, $08                     ;Sprite 08E do event: 08
db $0C                          ;<Unknown>
db $C7, $03                     ;Play next 03 bytes simultaneously
db $03                          ;Player Move Down
db $8E, $03                     ;Sprite 08E do event: Move Down
db $2A                          ;Player pose: face left, left hand raised
db $B2, $05                     ;Pause for 05 cycles
db $39                          ;Player pose: face down, both arms raised
db $70                          ;Very short pause
db $8E, $01                     ;Sprite 08E do event: Move Up
db $CD, $B1, $06                ;Run event index 06B1
db $8E, $13                     ;Sprite 08E do event: face right, down hand backward
db $05                          ;Player Bounce in Place
db $C7, $03                     ;Play next 03 bytes simultaneously
db $00                          ;Player Hold
db $8E, $03                     ;Sprite 08E do event: Move Down
db $8E, $0A                     ;Sprite 08E do event: Hide
db $CD, $B2, $06                ;Run event index 06B2
db $DE, $32				; set up reward

db $CB, $2C, $01                ;Turn off bit 10 at address  0x7e0a79
db $FF                          ;End Event

pad $C9B8B4
org $C9B8B5
db $3D                          ;Player pose: face up, both arms raised out
db $8F, $07                     ;Sprite 08F do event: 07
db $8F, $08                     ;Sprite 08F do event: 08
db $0C                          ;<Unknown>
db $C7, $03                     ;Play next 03 bytes simultaneously
db $03                          ;Player Move Down
db $8F, $03                     ;Sprite 08F do event: Move Down
db $2A                          ;Player pose: face left, left hand raised
db $B2, $05                     ;Pause for 05 cycles
db $39                          ;Player pose: face down, both arms raised
db $70                          ;Very short pause
db $8F, $01                     ;Sprite 08F do event: Move Up
db $CD, $B1, $06                ;Run event index 06B1
db $8F, $13                     ;Sprite 08F do event: face right, down hand backward
db $05                          ;Player Bounce in Place
db $C7, $03                     ;Play next 03 bytes simultaneously
db $00                          ;Player Hold
db $8F, $03                     ;Sprite 08F do event: Move Down
db $8F, $0A                     ;Sprite 08F do event: Hide
db $CD, $B2, $06                ;Run event index 06B2
db $DE, $30				; set up reward
db $CB, $2D, $01                ;Clear Flag 2/3/4/5/2D 01
db $FF                          ;End Event

pad $C9B8DC
org $C9B8DD
db $3D                          ;Player pose: face up, both arms raised out
db $90, $07                     ;Sprite 190 do event: 07
db $90, $08                     ;Sprite 190 do event: 08
db $0C                          ;<Unknown>
db $C7, $03                     ;Play next 03 bytes simultaneously
db $03                          ;Player Move Down
db $90, $03                     ;Sprite 190 do event: Move Down
db $2A                          ;Player pose: face left, left hand raised
db $B2, $05                     ;Pause for 05 cycles
db $39                          ;Player pose: face down, both arms raised
db $70                          ;Very short pause
db $90, $01                     ;Sprite 190 do event: Move Up
db $CD, $B1, $06                ;Run event index 06B1
db $90, $13                     ;Sprite 190 do event: face right, down hand backward
db $05                          ;Player Bounce in Place
db $C7, $03                     ;Play next 03 bytes simultaneously
db $00                          ;Player Hold
db $90, $03                     ;Sprite 190 do event: Move Down
db $90, $0A                     ;Sprite 190 do event: Hide
db $CD, $B2, $06                ;Run event index 06B2
db $DE, $2A				; set up reward
db $CB, $2E, $01                ;Clear Flag 2/3/4/5/2E 01
db $FF                          ;End Event

pad $C9B904
org $C9B905
db $3D                          ;Player pose: face up, both arms raised out
db $91, $07                     ;Sprite 191 do event: 07
db $91, $08                     ;Sprite 191 do event: 08
db $0C                          ;<Unknown>
db $C7, $03                     ;Play next 03 bytes simultaneously
db $03                          ;Player Move Down
db $91, $03                     ;Sprite 191 do event: Move Down
db $2A                          ;Player pose: face left, left hand raised
db $B2, $05                     ;Pause for 05 cycles
db $39                          ;Player pose: face down, both arms raised
db $70                          ;Very short pause
db $91, $01                     ;Sprite 191 do event: Move Up
db $CD, $B1, $06                ;Run event index 06B1
db $91, $13                     ;Sprite 191 do event: face right, down hand backward
db $05                          ;Player Bounce in Place
db $C7, $03                     ;Play next 03 bytes simultaneously
db $00                          ;Player Hold
db $91, $03                     ;Sprite 191 do event: Move Down
db $91, $0A                     ;Sprite 191 do event: Hide
db $CD, $B2, $06                ;Run event index 06B2
db $DE, $2D				; set up reward
db $CB, $2F, $01                ;Clear Flag 2/3/4/5/2F 01
db $FF                          ;End Event

pad $C9B92C
org $C9B92D







; animations

org $C9C722
db $D8, $14, $0E, $D8           ;Unknown
db $55                  ;Player or Sprite Pose
db $0E                          ;<Unknown>
db $D8, $96, $0E, $C7           ;Unknown
db $06                          ;Player Bounce in Place
db $94, $04                     ;Sprite 194 do event: Move Left
db $95, $01                     ;Sprite 195 do event: Move Up
db $96, $02                     ;Sprite 196 do event: Move Right
db $00                          ;Very short pause
db $C7, $06                     ;Play next 06 bytes simultaneously
db $94, $01                     ;Sprite 194 do event: Move Up
db $95, $02                     ;Sprite 195 do event: Move Right
db $96, $03                     ;Sprite 196 do event: Move Down
db $CF, $02, $06                ;Play next 06 bytes simultaneously 02 times
db $94, $02                     ;Sprite 194 do event: Move Right
db $95, $03                     ;Sprite 195 do event: Move Down
db $96, $04                     ;Sprite 196 do event: Move Left
db $D8, $14, $1E, $D8           ;Unknown
db $15                          ;Player pose: face down, right hand forward
db $0F                          ;<Unknown>
db $D8, $16, $FE, $B2           ;Unknown
db $02                          ;Player Move Right
db $D8, $14, $1F, $D8           ;Unknown
db $15                          ;Player pose: face down, right hand forward
db $FF                          ;End Event




org $C9C756
db $D8, $16, $FD, $B2           ;Unknown
db $02                          ;Player Move Right
db $B5, $02                     ;Play Sound Effect Void, Image
db $D8, $14, $0F, $D8           ;Unknown
db $15                          ;Player pose: face down, right hand forward
db $FE                          ;Noop
db $D8, $16, $0D, $B2           ;Unknown
db $02                          ;Player Move Right
db $D8, $14, $ED, $D8           ;Unknown
db $12                          ;Player pose: face right, standing
db $FE                          ;Noop
db $D8, $15, $0D, $D8           ;Unknown
db $16                          ;Player pose: face left, standing
db $1E                          ;Player pose: face right, standing
db $00, $00
db $D8, $14, $DC, $D8           ;Unknown
db $12                          ;Player pose: face right, standing
db $ED                          ;Noop
db $D8, $17, $FE, $D8           ;Unknown
db $15                          ;Player pose: face down, right hand forward
db $1D                          ;Player pose: face up, walking, right hand forward
db $D8, $16, $1F, $B2           ;Unknown
db $02                          ;Player Move Right
db $D8, $14, $CB, $D8           ;Unknown
db $12                          ;Player pose: face right, standing
db $DC, $D8, $17, $ED           ;Unknown
db $D8, $15, $1E, $D8           ;Unknown
db $16                          ;Player pose: face left, standing
db $0F                          ;<Unknown>
db $00, $00
db $D8, $14, $BA, $D8           ;Unknown
db $12                          ;Player pose: face right, standing
db $CB, $D8, $17                ;Clear Flag 2/3/4/5/D8 17
db $DC, $D8, $15, $1F           ;Unknown
db $D8, $16, $FF, $B2           ;Unknown
db $02                          ;Player Move Right
db $D8, $14, $A9, $D8           ;Unknown
db $12                          ;Player pose: face right, standing
db $ba
db $D8, $17, $CB, $D8           ;Unknown
db $15                          ;Player pose: face down, right hand forward
db $0F                          ;<Unknown>
db $D8, $16, $FE, $B2           ;Unknown
db $02                          ;Player Move Right
db $B5, $02                     ;Play Sound Effect Void, Image
db $D3, $94, $02, $02           ;Sprite 94 set map position 02, 02
db $D8, $12, $A9, $D8           ;Unknown
db $17                          ;Player pose: face left, down hand backward
db $ba
db $D8, $15, $FF, $D8           ;Unknown
db $16                          ;Player pose: face left, standing
db $FD                          ;Noop
db $00, $00
db $D8, $17, $A9, $D8           ;Unknown
db $15                          ;Player pose: face down, right hand forward
db $2C                          ;Player pose: face right, right hand raised
db $D8, $12, $1D, $D8           ;Unknown
db $16                          ;Player pose: face left, standing
db $FE                          ;Noop
db $00, $00
db $D8, $15, $3B, $D8           ;Unknown
db $12                          ;Player pose: face right, standing
db $2C                          ;Player pose: face right, right hand raised
db $D8, $17, $1D, $D8           ;Unknown
db $16                          ;Player pose: face left, standing
db $FD                          ;Noop
db $00, $00
db $D8, $15, $4A, $D8           ;Unknown
db $12                          ;Player pose: face right, standing
db $3B                          ;Player pose: nothing
db $D8, $17, $2C, $D8           ;Unknown
db $16                          ;Player pose: face left, standing
db $0D                          ;<Unknown>
db $00, $00
db $D8, $15, $59, $D8           ;Unknown
db $12                          ;Player pose: face right, standing
db $4A                          ;Player pose: garbage
db $D8, $17, $3B, $D8           ;Unknown
db $16                          ;Player pose: face left, standing
db $1E                          ;Player pose: face right, standing
db $00, $00
db $B5, $02                     ;Play Sound Effect Void, Image
db $D3, $95, $02, $02           ;Sprite 95 set map position 02, 02
db $D8, $12, $59, $D8           ;Unknown
db $17                          ;Player pose: face left, down hand backward
db $4A                          ;Player pose: garbage
db $D8, $16, $0F, $B2           ;Unknown
db $02                          ;Player Move Right
db $D8, $17, $59, $D8           ;Unknown
db $16                          ;Player pose: face left, standing
db $0C                          ;<Unknown>
db $D8, $12, $0D, $B2           ;Unknown
db $02                          ;Player Move Right
db $D8, $16, $0B, $D8           ;Unknown
db $12                          ;Player pose: face right, standing
db $0C                          ;<Unknown>
db $D8, $17, $0D, $B2           ;Unknown
db $02                          ;Player Move Right
db $D8, $16, $0A, $D8           ;Unknown
db $12                          ;Player pose: face right, standing
db $0B                          ;<Unknown>
db $D8, $17, $0C, $B2           ;Unknown
db $02                          ;Player Move Right
db $D8, $16, $09, $D8           ;Unknown
db $12                          ;Player pose: face right, standing
db $0A                          ;Player Hide
db $D8, $17, $0B, $B2           ;Unknown
db $02                          ;Player Move Right
db $D3, $96, $02, $02           ;Sprite 96 set map position 02, 02
db $D8, $12, $09, $D8           ;Unknown
db $17                          ;Player pose: face left, down hand backward
db $0A                          ;Player Hide
db $00, $00
db $D3, $92, $02, $02           ;Sprite 92 set map position 02, 02
db $D8, $17, $09, $B2           ;Unknown
db $05                          ;Player Bounce in Place
db $D3, $97, $02, $02           ;Sprite 97 set map position 02, 02
db $C5                          ;<unknown>
db $E0, $73                     ;Unknown
db $38                          ;Player pose: face down, squatting
db $00                          ;Very short pause
db $20                          ;Player pose: face down, left hand raised out
db $FF                          ;End Event



; remove unsetting of key items in key item inventory
org $C9B5A6
db $00, $00
org $C9B5AE
db $00, $00
org $C9B5B6
db $00, $00
org $C9B5BE
db $00, $00

; speed up get item cutscene
org $C9C863
db $0B                          ;<Unknown>
; db $B4, $29                     ;Play Background Music Fanfare 1 (short)
db $24                          ;Player pose: face down, right hand raised in

db $FF                          ;End Event
