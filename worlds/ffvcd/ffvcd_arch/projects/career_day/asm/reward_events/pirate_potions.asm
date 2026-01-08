hirom

org $C99C9D
db $DE, $23				; set up reward
db $DF					; call text handler
db $B5, $68                     ;Play Sound Effect Find item
db $A4, $4E                     ;Turn on bit 40 at address 0x7e0a3d
db $FF                          ;End Event
pad $C99CA9