//; Base Patch for Kirby 64 - The Crystal Shards Archipelago
.n64

.open "Kirby 64 - The Crystal Shards (USA).z64", "K64Basepatch.z64", 0x0

//; NOP CRC checks
.org 0x63C
nop

.org 0x648
nop

.headersize 0x80000400 - 0x1000 //;ovl0

.org 0x80005400
alloc_with_alignment:

.headersize 0x8009B540 - 0x43790 //;ovl1

.org 0x800A28A8
OpenNewWorld:
li      at, LevelStart
addu    at, at, t7
lb      s2, 0x0000 (at)
sb      s2, 0x0007 (s6)
jr      ra

.org 0x800A3B1C
jal     RedirectStage
nop

.org 0x800A3CC0
nop

.org 0x800A3CD4
nop

.org 0x800A3E0C
jal     AllowFinalBoss
nop

.org 0x800A3E30
lw      t5, 0x6C78 (t5)
addiu   at, r0, 0x0001
addiu   a0, r0, 0x000D
bne     t5, at, 0x800A3F4C

.org 0x800A3CE8
jal     PreventBossAccess

.org 0x800A3D80
sw      s2, 0x6B7C (at)
jal     OpenNewWorld
nop

.org 0x800A3EFC
jal     SetZeroTwoComplete
nop

.org 0x800A7678
PlaySFX:

.org 0x800B8C94
jal     SetStartingStage

.org 0x800B9568
j       MarkStagesIncomplete
nop
.org 0x800E4550
gEntitiesScaleXArray:

.org 0x800E4710 
gEntitiesScaleYArray:

.org 0x800E48D0 
gEntitiesScaleZArray:

.headersize 0x800f61a0 - 0x7ec10 //; ovl2

.org 0x800F8568
j       DededeOverride
nop

//; Block Copy Abilities and Power Combos when flag isn't set
.org 0x80127490
.db "ARCHIPELAGO_DATA"
// Starting Stage for Levels
LevelStart:
.db 0x00, 0x03, 0x04, 0x04, 0x04, 0x04, 0x03, 0x01
CrystalRequirements:
// Placeholder values for crystal requirements
.db 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0xFF, 0xFF
SlotData:
.fill 16
LevelIndex:
//; Level Order
.dw 0, 0, 0, 0, -1, -1, -1, -1
.dw 1, 1, 1, 1, 1, -1, -1, -1
.dw 2, 2, 2, 2, 2, -1, -1, -1
.dw 3, 3, 3, 3, 3, -1, -1, -1
.dw 4, 4, 4, 4, 4, -1, -1, -1
.dw 5, 5, 5, 5, -1, -1, -1, -1
StageIndex:
//; Stage Order
.dw 0, 1, 2, 3, -1, -1, -1, -1
.dw 0, 1, 2, 3, 4, -1, -1, -1
.dw 0, 1, 2, 3, 4, -1, -1, -1
.dw 0, 1, 2, 3, 4, -1, -1, -1
.dw 0, 1, 2, 3, 4, -1, -1, -1
.dw 0, 1, 2, 3, -1, -1, -1, -1

CopyAbilityBlocker:
lui     at, 0x800D
ld      t0, 0x6C68 (at) //; Get Copy Ability Flag dw
addiu   t7, r0, 0x0001
addiu   t2, v0, -0x0001
dsllv    t7, t7, t2      //; Shift current ability to match
and     t0, t0, t7
bnez    t0, @@ReturnToSwallow //; we are allowed to use the ability
nop
addiu   v0, r0, 0x0000
addiu   a0, r0, 0x0000
lui     at, 0x8013
sw      v0, 0xE850 (at)
@@ReturnToSwallow:
j       0x8012310C
nop

SetStartingStage:
addiu   a2, r0, 0x0003
sw      a2, 0x0014 (a3)
addiu   a2, r0, 0x0001
jr      ra
nop

