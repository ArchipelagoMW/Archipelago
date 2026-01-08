hirom

org $C953F5

db $C8, $0B, $03                ;Display Message/Text/Dialogue 0B 03
db $C5, $E0                     ;<unknown>
db $DE, $19				; set up reward
db $DF					; call text handler

db $A4, $11                     ;Turn on bit 02 at address 0x7e0a36
db $FF                          ;End Event

pad $C95402