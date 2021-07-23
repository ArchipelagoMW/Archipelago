;;; 
;;; Progressive suits patch
;;; 
;;; Author: Smiley
;;; 
;;; Disassembled from DASH IPS patch
;;; 
;;; Effects :
;;; 
;;; * Enemy damage : each suit brings 50% additional damage reduction
;;;   instead of 50% for varia and 75% for gravity
;;; * Heat damage : full protection for Varia, half for gravity

;;; compile with asar (https://www.smwcentral.net/?a=details&id=14560&p=section),
;;; or a variant of xkas that supports arch directive

lorom
arch snes.cpu

;;; full heat protection with varia instead of varia or gravity
org $8de37d
	db $01

;;; periodic damage modification (environmental damage)
org $90e9df
periodic_dmg:
	beq .nogravity
	;; takes MSB of periodic dmg float part and divide it by 2
	lda $0A4F
	lsr
	pha
	xba
	and #$FF00
	sta $0A4E
	pla
	xba
	and #$00FF
	;; 1 HP hit if needed
	sta $0A50
.nogravity:
	lda $09A2		; check equipped items for varia
	bit #$0001
	beq .novaria
	lda $0A4F		; proceed with routine

org $90ea11
.novaria:			; vanilla branch for no suits

;;; enemy damage division routine (suits patch)
;;; $12 is tmp var with enemy damage
org $a0a463
damage_div:
	bit #$0001		; A contains equipped items
	beq .novaria
	lsr $12			; /2 if varia
.novaria:
	bit #$0020
	beq .nogravity
	lsr $12			; /2 if grav
.nogravity:
	lda $12
	rtl

;;; metroid damage subroutine patch. (workaround hardcoded stuff??)
org $a3eed8
metroid_dmg:
	lda #$C000		; metroid damage value to dmg tmp var
	sta $12			;
	lda $09A2		; equipped items
	bit #$0020
	beq .nogravity
	lsr $12			; /2 if grav
.nogravity:
	bit #$0001
	beq .novaria		; /2 if varia
	lsr $12
.novaria:
	jmp $EEF2 		; continue routine
