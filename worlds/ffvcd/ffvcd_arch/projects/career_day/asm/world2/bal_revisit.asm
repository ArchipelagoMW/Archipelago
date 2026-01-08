hirom


; Cutscene outside Bal after obtaining Hiryuu Plant
; This sets flag for Cara in bed cutscene 

org $C95A58

db $A4, $1D                     ;Set Event Flag 11D
db $83, $0A                     ;Sprite 083 do event: Hide (this is Cara being repositioned)
db $CB, $69, $02                ;Clear Flag 2/3/4/5/69 02
db $CA, $7B, $02                ;Set Flag 2/3/4/5/7B 02
db $A2, $67                     ;Set Event Flag 067 (this is speaking with Cara cutscene)
db $FF                          ;End Event

padbyte $00
pad $C95B6B