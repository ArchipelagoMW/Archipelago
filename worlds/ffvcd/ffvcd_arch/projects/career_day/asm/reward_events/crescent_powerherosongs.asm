hirom

org $C91FEB


db $A0, $02			;(Message) 02
db $B4, $29			;Play Background Music Fanfare 1 (short)
db $DE, $1D				; set up reward
db $DF					; call text handler
db $DE, $1E				; set up reward
db $DF					; call text handler
db $A2, $CE			;Turn on bit 40 at address 0x7e0a2d
db $A2, $CF			;Turn on bit 80 at address 0x7e0a2d
db $FF				;End Event

pad $C92001