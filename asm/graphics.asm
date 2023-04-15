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
    .halfword 0x7FFF, 0x72F5, 0x560E, 0x4169, 0x0000  ; Archipelago item

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
    ldr r0, =0x80000005
    str r0, [r1, #8]
    ldr r0, [r1, #8]

    mov pc, lr
.pool

.endautoregion
