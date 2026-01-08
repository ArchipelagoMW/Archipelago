hirom


org $C83BDB
db $B0, $00, $F9

; World 2 Warp Dialogue
org $F900B0

; ; TESTING MUSIC ONLY
; db $B4, $19

; db $FF
db $F0, $01, $02              ;Conditional yes/no dialogue at 04B7
db $CD, $C6, $06                ;Run event index 0408
db $FF
db $FF




; Change first warp to void scene 
org $C84772
db $00, $02, $F9

; world 2 warp
org $F90200
; change world flag to WORLD 2
db $A3, $C8 ; off
db $A2, $C9 ; on
db $A3, $CA ; off

db $C5, $80                     ;<unknown>
db $B5, $02                     ;Play Sound Effect Void, Image
db $C4, $06
db $71
db $E1, $01, $00, $4C, $6F, $00 ;Return from cutscene? E1 00 97 1A 00
db $ED, $01, $AC, $A5, $6C ; hiryuu CONDITIONAL
db $ED, $01, $AD, $A5, $90 ; submarine CONDITIONAL
db $D2, $01, $4D, $6F, $D8 ; airship ???

; WORLD CONDITIONALS
; Set world 3 off status
db $A3, $79            ; set address 000A23 bit OFF 02
; Submarine deactivated
db $A5, $F9            ; set address 000A53 bit OFF 02
; Lonka de-access
db $A5, $FA            ; set address 000A53 bit OFF 04

db $EE
db $14
db $C3, $06
db $71
db $FF

; Warp message world 2
org $E191EA
db $76, $7A, $8B, $89, $96, $8D, $88, $96, $76, $88, $8B, $85, $7D, $96, $55, $A2
db $FF, $00