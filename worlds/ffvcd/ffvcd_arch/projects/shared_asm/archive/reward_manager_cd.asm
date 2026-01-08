hirom
org $c00e3a
JML ChestHook1

org !ADDRESS_chesthook
ChestHook1:
STZ $BB0
lda $D13213,x
STA !rewardid
LDA !typeid
CMP #$50 ; if new id 'JOB' 
BEQ IntermediateBranchToJobReward
LDA !typeid
CMP #$60
BEQ IntermediateBranchToAbilityReward
LDA !typeid
CMP #$20
BEQ IntermediateBranchToMagicReward
LDA !typeid
CMP #$30
BEQ IntermediateBranchToKeyItemReward
LDA !typeid
BPL BranchIfPlusChestIDBranch
JML $C00E44

IntermediateBranchToAbilityReward:
phy
phx
php
JSL BranchToAbilityReward
plp
plx
ply
JML $C00E3E

IntermediateBranchToMagicReward:
phy
phx
php
JSL BranchToMagicReward
plp
plx
ply
JML $C00E69

IntermediateBranchToKeyItemReward:
JSL BranchToKeyItemReward
JML $c00e74

BranchIfPlusChestIDBranch:
JML $C00E47

IntermediateBranchToJobReward:
JSL BranchToJobReward
JML $c00e74

BranchToJobReward:
LDA !rewardid
; sets of 8 jobs per unlockedjobs1/2/3
;unlockedjobs1
CMP #$00; Knight
BEQ RewardKnight
CMP #$01; Monk
BEQ RewardMonk
CMP #$02; Thief
BEQ RewardThief
CMP #$03; Dragoon
BEQ RewardDragoon
CMP #$04; Ninja
BEQ RewardNinja
CMP #$05; Samurai
BEQ RewardSamurai
CMP #$06; Berserker
BEQ RewardBerserker
CMP #$07; Hunter
BEQ RewardHunter
JMP CheckSecondJobs


RewardKnight:
LDA #$80
TSB !unlockedjobs1
JMP JobsAssigned
RewardMonk:
LDA #$40
TSB !unlockedjobs1
JMP JobsAssigned
RewardThief:
LDA #$20
TSB !unlockedjobs1
JMP JobsAssigned
RewardDragoon:
LDA #$10
TSB !unlockedjobs1
JMP JobsAssigned
RewardNinja:
LDA #$08
TSB !unlockedjobs1
JMP JobsAssigned
RewardSamurai:
LDA #$04
TSB !unlockedjobs1
JMP JobsAssigned
RewardBerserker:
LDA #$02
TSB !unlockedjobs1
JMP JobsAssigned
RewardHunter:
LDA #$01
TSB !unlockedjobs1
JMP JobsAssigned



;unlockedjobs2
CheckSecondJobs:
CMP #$08; MysticKnight
BEQ RewardMysticKnight
CMP #$09; WhiteMage
BEQ RewardWhiteMage
CMP #$0A; BlackMage
BEQ RewardBlackMage
CMP #$0B; TimeMage
BEQ RewardTimeMage
CMP #$0C; Summoner
BEQ RewardSummoner
CMP #$0D; Blue Mage
BEQ RewardRedMage
CMP #$0E; Red Mage
BEQ RewardRedMage
CMP #$0F; Mediator
BEQ RewardMediator
JMP CheckThirdJobs


RewardMysticKnight:
LDA #$80
TSB !unlockedjobs2
JMP JobsAssigned
RewardWhiteMage:
LDA #$40
TSB !unlockedjobs2
JMP JobsAssigned
RewardBlackMage:
LDA #$20
TSB !unlockedjobs2
JMP JobsAssigned
RewardTimeMage:
LDA #$10
TSB !unlockedjobs2
JMP JobsAssigned
RewardSummoner:
LDA #$08
TSB !unlockedjobs2
JMP JobsAssigned
RewardBlueMage:
LDA #$04
TSB !unlockedjobs2
JMP JobsAssigned
RewardRedMage:
LDA #$02
TSB !unlockedjobs2
JMP JobsAssigned
RewardMediator:
LDA #$01
TSB !unlockedjobs2
JMP JobsAssigned


;unlockedjobs3
CheckThirdJobs:
CMP #$10; Chemist
BEQ RewardChemist
CMP #$11; Geomancer
BEQ RewardGeomancer
CMP #$12; Bard
BEQ RewardBard
CMP #$13; Dancer
BEQ RewardDancer
CMP #$14; Mimic
BEQ RewardMimic
CMP #$15; Freelancer
BEQ RewardFreelancer
; for some reason if none are met, JMP to end
JMP JobsAssigned

