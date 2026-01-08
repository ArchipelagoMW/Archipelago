hirom


; Apocalypse text box skip
org $C9C217

db $CD, $3E, $05		;Run event index 053E
db $FF					;End Event

padbyte $00
pad $C9C21D

; Apocalypse second text box skip
org $C99E60

db $81, $0A				;Sprite 081 do event: Hide
db $BD, $48, $FF		;Start Event Battle 48
db $DE, $A2 ; custom reward
db $DF
db $CD, $A6, $06		;Run event index 06A6
db $CD, $88, $06		;Run event index 0688
db $CB, $87, $03		;Turn off bit 80 at address  0x7e0ac4
db $A4, $73				;Turn on bit 08 at address 0x7e0a42
db $FF					;End Event

padbyte $00
pad $C99E79