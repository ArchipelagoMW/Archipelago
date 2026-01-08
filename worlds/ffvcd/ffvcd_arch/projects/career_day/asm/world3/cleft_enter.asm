hirom


; Cutscene at first door in sand area
; This is going to be used as the main trigger for setting most cutscenes watched flags
; If space is ran out, use 
; db $CD, $3A, $05                ;Run event index 053A
; at address 


org $C9E728

; first door cutscene flag
db $A4, $7A                     ;Set Event Flag 17A
; final Exdeath cutscene 
db $A5, $FE                     ;Clear Event Flag 1FE
db $A4, $9F                     ;Set Event Flag 19F
db $CB, $97, $03                ;Clear Flag 2/3/4/5/97 03

db $FF                          ;End Event

padbyte $00
pad $C9E755






; Part of the original cutscene where the minions show up & fade out. Free space now

org $C99E10

padbyte $00
pad $C99E39


; if you leave the cleft, disable cutscene:

org $C93038

db $B5, $AE                     ;Play Sound Effect The Void
db $BF, $0E                     ;Sprite effect 0E
db $E1, $0D, $00, $00, $00, $00 ;Return from cutscene? 0D 00 00 00 00
db $0A                          ;Player Hide
db $C3, $0A                     ;Fade in Speed 0A
db $70                          ;Very short pause
db $C4, $0A                     ;Fade out Speed 0A
db $71                          ;Short pause
db $CD, $FB, $03                ;Run event index 03FB
db $FF                          ;End Event

pad $C93051