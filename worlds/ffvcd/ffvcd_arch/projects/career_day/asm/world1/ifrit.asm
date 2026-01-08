hirom



; Skip ifrit's text before the fight
org $C9728F

db $BD, $39, $FF		;Start Event Battle 39
;db $A4, $28				;Set Event Flag 128
db $CB, $97, $01		;Clear Flag 2/3/4/5/97 01 (Tied to ifrit book not respawning)
;db $A4, $29                     ;Turn on bit 02 at address 0x7e0a39
db $83, $03				;Sprite 083 do event: Move Down
db $83, $0A				;Sprite 083 do event: Hide
db $DE, $36					; set up reward
db $DF						; call text handler
db $C5, $80
db $B5, $02
db $71
db $DE, $83 ; custom reward
db $DF
; db $E4, $C9                     ;Unknown
; db $08                          ;<Unknown>
; db $0F                          ;<Unknown>
db $FF					;End Event

padbyte $00
pad $C972C5