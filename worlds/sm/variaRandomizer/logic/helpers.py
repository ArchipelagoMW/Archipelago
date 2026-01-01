
import math

from ..logic.cache import Cache
from ..logic.smbool import SMBool, smboolFalse
from ..utils.parameters import Settings, easy, medium, diff2text
from ..rom.rom_patches import RomPatches
from ..utils.utils import normalizeRounding


class Helpers(object):
    def __init__(self, smbm):
        self.smbm = smbm

    # return bool
    def haveItemCount(self, item, count):
        return self.smbm.itemCount(item) >= count

    # return integer
    @Cache.decorator
    def energyReserveCount(self):
        return self.smbm.itemCount('ETank') + self.smbm.itemCount('Reserve')

    def energyReserveCountOkDiff(self, difficulties, mult=1.0):
        if difficulties is None or len(difficulties) == 0:
            return smboolFalse

        def f(difficulty):
            return self.smbm.energyReserveCountOk(normalizeRounding(difficulty[0] / mult), difficulty=difficulty[1])

        result = f(difficulties[0])
        for difficulty in difficulties[1:]:
            result = self.smbm.wor(result, f(difficulty))
        return result

    def energyReserveCountOkHellRun(self, hellRunName, mult=1.0):
        difficulties = Settings.hellRuns[hellRunName]
        result = self.energyReserveCountOkDiff(difficulties, mult)

        if result == True:
            result.knows = [hellRunName+'HellRun']

        return result

    # gives damage reduction factor with the current suits
    # envDmg : if true (default) will return environmental damage reduction
    def getDmgReduction(self, envDmg=True):
        ret = 1.0
        sm = self.smbm
        hasVaria = sm.haveItem('Varia')
        hasGrav = sm.haveItem('Gravity')
        items = []
        if RomPatches.has(sm.player, RomPatches.NoGravityEnvProtection):
            if hasVaria:
                items = ['Varia']
                if envDmg:
                    ret = 4.0
                else:
                    ret = 2.0
            if hasGrav and not envDmg:
                ret = 4.0
                items = ['Gravity']
        elif RomPatches.has(sm.player, RomPatches.ProgressiveSuits):
            if hasVaria:
                items.append('Varia')
                ret *= 2
            if hasGrav:
                items.append('Gravity')
                ret *= 2
        else:
            if hasVaria:
                ret = 2.0
                items = ['Varia']
            if hasGrav:
                ret = 4.0
                items = ['Gravity']
        return (ret, items)

    # higher values for mult means room is that much "easier" (HP mult)
    def energyReserveCountOkHardRoom(self, roomName, mult=1.0):
        difficulties = Settings.hardRooms[roomName]
        (dmgRed, items) = self.getDmgReduction()
        mult *= dmgRed
        result = self.energyReserveCountOkDiff(difficulties, mult)

        if result == True:
            result.knows = ['HardRoom-'+roomName]
            if dmgRed != 1.0:
                result._items.append(items)
        return result

    @Cache.decorator
    def heatProof(self):
        sm = self.smbm
        return sm.wor(sm.haveItem('Varia'),
                      sm.wand(sm.wnot(RomPatches.has(sm.player, RomPatches.NoGravityEnvProtection)),
                              sm.wnot(RomPatches.has(sm.player, RomPatches.ProgressiveSuits)),
                              sm.haveItem('Gravity')))

    # helper here because we can't define "sublambdas" in locations
    def getPiratesPseudoScrewCoeff(self):
        sm = self.smbm
        ret = 1.0
        if RomPatches.has(sm.player, RomPatches.NerfedCharge).bool == True:
            ret = 4.0
        return ret

    @Cache.decorator
    def canFireChargedShots(self):
        sm = self.smbm
        return sm.wor(sm.haveItem('Charge'), RomPatches.has(sm.player, RomPatches.NerfedCharge))

    # higher values for mult means hell run is that much "easier" (HP mult)
    def canHellRun(self, hellRun, mult=1.0, minE=2):
        sm = self.smbm

        items = []
        isHeatProof = sm.heatProof()
        if isHeatProof == True:
            return isHeatProof
        if sm.wand(RomPatches.has(sm.player, RomPatches.ProgressiveSuits), sm.haveItem('Gravity')).bool == True:
            # half heat protection
            mult *= 2.0
            minE /= 2.0
            items.append('Gravity')
        if self.energyReserveCount() >= minE:
            if hellRun != 'LowerNorfair':
                ret = self.energyReserveCountOkHellRun(hellRun, mult)
                if ret.bool == True:
                    ret._items.append(items)
                return ret
            else:
                tanks = self.energyReserveCount()
                multCF = mult
                if tanks >= 14:
                    multCF *= 2.0
                nCF = int(math.ceil(2/multCF))
                ret = sm.wand(self.energyReserveCountOkHellRun(hellRun, mult),
                              self.canCrystalFlash(nCF))
                if ret.bool == True:
                    if sm.haveItem('Gravity') == True:
                        ret.difficulty *= 0.7
                        ret._items.append('Gravity')
                    elif sm.haveItem('ScrewAttack') == True:
                        ret.difficulty *= 0.7
                        ret._items.append('ScrewAttack')
                #nPB = self.smbm.itemCount('PowerBomb')
                #print("canHellRun LN. tanks=" + str(tanks) + ", nCF=" + str(nCF) + ", nPB=" + str(nPB) + ", mult=" + str(mult) + ", heatProof=" + str(isHeatProof.bool) + ", ret=" + str(ret))
                return ret
        else:
            return smboolFalse

    @Cache.decorator
    def canMockball(self):
        sm = self.smbm
        return sm.wand(sm.haveItem('Morph'),
                       sm.knowsMockball())

    @Cache.decorator
    def canFly(self):
        sm = self.smbm
        return sm.wor(sm.haveItem('SpaceJump'),
                      sm.canInfiniteBombJump())

    @Cache.decorator
    def canSimpleShortCharge(self):
        sm = self.smbm
        return sm.wand(sm.haveItem('SpeedBooster'),
                       sm.wor(sm.knowsSimpleShortCharge(),
                              sm.knowsShortCharge()))

    @Cache.decorator
    def canShortCharge(self):
        sm = self.smbm
        return sm.wand(sm.haveItem('SpeedBooster'), sm.knowsShortCharge())

    @Cache.decorator
    def canUseBombs(self):
        sm = self.smbm
        return sm.wand(sm.haveItem('Morph'), sm.haveItem('Bomb'))

    @Cache.decorator
    def canInfiniteBombJump(self):
        sm = self.smbm
        return sm.wand(sm.haveItem('Morph'), sm.haveItem('Bomb'), sm.knowsInfiniteBombJump())

    @Cache.decorator
    def canInfiniteBombJumpSuitless(self):
        sm = self.smbm
        return sm.wand(sm.haveItem('Morph'), sm.haveItem('Bomb'), sm.knowsInfiniteBombJumpSuitless())

    @Cache.decorator
    def haveMissileOrSuper(self):
        sm = self.smbm
        return sm.wor(sm.haveItem('Missile'), sm.haveItem('Super'))

    @Cache.decorator
    def canOpenRedDoors(self):
        sm = self.smbm
        return sm.wor(sm.wand(sm.wnot(RomPatches.has(sm.player, RomPatches.RedDoorsMissileOnly)),
                              sm.haveMissileOrSuper()),
                      sm.haveItem('Missile'))

    @Cache.decorator
    def canOpenEyeDoors(self):
        sm = self.smbm
        return sm.wor(RomPatches.has(sm.player, RomPatches.NoGadoras),
                      sm.haveMissileOrSuper())

    @Cache.decorator
    def canOpenGreenDoors(self):
        return self.smbm.haveItem('Super')

    @Cache.decorator
    def canGreenGateGlitch(self):
        sm = self.smbm
        return sm.wand(sm.haveItem('Super'),
                       sm.knowsGreenGateGlitch())

    @Cache.decorator
    def canBlueGateGlitch(self):
        sm = self.smbm
        return sm.wand(sm.haveMissileOrSuper(),
                       sm.knowsGreenGateGlitch())
    @Cache.decorator
    def canUsePowerBombs(self):
        sm = self.smbm
        return sm.wand(sm.haveItem('Morph'), sm.haveItem('PowerBomb'))

    canOpenYellowDoors = canUsePowerBombs

    @Cache.decorator
    def canUseSpringBall(self):
        sm = self.smbm
        return sm.wand(sm.haveItem('Morph'),
                       sm.haveItem('SpringBall'))

    @Cache.decorator
    def canSpringBallJump(self):
        sm = self.smbm
        return sm.wand(sm.canUseSpringBall(),
                       sm.knowsSpringBallJump())

    @Cache.decorator
    def canDoubleSpringBallJump(self):
        sm = self.smbm
        return sm.wand(sm.canUseSpringBall(),
                       sm.haveItem('HiJump'),
                       sm.knowsDoubleSpringBallJump())

    @Cache.decorator
    def canSpringBallJumpFromWall(self):
        sm = self.smbm
        return sm.wand(sm.canUseSpringBall(),
                       sm.knowsSpringBallJumpFromWall())

    @Cache.decorator
    def canDestroyBombWalls(self):
        sm = self.smbm
        return sm.wor(sm.wand(sm.haveItem('Morph'),
                              sm.wor(sm.haveItem('Bomb'),
                                     sm.haveItem('PowerBomb'))),
                      sm.haveItem('ScrewAttack'))

    @Cache.decorator
    def canDestroyBombWallsUnderwater(self):
        sm = self.smbm
        return sm.wor(sm.wand(sm.haveItem('Gravity'),
                              sm.canDestroyBombWalls()),
                      sm.wand(sm.haveItem('Morph'),
                              sm.wor(sm.haveItem('Bomb'),
                                     sm.haveItem('PowerBomb'))))

    @Cache.decorator
    def canPassBombPassages(self):
        sm = self.smbm
        return sm.wor(sm.canUseBombs(),
                      sm.canUsePowerBombs())

    @Cache.decorator
    def canMorphJump(self):
        # small hop in morph ball form
        sm = self.smbm
        return sm.wor(sm.canPassBombPassages(), sm.canUseSpringBall())

    def canCrystalFlash(self, n=1):
        sm = self.smbm
        if not RomPatches.has(sm.player, RomPatches.RoundRobinCF).bool:
            ret = sm.wand(sm.canUsePowerBombs(),
                          sm.itemCountOk('Missile', 2*n),
                          sm.itemCountOk('Super', 2*n),
                          sm.itemCountOk('PowerBomb', 2*n+1))
        else:
            # simplified view of actual patch behavior: only count full refills to stick with base CF logic
            nAmmo = 5 * (sm.itemCount('Missile') + sm.itemCount('Super') + sm.itemCount('PowerBomb'))
            ret = sm.wand(sm.canUsePowerBombs(),
                          SMBool(nAmmo >= 30*n))
        if ret:
            ret._items.append("{}-CrystalFlash".format(n))
        return ret

    @Cache.decorator
    def canCrystalFlashClip(self):
        sm = self.smbm
        return sm.wand(sm.canCrystalFlash(),
                       sm.wor(sm.wand(sm.haveItem('Gravity'),
                                      sm.canUseBombs(),
                                      sm.knowsCrystalFlashClip()),
                              sm.wand(sm.knowsSuitlessCrystalFlashClip(),
                                      sm.itemCountOk('PowerBomb', 4))))

    @Cache.decorator
    def canDoLowGauntlet(self):
        sm = self.smbm
        return sm.wand(sm.canShortCharge(),
                       sm.canUsePowerBombs(),
                       sm.itemCountOk('ETank', 1),
                       sm.knowsLowGauntlet())

    @Cache.decorator
    def canUseHyperBeam(self):
        sm = self.smbm
        return sm.haveItem('Hyper')

    @Cache.decorator
    def getBeamDamage(self):
        sm = self.smbm
        standardDamage = 20

        if sm.wand(sm.haveItem('Ice'),
                   sm.haveItem('Wave'),
                   sm.haveItem('Plasma')) == True:
            standardDamage = 300
        elif sm.wand(sm.haveItem('Wave'),
                     sm.haveItem('Plasma')) == True:
            standardDamage = 250
        elif sm.wand(sm.haveItem('Ice'),
                     sm.haveItem('Plasma')) == True:
            standardDamage = 200
        elif sm.haveItem('Plasma') == True:
            standardDamage = 150
        elif sm.wand(sm.haveItem('Ice'),
                     sm.haveItem('Wave'),
                     sm.haveItem('Spazer')) == True:
            standardDamage = 100
        elif sm.wand(sm.haveItem('Wave'),
                     sm.haveItem('Spazer')) == True:
            standardDamage = 70
        elif sm.wand(sm.haveItem('Ice'),
                     sm.haveItem('Spazer')) == True:
            standardDamage = 60
        elif sm.wand(sm.haveItem('Ice'),
                     sm.haveItem('Wave')) == True:
            standardDamage = 60
        elif sm.haveItem('Wave') == True:
            standardDamage = 50
        elif sm.haveItem('Spazer') == True:
            standardDamage = 40
        elif sm.haveItem('Ice') == True:
            standardDamage = 30

        return standardDamage

    # returns a tuple with :
    #
    # - a floating point number : 0 if boss is unbeatable with
    # current equipment, and an ammo "margin" (ex : 1.5 means we have 50%
    # more firepower than absolutely necessary). Useful to compute boss
    # difficulty when not having charge. If player has charge, the actual
    # value is not useful, and is guaranteed to be > 2.
    #
    # - estimation of the fight duration in seconds (well not really, it
    # is if you fire and land shots perfectly and constantly), giving info
    # to compute boss fight difficulty
    def canInflictEnoughDamages(self, bossEnergy, doubleSuper=False, charge=True, power=False, givesDrops=True, ignoreMissiles=False, ignoreSupers=False, missilesOffset=0, supersOffset=0, powerBombsOffset=0):
        # TODO: handle special beam attacks ? (http://deanyd.net/sm/index.php?title=Charge_Beam_Combos)
        sm = self.smbm
        items = []

        # http://deanyd.net/sm/index.php?title=Damage
        standardDamage = 0
        if sm.canFireChargedShots().bool == True and charge == True:
            standardDamage = self.getBeamDamage()
            items.append('Charge')
        # charge triples the damage
        chargeDamage = standardDamage
        if sm.haveItem('Charge').bool == True:
            chargeDamage *= 3.0

        # missile 100 damages, super missile 300 damages, PBs 200 dmg, 5 in each extension
        missilesAmount = max(0, (sm.itemCount('Missile') - missilesOffset)) * 5
        if ignoreMissiles == True:
            missilesDamage = 0
        else:
            missilesDamage = missilesAmount * 100
            if missilesAmount > 0:
                items.append('Missile')
        supersAmount = max(0, (sm.itemCount('Super') - supersOffset)) * 5
        if ignoreSupers == True:
            oneSuper = 0
        else:
            oneSuper = 300.0
            if supersAmount > 0:
                items.append('Super')
        if doubleSuper == True:
            oneSuper *= 2
        supersDamage = supersAmount * oneSuper
        powerDamage = 0
        powerAmount = 0
        if power == True and sm.haveItem('PowerBomb') == True:
            powerAmount = max(0, (sm.itemCount('PowerBomb') - powerBombsOffset)) * 5
            powerDamage = powerAmount * 200
            items.append('PowerBomb')

        canBeatBoss = chargeDamage > 0 or givesDrops or (missilesDamage + supersDamage + powerDamage) >= bossEnergy
        if not canBeatBoss:
            return (0, 0, [])

        ammoMargin = (missilesDamage + supersDamage + powerDamage) / bossEnergy
        if chargeDamage > 0:
            ammoMargin += 2

        missilesDPS = Settings.algoSettings['missilesPerSecond'] * 100.0
        supersDPS = Settings.algoSettings['supersPerSecond'] * 300.0
        if doubleSuper == True:
            supersDPS *= 2
        if powerDamage > 0:
            powerDPS = Settings.algoSettings['powerBombsPerSecond'] * 200.0
        else:
            powerDPS = 0.0
        chargeDPS = chargeDamage * Settings.algoSettings['chargedShotsPerSecond']
        # print("chargeDPS=" + str(chargeDPS))
        dpsDict = {
            missilesDPS: (missilesAmount, 100.0),
            supersDPS: (supersAmount, oneSuper),
            powerDPS: (powerAmount, 200.0),
            # no boss will take more 10000 charged shots
            chargeDPS: (10000, chargeDamage)
        }
        secs = 0
        for dps in sorted(dpsDict, reverse=True):
            amount = dpsDict[dps][0]
            one = dpsDict[dps][1]
            if dps == 0 or one == 0 or amount == 0:
                continue
            fire = min(bossEnergy / one, amount)
            secs += fire * (one / dps)
            bossEnergy -= fire * one
            if bossEnergy <= 0:
                break
        if bossEnergy > 0:
            # print ('!! drops !! ')
            secs += bossEnergy * Settings.algoSettings['missileDropsPerMinute'] * 100 / 60
            # print('ammoMargin = ' + str(ammoMargin) + ', secs = ' + str(secs))

        return (ammoMargin, secs, items)

    # return diff score, or -1 if below minimum energy in diffTbl
    def computeBossDifficulty(self, ammoMargin, secs, diffTbl, energyDiff=0):
        sm = self.smbm

        # actual fight duration :
        rate = None
        if 'Rate' in diffTbl:
            rate = float(diffTbl['Rate'])
        if rate is None:
            duration = 120.0
        else:
            duration = secs / rate
 #       print('rate=' + str(rate) + ', duration=' + str(duration))
        (suitsCoeff, items) = sm.getDmgReduction(envDmg=False)
        suitsCoeff /= 2.0
        energyCount = self.energyReserveCount()
        energy = suitsCoeff * (1 + energyCount + energyDiff)
