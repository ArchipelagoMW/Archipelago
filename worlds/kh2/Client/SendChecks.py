from CommonClient import logger
from .WorldLocations import *
from typing import TYPE_CHECKING
from .Socket import MessageType

# I don't know what is going on here, but it works.
if TYPE_CHECKING:
    from . import KH2Context
else:
    KH2Context = object

def finishedGame(ctx: KH2Context):
    # three proofs
    if ctx.kh2slotdata['Goal'] == 0:
        if ctx.proof_of_nonexistence and ctx.proof_of_connection and ctx.proof_of_peace:
            if ctx.kh2slotdata['FinalXemnas'] == 1:
                return ctx.final_xemnas_defeated
            return True
        return False
    elif ctx.kh2slotdata['Goal'] == 1:
        if ctx.lucky_emblems >= ctx.kh2slotdata['LuckyEmblemsRequired']:
            if not ctx.give_proofs:
                ctx.socket.send(MessageType.GiveProofs, ())
                ctx.give_proofs = True
                logger.info("The Final Door is now Open")
            if ctx.kh2slotdata['FinalXemnas'] == 1:
                return ctx.final_xemnas_defeated
            return True
        return False
    elif ctx.kh2slotdata['Goal'] == 2:
        if len(ctx.bounties) >= ctx.kh2slotdata["BountyRequired"]:
            if not ctx.give_proofs:
                ctx.socket.send(MessageType.GiveProofs, ())
                ctx.give_proofs = True
                logger.info("The Final Door is now Open")
            if ctx.kh2slotdata['FinalXemnas'] == 1:
                return ctx.final_xemnas_defeated
            return True
        return False
    elif ctx.kh2slotdata["Goal"] == 3:
        if len(ctx.bounties) >= ctx.kh2slotdata["BountyRequired"] and ctx.lucky_emblems >= ctx.kh2slotdata['LuckyEmblemsRequired']:
            if not ctx.give_proofs:
                ctx.socket.send(MessageType.GiveProofs, ())
                ctx.give_proofs = True
                logger.info("The Final Door is now Open")
            if ctx.kh2slotdata['FinalXemnas'] == 1:
                return ctx.final_xemnas_defeated
            return True
        return False

async def checkWorldLocations(self):
    try:
        if self.last_world_int != self.current_world_int:
            self.last_world_int = self.current_world_int
            await self.send_msgs([{
                "cmd":     "Set", "key": "Slot: " + str(self.slot) + " :CurrentWorld",
                "default": 0, "want_reply": False, "operations": [{
                    "operation": "replace",
                    "value":     self.current_world_int
                }]
            }])
        if self.current_world_int in self.worldid_to_locations:
            curworldid = self.worldid_to_locations[self.current_world_int]
            for location, data in curworldid.items():
                if location in self.kh2_loc_name_to_id.keys():
                    locationId = self.kh2_loc_name_to_id[location]
                    if location in self.world_locations_checked:
                        self.sending.append(int(locationId))
                        self.world_locations_checked.discard(location)
    except Exception as e:
        if self.kh2connected:
            self.kh2connected = False
        logger.info(e)
        logger.info("Error in checkWorldLocations")


async def checkLevels(self):
    try:
        for location, data in SoraLevels.items():
            currentLevel = self.sora_levels["Sora"]
            locationId = self.kh2_loc_name_to_id[location]
            if locationId not in self.checked_locations \
                    and currentLevel >= data.bitIndex:
                self.sending.append(int(locationId))
        formDict = {
            0: ["ValorLevel", ValorLevels], 1: ["WisdomLevel", WisdomLevels], 2: ["LimitLevel", LimitLevels],
            3: ["MasterLevel", MasterLevels], 4: ["FinalLevel", FinalLevels], 5: ["SummonLevel", SummonLevels]
        }
        for i in range(6):
            for location, data in formDict[i][1].items():
                formlevel = self.sora_levels[formDict[i][0]]
                if location in self.kh2_loc_name_to_id.keys():
                    # if current form level is above other form level
                    locationId = self.kh2_loc_name_to_id[location]
                    if locationId not in self.checked_locations \
                            and formlevel >= data.bitIndex:
                        self.sending.append(int(locationId))
    except Exception as e:
        if self.kh2connected:
            self.kh2connected = False
        logger.info(e)
        logger.info("Error in checkLevels")


async def checkSlots(self):
    try:
        for location, data in weaponSlots.items():
            locationId = self.kh2_loc_name_to_id[location]
            if locationId not in self.checked_locations:
                if location in self.keyblade_ability_checked:
                    self.sending.append(int(locationId))
                    self.keyblade_ability_checked.discard(location)

        for location, data in formSlots.items():
            locationId = self.kh2_loc_name_to_id[location]
            if locationId not in self.checked_locations and location in self.keyblade_ability_checked:
                self.sending.append(int(locationId))
                self.keyblade_ability_checked.discard(location)
    except Exception as e:
        if self.kh2connected:
            self.kh2connected = False
        logger.info(e)
        logger.info("Error in checkSlots")
