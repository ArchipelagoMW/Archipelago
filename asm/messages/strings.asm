.gba

.autoregion
.align 2


.loadtable "data/charset.tbl"

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
