hirom

org $C97313
db $BE, $05                     ;Rumble effect of 05 magnitude
db $71                          ;Short pause
db $B5, $88                     ;Play Sound Effect Titan steps
db $F3, $13, $3B, $00, $45      ;Set Map Tiles 13 3B 00 45
db $BE, $00                     ;Rumble effect of 00 magnitude
db $A4, $0D                     ;Turn on bit 20 at address 0x7e0a35
db $FF                          ;End Event
pad $C9732D