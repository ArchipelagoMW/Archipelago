 hirom


; sandworm fight
org $C88E5A

db $D8, $83, $09, $D8			;Unknown
db $84, $09						;Sprite 084 do event: Show
db $83, $10						;Sprite 083 do event: face up, left hand forward
db $84, $10						;Sprite 084 do event: face up, left hand forward
db $83, $09						;Sprite 083 do event: Show
db $84, $09						;Sprite 084 do event: Show
db $83, $03						;Sprite 083 do event: Move Down
db $CF, $02, $04				;Play next 04 bytes simultaneously 02 times
db $84, $03						;Sprite 084 do event: Move Down
db $83, $03						;Sprite 083 do event: Move Down
db $C7, $04						;Play next 04 bytes simultaneously
db $84, $03						;Sprite 084 do event: Move Down
db $83, $02						;Sprite 083 do event: Move Right
db $83, $24						;Sprite 083 do event: face down, right hand raised in
db $C7, $04						;Play next 04 bytes simultaneously
db $83, $02						;Sprite 083 do event: Move Right
db $84, $04						;Sprite 084 do event: Move Left
db $84, $04						;Sprite 084 do event: Move Left
db $CF, $04, $04				;Play next 04 bytes simultaneously 04 times
db $83, $03						;Sprite 083 do event: move down
db $84, $03						;Sprite 084 do event: move down
db $CB, $7A, $01				;Clear Flag 2/3/4/5/7A 01
db $CB, $7B, $01				;Clear Flag 2/3/4/5/7B 01
db $CA, $CB, $00				;Set Flag 2/3/4/5/CB 00
db $CA, $CC, $00				;Set Flag 2/3/4/5/CC 00
db $83, $26						;Sprite 083 do event: face up, right hand raised out
db $84, $22						;Sprite 084 do event: face down, left hand on head
db $83, $11						;Sprite 083 do event: face up, right hand forward
db $84, $11						;Sprite 084 do event: face up, right hand forward
db $72							;Shortish pause
db $A2, $3E						;Set Event Flag 03E
db $B5, $8F						;Play Sound Effect Sandworm
db $CD, $9B, $03				;Run event index 039B
db $BD, $0A, $FF				;Start Event Battle 0A
db $C5, $80
db $B5, $02
db $71
db $DE, $68 ; custom reward
db $DF
db $A2, $3C                     ;Turn on bit 10 at address 0x7e0a1b
db $FF							;End Event

padbyte $00
pad $C88F07 