PreventBossAccess:
lui     t2, 0x800D
addiu   t3, r0, 0x0002
addiu   t1, v1, -0x0001
addiu   t6, r0, 0x0006
mult    t0, t6
mflo    t6
addu    t2, t2, t6
addu    t2, t2, t1
sb      t3, 0x6BE0 (t2)
lw      t3, 0x6B90 (at)
addiu   t3, t3, -0x0001
lw      t1, 0x6C70 (at)
li      t2, CrystalRequirements
addu    t2, t2, t3
lb      t3, 0x0000 (t2)
sub     t3, t1, t3
bgez    t3, @@HasCrystals
nop
addiu   t2, v0, 0x0000
beql    t2, t2, @@ReturnToStageClear
nop
@@HasCrystals:
addiu   t2, v0, 0x0001
@@ReturnToStageClear:
li      t1, SlotData
lb      t3, 0x0002 (t1)
blez    t3, @@SkipFast
li      t1, CrystalRequirements
lb      t3, 0x0005 (t1)
lw      t1, 0x6C70 (at)
sub     t3, t1, t3
bltz    t3, @@SkipFast
nop
lw      t3, 0x6C80 (at)
li      t1, 0x01010100
bnel     t1, t3, @@SkipFast
nop
addiu   t3, v0, 0x0064
sw      t3, 0x6C78 (at)
@@SkipFast:
j       0x800B9C50
sw      t2, 0x6B94 (at)

MarkStagesIncomplete:
//; a2 - unlocked level, t3 - save address, t0 free
//; quickly unlock boss if crystal requirement is met
addiu   t0, a2, -0x0001
li      t2, CrystalRequirements
addu    t2, t2, t0
lb      t2, 0x0000 (t2)
lw      t0, 0x0090 (t3)
sub     t0, t0, t2
bltz    t0, @@BeginIncomplete
lw      t2, -0x0050 (t3)
li      t0, LevelStart
addu    t0, t0, t2
lb      t2, 0x0000 (t0)
lw      t0, -0x004C (t3)
sub     t0, t0, t2
bgtz    t0, @@BeginIncomplete
lw      t0, -0x004C (t3)
addiu   t0, t0, 0x0001
sw      t0, -0x004C (t3)
addiu   t2, r0, 0x0058
lw      t0, -0x0058 (t3)
mult    t0, t2
mflo    t2
li      t0, 0x800EC9F8
addu    t2, t2, t0
lw      t0, -0x004C (t3)
sw      t0, 0x0014 (t2)

@@BeginIncomplete:
addiu   s0, r0, 0x0001
addiu   t2, r0, 0x0006
addiu   t0, r0, 0x0000
@@MarkIncomplete:
addiu   t7, r0, 0x0000
addiu   t0, t0, 0x0001
beql    t0, a2, @@MarkIndividualStages
nop
@@MarkLevel:
beq     t7, t2, @@MarkIncomplete
lb      t6, 0x0000 (t3)
addiu   t7, t7, 0x0001
bnez    t6, @@IncrementStage
nop
sb      s0, 0x0000(t3)
@@IncrementStage:
b       @@MarkLevel
addiu   t3, t3, 0x0001
@@MarkIndividualStages:
lui     at, 0x800D
lw      t2, 0x6B94 (at)
@@MarkIndividualStage:
beq     t7, t2, @@Return
lb      t6, 0x0000 (t3)
addiu   t7, t7, 0x0001
bnez   t6, @@IncrementIndividualStage
nop
sb      s0, 0x0000(t3)
@@IncrementIndividualStage:
b       @@MarkIndividualStage
addiu   t3, t3, 0x0001
@@Return:
lw      s1, 0x000C (sp)
lw      s0, 0x0008 (sp)
jr      ra
addiu   sp, sp, 0x10

AllowFinalBoss:
lui     at, 0x800D
lw      s2, 0x6C80 (at)
li      t5, 0x01010100
bne     s2, t5, @@SetFalse
li      s2, 0x0001
@@Set:
sw      s2, 0x6B94 (at)
sw      s2, 0x6C78 (at)
jr      ra
nop
@@SetFalse:
li      s2, 6
sw      s2, 0x6B90 (at)
li      s2, 0x0004
beqz    s2, @@Set

RedirectStage:
lw      t5, 0xE500 (at)
sll     t5, 5
sll     t3, 2
addu    t5, t5, t3
li      t3, LevelIndex
addu    t5, t5, t3
lw      t3, 0x0000 (t5)
lw      t5, 0x00C0 (t5)
sw      t3, 0xE500 (at)
sw      t5, 0xE504 (at)
addiu   t5, r0, 0x000F
jr      ra
sw      t3, 0x0000 (v0)

DeathLink:
lui     at, 0x800D
lw      t0, 0x6C7C (at)
blez    t0, @@CheckCollision
sw      r0, 0x6C7C (at)
jr      ra
addiu   v0, r0, 0x01
@@CheckCollision:
j       0x8010474C
nop

