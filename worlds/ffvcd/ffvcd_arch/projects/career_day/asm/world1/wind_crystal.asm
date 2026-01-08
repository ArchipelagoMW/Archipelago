hirom


; Make the wind crystal job acquisition more efficient
org $C8563B

db $01              ;Player move up
db $01              ;Player move up
db $01              ;Player move up
db $73              ;Pause for a bit
db $D3, $87, $2D, $10		;Sprite 87 set map position 2D, 10
db $D3, $86, $2D, $10		;Sprite 86 set map position 2D, 10
db $D3, $87, $2D, $11		;Sprite 87 set map position 2D, 11
db $D3, $86, $2D, $11		;Sprite 86 set map position 2D, 11
db $D3, $87, $2D, $10		;Sprite 87 set map position 2D, 10
db $D3, $86, $2D, $10		;Sprite 86 set map position 2D, 10
db $D3, $87, $2D, $0F		;Sprite 87 set map position 2D, 0F
db $D3, $86, $2D, $0F		;Sprite 86 set map position 2D, 0F
db $D3, $87, $2D, $10		;Sprite 87 set map position 2D, 10
db $D3, $86, $2D, $10		;Sprite 86 set map position 2D, 10
db $D3, $87, $2D, $0F		;Sprite 87 set map position 2D, 0F
db $D3, $86, $2D, $0F		;Sprite 86 set map position 2D, 0F
db $D3, $87, $2D, $0E		;Sprite 87 set map position 2D, 0E
db $D3, $86, $2D, $0E		;Sprite 86 set map position 2D, 0E
db $D3, $87, $2D, $0F		;Sprite 87 set map position 2D, 0F
db $D3, $86, $2D, $0F		;Sprite 86 set map position 2D, 0F
db $D3, $87, $2D, $0E		;Sprite 87 set map position 2D, 0E
db $D3, $86, $2D, $0E		;Sprite 86 set map position 2D, 0E
db $D3, $87, $2D, $0D		;Sprite 87 set map position 2D, 0D
db $D3, $86, $2D, $0D		;Sprite 86 set map position 2D, 0D
db $D3, $87, $2D, $0E		;Sprite 87 set map position 2D, 0E
db $D3, $86, $2D, $0E		;Sprite 86 set map position 2D, 0E
db $D3, $87, $2D, $0D		;Sprite 87 set map position 2D, 0D
db $D3, $86, $2D, $0D		;Sprite 86 set map position 2D, 0D
db $D3, $87, $2D, $0C		;Sprite 87 set map position 2D, 0C
db $D3, $86, $2D, $0C		;Sprite 86 set map position 2D, 0C
db $D3, $87, $2D, $0D		;Sprite 87 set map position 2D, 0D
db $D3, $86, $2D, $0D		;Sprite 86 set map position 2D, 0D
db $D3, $87, $2D, $0C		;Sprite 87 set map position 2D, 0C
db $D3, $86, $2D, $0C		;Sprite 86 set map position 2D, 0C
db $D3, $87, $2D, $0B		;Sprite 87 set map position 2D, 0B
db $D3, $86, $2D, $0B		;Sprite 86 set map position 2D, 0B
db $87, $0A			;Sprite 087 do event: Hide
db $86, $0A			;Sprite 086 do event: Hide
db $83, $4D			;Sprite 083 do event: garbage
db $83, $38			;Sprite 083 do event: face down, squatting
db $83, $3F			;Sprite 083 do event: face down, looking left, eyes lowered
db $D3, $88, $2A, $11		;Sprite 88 set map position 2A, 11
db $D3, $89, $29, $13		;Sprite 89 set map position 29, 13
db $D3, $8A, $29, $15		;Sprite 8A set map position 29, 15
db $D3, $8B, $30, $16		;Sprite 8B set map position 30, 16
db $D3, $8C, $31, $14		;Sprite 8C set map position 31, 14
db $D3, $8D, $30, $11		;Sprite 8D set map position 30, 11
db $B2, $04			;Pause for 04 cycles
db $D3, $88, $2A, $12		;Sprite 88 set map position 2A, 12
db $D3, $89, $29, $14		;Sprite 89 set map position 29, 14
db $D3, $8A, $2A, $16		;Sprite 8A set map position 2A, 16
db $D3, $8B, $2F, $17		;Sprite 8B set map position 2F, 17
db $D3, $8C, $31, $15		;Sprite 8C set map position 31, 15
db $D3, $8D, $30, $12		;Sprite 8D set map position 30, 12
db $B2, $04			;Pause for 04 cycles
db $D3, $88, $2A, $13		;Sprite 88 set map position 2A, 13
db $D3, $89, $29, $15		;Sprite 89 set map position 29, 15
db $D3, $8A, $2B, $17		;Sprite 8A set map position 2B, 17
db $D3, $8C, $30, $16		;Sprite 8C set map position 30, 16
db $D3, $8D, $30, $13		;Sprite 8D set map position 30, 13
db $B2, $04			;Pause for 04 cycles
db $D3, $88, $2A, $14		;Sprite 88 set map position 2A, 14
db $D3, $89, $2A, $16		;Sprite 89 set map position 2A, 16
db $D3, $8D, $30, $14		;Sprite 8D set map position 30, 14
db $B2, $04			;Pause for 04 cycles
db $D3, $88, $2B, $15		;Sprite 88 set map position 2B, 15
db $D3, $8D, $2F, $15		;Sprite 8D set map position 2F, 15
db $71				;Short pause
db $C7, $0C			;Play next 0C bytes simultaneously
db $88, $02			;Sprite 088 do event: Move Right
db $89, $02			;Sprite 089 do event: Move Right
db $8A, $02			;Sprite 08A do event: Move Right
db $8B, $04			;Sprite 08B do event: Move Left
db $8C, $04			;Sprite 08C do event: Move Left
db $8D, $04			;Sprite 08D do event: Move Left
db $71				;Short pause
db $C7, $0C			;Play next 0C bytes simultaneously
db $88, $02			;Sprite 088 do event: Move Right
db $89, $02			;Sprite 089 do event: Move Right
db $8A, $01			;Sprite 08A do event: Move Up
db $8B, $01			;Sprite 08B do event: Move Up
db $8C, $04			;Sprite 08C do event: Move Left
db $8D, $04			;Sprite 08D do event: Move Left
db $71
db $C7, $0C			;Play next 0C bytes simultaneously
db $88, $03			;Sprite 088 do event: Move Down
db $89, $02			;Sprite 089 do event: Move Right
db $8A, $02			;Sprite 08A do event: Move Right
db $8B, $04			;Sprite 08B do event: Move Left
db $8C, $04			;Sprite 08C do event: Move Left
db $8D, $03			;Sprite 08D do event: Move Down
db $C7, $0C         ;Play next 0C bytes simultaneously
db $88, $0A			;Sprite 088 do event: Hide
db $89, $0A			;Sprite 089 do event: Hide
db $8A, $0A			;Sprite 08A do event: Hide
db $8B, $0A			;Sprite 08B do event: Hide
db $8C, $0A			;Sprite 08C do event: Hide
db $8D, $0A			;Sprite 08D do event: Hide
db $72
db $23				;Player pose: face up, left hand forward
db $DE, $01		; set up reward  		; <---reward--->
db $DF			; call text handler  	; <---reward--->
db $DE, $02		; set up reward  		; <---reward--->
db $DF			; call text handler  	; <---reward--->
db $DE, $03		; set up reward  		; <---reward--->
db $DF			; call text handler  	; <---reward--->
db $DE, $04		; set up reward  		; <---reward--->
db $DF			; call text handler  	; <---reward--->
db $DE, $05		; set up reward  		; <---reward--->
db $DF			; call text handler  	; <---reward--->
db $DE, $06		; set up reward  		; <---reward--->
db $DF			; call text handler  	; <---reward--->
db $B4, $29			;Play Background Music Fanfare 1 (short)
db $75
db $75
db $74
db $CB, $4B, $00	;Clear Flag 2/3/4/5/4B 00
db $CB, $4C, $00	;Clear Flag 2/3/4/5/4C 00
db $CB, $4D, $00	;Clear Flag 2/3/4/5/4D 00
db $CB, $4E, $00	;Clear Flag 2/3/4/5/4E 00
db $CB, $4F, $00	;Clear Flag 2/3/4/5/4F 00
db $CB, $50, $00	;Clear Flag 2/3/4/5/50 00
db $A2, $17			;Set Event Flag 017
db $CA, $7E, $00	;Set Flag 2/3/4/5/7E 00
db $A4, $DC                     ;Set Event Flag 1DC ; DISABLED in v0.75, re-enabled 1.0, appears to only be tied to 4 crystal barriers on world map in world 1. MOVED FROM INTRO CUTSCENE
db $A5, $FE			;Clear Event Flag 1FE
db $B4, $08			;Play Background Music The Prelude
db $FF              ;End Event

padbyte $00
pad $C85B8F