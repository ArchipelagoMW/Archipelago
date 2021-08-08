;;; allows to leave boss rooms as soon as the boss is dead
;;; instead of having to wait for the drops
;;;
;;; Compiles with asar

arch snes.cpu
lorom

!mark_boss = $8081a6

org $A7AFAD
	jml kraid_death

org $A7DDBC
	jsl phantoon_death

org $A59621
	jsl draygon_death

org $A6C590
	jsl ridley_death	; (actually after some explosions instead of 0 HP check)

org $a1f500
kraid_death:
	LDA $0FA8 : CMP #$C537	; vanilla comparison
	beq .dead
	jml $a7afb3		; go to vanilla branching
.dead:
	lda #$0001 : jsl !mark_boss
	jml $a7afb5		; go to "dead" branch

phantoon_death:
	JSL $8090CB		; hijacked code
	lda #$0001 : jsl !mark_boss
	rtl

draygon_death:
	lda #$0001 : jsl !mark_boss
	LDA $7E8000		; hijacked code
	rtl

ridley_death:
	lda #$0001 : jsl !mark_boss
	LDA $7E7836		; hijacked code
	rtl

warnpc $a1f54f

org $a7d4e5
phantoon_door_spawn:
	bra .skip
org $a7d4ed
.skip:

org $a7db89
phantoon_door_restore:
	bra .skip
org $a7db91
.skip:
