hirom


; admantoise fight
org $C85F9B

db $B9, $63							;Toggle Subtracitve Tint by 63
db $BE, $05							;Rumble effect of 05 magnitude
db $72								;Short pause
db $C5, $80							;<unknown>
db $BE, $00							;Rumble effect of 00 magnitude
db $BD, $0B, $FF					;Start Event Battle 0B
db $C5, $80
db $B5, $02
db $71
db $DE, $69 ; custom reward
db $DF
db $A2, $48							;Set Event Flag 048
db $A3, $49							;Set Event Flag 049. Unsets adamantium get as a flag

; CAREERDAY
; This is setting automatically upgrading the ship
db $A2, $4A                     ;Turn on bit 04 at address 0x7e0a1d
; db $A4, $FA                     ;Turn on bit 04 at address 0x7e0a53


db $CC, $14                 		;Custom destination flag 14
db $FF								;End event

padbyte $00
pad $C85FC9