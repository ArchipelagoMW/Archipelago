hirom

; climbing up vines
org $C9B0B1

db $3D                          ;Player pose: face up, both arms raised out
db $0C                          ;<Unknown>
db $05                          ;Player Bounce in Place
db $01                          ;Player Move Up
db $70                          ;Medium pause
db $01                          ;Player Move Up
db $70                          ;Short pause
db $01                          ;Player Move Up
db $70                          ;Short pause
db $C4, $10                     ;Fade out Speed 10
db $70                          ;Very short pause
db $FF                          ;End Event


padbyte $00
pad $C8731A