.gba


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


.autoregion


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