#        print("energy="+str(energy)+", energyCount="+str(energyCount)+",energyDiff="+str(energyDiff)+",suitsCoeff="+str(suitsCoeff))

        # add all energy in used items
        items += sm.energyReserveCountOk(energyCount).items

        energyDict = None
        if 'Energy' in diffTbl:
            energyDict = diffTbl['Energy']
        difficulty = medium
        # get difficulty by energy
        if energyDict:
            energyDict = {float(k):float(v) for k,v in energyDict.items()}
            keyz = sorted(energyDict.keys())
            if len(keyz) > 0:
                current = keyz[0]
                if energy < current:
                    return (-1, [])
                sup = None
                difficulty = energyDict[current]
                for k in keyz:
                    if k > energy:
                        sup=k
                        break
                    current = k
                    difficulty = energyDict[k]
                # interpolate if we can
                if energy > current and sup is not None:
                    difficulty += (energyDict[sup] - difficulty)/(sup - current) * (energy - current)
 #       print("energy=" + str(energy) + ", base diff=" + str(difficulty))
        # adjust by fight duration
        difficulty *= (duration / 120)
        # and by ammo margin
        # only augment difficulty in case of no charge, don't lower it.
        # if we have charge, ammoMargin will have a huge value (see canInflictEnoughDamages),
        # so this does not apply
        diffAdjust = (1 - (ammoMargin - Settings.algoSettings['ammoMarginIfNoCharge']))
        if diffAdjust > 1:
            difficulty *= diffAdjust
