hirom

org $C97E5B
db $DE, $37				; set up reward
db $DF					; call text handler
db $89, $0A                     ;Sprite 089 do event: Hide
db $A2, $9B                     ;Turn on bit 08 at address 0x7e0a27
db $FF                          ;End Event
pad $C97E66
org $C97E67
db $DE, $38				; set up reward
db $DF					; call text handler
db $8A, $0A                     ;Sprite 08A do event: Hide
db $A2, $9C                     ;Turn on bit 10 at address 0x7e0a27
db $FF                          ;End Event
pad $C97E72
org $C97E73
db $DE, $39				; set up reward
db $DF					; call text handler
db $8B, $0A                     ;Sprite 08B do event: Hide
db $A2, $9D                     ;Turn on bit 20 at address 0x7e0a27
db $FF                          ;End Event
pad $C97E7E
org $C97E7F
db $DE, $3A				; set up reward
db $DF					; call text handler
db $8C, $0A                     ;Sprite 08C do event: Hide
db $A2, $9E                     ;Turn on bit 40 at address 0x7e0a27
db $FF                          ;End Event
pad $C97E8A
org $C97E8B
db $DE, $3B				; set up reward
db $DF					; call text handler
db $8D, $0A                     ;Sprite 08D do event: Hide
db $A2, $9F                     ;Turn on bit 80 at address 0x7e0a27
db $FF                          ;End Event
pad $C97E96