RemapStage:
//; assume level/stage is in a0/a1, add output to t8

sll     t5, a0, 5
sll     t6, a1, 2
addu    t5, t5, t6
li      t6, LevelIndex
addu    t6, t5, t6
lw      t6, 0x0000 (t6)
li      t7, StageIndex
addu    t7, t5, t7
lw      t7, 0x0000 (t7)
sll     t6, t6, 2
addu    t7, t6, t7
addu    t8, t7, t8
j       0x801532A4
nop

SetZeroTwoComplete:
addiu   t3, r0, 0x0001
lui     at, 0x800D
sb      t3, 0x6BC6 (at)
j       0x800A74D8
nop

//; future reference
//; 8004A7C4 is the entity list
//; first entry appears to always be a helper if one is on screen? (hopefully)
//; entities can be linked together
//; ex. cart waddle dee has the cart as the first entity, but is linked to the waddle dee entity that follows
//; for now, we'll hardcode them and make something more scalable later

ScaleGObjNone: //; arg0 - gobj ptr
@@Scale:
lw      t1, 0x0000 (a0)
blez    t1, @@Return
sll     t1, t1, 2
li      at, gEntitiesScaleXArray
addu    at, at, t1
li      t2, 0x00000000
sw      t2, 0x0000 (at)
li      at, gEntitiesScaleYArray
addu    at, at, t1
sw      t2, 0x0000 (at)
li      at, gEntitiesScaleZArray
addu    at, at, t1
sw      t2, 0x0000 (at)
lw      a0, 0x0004 (a0)
bnez     a0, @@Scale
nop
@@Return:
jr      ra
nop

.macro safe_call,func,arg0, ret0
    addiu   sp, sp, -0x10
    sw      ra, 0x10 (sp)
    sw      v0, 0xC (sp)
    sw      v1, 0x8 (sp)
    sw      a0, 0x4 (sp)
    jal     func
    or      a0, arg0, r0
    or      ret0, v0, r0
    lw      a0, 0x4 (sp)
    lw      v1, 0x8 (sp)
    lw      v0, 0xC (sp)
    lw      ra, 0x10 (sp)
    addiu   sp, sp, 0x10
.endmacro

.macro safe_call_2, func, arg0, arg1, ret0
    addiu   sp, sp, -0x14
    sw      ra, 0x14 (sp)
    sw      v0, 0x10 (sp)
    sw      v1, 0xC (sp)
    sw      a1, 0x8 (sp)
    sw      a0, 0x4 (sp)
    or      a1, arg1, r0
    jal     func
    or      a0, arg0, r0
    or      ret0, v0, r0
    lw      a0, 0x4 (sp)
    lw      a1, 0x8 (sp)
    lw      v1, 0xC (sp)
    lw      v0, 0x10 (sp)
    lw      ra, 0x14 (sp)
    addiu   sp, sp, 0x14
.endmacro

.macro scale_gobj,gobj
    addiu   sp, sp, -0x10
    sw      ra, 0x10 (sp)
    sw      t1, 0xC (sp)
    sw      t2, 0x8 (sp)
    sw      a0, 0x4 (sp)
    jal     ScaleGObjNone
    or     a0, gobj, r0
    lw      a0, 0x4 (sp)
    lw      t2, 0x8 (sp)
    lw      t1, 0xC (sp)
    lw      ra, 0x10 (sp)
    addiu   sp, sp, 0x10
.endmacro

BridgeDededeVisual:
lui     t1, 0x800D
lb      t1, 0x6C82 (t1)
bnez    t1, @@SetCorrect
nop
scale_gobj a0
@@SetCorrect:
j       0x8021F0AC
lw      v0, 0xA7C4 (v0)

BridgeDededeOverride: //; t1 replace with 4f
lui     t1, 0x800D
lb      t1, 0x6C82 (t1)
bnez    t1, @@SetCorrect
nop

li      t1, 0x26A
safe_call   PlaySFX,t1, t1
li      t1, 0x0000
beqz    t1, @@Return
nop
@@SetCorrect:
li      t1, 0x004F
@@Return:
sb      t1, 0x000C (a0)
j       0x8021F100
nop

