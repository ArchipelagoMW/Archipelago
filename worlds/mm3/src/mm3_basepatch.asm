norom
!headersize = 16

!controller_flip = $14 ; only on first frame of input, used by crash man, etc
!controller_mirror = $16
!current_stage = $22
!current_state = $60
!completed_rbm_stages = $61
!completed_doc_stages = $62
!current_wily = $75
!received_rbm_stages = $680
!received_doc_stages = $681
; !deathlink = $30, set to $0E
!energylink_packet = $682
!last_wily = $683
!rbm_strobe = $684
!sound_effect_strobe = $685
!doc_robo_kills = $686
!wily_stage_completion = $687
;!received_items = $688
!acquired_rush = $689

!current_weapon = $A0
!current_health = $A2
!received_weapons = $A3

'0' = $00
'1' = $01
'2' = $02
'3' = $03
'4' = $04
'5' = $05
'6' = $06
'7' = $07
'8' = $08
'9' = $09
'A' = $0A
'B' = $0B
'C' = $0C
'D' = $0D
'E' = $0E
'F' = $0F
'G' = $10
'H' = $11
'I' = $12
'J' = $13
'K' = $14
'L' = $15
'M' = $16
'N' = $17
'O' = $18
'P' = $19
'Q' = $1A
'R' = $1B
'S' = $1C
'T' = $1D
'U' = $1E
'V' = $1F
'W' = $20
'X' = $21
'Y' = $22
'Z' = $23
' ' = $25
'.' = $26
',' = $27
'!' = $29
'r' = $2A
':' = $2B

; !consumable_checks = $0F80 ; have to find in-stage solutions for this, there's literally not enough ram

!CONTROLLER_SELECT = #$20
!CONTROLLER_SELECT_START = #$30
!CONTROLLER_ALL_BUTTON = #$F0

!PpuControl_2000 = $2000
!PpuMask_2001 = $2001
!PpuAddr_2006 = $2006
!PpuData_2007 = $2007

;!LOAD_BANK = $C000

macro org(address,bank)
    if <bank> == $3E
        org <address>-$C000+($2000*<bank>)+!headersize ; org sets the position in the output file to write to (in norom, at least)
        base <address> ; base sets the position that all labels are relative to - this is necessary so labels will still start from $8000, instead of $0000 or somewhere
    else 
      if <bank> == $3F
          org <address>-$E000+($2000*<bank>)+!headersize ; org sets the position in the output file to write to (in norom, at least)
          base <address> ; base sets the position that all labels are relative to - this is necessary so labels will still start from $8000, instead of $0000 or somewhere
      else
        if <address> >= $A000
          org <address>-$A000+($2000*<bank>)+!headersize
          base <address>
        else
          org <address>-$8000+($2000*<bank>)+!headersize
          base <address>
        endif
      endif
    endif
endmacro

; capcom.....
; i can't keep defending you like this

;P
%org($BEBA, $13)
RemoveP:
db $25
;A
%org($BD7D, $13)
RemoveA:
db $25
;S
%org($BE7D, $13)
RemoveS1:
db $25
;S
%org($BDD5, $13)
RemoveS2:
db $25

;W
%org($BDC7, $13)
RemoveW:
db $25
;O
%org($BEC7, $13)
RemoveO:
db $25
;R
%org($BDCF, $13)
RemoveR:
db $25
;D
%org($BECF, $13)
RemoveD:
db $25

%org($A17C, $02)
AdjustWeaponRefill:
  ; compare vs unreceived instead. Since the stage ends anyways, this just means you aren't granted the weapon if you don't have it already
  CMP #$1C
  BCS WeaponRefillJump

%org($A18B, $02)
WeaponRefillJump:
  ; just as a branch target

%org($A3BF, $02)
FixPseudoSnake:
  JMP CheckFirstWep
  NOP

%org($A3CB, $02)
FixPseudoRush:
  JMP CheckRushWeapon
  NOP

%org($BF80, $02)
CheckRushWeapon:
  AND #$01
  BNE .Rush
  JMP $A3CF
  .Rush:
  LDA $A1
  CLC
  ADC $B4
  TAY
  LDA $00A2, Y
  BNE .Skip
  DEC $A1
  .Skip:
  JMP $A477

; don't even try to go past this point

%org($802F, $0B)
HookBreakMan:
  JSR SetBreakMan
  NOP

%org($90BC, $18)
BlockPassword:
  AND #$08 ; originally 0C, just block down inputs

%org($9258, $18)
HookStageSelect:
  JSR ChangeStageMode
  NOP

%org($92F2, $18)
AccessStageTarget:

