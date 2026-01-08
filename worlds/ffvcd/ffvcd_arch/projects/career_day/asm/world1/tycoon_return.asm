hirom


; Guard outside of tycoon (simply disables messages)
org $C91BC6

db $CD, $AE, $02	;Run event index 02AE
db $FF				;End Event

padbyte $00
pad $C91BCD

; Chancellor and faris/lenna balcony conversation
org $C8739B

db $CA, $09, $01		;Set Flag 2/3/4/5/09 01
db $CB, $06, $01		;Clear Flag 2/3/4/5/06 01
db $CB, $07, $01		;Clear Flag 2/3/4/5/07 01
db $CB, $08, $01		;Clear Flag 2/3/4/5/08 01
db $CB, $01, $01		;Clear Flag 2/3/4/5/01 01
db $CA, $0A, $01		;Set Flag 2/3/4/5/0A 01
db $CB, $09, $01		;Clear Flag 2/3/4/5/09 01
db $A5, $FE				;Clear Event Flag 1FE
db $A2, $2B				;Set Event Flag 02B
db $FF					;End Event
	
padbyte $00
pad $C874DD

; In the event the tycoon cutscene does occur, make it very short

org $C98BBF
db $86, $09
db $86, $03                     ;Sprite 086 do event: Move Down
db $01
db $01
db $01
db $73                          ;Short pause
db $80, $3F                     ;Sprite 080 do event: face down, looking left, eyes lowered
db $70                          ;Very short pause
db $C4, $03
db $73
db $CB, $01, $01                ;Turn off bit 02 at address  0x7e0a74
db $CA, $0A, $01                ;Turn on bit 04 at address  0x7e0a75
db $A2, $52                     ;Turn on bit 04 at address 0x7e0a1e
db $86, $0A                     ;Sprite 086 do event: Hide
db $80, $0A                     ;Sprite 086 do event: Hide
db $C3, $03
db $73
db $FF                          ;End Event

org $C98BE2