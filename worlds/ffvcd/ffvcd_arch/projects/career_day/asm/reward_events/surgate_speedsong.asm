hirom

org $C92706

db $80, $16                     ;Sprite 080 do event: face left, standing
db $DE, $1B				; set up reward
db $DF					; call text handler
db $80, $16                     ;Sprite 080 do event: face left, standing
db $71                          ;Short pause
db $80, $0A                     ;Sprite 080 do event: Hide
db $CB, $14, $00                ;Turn off bit 10 at address  0x7e0a56
db $A2, $E6                     ;Turn on bit 40 at address 0x7e0a30
db $FF                          ;End Event

pad $C92717