hirom



org $C92F58

db $7C                          ;<Unknown>
db $80, $0A                     ;Sprite 080 do event: Hide
db $B4, $29                     ;Play Background Music Fanfare 1 (short)

db $DE, $14				; set up reward
db $DF					; call text handler
db $C5, $80                     ;<unknown>
db $B5, $02                     ;Play Sound Effect Void, Image
db $71
db $DE, $7B ; custom reward
db $DF

db $E4, $B4                     ;Unknown
db $06                          ;Player Bounce in Place
db $CB, $2F, $00                ;Turn off bit 80 at address  0x7e0a59
db $A5, $00                     ;Turn off bit 01 at address 0x7e0a34
db $A5, $01                     ;Turn off bit 02 at address 0x7e0a34
db $FF                          ;End Event

pad $C92F64


; finally... disable timer
org $c92f38
db $C8, $EE, $02		;Display Message/Text/Dialogue EE 02
db $A4, $00			;Turn on bit 01 at address 0x7e0a34
db $FF				;End Event
pad $c92f42

; remove 1 minute from odin's dialogue
org $E1d794
pad $E1d7A6

org $E1d7E9
db $A3, $01, $FF, $FF, $63, $88, $96, $92, $88, $8E, $96, $8C, $8D, $82, $85, $85, $96, $90, $7A, $87, $8D, $96, $8D, $88, $96, $8D, $8B, $92, $a2
pad $E1d80C