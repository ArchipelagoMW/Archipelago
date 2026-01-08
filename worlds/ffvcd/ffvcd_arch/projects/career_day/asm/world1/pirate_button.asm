hirom


; this is the event teaching the player how the buttons work.
; simply enable the flag that disables this event and move on
org $C85313

db $A2, $13			;Set Event Flag 013
db $FF              ;End Event

padbyte $00
pad $C853A1


; speed up cutscene where 3 chests are
org $C90DD3
db $70
