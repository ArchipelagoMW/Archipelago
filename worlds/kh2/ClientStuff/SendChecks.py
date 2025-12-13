from CommonClient import logger
from .WorldLocations import *
from typing import TYPE_CHECKING

# I don't know what is going on here, but it works.
if TYPE_CHECKING:
    from . import KH2Context
else:
    KH2Context = object

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
                        self.sending = self.sending + [(int(locationId))]
                        self.check_location_IDs.append((int(locationId)))
                        self.world_locations_checked.remove(location)
    except Exception as e:
        if self.kh2connected:
            self.kh2connected = False
        logger.info(e)
        logger.info("line 425")


async def checkLevels(self):
    try:
        for location, data in SoraLevels.items():
            currentLevel = self.sora_form_levels["Sora"]
            locationId = self.kh2_loc_name_to_id[location]
            if locationId not in self.locations_checked \
                    and currentLevel >= data.bitIndex:
                if self.kh2_seed_save["Levels"]["SoraLevel"] < currentLevel:
                    self.kh2_seed_save["Levels"]["SoraLevel"] = currentLevel
                self.sending = self.sending + [(int(locationId))]
                self.check_location_IDs.append((int(locationId)))
        formDict = {
            0: ["ValorLevel", ValorLevels], 1: ["WisdomLevel", WisdomLevels], 2: ["LimitLevel", LimitLevels],
            3: ["MasterLevel", MasterLevels], 4: ["FinalLevel", FinalLevels], 5: ["SummonLevel", SummonLevels]
        }
        for i in range(6):
            for location, data in formDict[i][1].items():
                formlevel = self.sora_form_levels[formDict[i][0]]
                if location in self.kh2_loc_name_to_id.keys():
                    # if current form level is above other form level
                    locationId = self.kh2_loc_name_to_id[location]
                    if locationId not in self.locations_checked \
                            and formlevel >= data.bitIndex:
                        if formlevel > self.kh2_seed_save["Levels"][formDict[i][0]]:
                            self.kh2_seed_save["Levels"][formDict[i][0]] = formlevel
                        self.sending = self.sending + [(int(locationId))]
                        self.check_location_IDs.append((int(locationId)))
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
                if location in self.keyblade_ability_checked:
                    self.sending = self.sending + [(int(locationId))]
                    self.check_location_IDs.append((int(locationId)))
                    self.keyblade_ability_checked.remove(location)

        for location, data in formSlots.items():
            locationId = self.kh2_loc_name_to_id[location]
            if locationId not in self.locations_checked and location in self.keyblade_ability_checked:
                self.sending = self.sending + [(int(locationId))]
                self.check_location_IDs.append((int(locationId)))
                self.keyblade_ability_checked.remove(location)
    except Exception as e:
        if self.kh2connected:
            self.kh2connected = False
        logger.info(e)
        logger.info("line 475")
