hirom

; the below code disables gauge changing. it is always on, value #$80, loaded upon every battle.
; the address it loads from is the bitwise config option in WRAM $7E0973
org $C104f7
lda #$80
nop
nop
nop
nop
nop
