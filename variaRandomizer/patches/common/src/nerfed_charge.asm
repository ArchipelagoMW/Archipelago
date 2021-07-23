;;; 
;;; Nerfed charge beam patch
;;; 
;;; Authors: Smiley for permanent charge and beam damage hijack.
;;;          Flo for hardware division usage and SBA/pseudo screw damage.
;;; 
;;; Originally disassembled from DASH IPS patch
;;; 
;;; Effects : charge beam is available from the start, with nerfed damage

;;; compile with asar (https://www.smwcentral.net/?a=details&id=14560&p=section),
;;; or a variant of xkas that supports arch directive

lorom
arch snes.cpu

;;; divides projectile damage by 3
macro divprojdmg3()
	lda $0C2C,X
	sta $4204
	sep #$20
	lda #$03
	sta $4206
	rep #$20
	pha : pla : xba : xba 	; wait for division
	lda $4214
	sta $0C2C,X
endmacro

;;; goes to charge branch whatever items
org $90b81e
	bit #$0000
	bra $0a

;;; disables a "no charge" check
org $90b8f2
	bra $00

;;; hijack for beam damage modification 
org $90b9e6
	jsr charge

;;; hijack for SBA ammo spend
org $90ccd2
	jmp sba_ammo

;;; nerfed charge : damage modification
org $90f6a0
charge:
	lda $09A6		; equipped beams
	bit #$1000		; check for charge
	bne .end
	;; if no charge, nerfs charge dmg : divide by 3
	%divprojdmg3()
.end:
	lda $0C18,X
	rts

org $90f810
nochargesba:
; This alternate table is just as inefficient as the original
        dw $0000 ; 0: Power
        dw $0003 ; 1: Wave
        dw $0003 ; 2: Ice
        dw $0000 ; 3: Ice + wave
        dw $0003 ; 4: Spazer
        dw $0000 ; 5: Spazer + wave
        dw $0000 ; 6: Spazer + ice
        dw $0000 ; 7: Spazer + ice + wave
        dw $0003 ; 8: Plasma
        dw $0000 ; 9: Plasma + wave
        dw $0000 ; Ah: Plasma + ice
        dw $0000 ; Bh: Plasma + ice + wave
sba_ammo:
	lda $09a6
	bit #$1000 : beq .nocharge  ; if charge :
	lda $09ce    		    ; 	restore A (PB count)
	jmp $ccd5		    ;   continue original routine
.nocharge:
	;; vanilla code actually works only with 1s or 0s in the table
	;; so we add an actual check for PB qty
	lda $09ce		    ; PB count
	sec : sbc nochargesba,X	    ; substract PB qty needed
	bmi .notenough		    ; if enough PBs:
	jmp $ccd9		    ; 	proceed with routine after original substraction
.notenough:			    ; else:
	jmp $ccc8		    ;   make original function return with carry clear (SBA failed)

;;; what's below works, uncomment to enable nerfed SBA damage
;; ;;; nerf SBA damage
;; org $9381b9
;; 	jsr sba_nerf

;; org $93f620
;; sba_nerf:
;; 	sta $0C2C,X
;; 	lda $09A6		; equipped beams
;; 	bit #$1000		; check for charge
;; 	bne .end
;; 	;; if no charge, nerfs SBA dmg : divide by 3
;; 	%divprojdmg3()
;; .end:
;; 	rts

;;; nerf pseudo screw damage
org $a0a4cc
	jsr pseudo

org $a0f800
pseudo:
	;; we can't freely use A here. Y shall contain pseudo screw dmg at the end
	pha
	lda $09A6		; equipped beams
	bit #$1000		; check for charge
	beq .nocharge
.charge:
	ldy #$00C8		; vanilla value
	bra .end
.nocharge:
	ldy #$0042		; 66 (approx 200/3)
.end:
	pla
	rts

warnpc $a0f820
