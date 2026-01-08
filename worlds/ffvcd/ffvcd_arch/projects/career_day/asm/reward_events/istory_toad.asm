hirom

org $C958B7

db $B5, $7E					;Play Sound Effect ?
db $BE, $05					;Rumble effect of 05 magnitude
db $71						;Short pause
db $F3, $5A, $14, $22, $37	;Set Map Tiles 5A 14 22 37
db $C2, $37					;Map 37
db $A3, $E2					;Turn off bit 04 at address 0x7e0a30
db $A1, $37					;Run Shop Mirage Weapon 2 (I think)
db $92, $37					;Sprite 192 do event: face down, eyes closed mouth open smiling
db $71						;Short pause
db $BE, $00					;Rumble effect of 00 magnitude
db $74						;Very long pause
db $16						;Player pose: face left, standing
db $92, $09					;Sprite 192 do event: Show
db $92, $4A					;Sprite 192 do event: garbage
db $92, $0B					;Sprite 192 do event: 0B
db $B5, $0A					;Play Sound Effect Bouncing
db $92, $05					;Sprite 192 do event: Bounce
db $92, $00					;Sprite 192 do event: Hold
db $71						;Short pause
db $B5, $0A					;Play Sound Effect Bouncing
db $92, $05					;Sprite 192 do event: Bounce
db $92, $00					;Sprite 192 do event: Hold
db $71						;Short pause
db $92, $0B					;Sprite 192 do event: 0B
db $92, $20					;Sprite 192 do event: face down, left hand raised out
db $71						;Short pause
db $B5, $0A					;Play Sound Effect Bouncing
db $92, $05					;Sprite 192 do event: Bounce
db $92, $01					;Sprite 192 do event: Move Up
db $B5, $0A					;Play Sound Effect Bouncing
db $92, $05					;Sprite 192 do event: Bounce
db $92, $01					;Sprite 192 do event: Move Up
db $72						;Medium pause
db $10						;Player pose: face up, left hand forward
db $B5, $0A					;Play Sound Effect Bouncing
db $92, $06					;Sprite 192 do event: Bounce
db $92, $01					;Sprite 192 do event: Move Up
db $70						;Very short pause
db $92, $0A					;Sprite 192 do event: Hide
db $73						;Long pause
db $04						;Player move Left
db $10						;Player pose: face up, left hand forward
db $71						;Short pause
db $2F						;Player pose: face up, head lowered
db $73						;Long pause
db $B5, $68					;Play Sound Effect Find item
db $10						;Player pose: face up, left hand forward
db $70						;Very short pause
db $0C						;<Unknown>
db $05						;Player Bounce in Place
db $03						;Player Move Down
db $0B						;<Unknown>
db $72						;Medium pause
db $DE, $42					;set up reward
db $DF						;call text handler
db $A4, $16					;Turn on bit 40 at address 0x7e0a36
db $FF						;End Event