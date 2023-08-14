.gba

.loadtable "data/charset.tbl"

.autoregion
.align 2

; Create OAM data for text
; Arguments:
;   r0: No gaps between objects if 0; otherwise, add spaces around the third object
CreateTextOAM:
    push {r4-r6, lr}
    mov r6, r0
    ldr r0, =attr0_wide | attr0_4bpp | attr0_y(146)
    ldr r1, =attr1_size(1) | attr1_x(8)
    ldr r2, =attr2_palette(3) | attr2_priority(0) | attr2_id(0x10C)
    ldr r3, =ucCntObj
    ldr r4, =OamBuf

    ldrb r5, [r3]
    lsl r5, r5, #3
    add r4, r4, r5

; 1st
    strh r0, [r4]
    strh r1, [r4, #2]
    strh r2, [r4, #4]
; 2nd
    add r1, #32
    add r2, #4
    add r4, #8
    strh r0, [r4]
    strh r1, [r4, #2]
    strh r2, [r4, #4]
; 3rd
    cmp r6, #0
    beq @@NoSpace3
    add r1, #8
@@NoSpace3:
    add r1, #32
    add r2, #4
    add r4, #8
    strh r0, [r4]
    strh r1, [r4, #2]
    strh r2, [r4, #4]
    ; 4th
    cmp r6, #0
    beq @@NoSpace4
    add r1, #8
@@NoSpace4:
    add r1, #32
    add r2, #0x130-0x114
    add r4, #8
    strh r0, [r4]
    strh r1, [r4, #2]
    strh r2, [r4, #4]
; 5th
    add r1, #32
    add r2, #4
    add r4, #8
    strh r0, [r4]
    strh r1, [r4, #2]
    strh r2, [r4, #4]
; 6th
    add r1, #32
    add r2, #0x20-4
    add r4, #8
    strh r0, [r4]
    strh r1, [r4, #2]
    strh r2, [r4, #4]
; 7th
    add r1, #32
    add r2, #4
    add r4, #8
    strh r0, [r4]
    strh r1, [r4, #2]
    strh r2, [r4, #4]

    ldrb r5, [r3]
    add r5, #7
    strb r5, [r3]

    pop {r4-r6, pc}
.pool

.definelabel @ObjectPalette3, 0x5000260


; Copy text sprites into the sprite table. On encountering 0xFE, blank spaces
; will be copied into the remaining space.
; Arguments:
;   r0: Pointer to 0xFE-terminated string
;   r1: Pointer to first letter destination
;   r2: Number of characters to copy.
; Returns:
;   r0: Pointer to byte after the last one loaded. If the end of the string was
;       hit, this will point to 0xFE.
LoadSpriteString:
    push {lr}
    push {r4-r6}
    mov r4, r0
    mov r5, r1
    mov r6, r2

; Override OBP3 color 2 with white.
; TODO: find where the overridden purple color is used and change methods if necessary
    ldr r1, =@ObjectPalette3 + 4
    ldr r0, =0x7FFF
    strh r0, [r1]

@@LoadFromString:
    ldrb r0, [r4]
    cmp r0, #0xFE
    beq @@LoadCharacter
    add r4, r4, #1

@@LoadCharacter:
    mov r1, r5
    bl LoadSpriteCharacter
    add r5, #0x20
    sub r6, r6, #1

@@CheckNChars:
    cmp r6, #0
    bne @@LoadFromString
@@Return:
    mov r0, r4
    pop {r4-r6}
    pop {pc}
.pool

; Load a character into the sprite table.
; Parameters:
;   r0: Pointer to character
;   r1: Pointer to destination
LoadSpriteCharacter:
    lsl r0, r0, #2
    ldr r2, =LetterToSpriteTile
    add r0, r2, r0
    ldr r0, [r0]

    ldr r2, =REG_DMA3SAD
    str r0, [r2]
    mov r0, r1
    str r0, [r2, #4]
    ldr r0, =dma_enable | dma_words(8)
    str r0, [r2, #8]
    ldr r0, [r2, #8]

    mov pc, lr
.pool


; Count up to the next 0xFE byte.
; Arguments:
;  r0: Pointer to a WL4 encoded, 0xFE-terminated string
; Returns:
;  r0: The length of the string
StrLen:
    mov r1, #0

@@Next:
    ldrb r2, [r0]
    cmp r2, #0xFE
    beq @@Return
    add r0, #1
    add r1, #1
    b @@Next

@@Return:
    mov r0, r1
    mov pc, lr
.pool


.align 4
LetterToSpriteTile:
    .word Text8x8_0, Text8x8_1, Text8x8_2, Text8x8_3, Text8x8_4, Text8x8_5, Text8x8_6, Text8x8_7
    .word Text8x8_8, Text8x8_9, Text8x8_A, Text8x8_B, Text8x8_C, Text8x8_D, Text8x8_E, Text8x8_F
    .word Text8x8_G, Text8x8_H, Text8x8_I, Text8x8_J, Text8x8_K, Text8x8_L, Text8x8_M, Text8x8_N
    .word Text8x8_O, Text8x8_P, Text8x8_Q, Text8x8_R, Text8x8_S, Text8x8_T, Text8x8_U, Text8x8_V
    .word Text8x8_W, Text8x8_X, Text8x8_Y, Text8x8_Z, Text8x8_A, Text8x8_B, Text8x8_C, Text8x8_D
    .word Text8x8_E, Text8x8_F, Text8x8_G, Text8x8_H, Text8x8_I, Text8x8_J, Text8x8_K, Text8x8_L
    .word Text8x8_M, Text8x8_N, Text8x8_O, Text8x8_P, Text8x8_Q, Text8x8_R, Text8x8_S, Text8x8_T
    .word Text8x8_U, Text8x8_V, Text8x8_W, Text8x8_X, Text8x8_Y, Text8x8_Z, Text8x8_Period, EmptyTile
    .word EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile
    .word EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile
    .word EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile
    .word EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile
    .word EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile
    .word EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile
    .word EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile
    .word EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile
    .word EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile
    .word EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile
    .word EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile
    .word EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile
    .word EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile
    .word EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile
    .word EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile
    .word EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile
    .word EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile
    .word EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile
    .word EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile
    .word EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile
    .word EmptyTile, Emptytile, Text8x8_Comma, Text8x8_Period, EmptyTile, EmptyTile, EmptyTile, EmptyTile
    .word EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile
    .word EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile
    .word EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile, EmptyTile

StrScreenFiller: .fill (TextBoxCharCount - 9), 0xFF
StrItemSent: .string "Sent "
StrItemTo: .string " to "
StrItemReceived: .string "Received "
StrItemFrom: .string "from "

; The ExtData tables will point into this area, which is intended to take up the
; rest of the space in the ROM.
.align 4
MultiworldStringDump: .byte 0
.endautoregion
