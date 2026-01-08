hirom


; $C9F41E → $C9F6DA
; Airship get after Merugene, changes world state

org $C9F41E

db $A4, $F7                     ;Set Event Flag 1F7

db $B4, $3F                     ;Play Background Music The Land Unknown
db $01
db $C4, $02                     ;Fade out Speed 04
db $B3, $10                     ;Pause for 100 cycles
db $E1, $02, $20, $AE, $2E, $D8 ;Return from cutscene? 02 20 AE 2E D8
db $03                          ;Player Move Down
db $C3, $02                     ;Fade in Speed 04
db $B5, $69                     ;Play Sound Effect Airship
db $B3, $0C                     ;Pause for 0C0 cycles
db $76                          ;<Unknown>
db $A5, $FE                     ;Clear Event Flag 1FE
db $A4, $7D                     ;Set Event Flag 17D

; Set flag for Cleft of Dimensions first visit
db $A4, $7E                     ;Set Event Flag 17E
db $CC, $28                  ;Custom destination flag 28

db $FF                          ;End Event

padbyte $00
pad $C9F6DA