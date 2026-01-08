hirom


; disables canal gate cutscene, skips straight to opening.
; the left and right gate tiles have their own events, so this
; has to be duplicated

org $C8645F

db $A4, $FE			;Set Event Flag 1FE
db $BE, $05			;Rumble effect of 05 magnitude
db $73				;Long pause
db $B5, $43			;Play Sound Effect Gate opens
db $F3, $0B, $11, $11		;Set Map Tiles 0B 11 11
db $ED				;Noop
db $C4, $FD			;Fade out Speed FD
db $FA				;Noop
db $73				;Long pause
db $BE, $00			;Rumble effect of 00 magnitude
db $A2, $1E			;Set Event Flag 01E
db $A5, $FE			;Clear Event Flag 1FE
db $FF				;End Event


padbyte $00
pad $C86484

org $C86439

db $A4, $FE			;Set Event Flag 1FE
db $BE, $05			;Rumble effect of 05 magnitude
db $73				;Long pause
db $B5, $43			;Play Sound Effect Gate opens
db $F3, $0B, $11, $11		;Set Map Tiles 0B 11 11
db $ED				;Noop
db $C4, $FD			;Fade out Speed FD
db $FA				;Noop
db $73				;Long pause
db $BE, $00			;Rumble effect of 00 magnitude
db $A2, $1E			;Set Event Flag 01E  (steamship spawn)
db $A5, $FE			;Clear Event Flag 1FE
db $CC, $05                  ;Custom destination flag 05
db $FF				;End Event


padbyte $00
pad $C8645E

;CAREERDAY

; Set airship upon leaving instead of pirate ship. This changes the 5th argument in the warp code (event code $E1)

org $C8340A
db $F0, $61, $C8

org $C861F0
db $C4, $0C                     ;Fade out Speed 0C
db $73                          ;Long pause
db $B1, $02                     ;Set Player Sprite 02
db $E1, $00, $00, $A9, $56, $00 ;Return from cutscene? 00 00 A9 58 C0
db $D2, $00, $A8, $56, $D8
db $B4, $23                     ;Play Background Music Four Valiant Hearts
db $DB                          ;Restore Player status
db $C3, $0C                     ;Fade in Speed 0C
db $73                          ;Long pause
db $FF                          ;End Event


; Always allow canal access regardless of vehicle type

org $C00628
db $05

; Never check for flags for re-entry

; org $D8EDF4
org $F04D74
db $ff, $50, %00, $00, $00


; new event for custom canal gate relocating to graveyard

org $C8973F

db $C4, $02                     ;Fade out Speed 0C
db $75                          ;Very long pause
db $B1, $02                     ;Set Player Sprite 02
db $E1, $2B, $00, $8B, $19, $00 ;Return from cutscene? 2B 00 8B 19 00
db $CD, $7F, $05                ;Run event index 057F
db $C3, $08                     ;Fade in Speed 08
db $FF                          ;End Event

pad $C89770



; NEW - Disable Torna Canal lock entirely
; tie it to world map, always on, never not set
org $F04D84
db $FC, $FB