RewardChemist:
LDA #$80
TSB !unlockedjobs3
JMP JobsAssigned
RewardGeomancer:
LDA #$40
TSB !unlockedjobs3
JMP JobsAssigned
RewardBard:
LDA #$20
TSB !unlockedjobs3
JMP JobsAssigned
RewardDancer:
LDA #$10
TSB !unlockedjobs3
JMP JobsAssigned
RewardMimic:
LDA #$08
TSB !unlockedjobs3
JMP JobsAssigned
RewardFreelancer:
LDA #$04
TSB !unlockedjobs3
JMP JobsAssigned

JobsAssigned:
LDA #$02
STA $AF
LDA !rewardid
STA $16a3
RTL






org !ADDRESS_progressiverewards
;################
;Reward Abilities
;################
BranchToAbilityReward:

rep #$20
lda !rewardid
asl a
asl a
asl a
sta !progabilityentry
lda #$0000 ;loop counter
sep #$20

sta !loopcounter

AbilityProgressionLoop:
lda !loopcounter

; if our index is 8, we already have everything in that progression, exit early
cmp #$08
beq AbilityGetLastAndExit

; if the current progression value is $#FF, no more progression is defined, exit early
ldx !progabilityentry
lda !progabilitytable, x ;load the current ability to check
sta !currentability
cmp #$FF
beq AbilityGetLastAndExit

;divide by 8 to get the byte we want to reference and store in y
lsr a
lsr a
lsr a
tay

;retrieve the current ability again and test it against #$07 to 
;know which bit we're referring to
lda !currentability
and #$07
tax

;load the byte storing the relevant ability info. And it vs
;the correct bit.
lda !unlockedability,y
and $C0C9B9,x

;if the result isn't 0, we have that ability already, so loop again
bne AbilityProgressionReloop

;otherwise, we don't have that ability, so load the value back into a and exit, also clean up our stack
lda !currentability
jmp AbilityExitProgression

AbilityProgressionReloop:
inc !progabilityentry
inc !loopcounter
jmp AbilityProgressionLoop

AbilityGetLastAndExit: ;get last result, which should be valid, and exit with that in a
ldx !progabilityentry
dex
lda !progabilitytable, x
sta !currentability
jmp AbilityExitProgression

AbilityExitProgression:
pha
lsr a
lsr a
lsr a
tay
pla
and #$07
tax
lda !1pabilities, y
ora $C0C9B9,X
sta !1pabilities, y

lda !2pabilities, y
ora $C0C9B9,X
sta !2pabilities, y

lda !3pabilities, y
ora $C0C9B9,X
sta !3pabilities, y

lda !4pabilities, y
ora $C0C9B9,X
sta !4pabilities, y

inc !1pabilitiescount
inc !2pabilitiescount
inc !3pabilitiescount
inc !4pabilitiescount

; end with generic finisher
lda !currentability
RTL


;###################
;Reward Magic Spells
;###################
BranchToMagicReward:

sep #$10
lda !rewardid
asl a
asl a
sta !progmagicentry

lda #$00 ;loop counter
sta !loopcounter

MagicProgressionLoop:
lda !loopcounter

; if our index is 4, we already have everything in that progression, exit early
cmp #$04 
beq MagicGetLastAndExit

; if the current progression value is $#FF, no more progression is defined, exit early
ldx !progmagicentry
lda !progmagictable, x ;load the current magic to check
sta !currentmagic
cmp #$FF
beq MagicGetLastAndExit

;divide by 8 to get the byte we want to reference and store in y
lsr a
lsr a
lsr a
tay

;retrieve the current magic again and test it against #$07 to 
;know which bit we're referring to
lda !currentmagic
and #$07
tax

;load the byte storing the relevant spell info. And it vs
;the correct bit.
lda !unlockedmagic,y
and $C0C9B9,x

;if the result isn't 0, we have that spell already, so loop again
bne MagicProgressionReloop

;otherwise, we don't have that spell, so load the value back into a and exit, also clean up our stack
lda !currentmagic
jmp MagicExitProgression

MagicProgressionReloop:
inc !progmagicentry
inc !loopcounter
jmp MagicProgressionLoop

MagicGetLastAndExit: ;get last result, which should be valid, and exit with that in a
ldx !progmagicentry
dex
lda !progmagictable, x
jmp MagicExitProgression

MagicExitProgression:
RTL







; this code will set the proper bits per key item
; refer to key_items.asm 
BranchToKeyItemReward:

; these are set up manually. this is for debugging & cleanliness
; no reason to come up with a complex indexing table here

; we're going to be using a custom bit setter 
; so we'll push A and X and Y
pha 
phx
phy
LDA !rewardid

; CANAL KEY
CMP #$12
BNE KeyItemContinue1
JSL KeyItemTornaCanal
JMP KeyItemAddText


; WALSE KEY
KeyItemContinue1:
CMP #$00
BNE KeyItemContinue2
JSL KeyItemWalseKey
JMP KeyItemAddText

; STEAMSHIP KEY
KeyItemContinue2:
CMP #$01
BNE KeyItemContinue3
JSL KeyItemSteamshipKey
JMP KeyItemAddText

