#org $AB60, $2B70
OptionsFlag_PalaceRespawn:
#byte $00

#org $BDA3, $17DB3
OptionsFlag_StartingLives:
#byte $03

#org $AC30, $2C40
OptionsFlag_PreserveEXP:
#byte $01

#org $968D, $169D
JMP GetAPItem

#org $A150, $2160
JMP DisplayCurrentKeys

#org $E818, $1E828
JMP $DD47

#org $CD72, $1CD82
JMP StorePalacePerBank

#org $D9DF, $1D9EF
JMP CheckPalaceKeys

#org $B6BD, $F6CD
NOP
NOP

#org $B2B9, $172C9
JSR LoadAPFile

#org $B8B3, $178C3
JMP InitSavedData

#org $CF26, $1CF36
JSR SaveAPData

#org $A1DD, $21ED
LDA $F7
CMP #$F0

#org $B52F, $F53F
JMP SetSpellChecks

#org $B51C, $F52C
JMP CheckSpellChecks

#org $87A5, $47B5
JMP $87C2

#org $B4BF, $F4CF
LDA $7A19

#org $B4D7, $F4E7
LDA $7A19

#ORG $B4E3, $F4F3
JMP SetUpStabCheck

#ORG $B4CB, $F4DB
JMP SetDownStabCheck

#ORG $B554, $F564
JMP SetBaguNote

#org $CAD3, $1CAE3
JMP TriggerPalaceRespawn

#ORG $CAE1, $1CAF1
JMP InitPalaceScene

#ORG $B526, $F536
JMP $B52D

#ORG $A162, $2172
JMP Display2DigitLifeCount

#ORG $9620, $5630
LDA #$08

#ORG $C35A, $1C36A
JMP LoadLives

#ORG $CAC4, $1CAD4
JMP SaveEXP

#ORG $A1C9, $21D9
JMP StoreEXP

#ORG $C9E2, $1C9F2
JMP $7A90

#ORG $9610, $9620
LDA #$12

#ORG $87AE, $87BE
JMP $87CB

#ORG $CA5F, $1CA6F
STA $0756
STA $0756

; #ORG $E7D7, $1E7E7
; CMP #$FF

#org $C9EA, $1C9FA
#byte $16, $16, $16, $16

#org $0000, $1033B
#byte $64, $75

#org $0000, $126BF
#byte $64, $75

#org $A8B0, $28C0
CollectibleOffset:
#byte $00, $00, $02, $04, $06, $04
CollectibleBits:
#byte $10, $04, $10, $40, $20, $08
EXPBytes:
#byte $32, $64, $C8, $F4
CollectibleSprites:
#byte $16, $16, $14, $13, $15

#org $A770, $12780
PalaceNumbers:
#byte $00, $01, $06, $FF, $FF, $02, $03, $04, $05

PalaceTiles:
#byte $04, $05, $09, $0A, $0B, $0C

#org $A560, $16570
SaveOffsets:
#byte $00, $10, $20

#org $B820, $0F830
SpellBytes:
#byte $01, $02, $04, $08, $10, $20, $40, $80

#org $AB70, $2B80
PalaceScenes:
#byte $00, $0E, $00, $0F, $23, $24

