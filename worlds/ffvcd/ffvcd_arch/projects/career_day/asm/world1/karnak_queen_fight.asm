hirom


; Instantly start the fight with Queen Karnak
org $C9707A

db $01				;Player move up
db $01				;Player move up
db $CD, $10, $04	;Run event index 0410
db $85, $0A			
db $86, $09
db $BD, $07, $FF	;Start Event Battle 07
db $B4, $18			;Play Background Music The Fired Powered Ship
db $C5, $80                     ;<unknown>
db $B5, $02                     ;Play Sound Effect Void, Image
db $71
db $C5, $80
db $B5, $02
db $71
db $DE, $66 ; custom reward
db $DF
db $CA, $81, $01	;Set Flag 2/3/4/5/81 01
db $CB, $80, $01	;Clear Flag 2/3/4/5/80 01
db $A2, $2F			;Set Event Flag 02F
db $FF				;End Event

padbyte $00
pad $C97079