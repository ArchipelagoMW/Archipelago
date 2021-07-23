; Copyright 2015 Adam <https://github.com/n00btube>
; MIT license.

; Makes save points refill Samus' energy and supplies, like the ship.
;
; Hijacks the save station PLM and uses some free space in that bank ($84), as
; well as any other bank of your choosing.  This *is* the cross-bank version.

lorom

; hijack point: reconfigure the save-station PLM instructions. do not edit.
; the original instructions read:
; [8CF1=prompt][B008][B00E=freeze/pose Samus][8C07,2E=saving sound]...
; we overwrite those first 3 words and chain into the hijacked instructions,
; making it have the effect of:
; [B00E][refill_run, repeated until full][8CF1][B008][8C07,2E]...
org $84AFEE
	DW plm_start    ; hijack the "save?" message & posing
	DW plm_run, $B008
	; the hijack will chain the PLMs we overwrote.
	; remaining PLM instructions are used as-is.

; this stub can be moved anywhere in bank $84’s free space, and MUST be bank $84.
; the stub needs 31 ($1F) bytes of space.
; moved to an unused plm instruction.
org $84853E
plm_start:
	TYA                ; copy pointer to refill_run into A
	STA $1D27,X        ; set refill_run as next PLM instruction
	JSR $B00E          ; freeze and pose Samus (saves X/Y itself)
	JSL refill_start
plm_run:
	JSL refill_run
	ASL                ; set Z flag if A is $0000 (saves 2 bytes vs. CMP)
	BNE plm_more       ; not all full: run this refill instruction next frame
	JMP $8CF1          ; all items full: run hijacked save prompt
	; (this will stop the current PLM instruction from running again)

plm_more:
	LDA #$0001         ; run this PLM instruction next frame
	STA $7EDE1C,X      ; write frame delay
	PLA                ; end current frame's instructions for this PLM
	RTS                ; run next PLM


; this can be any free space, anywhere in the ROM.
; all it needs is 86 ($56) bytes of space there.
; for demonstration, I just picked the first possible location.
org $A1F400
refill_start:
	STZ $0A6A          ; zero "health alarm on" flag
	LDA #$0001         ; stop sound
	JSL $80914D        ; sound lib 3 routine (also saves X/Y)
	INY : INY          ; advance past the refill_run instruction
	; (if we are ALREADY full, JMP $8CF1 wouldn't have $B008 as arg.)
	RTL                ; get back to PLM code (so it can JSL refill_run...)

refill_run:
	PHX : PHY          ; preserve regs
	LDY #$0000         ; set up "everything fully refilled" value

	; comment the LDX/JSR line (add a semicolon to the beginning of the line)
	; of any items you DO NOT want to refill.  or just delete it.

	LDA #$0005 : STA $12      ; energy increment value per frame
	LDX #$09C2 : JSR inc_item ; energy tanks
	LDX #$09D4 : JSR inc_reserve ; reserve tanks

	LDA #$0002 : STA $12      ; other supplies increment value per frame
	LDX #$09C6 : JSR inc_item ; missiles
	LDX #$09CA : JSR inc_item ; super missiles
	LDX #$09CE : JSR inc_item ; power bombs

	TYA                ; hang onto fill-state result
	PLY : PLX          ; restore regs
	RTL

inc_item:
	LDA $0000,X        ; current value
	CMP $0002,X        ; max value
	BEQ inc_is_full    ; already full?  just exit out
	INY                ; not already full: mark as such
	CLC : ADC $12      ; add current increment value
	CMP $0002,X        ; is it full now?
	BCC inc_item_write ; less than full: only save back to current
	LDA $0002,X        ; equal or overfull: set to full exactly
inc_item_write:
	STA $0000,X        ; write new (calculated or max) value to current
inc_is_full:
	RTS                ; return

;;; reserve current / max is inverted in RAM compared to other items
inc_reserve:
	LDA $0002,X        ; current value
	CMP $0000,X        ; max value
	BEQ inc_reserve_is_full    ; already full?  just exit out
	INY                ; not already full: mark as such
	CLC : ADC $12      ; add current increment value
	CMP $0000,X        ; is it full now?
	BCC inc_reserve_write ; less than full: only save back to current
	LDA $0000,X        ; equal or overfull: set to full exactly
inc_reserve_write:
	STA $0002,X        ; write new (calculated or max) value to current
inc_reserve_is_full:
	RTS                ; return

warnpc $a1f4ff
