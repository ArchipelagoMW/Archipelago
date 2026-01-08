hirom


; Mid showing the book to Cid
org $C8810E

db $E0, $99						;Unknown
db $00							;Player Hold
db $9D, $1D						;Sprite 19D do event: face up, walking, right hand forward
db $00							;Player Hold
db $83, $55						;Sprite 083 do event: 55
db $04							;Player move Left
db $04							;Player move Left
db $04							;Player move Left
db $04							;Player move Left
db $03							;Player Move Down
db $71
db $83, $10
db $83, $02						;Sprite 083 do event: move right
db $83, $01						;Sprite 083 do event: move up
db $83, $02						;Sprite 083 do event: move right
db $83, $02						;Sprite 083 do event: move right
db $83, $02						;Sprite 083 do event: move right
db $83, $01						;Sprite 083 do event: move up
db $83, $0A						;Sprite 083 do event: hide
db $CB, $51, $01				;Clear Flag 2/3/4/5/51 01
db $A2, $36						;Set Event Flag 036
db $CB, $73, $01				;Clear Flag 2/3/4/5/73 01
db $CB, $74, $01				;Clear Flag 2/3/4/5/74 01
db $CB, $75, $01				;Clear Flag 2/3/4/5/75 01
db $CB, $76, $01				;Clear Flag 2/3/4/5/76 01
db $CC, $0E                  	;Custom destination flag 0E
db $FF							;End Event

padbyte $00
pad $C88270