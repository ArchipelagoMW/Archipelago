hirom


padbyte $00
org $C94D1D

db $B4, $34                     ;Play Background Music Good Night!
db $C4, $04                     ;Fade out Speed 04
db $75
db $73
db $A8, $1F                     ;Adjust Character HP by 1F
db $A8, $5F                     ;Adjust Character HP by 5F
db $A8, $9F                     ;Adjust Character HP by 9F
db $A8, $DF                     ;Adjust Character HP by DF
db $A9, $1F                     ;Adjust Character MP by 1F
db $A9, $5F                     ;Adjust Character MP by 5F
db $A9, $9F                     ;Adjust Character MP by 9F
db $A9, $DF                     ;Adjust Character MP by DF
db $BA, $00, $00                ;Clear Character Butz status
db $BA, $01, $00               ;Clear Character Lenna status
db $BA, $02, $00                ;Clear Character Galuf status
db $BA, $03, $00                ;Clear Character Faris status
db $C3, $04                     ;Fade out Speed 04
db $14
db $72
db $C9, $68, $0F                ;Play Music 68 0F
db $DB                          ;Restore Player status

db $FF                          ;End Event

pad $C94D6F

org $C94D70
db $FF                          ;End Event


pad $C94DF7
org $C94DF8
db $FF                          ;End Event

pad $C94E39


; healing pots/springs clear zombie
org $c9a6d9

db $A8, $1F                     ;Adjust Character HP by 1F
db $A8, $5F                     ;Adjust Character HP by 5F
db $A8, $9F                     ;Adjust Character HP by 9F
db $A8, $DF                     ;Adjust Character HP by DF
db $A9, $1F                     ;Adjust Character MP by 1F
db $A9, $5F                     ;Adjust Character MP by 5F
db $A9, $9F                     ;Adjust Character MP by 9F
db $A9, $DF                     ;Adjust Character MP by DF
db $BA, $00, $00                ;Clear Character Butz status
db $BA, $01, $00               ;Clear Character Lenna status
db $BA, $02, $00                ;Clear Character Galuf status
db $BA, $03, $00                ;Clear Character Faris status
db $FF                          ;End Event