#org $AA44, $2A54
GetAPItem:
LDA $0C9C
BNE ItemHandler_Return
LDA $074C
BNE ItemHandler_Return
LDA $7A10
BNE HandleItem
ItemHandler_Return:
LDA $0776
JMP $9690
HandleItem:
PHA
LDA #$00
STA $0743
PLA
CMP #$10
BCS CheckMagic
SEC
SBC #$01
TAY
LDA #$01
STA $0785,Y
TYA
JMP DoneGettingItem
CheckMagic:
CMP #$20
BCS CheckContainer
SEC
SBC #$10
TAY
LDA #$01
STA $077B,Y
LDA #$16
JMP DoneGettingItem
CheckContainer:
CMP #$30
BCS CheckCollectible
SEC
SBC #$20
JMP ContainerCheck
MagicMagicDone:
TAX
LDA $0783,X
CMP #$08
BCS ContainerMax
INC $0783,X
ContainerMax:
LDA #$F0
STA $070C,X
TXA
CLC
ADC #$0E
JMP DoneGettingItem
CheckCollectible:
CMP #$40
BCS CheckPowerup
SEC
SBC #$30
TAX
LDA CollectibleOffset,X
TAY
LDA CollectibleBits,X
ORA $0796,Y
STA $0796,Y
LDA CollectibleSprites,X
JMP DoneGettingItem
CheckPowerup:
CMP #$50
BCS CheckKeys
SEC
SBC #$40
BNE Not1Up
LDA $0700
CMP #$FF
BEQ DontOverflowLives
INC $0700
LDA $7A1E
CMP #$FF
BCS DontOverflowLives
INC $7A1E
DontOverflowLives:
LDA #$12
JMP DoneGettingItem
Not1Up:
CMP #$03
BCS GetExperience
SEC
SBC #$01
TAX
BNE CalcMagicCap
LDA #$10
STA $0C9D
CLC
ADC $070C
JMP AddMagic
CalcMagicCap:
LDA #$11
STA $0C9D
LDA $0783
ASL
ASL
ASL
ASL
CLC
ADC $070C
AddMagic:
STA $070C
JMP DoneGettingItemNoAnim
GetExperience:
PHA
LDA #$0B
STA $0C9D
PLA
SEC
SBC #$03
TAX
LDA EXPBytes,X
CMP #$F4
BNE Gain500EXP
INC $0755
Gain500EXP:
CLC
ADC $0756
BCC EXPDone
INC $0755
EXPDone:
STA $0756
JMP DoneGettingItem_NoSound
CheckKeys:
SEC
SBC #$50
TAX
INC $7A11,X
LDA #$08
DoneGettingItem:
STA $0C9D
DoneGettingItemNoAnim:
LDA #$10
STA $00EB
DoneGettingItem_NoSound:
LDA #$70
STA $0C9C
LDA #$00
STA $7A10
JMP ItemHandler_Return

DisplayCurrentKeys:
LDX $7A17
LDA $7A11,X
CLC
ADC #$D0
STA $7881
JMP $A159



#org $A780, $12790
StorePalaceNum:
LDA $CD2A,Y
SEC
SBC #$04
TAY
LDA PalaceNumbers,Y
STA $7A17
TAY
LDA PalaceTiles,Y
JMP $CD75

CheckPalaceKeys:
TXA
PHA
LDA $7A17
TAX
LDA $7A11,X
BEQ OutofKeys
STA $0793
DEC $7A11,X
LeaveKeys:
PLA
TAX
LDA $0793
JMP $D9E2
OutofKeys:
LDA #$00
STA $0793
JMP LeaveKeys

#org $BDB0, $17DC0
LoadAPFile:
STX $7A20
STY $7A21
TAX
LDA #$00
CheckSaveCount:
CPX #$00
BEQ HaveSaveNumber
CLC
ADC #$10
DEX
BNE CheckSaveCount
HaveSaveNumber:
LDY #$00
TAX
CheckItemSave:
LDA $7A30,X
STA $7A10,Y
CPY #$0E
BEQ ExitSaveInit
INX
INY
BNE CheckItemSave
ExitSaveInit:
STA $0700
LDX $7A20
LDY $7A21
LDA $19
JMP $B911

InitSavedData:
STX $7A20
STY $7A21
JMP PUTDACODEINSRAM
CODEMOVEDONE:
LDX $19
LDA #$00
DelSave_Check:
CPX #$00
BEQ DelSave_HaveNum
CLC
ADC #$10
DEX
JMP DelSave_Check
DelSave_HaveNum:
TAX
LDY #$00
LDA #$00
DelSave_Del:
STA $7A30,X
CPY #$0E
BEQ DelSave_End
INY
INX
BNE DelSave_Del
DelSave_End:
LDA OptionsFlag_StartingLives
STA $7A30,X
LDX $7A20
LDY $7A21
LDA $B23C,X
JMP $B8B6

SaveAPData:
LDA $0775
STA $7A1A
LDA $0776
STA $7A1B
STX $7A20
STY $7A21
LDX $0772
LDA SaveOffsets,X
TAX
LDY #$00
SaveNextData:
LDA $7A10,Y
STA $7A30,X
CPY #$0E
BEQ EndAPSave
INY
INX
JMP SaveNextData
EndAPSave:
LDX $7A20
LDY $7A21
JMP $B9CA