CeilingWaddleDeeOverride: //; t9 safe
BC1FL   @@ReturnFalse
nop
lui     t9, 0x800D
lb      t9, 0x6C80 (t9)
bnez    t9, @@ReturnTrue
nop
li      t9, FriendPlayedSFXFlag
lw      t9, 0x0000 (t9)
bnez    t9, @@ReturnFalse
li      t9, 0x26A
safe_call   PlaySFX, t9, t9
li      t9, 0x0001
li      t6, FriendPlayedSFXFlag
sw      t9, 0x0000 (t6)
b       @@ReturnFalse
nop

@@ReturnTrue:
j       0x8021FF4C
nop

@@ReturnFalse:
j       0x8021FF84
lw      ra, 0x0014 (sp)

CartWaddleDeeOverride: //; t1 safe
lui     t1, 0x800D
lb      t1, 0x6C80 (t1)
bnez    t1, @@Continue
nop
lw      a0, 0x0018 (sp)
scale_gobj a0
li      t1, FriendPlayedSFXFlag
lw      t1, 0x0000 (t1)
bnez    t1, @@Passthrough
li      t1, 0x26A
safe_call PlaySFX, t1, t1
li      a0, 0x0001
li      t1, FriendPlayedSFXFlag
sw      a0, 0x0000 (t1)
@@Passthrough:
j       0x80228450
nop
@@Continue:
jal     0x80122F94
sb      t9, 0x000C (v0)
j       0x80228430

RaftWaddleDeeVisual:

RaftWaddleDeeOverride: //; t6 safe
lui     t6, 0x800D
lb      t6, 0x6C80 (t6)
bnez    t6, @@Continue
nop
li      t6, 0x26A
safe_call PlaySFX, t6, t6
@@Skip:
scale_gobj v1
j       0x80228EE4
nop
@@Continue:
sb      t9, 0x000C (a0)
j       0x80228EE4
nop

SledWaddleDeeOverride: //; t7 safe
lui     t7, 0x800D
lb      t7, 0x6C80 (t7)
bnez    t7, @@Continue
nop
li      t7, 0x26A
safe_call PlaySFX, t7, t7
@@Skip:
j       0x8022857C
nop
@@Continue:
sb      t4, 0x000C (a2)
jal     0x800B1900
lhu     a0, 0x0002 (v0)
j       0x8022857C
nop

WallDededeOverride: //; t9 replace, final 50
lui     t9, 0x800D
lb      t9, 0x6C82 (t9)
bnez    t9, @@SetCorrect
nop
li      t9, 0x26A
safe_call PlaySFX, t9, t9
li      t9, 0x0000
beqz    t9, @@Return
nop
@@SetCorrect:
li      t9, 0x0050
@@Return:
sb      t9, 0x000C (v0)
j       0x80222088
nop

DededeOverride: //; t6 free after first instruction
lhu     v0, 0x0016 (t6)
or      t6, r0, v0
addi    t6, t6, -0x0008
bnez    t6, @@Passthrough
nop
lui     t6, 0x800D
lb      t6, 0x6C82 (t6)
bnez    t6, @@Passthrough
nop
li      t6, FriendPlayedSFXFlag
lw      t6, 0x0000 (t6)
bnez    t6, @@Passthrough
or      v0, r0, r0
li      t6, 0x26A
safe_call PlaySFX,t6, t6
li      t5, 0x0001
li      t6, FriendPlayedSFXFlag
sw      t5, 0x0000 (t6)
@@Passthrough:
jr      ra
nop

MatchAdeleineOverride://; t4-t6 probably safe
//; start by checking v0
beqz    v0, @@ReturnFalse
nop
lui     t4, 0x800D
lb      t4, 0x6C81 (t4)
beqz    t4, @@ReturnFalse
nop
j       0x80220C00
nop
@@ReturnFalse:
li      t6, FriendPlayedSFXFlag
lw      t6, 0x0000 (t6)
bnez    t6, @@Passthrough
li      t6, 0x26A
safe_call PlaySFX,t6, t6
li      t5, 0x0001
li      t6, FriendPlayedSFXFlag
sw      t5, 0x0000 (t6)
@@Passthrough:
j       0x80220BF0
nop

MatchAdeleineVisual://; t8 safe with return set
lui     t8, 0x800D
lb      t8, 0x6C81 (t8)
bnez    t8, @@Return
nop
mtc1    r0, f0
swc1    f0, 0x4554 (at)
swc1    f0, 0x4710 (at)
swc1    f0, 0x48D0 (at)

