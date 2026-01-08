hirom 

org $C96EB4
db $DE, $22				; set up reward
db $DF					; call text handler
db $A4, $26                     ;Turn on bit 40 at address 0x7e0a38
db $FF                          ;End Event
pad $C96EC5