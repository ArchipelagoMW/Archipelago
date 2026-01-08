hirom

org $C99E3A

db $DE, $1C				; set up reward
db $DF					; call text handler
db $A4, $51                     ;Turn on bit 02 at address 0x7e0a3e
db $FF                          ;End Event

pad $C99E4C