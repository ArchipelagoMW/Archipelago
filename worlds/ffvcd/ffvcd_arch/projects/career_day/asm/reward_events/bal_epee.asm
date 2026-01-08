hirom

org $C95EF6

db $B5, $68			;Play Sound Effect Find item
db $DE, $46					; set up reward
db $DF						; call text handler
db $A4, $98			;Turn on bit 01 at address 0x7e0a47
db $FF				;End Event