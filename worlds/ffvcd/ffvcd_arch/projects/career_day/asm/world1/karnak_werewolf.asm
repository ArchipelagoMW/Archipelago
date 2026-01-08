hirom


; skip the event where they drive off the werewolf
org $C959E9

db $A4, $18			;Set Event Flag 118

db $FF
padbyte $00
pad $C95A42