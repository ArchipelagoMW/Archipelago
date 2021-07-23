;;; Reduce rainbow beam from 300 damage to 20 (for ultra sparse energy seeds)
;;;
;;; compile with asar (https://www.smwcentral.net/?a=details&id=14560&p=section),
;;; or a variant of xkas that supports arch directive

lorom
arch snes.cpu
	
;;; vanilla
;;; $BA27:  ;;;
; {
; $A9:BA27 A9 3C BA    LDA #$BA3C            ; next instruction
; $A9:BA2A 8D A8 0F    STA $0FA8  [$7E:0FA8] ; store next instruction in enemy ai var
; $A9:BA2D A9 2B 01    LDA #$012B            ; 299 loops to remove energy from samus
; $A9:BA30 8D B2 0F    STA $0FB2  [$7E:0FB2] ; enemy ai var for loops
; $A9:BA33 8D 40 18    STA $1840  [$7E:1840] ; screen shaking
; $A9:BA36 A9 08 00    LDA #$0008
; $A9:BA39 8D 3E 18    STA $183E  [$7E:183E] ; type of screen shaking
; }

;;; reduce samus energy for 19 loops instead of 299. One more loop is done.
;;; each loop reduce 1 energy when varia is equipped, 2 if not
org $A9BA2D
        lda #$0013
