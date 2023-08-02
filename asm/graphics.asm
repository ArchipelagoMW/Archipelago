.gba


; SelectDmapOamCreate returning
.org 0x807ca64
.area 0x807ca6c-.
        ldr r0, =PyramidScreenCreateReceivedItemOAM | 1
        bx r0
    .pool
.endarea

.autoregion
.align 2
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

.align 2
APLogoObj:
    .halfword 1, 0xF8, 0x41F8, 0x412E

.align 4
APLogoAnm:
    .word APLogoObj
    .byte 0xC8
    .fill 0, 3
    .word 0, 0
.endautoregion


.expfunc tile_no_4b(n), n * 0x20
.expfunc tile_coord_4b(x, y), tile_no_4b(x + 32 * y)

; Store letters and AP logo in some unused space in the tile data near the
; jewels and such. WL4 stores graphics data in 4bpp uncompressed 2D format.

; Spaces that will be used by text are now filled with empty tiles for clarity.

; Interestingly, graphics are considered as a stream of nybbles (that is, the
; left pixel is the least significant half byte), which means that the easiest
; way to write them is as eight words, such that the hexits appear mirrored in
; the assembly compared to how they look in the final game

.org BasicElementTiles + tile_coord_4b(12, 4)
EmptyTile:
    .fill 0x20 * 12, 0

.org BasicElementTiles + tile_coord_4b(14, 5)
APLogoTile1:
    .word 0x50000000
    .word 0xB5000000
    .word 0xBB555000
    .word 0xB5888500
    .word 0x58888850
    .word 0x58888850
    .word 0x58555850
    .word 0x05FFF500

APLogoTile2:
    .word 0x00000055
    .word 0x000005BB
    .word 0x00555BBB
    .word 0x05DDD5BB
    .word 0x5DDDDD5B
    .word 0x5DDDDD5B
    .word 0x5D555D55
    .word 0x05EEE500

.fill 0x20 * 8, 0

.org BasicElementTiles + tile_coord_4b(14, 6)
APLogoTile3:
    .word 0x5FFFFF50
    .word 0x5FFFFF50
    .word 0xC5FFFF50
    .word 0xCC5FF500
    .word 0xCC555000
    .word 0xCC500000
    .word 0xC5000000
    .word 0x50000000

APLogoTile4:
    .word 0x5EEEEE50
    .word 0x5EEEEE55
    .word 0x5EEEE5CC
    .word 0x05EE5CCC
    .word 0x00555CCC
    .word 0x00005CCC
    .word 0x000005CC
    .word 0x00000055

.fill 0x20 * 8, 0

.org 0x0869FC88
Text8x8_0: .skip 0x20
Text8x8_1: .skip 0x20
Text8x8_2: .skip 0x20
Text8x8_3: .skip 0x20
Text8x8_4: .skip 0x20
Text8x8_5: .skip 0x20
Text8x8_6: .skip 0x20
Text8x8_7: .skip 0x20
Text8x8_8: .skip 0x20
Text8x8_9: .skip 0x20

.org 0x08749870
Text8x8_A: .skip 0x20
Text8x8_B: .skip 0x20
Text8x8_C: .skip 0x20
Text8x8_D: .skip 0x20
Text8x8_E: .skip 0x20
Text8x8_F: .skip 0x20
Text8x8_G: .skip 0x20
Text8x8_H: .skip 0x20
Text8x8_I: .skip 0x20
Text8x8_J: .skip 0x20
Text8x8_K: .skip 0x20
Text8x8_L: .skip 0x20
Text8x8_M: .skip 0x20
Text8x8_N: .skip 0x20
Text8x8_O: .skip 0x20
Text8x8_P: .skip 0x20
Text8x8_Q: .skip 0x20
Text8x8_R: .skip 0x20
Text8x8_S: .skip 0x20
Text8x8_T: .skip 0x20
Text8x8_U: .skip 0x20
Text8x8_V: .skip 0x20
Text8x8_W: .skip 0x20
Text8x8_X: .skip 0x20
Text8x8_Y: .skip 0x20
Text8x8_Z: .skip 0x20
Text8x8_Period: .skip 0x20
Text8x8_Comma: .skip 0x20

