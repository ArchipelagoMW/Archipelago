import os, random, re
from worlds.sm.variaRandomizer.rando.Items import ItemManager
from worlds.sm.variaRandomizer.rom.ips import IPS_Patch
from worlds.sm.variaRandomizer.utils.doorsmanager import DoorsManager
from worlds.sm.variaRandomizer.graph.graph_utils import GraphUtils, getAccessPoint, locIdsByAreaAddresses
from worlds.sm.variaRandomizer.logic.logic import Logic
from worlds.sm.variaRandomizer.rom.rom import RealROM, snes_to_pc, pc_to_snes
from worlds.sm.variaRandomizer.patches.patchaccess import PatchAccess
from worlds.sm.variaRandomizer.utils.parameters import appDir
from worlds.sm.variaRandomizer.utils import log

def getWord(w):
    return (w & 0x00FF, (w & 0xFF00) >> 8)

class RomPatcher:
    # possible patches. see patches asm source if applicable and available for more information
    IPSPatches = {
        # applied on all seeds
        'Standard': [
            # faster MB cutscene transitions
            'Mother_Brain_Cutscene_Edits',
            # "Balanced" suit mode
            'Removes_Gravity_Suit_heat_protection',
            # door ASM to skip G4 cutscene when all 4 bosses are dead
            'g4_skip.ips',
        ],
        # VARIA tweaks
        'VariaTweaks' : ['WS_Etank', 'LN_Chozo_SpaceJump_Check_Disable', 'ln_chozo_platform.ips', 'bomb_torizo.ips'],
        # anti-softlock/game opening layout patches
        'Layout': ['dachora.ips', 'early_super_bridge.ips', 'high_jump.ips', 'moat.ips', 'spospo_save.ips',
                   'nova_boost_platform.ips', 'red_tower.ips', 'spazer.ips',
                   'brinstar_map_room.ips', 'kraid_save.ips', 'mission_impossible.ips'],
        # comfort patches
        'Optional': ['rando_speed.ips', 'Infinite_Space_Jump', 'refill_before_save.ips',
                     'spinjumprestart.ips', 'elevators_doors_speed.ips', 'No_Music', 'random_music.ips',
                     # animals 
                     'animal_enemies.ips', 'animals.ips', 'draygonimals.ips',
                     'escapimals.ips', 'gameend.ips', 'grey_door_animals.ips',
                     'low_timer.ips', 'metalimals.ips', 'phantoonimals.ips', 'ridleyimals.ips',
                     'Escape_Animals_Change_Event', # ...end animals
                     # vanilla behaviour restore
                     'remove_elevators_doors_speed.ips',
                     'varia_hud.ips'],
        # base patchset+optional layout for area rando
        'Area': ['area_rando_layout.ips', 'door_transition.ips', 'area_rando_doors.ips',
                 'Sponge_Bath_Blinking_Door', 'east_ocean.ips', 'area_rando_warp_door.ips',
                 'crab_shaft.ips', 'Save_Crab_Shaft', 'Save_Main_Street', 'no_demo.ips'],
        # patches for boss rando
        'Bosses': ['door_transition.ips', 'no_demo.ips'],
        # patches for escape rando
        'Escape' : ['rando_escape.ips', 'rando_escape_ws_fix.ips', 'door_transition.ips'],
        # patches for  minimizer with fast Tourian
        'MinimizerTourian': ['minimizer_tourian.ips', 'open_zebetites.ips'],
        # patches for door color rando
        'DoorsColors': ['beam_doors_plms.ips', 'beam_doors_gfx.ips', 'red_doors.ips']
    }

    def __init__(self, romFileName=None, magic=None, plando=False, player=0):
        self.log = log.get('RomPatcher')
        self.romFileName = romFileName
        self.race = None
        self.romFile = RealROM(romFileName)
        #if magic is not None:
        #    from rom.race_mode import RaceModePatcher
        #    self.race = RaceModePatcher(self, magic, plando)
        # IPS_Patch objects list
        self.ipsPatches = []
        # loc name to alternate address. we still write to original
        # address to help the RomReader.
        self.altLocsAddresses = {}
        # specific fixes for area rando connections
        self.roomConnectionSpecific = {
            # fix scrolling sky when transitioning to west ocean
            0x93fe: self.patchWestOcean
        }
        self.doorConnectionSpecific = {
            # get out of kraid room: reload CRE
            0x91ce: self.forceRoomCRE,
            # get out of croc room: reload CRE
            0x93ea: self.forceRoomCRE
        }
        self.patchAccess = PatchAccess()
        self.player = player

    def end(self):
        self.romFile.close()

    def writeItemCode(self, item, visibility, address):
        itemCode = ItemManager.getItemTypeCode(item, visibility)
        if self.race is None:
            self.romFile.writeWord(itemCode, address)
        else:
            self.race.writeItemCode(itemCode, address)

    def getLocAddresses(self, loc):
        ret = [loc.Address]
        if loc.Name in self.altLocsAddresses:
            ret.append(self.altLocsAddresses[loc.Name])
        return ret

    def writeItem(self, itemLoc):
        loc = itemLoc.Location
        if loc.isBoss():
            raise ValueError('Cannot write Boss location')
        #print('write ' + itemLoc.Item.Type + ' at ' + loc.Name)
        for addr in self.getLocAddresses(loc):
            self.writeItemCode(itemLoc.Item, loc.Visibility, addr)

    def writeItemsLocs(self, itemLocs):
        self.nItems = 0
        for itemLoc in itemLocs:
            loc = itemLoc.Location
            item = itemLoc.Item
            if loc.isBoss():
                continue
            self.writeItem(itemLoc)
            if item.Category != 'Nothing':
                self.nItems += 1
                if loc.Name == 'Morphing Ball':
                    self.patchMorphBallEye(item)

    def writeSplitLocs(self, split, itemLocs, progItemLocs):
        majChozoCheck = lambda itemLoc: itemLoc.Item.Class == split and itemLoc.Location.isClass(split)
        fullCheck = lambda itemLoc: itemLoc.Location.Id is not None
        splitChecks = {
            'Full': fullCheck,
            'Scavenger': fullCheck,
            'Major': majChozoCheck,
            'Chozo': majChozoCheck,
            'FullWithHUD': lambda itemLoc: itemLoc.Item.Category not in ['Energy', 'Ammo', 'Boss']
        }
        itemLocCheck = lambda itemLoc: itemLoc.Item.Category != "Nothing" and splitChecks[split](itemLoc)
        for area,addr in locIdsByAreaAddresses.items():
            locs = [il.Location for il in itemLocs if itemLocCheck(il) and il.Location.GraphArea == area]
            self.log.debug("writeSplitLocs. area="+area)
            self.log.debug(str([loc.Name for loc in locs]))
            self.romFile.seek(addr)
            for loc in locs:
                self.romFile.writeByte(loc.Id)
            self.romFile.writeByte(0xff)
        if split == "Scavenger":
            # write required major item order
            self.romFile.seek(snes_to_pc(0xA1F5D8))
            for itemLoc in progItemLocs:
                self.romFile.writeWord((itemLoc.Location.Id << 8) | itemLoc.Location.HUD)
            # bogus loc ID | "HUNT OVER" index
            self.romFile.writeWord(0xff10)

    # trigger morph eye enemy on whatever item we put there,
    # not just morph ball
    def patchMorphBallEye(self, item):
