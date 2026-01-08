hirom


; collecting adamantium
org $C8553B

db $83, $0A			;Sprite 083 do event: Hide
db $B4, $29			;Play Background Music Fanfare 1 (short)
db $CB, $5A, $00	;Clear Flag 2/3/4/5/5A 00
db $A2, $49			;Set Event Flag 049
		
db $FF								;End event

padbyte $00
pad $C8559F

; clear out cid/mid from appearing
org $CE6DFF
pad $CE6E0E

; set first part of conditional code to always be true 
; the old code was $FD, $48 corresponding to $000A1D bit 1
; the old code to trigger the fight was 
;   000A1D bit 1 set, 000A1D bit 2 unset
; now it's just 000A1D bit 2 unset and the first clause is always true
; in order to accommodate this, adamantoise.asm UNSETS the flag that adamantium get here does (A2, 49)
;  but the idea is that the player can't ever RE-SET that flag because adamantium no longer spawns
org $f055ef
db $FC, $FB
