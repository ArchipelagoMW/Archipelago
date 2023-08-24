.gba


; SelectDmapOamCreate() returning
.org 0x807CA64
.area 0x807CA6C-.
        ldr r0, =PyramidScreenCreateReceivedItemOAM | 1
        bx r0
    .pool
.endarea


.autoregion
.align 2


; On level select screen
; ----------------------


; Create the sprite for the item received.
PyramidScreenCreateReceivedItemOAM:
        ldr r0, =MultiworldState
        ldrb r0, [r0]
        cmp r0, #2
        bne @@Return

        ldr r3, =ucCntObj
        ldrb r5, [r3]
        ldr r4, =OamBuf
        lsl r0, r5, #3
        add r4, r4, r0

        ldr r0, =attr0_square | attr0_4bpp | attr0_y(104)
        ldr r2, =attr2_palette(0xF) | attr2_priority(0) | attr2_id(0x200)

        ldr r6, =IncomingItemID
        ldrb r6, [r6]
        get_bit r1, r6, 6
        cmp r1, #0
        bne @@JunkItem

    ; Jewel Pieces or CD
        add r5, #1

        get_bit r1, r6, 5
        cmp r1, #0
        bne @@CD

    ; Jewel pieces
        ldr r1, =attr1_size(1) | attr1_x(120 - 8)
        strh r0, [r4]
        strh r1, [r4, #2]
        strh r2, [r4, #4]
        b @@Return

    @@CD:
        sub r0, #8
        ldr r1, =attr1_size(2) | attr1_x(120 - 16)
        strh r0, [r4]
        strh r1, [r4, #2]
        strh r2, [r4, #4]
        b @@Return

    @@JunkItem:
        get_bits r1, r6, 3, 0
        lsl r1, #2
        ldr r7, =@@JunkJumpTable
        add r1, r7
        ldr r1, [r1]
        mov pc, r1

    .align 4
    @@JunkJumpTable:
        .word @@FullHealthItem
        .word @@BigBoardTrap  ; Wario transform
        .word @@Heart
        .word @@BigBoardTrap  ; Lightning damage

    @@FullHealthItem:
        ldr r1, =attr1_size(1) | attr1_x(120 - 8)
        strh r0, [r4]
        strh r1, [r4, #2]
        strh r2, [r4, #4]

        ldr r0, =attr0_wide | attr0_4bpp | attr0_y(104 - 8)
        mov r1, #attr1_size(0) | attr1_x(120 - 8)
        add r2, #2
        strh r0, [r4, #8]
        strh r1, [r4, #10]
        strh r2, [r4, #12]

        add r5, #2
        b @@Return

    @@Heart:
        ldr r1, =attr1_size(1) | attr1_x(120 - 8)
        strh r0, [r4]
        strh r1, [r4, #2]
        strh r2, [r4, #4]

        add r5, #1
        b @@Return

    @@BigBoardTrap:
        sub r0, #4
        ldr r1, =attr1_size(1) | attr1_x(120 - 12)
        strh r0, [r4]
        strh r1, [r4, #2]
        strh r2, [r4, #4]

        ldr r0, =attr0_tall | attr0_4bpp | attr0_y(104 - 4)
        ldr r7, =attr1_size(0) | attr1_x(120 + 4)
        add r2, #2
        strh r0, [r4, #8]
        strh r7, [r4, #10]
        strh r2, [r4, #12]

        ; Wario is padded on the left. Lightning on the right.
        cmp r6, #0x43
        beq @@BigBoardSpriteBottom
        sub r1, #8

    @@BigBoardSpriteBottom:
        ldr r0, =attr0_wide | attr0_4bpp | attr0_y(104 - 4 + 16)
        add r2, #1
        strh r0, [r4, #16]
        strh r1, [r4, #18]
        strh r2, [r4, #20]

        add r5, #3

    @@Return:
        strb r5, [r3]  ; Write object count back

    ; Return from SelectDmapOamCreate
        pop {r4-r7}
        pop {r0}
        bx r0
    .pool


; Load the background for the vanilla autosave tutorial.
LoadMessageBG:
        ldr r0, =REG_BG3CNT
        ldr r1, =bg_reg_32x32 | bg_sbb(0x1E) | bg_4bpp | bg_cbb(2) | bg_priority(0)
        strh r1, [r0]

        ; Miraculously, BGP 6 color 2 isn't used at all as far as I can tell
        ldr r0, =0x50000C4
        ldr r1, =0xFFFF
        strh r1, [r0]

        ldr r0, =REG_DMA3SAD
        ldr r1, =SaveTutorialTilemap
        str r1, [r0]
        ldr r1, =0x600F000
        str r1, [r0, #4]
        ldr r1, =dma_enable | dma_halfwords(0x800)
        str r1, [r0, #8]
        ldr r1, [r0, #8]

        ldr r1, =PortalTileset2
        str r1, [r0]
        ldr r1, =0x6008000
        str r1, [r0, #4]
        ldr r1, =dma_enable | dma_words(0x1000)
        str r1, [r0, #8]
        ldr r1, [r0, #8]

        mov pc, lr
    .pool


; Load the original pyramid background 3 graphics.
LoadPyramidBG3:
        ldr r0, =REG_BG3CNT
        ldr r1, =bg_reg_32x32 | bg_sbb(0x1E) | bg_4bpp | bg_cbb(0) | bg_priority(0)
        strh r1, [r0]

        ldr r0, =REG_DMA3SAD
        ldr r1, =PortalTilemap3
        str r1, [r0]
        ldr r1, =0x600F000
        str r1, [r0, #4]
        ldr r1, =dma_enable | dma_halfwords(0x800)
        str r1, [r0, #8]
        ldr r1, [r0, #8]

        mov pc, lr
    .pool


PassagePaletteTable:
    .halfword 0x7B3E, 0x723C, 0x6576, 0x58B0, 0x4C07  ; Entry passage
    .halfword 0x5793, 0x578D, 0x4B20, 0x2E40, 0x1160  ; Emerald passage
    .halfword 0x6B5F, 0x529F, 0x253F, 0x14B4, 0x14AE  ; Ruby passage
    .halfword 0x6BDF, 0x23DF, 0x139B, 0x1274, 0x0DAE  ; Topaz passage
    .halfword 0x7F5A, 0x7E94, 0x7D29, 0x50A5, 0x38A5  ; Sapphire passage
    .halfword 0x579F, 0x3B1F, 0x1A7F, 0x05DE, 0x00FB  ; Golden pyramid
    .halfword 0x3D9C, 0x327D, 0x2B28, 0x6A3B, 0x6DED  ; Archipelago item


; Set the end of object palette 4 to the colors matching the passage in r0
SetTreasurePalette:
        ldr r1, =PassagePaletteTable
        lsl r2, r0, #2
        add r0, r2, r0
        lsl r0, r0, #1
        add r0, r1, r0

    ; DMA transfer - 5 halfwords from palette table entry
        ldr r1, =REG_DMA3SAD
        str r0, [r1]
        ldr r0, =ObjectPalette4 + 0x296 - 0x280
        str r0, [r1, #4]
        ldr r0, =dma_enable | dma_halfwords(5)
        str r0, [r1, #8]
        ldr r0, [r1, #8]

        mov pc, lr
    .pool


; In level
; --------


; Create OAM data for text
; Parameters:
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
; Parameters:
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
; Parameters:
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


.endautoregion
