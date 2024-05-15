.n64
.open "gl.z64", "gl_loop.z64", 0x80000000

.org 0x80000080
	jal 0xA4000518
	nop
	
.org 0x80000518
	sw ra, 0x0000 (sp)
	sw t1, 0x0004 (sp)
	la t2, 0xA4600004
	lwu t2, 0x0000 (t2)
	lui t1, 0x00FF
	lw t1, 0xE7FC (t1)
	add t2, t2, t1
	la t3, 0xA4600000
	lwu t3, 0x0000 (t3)
	lui t1, 0x007F
	lw t1, 0xE000 (t1)
	add t3, t3, t1
	li t1, 0x0000
	.loop:
	addiu t2, t2, 0x0004
	lwu t4, 0x0000 (t2)
	sw t4, 0x0000 (t3)
	addiu t3, t3, 0x0004
	addiu t1, t1, 0x0001
	blt t1, 0x0004, .loop
	nop
	lw t1, 0x0004 (sp)
	lw ra, 0x0000 (sp)
	lui t2, 0xA3F8
	lui t3, 0xA3F0
	jr ra
	nop
.close