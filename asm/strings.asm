.gba

.loadtable "data/charset.tbl"

.autoregion

.align 4
LetterToSpriteGraphic:
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
    .word TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp, TextTileSp, 0, TextTileSp

ItemSent: .string "Sent"
ItemTo: .string "to"
ItemReceived: .string "Received"
ItemFrom: .string "from"

; The ExtData tables will point into this area, which is intended to take up the
; rest of the space in the ROM.
.align 4
MultiworldStringDump: .byte 0
.endautoregion
