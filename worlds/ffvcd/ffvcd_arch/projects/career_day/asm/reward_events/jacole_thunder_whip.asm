hirom

org $C94B5C

db $B5, $8E					;Play Sound Effect Treasure chest
db $F3, $1A, $1D, $00, $12	;Set Map Tiles 1A 1D 00 12
db $DE, $45					; set up reward
db $DF						; call text handler
db $A2, $0B					;Turn on bit 08 at address 0x7e0a15
db $A4, $00					;Turn on bit 01 at address 0x7e0a34
db $FF						;End Event