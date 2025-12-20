.n64
.open "game.bin", 0xE0000000

.org 0xE0006878
	j 0xE00D0000
	nop
	
.org 0xE0055034
	j 0xE00D0100
	nop

.close