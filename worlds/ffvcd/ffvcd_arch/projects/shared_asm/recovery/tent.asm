hirom


; first event, which handles the whole cycle for tent or cabin usage 

org $C84A3F
db $B9, $62                     ;Toggle Subtracitve Tint by 62
db $CD, $CC, $03                ;Run event index 03CC
db $B9, $62                     ;Toggle Subtracitve Tint by 62
db $DB                          ;Restore Player status
db $73                          ;Very long pause
db $FF                          ;End Event


padbyte $00
pad $C84A48


; TENT - event for changing sprites & executing recovery 

org $C94BE4
db $14                          ;Player pose: face down, left hand forward
db $B1, $0B                     ;Set Player Sprite 0B
db $73                          ;Very long pause
db $CD, $8A, $03                ;Run event index 038A
db $FF                          ;End Event

pad $C94BF5


; CABIN

org $C931A1
db $14                          ;Player pose: face down, left hand forward
db $B1, $0C                     ;Set Player Sprite 0C
db $73                          
db $CD, $7F, $05                ;Run event index 057F
db $FF                          ;End Event

pad $C931B2