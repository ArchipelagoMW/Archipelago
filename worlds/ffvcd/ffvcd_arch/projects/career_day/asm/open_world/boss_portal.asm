; move necrophobe sprite elsewhere and update
org $ce9a76
db $C9, $01, $17, $2d, $22, $3c, $03

; event reference 01C9 used here
; change to allow all directions
org $CE1623
db $FC, $FB
; Disable dancer in Jacohl
org $ce7737
db $C8
; Disable Purple warp guy in Tule
org $CE0ADD
db $FC, $FB


; Interact with NPC in final Void area
org $C9FBD3
db $F0, $C7, $04              ;Conditional yes/no dialogue at 04B7
db $CD, $0E, $04                ;Run event index 0408
db $FF                          ;End Event
db $FF                          ;End Event
pad $C9FC2C


org $c954a8
db $C5, $E0                     ;<unknown>
db $B5, $02                     ;Play Sound Effect Void, Image
db $71
db $C5, $E0                     ;<unknown>
db $B5, $02                     ;Play Sound Effect Void, Image
db $71
db $C5, $E0                     ;<unknown>
db $B5, $02                     ;Play Sound Effect Void, Image
db $71
db $C4, $03
db $75
db $E1, $21, $01, $08, $07, $00 ; Warp
db $03
db $C3, $03
db $75
db $FF
pad $C954CB

; text
org $E25BFF
;A powerful enemy calls... Proceed?
db $60, $96, $89, $88, $90, $7E, $8B, $7F, $8E, $85, $96, $7E, $87, $7E, $86, $92, $96, $7C, $7A, $85, $85, $8C, $A3, $A3, $A3, $01, $60, $87, $96, $7A, $85, $8D, $7E, $8B, $87, $7A, $8D, $7E, $96, $7F, $82, $87, $7A, $85, $96, $7B, $88, $8C, $8C, $96, $7A, $90, $7A, $82, $8D, $8C, $A3, $01, $6F, $8B, $88, $7C, $7E, $7E, $7D, $A2, $00


; C83515
; C84454

; conditional event A7, 00 should be freed now that the warps aren't using it
            ; ; change conditionals for meteors
            ; ; walse
            ; org $F04803
            ; db $FF, $A7, $00, $00, $00
            ; ; karnak
            ; org $F04819
            ; db $FF, $A7, $00, $00, $00

            ; ; reference event at meteors
            ; org $C83515
            ; db $A0, $2B, $F8


; talk to Exdeath Event
org $F82BD0
db $C8, $11, $01
db $B5, $18 ; sound
db $75
db $83, $0A
db $80, $0A
db $81, $0A
db $82, $0A
db $84, $0A
db $86, $0A
db $85, $0A
db $BD, $55, $07
db $A4, $A8            ; set address 000A49 bit ON 01
db $A4, $A9            ; set address 000A49 bit ON 02
                        ; this will set the battle to be considered complete
db $FF





; Event for post Exdeath, if fight was ended properly
; This was original event A7, 05
org $C84415
db $F0, $2B, $F8

org $F82BF0
; Everything below is post fight 
db $A2, $C8            ; set address 000A2D bit ON 01
db $A2, $C9            ; set address 000A2D bit ON 02
db $A2, $CA            ; set address 000A2D bit ON 04
db $73
db $C4, $02
db $75
db $0A                          ;Player Hide
db $E1, $0D, $00, $01, $01, $00 ;Inter-map cutscene
db $C3, $06
db $B4, $0B ; play requiem
db $73
db $C8, $12, $01
db $75
db $B7, $0C                     ;Add/Remove character 0C
db $CD, $43, $01                ;Run event index 0143
db $FF


; Event for post Exdeath, if fight was NOT ended properly 
; This was original event AA, 05
org $C8441E
db $10, $2C, $F8

org $F82C10
; Text box into death
db $73
db $C8, $20, $06
db $A5, $A8            ; set address 000A49 bit OFF 01
db $CD, $8A, $00                ;Runs event for warpshard
db $FF

;Fools... underhanded tactics will never win. Begone!
org $E2B92F
db $65, $88, $88, $85, $8C, $A3, $A3, $A3, $96, $8E, $87, $7D, $7E, $8B, $81, $7A, $87, $7D, $7E, $7D, $96, $8D, $7A, $7C, $8D, $82, $7C, $8C, $96, $90, $82, $85, $85, $01, $87, $7E, $8F, $7E, $8B, $96, $7D, $7E, $7F, $7E, $7A, $8D, $96, $86, $7E, $A3, $96, $61, $7E, $80, $88, $87, $7E, $A1, $00


; Event for rejecting without enough tablets
; Event A3, 05
org $C84409
db $30, $2C, $F8
org $F82C30


; Text box into death
db $C8, $22, $06
db $A5, $A8            ; set address 000A49 bit OFF 01
db $CD, $8A, $00                ;Runs event for warpshard
db $FF


org $E2B9CB
;Come back when you have unlocked the power to traverse the Rift...
db $62, $88, $86, $7E, $96, $7B, $7A, $7C, $84, $96, $90, $81, $7E, $87, $96, $92, $88, $8E, $96, $81, $7A, $8F, $7E, $01, $8E, $87, $85, $88, $7C, $84, $7E, $7D, $96, $8D, $81, $7E, $96, $89, $88, $90, $7E, $8B, $96, $8D, $88, $96, $8D, $8B, $7A, $8F, $7E, $8B, $8C, $7E, $01, $8D, $81, $7E, $96, $71, $82, $7F, $8D, $A3, $A3, $A3, $00






; talk to Exdeath NPC
org $C84454
db $D0, $2B, $F8

; org $F82BD0 ??


; blank out other NPCs here
org $CE8736
; pad $Ce874B

; if you eventually want to do something with them ... 
db $57, $01, $19, $07, $0C, $b7, $03
db $57, $01, $19, $08, $0D, $b7, $03
db $57, $01, $19, $09, $0C, $b7, $03
; db $ff, $00, $09, $07, $0b, $04, $47
; db $ff, $00, $09, $09, $0b, $04, $47
; db $ff, $00, $09, $08, $0c, $04, $47
db $b1, $01, $20, $08, $0b, $0d, $16 ; exdeath placeholder
db $57, $01, $19, $07, $0B, $b7, $03
db $57, $01, $19, $09, $0B, $b7, $03
; db $ff, $00, $09, $08, $0C, $04, $47


; change exdeath to have an event
org $CE874B
db $B1, $01 ; this is just some arbitrary test event. is it..??
db $20
db $08, $0B
org $CE15AF
db $BC, $05

; change  Exdeath sprite, then change inplace walk cycle & color
org $CE874D
db $1B
org $CE8750
db $3F, $1B


; dialogue after 
org $E14CBA
db $01
db $96,$96,$96,$96,$96,$96,$96,$96,$96,$96, $96,$96, $60, $96, $7D, $82, $7F, $7F, $7E, $8B, $7E, $87, $8D, $96, $8C, $8D, $88, $8B, $92, $01
db $96,$96,$96,$96,$96,$96,$96,$96,$96,$96, $96,$96, $8D, $88, $88, $84, $96, $89, $85, $7A, $7C, $7E, $96, $8D, $88, $7D, $7A, $92, $A3, $A3, $A3, $00