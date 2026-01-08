hirom



; Removes cutscene upon discovering pirate's cove
org $C8520C

db $A5, $FE						;Clear Event Flag 1FE
db $76							;<Unknown>
db $D3, $80, $20, $23			;Sprite 80 set map position 20, 23
db $80, $09						;Sprite 080 do event: Show
db $80, $24                     ;Sprite 080 do event: face down, right hand raised in
db $B1, $02						;Set Player Sprite 02
db $09							;Player Show
db $05							;Player Bounce in Place
db $04							;Player move Left
db $12							;Player pose: face right, standing
db $70							;Very short pause
db $80, $10                     ;Sprite 080 do event: face up, left hand forward
db $80, $02                     ;Sprite 080 do event: Move Right
db $80, $26                     ;Sprite 080 do event: face up, right hand raised out
db $80, $11                     ;Sprite 080 do event: face up, right hand forward
db $02              			;Player move right
db $01              			;Player move up
db $C4, $08						;Fade out Speed 08
db $74							;Very long pause
db $E1, $13, $00, $14, $36, $00	;Return from cutscene? 13 00 14 36 00
db $DB							;Restore Player status
db $C3, $0C						;Fade in Speed 0C
db $73							;Long pause
db $A4, $1A						;Set Event Flag 11A
db $A4, $1B						;Set Event Flag 11B
db $CA, $34, $00				;Set Flag 2/3/4/5/34 00
db $A5, $FF						;Clear Event Flag 1FF
db $FF                          ;End Event

padbyte $00
pad $C85286

; Leaving Pirate's Cove before reaching boat
org $C852C6

db $71				;Short pause
db $12				;Player pose: face right, standing
db $80, $55			;Sprite 080 do event: 55
db $70				;Very short pause
db $80, $26			;Sprite 080 do event: face up, right hand raised out
db $70				;Very short pause
db $05				;Player Bounce in Place
db $02				;Player Move Right
db $0A				;Player Hide
db $B1, $07			;Set Player Sprite 07
db $80, $0A			;Sprite 080 do event: Hide
db $09				;Player Show
db $14				;Player pose: face down, left hand forward
db $70				;Very short pause
db $03				;Player Move Down
db $A5, $1B			;Turn off bit 08 at address 0x7e0a37
db $CB, $34, $00	;Turn off bit 10 at address  0x7e0a5a
db $A4, $FF			;Turn on bit 80 at address 0x7e0a53
db $77				;<Unknown>
db $FF				;End Event

padbyte $00
pad $C852E6

; Non first time entering the pirate's cove
org $C85287

db $76							;<Unknown>
db $D3, $80, $20, $23			;Sprite 80 set map position 20, 23
db $80, $09						;Sprite 080 do event: Show
db $0A							;Player Hide
db $70							;Very short pause
db $80, $24						;Sprite 080 do event: face down, right hand raised in
db $72							;Medium pause
db $B1, $02						;Set Player Sprite 02
db $DB							;Restore Player status
db $09							;Player Show
db $05							;Player Bounce in Place
db $04							;Player move Left
db $70							;Very short pause
db $12							;Player pose: face right, standing
db $80, $26						;Sprite 080 do event: face up, right hand raised out
db $70							;Very short pause
db $71							;Short pause
db $80, $55						;Sprite 080 do event: 55
db $70							;Very short pause
db $80, $26						;Sprite 080 do event: face up, right hand raised out
db $70							;Very short pause
db $80, $10						;Sprite 080 do event: face up, left hand forward
db $C7, $03						;Play next 03 bytes simultaneously
db $80, $02						;Sprite 080 do event: Move Right
db $02							;Player Move Right
db $80, $26						;Sprite 080 do event: face up, right hand raised out
db $80, $11						;Sprite 080 do event: face up, right hand forward
db $71							;Short pause
db $01							;Player Move Up
db $E3, $13, $00, $14, $36, $00	;Inter-map cutscene? 13 00 14 36 00
db $C3, $08						;Fade in Speed 0C
db $74							;Very long pause
db $A4, $1B						;Turn on bit 08 at address 0x7e0a37
db $CA, $34, $00				;Turn on bit 10 at address  0x7e0a5a
db $A5, $FF						;Turn off bit 80 at address 0x7e0a53
db $FF							;End Event

padbyte $00
pad $C852C5