@@Return:
swc1    f0, 0x4550 (at)
lw      t8, 0x0000 (v1)
j       0x80220AD8
nop

PaintingAdeleineOverride://; t4 safe
lui     t4, 0x800D
lb      t4, 0x6C81 (t4)
beqz    t4, @@ReturnFalse
nop
j       0x80221318
nop
@@ReturnFalse:
li      t4, 0x26A
safe_call PlaySFX, t4, t4
j       0x80221308
nop

PaintingAdeleineVisual1://; t7 safe with return set
lui     t7, 0x800D
lb      t7, 0x6C81 (t7)
bnez    t7, @@Return
nop
mtc1    r0, f0

@@Return:
swc1    f0, 0x4550 (at)
lw      t7, 0x0000 (v1)
j       0x8022105C
nop

PaintingAdeleineVisual2://; all safe after start
lui     t3, 0x800D
lb      t3, 0x6C81 (t3)
bnez    t3, @@Return
nop
mtc1    r0, f0

@@Return:
swc1    f0, 0x4550 (at)
lw      t3, 0x0000 (v0)
j       0x80221604
nop

PaintingAdeleinePaintVisual://; all safe after start
lui     t6, 0x800D
lb      t6, 0x6C81 (t6)
bnez    t6, @@Continue
nop
scale_gobj a0

@@Continue:
lui     t6, 0x8005
j       0x80220F50
lw      t6, 0xA7C4 (t6)

AdeleineOverride://; t9 safe
bne     t8, r0, @@Passthrough
lui     t9, 0x800D
lb      t9, 0x6C81 (t9)
beqz    t9, @@ReturnFalse
nop
j       0x8021F644
nop
@@ReturnFalse:

li      t9, FriendPlayedSFXFlag
lw      t9, 0x0000 (t9)
bnez    t9, @@Passthrough
li      t9, 0x26A
safe_call PlaySFX,t9, t9
scale_gobj a0
li      t8, 0x0001
li      t9, FriendPlayedSFXFlag
sw      t8, 0x0000 (t9)
@@Passthrough:
j       0x8021F6C8
nop

FriendCheck: //; friend in a0, kirby is friend 0, return 1 in v0 for true else 0
//; kirby - 0
//; dedede - 1
//; waddle - 2
//; adeleine - 3
beqz    a0, @@ReturnTrue
li      t1, 1
beq     a0, t1, @@SetDedede
nop
addiu   a0, a0, -1
b       @@WriteProper
nop
@@SetDedede:
li      a0, 3

@@WriteProper:
lui     t1, 0x800D
addu    t1, t1, a0
lb      t1, 0x6C7F (t1)
bnez    t1, @@ReturnTrue

li      v0, 0
b       @@Return
nop

@@ReturnTrue:
li      v0, 1
@@Return:
jr      ra
nop


ConsumableBase://; assumptions: the gobj is at 0x20 from the current sp
li      t7, SlotData
lb      t7, 0x0003 (t7)
beqz    t7, @@ReturnEarly
lw      t5, 0x0000 (a0) //; gobj id
addiu   sp, sp, -0x08
lui     t8, 0x800E
addu    t8, t8, t5
lb      t8, 0x7730 (t8)
li      t7, 0x0003
bne     t8, t7, @@ReturnWithStack
lui     t8, 0x800E
addu    t8, t8, t5
addu    t8, t8, t5
lhu     t8, 0x77A0 (t8)
li      t7, 0x0005
beq     t8, t7, @@ReturnWithStack //; filter out invin candy
nop
li      t7, SlotData
lb      t7, 0x0003 (t7)
andi    t6, t7, 0x0001
beqz    t6, @@OneUp
nop
li      t6, 0x0005
blt     t8, t6, @@Apply
nop
@@OneUp:
andi    t6, t7, 0x0002
beqz    t6, @@Stars
nop
li      t6, 0x0009
beq     t8, t6, @@Apply
nop
@@Stars:
andi    t6, t7, 0x0004
beqz    t6, @@ReturnWithStack
nop
li      t6, 0x0006
beq     t8, t6, @@Apply
nop
li      t7, 0x0007
beq     t8, t6, @@Apply
nop
b       @@ReturnWithStack
nop

