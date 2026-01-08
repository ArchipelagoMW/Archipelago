; Author: TestRunner

lorom
arch snes.cpu

; New message ID start at 0x60, there are more lower IDs, but this is simplest. max is 0x7F
; Change map station plms (B6D3) to message station (F2C0)
;     PLM arg: hi bit = unset, hi byte = message id, low byte = event id
; Message box table starts at 0x296ed (pc)
;     8436,8289,XXXX
; Buttom table starts at 0x29857 (pc)
;     This table should just be filled with 00s
;     Can probably be omitted, if so ,ID can start at 0x40
; Log Events sgo from 0xF2 to 0xFF, more lower values can be used, but the used elevator flags should be skipped over
;     E0  Lomry-Space
;     F0  Oceania-ShipR
;     F1  Oceania-ShipD



!log_hint_event = $00F2 ; index + 0xF2 is the discovered event
!log_hint_id = $01C0  ; index + 0x01C0 is the logbook discovered event



org $84fb66
LogPLMTrigger_no_notify:
    ; the no notify log event plm is only used for hints. disable them
    ; alternatively could've removed all the PLMs but this was simpler
    ;JSL SetLogEvent ; set event bit
    NOP : NOP : NOP : NOP

org $8DE3AB
    ; Revert hook to disable heated room logbook hint
    ;JSL SetHeatLog
    ;NOP : NOP
    LDA $1EED
    CMP $1EEF

; hook in pause logbook loading
org $bcd9ba
    JSL LogLoadInjection


org $bcdc44
SetLogEvent:


org $858477
MessageBoxWaitTable_LoadA:
    JSL LoadMessageBoxWaitTable
    ;LDA.l MessageBoxWaitTable,X

org $8586a5
MessageBoxWaitTable_LoadB:
    JSL LoadMessageBoxWaitTable
    ;LDA.l MessageBoxWaitTable,X


org $8586d2
MessageBoxWaitTable:



org $8FF600
RoomASMCheckEvents:
    JSL ManyStateTest
    BCS .return
    LDA #$6000 ; if events are not complete then
    STA $1E15  ; set message box plm to give incomplete message
.return
    RTS


org $A1C000
EventTestList:
    DB $00, $00, $00, $00, $00, $00, $00, $00
    DB $00, $00, $00, $00
.end

ManyStateTest:
  PHX
  LDX #(EventTestList_end-EventTestList-1) ; index of last event, for looping backwards
-
  LDA.l EventTestList,X
  AND #$00FF ; check a byte at a time
  BEQ +      ; skip event if 0
  JSL $808233 ; test event
  BCC .fail   ; if any event fails, then return CLC
+ 
  DEX
  BPL -       ; loop over all events in list

.pass
  SEC         ; if all events passed, then return SEC
.fail
  PLX
  RTL


;SetInitFlags:
;    ; Set Event ID 0x3E
;    LDA #$003E
;    JSL $8081FA
;    RTL


LogLoadInjection:
    ; displaced code
    STZ $B1      ; BG1 X scroll = 0
    STZ $B3      ; BG1 Y scroll = 0

    ; for each event in the list
    LDX #(EventTestList_end-EventTestList-1) ; index of last event, for looping backwards
.loop
.testDiscovered
    TXA
    CLC : ADC #!log_hint_event
    JSL $808233 ; check if event is set
    BCC .testComplete ; mark hint as discovered if event set
    ; set log entry
    TXA
    ASL ; log entries are every other
    CLC : ADC #!log_hint_id
    JSL SetLogEvent

.testComplete
    TXA
    LDA.l EventTestList,X
    AND #$00FF
    BEQ .next ; skip if event is 0
    JSL $808233 ; test event
    BCC .clearComplete
.setComplete ; if event is set, mark hint as complete
    TXA
    CLC
    ADC #$01E1
    JSL $BCDC44 ; set logbook event
    BRA .next
.clearComplete ; if event is not set, mark hint incomplete
    TXA
    CLC
    ADC #$01E1
    JSL ClearLogbookEvent

.next
    DEX
    BPL .loop ; loop for all events

    RTL


ClearLogbookEvent:
    PHX
    PHY
    PHP
    REP #$30
    JSL $80818E ; get bit mask + offset
    LDA $7FFE20,X
    BIT $05E7
    BEQ .return ; return if already clear
    EOR #$FFFF
    ORA $05E7
    STA $7FFE20,X ; clear bit
    EOR #$FFFF; does nothing ???
    JSL $81EF24 ; save logbook sram
    SEC
.return
    PLP
    PLY
    PLX
    RTL


LoadMessageBoxWaitTable:
    LDA.l MessageBoxWaitTable,X ; load message box time length
    CPX #$0040                  ; if message box id > 0x40
    BMI +
    LDA #$000A                  ; then use message box time 0x0A frames
+
    RTL
