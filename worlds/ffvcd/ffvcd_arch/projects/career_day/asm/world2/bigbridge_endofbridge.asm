hirom


org $c8b745

; Big Bridge: End of bridge → placement on continent

; db $D3, $88, $8F, $0F           ;Sprite 88 set map position 8F, 0F
; db $B1, $04                     ;Set Player Sprite 04
; db $88, $03                     ;Sprite 088 do event Move Down
; db $88, $03                     ;Sprite 088 do event Move Down
; db $C4, $03                     ;Fade out Speed 02
; db $74                          ;Timing
; db $E1, $01, $00, $63, $2D, $00 ;Return from cutscene? 01 00 63 2D 00
; db $DB                          ;Restore Player status
; db $09                          ;Player Show
; db $14                          ;Player Move Down
; db $C3, $03                     ;Fade in Speed 02
; db $74                          ;Timing
; db $CC, $19                  ;Custom destination flag 19


; CAREERDAY
; db $D2, $01, $64, $2D, $6C ; hiryuu
db $A5, $FE                     ;Clear Event Flag 1FE
db $A2, $5D            ; set address 000A1F bit ON 20
db $FF                          ;End Event

padbyte $00
pad $C8BA3B