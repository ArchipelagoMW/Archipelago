hirom



; Removes cutscene upon returning to the pirate's cove
org $C99B1E

db $A4, $4D			;Turn on bit 20 at address 0x7e0a3d
db $FF				;End Event

padbyte $00
pad $C99B26