%org($9316, $18)
AccessStage:
  JSR RewireDocRobotAccess
  NOP #2
  BEQ AccessStageTarget

%org($9468, $18)
HookWeaponGet:
  JSR WeaponReceived
  NOP #4

%org($9917, $18)
GameOverStageSelect:
  ; fix it returning to Wily 1
  CMP #$16

%org($9966, $18)
SwapSelectTiles:
  ; swaps when stage select face tiles should be shown
  JMP InvertSelectTiles
  NOP

%org($9A54, $18)
SwapSelectSprites:
  JMP InvertSelectSprites
  NOP

%org($9AFF, $18)
BreakManSelect:
  JSR ApplyLastWily
  NOP

%org($BE22, $1D)
ConsumableHook:
  JMP CheckConsumable

%org($BE32, $1D)
EnergyLinkHook:
  JSR EnergyLink

%org($A000, $1E)
db $21, $A5, $0C, "PLACEHOLDER 1"
db $21, $C5, $0C, "PLACEHOLDER 2"
db $21, $E5, $0C, "PLACEHOLDER 3"
db $22, $05, $0C, "PLACEHOLDER P"
db $22, $45, $0C, "PLACEHOLDER 1"
db $22, $65, $0C, "PLACEHOLDER 2"
db $22, $85, $0C, "PLACEHOLDER 3"
db $22, $A5, $0C, "PLACEHOLDER P", $FF
db $21, $A5, $0C, "PLACEHOLDER 1"
db $21, $C5, $0C, "PLACEHOLDER 2"
db $21, $E5, $0C, "PLACEHOLDER 3"
db $22, $05, $0C, "PLACEHOLDER P", $FF
db $21, $A5, $0C, "PLACEHOLDER 1"
db $21, $C5, $0C, "PLACEHOLDER 2"
db $21, $E5, $0C, "PLACEHOLDER 3"
db $22, $05, $0C, "PLACEHOLDER P", $FF
db $21, $A5, $0C, "PLACEHOLDER 1"
db $21, $C5, $0C, "PLACEHOLDER 2"
db $21, $E5, $0C, "PLACEHOLDER 3"
db $22, $05, $0C, "PLACEHOLDER P", $FF
db $21, $A5, $0C, "PLACEHOLDER 1"
db $21, $C5, $0C, "PLACEHOLDER 2"
db $21, $E5, $0C, "PLACEHOLDER 3"
db $22, $05, $0C, "PLACEHOLDER P", $FF
db $21, $A5, $0C, "PLACEHOLDER 1"
db $21, $C5, $0C, "PLACEHOLDER 2"
db $21, $E5, $0C, "PLACEHOLDER 3"
db $22, $05, $0C, "PLACEHOLDER P", $FF
db $21, $A5, $0C, "PLACEHOLDER 1"
db $21, $C5, $0C, "PLACEHOLDER 2"
db $21, $E5, $0C, "PLACEHOLDER 3"
db $22, $05, $0C, "PLACEHOLDER P", $FF
db $21, $A5, $0C, "PLACEHOLDER 1"
db $21, $C5, $0C, "PLACEHOLDER 2"
db $21, $E5, $0C, "PLACEHOLDER 3"
db $22, $05, $0C, "PLACEHOLDER P"
db $22, $45, $0C, "PLACEHOLDER 1"
db $22, $65, $0C, "PLACEHOLDER 2"
db $22, $85, $0C, "PLACEHOLDER 3"
db $22, $A5, $0C, "PLACEHOLDER P", $FF

ShowItemString:
  STY $04
  LDA ItemLower,X
  STA $02
  LDA ItemUpper,X
  STA $03
  LDY #$00
  .LoadString:
  LDA ($02),Y
  ORA $10
  STA $0780,Y
  BMI .Return
  INY
  LDA ($02),Y
  STA $0780,Y
  INY
  LDA ($02),Y
  STA $0780,Y
  STA $00
  INY
  .LoadCharacters:
  LDA ($02),Y
  STA $0780,Y
  INY
  DEC $00
  BPL .LoadCharacters
  BMI .LoadString
  .Return:
  STA $19
  LDY $04
  RTS

ItemUpper:
  db $A0, $A0, $A0, $A1, $A1, $A1, $A1, $A2, $A2

ItemLower:
  db $00, $81, $C2, $03, $44, $85, $C6, $07, $47

%org($C8F7, $3E)
RemoveRushCoil:
  NOP #4

%org($CA73, $3E)
HookController:
  JMP ControllerHook
  NOP

%org($DA18, $3E)
NullWeaponGet:
  NOP #5 ; TODO: see if I can reroute this write instead for nicer timings