#        print("final diff: "+str(round(difficulty, 2)))

        return (round(difficulty, 2), items)

    @Cache.decorator
    def enoughStuffSporeSpawn(self):
        sm = self.smbm
        return sm.wor(sm.haveItem('Missile'), sm.haveItem('Super'), sm.haveItem('Charge'))

    @Cache.decorator
    def enoughStuffCroc(self):
        sm = self.smbm
        # say croc has ~5000 energy, and ignore its useless drops
        (ammoMargin, secs, items) = self.canInflictEnoughDamages(5000, givesDrops=False)
        if ammoMargin == 0:
            return sm.wand(sm.knowsLowAmmoCroc(),
                           sm.wor(sm.itemCountOk("Missile", 2),
                                  sm.wand(sm.haveItem('Missile'),
                                          sm.haveItem('Super'))))
        else:
            return SMBool(True, easy, items=items)

    @Cache.decorator
    def enoughStuffBotwoon(self):
        sm = self.smbm
        (ammoMargin, secs, items) = self.canInflictEnoughDamages(6000, givesDrops=False)
        diff = SMBool(True, easy, [], items)
        lowStuff = sm.knowsLowStuffBotwoon()
        if ammoMargin == 0 and lowStuff.bool:
            (ammoMargin, secs, items) = self.canInflictEnoughDamages(3500, givesDrops=False)
            diff = SMBool(lowStuff.bool, lowStuff.difficulty, lowStuff.knows, items)
        if ammoMargin == 0:
            return smboolFalse
        fight = sm.wor(sm.energyReserveCountOk(math.ceil(4/sm.getDmgReduction(envDmg=False)[0])),
                       lowStuff)
        return sm.wandmax(fight, diff)

    @Cache.decorator
    def enoughStuffGT(self):
        sm = self.smbm
        hasBeams = sm.wand(sm.haveItem('Charge'), sm.haveItem('Plasma')).bool
        (ammoMargin, secs, items) = self.canInflictEnoughDamages(9000, ignoreMissiles=True, givesDrops=hasBeams)
        diff = SMBool(True, easy, [], items)
        lowStuff = sm.knowsLowStuffGT()
        if ammoMargin == 0 and lowStuff.bool:
            (ammoMargin, secs, items) = self.canInflictEnoughDamages(3000, ignoreMissiles=True)
            diff = SMBool(lowStuff.bool, lowStuff.difficulty, lowStuff.knows, items)
        if ammoMargin == 0:
            return smboolFalse
        fight = sm.wor(sm.energyReserveCountOk(math.ceil(8/sm.getDmgReduction(envDmg=False)[0])),
                       lowStuff)
        return sm.wandmax(fight, diff)

    @Cache.decorator
    def enoughStuffsRidley(self):
        sm = self.smbm
        if not sm.haveItem('Morph') and not sm.haveItem('ScrewAttack'):
            return smboolFalse
        (ammoMargin, secs, ammoItems) = self.canInflictEnoughDamages(18000, doubleSuper=True, power=True, givesDrops=False)
        if ammoMargin == 0:
            return smboolFalse

        # print('RIDLEY', ammoMargin, secs)
        (diff, defenseItems) = self.computeBossDifficulty(ammoMargin, secs,
                                                          Settings.bossesDifficulty['Ridley'])
        if (sm.onlyBossLeft):
            diff = 1
        if diff < 0:
            return smboolFalse
        else:
            return SMBool(True, diff, items=ammoItems+defenseItems)

    @Cache.decorator
    def enoughStuffsKraid(self):
        sm = self.smbm
        (ammoMargin, secs, ammoItems) = self.canInflictEnoughDamages(1000)
        if ammoMargin == 0:
            return smboolFalse
        #print('KRAID True ', ammoMargin, secs)
        (diff, defenseItems) = self.computeBossDifficulty(ammoMargin, secs,
                                                          Settings.bossesDifficulty['Kraid'])
        if (sm.onlyBossLeft):
            diff = 1
        if diff < 0:
            return smboolFalse

        return SMBool(True, diff, items=ammoItems+defenseItems)

    def adjustHealthDropDiff(self, difficulty):
        (dmgRed, items) = self.getDmgReduction(envDmg=False)
        # 2 is Varia suit, considered standard eqt for boss fights
        # there's certainly a smarter way to do this but...
        if dmgRed < 2:
            difficulty *= Settings.algoSettings['dmgReductionDifficultyFactor']
        elif dmgRed > 2:
            difficulty /= Settings.algoSettings['dmgReductionDifficultyFactor']
        return difficulty

    @Cache.decorator
    def enoughStuffsDraygon(self):
        sm = self.smbm
        if not sm.haveItem('Morph') and not sm.haveItem('Gravity'):
            return smboolFalse
        # some ammo to destroy the turrets during the fight
        if not sm.haveMissileOrSuper():
            return smboolFalse
        (ammoMargin, secs, ammoItems) = self.canInflictEnoughDamages(6000,
                                                                     # underestimate missiles/supers in case a CF exit is needed
                                                                     missilesOffset=2, supersOffset=2)
        # print('DRAY', ammoMargin, secs)
        if ammoMargin > 0:
            (diff, defenseItems) = self.computeBossDifficulty(ammoMargin, secs,
                                                              Settings.bossesDifficulty['Draygon'])
            if diff < 0:
                fight = smboolFalse
            else:
                fight = SMBool(True, diff, items=ammoItems+defenseItems)
            if sm.haveItem('Gravity') == False:
                fight.difficulty *= Settings.algoSettings['draygonNoGravityMalus']
            else:
                fight._items.append('Gravity')
            if not sm.haveItem('Morph'):
                fight.difficulty *= Settings.algoSettings['draygonNoMorphMalus']
            if sm.haveItem('Gravity') and sm.haveItem('ScrewAttack'):
                fight.difficulty /= Settings.algoSettings['draygonScrewBonus']
            fight.difficulty = self.adjustHealthDropDiff(fight.difficulty)
            if (sm.onlyBossLeft):
                fight.difficulty = 1
        else:
            fight = smboolFalse
        # for grapple kill considers energy drained by wall socket + 2 spankings by Dray
        # (original 99 energy used for rounding)
        nTanksGrapple = (240/sm.getDmgReduction(envDmg=True)[0] + 2*160/sm.getDmgReduction(envDmg=False)[0])/100
        return sm.wor(fight,
                      sm.wand(sm.knowsDraygonGrappleKill(),
                              sm.haveItem('Grapple'),
                              sm.energyReserveCountOk(nTanksGrapple)),
                      sm.wand(sm.knowsMicrowaveDraygon(),
                              sm.haveItem('Plasma'),
                              sm.canFireChargedShots(),
                              sm.haveItem('XRayScope')),
                      sm.wand(sm.haveItem('Gravity'),
                              sm.energyReserveCountOk(3),
                              sm.knowsDraygonSparkKill(),
                              sm.haveItem('SpeedBooster')))

    @Cache.decorator
    def enoughStuffsPhantoon(self):
        sm = self.smbm
        (ammoMargin, secs, ammoItems) = self.canInflictEnoughDamages(2500, doubleSuper=True)
        if ammoMargin == 0:
            return smboolFalse
        # print('PHANTOON', ammoMargin, secs)
        (difficulty, defenseItems) = self.computeBossDifficulty(ammoMargin, secs,
                                                                Settings.bossesDifficulty['Phantoon'])
        if difficulty < 0:
            return smboolFalse
        hasCharge = sm.canFireChargedShots()
        hasScrew = sm.haveItem('ScrewAttack')
        if hasScrew:
            difficulty /= Settings.algoSettings['phantoonFlamesAvoidBonusScrew']
            defenseItems += hasScrew.items
        elif hasCharge:
            difficulty /= Settings.algoSettings['phantoonFlamesAvoidBonusCharge']
            defenseItems += hasCharge.items
        elif not hasCharge and sm.itemCount('Missile') <= 2: # few missiles is harder
            difficulty *= Settings.algoSettings['phantoonLowMissileMalus']
        difficulty = self.adjustHealthDropDiff(difficulty)
        if (sm.onlyBossLeft):
            difficulty = 1
        fight = SMBool(True, difficulty, items=ammoItems+defenseItems)

        return sm.wor(fight,
                      sm.wand(sm.knowsMicrowavePhantoon(),
                              sm.haveItem('Plasma'),
                              sm.canFireChargedShots(),
                              sm.haveItem('XRayScope')))

    def mbEtankCheck(self):
        sm = self.smbm
        if sm.wor(RomPatches.has(sm.player, RomPatches.NerfedRainbowBeam), RomPatches.has(sm.player, RomPatches.TourianSpeedup)):
            # "add" energy for difficulty calculations
            energy = 2.8 if sm.haveItem('Varia') else 2.6
            return (True, energy)
        nTanks = sm.energyReserveCount()
        energyDiff = 0
        if sm.haveItem('Varia') == False:
            # "remove" 3 etanks (accounting for rainbow beam damage without varia)
            if nTanks < 6:
                return (False, 0)
            energyDiff = -3
        elif nTanks < 3:
            return (False, 0)
        return (True, energyDiff)

    @Cache.decorator
    def enoughStuffsMotherbrain(self):
        sm = self.smbm
        # MB1 can't be hit by charge beam
        (ammoMargin, secs, _) = self.canInflictEnoughDamages(3000, charge=False, givesDrops=False)
        if ammoMargin == 0:
            return smboolFalse
        # requires 10-10 to break the glass
        if sm.itemCount('Missile') <= 1 or sm.itemCount('Super') <= 1:
            return smboolFalse
        # we actually don't give a shit about MB1 difficulty,
        # since we embark its health in the following calc
        (ammoMargin, secs, ammoItems) = self.canInflictEnoughDamages(18000 + 3000, givesDrops=False)
        if ammoMargin == 0:
            return smboolFalse
        (possible, energyDiff) = self.mbEtankCheck()
        if possible == False:
            return smboolFalse
        # print('MB2', ammoMargin, secs)
        #print("ammoMargin: {}, secs: {}, settings: {}, energyDiff: {}".format(ammoMargin, secs, Settings.bossesDifficulty['MotherBrain'], energyDiff))
        (diff, defenseItems) = self.computeBossDifficulty(ammoMargin, secs, Settings.bossesDifficulty['MotherBrain'], energyDiff)
        if (sm.onlyBossLeft):
            diff = 1
        if diff < 0:
            return smboolFalse
        return SMBool(True, diff, items=ammoItems+defenseItems)

    @Cache.decorator
    def canPassMetroids(self):
        sm = self.smbm
        return sm.wor(sm.wand(sm.haveItem('Ice'), sm.haveMissileOrSuper()),
                      # to avoid leaving tourian to refill power bombs
                      sm.itemCountOk('PowerBomb', 3))

    @Cache.decorator
    def canPassZebetites(self):
        sm = self.smbm
        return sm.wor(sm.wand(sm.haveItem('Ice'), sm.knowsIceZebSkip()),
                      sm.wand(sm.haveItem('SpeedBooster'), sm.knowsSpeedZebSkip()),
                      # account for one zebetite, refill may be necessary
                      SMBool(self.canInflictEnoughDamages(1100, charge=False, givesDrops=False, ignoreSupers=True)[0] >= 1, 0))

    @Cache.decorator
    def enoughStuffTourian(self):
        sm = self.smbm
        ret = self.smbm.wand(sm.wor(RomPatches.has(sm.player, RomPatches.TourianSpeedup),
                                    sm.wand(sm.canPassMetroids(), sm.canPassZebetites())),
                             sm.canOpenRedDoors(),
                             sm.enoughStuffsMotherbrain(),
                             sm.wor(RomPatches.has(sm.player, RomPatches.OpenZebetites), sm.haveItem('Morph')))
        return ret

