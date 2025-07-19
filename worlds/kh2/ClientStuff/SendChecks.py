from CommonClient import logger
from .WorldLocations import *
from typing import TYPE_CHECKING

# I don't know what is going on here, but it works.
if TYPE_CHECKING:
    from . import KH2Context
else:
    KH2Context = object


def finishedGame(ctx: KH2Context):
    if ctx.kh2slotdata['FinalXemnas'] == 1:
        if not ctx.final_xemnas and ctx.kh2_read_byte(
                ctx.Save + all_world_locations[LocationName.FinalXemnas].addrObtained) \
                & 0x1 << all_world_locations[LocationName.FinalXemnas].bitIndex > 0:
            ctx.final_xemnas = True
    # three proofs
    if ctx.kh2slotdata['Goal'] == 0:
        if ctx.kh2_read_byte(ctx.Save + 0x36B2) > 0 \
                and ctx.kh2_read_byte(ctx.Save + 0x36B3) > 0 \
                and ctx.kh2_read_byte(ctx.Save + 0x36B4) > 0:
            if ctx.kh2slotdata['FinalXemnas'] == 1:
                if ctx.final_xemnas:
                    return True
                return False
            return True
        return False
    elif ctx.kh2slotdata['Goal'] == 1:
        if ctx.kh2_read_byte(ctx.Save + 0x3641) >= ctx.kh2slotdata['LuckyEmblemsRequired']:
            if ctx.kh2_read_byte(ctx.Save + 0x36B3) < 1:
                ctx.kh2_write_byte(ctx.Save + 0x36B2, 1)
                ctx.kh2_write_byte(ctx.Save + 0x36B3, 1)
                ctx.kh2_write_byte(ctx.Save + 0x36B4, 1)
                logger.info("The Final Door is now Open")
            if ctx.kh2slotdata['FinalXemnas'] == 1:
                if ctx.final_xemnas:
                    return True
                return False
            return True
        return False
    elif ctx.kh2slotdata['Goal'] == 2:
        # for backwards compat
        if "hitlist" in ctx.kh2slotdata:
            locations = ctx.sending
            for boss in ctx.kh2slotdata["hitlist"]:
                if boss in locations:
                    ctx.hitlist_bounties += 1
        if ctx.hitlist_bounties >= ctx.kh2slotdata["BountyRequired"] or ctx.kh2_seed_save_cache["AmountInvo"]["Amount"][
            "Bounty"] >= ctx.kh2slotdata["BountyRequired"]:
            if ctx.kh2_read_byte(ctx.Save + 0x36B3) < 1:
                ctx.kh2_write_byte(ctx.Save + 0x36B2, 1)
                ctx.kh2_write_byte(ctx.Save + 0x36B3, 1)
                ctx.kh2_write_byte(ctx.Save + 0x36B4, 1)
                logger.info("The Final Door is now Open")
            if ctx.kh2slotdata['FinalXemnas'] == 1:
                if ctx.final_xemnas:
                    return True
                return False
            return True
        return False
    elif ctx.kh2slotdata["Goal"] == 3:
        if ctx.kh2_seed_save_cache["AmountInvo"]["Amount"]["Bounty"] >= ctx.kh2slotdata["BountyRequired"] and \
                ctx.kh2_read_byte(ctx.Save + 0x3641) >= ctx.kh2slotdata['LuckyEmblemsRequired']:
            if ctx.kh2_read_byte(ctx.Save + 0x36B3) < 1:
                ctx.kh2_write_byte(ctx.Save + 0x36B2, 1)
                ctx.kh2_write_byte(ctx.Save + 0x36B3, 1)
                ctx.kh2_write_byte(ctx.Save + 0x36B4, 1)
                logger.info("The Final Door is now Open")
            if ctx.kh2slotdata['FinalXemnas'] == 1:
                if ctx.final_xemnas:
                    return True
                return False
            return True
        return False