%org($DB99, $3E)
HookMidDoc:
  JSR SetMidDoc
  NOP

%org($DBB0, $3E)
HoodEndDoc:
  JSR SetEndDoc
  NOP

%org($DC57, $3E)
RerouteStageComplete:
  LDA $60
  JSR SetStageComplete
  NOP #2

%org($DC6F, $3E)
RerouteRushMarine:
  JMP SetRushMarine
  NOP

%org($DC6A, $3E)
RerouteRushJet:
  JMP SetRushJet
  NOP

%org($DC78, $3E)
RerouteWilyComplete:
  JMP SetEndWily
  NOP
  EndWilyReturn:

%org($DF81, $3E)
NullBreak:
  NOP #5 ; nop break man giving every weapon

%org($E15F, $3F)
Wily4:
  JMP Wily4Comparison
  NOP


%org($F340, $3F)
RewireDocRobotAccess:
  LDA !current_state
  BNE .DocRobo
  LDA !received_rbm_stages
  SEC
  BCS .Return
  .DocRobo:
  LDA !received_doc_stages
  .Return:
  AND $9DED,Y
  RTS

ChangeStageMode:
  ; also handles hot reload of stage select
  ; kinda broken, sprites don't disappear and palettes go wonky with Break Man access
  ; but like, it functions!
  LDA !sound_effect_strobe
  BEQ .Continue
  JSR $F89A
  LDA #$00
  STA !sound_effect_strobe
  .Continue:
  LDA $14
  AND #$20
  BEQ .Next
  LDA !current_state
  BNE .Set
  LDA !completed_doc_stages
  CMP #$C5
  BEQ .BreakMan
  LDA #$09
  SEC
  BCS .Set
  .EarlyReturn:
  LDA $14
  AND #$90
  RTS
  .BreakMan:
  LDA #$12
  .Set:
  EOR !current_state
  STA !current_state
  LDA #$01
  STA !rbm_strobe
  .Next:
  LDA !rbm_strobe
  BEQ .EarlyReturn
  LDA #$00
  STA !rbm_strobe
  ; Clear the sprite buffer
  LDX #$98
  .Loop:
  LDA #$00
  STA $01FF, X
  DEX
  STA $01FF, X
  DEX
  STA $01FF, X
  DEX
  LDA #$F8
  STA $01FF, X
  DEX
  CPX #$00
  BNE .Loop
  ; Break Man Sprites
  LDX #$24
  .Loop2:
  LDA #$00
  STA $02DB, X
  DEX
  STA $02DB, X
  DEX
  STA $02DB, X
  DEX
  LDA #$F8
  STA $02DB, X
  DEX
  CPX #$00
  BNE .Loop2
  ; Swap out the tilemap and write sprites
  LDY #$10
  LDA $11
  BMI .B1
  LDA $FD
  EOR #$01
  ASL A
  ASL A
  STA $10
  LDA #$01
  JSR $E8B4
  LDA #$00
  STA $70
  STA $EE
  .B3:
  LDA $10
  PHA
  JSR $EF8C
  PLA
  STA $10
  JSR $FF21
  LDA $70
  BNE .B3
  JSR $995C
  LDX #$03
  JSR $939E
  JSR $FF21
  LDX #$04
  JSR $939E
  LDA $FD
  EOR #$01
  STA $FD
  LDY #$00
  LDA #$7E
  STA $E9
  JSR $FF3C
  .B1:
  LDX #$00
  ; palettes
  .B2:
  LDA $9C33,Y
  STA $0600,X
  LDA $9C23,Y
  STA $0610,X
  INY
  INX
  CPX #$10
  BNE .B2
  LDA #$FF
  STA $18
  LDA #$01
  STA $12
  LDA #$03
  STA $13
  LDA $11
  JSR $99FA
  LDA $14
  AND #$90
  RTS

InvertSelectTiles:
  LDY !current_state
  BNE .DocRobo
  AND !received_rbm_stages
  SEC
  BCS .Compare
  .DocRobo:
  AND !received_doc_stages
  .Compare:
  BNE .False
  JMP $996A
  .False:
  JMP $99BA

InvertSelectSprites:
  LDY !current_state
  BNE .DocRobo
  AND !received_rbm_stages
  SEC
  BCS .Compare
  .DocRobo:
  AND !received_doc_stages
  .Compare:
  BNE .False
  JMP $9A58
  .False:
  JMP $9A6D

SetStageComplete:
  CMP #$00
  BNE .DocRobo
  LDA !completed_rbm_stages
  ORA $DEC2, Y
  STA !completed_rbm_stages
  SEC
  BCS .Return
  .DocRobo:
  LDA !completed_doc_stages
  ORA $DEC2, Y
  STA !completed_doc_stages
  .Return:
  RTS

