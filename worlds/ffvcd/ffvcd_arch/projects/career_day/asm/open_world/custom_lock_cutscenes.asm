hirom


; STEAMSHIP TEXTBOX
; Replaces Hiryuu dying cutscene
; Event ID $F000
org $C8C71D

db $C8, $AB, $84                ;Display Message/Text/Dialogue AB 84
db $04
db $FF                          ;End Event

pad $C8C7DE

; Text for C8, AB, 84
; Door locked. Steamship Key required
org $E250A3
db $72, $8D, $7E, $7A, $86, $8C, $81, $82, $89, $96, $6A, $7E, $92, $96, $8B, $7E, $8A, $8E, $82, $8B, $7E, $7D, $A3, $00


; BIG BRIDGE TEXTBOX
; This one is for SOUTH entrance 
; Replaces a Hiryuu dying cutscene
org $C86401


db $C8, $AC, $84                ;Display Message/Text/Dialogue AC 84
db $03
db $FF                          ;End Event

; pad $C84606
; This one is for NORTH entrance 
; Replaces an early Butz dialogue cutscene with the ship/sea
org $C86A13


db $C8, $AC, $84                ;Display Message/Text/Dialogue AC 84
db $01
db $FF                          ;End Event



; Big Bridge Key required.
org $E250BF
db $61, $82, $80, $96, $61, $8B, $82, $7D, $80, $7E, $96, $6A, $7E, $92, $96, $8B, $7E, $8A, $8E, $82, $8B, $7E, $7D, $A3, $00







; GENERIC "MISSING PAGE" TEXTBOX
; Used for last 3 shrine visits
org $C8C868
db $C8, $BA, $04                ;Display Message/Text/Dialogue BA 04
db $03
db $FF

; Sealed Book page required
org $E25760
db $72, $7E, $7A, $85, $7E, $7D, $96, $61, $88, $88, $84, $96, $89, $7A, $80, $7E, $96, $8B, $7E, $8A, $8E, $82, $8B, $7E, $7D, $A3, $00




; RIFT TABLET HANDLING
; Replaces old Zeza first visit cutscene
org $C8D048
db $EF
db $FF

; Replaces Zeza blowup cutscene
org $C8D2D7
db $C8, $BD, $04                ;Display Message/Text/Dialogue BB 04
db $03
db $A5, $68            ; set address 000A42 bit OFF 01
db $A5, $69            ; set address 000A42 bit OFF 02
db $FF
; Tablet required
org $E2587A
db $6D, $88, $8D, $96, $7E, $87, $88, $8E, $80, $81, $96, $73, $7A, $7B, $85, $7E, $8D, $8C, $A3, $A3,  $A3,$00

; Replaces Zeza transceiver
org $C8D3CC
db $C8, $BC, $04                ;Display Message/Text/Dialogue BB 04
db $01
db $A5, $68            ; set address 000A42 bit OFF 01
db $A5, $69            ; set address 000A42 bit OFF 02
db $FF

; Tablet accepted
org $E257BC
db $73, $7A, $7B, $85, $7E, $8D, $96, $7A, $7C, $7C, $7E, $89, $8D, $7E, $7D, $A3, $96, $64, $87, $8D, $7E, $8B, $96, $8D, $81, $7E, $96, $71, $82, $7F, $8D, $A3, $A3, $A3, $00

; Disable world map back entrance for Ship Graveyard. Instead, custom torna canal event allows you to re-enter
; Code below is replicating Torna Canal again
org $CE2808
db $AA, $58, $C5, $00



; Submarine disallow access at shoat cave without sub key
; event bd01 
org $c9148d
db $01, $FF

; event bd02
org $C914A4
db $03
db $C8, $BE, $04                ;Display Message/Text/Dialogue BB 04

db $FF

; No submarine key text
org $e258fe
db $64, $91, $82, $8D, $96, $7B, $85, $88, $7C, $84, $7E, $7D, $96, $88, $7F, $7F, $A3, $00