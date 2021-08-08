lorom

macro a8()
	sep #$20
endmacro

macro a16()
	rep #$20
endmacro

macro i8()
	rep #$10
endmacro

macro ai8()
	sep #$30
endmacro

macro ai16()
	rep #$30
endmacro

macro i16()
	rep #$10
endmacro

org $00ffc0
    ;   0              f01234
    db "      SM RANDOMIZER  "
    db $30, $02, $0C, $04, $00, $01, $00, $20, $07, $DF, $F8

org $808000				; Disable copy protection screen
	db $ff

; Config flags
incsrc config.asm

; Super Metroid custom Samus sprite "engine" by Artheau
incsrc "sprite/sprite.asm"

; These patches include their own origins and patch locations
incsrc randopatches/introskip.asm
incsrc randopatches/wake_zebes.asm
incsrc randopatches/misc.asm
incsrc randopatches/nofanfare.asm
incsrc randopatches/g4_skip.asm
incsrc randopatches/credits.asm
incsrc randopatches/tracking.asm
incsrc randopatches/seed_display.asm
incsrc randopatches/max_ammo.asm

; Start anywhere patch, not used right now until graph based generation is in.
; incsrc startanywhere.asm

; Add code to the main code bank
org $b88000
incsrc common.asm
incsrc randolive.asm
incsrc multiworld.asm
incsrc items.asm

org $b8cf00
incsrc seeddata.asm

org $b8d000
incsrc playertable.asm

org $b8e000
incsrc itemtable.asm