#        print('Eye item = ' + item.Type)
        isAmmo = item.Category == 'Ammo'
        # category to check
        if ItemManager.isBeam(item):
            cat = 0xA8 # collected beams
        elif item.Type == 'ETank':
            cat = 0xC4 # max health
        elif item.Type == 'Reserve':
            cat = 0xD4 # max reserves
        elif item.Type == 'Missile':
            cat = 0xC8 # max missiles
        elif item.Type == 'Super':
            cat = 0xCC # max supers
        elif item.Type == 'PowerBomb':
            cat = 0xD0 # max PBs
        else:
            cat = 0xA4 # collected items
        # comparison/branch instruction
        # the branch is taken if we did NOT collect item yet
        if item.Category == 'Energy' or isAmmo:
            comp = 0xC9 # CMP (immediate)
            branch = 0x30 # BMI
        else:
            comp = 0x89 # BIT (immediate)
            branch = 0xF0 # BEQ
        # what to compare to
        if item.Type == 'ETank':
            operand = 0x65 # < 100
        elif item.Type == 'Reserve' or isAmmo:
            operand = 0x1 # < 1
        elif ItemManager.isBeam(item):
            operand = item.BeamBits
        else:
            operand = item.ItemBits
        self.patchMorphBallCheck(0x1410E6, cat, comp, operand, branch) # eye main AI
        self.patchMorphBallCheck(0x1468B2, cat, comp, operand, branch) # head main AI

    def patchMorphBallCheck(self, offset, cat, comp, operand, branch):
        # actually patch enemy AI
        self.romFile.writeByte(cat, offset)
        self.romFile.writeByte(comp, offset+2)
        self.romFile.writeWord(operand)
        self.romFile.writeByte(branch)

    def writeItemsNumber(self):
        # write total number of actual items for item percentage patch (patch the patch)
        for addr in [0x5E64E, 0x5E6AB]:
            self.romFile.writeByte(self.nItems, addr)

    def addIPSPatches(self, patches):
        for patchName in patches:
            self.applyIPSPatch(patchName)

    def writePlmTable(self, plms, area, bosses, startLocation):
        # called when saving a plando
        try:
            if bosses == True or area == True:
                plms.append('WS_Save_Blinking_Door')

            doors = self.getStartDoors(plms, area, None)
            self.writeDoorsColor(doors, self.player)
            self.applyStartAP(startLocation, plms, doors)

            self.applyPLMs(plms)
        except Exception as e:
            raise Exception("Error patching {}. ({})".format(self.romFileName, e))

    def applyIPSPatches(self, startLocation="Landing Site",
                        optionalPatches=[], noLayout=False, suitsMode="Balanced",
                        area=False, bosses=False, areaLayoutBase=False,
                        noVariaTweaks=False, nerfedCharge=False, nerfedRainbowBeam=False,
                        escapeAttr=None, minimizerN=None, minimizerTourian=True,
                        doorsColorsRando=False):
        try:
            # apply standard patches
            stdPatches = []
            plms = []
            # apply race mode first because it fills the rom with a bunch of crap
            if self.race is not None:
                stdPatches.append('race_mode.ips')
            stdPatches += RomPatcher.IPSPatches['Standard'][:]
            if self.race is not None:
                stdPatches.append('race_mode_credits.ips')
            if suitsMode != "Balanced":
                stdPatches.remove('Removes_Gravity_Suit_heat_protection')
            if suitsMode == "Progressive":
                stdPatches.append('progressive_suits.ips')
            if nerfedCharge == True:
                stdPatches.append('nerfed_charge.ips')
            if nerfedRainbowBeam == True:
                stdPatches.append('nerfed_rainbow_beam.ips')
            if bosses == True or area == True:
                stdPatches += ["WS_Main_Open_Grey", "WS_Save_Active"]
                plms.append('WS_Save_Blinking_Door')
            if bosses == True:
                stdPatches.append("Phantoon_Eye_Door")
            if area == True or doorsColorsRando == True:
                stdPatches.append("Enable_Backup_Saves")
            if 'varia_hud.ips' in optionalPatches:
                # varia hud has its own variant of g4_skip for scavenger mode,
                # it can also make demos glitch out
                stdPatches.remove("g4_skip.ips")
                self.applyIPSPatch("no_demo.ips")
            for patchName in stdPatches:
                self.applyIPSPatch(patchName)

            if noLayout == False:
                # apply layout patches
                for patchName in RomPatcher.IPSPatches['Layout']:
                    self.applyIPSPatch(patchName)
            if noVariaTweaks == False:
                # VARIA tweaks
                for patchName in RomPatcher.IPSPatches['VariaTweaks']:
                    self.applyIPSPatch(patchName)

            # apply optional patches
            for patchName in optionalPatches:
                if patchName in RomPatcher.IPSPatches['Optional']:
                    self.applyIPSPatch(patchName)

            # random escape
            if escapeAttr is not None:
                for patchName in RomPatcher.IPSPatches['Escape']:
                    self.applyIPSPatch(patchName)
                # animals and timer
                self.applyEscapeAttributes(escapeAttr, plms)

            # apply area patches
            if area == True:
                for patchName in RomPatcher.IPSPatches['Area']:
                    if areaLayoutBase == True and patchName in ['area_rando_layout.ips', 'Sponge_Bath_Blinking_Door', 'east_ocean.ips']:
                        continue
                    self.applyIPSPatch(patchName)
                if areaLayoutBase == True:
                    self.applyIPSPatch('area_rando_layout_base.ips')

                
            else:
                self.applyIPSPatch('area_ids_alt.ips')
            if bosses == True:
                for patchName in RomPatcher.IPSPatches['Bosses']:
                    self.applyIPSPatch(patchName)
            if minimizerN is not None:
                self.applyIPSPatch('minimizer_bosses.ips')
                if minimizerTourian == True:
                    for patchName in RomPatcher.IPSPatches['MinimizerTourian']:
                        self.applyIPSPatch(patchName)
            doors = self.getStartDoors(plms, area, minimizerN)
            if doorsColorsRando == True:
                for patchName in RomPatcher.IPSPatches['DoorsColors']:
                    self.applyIPSPatch(patchName)
                self.writeDoorsColor(doors, self.player)
            self.applyStartAP(startLocation, plms, doors)
            self.applyPLMs(plms)
        except Exception as e:
            raise Exception("Error patching {}. ({})".format(self.romFileName, e))

    def applyIPSPatch(self, patchName, patchDict=None, ipsDir=None):
        if patchDict is None:
            patchDict = self.patchAccess.getDictPatches()
        # print("Apply patch {}".format(patchName))
        if patchName in patchDict:
            patch = IPS_Patch(patchDict[patchName])
        else:
            # look for ips file
            if ipsDir is None:
                patch = IPS_Patch.load(self.patchAccess.getPatchPath(patchName))
            else:
                patch = IPS_Patch.load(os.path.join(appDir, ipsDir, patchName))
        self.ipsPatches.append(patch)
    
    def applyIPSPatchDict(self, patchDict):
        for patchName in patchDict.keys():
            # print("Apply patch {}".format(patchName))
            patch = IPS_Patch(patchDict[patchName])
            self.ipsPatches.append(patch)

    def getStartDoors(self, plms, area, minimizerN):
        doors = [0x10] # red brin elevator
        def addBlinking(name):
            key = 'Blinking[{}]'.format(name)
            if key in self.patchAccess.getDictPatches():
                self.applyIPSPatch(key)
            if key in self.patchAccess.getAdditionalPLMs():
                plms.append(key)
        if area == True:
            plms += ['Maridia Sand Hall Seal', "Save_Main_Street", "Save_Crab_Shaft"]
            for accessPoint in Logic.accessPoints:
                if accessPoint.Internal == True or accessPoint.Boss == True:
                    continue
                addBlinking(accessPoint.Name)
            addBlinking("West Sand Hall Left")
            addBlinking("Below Botwoon Energy Tank Right")
        if minimizerN is not None:
            # add blinking doors inside and outside boss rooms
            for accessPoint in Logic.accessPoints:
                if accessPoint.Boss == True:
                    addBlinking(accessPoint.Name)
        return doors

    def applyStartAP(self, apName, plms, doors):
        ap = getAccessPoint(apName)
        # if start loc is not Ceres or Landing Site, or the ceiling loc picked up before morph loc,
        # Zebes will be awake and morph loc item will disappear.
        # this PLM ensures the item will be here whenever zebes awakes
        plms.append('Morph_Zebes_Awake')
        (w0, w1) = getWord(ap.Start['spawn'])
        if 'doors' in ap.Start:
            doors += ap.Start['doors']
        doors.append(0x0)
        addr = 0x10F200
        patch = [w0, w1] + doors
        assert (addr + len(patch)) < 0x10F210, "Stopped before new_game overwrite"
        patchDict = {
            'StartAP': {
                addr: patch
            },
        }
        self.applyIPSPatch('StartAP', patchDict)
        # handle custom saves
        if 'save' in ap.Start:
            self.applyIPSPatch(ap.Start['save'])
            plms.append(ap.Start['save'])
        # handle optional rom patches
        if 'rom_patches' in ap.Start:
            for patch in ap.Start['rom_patches']:
                self.applyIPSPatch(patch)

    def applyEscapeAttributes(self, escapeAttr, plms):
        # timer
        escapeTimer = escapeAttr['Timer']
        if escapeTimer is not None:
            minute = int(escapeTimer / 60)
            second = escapeTimer % 60
            minute = int(minute / 10) * 16 + minute % 10
            second = int(second / 10) * 16 + second % 10
            patchDict = {'Escape_Timer': {0x1E21:[second, minute]}}
            self.applyIPSPatch('Escape_Timer', patchDict)
        # animals door to open
        if escapeAttr['Animals'] is not None:
            escapeOpenPatches = {
                'Green Brinstar Main Shaft Top Left':'Escape_Animals_Open_Brinstar',
                'Business Center Mid Left':"Escape_Animals_Open_Norfair",
                'Crab Hole Bottom Right':"Escape_Animals_Open_Maridia",
            }
            if escapeAttr['Animals'] in escapeOpenPatches:
                plms.append("WS_Map_Grey_Door")
                self.applyIPSPatch(escapeOpenPatches[escapeAttr['Animals']])
            else:
                plms.append("WS_Map_Grey_Door_Openable")
        else:
            plms.append("WS_Map_Grey_Door")
        # optional patches (enemies, scavenger)
        for patch in escapeAttr['patches']:
            self.applyIPSPatch(patch)

    # adds ad-hoc "IPS patches" for additional PLM tables
    def applyPLMs(self, plms):
        # compose a dict (room, state, door) => PLM array
        # 'PLMs' being a 6 byte arrays
        plmDict = {}
        # we might need to update locations addresses on the fly
        plmLocs = {} # room key above => loc name
        additionalPLMs = self.patchAccess.getAdditionalPLMs()
        for p in plms:
            plm = additionalPLMs[p]
            room = plm['room']
            state = 0
            if 'state' in plm:
                state = plm['state']
            door = 0
            if 'door' in plm:
                door = plm['door']
            k = (room, state, door)
            if k not in plmDict:
                plmDict[k] = []
            plmDict[k] += plm['plm_bytes_list']
            if 'locations' in plm:
                locList = plm['locations']
                for locName, locIndex in locList:
                    plmLocs[(k, locIndex)] = locName
        # make two patches out of this dict
        plmTblAddr = 0x7E9A0 # moves downwards
        plmPatchData = []
        roomTblAddr = 0x7EC00 # moves upwards
        roomPatchData = []
        plmTblOffset = plmTblAddr
        def appendPlmBytes(bytez):
            nonlocal plmPatchData, plmTblOffset
            plmPatchData += bytez
            plmTblOffset += len(bytez)
        def addRoomPatchData(bytez):
            nonlocal roomPatchData, roomTblAddr
            roomPatchData = bytez + roomPatchData
            roomTblAddr -= len(bytez)
        for roomKey, plmList in plmDict.items():
            entryAddr = plmTblOffset
            roomData = []
            for i in range(len(plmList)):
                plmBytes = plmList[i]
                assert len(plmBytes) == 6, "Invalid PLM entry for roomKey " + str(roomKey) + ": PLM list len is " + str(len(plmBytes))
                if (roomKey, i) in plmLocs:
                    self.altLocsAddresses[plmLocs[(roomKey, i)]] = plmTblOffset
                appendPlmBytes(plmBytes)
            appendPlmBytes([0x0, 0x0]) # list terminator
            def appendRoomWord(w, data):
                (w0, w1) = getWord(w)
                data += [w0, w1]
            for i in range(3):
                appendRoomWord(roomKey[i], roomData)
            appendRoomWord(entryAddr, roomData)
            addRoomPatchData(roomData)
        # write room table terminator
        addRoomPatchData([0x0] * 8)
        assert plmTblOffset < roomTblAddr, "Spawn PLM table overlap"
        patchDict = {
            "PLM_Spawn_Tables" : {
                plmTblAddr: plmPatchData,
                roomTblAddr: roomPatchData
            }
        }
        self.applyIPSPatch("PLM_Spawn_Tables", patchDict)

    def commitIPS(self):
        self.romFile.ipsPatch(self.ipsPatches)

    def writeSeed(self, seed):
        random.seed(seed)
        seedInfo = random.randint(0, 0xFFFF)
        seedInfo2 = random.randint(0, 0xFFFF)
        self.romFile.writeWord(seedInfo, 0x2FFF00)
        self.romFile.writeWord(seedInfo2)

    def writeMagic(self):
        if self.race is not None:
            self.race.writeMagic()

    def writeMajorsSplit(self, majorsSplit):
        address = 0x17B6C
        splits = {
            'Chozo': 'Z',
            'Major': 'M',
            'FullWithHUD': 'H',
            'Scavenger': 'S'
        }
        char = splits.get(majorsSplit, 'F')
        self.romFile.writeByte(ord(char), address)

    def getItemQty(self, itemLocs, itemType):
        return len([il for il in itemLocs if il.Accessible and il.Item.Type == itemType])

    def getMinorsDistribution(self, itemLocs):
        dist = {}
        minQty = 100
        minors = ['Missile', 'Super', 'PowerBomb']
        for m in minors:
            # in vcr mode if the seed has stuck we may not have these items, return at least 1
            q = float(max(self.getItemQty(itemLocs, m), 1))
            dist[m] = {'Quantity' : q }
            if q < minQty:
                minQty = q
        for m in minors:
            dist[m]['Proportion'] = dist[m]['Quantity']/minQty

        return dist

    def getAmmoPct(self, minorsDist):
        q = 0
        for m,v in minorsDist.items():
            q += v['Quantity']
        return 100*q/66

    def writeRandoSettings(self, settings, itemLocs):
        dist = self.getMinorsDistribution(itemLocs)
        totalAmmo = sum(d['Quantity'] for ammo,d in dist.items())
        totalItemLocs = sum(1 for il in itemLocs if il.Accessible and not il.Location.isBoss())
        totalNothing = sum(1 for il in itemLocs if il.Accessible and il.Item.Category == 'Nothing')
        totalEnergy = self.getItemQty(itemLocs, 'ETank')+self.getItemQty(itemLocs, 'Reserve')
        totalMajors = max(totalItemLocs - totalEnergy - totalAmmo - totalNothing, 0)
        address = 0x2736C0
        value = "{:>2}".format(totalItemLocs)
        line = " ITEM LOCATIONS              %s " % value
        self.writeCreditsStringBig(address, line, top=True)
        address += 0x40

        line = " item locations ............ %s " % value
        self.writeCreditsStringBig(address, line, top=False)
        address += 0x40

        maj = "{:>2}".format(int(totalMajors))
        htanks = "{:>2}".format(int(totalEnergy))
        ammo = "{:>2}".format(int(totalAmmo))
        blank = "{:>2}".format(int(totalNothing))
        line = "  MAJ %s EN %s AMMO %s BLANK %s " % (maj, htanks, ammo, blank)
        self.writeCreditsStringBig(address, line, top=True)
        address += 0x40
        line = "  maj %s en %s ammo %s blank %s " % (maj, htanks, ammo, blank)
        self.writeCreditsStringBig(address, line, top=False)
        address += 0x40

        pbs = "{:>2}".format(int(dist['PowerBomb']['Quantity']))
        miss = "{:>2}".format(int(dist['Missile']['Quantity']))
        supers = "{:>2}".format(int(dist['Super']['Quantity']))
        line = " AMMO PACKS  MI %s SUP %s PB %s " % (miss, supers, pbs)
        self.writeCreditsStringBig(address, line, top=True)
        address += 0x40

        line = " ammo packs  mi %s sup %s pb %s " % (miss, supers, pbs)
        self.writeCreditsStringBig(address, line, top=False)
        address += 0x40

        etanks = "{:>2}".format(int(self.getItemQty(itemLocs, 'ETank')))
        reserves = "{:>2}".format(int(self.getItemQty(itemLocs, 'Reserve')))
        line = " HEALTH TANKS         E %s R %s " % (etanks, reserves)
        self.writeCreditsStringBig(address, line, top=True)
        address += 0x40

        line = " health tanks ......  e %s r %s " % (etanks, reserves)
        self.writeCreditsStringBig(address, line, top=False)
        address += 0x80

        value = " "+"NA" # settings.progSpeed.upper()
        line = " PROGRESSION SPEED ....%s " % value.rjust(8, '.')
        self.writeCreditsString(address, 0x04, line)
        address += 0x40

        line = " PROGRESSION DIFFICULTY %s " % value.rjust(7, '.') # settings.progDiff.upper()
        self.writeCreditsString(address, 0x04, line)
        address += 0x80 # skip item distrib title

        param = (' SUITS RESTRICTION ........%s', 'Suits')
        line = param[0] % ('. ON' if settings.restrictions[param[1]] == True else ' OFF')
        self.writeCreditsString(address, 0x04, line)
        address += 0x40

        value = " "+settings.restrictions['Morph'].upper()
        line  = " MORPH PLACEMENT .....%s" % value.rjust(9, '.')
        self.writeCreditsString(address, 0x04, line)
        address += 0x40

        for superFun in [(' SUPER FUN COMBAT .........%s', 'Combat'),
                         (' SUPER FUN MOVEMENT .......%s', 'Movement'),
                         (' SUPER FUN SUITS ..........%s', 'Suits')]:
            line = superFun[0] % ('. ON' if superFun[1] in settings.superFun else ' OFF')
            self.writeCreditsString(address, 0x04, line)
            address += 0x40

        value = "%.1f %.1f %.1f" % (dist['Missile']['Proportion'], dist['Super']['Proportion'], dist['PowerBomb']['Proportion'])
        line = " AMMO DISTRIBUTION  %s " % value
        self.writeCreditsStringBig(address, line, top=True)
        address += 0x40

        line = " ammo distribution  %s " % value
        self.writeCreditsStringBig(address, line, top=False)
        address += 0x40

        # write ammo/energy pct
        address = 0x273C40
        (ammoPct, energyPct) = (int(self.getAmmoPct(dist)), int(100*totalEnergy/18))
        line = " AVAILABLE AMMO {:>3}% ENERGY {:>3}%".format(ammoPct, energyPct)
        self.writeCreditsStringBig(address, line, top=True)
        address += 0x40
        line = " available ammo {:>3}% energy {:>3}%".format(ammoPct, energyPct)
        self.writeCreditsStringBig(address, line, top=False)

    def writeSpoiler(self, itemLocs, progItemLocs=None):
        # keep only majors
        fItemLocs = [il for il in itemLocs if il.Item.Category not in ['Ammo', 'Nothing', 'Energy', 'Boss']]
        # add location of the first instance of each minor
        for t in ['Missile', 'Super', 'PowerBomb']:
            itLoc = None
            if progItemLocs is not None:
                itLoc = next((il for il in progItemLocs if il.Item.Type == t), None)
            if itLoc is None:
                itLoc = next((il for il in itemLocs if il.Item.Type == t), None)
            if itLoc is not None: # in vcr mode if the seed has stucked we may not have these minors
                fItemLocs.append(itLoc)
        regex = re.compile(r"[^A-Z0-9\.,'!: ]+")

        itemLocs = {}
        for iL in fItemLocs:
            itemLocs[iL.Item.Name] = iL.Location.Name

        def prepareString(s, isItem=True):
            s = s.upper()
            # remove chars not displayable
            s = regex.sub('', s)
            # remove space before and after
            s = s.strip()
            # limit to 30 chars, add one space before
            # pad to 32 chars
            if isItem is True:
                s = " " + s[0:30]
                s = s.ljust(32)
            else:
                s = " " + s[0:30] + " "
                s = " " + s.rjust(31, '.')

            return s

        isRace = self.race is not None
        startCreditAddress = 0x2f5240
        address = startCreditAddress
        if isRace:
            addr = address - 0x40
            data = [0x007f, 0x007f, 0x007f, 0x007f, 0x007f, 0x007f, 0x007f, 0x007f, 0x007f, 0x1008, 0x1013, 0x1004, 0x100c, 0x007f, 0x100b, 0x100e, 0x1002, 0x1000, 0x1013, 0x1008, 0x100e, 0x100d, 0x1012, 0x007f, 0x007f, 0x007f, 0x007f, 0x007f, 0x007f, 0x007f, 0x007f, 0x007f]
            for i in range(0x20):
                w = data[i]
                self.romFile.seek(addr)
                self.race.writeWordMagic(w)
                addr += 0x2
        # standard item order
        items = ["Missile", "Super Missile", "Power Bomb",
                 "Charge Beam", "Ice Beam", "Wave Beam", "Spazer", "Plasma Beam",
                 "Varia Suit", "Gravity Suit",
                 "Morph Ball", "Bomb", "Spring Ball", "Screw Attack",
                 "Hi-Jump Boots", "Space Jump", "Speed Booster",
                 "Grappling Beam", "X-Ray Scope"]
        displayNames = {}
        if progItemLocs is not None:
            # reorder it with progression indices
            prog = ord('A')
            idx = 0
            progNames = [il.Item.Name for il in progItemLocs if il.Item.Category != 'Boss']
            for i in range(len(progNames)):
                item = progNames[i]
                if item in items and item not in displayNames:
                    items.remove(item)
                    items.insert(idx, item)
                    displayNames[item] = chr(prog + i) + ": " + item
                    idx += 1
        for item in items:
            # super fun removes items
            if item not in itemLocs:
                continue
            display = item
            if item in displayNames:
                display = displayNames[item]
            itemName = prepareString(display)
            locationName = prepareString(itemLocs[item], isItem=False)

            self.writeCreditsString(address, 0x04, itemName, isRace)
            self.writeCreditsString((address + 0x40), 0x18, locationName, isRace)

            address += 0x80

        # we need 19 items displayed, if we've removed majors, add some blank text
        while address < startCreditAddress + len(items)*0x80:
            self.writeCreditsString(address, 0x04, prepareString(""), isRace)
            self.writeCreditsString((address + 0x40), 0x18, prepareString(""), isRace)

            address += 0x80

        self.patchBytes(address, [0, 0, 0, 0], isRace)

    def writeCreditsString(self, address, color, string, isRace=False):
        array = [self.convertCreditsChar(color, char) for char in string]
        self.patchBytes(address, array, isRace)

    def writeCreditsStringBig(self, address, string, top=True):
        array = [self.convertCreditsCharBig(char, top) for char in string]
        self.patchBytes(address, array)

    def convertCreditsChar(self, color, byte):
        if byte == ' ':
            ib = 0x7f
        elif byte == '!':
            ib = 0x1F
        elif byte == ':':
            ib = 0x1E
        elif byte == '\\':
            ib = 0x1D
        elif byte == '_':
            ib = 0x1C
        elif byte == ',':
            ib = 0x1B
        elif byte == '.':
            ib = 0x1A
        else:
            ib = ord(byte) - 0x41

        if ib == 0x7F:
            return 0x007F
        else:
            return (color << 8) + ib

    def convertCreditsCharBig(self, byte, top=True):
        # from: https://jathys.zophar.net/supermetroid/kejardon/TextFormat.txt
        # 2-tile high characters:
        # A-P = $XX20-$XX2F(TOP) and $XX30-$XX3F(BOTTOM)
        # Q-Z = $XX40-$XX49(TOP) and $XX50-$XX59(BOTTOM)
        # ' = $XX4A, $XX7F
        # " = $XX4B, $XX7F
        # . = $XX7F, $XX5A
        # 0-9 = $XX60-$XX69(TOP) and $XX70-$XX79(BOTTOM)
        # % = $XX6A, $XX7A

        if byte == ' ':
            ib = 0x7F
        elif byte == "'":
            if top == True:
                ib = 0x4A
            else:
                ib = 0x7F
        elif byte == '"':
            if top == True:
                ib = 0x4B
            else:
                ib = 0x7F
        elif byte == '.':
            if top == True:
                ib = 0x7F
            else:
                ib = 0x5A
        elif byte == '%':
            if top == True:
                ib = 0x6A
            else:
                ib = 0x7A

        byte = ord(byte)
        if byte >= ord('A') and byte <= ord('P'):
            ib = byte - 0x21
        elif byte >= ord('Q') and byte <= ord('Z'):
            ib = byte - 0x11
        elif byte >= ord('a') and byte <= ord('p'):
            ib = byte - 0x31
        elif byte >= ord('q') and byte <= ord('z'):
            ib = byte - 0x21
        elif byte >= ord('0') and byte <= ord('9'):
            if top == True:
                ib = byte + 0x30
            else:
                ib = byte + 0x40

        return ib

    def patchBytes(self, address, array, isRace=False):
        self.romFile.seek(address)
        for w in array:
            if not isRace:
                self.romFile.writeWord(w)
            else:
                self.race.writeWordMagic(w)

    # write area randomizer transitions to ROM
    # doorConnections : a list of connections. each connection is a dictionary describing
    # - where to write in the ROM :
    # DoorPtr : door pointer to write to
    # - what to write in the ROM :
    # RoomPtr, direction, bitflag, cap, screen, distanceToSpawn : door properties
    # * if SamusX and SamusY are defined in the dict, custom ASM has to be written
    #   to reposition samus, and call doorAsmPtr if non-zero. The written Door ASM
    #   property shall point to this custom ASM.
    # * if not, just write doorAsmPtr as the door property directly.
    def writeDoorConnections(self, doorConnections):
        asmAddress = 0x7F800
        for conn in doorConnections:
            # write door ASM for transition doors (code and pointers)
