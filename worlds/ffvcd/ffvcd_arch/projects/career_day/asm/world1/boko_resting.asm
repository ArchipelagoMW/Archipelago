hirom



; Removes cutscene upon discovering boko resting in the pirate's cove
org $C96E58

db $A4, $24				;Turn on bit 10 at address 0x7e0a38
db $FF					;End Event

padbyte $00
pad $C96E7A