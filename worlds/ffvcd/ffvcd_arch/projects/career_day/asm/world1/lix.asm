hirom


; removing lix musicbox cutscene. This turns on the music
; and sets the bit that lets you get the song
org $C9229F
db $B4, $1B							;Play Background Music Music Box
db $A5, $FE							;Turn off bit 40 at address 0x7e0a53
db $A2, $A9							;Turn on bit 02 at address 0x7e0a29

db $FF								;End event

padbyte $00
pad $C92384

;Remove message before lix inn shop
org $C9238B
db $A1, $31							;Run Shop Lix Inn

db $FF								;End event

padbyte $00
pad $C9238F

;Remove cutscene from sleeping in lix inn. You're forced into
;sleeping here, but the cutscene is fast so it's ok
org $C9243F

db $CD, $DB, $03					;Run event index 03DB
db $CD, $DC, $03					;Run event index 03DC
db $CD, $DD, $03					;Run event index 03DD
db $A2, $99							;Turn on bit 02 at address 0x7e0a27

db $FF								;End event

padbyte $00
pad $C924E4

;Remove message before inn after seeing cutscene. this just makes
;the experience the same at the inn always.
org $C92418

db $CD, $DB, $03					;Run event index 03DB
db $CD, $DC, $03					;Run event index 03DC
db $CD, $DD, $03					;Run event index 03DD

db $FF								;End event

padbyte $00
pad $C92423

;Remove cutscene from talking to scholar.
org $C93D12
db $A0, $00							;(Message) 00
db $A2, $E2							;Turn on bit 04 at address 0x7e0a30

db $FF								;End event

padbyte $00
pad $C93D9E