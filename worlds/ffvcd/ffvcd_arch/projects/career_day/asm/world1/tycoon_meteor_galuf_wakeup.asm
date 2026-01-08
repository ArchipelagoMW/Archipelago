hirom


; this short circuits the galuf wakeup cutscene.
; lenna simply wakes up galuf and he and she leave the screen

org $C91754

db $72				;Medium pause
db $85, $09			;Sprite 085 do event: Show
db $85, $3E			;Sprite 085 do event: face up, both arms raised in
db $86, $0A			;Sprite 086 do event: Hide
db $84, $03			;Sprite 084 do event: Move Down
db $85, $02			;Sprite 085 do event: Move Right
db $CF, $02, $04		;Play next 04 bytes simultaneously 02 times
db $84, $03			;Sprite 084 do event: Move Down
db $85, $03			;Sprite 085 do event: Move Down
db $C7, $04			;Play next 04 bytes simultaneously
db $84, $04			;Sprite 084 do event: Move Left
db $85, $03			;Sprite 085 do event: Move Down
db $C7, $04			;Play next 04 bytes simultaneously
db $84, $03			;Sprite 084 do event: Move Down
db $85, $04			;Sprite 085 do event: Move Left
db $CF, $06, $04		;Play next 04 bytes simultaneously 06 times
db $84, $03			;Sprite 084 do event: Move Down
db $85, $03			;Sprite 085 do event: Move Down
db $C7, $04			;Play next 04 bytes simultaneously
db $85, $0A			;Sprite 085 do event: Hide
db $84, $0A			;Sprite 084 do event: Hide
db $A2, $10			;Set Event Flag 010
db $CB, $32, $00		;Clear Flag 2/3/4/5/32 00
db $CD, $42, $07		;Run event index 0742
; db $B7, $89			;Add/Remove character 89
db $CD, $7F, $05		;Run event index 057F
db $A5, $FE			;Clear Event Flag 1FE
db $CC, $01                  ;Custom destination flag 01
db $FF				;End Event

padbyte $00
pad $C9183D