hirom

; TEXT FOR AFTER DEFEATING EXDEATH IN WORLD 2

; [ HARDCODE, NEVER CHANGED ]
; Phase 1 against final Exdeath weakened!
org $E2A067
db $6F, $81, $7A, $8C, $7E, $96, $54, $96, $7A, $80, $7A, $82, $87, $8C, $8D, $96, $7F, $82, $87, $7A, $85, $01
db $64, $91, $7D, $7E, $7A, $8D, $81, $96, $90, $7E, $7A, $84, $7E, $87, $7E, $7D, $A1, $01, $01, $01
; [ HARDCODE, NEVER CHANGED ]
; Now choose an item...
db $6D, $88, $90, $96, $7C, $81, $88, $88, $8C, $7E, $96, $7A, $87, $96, $82, $8D, $7E, $86, $A3, $A3, $A3, $01



; Key items displayed before choosing individually. All 3 choices appear. 
; >>>>>>>>>>> [ DYNAMICALLY CHANGED ] <<<<<<<<<< 
; org $E2A0A7
; ; [TEXT BLOCK] Big Bridge Key
; db $61, $82, $80, $96, $61, $8B, $82, $7D, $80, $7E, $96, $6A, $7E, $92, $01
; ; [TEXT BLOCK] Walse Tower Key
; db $76, $7A, $85, $8C, $7E, $96, $73, $88, $90, $7E, $8B, $96, $6A, $7E, $92, $01
; ; [TEXT BLOCK] Hiryuu Call
; db $67, $82, $8B, $92, $8E, $8E, $96, $62, $7A, $85, $85, $01
; ; terminator
; db $00
org $E2A0A7
; terminator
db $00


; ; Key items menu. Each one now shows up alone in it's own text box
; ; >>>>>>>>>>> [ DYNAMICALLY CHANGED ] <<<<<<<<<< 
; ; [ TEXT 1 ] Big Bridge Key
; org $E2A10B
; db  $61, $82, $80, $96, $61, $8B, $82, $7D, $80, $7E, $96, $6A, $7E, $92, $A2, $00
; ; [ TEXT 2 ] Walse Tower Key
; org $E2A166
; db  $76, $7A, $85, $8C, $7E, $96, $73, $88, $90, $7E, $8B, $96, $6A, $7E, $92, $A2, $00
; ; [ TEXT 3 ] Hiryuu Call
; org $E2A1C6
; db  $67, $82, $8B, $92, $8E, $8E, $96, $62, $7A, $85, $85, $A2, $00

org $E2A10B
db $00
org $E2A166
db $00
org $E2A1C6
db $00


; QUESTION EVENTS - asking the player do they want X item
; [ HARDCODE, NEVER CHANGED ]
org $C9497A
; first question
db $F0, $AA, $05                ; [ TEXT 1 ] 
db $CD, $88, $03                ; [ EVENT 1 ]
db $FF                          ;End Event
db $CD, $9F, $03
db $FF

;second question
org $C949E7
db $F0, $AB, $05                ; [ TEXT 2 ] 
db $CD, $25, $03                ; [ EVENT 2 ]
db $FF                          ;End Event
db $CD, $94, $03
db $FF
; third question

org $C9477D
db $F0, $AC, $05                ; [ TEXT 3 ] 
db $CD, $C2, $03                ; [ EVENT 3 ]
db $FF                          ;End Event
; db $CD, $9C, $03 ; disabled for now - answering no immediately ends the sequence
db $FF







; REWARDING EVENTS - rewarding the player X item 
; [ HARDCODE ] EXCEPT for "BOTTOM CODE FOR ADDRESSES", look for "<<<<<<<<<<"
; relocate event 1 for confirm ; relates to original event code CD8803
; [ EVENT 1 ]
org $C83DB8
db $00, $04, $F9
org $F90400
db $C5, $60
db $B5, $02
db $71
db $DE, $60 ; >>>>>>>>>>> [ DYNAMICALLY CHANGED ] <<<<<<<<<<  THIS GETS WRITTEN WITH A NEW "KEY ITEM LOCATION". SEE BOTTOM CODE FOR ADDRESSES
db $DF
db $FF

; relocate event 2 for confirm  ; relates to CD4D03
; [ EVENT 2 ]
org $C83C8F
db $20, $04, $F9
org $F90420
db $C5, $20
db $B5, $02
db $71
db $DE, $61 ; >>>>>>>>>>> [ DYNAMICALLY CHANGED ] <<<<<<<<<<  THIS GETS WRITTEN WITH A NEW "KEY ITEM LOCATION". SEE BOTTOM CODE FOR ADDRESSES
db $DF
db $FF

; relocate event 3 for confirm ; relates to CDC203
; [ EVENT 3 ]
org $c83e66
db $10, $04, $F9
org $F90410
db $C5, $A0
db $B5, $02
db $71
db $DE, $64  ; >>>>>>>>>>> [ DYNAMICALLY CHANGED ] <<<<<<<<<<  THIS GETS WRITTEN WITH A NEW "KEY ITEM LOCATION". SEE BOTTOM CODE FOR ADDRESSES
db $DF
db $FF



; BOTTOM CODE FOR ADDRESSES
; Addresses for key item actual rewards. These are already present above (hardcode as example), but during randomization these will get overwritten
; Example, we want to place Big Bridge Key.
    ; Galura's location has Big Bridge Key
    ; In world1/water_crystal.asm, the following code is present:
    ; $DE, $65
    ; This ID of $65 is where Big Bridge Key is for THIS seed
    ; So, we write $65 to the first event below at $F90406

; org $F90406
; db $62
; org $F90426
; db $7F
; org $F90416
; db $70