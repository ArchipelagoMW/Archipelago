hirom

org $C8DDC2

db $CD, $CF, $03	;Run event index 03CF
db $DE, $43			;set up reward
db $DF				;call text handler
db $A2, $73			;Turn on bit 08 at address 0x7e0a22
db $FF				;End Event