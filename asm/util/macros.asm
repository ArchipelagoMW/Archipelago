.gba

; Replaces some code with a call to a mod function.
; Unlike the other two hook macros, this doesn't set the link register, so this
; is cheaper to use if the hook ends with a branch.
.macro hook_manual, Start, End, HackFunction
    .org Start
    .area End-.
        ldr r0, =HackFunction
        mov pc, r0
    .pool
    .endarea
.endmacro

; Replaces a branch with a call to a mod function.
; This is for when the replaced code ends with an unconditional jump so that the
; pool afterward in the original code can also be replaced.
.macro hook_branch, Start, End, ReturnAddress, HackFunction
    .org Start
    .area End-.
        ldr r0, =ReturnAddress
        mov lr, r0
        ldr r0, =HackFunction
        mov pc, r0
    .pool
    .endarea
.endmacro

; Replace some code with a call to a mod function.
; This will return execution to the end of the code that was replaced.
.macro hook, Start, End, HackFunction
        hook_branch Start, End, End, HackFunction
.endmacro

; Load a function pointer into a register and call it. Since mod code is at the
; end of the ROM while vanilla code is at the beginning, this is needed for the
; large jumps between modded/vanilla subroutines
.macro call_using, register, Function
        ldr register, =@@Return | 1
        mov lr, register
        ldr register, =Function
        mov pc, register
    @@Return:
.endmacro

; Copy bits m-n inclusive from the source register into a destination register.
; They'll be shifted into the least significant position, and the most
; significant bits will all be cleared.
.macro get_bits, dst, src, msb, lsb
        lsl dst, src, #31-msb
        lsr dst, dst, #31 - (msb - lsb)
.endmacro

; Copy bit n from the source register into the least significant bit in the
; destination register. The most significant 31 bits will be cleared.
.macro get_bit, dst, src, bit
        get_bits dst, src, bit, bit
.endmacro

; Tile sizes and coordinates
sizeof_tile equ 0x20
.expfunc tile_no_4b(n), n * sizeof_tile
.expfunc tile_coord_4b(x, y), tile_no_4b(x + 32 * y)
