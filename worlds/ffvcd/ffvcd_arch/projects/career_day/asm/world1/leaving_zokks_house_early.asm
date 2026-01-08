hirom



; Removes the cutscene for visiting and leaving Zokk's house before he's there
org $C85C46

db $A4, $31			;Turn on bit 02 at address 0x7e0a3a
db $FF				;End Event

padbyte $00
pad $C85C82