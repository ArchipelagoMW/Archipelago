hirom

org $C927F2

db $B5, $68			;Play Sound Effect Find item
db $DE, $44			;set up reward
db $DF				;call text handler
db $A2, $85			;Turn on bit 20 at address 0x7e0a24
db $FF				;End Event