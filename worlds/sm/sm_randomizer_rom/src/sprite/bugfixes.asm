; These are significant typos that reference bad palettes or similar, and would
; raise assertion errors in any clean code


; Last byte should be $28, like everything else
;TM_193:
;DW $0001
;DB $F8, $01, $F8, $00, $30

org $92BEC1+4 : db $28


; Last byte should be $28, like everything else
;TM_181:
;DW $0001
;DB $F8, $01, $F8, $00, $10

org $92BC7C+4 : db $28


; Last byte should be $68, like everything else
;TM_0DA:
;DW $0004
;DB $FD, $01, $0F, $0A, $78

org $92AEE3+4 : db $68


; Last byte should be $38, just like the other elevator poses
;TM_06F:
;DW $0001
;DB $F8, $01, $F8, $00, $30

org $92A12E+4 : db $38
