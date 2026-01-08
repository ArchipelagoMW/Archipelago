hirom


; small intro cutscene in ruined city
; this also sets all the other flags so you can go right to the end
org $C93843

db $D3, $83, $22, $13		;Sprite 83 set map position 10, 10
db $83, $09					;Sprite 083 do event: Show
db $A2, $3D					;Set Event Flag 03D
db $A2, $AB					;Set Event Flag 0AB ; first king tycoon
db $A2, $AE					;Set Event Flag 0AE	; second king tycoon
db $A4, $00					;Set Event Flag 100 ; third king tycoon
db $01
db $FF						;End event

padbyte $00
pad $C93888

; falling in the ruined city
org $C88FE0

db $01							;Player move up
db $C4, $04
db $E3, $D5, $00, $B3, $04, $00	;Inter-map cutscene? D5 00 B3 04 00
db $A5, $FE						;Clear Event Flag 1FE
db $D0, $81, $F0				;(Music) 81 F0
db $09							;Player Show
db $03							;Player move down
db $03							;Player move down
db $03							;Player move down
db $03							;Player move down
db $03							;Player move down
db $03							;Player move down
db $C3, $04						;Fade in Speed 10
db $DB							;Restore Player status
db $73
db $B4, $3D						;Play Background Music Musica Machina
db $CB, $CB, $00				;Clear Flag 2/3/4/5/CB 00
db $CB, $CC, $00				;Clear Flag 2/3/4/5/CC 00
db $CA, $01, $01				;Set Flag 2/3/4/5/01 01
db $CB, $0A, $01				;Clear Flag 2/3/4/5/0A 01
db $FF							;End event

padbyte $00
pad $C8916D