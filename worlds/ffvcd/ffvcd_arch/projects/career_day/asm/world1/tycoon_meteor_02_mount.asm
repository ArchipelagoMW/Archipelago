hirom


;  Boco mount Tycoon 
org $C96E99

db $05, $03	; player bounce down
db $b1, $07	; set player sprite to boco
db $10 		; boco (player) pose
db $87, $0a	; hide old sprite
db $03		; move player down
db $a4, $ff	; event flag set
db $a5, $fe	; event flag clear
db $ff		; end flag


fillbyte $00 ; this is for cleanliness only, the rest of this code wouldn't be called
fill 14