ControllerHook:
  ; Jump in here too for sfx
  LDA !sound_effect_strobe
  BEQ .Next
  JSR $F89A
  LDA #$00
  STA !sound_effect_strobe
  .Next:
  LDA !controller_mirror
  CMP !CONTROLLER_ALL_BUTTON
  BNE .Continue
  JMP $CBB1
  .Continue:
  LDA !controller_flip
  AND #$10 ; start
  JMP $CA77

SetRushMarine:
  LDA #$01
  SEC
  BCS SetRushAcquire

SetRushJet:
  LDA #$02
  SEC
  BCS SetRushAcquire

SetRushAcquire:
  ORA !acquired_rush
  STA !acquired_rush
  RTS

ApplyLastWily:
  LDA !controller_mirror
  AND !CONTROLLER_SELECT
  BEQ .LastWily
  .Default:
  LDA #$00
  SEC
  BCS .Set
  .LastWily:
  LDA !last_wily
  BEQ .Default
  SEC
  SBC #$0C
  .Set:
  STA $75 ; wily index
  LDA #$03
  STA !current_stage
  RTS

SetMidDoc:
  LDA !current_stage
  SEC
  SBC #$08
  ASL
  TAY
  LDA #$01
  .Loop:
  CPY #$00
  BEQ .Return
  DEY
  ASL
  SEC
  BCS .Loop
  .Return:
  ORA !doc_robo_kills
  STA !doc_robo_kills
  LDA #$00
  STA $30
  RTS

SetEndDoc:
  LDA !current_stage
  SEC
  SBC #$08
  ASL
  TAY
  INY
  LDA #$01
  .Loop:
  CPY #$00
  BEQ .Set
  DEY
  ASL
  SEC
  BCS .Loop
  .Set:
  ORA !doc_robo_kills
  STA !doc_robo_kills
  .Return:
  LDA #$0D
  STA $30
  RTS

SetEndWily:
  LDA !current_wily
  PHA
  CLC
  ADC #$0C
  STA !last_wily
  PLA
  TAX
  LDA #$01
  .WLoop:
  CPX #$00
  BEQ .WContinue
  DEX
  ASL A
  SEC
  BCS .WLoop
  .WContinue:
  ORA !wily_stage_completion
  STA !wily_stage_completion
  INC !current_wily
  LDA #$9C
  JMP EndWilyReturn


SetBreakMan:
  LDA #$80
  ORA !wily_stage_completion
  STA !wily_stage_completion
  LDA #$16
  STA $22
  RTS
  
CheckFirstWep:
  LDA $B4
  BEQ .SetNone
  TAY
  .Loop:
  LDA $00A2,Y
  BMI .SetNew
  INY
  CPY #$0C
  BEQ .SetSame
  BCC .Loop
  .SetSame:
  LDA #$80
  STA $A1
  JMP $A3A1
  .SetNew:
  TYA
  SEC
  SBC $B4
  BCS .Set
  .SetNone:
  LDA #$00
  .Set:
  STA $A1
  JMP $A3DE

Wily4Comparison:
  TYA
  PHA
  TXA
  PHA
  LDY #$00
  LDX #$08
  LDA #$01
  .Loop:
  PHA
  AND $6E
  BEQ .Skip
  INY
  .Skip:
  PLA
  ASL
  DEX
  BNE .Loop
  print "Wily 4 Requirement:", hex(realbase())
  CPY #$08
  BCC .Return
  LDA #$FF
  STA $6E
  .Return:
  PLA
  TAX
  PLA
  TAY
  LDA #$0C
  STA $EC
  RTS

; out of space here :(

%org($FDBA, $3F)
WeaponReceived:
  TAX
  LDA $F5
  PHA
  LDA #$1E
  STA $F5
  JSR $FF6B
  TXA
  JSR ShowItemString
  PLA
  STA $F5
  JSR $FF6B
  RTS

CheckConsumable:
  STA $0150, Y
  LDA $0320, X
  CMP #$64
  BMI .Return
  print "Consumables (replace 67): ", hex(realbase())
  CMP #$6A
  BPL .Return
  LDA #$00
  STA $0300, X
  JMP $BE49
  .Return:
  JMP $BE25

EnergyLink:
  print "Energylink: ", hex(realbase())
  LDA #$01
  BEQ .Return
  TYA
  STA !energylink_packet
  LDA #$49
  STA $00
  .Return:
  LDA $BDEC, Y
  RTS

; out of room here :(