; IFRITS FIRE
KeyItemContinue3:
CMP #$02
BNE KeyItemContinue4
JSL KeyItemIfritsFire
JMP KeyItemAddText


; SandWormBait
KeyItemContinue4:
CMP #$03
BNE KeyItemContinue5
JSL KeyItemSandWormBait
JMP KeyItemAddText

; Adamantite
KeyItemContinue5:
CMP #$15
BNE KeyItemContinue6
JSL KeyItemAdamantite
JMP KeyItemAddText

; Big Bridge Key
KeyItemContinue6:
CMP #$04
BNE KeyItemContinue7
JSL KeyItemBigBridge
JMP KeyItemAddText

KeyItemContinue7:

; Moogle Suit
CMP #$16
BNE KeyItemContinue8
JSL KeyItemMoogleSuit
JMP KeyItemAddText

KeyItemContinue8:

; Submarine Key
CMP #$06
BNE KeyItemContinue9
JSL KeyItemSubmarineKey
JMP KeyItemAddText

KeyItemContinue9:

; Hiryuu Call
CMP #$05
BNE KeyItemContinue10
JSL KeyItemHiryuuCall
JMP KeyItemAddText

KeyItemContinue10:

; Elder Branch
CMP #$18
BNE KeyItemContinue11
JSL KeyItemElderBranch
JMP KeyItemAddText

KeyItemContinue11:

; Elder Branch
CMP #$08
BNE KeyItemContinue12
JSL KeyItemBracelet
JMP KeyItemAddText

KeyItemContinue12:

; Anti Barrier
CMP #$07
BNE KeyItemContinue13
JSL KeyItemAntiBarrier
JMP KeyItemAddText

KeyItemContinue13:

; Pyramid Page
CMP #$0B
BNE KeyItemContinue14
JSL KeyItemPyramidPage
JMP KeyItemAddText

KeyItemContinue14:

; Shrine Page
CMP #$0C
BNE KeyItemContinue15
JSL KeyItemShrinePage
JMP KeyItemAddText

KeyItemContinue15:

; Trench Page
CMP #$0D
BNE KeyItemContinue16
JSL KeyItemTrenchPage
JMP KeyItemAddText

KeyItemContinue16:

; Falls Page
CMP #$0E
BNE KeyItemContinue17
JSL KeyItemFallsPage
JMP KeyItemAddText

KeyItemContinue17:



; Pyramid 1st Tablet
CMP #$1A
BNE KeyItemContinue18
JSL KeyItem1stTablet
JMP KeyItemAddText

KeyItemContinue18:

; Shrine 2nd Tablet
CMP #$1B
BNE KeyItemContinue19
JSL KeyItem2ndTablet
JMP KeyItemAddText

KeyItemContinue19:

; Trench 3rd Tablet
CMP #$1C
BNE KeyItemContinue20
JSL KeyItem3rdTablet
JMP KeyItemAddText

KeyItemContinue20:

; Falls 4th Tablet
CMP #$1D
BNE KeyItemContinue21
JSL KeyItem4thTablet
JMP KeyItemAddText

KeyItemContinue21:

KeyItemAddText:
; < SET UP KEY ITEM SETTER HERE > 
LDA !rewardid
pha
lsr a
lsr a
lsr a
tay
pla
and #$07
tax
lda !eventflags, y
ora $C0C9B9,X
sta !eventflags, y


EndKeyItemReward:
ply
plx
pla

; end with generic finisher
JML JobsAssigned










; hook for changing indexing based on job id or not 
org $C08AC2
JML JobIndexing

org !ADDRESS_jobindexing
JobIndexing:
ADC $0F
PHA
sep #$20
LDA !typeid ; $000B11, the reward type (50 = JOB)
CMP #$50
BEQ AddJobIndex
CMP #$30
BEQ AddKeyItemIndex
CMP #$60
BEQ AddAbilityIndex
BNE DoNotAddJobIndex


; if job, then add #$1D00 to index
AddJobIndex:
rep #$20
PLA
STA $0F ; store A into $000B0F
LDA #$1D00
CLC
ADC $0F ; original contents + 1D00
; continue as usual
TAX
LDA $06
JML $C08AC7

AddKeyItemIndex:
; if ability, then add #$28A0 (for E78100 starting)
rep #$20
PLA
STA $0F ; store A into $000B0F
LDA #$28A0
CLC
ADC $0F ; original contents + 1D00
; continue as usual
TAX
LDA $06
JML $C08AC7

AddAbilityIndex:
; if ability, then add #$2EA0 (for E78700 starting)
rep #$20
PLA
STA $0F ; store A into $000B0F
LDA #$2EA0
CLC
ADC $0F ; original contents + 1D00
; continue as usual
TAX
LDA $06
JML $C08AC7




DoNotAddJobIndex:
rep #$20
PLA
TAX
LDA $06
JML $C08AC7