;;; makes it so that red doors are only openable with 1 missile, instead of 5 missiles or 1 super
;;; compile with asar

arch snes.cpu
lorom	

;;; duplicate of door hit PLM instruction used for
;;; eye and red doors, with just super missile related code removed
;;; (in some unused space inside bank $84)
org $848560
red_doors:
	LDA $1D77,x  ;\
	BEQ .end     ;} If not shot: return
	AND #$0F00   ;\
	CMP #$0100   ;\
	BNE .dud     ;} If not shot with missile: go to BRANCH_DUD
.missile:
	STZ $1D77,x   ; Clear PLM shot status
	LDA $7EDEBC,x ;\
	STA $1D27,x   ;} PLM instruction list pointer = [PLM link instruction]
	LDA #$0001    ;\
	STA $7EDE1C,x ;} PLM instruction timer = 1
	bra .end
.dud:
	LDA #$0057   ;\
	JSL $8090CB  ;} Queue sound 57h, sound library 2, max queued sounds allowed = 6 (shot door/gate with dud shot)
	STZ $1D77,x  ; Clear PLM shot status
.end:
	RTS

;;; start of save station fix
warnpc $84858c

;;; now overwrite all references to vanilla PLM instruction with our
;;; tweaked one in red door PLMs instruction lists, and update 
;;; door hit count to 1 instead of 5
org $84c322
	dw red_doors
org $84c32c
	db $01
org $84c384
	dw red_doors
org $84c38e
	db $01
org $84c3e6
	dw red_doors
org $84c3f0
	db $01
org $84c448
	dw red_doors
org $84c452
	db $01
