hirom


; Carwen lady conversation
org $C86A13

db $C8, $6C, $01		;Display Message/Text/Dialogue 6C 01
db $A2, $AF				;Set Event Flag 0AF
db $8A, $09				;Sprite 08A do event: Show
db $CA, $88, $00		;Set Flag 2/3/4/5/88 00
db $CA, $83, $00		;Set Flag 2/3/4/5/83 00

padbyte $00
pad $C86A57