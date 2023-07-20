.gba

.autoregion
.align 2
PassagePaletteTable:
    .halfword 0x7B3E, 0x723C, 0x6576, 0x58B0, 0x4C07  ; Entry passage
    .halfword 0x5793, 0x578D, 0x4B20, 0x2E40, 0x1160  ; Emerald passage
    .halfword 0x6B5F, 0x529F, 0x253F, 0x14B4, 0x14AE  ; Ruby passage
    .halfword 0x6BDF, 0x23DF, 0x139B, 0x1274, 0x0DAE  ; Topaz passage
    .halfword 0x7F5A, 0x7E94, 0x7D29, 0x50A5, 0x38A5  ; Sapphire passage
    .halfword 0x579F, 0x3B1F, 0x1A7F, 0x05DE, 0x00FB  ; Golden pyramid
    .halfword 0x3D9C, 0x327D, 0x2B28, 0x6A3B, 0x6DED  ; Archipelago item

.definelabel @ObjectPalette4, 0x5000280

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
    ldr r0, =@ObjectPalette4 + 0x296 - 0x280
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


; Store letters and AP logo in some unused space in the tile data near the
; jewels and such. WL4 stores graphics data in 4bpp uncompressed 2D format.

; Spaces that will be used by text are now filled with empty tiles for clarity.

; Interestingly, graphics are considered as a stream of nybbles (that is, the
; left pixel is the least significant half byte), which means that the easiest
; way to write them is as eight words, such that the hexits appear mirrored in
; the assembly compared to how they look in the final game

.org 0x8401C68
EmptyTile:
    .fill 0x20 * 12, 0

.org 0x84020A8
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

.org 0x84024A8
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
