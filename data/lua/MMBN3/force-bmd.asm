input equ blue.gba

.gba
;Put the name of your game 
;and the name of the output file (should be different)
;Always make sure the final number is 0x08000000 as that is the GBA game address in memory space
.open input,output.gba,0x08000000 

;In my files this is where I put assembler constants. You can use Name EQU Value format. 
;When the item on the left is encountered, it will be replaced with what is on the right.
;In C this is done as #define.
StartDialog EQU 0x080266fc

;==================CODE============================
;The .org directive here says this is where we will be writing data to. 
;This address provides some free space we can use in this game.
.org 0x08235156
	;The block of free space we have to use is 0xDAC long.
	;The .area directive will make sure we don't exceed this.
	.area 0xDAC

	;We want to make sure we are aligned on a proper boundary. The compiler will fail if we aren't.
	.align 4
	
	checkForNewItems:
		;Check a specific point in memory
		push r14 ;store return pointer
		;store our old registers
		push r4-r7
		push r0-r3
		ldr r3,=0x203FD00 ;address where we store the "items queued" bit
		; If the value of the memory at address r3 is 1, give new items. Otherwise, skip to return
		ldr r2,[r3]
		cmp r2,1h
		beq giveNewItems
		
		;Get back the old registers. It's like we were never here
		pop r0-r3 
		pop r4-r7
		
		;Here be the code we overwrote to inject our hook
		;r10 should still be 0x080004C0
		mov r0, r10
		ldr r0, [r0,50h]
		pop r15 ;return
	
	giveNewItems:
		push r14
		
		;Un-set our check bit
		mov r0,0x00
		ldr r3,=0x203FD00
		str r0,[r3]
		
		ldr r0,=0x203FD10
		
		mov r1,0x00
		mov r2,0x0
		ldr r3,=0x02004A88
		
		bl StartDialog ;08026716
		
		
		pop r15
	
	saveItemIndex:
		push r14
		push r0-r2
		
		;set r1 to memory address of RAM item index
		ldr r1,=0x203FD02
		;set r2 to memory address of SRAM save index
		ldr r2,=0xE0057FC
		;Load the value at r1 to r0
		ldrb r0,[r1]
		;Save r0 to the value at r2
		strb r0,[r2]
		
		ldr r1,=0x203FD03
		ldr r2,=0xE0057FD
		ldrb r0,[r1]
		strb r0,[r2]

		ldr r1,=0x203FD04
		ldr r2,=0xE0057FE
		ldrb r0,[r1]
		strb r0,[r2]

		ldr r1,=0x203FD05
		ldr r2,=0xE0057FF
		ldrb r0,[r1]
		strb r0,[r2]

		pop r0-r2

		;re-run the code we replaced and return
		add r5,r0,0
		add r4,r1,0
		pop r15

	loadItemIndex:
		push r14
		push r0-r2

		ldr r1,=0x203FD02
		ldr r2,=0xE0057FC
		ldrb r0,[r2]
		strb r0,[r1]

		ldr r1,=0x203FD03
		ldr r2,=0xE0057FD
		ldrb r0,[r2]
		strb r0,[r1]

		ldr r1,=0x203FD04
		ldr r2,=0xE0057FE
		ldrb r0,[r2]
		strb r0,[r1]

		ldr r1,=0x203FD05
		ldr r2,=0xE0057FF
		ldrb r0,[r2]
		strb r0,[r1]

		pop r0-r2
		;re-run the code we replaced and return
		mov r0,12h
		mov r1,66h
		pop r15

	.pool
.endarea

;====================HOOKS==========================
;Our hooking code(s) will go here
.org 0x080002E8 ;During the frame loop, before the dialog check
	bl checkForNewItems

.org 0x081327CA
	bl saveItemIndex

.org 0x08022080
	bl loadItemIndex
	
;Close file and finish
.close