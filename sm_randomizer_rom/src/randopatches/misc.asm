; Removes Gravity Suit heat protection
org $8de37d
    db $01
org $90e9dd
    db $01

; Suit acquisition animation skip
org $848717
    db $ea, $ea, $ea, $ea

; Mother brain cutscene edits
org $a98824 : db $01, $00
org $a98848 : db $01, $00
org $a98867 : db $01, $00
org $a9887f : db $01, $00
org $a98bdb : db $04, $00
org $a9897d : db $10, $00
org $a989af : db $10, $00
org $a989e1 : db $10, $00
org $a98a09 : db $10, $00
org $a98a31 : db $10, $00
org $a98a63 : db $10, $00
org $a98a95 : db $10, $00
org $a98b33 : db $10, $00
org $a98dc6 : db $b0
org $a98b8d : db $12, $00
org $a98d74 : db $00, $00
org $a98d86 : db $00, $00
org $a98daf : db $00, $01
org $a98e51 : db $01, $00
org $a9b93a : db $00, $01
org $a98eef : db $0a, $00
org $a98f0f : db $60, $00
org $a9af4e : db $0a, $00
org $a9af0d : db $0a, $00
org $a9b00d : db $00, $00
org $a9b132 : db $40, $00
org $a9b16d : db $00, $00
org $a9b19f : db $20, $00
org $a9b1b2 : db $30, $00
org $a9b20c : db $03, $00

; Fix Morph & Missiles room state
org $8fe652
 morph_missiles:
     lda.l $7ed873
     beq .no_items
     bra .items
org $8fe65f
 .items
org $8fe666
 .no_items    

 ; Fix heat damage speed echoes bug
org $91b629
    db $01

; Disable GT Code
org $aac91c
    db $80

; Disable Space/time
org $82b175
    db $01

; Fix Morph Ball Hidden/Chozo PLM's
org $84e8ce
    db $04
org $84ee02
    db $04

; Fix Screw Attack selection in menu
org $82b4c5
    db $0c

