hirom


; Cutscene and job acquisition after Karnak
org $C87F79

db $7C							;Stops the timer
db $C4, $0C						;Fade out Speed 0C
db $73
db $A5, $FF						;Clear Event Flag 1FF

db $CA, $9D, $02				;Set Flag 2/3/4/5/9D 02 (karnak weapon shop 2 turned on)

; disable for archipelago - lets the player re-enter karnak and fight
db $A5, $E4						;Set Event Flag 1E4
db $CA, $81, $01				;Clear Flag 2/3/4/5/81 01 

db $CA, $54, $01				;Clear Flag 2/3/4/5/54 01
db $CB, $51, $01				;Set Flag 2/3/4/5/51 01


db $A3, $30
db $A3, $31
db $A3, $32
db $A3, $33
db $A5, $19						;Set Event Flag 119


; inverted from fire crystal, restore NPCs in Karnak...?

db $CA, $58, $01				;Clear Flag 2/3/4/5/58 01
db $CA, $59, $01				;Clear Flag 2/3/4/5/59 01
db $CA, $5A, $01				;Clear Flag 2/3/4/5/5A 01
db $CA, $5B, $01				;Clear Flag 2/3/4/5/5B 01
db $CA, $5C, $01				;Clear Flag 2/3/4/5/5C 01
db $CA, $5D, $01				;Clear Flag 2/3/4/5/5D 01
db $CA, $5E, $01				;Clear Flag 2/3/4/5/5E 01
db $CA, $5F, $01				;Clear Flag 2/3/4/5/5F 01
db $CA, $60, $01				;Clear Flag 2/3/4/5/60 01
db $CA, $61, $01				;Clear Flag 2/3/4/5/61 01
db $CA, $62, $01				;Clear Flag 2/3/4/5/62 01
db $CA, $63, $01				;Clear Flag 2/3/4/5/63 01
db $CA, $64, $01				;Clear Flag 2/3/4/5/64 01
db $CA, $65, $01				;Clear Flag 2/3/4/5/65 01
db $CA, $66, $01				;Clear Flag 2/3/4/5/66 01
db $CA, $67, $01				;Clear Flag 2/3/4/5/67 01
db $CA, $68, $01				;Clear Flag 2/3/4/5/68 01
db $CA, $69, $01				;Clear Flag 2/3/4/5/69 01
db $CB, $6A, $01				;Clear Flag 2/3/4/5/6A 01 // this is second row of guards and is turn off. it used for checking that karnak was finished, and should not ever get set on again

db $CB, $57, $01				;Clear Flag 2/3/4/5/57 01 - this is karnak town fire (also portal boss?)

db $CA, $6B, $01				;Clear Flag 2/3/4/5/6B 01
db $CB, $6C, $01				;Set Flag 2/3/4/5/6C 01
db $CB, $6D, $01				;Set Flag 2/3/4/5/6D 01
db $CB, $6E, $01				;Set Flag 2/3/4/5/6E 01
db $CB, $6F, $01				;Set Flag 2/3/4/5/6F 01
db $CB, $70, $01				;Set Flag 2/3/4/5/70 01
db $CB, $71, $01				;Set Flag 2/3/4/5/71 01
db $CA, $52, $01				;Clear Flag 2/3/4/5/52 01
db $CB, $54, $01				;Set Flag 2/3/4/5/54 01
db $CA, $73, $01				;Clear Flag 2/3/4/5/73 01
db $CA, $74, $01				;Clear Flag 2/3/4/5/74 01
db $CA, $75, $01				;Clear Flag 2/3/4/5/75 01
db $CA, $76, $01				;Clear Flag 2/3/4/5/76 01


db $D0, $F0, $00				;(Music) F0 00
db $A4, $FE						;Set Event Flag 1FE
db $E1, $A3, $00, $21, $08, $00	;Return from cutscene? A3 00 21 08 00
db $A5, $FE						;Clear Event Flag 1FE
db $C1, $00						;<Unknown>
db $B1, $02						;Set Player Sprite 02
db $09							;Player Show
db $7D							;<Unknown>
db $BE, $00						;Rumble effect of 00 magnitude
db $D9, $0A, $03, $70			;Unknown
db $B1, $02						;Set Player Sprite 02
db $09							;Player Show
db $23							;Sprite 080 do event: face down, right hand raised out
db $B4, $08						;Play Background Music The Prelude
db $85, $09						;Sprite 085 do event: Show
db $86, $09						;Sprite 086 do event: Show
db $87, $09						;Sprite 087 do event: Show
db $C3, $0C						;Fade in Speed 0C
db $73
db $DE, $07		; set up reward  		; <---reward--->
db $DF			; call text handler  	; <---reward--->
db $85, $02						;Sprite 085 do event: Move Right
db $85, $0A						;Sprite 085 do event: Hide
db $DE, $08		; set up reward  		; <---reward--->
db $DF			; call text handler  	; <---reward--->
db $86, $03						;Sprite 086 do event: Move Down
db $86, $0A						;Sprite 086 do event: Hide
db $DE, $09		; set up reward  		; <---reward--->
db $DF			; call text handler  	; <---reward--->
db $87, $04						;Sprite 087 do event: Move Left
db $87, $0A						;Sprite 087 do event: Hide
db $73							;Medium pause

db $A5, $FF						;Clear Event Flag 1FF
db $CC, $0C                  ;Custom destination flag 0C

; CAREERDAY
db $D2, $00, $54, $4E, $D8          ; set airship again
; db $D2, $00, $54, $4F, $B5		; disable standard steamship

; db $71
; db $C8, $AF, $01 ; CUSTOM MESSAGE FOR WARPZONE
db $C4, $03						;Fade in speed 0C
db $73
db $E1, $00, $00, $56, $4D, $00 ;Return from cutscene? 00 00 9C 96 00


; db $E3, $00, $00, $53, $4E, $00	;Inter-map cutscene? 00 00 53 4E 00
; db $DB							;Restore Player status
; db $B4, $23						;Play Background Music Four Valiant Hearts
db $C3, $03						;Fade in speed 0C
db $73











db $FF							;End event

padbyte $00
pad $C880B5