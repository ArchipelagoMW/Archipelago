hirom

org $C94C15
db $DE, $3E						; set up reward
db $DF							; call text handler
db $00, $00 						; do not add cabin


org $C94C36
db $DE, $3F						; set up reward
db $DF							; call text handler
db $00, $00 						; do not add cabin