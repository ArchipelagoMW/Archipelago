norom
!headersize = 16

!controller_flip = $14 ; only on first frame of input, used by crash man, etc
!controller_mirror = $16
!current_stage = $22
!current_state = $60
!completed_rbm_stages = $61
!completed_doc_stages = $62
;!received_items = $63
!acquired_rush = $64
!received_rmb_stages = $680
!received_doc_stages = $681
; !deathlink = $30, set to $0E
!energylink_packet = $682
!last_wily = $683
!rbm_strobe = $684
!sound_effect_strobe = $685
!doc_robo_kills = $686
!wily_stage_completion = $687

!current_weapon = $A0
!current_health = $A2
!received_weapons = $A3


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
    if <bank> == $1E
        org <address>-$C000+($2000*<bank>)+!headersize ; org sets the position in the output file to write to (in norom, at least)
        base <address> ; base sets the position that all labels are relative to - this is necessary so labels will still start from $8000, instead of $0000 or somewhere
    else 
      if <bank> == $1F
          org <address>-$E000+($2000*<bank>)+!headersize ; org sets the position in the output file to write to (in norom, at least)
          base <address> ; base sets the position that all labels are relative to - this is necessary so labels will still start from $8000, instead of $0000 or somewhere
      else
          org <address>-$8000+($2000*<bank>)+!headersize
          base <address>
      endif
    endif
endmacro

%org($802F, $0B)
HookBreakMan:
  JSR SetBreakMan
  NOP

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

%org($C8F7, $1E)
RemoveRushCoil:
  NOP #4

%org($CA73, $1E)
HookController:
  JMP ControllerHook
  NOP

%org($DA18, $1E)
NullWeaponGet:
  NOP #5 ; TODO: see if I can reroute this write instead for nicer timings

%org($DB99, $1E)
HookMidDoc:
  JSR SetMidDoc
  NOP

%org($DBB0, $1E)
HoodEndDoc:
  JSR SetEndDoc
  NOP

%org($DC57, $1E)
RerouteStageComplete:
  LDA $60
  JSR SetStageComplete
  NOP #2

%org($DC6F, $1E)
RerouteRushMarine:
  LDA #$01
  JMP SetRushAcquire

%org($DC6A, $1E)
RerouteRushJet:
  LDA #$02
  JMP SetRushAcquire

%org($F340, $1F)
RewireDocRobotAccess:
  LDA !current_state
  BNE .DocRobo
  LDA !received_rmb_stages
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
  .B2:
  LDA $9C33,Y
  STA $0600,X
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
  AND !received_rmb_stages
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
  AND !received_rmb_stages
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

SetRushAcquire:
  ORA $64
  STA $64
  RTS

SetWilyStageComplete:
  LDA !current_stage
  STA !last_wily
  SEC
  SBC #$0C
  TAX
  LDA #$01
  CPX #$00
  BEQ $F45D
  DEX
  ASL A
  SEC
  BCS $F454
  ORA $0687
  STA $0687
  LDA #$16
  STA $22
  RTS

ApplyLastWily:
  LDA !controller_mirror
  AND !CONTROLLER_SELECT
  BEQ .LastWily
  LDA #$00
  SEC
  BCS .Set
  .LastWily:
  LDA !last_wily
  SEC
  SBC #$0C
  .Set:
  STA $75 ; wily index
  LDA #$03
  STA !current_stage
  RTS

SetMidDoc:
  LDA $22
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
  LDA $22
  SEC
  SBC #$08
  ASL
  TAY
  INY
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
  LDA #$0D
  STA $30
  RTS

SetBreakMan:
  LDA #$80
  ORA !wily_stage_completion
  STA !wily_stage_completion
  LDA #$16
  STA $22
  RTS