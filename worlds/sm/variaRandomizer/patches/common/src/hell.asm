;;; permanent hell run
;;; compile with asar

lorom
arch snes.cpu

org $8fe893
	jsr add_heat_fx		; setup asm call

org $8ff410
add_heat_fx:
	phy
	ldy #$f761 : jsl $8dc4e9 ; spawn heat dmg fx
	ply
	ldx $07bb		; hijacked code
	rts