#            print('Writing door connection ' + conn['ID'])
            doorPtr = conn['DoorPtr']
            roomPtr = conn['RoomPtr']
            if doorPtr in self.doorConnectionSpecific:
                self.doorConnectionSpecific[doorPtr](roomPtr)
            if roomPtr in self.roomConnectionSpecific:
                self.roomConnectionSpecific[roomPtr](doorPtr)
            self.romFile.seek(0x10000 + doorPtr)

            # write room ptr
            self.romFile.writeWord(roomPtr & 0xFFFF)

            # write bitflag (if area switch we have to set bit 0x40, and remove it if same area)
            self.romFile.writeByte(conn['bitFlag'])

            # write direction
            self.romFile.writeByte(conn['direction'])

            # write door cap x
            self.romFile.writeByte(conn['cap'][0])

            # write door cap y
            self.romFile.writeByte(conn['cap'][1])

            # write screen x
            self.romFile.writeByte(conn['screen'][0])

            # write screen y
            self.romFile.writeByte(conn['screen'][1])

            # write distance to spawn
            self.romFile.writeWord(conn['distanceToSpawn'] & 0xFFFF)

            # write door asm
            asmPatch = []
            # call original door asm ptr if needed
            if conn['doorAsmPtr'] != 0x0000:
                # endian convert
                (D0, D1) = (conn['doorAsmPtr'] & 0x00FF, (conn['doorAsmPtr'] & 0xFF00) >> 8)
                asmPatch += [ 0x20, D0, D1 ]        # JSR $doorAsmPtr
            # special ASM hook point for VARIA needs when taking the door (used for animals)
            if 'exitAsmPtr' in conn:
                # endian convert
                (D0, D1) = (conn['exitAsmPtr'] & 0x00FF, (conn['exitAsmPtr'] & 0xFF00) >> 8)
                asmPatch += [ 0x20, D0, D1 ]        # JSR $exitAsmPtr
            # incompatible transition
            if 'SamusX' in conn:
                # endian convert
                (X0, X1) = (conn['SamusX'] & 0x00FF, (conn['SamusX'] & 0xFF00) >> 8)
                (Y0, Y1) = (conn['SamusY'] & 0x00FF, (conn['SamusY'] & 0xFF00) >> 8)
                # force samus position
                # see door_transition.asm. assemble it to print routines SNES addresses.
                asmPatch += [ 0x20, 0x00, 0xF6 ]    # JSR incompatible_doors
                asmPatch += [ 0xA9, X0,   X1   ]    # LDA #$SamusX        ; fixed Samus X position
                asmPatch += [ 0x8D, 0xF6, 0x0A ]    # STA $0AF6           ; update Samus X position in memory
                asmPatch += [ 0xA9, Y0,   Y1   ]    # LDA #$SamusY        ; fixed Samus Y position
                asmPatch += [ 0x8D, 0xFA, 0x0A ]    # STA $0AFA           ; update Samus Y position in memory
            else:
                # still give I-frames
                asmPatch += [ 0x20, 0x40, 0xF6 ]    # JSR giveiframes
            # return
            asmPatch += [ 0x60 ]   # RTS
            self.romFile.writeWord(asmAddress & 0xFFFF)

            self.romFile.seek(asmAddress)
            for byte in asmPatch:
                self.romFile.writeByte(byte)
            # print("asmAddress=%x" % asmAddress)
            # print("asmPatch=" + str(["%02x" % b for b in asmPatch]))

            asmAddress += len(asmPatch)
            # update room state header with song changes
            # TODO just do an IPS patch for this as it is completely static
            #      this would get rid of both 'song' and 'songs' fields
            #      as well as this code
            if 'song' in conn:
                for addr in conn["songs"]:
                    self.romFile.seek(0x70000 + addr)
                    self.romFile.writeByte(conn['song'])
                    self.romFile.writeByte(0x5)

    # change BG table to avoid scrolling sky bug when transitioning to west ocean
    def patchWestOcean(self, doorPtr):
        self.romFile.writeWord(doorPtr, 0x7B7BB)

    # forces CRE graphics refresh when exiting kraid's or croc room
    def forceRoomCRE(self, roomPtr, creFlag=0x2):
        # Room ptr in bank 8F + CRE flag offset
        offset = 0x70000 + roomPtr + 0x8
        self.romFile.writeByte(creFlag, offset)

    buttons = {
        "Select" : [0x00, 0x20],
        "A"      : [0x80, 0x00],
        "B"      : [0x00, 0x80],
        "X"      : [0x40, 0x00],
        "Y"      : [0x00, 0x40],
        "L"      : [0x20, 0x00],
        "R"      : [0x10, 0x00],
        "None"   : [0x00, 0x00]
    }

    controls = {
        "Shoot"       : [0xb331, 0x1722d],
        "Jump"        : [0xb325, 0x17233],
        "Dash"        : [0xb32b, 0x17239],
        "Item Select" : [0xb33d, 0x17245],
        "Item Cancel" : [0xb337, 0x1723f],
        "Angle Up"    : [0xb343, 0x1724b],
        "Angle Down"  : [0xb349, 0x17251]
    }

    # write custom contols to ROM.
    # controlsDict : possible keys are "Shot", "Jump", "Dash", "ItemSelect", "ItemCancel", "AngleUp", "AngleDown"
    #                possible values are "A", "B", "X", "Y", "L", "R", "Select", "None"
    def writeControls(self, controlsDict):
        for ctrl, button in controlsDict.items():
            if ctrl not in RomPatcher.controls:
                raise ValueError("Invalid control name : " + str(ctrl))
            if button not in RomPatcher.buttons:
                raise ValueError("Invalid button name : " + str(button))
            for addr in RomPatcher.controls[ctrl]:
                self.romFile.writeByte(RomPatcher.buttons[button][0], addr)
                self.romFile.writeByte(RomPatcher.buttons[button][1])

    def writePlandoAddresses(self, locations):
        self.romFile.seek(0x2F6000)
        for loc in locations:
            self.romFile.writeWord(loc.Address & 0xFFFF)

        # fill remaining addresses with 0xFFFF
        maxLocsNumber = 128
        for i in range(0, maxLocsNumber-len(locations)):
            self.romFile.writeWord(0xFFFF)

    def writePlandoTransitions(self, transitions, doorsPtrs, maxTransitions):
        self.romFile.seek(0x2F6100)

        for (src, dest) in transitions:
            self.romFile.writeWord(doorsPtrs[src])
            self.romFile.writeWord(doorsPtrs[dest])

        # fill remaining addresses with 0xFFFF
        for i in range(0, maxTransitions-len(transitions)):
            self.romFile.writeWord(0xFFFF)
            self.romFile.writeWord(0xFFFF)

    def enableMoonWalk(self):
        # replace STZ with STA since A is non-zero at this point
        self.romFile.writeByte(0x8D, 0xB35D)

    def setOamTile(self, nth, middle, newTile, y=0xFC):
        # an oam entry is made of five bytes: (s000000 xxxxxxxxx) (yyyyyyyy) (YXpp000t tttttttt)

        # after and before the middle of the screen is not handle the same
        if nth >= middle:
            x = (nth - middle) * 0x08
        else:
            x = 0x200 - (0x08 * (middle - nth))

        self.romFile.writeWord(x)
        self.romFile.writeByte(y)
        self.romFile.writeWord(0x3100+newTile)

    def writeVersion(self, version, addRotation=False):
        # max 32 chars

        # new oamlist address in free space at the end of bank 8C
        self.romFile.writeWord(0xF3E9, 0x5a0e3)
        self.romFile.writeWord(0xF3E9, 0x5a0e9)

        # string length
        versionLength = len(version)
        if addRotation:
            rotationLength = len('rotation')
            length = versionLength + rotationLength
        else:
            length = versionLength
        self.romFile.writeWord(length, 0x0673e9)
        versionMiddle = int(versionLength / 2) + versionLength % 2

        # oams
        for (i, char) in enumerate(version):
            self.setOamTile(i, versionMiddle, char2tile[char])

        if addRotation:
            rotationMiddle = int(rotationLength / 2) + rotationLength % 2
            for (i, char) in enumerate('rotation'):
                self.setOamTile(i, rotationMiddle, char2tile[char], y=0x8e)

    def writeDoorsColor(self, doors, player):
        DoorsManager.writeDoorsColor(self.romFile, doors, player)

