.gba

.autoregion
.loadtable "data/charset.tbl"
ItemSent: .string "Sent "
ItemTo: .string " to "
ItemReceived: .string "Received "
ItemFrom: .string " from "

; The ExtData tables will point into this area, which is intended to take up the
; rest of the space in the ROM.
.align 4
MultiworldStringDump: .byte 0
.endautoregion
