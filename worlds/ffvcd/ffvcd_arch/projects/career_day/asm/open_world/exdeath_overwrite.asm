hirom

; change formation
; org $D07
; db $F7

; OVERWRITE EXDEATH GALUF
    ; Formation (changed $13 (after $4f) to $4D)
org $D04F70 ; THIS IS EXDEATH GALUF
org $D04DD0 ; THIS IS A TEST ON ASPIS 
db $20, $80, $00, $20, $4e, $4f, $4D, $6b, $6c, $6d, $6e, $ff, $1a, $a8, $28, $62

    ; AI
org $D0BF28
db $00, $00, $00, $00, $FE, $FD, $DE, $C0, $AA, $FD, $DE, $C0, $DE, $FD, $33, $22, $DE, $FD, $DE, $DE, $C0, $FD, $DE, $C0, $AA, $FD, $DE, $82, $C0, $FF, $0F, $00, $00, $00, $FE, $FD, $F7, $1E, $F0, $FD, $F8, $00, $3E, $FD, $F6, $07, $E3, $FD, $F6, $07, $E4, $FD, $F6, $07, $E5, $FD, $F6, $07, $E6, $FD, $F6, $07, $E7, $FD, $F2, $8D, $DE, $EE, $FF

pad $D0BFC9

    ; Enemy 
org $D029A0
db $2c, $6f, $11, $0a, $23, $19, $19, $0f, $01, $00, $30, $75, $00, $00, $00, $00, $00, $00, $ff, $ff, $10, $00, $40, $00, $a0, $18, $00, $00, $00, $00, $13, $4d

org $D098B8 ; GALUF FIGHT
org $D097E8 ; ASPIS FIGHT
db $a2, $16, $14, $98, $dd, $f6, $5c, $00


; D0D850 = enemy sprite layout
; D0C59E = same when switching enemies

org $F053B7
db $FF, $84, $07

; ; change index. THIS SHOULD NOT BE PERMANENT...?
; org $F04302
; db $BF

org $C9FE43

; This is the event for the INSTANT DEATH PHASE 1 FIGHT
; This will trigger if $000A2D bit 10 is set
org $F05E3C
db $FE, $CC, $FF, $23, $07


; Exdeath's final cutscene, lots of space. 
; VERSION FOR EXDEATH PHASE 1 SKIP FIGHT
org $C9DCCE

db $01, $01, $01
db $B5, $2D                     ;Play Sound Effect Demi, Qrter
db $CD, $86, $07                ;Run event index 0786
db $71                          ;Short pause
db $C8, $12, $08                ;Display Message/Text/Dialogue 11 08
db $71                          ;Short pause
db $0C                          ;<Unknown>
db $06                          ;Player Bounce in Place
db $01                          ;Player Move Up
db $0B                          ;<Unknown>
; db $BD, $3B, $1C ; GALUF FIGHT
db $BD, $A8, $1C ; ASPIS FIGHT
db $D0, $F0, $00                ;(Music) F0 00
db $B4, $11                     ;Play Background Music (Nothing)
db $75                          ;Extremely long pause
db $B7, $0C 					; add cara over galuf for non glitchy ending...?
db $CD, $43, $01                ;Run event index 0143

db $FF

; VERSION FOR NORMAL
org $C849AC
db $B0, $4E, $C8

org $C84EB0
db $B5, $2D                     ;Play Sound Effect Demi, Qrter
db $CD, $86, $07                ;Run event index 0786
db $C8, $11, $08                ;Display Message/Text/Dialogue 11 08
db $A2, $C8            ; set address 000A2D bit ON 01
db $06                          ;Player Bounce in Place
db $BD, $BA, $1C                ;Start Event Battle BA
db $A2, $C9            ; set address 000A2D bit ON 02
db $0A				;Player Hide
db $C3, $05			;Fade in Speed 04
db $73
db $C4, $05			;Fade out Speed 04
db $73
db $73
db $D0, $F0, $00                ;(Music) F0 00
db $B4, $11                     ;Play Background Music (Nothing)
db $B7, $0C 					; add cara over galuf for non glitchy ending...?
db $CD, $43, $01                ;Run event index 0143




; new text 
; [player]: Exdeath! Feel our wrath again!
org $E3493d
db $02, $9B, $FF, $FF, $64, $91, $7D, $7E, $7A, $8D, $81, $A1, $01, $FF, $FF, $65, $7E, $7E, $85, $96, $88, $8E, $8B, $96, $90, $8B, $7A, $8D, $81, $96, $7A, $80, $7A, $82, $87, $A1, $00