# tile number in tileset
char2tile = {
    '-': 207,
    'a': 208,
    '.': 243,
    '0': 244
}
for i in range(1, ord('z')-ord('a')+1):
    char2tile[chr(ord('a')+i)] = char2tile['a']+i
for i in range(1, ord('9')-ord('0')+1):
    char2tile[chr(ord('0')+i)] = char2tile['0']+i

class MessageBox(object):
    def __init__(self, rom):
        self.rom = rom

        # in message boxes the char a is at offset 0xe0 in the tileset
        self.char2tile = {'1': 0x00, '2': 0x01, '3': 0x02, '4': 0x03, '5': 0x04, '6': 0x05, '7': 0x06, '8': 0x07, '9': 0x08, '0': 0x09,
                          ' ': 0x4e, '-': 0xcf, 'a': 0xe0, '.': 0xfa, ',': 0xfb, '`': 0xfc, "'": 0xfd, '?': 0xfe, '!': 0xff}
        for i in range(1, ord('z')-ord('a')+1):
            self.char2tile[chr(ord('a')+i)] = self.char2tile['a']+i

        # add 0x0c/0x06 to offsets as there's 12/6 bytes before the strings, string length is either 0x13/0x1a
        self.offsets = {
            'ETank': (0x2877f+0x0c, 0x13),
            'Missile': (0x287bf+0x06, 0x1a),
            'Super': (0x288bf+0x06, 0x1a),
            'PowerBomb': (0x289bf+0x06, 0x1a),
            'Grapple': (0x28abf+0x06, 0x1a),
            'XRayScope': (0x28bbf+0x06, 0x1a),
            'Varia': (0x28cbf+0x0c, 0x13),
            'SpringBall': (0x28cff+0x0c, 0x13),
            'Morph': (0x28d3f+0x0c, 0x13),
            'ScrewAttack': (0x28d7f+0x0c, 0x13),
            'HiJump': (0x28dbf+0x0c, 0x13),
            'SpaceJump': (0x28dff+0x0c, 0x13),
            'SpeedBooster': (0x28e3f+0x06, 0x1a),
            'Charge': (0x28f3f+0x0c, 0x13),
            'Ice': (0x28f7f+0x0c, 0x13),
            'Wave': (0x28fbf+0x0c, 0x13),
            'Spazer': (0x28fff+0x0c, 0x13),
            'Plasma': (0x2903f+0x0c, 0x13),
            'Bomb': (0x2907f+0x06, 0x1a),
            'Reserve': (0x294ff+0x0c, 0x13),
            'Gravity': (0x2953f+0x0c, 0x13)
        }

    def updateMessage(self, box, message, vFlip=False, hFlip=False):
        (address, oldLength) = self.offsets[box]
        newLength = len(message)
        assert newLength <= oldLength, "string '{}' is too long, max {}".format(message, oldLength)
        padding = oldLength - newLength
        paddingLeft = int(padding / 2)
        paddingRight = int(padding / 2)
        paddingRight += padding % 2

        attr = self.getAttr(vFlip, hFlip)

        # write spaces for padding left
        for i in range(paddingLeft):
            self.writeChar(address, ' ')
            address += 0x02
        # write message
        for char in message:
            self.writeChar(address, char)
            address += 0x01
            self.updateAttr(attr, address)
            address += 0x01
        # write spaces for padding right
        for i in range(paddingRight):
            self.writeChar(address, ' ')
            address += 0x02

    def writeChar(self, address, char):
        self.rom.writeByte(self.char2tile[char], address)

    def getAttr(self, vFlip, hFlip):
        # vanilla is 0x28:
        byte = 0x28
        if vFlip:
            byte |= 0b10000000
        if hFlip:
            byte |= 0b01000000
        return byte

    def updateAttr(self, byte, address):
        self.rom.writeByte(byte, address)