; Repurpose the save tutorial and format it for arbitrary messages.
;
; The box is 14 tiles wide and 11 tiles tall.
; The first hexit of each halfword is the palette number (here always BGP 6),
; the last three are the index of the tile it displays.
; The text generating function places the bottom tile immediately after the top
; in memory, so each row gets alternating parity.

TextBoxCharCount equ 14 * (11 / 2)

.org SaveTutorialTilemap + 0x190
    .halfword 0x6080, 0x6082, 0x6084, 0x6086, 0x6088, 0x608A, 0x608C
    .halfword 0x608E, 0x6090, 0x6092, 0x6094, 0x6096, 0x6098, 0x609A

.org SaveTutorialTilemap + 0x1D0
    .halfword 0x6081, 0x6083, 0x6085, 0x6087, 0x6089, 0x608B, 0x608D
    .halfword 0x608F, 0x6091, 0x6093, 0x6095, 0x6097, 0x6099, 0x609B

.org SaveTutorialTilemap + 0x210
    .halfword 0x609C, 0x609E, 0x60A0, 0x60A2, 0x60A4, 0x60A6, 0x60A8
    .halfword 0x60AA, 0x60AC, 0x60AE, 0x60B0, 0x60B2, 0x60B4, 0x60B6

.org SaveTutorialTilemap + 0x250
    .halfword 0x609D, 0x609F, 0x60A1, 0x60A3, 0x60A5, 0x60A7, 0x60A9
    .halfword 0x60AB, 0x60AD, 0x60AF, 0x60B1, 0x60B3, 0x60B5, 0x60B7

.org SaveTutorialTilemap + 0x290
    .halfword 0x60B8, 0x60BA, 0x60BC, 0x60BE, 0x60C0, 0x60C2, 0x60C4
    .halfword 0x60C6, 0x60C8, 0x60CA, 0x60CC, 0x60CE, 0x60D0, 0x60D2

.org SaveTutorialTilemap + 0x2D0
    .halfword 0x60B9, 0x60BB, 0x60BD, 0x60BF, 0x60C1, 0x60C3, 0x60C5
    .halfword 0x60C7, 0x60C9, 0x60CB, 0x60CD, 0x60CF, 0x60D1, 0x60D3

.org SaveTutorialTilemap + 0x310
    .halfword 0x60D4, 0x60D6, 0x60D8, 0x60DA, 0x60DC, 0x60DE, 0x60E0
    .halfword 0x60E2, 0x60E4, 0x60E6, 0x60E8, 0x60EA, 0x60EC, 0x60EE

.org SaveTutorialTilemap + 0x350
    .halfword 0x60D5, 0x60D7, 0x60D9, 0x60DB, 0x60DD, 0x60DF, 0x60E1
    .halfword 0x60E3, 0x60E5, 0x60E7, 0x60E9, 0x60EB, 0x60ED, 0x60EF

.org SaveTutorialTilemap + 0x390
    .halfword 0x60F0, 0x60F2, 0x60F4, 0x60F6, 0x60F8, 0x60FA, 0x60FC
    .halfword 0x60FE, 0x6100, 0x6102, 0x6104, 0x6106, 0x6108, 0x610A

.org SaveTutorialTilemap + 0x3D0
    .halfword 0x60F1, 0x60F3, 0x60F5, 0x60F7, 0x60F9, 0x60FB, 0x60FD
    .halfword 0x60FF, 0x6101, 0x6103, 0x6105, 0x6107, 0x6109, 0x610B

; Not enough space, fill row with empty tiles
.org SaveTutorialTilemap + 0x410
    .fill 14 * 2, 0
