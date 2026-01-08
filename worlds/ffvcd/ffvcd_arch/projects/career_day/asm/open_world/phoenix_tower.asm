hirom

; remove wall fights
org $C97DB6
db $00, $00, $00
org $C99DCC
db $00, $00, $00
org $C99DC5
db $00, $00, $00
org $C99DBE
db $00, $00, $00

; HARDCODE TEMP FOR VALIDATION NAME, NEEDS TO BE SET BY RANDOMIZER
; org !ADDRESS_phoenixtowername
; db $61, $8E, $8D, $93, $93, $93

; ; change floor 1 phoenix tower for x/y events
; org $CE34BC
; db $0F, $13, $EA, $01
; db $0F, $16, $E9, $01


; ; EVENT FOR INPUTTING NAME
; ; overwrite event 10 00 (from beginning of game where butz gets named in vanilla)

; org $c833e9
; db $80, $05, $F9

; org $F90580
; ; set the event code for 'in naming validation event'
; db $C5, $F0
; db $B5, $02
; db $71
; db $C8, $16, $05
; db $F2
; db $7A
; db $F2



; db $A2, $65 ; 000A20 bit 20
; db $FF




; ; EVENT FOR VALIDATING PROGRESS - FAILURE (RED)
; ; Overwrite event 22 00 (canal key use cutscene)
; org $C83386
; db $00, $06, $F9

; org $F90600
; db $C5, $20
; db $B5, $02
; db $71
; db $C8, $17, $05
; db $03
; db $A3, $65 ; 000A20 bit 20
; db $FF

; ; EVENT FOR VALIDATING PROGRESS - SUCCESS (BLUE)
; ; Overwrite event 22 00 (canal key use cutscene)
; org $C83395
; db $40, $06, $F9

; org $F90640
; db $C5, $80
; db $B5, $02
; db $71
; db $C8, $18, $05
; db $01
; db $A3, $65 ; 000A20 bit 20
; db $A2, $5A ; 000A1F bit 04
; db $FF



; ; text boxes
; org $E2751E
; db $71, $82, $7F, $8D, $96, $8D, $8B, $7A, $8F, $7E, $85, $7E, $8B, $8C, $A3, $A3, $A3, $96, $8D, $7E, $86, $89, $88, $8B, $7A, $8B, $82, $85, $92, $01
; db $8D, $82, $8D, $85, $7E, $96, $92, $88, $8E, $8B, $96, $81, $7E, $8B, $88, $96, $8D, $81, $7E, $01
; db $62, $88, $7D, $7E, $96, $88, $7F, $96, $8D, $81, $7E, $96, $75, $88, $82, $7D, $A3, $00

; org $e275d6
; db $78, $88, $8E, $96, $81, $7A, $8F, $7E, $96, $89, $8B, $88, $8F, $7E, $87, $96, $92, $88, $8E, $8B, $96, $8C, $8D, $8B, $7E, $87, $80, $8D, $81, $A3, $A3, $A3, $01
; db $7A, $7C, $7C, $7E, $8C, $8C, $96, $80, $8B, $7A, $87, $8D, $7E, $7D, $A3, $00

; org $E2757C
; db $61, $7E, $80, $88, $87, $7E, $9D, $96, $8D, $81, $88, $8C, $7E, $96, $90, $81, $88, $96, $81, $7A, $8F, $7E, $96, $87, $88, $8D, $01
; db $7B, $8B, $7A, $8F, $7E, $7D, $96, $8D, $81, $7E, $96, $75, $88, $82, $7D, $A3, $00