class Pickup:
    def __init__(self, itemsPickup):
        self.itemsPickup = itemsPickup
        self.endGameLocations = ["Mother Brain", "Gunship"]

    # don't count end game location in the mix as it's now in the available locations
    def enoughMinors(self, smbm, minorLocations):
        if self.itemsPickup in ('all', 'all_strict'):
            return (len(minorLocations) == 0
                    or (len(minorLocations) == 1 and minorLocations[0].Name in self.endGameLocations))
        else:
            return True

    def enoughMajors(self, smbm, majorLocations):
        if self.itemsPickup in ('all', 'all_strict'):
            return (len(majorLocations) == 0
                    or (len(majorLocations) == 1 and majorLocations[0].Name in self.endGameLocations))
        else:
            return True

class Bosses:
    # bosses helpers to know if they are dead
    areaBosses = {
        # classic areas
        'Brinstar': 'Kraid',
        'Norfair': 'Ridley',
        'LowerNorfair': 'Ridley',
        'WreckedShip': 'Phantoon',
        'Maridia': 'Draygon',
        # solver areas
        'Blue Brinstar': 'Kraid',
        'Brinstar Hills': 'Kraid',
        'Bubble Norfair': 'Ridley',
        'Bubble Norfair Bottom': 'Ridley',
        'Bubble Norfair Reserve': 'Ridley',
        'Bubble Norfair Speed': 'Ridley',
        'Bubble Norfair Wave': 'Ridley',
        'Draygon Boss': 'Draygon',
        'Green Brinstar': 'Kraid',
        'Green Brinstar Reserve': 'Kraid',
        'Kraid': 'Kraid',
        'Kraid Boss': 'Kraid',
        'Left Sandpit': 'Draygon',
        'Lower Norfair After Amphitheater': 'Ridley',
        'Lower Norfair Before Amphitheater': 'Ridley',
        'Lower Norfair Screw Attack': 'Ridley',
        'Maridia Forgotten Highway': 'Draygon',
        'Maridia Green': 'Draygon',
        'Maridia Pink Bottom': 'Draygon',
        'Maridia Pink Top': 'Draygon',
        'Maridia Sandpits': 'Draygon',
        'Norfair Entrance': 'Ridley',
        'Norfair Grapple Escape': 'Ridley',
        'Norfair Ice': 'Ridley',
        'Phantoon Boss': 'Phantoon',
        'Pink Brinstar': 'Kraid',
        'Red Brinstar': 'Kraid',
        'Red Brinstar Top': 'Kraid',
        'Ridley Boss': 'Ridley',
        'Right Sandpit': 'Draygon',
        'Warehouse': 'Kraid',
        'WreckedShip': 'Phantoon',
        'WreckedShip Back': 'Phantoon',
        'WreckedShip Bottom': 'Phantoon',
        'WreckedShip Gravity': 'Phantoon',
        'WreckedShip Main': 'Phantoon',
        'WreckedShip Top': 'Phantoon'
    }

    accessPoints = {
        "Kraid": "KraidRoomIn",
        "Phantoon": "PhantoonRoomIn",
        "Draygon": "Draygon Room Bottom",
        "Ridley": "RidleyRoomIn",
        "SporeSpawn": "Big Pink",
        "Crocomire": "Crocomire Room Top",
        "Botwoon": "Aqueduct Bottom",
        "GoldenTorizo": "Screw Attack Bottom"
    }

    @staticmethod
    def Golden4():
        return ['Draygon', 'Kraid', 'Phantoon', 'Ridley']
    
    @staticmethod
    def miniBosses():
        return ['SporeSpawn', 'Crocomire', 'Botwoon', 'GoldenTorizo']

    @staticmethod
    def bossDead(sm, boss):
        return sm.haveItem(boss)

    @staticmethod
    def areaBossDead(sm, area):
        if area not in Bosses.areaBosses:
            return True
        return Bosses.bossDead(sm, Bosses.areaBosses[area])

    @staticmethod
    def allBossesDead(smbm):
        return smbm.wand(Bosses.bossDead(smbm, 'Kraid'),
                         Bosses.bossDead(smbm, 'Phantoon'),
                         Bosses.bossDead(smbm, 'Draygon'),
                         Bosses.bossDead(smbm, 'Ridley'))
    
    @staticmethod
    def allMiniBossesDead(smbm):
        return smbm.wand(Bosses.bossDead(smbm, 'SporeSpawn'),
                         Bosses.bossDead(smbm, 'Botwoon'),
                         Bosses.bossDead(smbm, 'Crocomire'),
                         Bosses.bossDead(smbm, 'GoldenTorizo'))

    @staticmethod
    def xBossesDead(smbm, target):
        count = sum([1 for boss in Bosses.Golden4() if Bosses.bossDead(smbm, boss)])
        return SMBool(count >= target)

    @staticmethod
    def xMiniBossesDead(smbm, target):
        count = sum([1 for miniboss in Bosses.miniBosses() if Bosses.bossDead(smbm, miniboss)])
        return SMBool(count >= target)

def diffValue2txt(diff):
    last = 0
    for d in sorted(diff2text.keys()):
        if diff >= last and diff < d:
            return diff2text[last]
        last = d
    return None
