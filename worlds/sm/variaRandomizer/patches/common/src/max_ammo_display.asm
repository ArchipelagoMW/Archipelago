;;; Display in HUD the maximum number of ammo that samus can carry
;;;
;;; compile with asar (https://www.smwcentral.net/?a=details&id=14560&p=section),
;;; or a variant of xkas that supports arch directive

lorom
arch snes.cpu

;;; $9D98: Draw two HUD digits ;;;
;;; Parameters:
;;;     A: Number to draw                   ; 0 -> 99
;;;     X: HUD tilemap index                ; to index into $7E:C608
;;;     $00: Long pointer to digits tilemap ; $80:9DD3 (Artillery HUD digits tilemap)
!draw_two_HUD_digits   = $9D98

;;; $9D78: Draw three HUD digits ;;;
;;; Parameters:
;;;     A: Number to draw                   ; 0 -> 999
;;;     X: HUD tilemap index                ; to index into $7E:C608
;;;     $00: Long pointer to digits tilemap ; $80:9DD3 (Artillery HUD digits tilemap)
!draw_three_HUD_digits = $9D78

!samus_missiles           = $09C6
!samus_max_missiles       = $09C8
!samus_super_missiles     = $09CA
!samus_max_super_missiles = $09CC
!samus_power_bombs        = $09CE
!samus_max_power_bombs    = $09D0

;;;    $09D2: HUD item index
;;;    {
;;;        0: Nothing
;;;        1: Missiles
;;;        2: Super missiles
;;;        3: Power bombs
;;;        4: Grapple beam
;;;        5: X-ray
;;;    }
!hud_item_index            = $09D2
!hud_item_index_missile    = #$0001
!hud_item_index_super      = #$0002
!hud_item_index_power_bomb = #$0003

;;; see $7E:C608..C7: HUD tilemap. Not including top-most row (row 0)
!row1_missile_index      = #$0014
!row1_missile_tile0      = $7EC61C
!row1_missile_tile1      = $7EC61E
!row1_missile_tile2      = $7EC620
!row2_missile_tile0      = $7EC65C
!row2_missile_tile1      = $7EC65E
!row2_missile_tile2      = $7EC660
!row3_missile_index      = #$0094

!row1_super_index        = #$001A
!row1_super_tile0        = $7EC622
!row1_super_tile1        = $7EC624
!row1_super_tile2        = $7EC626
!row2_super_tile0        = $7EC664
!row2_super_tile1        = $7EC666
!row3_super_index_vanilla = #$009C
!row3_super_index_custom  = #$009A
!row3_super_tile0        = $7EC6A2

!row1_power_bomb_index   = #$0020
!row1_power_bomb_tile0   = $7EC628
!row1_power_bomb_tile1   = $7EC62A
!row1_power_bomb_tile2   = $7EC62C
!row2_power_bomb_tile0   = $7EC66A
!row2_power_bomb_tile1   = $7EC66C
!row3_power_bomb_index_vanilla = #$00A2
!row3_power_bomb_index_custom  = #$00A0
!row3_power_bomb_tile0   = $7EC6A8

;;; ;;; $9DBF: HUD digits tilemap ;;;
;;; {
;;; ; Artillery                0     1     2     3     4     5     6     7     8     9
;;; $80:9DD3             dw 2C09, 2C00, 2C01, 2C02, 2C03, 2C04, 2C05, 2C06, 2C07, 2C08
;;; }
!HUD_digits_tilemap_row3 = #$9DD3
!empty_tile = #$2C0F

;;; used to return values from functions which extract digits
!digit1 = $0012
!digit2 = $0014
!digit3 = $0016

;;; or mask applied for selected/unselected item in hud
!select_mask = $0018
!selected   = #$1000
!unselected = #$1400

;;; 8x8 mult => 16
!mult1 = $4202
!mult2 = $4203
!mult_result = $4216

;;; 16/8 div => 16,16
!dividend  = $4204
!divisor   = $4206
!quotient  = $4214
!remainder = $4216

;;; NOP
org $8099E1
	;; nop it:
        ;; $80:99E1 AD A3 99    LDA $99A3  [$80:99A3]  ;\
        ;; $80:99E4 8F 1C C6 7E STA $7EC61C[$7E:C61C]  ;|
        ;; $80:99E8 AD A5 99    LDA $99A5  [$80:99A5]  ;|
        ;; $80:99EB 8F 1E C6 7E STA $7EC61E[$7E:C61E]  ;} Write top row of missile icon
        ;; $80:99EF AD A7 99    LDA $99A7  [$80:99A7]  ;|
        ;; $80:99F2 8F 20 C6 7E STA $7EC620[$7E:C620]  ;/
        nop : nop : nop
        nop : nop : nop : nop
        nop : nop : nop
        nop : nop : nop : nop
        nop : nop : nop
        nop : nop : nop : nop

