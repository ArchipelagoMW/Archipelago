.gba

.loadtable "data/charset.tbl"

.autoregion

LetterToSpriteGraphic:
    .word TextTile0
    .word TextTile1
    .word TextTile2
    .word TextTile3
    .word TextTile4
    .word TextTile5
    .word TextTile6
    .word TextTile7
    .word TextTile8
    .word TextTile9
    .word TextTileA
    .word TextTileB
    .word TextTileC
    .word TextTileD
    .word TextTileE
    .word TextTileF
    .word TextTileG
    .word TextTileH
    .word TextTileI
    .word TextTileJ
    .word TextTileK
    .word TextTileL
    .word TextTileM
    .word TextTileN
    .word TextTileO
    .word TextTileP
    .word TextTileQ
    .word TextTileR
    .word TextTileS
    .word TextTileT
    .word TextTileU
    .word TextTileV
    .word TextTileW
    .word TextTileX
    .word TextTileY
    .word TextTileZ

ItemSent: .string "Sent "
ItemTo: .string " to "
ItemReceived: .string "Received "
ItemFrom: .string " from "

; The ExtData tables will point into this area, which is intended to take up the
; rest of the space in the ROM.
.align 4
MultiworldStringDump: .byte 0
.endautoregion
