norom
!headersize = 16

!controller_mirror = $16
!controller_flip = $14 ; only on first frame of input, used by crash man, etc
!current_stage = $2A
!current_state = $60
!completed_rbm_stages = $61
!completed_doc_stages = $62
!received_rmb_stages = $680
!received_doc_stages = $681
; !deathlink = $30, set to $0E
!energylink_packet = $682
!last_wily = $683
!rbm_strobe = $684
!doc_robo_kills = $0685
!wily_stage_completion = $0686

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

%org($C8F7, $1E)
RemoveRushCoil:
  NOP #4

%org($CA73, $1E)
HookController:
  JMP ControllerHook
  NOP

%org($DA1A, $1E)
NullWeaponGet:
  NOP #5 ; TODO: see if I can reroute this write instead for nicer timings

%org($DC57, $1E)
RerouteStageComplete:
  LDA $60
  JSR SetStageComplete
  NOP #2

%org($F320, $1F)
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
  LDA $14
  AND #$20
  BEQ .Next
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
  LDA !controller_mirror
  CMP !CONTROLLER_ALL_BUTTON
  BNE .Continue
  JMP $CBB1
  .Continue:
  LDA !controller_flip
  CMP #$10 ; start
  JMP $CA77