hirom

; this enables the bottom right sheep in Rugor to give all key items to the player

; event relocation to custom bank
org $C83F80
db $C0, $00, $F9

; new custom event
org $F900C0

db $F0, $0B, $02              ;Conditional yes/no dialogue at 04B7
db $CD, $B6, $01                ; event relocation from intro cutscene 
db $FF
db $FF


; event relocation from intro cutscene 
org $c83842
db $D0, $00, $F9
; new custom event 2 (for yes case)
org $F900D0
db $C5, $80                     ;<unknown>
db $B5, $02                     ;Play Sound Effect Void, Image
db $71
db $DE, $60
db $DE, $61
db $DE, $62
db $DE, $63
db $DE, $64
db $DE, $65
db $DE, $66
db $DE, $67
db $DE, $68
db $DE, $69
db $DE, $6A
db $DE, $6B
db $DE, $6C
db $DE, $6D
db $DE, $6E
db $DE, $6F
db $DE, $70
db $DE, $71
db $DE, $72
db $DE, $73
db $DE, $74
db $DE, $75
db $DE, $76
db $DE, $77
db $DE, $78
db $DE, $79
db $DE, $7A
db $DE, $7B
db $DE, $7C
db $DE, $7D
db $DE, $7E
db $DE, $7F
db $DE, $80
db $DE, $81
db $DE, $82
db $DE, $83
db $DE, $84
db $DE, $85
db $FF



; magic sheep text box
org $E194ED
db $6C, $60, $66, $68, $62, $96, $63, $64, $61, $74, $66, $96, $72, $67, $64, $64, $6F, $01
db $66, $8B, $7A, $87, $8D, $96, $7A, $85, $85, $96, $7B, $88, $8C, $8C, $96, $7C, $81, $7E, $7C, $84, $8C, $96, $9E, $7A, $85, $85, $96, $84, $7E, $92, $96, $82, $8D, $7E, $86, $8C, $96, $89, $85, $8E, $8C, $96, $8B, $7E, $90, $7A, $8B, $7D, $8C, $9F, $A2, $00