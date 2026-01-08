hirom


; Currently disabled - these flags are set in tule.asm after Zokk gives the key
; Disables cutscene on boat after leaving Tule with Faris
; org $C99998

; db $C4, $03
; db $73
; db $E1, $00, $00, $8C, $5C, $B4	;Return from cutscene? 00 00 8C 5C B4
; db $12				;Player pose: face right, standing
; db $C3, $03			;Fade in Speed 06
; db $73				;Extremely long pause
; db $A4, $4C			;Set Event Flag 14C
; db $FF				;End Event

; padbyte $00
; pad $C99ACD