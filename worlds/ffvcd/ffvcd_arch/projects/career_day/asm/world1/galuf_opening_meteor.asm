hirom


; galuf opening the tycoon meteor
org $C84BF5

db $B5, $3A							;Play Sound Effect Quick
db $BE, $05							;Rumble effect of 05 magnitude
db $70								;Very short pause
db $B5, $43							;Play Sound Effect Gate opens
db $F3, $27, $0F, $10, $04, $14		;Set Map Tiles 27 0F 10
db $BE, $00							;Rumble effect of 00 magnitude
db $DB								;Restore Player status
db $A2, $47							;Set Event Flag 047
		
db $FF								;End event

padbyte $00
pad $C84C72