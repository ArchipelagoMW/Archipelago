hirom

org $C9F760

db $C5, $E0			;<unknown>
db $70				;Very short pause
db $B4, $29			;Play Background Music Fanfare 1 (short)
db $E4, $C9			;Unknown
db $48				;Player pose: garbage
db $0F				;<Unknown>
db $DE, $48 		; set up reward
db $DF				; call text handler
db $A4, $96			;Turn on bit 40 at address 0x7e0a46
db $FF				;End Event