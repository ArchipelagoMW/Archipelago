.gba

.loadtable "data/charset.tbl"

.autoregion
.align 2

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
    ldr r0, =0x84000008
    str r0, [r2, #8]
    ldr r0, [r2, #8]

    mov pc, lr
.pool

.align 4
LetterToSpriteTile:
    .word TextTile0,  TextTile1,  TextTile2,  TextTile3,  TextTile4,  TextTile5,  TextTile6,  TextTile7
    .word TextTile8,  TextTile9,  TextTileA,  TextTileB,  TextTileC,  TextTileD,  TextTileE,  TextTileF
    .word TextTileG,  TextTileH,  TextTileI,  TextTileJ,  TextTileK,  TextTileL,  TextTileM,  TextTileN
    .word TextTileO,  TextTileP,  TextTileQ,  TextTileR,  TextTileS,  TextTileT,  TextTileU,  TextTileV
    .word TextTileW,  TextTileX,  TextTileY,  TextTileZ,  TextTileAl, TextTileBl, TextTileCl, TextTileDl
    .word TextTileEl, TextTileFl, TextTileGl, TextTileHl, TextTileIl, TextTileJl, TextTileKl, TextTileLl
    .word TextTileMl, TextTileNl, TextTileOl, TextTilePl, TextTileQl, TextTileRl, TextTileSl, TextTileTl
    .word TextTileUl, TextTileVl, TextTileWl, TextTileXl, TextTileYl, TextTileZl, TextTileSp, TextTileSp
    .word TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp
    .word TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp
    .word TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp
    .word TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp
    .word TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp
    .word TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp
    .word TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp
    .word TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp
    .word TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp
    .word TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp
    .word TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp
    .word TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp
    .word TextTileSp, TextTileTsu, TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp
    .word TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp
    .word TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp
    .word TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp
    .word TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileTsuS, TextTileSp
    .word TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp
    .word TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp
    .word TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp
    .word TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp
    .word TextTileSp, TextTileLP, TextTileRP, TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp
    .word TextTileSp, TextTileSp, TextTileHyp, TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp
    .word TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp

StrItemSent: .string "Sent"
StrItemTo: .string "to"
StrItemReceived: .string "Received"
StrItemFrom: .string "from"

; The ExtData tables will point into this area, which is intended to take up the
; rest of the space in the ROM.
.align 4
MultiworldStringDump: .byte 0
.endautoregion
