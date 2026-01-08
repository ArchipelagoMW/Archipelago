hirom

org $C9BD29

db $DE, $27					; set up reward
db $DF						; call text handler
db $B5, $68                     ;Play Sound Effect Find item
db $A4, $6B                     ;Turn on bit 08 at address 0x7e0a41
db $FF                          ;End Event

pad $C9BD38