async def checkWorldLocations(self):
    try:
        currentworldint = self.kh2_read_byte(self.Now)
        if self.last_world_int != currentworldint:
            self.last_world_int = currentworldint
            await self.send_msgs([{
                "cmd":     "Set", "key": "Slot: " + str(self.slot) + " :CurrentWorld",
                "default": 0, "want_reply": False, "operations": [{
                    "operation": "replace",
                    "value":     currentworldint
                }]
            }])
        if currentworldint in self.worldid_to_locations:
            curworldid = self.worldid_to_locations[currentworldint]
            for location, data in curworldid.items():
                if location in self.kh2_loc_name_to_id.keys():
                    locationId = self.kh2_loc_name_to_id[location]
                    if locationId not in self.locations_checked \
                            and self.kh2_read_byte(self.Save + data.addrObtained) & 0x1 << data.bitIndex > 0:
                        self.sending = self.sending + [(int(locationId))]
    except Exception as e:
        if self.kh2connected:
            self.kh2connected = False
        logger.info(e)
        logger.info("line 425")


async def checkLevels(self):
    try:
        for location, data in SoraLevels.items():
            currentLevel = self.kh2_read_byte(self.Save + 0x24FF)
            locationId = self.kh2_loc_name_to_id[location]
            if locationId not in self.locations_checked \
                    and currentLevel >= data.bitIndex:
                if self.kh2_seed_save["Levels"]["SoraLevel"] < currentLevel:
                    self.kh2_seed_save["Levels"]["SoraLevel"] = currentLevel
                self.sending = self.sending + [(int(locationId))]
        formDict = {
            0: ["ValorLevel", ValorLevels], 1: ["WisdomLevel", WisdomLevels], 2: ["LimitLevel", LimitLevels],
            3: ["MasterLevel", MasterLevels], 4: ["FinalLevel", FinalLevels], 5: ["SummonLevel", SummonLevels]
        }
        for i in range(6):
            for location, data in formDict[i][1].items():
                formlevel = self.kh2_read_byte(self.Save + data.addrObtained)
                if location in self.kh2_loc_name_to_id.keys():
                    # if current form level is above other form level
                    locationId = self.kh2_loc_name_to_id[location]
                    if locationId not in self.locations_checked \
                            and formlevel >= data.bitIndex:
                        if formlevel > self.kh2_seed_save["Levels"][formDict[i][0]]:
                            self.kh2_seed_save["Levels"][formDict[i][0]] = formlevel
                        self.sending = self.sending + [(int(locationId))]
    except Exception as e:
        if self.kh2connected:
            self.kh2connected = False
        logger.info(e)
        logger.info("line 456")


async def checkSlots(self):
    try:
        for location, data in weaponSlots.items():
            locationId = self.kh2_loc_name_to_id[location]
            if locationId not in self.locations_checked:
                if self.kh2_read_byte(self.Save + data.addrObtained) > 0:
                    self.sending = self.sending + [(int(locationId))]

        for location, data in formSlots.items():
            locationId = self.kh2_loc_name_to_id[location]
            if locationId not in self.locations_checked and self.kh2_read_byte(self.Save + 0x06B2) == 0:
                if self.kh2_read_byte(self.Save + data.addrObtained) & 0x1 << data.bitIndex > 0:
                    self.sending = self.sending + [(int(locationId))]
    except Exception as e:
        if self.kh2connected:
            self.kh2connected = False
        logger.info(e)
        logger.info("line 475")


async def verifyChests(self):
    try:
        for location in self.locations_checked:
            locationName = self.lookup_id_to_location[location]
            if locationName in self.chest_set:
                if locationName in self.location_name_to_worlddata.keys():
                    locationData = self.location_name_to_worlddata[locationName]
                    if self.kh2_read_byte(
                            self.Save + locationData.addrObtained) & 0x1 << locationData.bitIndex == 0:
                        roomData = self.kh2_read_byte(self.Save + locationData.addrObtained)
                        self.kh2_write_byte(self.Save + locationData.addrObtained,
                                            roomData | 0x01 << locationData.bitIndex)

    except Exception as e:
        if self.kh2connected:
            self.kh2connected = False
        logger.info(e)
        logger.info("line 491")


async def verifyLevel(self):
    for leveltype, anchor in {
        "SoraLevel":   0x24FF,
        "ValorLevel":  0x32F6,
        "WisdomLevel": 0x332E,
        "LimitLevel":  0x3366,
        "MasterLevel": 0x339E,
        "FinalLevel":  0x33D6
    }.items():
        if self.kh2_read_byte(self.Save + anchor) < self.kh2_seed_save["Levels"][leveltype]:
            self.kh2_write_byte(self.Save + anchor, self.kh2_seed_save["Levels"][leveltype])
