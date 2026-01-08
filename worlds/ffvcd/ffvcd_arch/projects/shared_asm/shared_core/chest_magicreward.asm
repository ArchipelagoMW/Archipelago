hirom

; hardcode change the area that magic is currently read from
; the problem is that the internal magic names don't necessarily fit the 
; standard textbox upon chest reward
; so they need to be redirected to a separate data bank


; blue magic is a bit tricky
; there's a 4 address complete gap where its tracked
; so the offsets are different
; text area start for blue magic: $E78430 → 
; 'id' for blue magic start: $82 → $9F


org $C08AAF ; change magic textbox to be 24 chars instead of 6
db $18

org $C08A85
JML MagicIndexing

org !ADDRESS_magicreward
MagicIndexing:
lda $16a3
rep #$20
asl a
asl a
asl a
sta $0f
asl a
clc
adc $0f
tax
lda $06
sep #$20
JML $C08A96

org $C08A98
db $BF, $00, $78, $E7 ; $E77800

org $E77800
padbyte $FF
pad $E78700