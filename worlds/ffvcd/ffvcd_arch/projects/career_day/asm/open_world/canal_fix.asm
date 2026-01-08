hirom


; Allows airship vehicle to access canal. The game checks for no vehicle, chocobo, and pirate ship every frame on the world map to enter new areas. Does NOT do it for ANY other vehicle. So this needs to be fixed specifically for canal. 

org $C0061E
JML CanalAccessFix


org !ADDRESS_canalfix
CanalAccessFix:
LDA $0ADC
BEQ CanalAccessFixBranchOut1
CMP #$01
BEQ CanalAccessFixBranchOut1
CMP #$05
BEQ CanalAccessFixBranchOut1
CMP #$06
BEQ CanalAccessFixAirshipShip
CanalAccessFixBranchOut2:
LDA $0ADC
JML $C0062B

CanalAccessFixBranchOut1:
LDA $0ADC
JML $C00633

; We're branching to $C00633, but only on specific x/y/coord conditions
CanalAccessFixAirshipShip:

; x coord, $AA
LDA $0AD8
CMP #$AA
BNE CanalAccessFixBranchOut2
; y coord, $58
LDA $0AD9
CMP #$58
BNE CanalAccessFixBranchOut2

; vehicle is NOT flying
LDA $0AF2
CMP #$80
BNE CanalAccessFixBranchOut2
; world map, $00
LDA $0AD6
BNE CanalAccessFixBranchOut2

; if all met:
BRA CanalAccessFixBranchOut1