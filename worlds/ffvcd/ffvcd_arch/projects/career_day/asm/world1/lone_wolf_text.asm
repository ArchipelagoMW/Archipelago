hirom


; Disable extra text after freeing lone wolf
org $C9312F

db $80, $03			;Sprite 080 do event: Move Down
db $80, $03			;Sprite 080 do event: Move Down
db $80, $03			;Sprite 080 do event: Move Down
db $10				;Player pose: face up, left hand forward
db $F0, $9F, $01	;Yes/No Dialogue box (message is 9F 01)
db $CD, $C0, $02	;Run event index 02C0
db $FF				;End Event

db $00, $00, $00	;Display Message/Text/Dialogue A1 81
db $80, $01			;Sprite 080 do event: Move Up
db $80, $01			;Sprite 080 do event: Move Up
db $80, $01			;Sprite 080 do event: Move Up
db $80, $24			;Sprite 080 do event: face down, right hand raised in
db $14				;Player pose: face down, left hand forward
db $FF				;End Event

db $80, $01			;Sprite 080 do event: Move Up
db $80, $01			;Sprite 080 do event: Move Up
db $80, $01			;Sprite 080 do event: Move Up
db $80, $24			;Sprite 080 do event: face down, right hand raised in
db $CD, $87, $03	;Run event index 0387
db $B5, $8E			;Play Sound Effect Treasure chest
db $F4, $00			;Unknown
db $FE				;Noop
db $20				;Player pose: face down, left hand raised out
db $07				;<Unknown>
db $17				;Player pose: face left, down hand backward
db $01				;Player Move Up
db $04				;Player move Left
db $12				;Player pose: face right, standing
db $CE, $04, $02		;Play next 02 bytes 04 times
db $80, $03			;Sprite 080 do event: Move Down
db $80, $02			;Sprite 080 do event: Move Right
db $80, $02			;Sprite 080 do event: Move Right
db $CE, $04, $02		;Play next 02 bytes 04 times
db $80, $01			;Sprite 080 do event: Move Up
db $80, $01			;Sprite 080 do event: Move Up
db $80, $01			;Sprite 080 do event: Move Up
db $80, $0A			;Sprite 080 do event: Hide
db $A2, $9A			;Turn on bit 04 at address 0x7e0a27
db $A2, $06			;Turn on bit 40 at address 0x7e0a14
db $CB, $D6, $00	;Turn off bit 40 at address  0x7e0a6e
db $FF				;End Event


padbyte $00
pad $C93197