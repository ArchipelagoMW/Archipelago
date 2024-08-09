import json
import time

import worlds.seaofthieves.Client.SOTWebCollector as SOTWebCollector
import typing

import worlds.seaofthieves.Client.UserInformation as UserInformation
from worlds.seaofthieves.Locations.Locations import WebLocation
from worlds.seaofthieves.Locations.LocationCollection import LocationDetailsCollection, LocDetails
import worlds.seaofthieves.Locations.Shop.Balance as Balance


#from worlds.seaofthieves.Client.windowcapture import  WindowCapture

class SOTDataAnalyzerSettings:

    def __init__(self, details: UserInformation.SotAnalyzerDetails):
        self.details: UserInformation.SotAnalyzerDetails = details

    def get_name_ship(self) -> typing.Optional[str]:
        return self.details.get_ship()

    def get_name_pirate(self) -> typing.Optional[str]:
        return self.details.get_pirate()


class OldNewValues:
    old: int = 0
    new: int = 0


class SOTDataAnalyzer:
    counter = 0
    collector: SOTWebCollector
    settings: SOTDataAnalyzerSettings

    def __init__(self, userInfo: UserInformation.UserInformation, queryperiod: typing.Optional[int] = None):
        self.collector = SOTWebCollector.SOTWebCollector(userInfo.loginCreds, queryperiod)
        self.settings = SOTDataAnalyzerSettings(userInfo.analyzerDetails)
        self.trackedLocations: typing.Dict[int, LocDetails] = {}
        # maps item id -> idx -> value
        self.trackedLocationsData: typing.Dict[int, typing.Dict[int, OldNewValues]] = {}

        self.banned: typing.Dict[int, bool] = {}
        #self.window_capture: WindowCapture = WindowCapture()
        self.last_screenshot_time = -1000
        self.screenshot_second_interval = 2

        self.screenshot_hand = None
        self.screenshot_bottom_text = None
        self.bottom_text: str = ""

    def __readElementFromScreenText(self, web_location: WebLocation) -> bool:


        #check if there is a screen element on the web location
        if web_location.screenData is None:
            return False


        if self.last_screenshot_time + self.screenshot_second_interval < time.time():
            self.last_screenshot_time = time.time()

            try:
                #self.screenshot_hand = self.window_capture.get_screenshot_right_hand()
                #self.screenshot_hand.save("temp_hand.png")
                #self.screenshot_hand.show()
                #self.bottom_text = self.window_capture.get_bt()
                print(self.bottom_text)
                #self.bottom_text = self.window_capture.get_text_from_screenshgot(self.screenshot_bottom_text)

            except Exception as e:

                    print("Game window not found - report as bug if game is running {}".format(e))


        # if web_location.screenData.hasMatch(self.bottom_text, self.screenshot_hand):
        #     print("Found match!!")
        #     return True

        return False


    def __readElementFromWebLocation(self, web_location: WebLocation, json_data):

        if not web_location.webJsonIdentifier.valid:
            # The idea behind this is to allow checks that are not real checks to be incremented once they have started being tracked
            # EX "Item in your Pocket" is made up, so it gets incremented on read after initial population, triggering the item.
            #
            # Therefore, as long as the "Dont track until it should be" logic works, this code will reward fake items with specific conditions
            # at the correct moment during play (granted, it happens up to 'server polling time' after the check actually happens)

            SOTDataAnalyzer.counter = SOTDataAnalyzer.counter + 1
            return SOTDataAnalyzer.counter

        v = None
        alignment = web_location.webJsonIdentifier.alignment
        accolade = web_location.webJsonIdentifier.accolade
        stat = web_location.webJsonIdentifier.stat
        sub_stat = web_location.webJsonIdentifier.substat

        # for each pirate
        if self.settings.get_name_pirate() is not None:
            v = json_data['Pirate']['Alignments'][alignment]['Accolades'][accolade]['Stats'][stat]
        elif self.settings.get_name_ship() is not None:
            v = json_data['Ships'][int(self.settings.get_name_ship())]['Alignments'][alignment]['Accolades'][accolade][
                'Stats'][stat]
        else:
            print("Error: Web Parser: No pirate Name or Ship Name defined")
            return 0

        try:
            read_element = v
            if sub_stat >= 0:
                v = v['SubStats'][sub_stat]
            json_name = v['LocalisedTitle']
            value = v['Value']

            # check to see if the api has updated the substat location. If it did, try to figure out what location to read from in the meantime
            if sub_stat >= 0 and web_location.webJsonIdentifier.json_name is not None and web_location.webJsonIdentifier.json_name != json_name:
                for secondary_sub_stat in read_element['SubStats'].keys():
                    secondary_json_name = read_element['SubStats'][secondary_sub_stat]['LocalisedTitle']
                    secondary_value = read_element['SubStats'][secondary_sub_stat]['Value']

                    if secondary_json_name == web_location.webJsonIdentifier.json_name:
                        loc_ids = "{} {} {} {}".format(alignment, accolade, stat, sub_stat)
                        web_location.webJsonIdentifier.stat = secondary_sub_stat
                        # print("Warning: Web Parser: {} at {} has name {}, but we found {} at {}, using this instead.".format(web_location.webJsonIdentifier.json_name, loc_ids, json_name, secondary_json_name, secondary_value))
                        return secondary_value

            return value

        except:
            print(
                "Error: Web Parser: Please submit bug report for fix, this location will be awarded to the correct player right now. Web Location not found for - " + "{} {} {} {}".format(
                    alignment, accolade, stat, sub_stat))

            # The idea here is to award the player for completing the check
            SOTDataAnalyzer.counter = SOTDataAnalyzer.counter + 1
            return SOTDataAnalyzer.counter

    def stopTracking(self, key: int):
        try:
            self.trackedLocations.pop(key, None)
            self.trackedLocationsData.pop(key, None)
            self.banned[key] = True
        except:
            return

        return

    # region Update
    def update(self) -> None:
        json_data = self.collector.getJson()
        self.__updateWebDataForAll(json_data)

    def __updateWebDataForAll(self, json_data) -> None:
        for loc_det in self.trackedLocations.keys():

            # skip shop items
            if self.trackedLocations[loc_det].cost is None:
                self.__updateWebDataForLocation(self.trackedLocations[loc_det], json_data)

    def __updateWebDataForLocation(self, loc_details: LocDetails, json_data) -> None:

        # just make sure we are not banned
        if loc_details.id in self.banned.keys():
            return

        # we need to check if at least 1 web location value has been updated
        idx = 0
        for web_loc in loc_details.webLocationCollection:
            scrren_caped = False

            # # TODO this is the screen compare logic, WIP
            #
            # try:
            #     scrren_caped = self.__readElementFromScreenText(web_loc)
            # except Exception as e:
            #     print("Fatal Error: " + str(e))
            if scrren_caped:
                # then we detected the check event
                self.trackedLocationsData[loc_details.id][idx].new = self.trackedLocationsData[loc_details.id][
                                                                         idx].old + 1
            elif not web_loc.ocr_only:
                # since the screen event is likely faster, we need to account for that here
                value = self.__readElementFromWebLocation(web_loc, json_data)
                if value < self.trackedLocationsData[loc_details.id][idx].new:
                    # we know it was updated in a different way
                    pass
                else:
                    self.trackedLocationsData[loc_details.id][idx].new = value

            idx = idx + 1

    # endregion

    def rebuild_web_collector(self, loginCreds: SOTWebCollector.UserInformation.SotLoginCredentials):
        self.collector.loginCreds = loginCreds
    def stop_tasks(self):
        self.collector.stop_tasks()

    # region Adding a Location
    def allowTrackingOfLocation(self, loc_detail: LocDetails):

        # do not add twice
        if (loc_detail.id in self.trackedLocations.keys()):
            return

        self.__setInitialValueForLoc(loc_detail)
        self.trackedLocations[loc_detail.id] = loc_detail

    def __setInitialValueForLoc(self, loc_detail: LocDetails) -> None:
        json_data = self.collector.getJson()
        idx = 0
        for web_loc in loc_detail.webLocationCollection:
            value = self.__readElementFromWebLocation(web_loc, json_data)

            if (loc_detail.id not in self.trackedLocationsData.keys()):
                self.trackedLocationsData[loc_detail.id] = {}

            oldNewVals: OldNewValues = OldNewValues()
            oldNewVals.old = value
            oldNewVals.new = value
            self.trackedLocationsData[loc_detail.id][idx] = oldNewVals
            idx = idx + 1

    # endregion

    # region Get completed stuff

    def getAllCompletedChecks(self) -> typing.Dict[int, bool]:

        returndict = {}
        # location id to yes/no
        for locId in self.trackedLocationsData.keys():
            if locId in self.banned.keys():
                continue
            for index in self.trackedLocationsData[locId].keys():
                oldNewData: OldNewValues = self.trackedLocationsData[locId][index]
                if (oldNewData.old != oldNewData.new):
                    returndict[locId] = True

        return returndict

    # endregion

    def getBalance(self) -> Balance.Balance:
        js: json = self.collector.getBalance()
        return Balance.fromJson(js)
