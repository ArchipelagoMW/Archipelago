hirom

org $C9524E

db $80, $02			;Sprite 080 do event: Move Right
db $A4, $17			;Turn on bit 80 at address 0x7e0a36
db $DE, $47			; set up reward
db $DF				; call text handler
db $80, $04			;Sprite 080 do event: Move Left
db $80, $24			;Sprite 080 do event: face down hand out

db $FF				;End Event