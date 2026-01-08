hirom


; changes the first hole cutscene in the pass to simply
; make the hole appear and then butz jumps back on boko

org $C85128

db $E3, $11, $00, $0E, $3B, $00	;Inter-map cutscene? 11 00 0E 3B 00
db $A5, $FF			;Clear Event Flag 1FF
db $B4, $23			;Play Background Music Four Valiant Hearts
db $C3, $0C			;Fade in Speed 0C
db $70				;Very short pause
db $77				;<Unknown>
db $01				;Player Move Up
db $B5, $3D			;Play Sound Effect Sudden stop
db $0C				;<Unknown>
db $01				;Player Move Up
db $01				;Player Move Up
db $01				;Player Move Up
db $0B				;<Unknown>
db $80, $09			;Sprite 080 do event: Show
db $0A				;Player Hide
db $81, $09			;Sprite 081 do event: Show
db $81, $4A			;Sprite 081 do event: garbage
db $81, $0B			;Sprite 081 do event: 0B
db $81, $05			;Sprite 081 do event: Bounce
db $81, $01			;Sprite 081 do event: Move Up
db $81, $05			;Sprite 081 do event: Bounce
db $81, $01			;Sprite 081 do event: Move Up
db $81, $05			;Sprite 081 do event: Bounce
db $81, $01			;Sprite 081 do event: Move Up
db $BE, $04			;Rumble effect of 04 magnitude
db $B5, $42			;Play Sound Effect Collision
db $71				;Short pause
db $BE, $00			;Rumble effect of 00 magnitude
db $81, $0B			;Sprite 081 do event: 0B
db $81, $45			;Sprite 081 do event: face down, looking left, pointing finger left
db $73				;Long pause
db $81, $24			;Sprite 081 do event: face down, right hand raised in
db $73				;Long pause
db $81, $32			;Sprite 081 do event: collapsed, facing left
db $73				;Long pause
db $BE, $05			;Rumble effect of 05 magnitude
db $70				;Very short pause
db $B4, $26			;Play Background Music Hurry! Hurry!
db $A4, $FE			;Set Event Flag 1FE
db $73				;Long pause
db $B5, $7E			;Play Sound Effect ?
db $BE, $09			;Rumble effect of 09 magnitude
db $F3, $0C, $39, $24		;Set Map Tiles 0C 39 24
db $D0, $D1, $D2		;(Music) D1 D2
db $D3, $D4, $E0, $E1		;Sprite D4 set map position E0, E1
db $E2, $E3			;Unknown
db $E4, $F0			;Unknown
db $F1, $F2			;Unknown
db $F3, $F4, $81, $4A		;Set Map Tiles F4 81 4A
db $80, $20			;Sprite 080 do event: face down, left hand raised out
db $71				;Short pause
db $81, $03			;Sprite 081 do event: Move Down
db $81, $03			;Sprite 081 do event: Move Down
db $81, $02			;Sprite 081 do event: Move Right
db $81, $03			;Sprite 081 do event: Move Down
db $81, $26			;Sprite 081 do event: face up, right hand raised out
db $81, $05			;Sprite 081 do event: Bounce
db $81, $04			;Sprite 081 do event: Move Left
db $81, $0A			;Sprite 081 do event: Hide
db $09				;Player Show
db $80, $0A			;Sprite 080 do event: Hide
db $FF				;End Event

padbyte $00
pad $C85204