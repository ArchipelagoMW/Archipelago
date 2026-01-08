hirom

org $C92010

db $C8, $14, $03                ;Display Message/Text/Dialogue 14 03
db $DE, $17				; set up reward
db $DF					; call text handler
db $A2, $D0                     ;Turn on bit 01 at address 0x7e0a2e
db $FF                          ;End Event

pad $C9201F