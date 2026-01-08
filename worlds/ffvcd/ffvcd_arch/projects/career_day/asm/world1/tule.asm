hirom


; first we move the event coordinates for the intro to tule off into the forest
; this is unfortunately required, because there's no way to interact with 
; tule normally before receiving the canal key. We're kind of doing surgery here
org $CE2978
db $1E

; this disables the event with faris in the bed where butz and galuf go fall in love
org $C85FCA
db $CA, $6B, $00		;Set Flag 2/3/4/5/6B 00
db $CA, $57, $00		;Set Flag 2/3/4/5/57 00
db $CB, $58, $00		;Clear Flag 2/3/4/5/58 00
db $A2, $1A				;Set Event Flag 01A
db $FF					;End Event

padbyte $00
pad $C8614F

; disable zokk's house outside event
org $C86150
db $A2, $1B			;Set Event Flag 01B
db $FF				;End Event

padbyte $00
pad $C86191

; streamline zokk giving butz the canal key
; the events remove the pirates and basically set
; tule in a 'normal' state, as well as setting the canal key
org $C86192

db $01				;Player Move Up
db $01				;Player Move Up
db $01				;Player Move Up
db $01				;Player Move Up
db $04				;Player move Left
db $01				;Player Move Up
db $2D				;Player pose: face right, right hand out
db $83, $2A			;Sprite 083 do event: face left, left hand raised
db $73				;Long pause
db $38				;Player pose: face down, squatting
db $70				;Very short pause
db $39				;Player pose: face down, both arms raised
db $71				;Very short pause

db $03				;Player Move Down
; db $A2, $1C                     ;Turn on bit 10 at address 0x7e0a17
; db $A2, $1D                     ;Turn on bit 20 at address 0x7e0a17
db $CB, $60, $00                ;Turn off bit 01 at address  0x7e0a60
db $CB, $61, $00                ;Turn off bit 02 at address  0x7e0a60
db $CB, $62, $00                ;Turn off bit 04 at address  0x7e0a60
db $CB, $63, $00                ;Turn off bit 08 at address  0x7e0a60
db $CB, $64, $00                ;Turn off bit 10 at address  0x7e0a60
db $CA, $3B, $00                ;Turn on bit 08 at address  0x7e0a5b
db $CA, $3C, $00                ;Turn on bit 10 at address  0x7e0a5b
db $CA, $3D, $00                ;Turn on bit 20 at address  0x7e0a5b
db $CA, $3E, $00                ;Turn on bit 40 at address  0x7e0a5b
db $CA, $3F, $00                ;Turn on bit 80 at address  0x7e0a5b
db $CB, $6B, $00                ;Turn off bit 08 at address  0x7e0a61
db $CB, $57, $00                ;Turn off bit 80 at address  0x7e0a5e
db $CA, $0D, $00                ;Turn on bit 20 at address  0x7e0a55
db $CB, $7E, $00                ;Turn off bit 40 at address  0x7e0a63
db $CA, $77, $00                ;Turn on bit 80 at address  0x7e0a62
db $CC, $04         ;Custom destination flag 04
db $CD, $7F, $05	;Run event index 057F ; Party Heal
db $A4, $4C			;Set Event Flag 14C (this disables the boat after_tule_boat_cutscene entirely )
db $FF				;End Event

padbyte $00
pad $C863F1


; disable faris leaving at weapon shop
org $C9B9A3
db $A1, $00			;Run Shop Tule Weapon
db $FF				;End Event

padbyte $00
pad $C9B9AF

; disable faris leaving at armor shop
org $C9B9B0
db $A1, $01			;Run Shop Tule Armor
db $FF				;End Event

padbyte $00
pad $C9B9BC