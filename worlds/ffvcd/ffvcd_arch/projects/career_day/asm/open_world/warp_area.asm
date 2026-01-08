hirom


; overwrite pyramid quicksand discovery cutscene 
; corresponds to LDX #$003A, refer to UseableItemEE, which results in this cutscene 
org $C88F0C
db $C5, $80                     ;<unknown>
db $B5, $02                     ;Play Sound Effect Void, Image
db $72
db $C4, $06
db $71
db $E1, $FE, $01, $03, $13, $00 ;Return from cutscene? 00 00 9C 96 00

; this disables all timer related events 
db $CB, $38, $05
db $CB, $39, $05
db $CB, $3a, $05
db $CB, $3b, $05
db $CB, $3c, $05
db $CB, $3d, $05
db $CB, $3e, $05
db $CB, $3f, $05

; reset submarine bit each time
db $A3, $C7            ; set address 000A2C bit OFF 80
; db $A3, $C6            ; set address 000A2C bit OFF 40 (used elsewhere)
db $A3, $C5            ; set address 000A2C bit OFF 20
db $A3, $C4            ; set address 000A2C bit OFF 10
db $A3, $C3            ; set address 000A2C bit OFF 08
db $A3, $C2            ; set address 000A2C bit OFF 04
db $A3, $C1            ; set address 000A2C bit OFF 02
db $A3, $C0            ; set address 000A2C bit OFF 01

; restore player status for SAFETY
db $DB

; this blanket disables cutscene flag
db $A5, $FE                     ;Clear Event Flag 1FE

db $C3, $06
db $71
db $FF
pad $C88F86


; rewrite npc locations and data
; these stars will functionally serve as warppoints


; NPC 1
org $CE9AD8
db $D9, $02 ; action 
org $CE9ADB
db $00, $10 ; x/y

; NPC 2
org $CE9ADF
db $D8, $02 ; action
org $CE9AE2
db $03, $10 ; x/y

; NPC 3
org $CE9B02
db $DA, $02 ; action
org $CE9B04
db $1B ; change sprite
org $CE9B05
db $06, $10 ; x/y
org $CE9B07
db $3F, $1B ; walk cycle properties

; changes trigger from pyramid cutscene 
; dont make warpshard need any bits
org $F046E9
db $ff, $8a, $00, $00, $00

; leftmost book in surgate library. These are the events only, tied to what the warps do
org $CE1DA9
db $FF, $E9, $02 ; triggers always
db $FF, $00, $00, $F0, $4A, $05 ;unsure, keeping consistent with original
org $CE1DB6
db $FF, $EA, $02 ; triggers always
db $FF, $00, $00
db $FF, $EA, $02, $F0, $4A, $05 ;unsure, keeping consistent with original
org $CE1DC6
db $FF, $EB, $02 ; triggers always
db $FF, $00, $00
db $FF, $EB, $02, $F0, $4A, $05 ;unsure, keeping consistent with original
; librarian always gives access
org $CE1DEE
db $FF, $A4, $03 ; triggers always
db $FF, $00, $00
db $FF, $A4, $03


; finally disable books entirely
org $CE8A7E
pad $CE8AA1




; Code for NPC Triggered on Necrophobe defeat

; NPC 3
org $CE9B09
db $DB, $02 ; action
org $CE9B0B
db $1B ; change sprite
org $CE9B0C
db $03, $0D ; x/y
org $CE9B0E
db $3F, $1B ; walk cycle properties

; change NPC behavior for calling an event
org $CE1DD7
db $35, $04

; disable guards from calling above event
org $CE8997
db $E3
org $CE899E
db $E3
org $CE89A5
db $E3
org $CE89AC
db $E3
org $CE89B3
db $E3
org $CE89BA
db $E3

; change address for custom event
org $C83FBF
db $20, $00, $F9





; Rift Warp Dialogue
org $F90020

db $F0, $03, $02              ;Conditional yes/no dialogue at 04B7
db $CD, $43, $04                ;Run event index 0408
db $FF
db $FF



org $C83FE9
db $40, $02, $F9

; world 3 warp
org $F90240
; change world flag to WORLD 3
db $A3, $C8 ; off
db $A3, $C9 ; off
db $A2, $CA ; on

db $C5, $80                     ;<unknown>
db $B5, $02                     ;Play Sound Effect Void, Image
db $C4, $06
db $71
db $E1, $FC, $01, $27, $2A, $00 ;Return from cutscene? 00 00 9C 96 00
db $D2, $02, $93, $51, $D8     ; airship
; WORLD CONDITIONALS
; Submarine conditional $EE
; db $A4, $F9            ; set address 000A53 bit ON 02
; ; Lonka ruin restrict access
db $A5, $FA            ; set address 000A53 bit OFF 04
; Set world 3 on status
db $A2, $79            ; set address 000A23 bit ON 02


db $EE

db $14
db $C3, $06
db $71
db $FF


; Text box
; Warp to final Rift save point?
org $E1926A
db $76, $7A, $8B, $89, $96, $8D, $88, $96, $7F, $82, $87, $7A, $85, $96, $71, $82, $7F, $8D, $96, $8C, $7A, $8F, $7E, $96, $89, $88, $82, $87, $8D, $A2, $00