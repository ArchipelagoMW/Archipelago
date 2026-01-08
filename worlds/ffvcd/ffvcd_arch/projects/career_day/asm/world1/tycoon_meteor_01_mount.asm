hirom


;  Boco dismount Tycoon 
org $C84FD2

db $87, $09	; show sprite for choco. $8x refers to active sprites
db $87, $20	; choco pose
db $b1, $02	; set player sprite to butz
db $05, $01	; player bounce up
db $a5, $ff	; clear (some) event flag. as of now, not messing with these. if it was in the original function, keep 
db $ff		; end event (this event). this is a terminator. 

fillbyte $00 ; this is for cleanliness only, the rest of this code wouldn't be called
fill 18