GreatPalace:
LDA #$07
STA $7A17
LDA $CD2A,Y
JMP $CD75
PUTDACODEINSRAM:
LDX #$00
GetMoreCode:
LDA $BF00,X
STA $7A90,X
CPX #$1F
BEQ DoneMovingCode
INX
JMP GetMoreCode
DoneMovingCode:
JMP CODEMOVEDONE

#org $B840, $0F850
SetSpellChecks:
LDA SpellBytes,Y
ORA $7A18
STA $7A18
JMP $B534

CheckSpellChecks:
LDA SpellBytes,Y
BIT $7A18
JMP $B51F

SetUpStabCheck:
LDA $7A19
ORA #$04
STA $7A19
JMP $B5C7

SetDownStabCheck:
LDA $7A19
ORA #$10
STA $7A19
JMP $B5C7

SetBaguNote:
CPX #$00
BNE NotBagu
CPY #$03
BNE NotBagu
LDA #$08
ORA $7A19
STA $7A19
JMP $B5C7
NotBagu:
LDA $0797,Y
JMP $B557

#org $FF60, $1FF70
StorePalacePerBank:
LDA $0769
CMP #$04
BEQ StorePalaceNormal
JMP GreatPalace
StorePalaceNormal:
JMP StorePalaceNum

;If I want to make all scenes respawn, I can do that here too
#org $AB80, $2B90
TriggerPalaceRespawn:
CMP #$0F
BEQ SpawnAtGreatPalace
LDA OptionsFlag_PalaceRespawn
BEQ PalaceRespawnDisabled
LDA $0707
CMP #$03
BCC PalaceRespawnDisabled
SpawnAtGreatPalace:
JMP $CADE
PalaceRespawnDisabled:
JMP $CAD7

InitPalaceScene:
LDA OptionsFlag_PalaceRespawn
BEQ SkipInitForceZero
LDA $0707
CMP #$03
BCC SkipInit
LDA $7A17
CMP #$07
BEQ SkipInitForceZero ; Great Palace
TAY
LDA PalaceScenes,Y
STA $0561
SkipInit:
LDA #$00
JMP $CAE6
SkipInitForceZero:
LDA #$00
STA $0561
JMP $CAE6

Display2DigitLifeCount:
LDA $0700
CMP #$0B
BCS TenOrMoreLives
JMP $A165
TenOrMoreLives:
TAY
DEY
TYA
LDY #$00
CheckLiveCounter:
SEC
SBC #$0A
INY
CMP #$0A
BCC FinalLifeCount
JMP CheckLiveCounter
FinalLifeCount:
CLC
ADC #$D0
STA $7804
INY
TYA
PHA
LDA $0700
CMP #$65
BCS GetHundredLives
PLA
JMP $A165
GetHundredLives:
PLA
LDA $7804
STA $7805
TYA
CLC
SEC
SBC #$0B
ADC #$CF
STA $7804
LDA $0700
SEC
SBC #$65
CMP #$64
BCS Load200
LDA #$02
JMP $A165
Load200:
LDA $7804
SEC
SBC #$0A
STA $7804
LDA #$03
JMP $A165

#org $AC40,$2C50
LoadLives:
LDA $7A1E
STA $0700
LDA OptionsFlag_PreserveEXP
BEQ NoLoadExp
LDA $7A1B
STA $0776
LDA $7A1A
STA $0775
NoLoadExp:
JMP $C35D

SaveEXP:
LDA OptionsFlag_PreserveEXP
BEQ ClearExp
LDA #$00
JMP $CACA
ClearExp:
LDA #$00
STA $0775
JMP $CAC7

StoreEXP:
LDA OptionsFlag_PreserveEXP
BEQ ClearEXP2
LDA $775
STA $7A1A
LDA $776
STA $7A1B
ClearEXP2:
JMP $A1CF


#ORG $B080, $3090
ContainerCheck:
BNE MagicFlagDone
PHA
LDA $0783
CMP #$06
BCC LessThanSevenMagic
LDA #$08
ORA $079D
STA $079D
LessThanSevenMagic:
PLA
MagicFlagDone:
JMP MagicMagicDone

#ORG $BF00, $17F10
SpawnAPItem:
LDY $072F
LDA ($D4), Y
CMP #$08
BCC BecomeDoll
CMP #$0E
BEQ BecomeDoll
CMP #$0F
BEQ BecomeDoll
CMP #$12
BCS BecomeDoll
LDA #$08
JMP $C9E7
BecomeDoll:
LDA #$12
JMP $C9E7