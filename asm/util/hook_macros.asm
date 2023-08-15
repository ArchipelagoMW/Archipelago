.gba

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
