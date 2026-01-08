hirom

; changed for arch - this forces the first custom randomized reward ($3C)
; and ends the event immediately after
; chicken knife/brave blade event
org $c920c4

db $D0, $81, $80		;(Music) 81 80
db $B9, $61			;Toggle Subtracitve Tint by 61
db $75				;Extremely long pause
db $7D				;<Unknown>
db $C5, $E0			;<unknown>
db $F3, $07, $36, $44, $34	;Set Map Tiles 07 36 44 34
db $98, $98			;Sprite 198 do event: 98
db $98, $B2			;Sprite 198 do event: B2
db $11				;Player pose: face up, right hand forward
db $DD, $C7, $DD, $A2		;Unknown
db $69			;Player or Sprite Pose
db $EF				;Noop
db $01				;Player Move Up
db $EF				;Noop
db $69			;Player or Sprite Pose
db $79				;'The Crash Event'
db $11				;Player pose: face up, right hand forward
db $01				;Player Move Up
db $A2, $79			;Turn on bit 02 at address 0x7e0a23
db $95, $95			;Sprite 195 do event: 95
db $96, $95			;Sprite 196 do event: 95
db $95, $F3			;Sprite 195 do event: F3
db $47				;Player pose: face down, left hand up in
db $36				;Player pose: face down, eyes closed mouth open
db $44				;Player pose: face down, head lowered, left hand forward
db $6C			;Player or Sprite Pose
db $9D, $9D			;Sprite 19D do event: 9D
db $9D, $6C			;Sprite 19D do event: 6C
db $6C			;Player or Sprite Pose
db $6C			;Player or Sprite Pose
db $DD, $6C, $6C, $9D		;Unknown
db $6A			;Player or Sprite Pose
db $37				;Player pose: face down, eyes closed mouth open smiling
db $68			;Player or Sprite Pose
db $9D, $37			;Sprite 19D do event: face down, eyes closed mouth open smiling
db $37				;Player pose: face down, eyes closed mouth open smiling
db $37				;Player pose: face down, eyes closed mouth open smiling
db $37				;Player pose: face down, eyes closed mouth open smiling
db $37				;Player pose: face down, eyes closed mouth open smiling
db $37				;Player pose: face down, eyes closed mouth open smiling
db $37				;Player pose: face down, eyes closed mouth open smiling
db $37				;Player pose: face down, eyes closed mouth open smiling
db $37				;Player pose: face down, eyes closed mouth open smiling
db $37				;Player pose: face down, eyes closed mouth open smiling
db $00				;Player Hold
db $85, $09			;Sprite 085 do event: Show
db $73				;Long pause
db $A4, $00			;Turn on bit 01 at address 0x7e0a34

; choosing brave blade

db $DE, $3C						; set up reward
db $DF							; call text handler
db $CD, $47, $02					;Run event index 0247
db $FF								;End Event

padbyte $00
pad $C92116

; after choosing either

org $C9218E

db $85, $0A			;Sprite 085 do event: Hide
db $86, $09			;Sprite 086 do event: Show
db $D0, $81, $8F		;(Music) 81 8F
db $86, $03			;Sprite 086 do event: Move Down
db $86, $0A			;Sprite 086 do event: Show
db $C5, $E0			;<unknown>
db $F3, $07, $36, $44, $95	;Set Map Tiles 07 36 44 95
db $95, $CB			;Sprite 195 do event: CB
db $95, $95			;Sprite 195 do event: 95
db $79				;'The Crash Event'
db $79				;'The Crash Event'
db $CB, $79, $79		;Turn off bit 02 at address  0x7e1443
db $95, $95			;Sprite 195 do event: 95
db $CB, $95, $95		;Turn off bit 20 at address  0x7e1646
db $79				;'The Crash Event'
db $79				;'The Crash Event'
db $79				;'The Crash Event'
db $79				;'The Crash Event'
db $79				;'The Crash Event'
db $95, $95			;Sprite 195 do event: 95
db $95, $95			;Sprite 195 do event: 95
db $95, $F3			;Sprite 195 do event: F3
db $47				;Player pose: face down, left hand up in
db $36				;Player pose: face down, eyes closed mouth open
db $44				;Player pose: face down, head lowered, left hand forward
db $95, $95			;Sprite 195 do event: 95
db $95, $95			;Sprite 195 do event: 95
db $95, $79			;Sprite 195 do event: 79
db $79				;'The Crash Event'
db $79				;'The Crash Event'
db $79				;'The Crash Event'
db $79				;'The Crash Event'
db $95, $95			;Sprite 195 do event: 95
db $95, $95			;Sprite 195 do event: 95
db $95, $79			;Sprite 195 do event: 79
db $79				;'The Crash Event'
db $79				;'The Crash Event'
db $79				;'The Crash Event'
db $79				;'The Crash Event'
db $95, $95			;Sprite 195 do event: 95
db $95, $95			;Sprite 195 do event: 95
db $95, $A2			;Sprite 195 do event: A2
db $01				;Player Move Up
db $FF				;End Event

padbyte $00
pad $C921F4