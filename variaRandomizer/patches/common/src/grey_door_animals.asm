lorom
arch snes.cpu

org $8f98d8
	dw pre_bt_escape_plm_set

org $8ffd00
pre_bt_escape_plm_set:
	db $44,$db,$08,$08,$10,$00,$42,$c8
	db $2e,$06,$ee,$90,$00,$00

warnpc $8ffd2f

org $8ffd30
	db $e3,$ee,$1d,$07,$00,$00,$00,$00

