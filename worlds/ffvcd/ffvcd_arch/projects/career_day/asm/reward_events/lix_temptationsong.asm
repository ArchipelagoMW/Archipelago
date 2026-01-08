hirom

org $C92297

db $DE, $18				; set up reward
db $DF					; call text handler
db $A2, $D3                     ;Turn on bit 08 at address 0x7e0a2e
db $FF                          ;End Event

pad $C9229E