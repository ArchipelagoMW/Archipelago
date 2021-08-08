lorom

org $91E9E4 
	DW $09 ; A6 to 09 at offset $8E9E4 PC
org $91E9EC
	DW $0A ; A7 to 0A at offset $8E9EC PC

org $91E9F7
	DW $09 ; A4 to 09 at offset $8E9F7 PC
org $91EA01
	DW $0A ; A5 to 0A at offset $8EA01 PC

org $90F660
spinjumpentrypoint:
PHP ;push flags
PEA $0002 ;set the isitspinjump delta
JMP fromspinjumpentrypoint
normaljumpentrypoint:
PHP ;push flags
PEA $0000 ;clear the isitspinjump delta
fromspinjumpentrypoint:
CMP #$000A ;facing left
BEQ correctpose
CMP #$0009 ;facing right
BEQ correctpose
PLP ;move stack pointer, didn't find a better way to do it
PLP
PLP ;pop flags
STA $a28 ;do oppcodes we've overwritten
CLC
RTL

correctpose:

PHA
LDA $7E0B46 ;add two words of samus "momentum"
CLC
ADC $7E0B48
BCS moving ;in case we overflowed, but added up to exactly zero
BNE moving
PLA
CLC
ADC #$009b ;difference between landing and moving poses
ADC $01,S ;add the isitspinjump delta
JMP SKIPPLA
moving:
PLA
SKIPPLA:
PLP ;move stack pointer, didn't find a better way to do it
PLP
PLP ;pop flags
STA $a28 ;do oppcodes we've overwritten
CLC
RTL

org $91E9E6 ;spinjump landing facing right = A6
JSL spinjumpentrypoint
org $91E9EE ;spinjump landing facing left = A7
JSL spinjumpentrypoint

org $91E98E ; landing facing right = A4, facing left = A5
JSL normaljumpentrypoint