org $809ACE
        ;; nop it:
        ;; $80:9ACE 22 CF 99 80 JSL $8099CF            ; Add missiles to HUD tilemap
        nop : nop : nop : nop

org $809AD7
        ;; nop it:
        ;; $80:9AD7 22 0E 9A 80 JSL $809A0E            ; Add super missiles to HUD tilemap
        nop : nop : nop : nop

org $809AE0
        ;; nop it:
        ;; $80:9AE0 22 1E 9A 80 JSL $809A1E            ; Add power bombs to HUD tilemap
        nop : nop : nop : nop

;;; HIJACKS
org $809B1A
        ;; hijack vanilla super missile count drawing on row 3 to display on three digits when >= 100
        jsr super_missile_count_drawing_row3
	
org $809B28
        ;; hijack vanilla power bomb count drawing on row 3 to display on three digits when >= 100
        jsr power_bomb_count_drawing_row3

org $809C00
        ;; hijack into: $9B44: Handle HUD tilemap (HUD routine when game is paused/running) ;;;
        ;; ; Handle Samus' missiles
        ;; $80:9BFB A9 D3 9D    LDA #$9DD3             ;\
        ;; $80:9BFE 85 00       STA $00    [$7E:0000]  ;} $00 = pointer to digit tiles
        ;; $80:9C00 AD C8 09    LDA $09C8  [$7E:09C8]  ;\
        ;; $80:9C03 F0 11       BEQ $11    [$9C16]     ;} If [Samus' max missiles] != 0:
        jmp hud_ammo_drawing


;;; parameters set by vanilla before all hijacks:
;;; LDA !HUD_digits_tilemap_row3
;;; STA $00    [$7E:0000]
org $80CDA0

;;; parameters set before hijack:
;;; LDX !row3_super_index_vanilla
;;; LDA !samus_super_missiles
super_missile_count_drawing_row3:
	cmp #$0064
	bpl .three_digits
.two_digits
        jsr !draw_two_HUD_digits
	;; display empty tile in front of two digits
        lda !empty_tile
        sta !row3_super_tile0
	bra .end
.three_digits
	ldx !row3_super_index_custom
        jsr !draw_three_HUD_digits
.end
        rts

;;; parameters set before hijack:
;;; LDX !row3_power_bomb_index_vanilla
;;; LDA !samus_power_bombs
power_bomb_count_drawing_row3:
	cmp #$0064
	bpl .three_digits
.two_digits
        jsr !draw_two_HUD_digits
	;; display empty tile in front of two digits
        lda !empty_tile
        sta !row3_power_bomb_tile0
	bra .end
.three_digits
	ldx !row3_power_bomb_index_custom
        jsr !draw_three_HUD_digits
.end
        rts
 
;;; hijack into: $9B44: Handle HUD tilemap (HUD routine when game is paused/running) ;;;
;;; draw all three rows for missile/super/powerbomb as we skip that part in vanilla code
hud_ammo_drawing:
        pha 
        phx 
        phy 
        lda !samus_max_missiles
        beq .no_missile
        jsr draw_missile
.no_missile:
        lda !samus_max_super_missiles
        beq .no_super
        jsr draw_super
.no_super:
        lda !samus_max_power_bombs
        beq .no_power_bomb
        jsr draw_power_bomb
.no_power_bomb:
        ply 
        plx 
        pla 
        jmp $9C55
 
draw_missile:
        jsr extract_three_digits
        lda !hud_item_index
        cmp !hud_item_index_missile
        beq .missile_is_selected
        lda !unselected
        sta !select_mask
        bra .else
.missile_is_selected:
        lda !selected
        sta !select_mask
.else:
        ;; display custom digits on row 1
        ldx !digit1
        lda HUD_digits_tilemap_row1,X
        ora !select_mask
        sta !row1_missile_tile0
        ldx !digit2
        lda HUD_digits_tilemap_row1,X
        ora !select_mask
        sta !row1_missile_tile1
        ldx !digit3
        lda HUD_digits_tilemap_row1,X
        ora !select_mask
        sta !row1_missile_tile2
        ;; display custom missile icon on row 2
        lda #$0049
        ora !select_mask
        sta !row2_missile_tile0
        lda #$004A
        ora !select_mask
        sta !row2_missile_tile1
        lda #$004B
        ora !select_mask
        sta !row2_missile_tile2
        ;; display vanilla digits on row 3
        lda !samus_missiles
        ldx !row3_missile_index
	jsr !draw_three_HUD_digits
       rts
 
draw_super:
	jsr extract_three_digits
	lda !hud_item_index
	cmp !hud_item_index_super
	beq .super_is_selected
	lda !unselected
	sta !select_mask
	bra .else
.super_is_selected:
	lda !selected
	sta !select_mask
.else:
        ;; display custom digits on row 1
	ldx !digit1
	beq .two_digits
	lda HUD_digits_tilemap_row1,X
	ora !select_mask
	sta !row1_super_tile0
.two_digits:
	ldx !digit2
	lda HUD_digits_tilemap_row1,X
	ora !select_mask
	sta !row1_super_tile1
	ldx !digit3
	lda HUD_digits_tilemap_row1,X
	ora !select_mask
	sta !row1_super_tile2
        ;; display custom super icon on row 2
        lda #$0034
        ora !select_mask
        sta !row2_super_tile0
        lda #$0035
        ora !select_mask
        sta !row2_super_tile1
        ;; display vanilla digits on row 3
	lda !samus_super_missiles
        ldx !row3_super_index_vanilla
	jsr super_missile_count_drawing_row3
        rts
 
draw_power_bomb:
        jsr extract_three_digits
        lda !hud_item_index
        cmp !hud_item_index_power_bomb
        beq .power_bomb_is_selected
        lda !unselected
        sta !select_mask
        bra .else
.power_bomb_is_selected:
        lda !selected
        sta !select_mask
.else:
	;; display custom digits on row 1
        ldx !digit1
	beq .two_digits
        lda HUD_digits_tilemap_row1,X
        ora !select_mask
        sta !row1_power_bomb_tile0
.two_digits:
        ldx !digit2
        lda HUD_digits_tilemap_row1,X
        ora !select_mask
        sta !row1_power_bomb_tile1
        ldx !digit3
        lda HUD_digits_tilemap_row1,X
        ora !select_mask
        sta !row1_power_bomb_tile2
        ;; display custom pb icon on row 2
        lda #$0036
        ora !select_mask
        sta !row2_power_bomb_tile0
        lda #$0037
        ora !select_mask
        sta !row2_power_bomb_tile1
        ;; display vanilla digits on row 3
	lda !samus_power_bombs
	ldx !row3_power_bomb_index_vanilla
	jsr power_bomb_count_drawing_row3
        rts
 
;;; Extract three digits
;;; Parameters:
;;;     A: Three digits number
;;; Return:
;;;     $12: first digit
;;;     $14: second digit
;;;     $16: third digit
extract_three_digits:
	sta !dividend ; a = (a / 100) * 2
	sep #$20      ; 8-bit mode
	lda #$64 ; 100
	sta !divisor
	pha 
	pla 
	pha 
	pla 
	rep #$20                ; 16-bit mode
	lda !quotient
	asl A ; x2
	sta !digit1
	lda !remainder
 
;;; Extract two digits
;;; Parameters:
;;;     A: Two digits number
;;; Return:
;;;     $14: first digit
;;;     $16: second digit
extract_two_digits:
	sta !dividend
	sep #$20
	lda #$0A
	sta !divisor
	pha 
	pla 
	pha 
	pla 
	rep #$20
	lda !quotient
	asl A
	sta !digit2
	lda !remainder
	asl A
	sta !digit3
	rts

;;; HUD digits tilemap for row 1
HUD_digits_tilemap_row1:
        ;;     0      1      2      3      4      5      6      7      8      9
	dw $0045, $003C, $003D, $003E, $003F, $0040, $0041, $0042, $0043, $0044

;;; next patch start address (msu1)
warnpc $80D02F

;;; 85/ MISSILE/SUPER/POWER BOMB message tilemaps
org $858851
	dw $280F, $280F, $280F
	
org $858891
	dw $3049, $304A, $304B
	
org $858951
	dw $280F, $280F, $280F

org $858993
	dw $3034, $3035

org $858A4F
        dw $280F, $280F

org $858A8F
        dw $3036, $3037

;;; 9A/$B200: Standard BG3 tiles ;;;
org $9AB542
        db $9F, $7F, $B2, $7F, $AE, $73, $AE, $73, $B2, $7F, $9F, $7F, $FF, $80, $FF, $01
        db $F1, $FE, $FD, $2E, $2B, $F6, $FB, $26, $2D, $FE, $F1, $FE, $FF, $01, $FF, $80
        db $83, $7F, $86, $7F, $8F, $7A, $8E, $7B, $87, $7E, $83, $7F, $FF, $80, $FF, $01
        db $C1, $FE, $61, $FE, $F1, $5E, $71, $DE, $E1, $7E, $C1, $FE, $FF, $01

org $9AB5C0
        db $3C, $C3, $7C, $9B, $7C, $BB, $7C, $9B, $3C, $DB, $3C, $DB, $3C, $C3, $00, $FF
        db $FE, $01, $FF, $7C, $7F, $86, $FF, $3C, $FF, $60, $FF, $7E, $FF, $00, $00, $FF
        db $FE, $01, $FF, $7C, $FF, $06, $7F, $BC, $FF, $06, $FF, $7C, $FE, $01, $00, $FF
        db $3E, $C1, $7E, $9D, $FE, $2D, $FF, $4C, $FF, $7E, $FF, $0C, $1E, $E1, $00, $FF
        db $FF, $00, $FF, $7C, $FE, $61, $FF, $7C, $FF, $06, $FF, $7C, $FE, $01, $00, $FF
        db $7E, $81, $FE, $3D, $FE, $61, $FF, $7C, $FF, $66, $FF, $3C, $7E, $81, $00, $FF
        db $FF, $00, $FF, $7E, $FF, $06, $3F, $CC, $3E, $D9, $3C, $DB, $3C, $C3, $00, $FF
        db $7E, $81, $FF, $3C, $FF, $66, $FF, $3C, $FF, $66, $FF, $3C, $7E, $81, $00, $FF
        db $7E, $81, $FF, $3C, $FF, $66, $FF, $3E, $7F, $86, $7F, $BC, $7E, $81, $00, $FF
        db $7E, $81, $FF, $3C, $FF, $66, $FF, $66, $FF, $66, $FF, $3C, $7E, $81, $00

org $9AB691
        db $80, $80, $7F, $87, $7F, $89, $7E, $89, $7E, $87, $7F, $80, $7F, $FF, $80, $FF
        db $00, $E3, $FF, $1F, $FE, $FF, $21, $E1, $3F, $1E, $FF, $E3, $FF, $FF, $00, $FF
        db $01, $F9, $FE, $F1, $1E, $21, $FE, $E1, $3E, $11, $FE, $F9, $FE, $FF, $01