@@Apply:
lui     t7, 0x800E
addu    t7, t7, t5
lb      t5, 0x76C0 (t7)
li      t7, 0x0001
dsllv   t7, t7, t5
sd      t7, 0x0000 (sp)
lui     t5, 0x800C
lw      t7, 0xE500 (t5)
lw      t4, 0xE508 (t5)
lw      t5, 0xE504 (t5)
sll     t7, t7, 9
sll     t5, t5, 7
sll     t4, t4, 4
addu    t5, t5, t7
addu    t5, t5, t4
li      t6, 0x80500000
addu    t6, t5, t6
ld      t7, 0x0000 (sp)
ld      t5, 0x0000 (t6)
or      t7, t7, t5
sd      t7, 0x0000 (t6)
li      v0, 1
b       @@Return
@@ReturnWithStack:
addiu   sp, sp, 0x08
@@ReturnEarly:
li      v0, 0
@@Return:
jr      ra
nop

ConsumableCollide:
sw      t8, 0x001C (sp)
lw      v0, 0x0088 (t8)
safe_call ConsumableBase, a0, t5
beqz    t5, @@ReturnNormal
nop
j       0x801BD73C
nop
@@ReturnNormal:
j       0x801BD540
nop

ConsumableInhale:
lui     t1, 0x8005
lw      t1, 0xA7C4 (t1)
safe_call ConsumableBase, t1, t1
bnez    t1, @@ReturnQuick
nop
@@ReturnNormal:
jal     0x801A94D8
nop

@@ReturnQuick:
j       0x801A93B4
nop


.org 0x8011E1BC //; write our jump
jal     CopyAbilityBlocker

.org 0x80121354
jal     DeathLink

.headersize 0x80151100 - 0xB1B40 //; ovl3


.headersize 0x80151100 - 0xF8630 //; ovl4

.org 0x80152134
nop  //; always skip check, assume all friends init

.org 0x801521B4
j       FriendCheck
nop

.org 0x8015329C
j       RemapStage
lui     t8, 0x800D

//; Give access to Dark Star only when flag is set
.org 0x80158760
b       0x80158770

.org 0x80158770
addiu   t6, r0, 0x0001 //; force 1 for miracle matter check

.org 0x80158788
nop
nop
nop
nop                     //; remove percentage check
lui     t6, 0x800D
lw      t7, 0x6B90 (t6)
lw      v0, 0x6C78 (t6) //; read from save area for cutscene check
addiu   a0, r0, 0x000D
bnez    v0, 0x801587BC

.headersize 0x80198880 - 0x13E8F0 //; ovl7

.org 0x801A93AC
j   ConsumableInhale
nop


.org 0x801BD538
j   ConsumableCollide
nop


.headersize 0x801D0C60 - 0x174740 //; ovl8

.org 0x801D2C60
b       0x801D2CD4 //; always spawn a crystal shard for friend miniboss

.headersize 0x8021DF20 - 0x23E630 //; ovl19

.org 0x8021F0A4
j       BridgeDededeVisual
lui     v0, 0x8005

.org 0x8021F0F8
j       BridgeDededeOverride
//; don't care about nop here

.org 0x8021F640
j       AdeleineOverride

.org 0x8021FF44
j       CeilingWaddleDeeOverride
nop
//; don't care about nop here, just keep what's there

.org 0x80220BE8
j       MatchAdeleineOverride
//; already followed by nop

.org 0x80220AD0
j       MatchAdeleineVisual
nop

.org 0x80220F48
j       PaintingAdeleinePaintVisual
nop

.org 0x80221054
j       PaintingAdeleineVisual1
nop

.org 0x802215FC
j       PaintingAdeleineVisual2
nop

.org 0x802212F8
j       PaintingAdeleineOverride
//; already followed by nop

.org 0x80222080
j       WallDededeOverride
sb      v1, 0x0017 (v0)

.org 0x80228428
j       CartWaddleDeeOverride
nop

.org 0x80228D70
j       RaftWaddleDeeOverride
nop

.org 0x80228570
j       SledWaddleDeeOverride
nop
FriendPlayedSFXFlag: //; this is sketchy as hell, but we need it loaded in this ovl
//; since this ovl gets refreshed on level load
.dw 0

.notice "Crystal Requirements: " + orga(CrystalRequirements)
.notice "Slot Data: " + orga(SlotData)
.notice "Level Index: " + orga(LevelIndex)
.notice "Stage Index: " + orga(StageIndex) 

.close