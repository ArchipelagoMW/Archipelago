import pathlib
import os
pathlib.Path(__file__).parent.resolve()

overallAllItems = set()
eventPanelsFromRegions = set()
eventPanelsFromPanels = set()

def getIndependentRequirementWithinRegionOf(check, checksDependentByHex): 
    global eventPanelsFromPanels
    global overallAllItems
    
    for itemSet in check["requirement"]["items"]:
        for item in itemSet:
            if item not in {item[0] for item in overallAllItems}:
                overallAllItems.add((item, len(overallAllItems)))
  
    if check["requirement"]["panels"] == frozenset({frozenset()}):
        return check["requirement"]["items"]

    allOptions = set()
   
    theseItems = check["requirement"]["items"]

    #redo tomorrow
    for option in check["requirement"]["panels"]: 
        dependentItemsForOption = frozenset({frozenset()})
    
        for panel in option:
            newDependentItems = set()
            
            if panel == "7 Lasers" or panel == "11 Lasers":
                newDependentItems = frozenset({frozenset([panel])})
            elif checksDependentByHex[panel]["region"]["name"] != check["region"]["name"]:
                newDependentItems = frozenset({frozenset([panel])})
                eventPanelsFromPanels.add(panel)
            else:
                newDependentItems = getIndependentRequirementWithinRegionOf(checksDependentByHex[panel], checksDependentByHex)
            
            newDependentItemsForOption = set()
            
            for itemsOption in dependentItemsForOption:
                for itemsOption2 in newDependentItems:
                    newDependentItemsForOption.add(itemsOption.union(itemsOption2))
            
            dependentItemsForOption = set(newDependentItemsForOption)
                    
        for itemsOption in theseItems:
            for dependentItem in dependentItemsForOption:
                allOptions.add(itemsOption.union(dependentItem))
       
                    
                    
    return frozenset(allOptions)
           
            

def parseLambda(lambdaString):
    if lambdaString == "True":
        return frozenset([frozenset()])
    lambdaStringAnds = set(lambdaString.split(" | "))
    lambdaList = frozenset({frozenset(andString.split(" & ")) for andString in lambdaStringAnds})
    
    return lambdaList



def defineNewRegion(line):
    line = line[:-1]
    lineSplit = line.split(" - ")
   
    regionNameFull = lineSplit.pop(0)
    
    regionNameSplit = regionNameFull.split(" (")
    
    regionName = regionNameSplit[0]
    regionNameShort = regionNameSplit[1][:-1]
    
    options = set()
    
    for i in range(len(lineSplit) // 2):
        connectedRegion = lineSplit.pop(0)
        correspondingLambda = lineSplit.pop(0)
        
        for panelOption in parseLambda(correspondingLambda):
            for panel in panelOption:
                eventPanelsFromRegions.add(panel)
    
        options.add((connectedRegion, parseLambda(correspondingLambda)))   
    
    regionObject = {"name": regionName, "shortName": regionNameShort, "connections": options, "panels": []};
    return regionObject


f = open(os.path.join(os.path.dirname(__file__), "WitnessLogic.txt"));

currentRegion = ""

allRegionsByName = dict()
checksDependentByHex = dict()

discardIDs = 0
normalPanelIDs = 0
vaultIDs = 0
laserIDs = 0

for line in f.readlines():
    line = line.strip()
    
    if line == "":
        continue
        
    if line[0] != "0":
        currentRegion = defineNewRegion(line)
        allRegionsByName[currentRegion["name"]] = currentRegion
        continue;
    
    
    lineSplit = line.split(" - ")
        
    checkNameFull = lineSplit.pop(0)
    
    checkHex = checkNameFull[0:7]
    checkName = checkNameFull[9:-1]    
    
    requiredPanel = lineSplit.pop(0)
    correspondingLambda = lineSplit.pop(0)
    
    locationID = 0
    locationType = ""
    
    if "Discard" in checkName:
        locationType = "Discard"
        locationID = discardIDs
        discardIDs += 1
    elif "Vault" in checkName or "Video" in checkName or checkName == "Tutorial Gate Close":
        locationType = "Vault"
        locationID = vaultIDs
        vaultIDs += 1
    elif checkName == "Laser" or checkName == "Laser Hedges" or checkName == "Laser Pressure Plates":
        locationType = "Laser"
        locationID = laserIDs
        laserIDs += 1
    else:
        locationType = "General"
        locationID = normalPanelIDs
        normalPanelIDs += 1
   
    requirement = {"panels": parseLambda(requiredPanel), "items": parseLambda(correspondingLambda)}
    
    checksDependentByHex[checkHex] = {"checkName": currentRegion["shortName"] + " " + checkName, "checkHex": checkHex, "region": currentRegion, "requirement": requirement, "idOffset": locationID, "panelType": locationType}
   
    currentRegion["panels"].append(checkHex)
    

checksByHex = dict()
checksByName = dict()

for checkHex, check in checksDependentByHex.items():
    independentRequirement = getIndependentRequirementWithinRegionOf(check, checksDependentByHex)
    
    newCheck = {"checkName": check["checkName"], "checkHex": check["checkHex"], "region": check["region"], "requirement": independentRequirement, "idOffset": check["idOffset"], "panelType": check["panelType"]}
    
    checksByHex[checkHex] = newCheck
    checksByName[newCheck["checkName"]] = newCheck
    
    
originalEventPanels = eventPanelsFromPanels | eventPanelsFromRegions
eventPanels = set() | eventPanelsFromPanels

for panel in eventPanelsFromRegions:
    for regionName, region in allRegionsByName.items():
        for connection in region["connections"]:
            connectedRegionName = connection[0]
            if connectedRegionName not in allRegionsByName:
                continue
            
            if regionName == "Boat" or connectedRegionName == "Boat":
                continue
            
            connectedRegion = allRegionsByName[connectedRegionName]
            
            if not any([panel in option for option in connection[1]]):
                continue
            
            if panel not in region["panels"] and panel not in connectedRegion["panels"]:
                eventPanels.add(panel)
               

eventItemNames = {
    "0x01A0F": "Keep Laser Panel (Hedge Mazes) Activates",
    "0x09D9B": "Monastery Overhead Doors Open",
    "0x193A6": "Monastery Laser Panel Activates",
    "0x00037": "Monastery Branch Panels Activate",
    "0x0A079": "Access to Bunker Laser",
    "0x0A3B5": "Door to Tutorial Discard Opens",
    "0x01D3F": "Keep Laser Panel (Pressure Plates) Activates",
    "0x09F7F": "Mountain Access",
    "0x0367C": "Quarry Laser Mill Requirement Met",
    "0x009A1": "Swamp Rotating Bridge Near Side",
    "0x00006": "Swamp Cyan Water Drains",
    "0x00990": "Swamp Broken Shapers 1 Activates",
    "0x0A8DC": "Lower Avoid 6 Activates",
    "0x0000A": "Swamp More Rotated Shapers 1 Access",
    "0x09ED8": "Inside Mountain Second Layer Both Light Bridges Solved",
    "0x0A3D0": "Quarry Laser Boathouse Requirement Met",
    "0x00596": "Swamp Red Water Drains",
}


alwaysEventsByName = {
    "Symmetry Laser Activation": "0x0360D",
    "Desert Laser Activation": "0x03608", 
    "Desert Laser Redirection": "0x09F98",
    "Quarry Laser Activation": "0x03612",
    "Shadows Laser Activation": "0x19650",
    "Keep Laser Hedges Activation": "0x0360E",
    "Keep Laser Pressure Plates Activation": "0x03317",
    "Monastery Laser Activation": "0x17CA4",
    "Town Laser Activation": "0x032F5",
    "Jungle Laser Activation": "0x03616",
    "Bunker Laser Activation": "0x09DE0",
    "Swamp Laser Activation": "0x03615",
    "Treehouse Laser Activation": "0x03613",
    "Shipwreck Video Pattern Knowledge": "0x03535",
    "Mountain Video Pattern Knowledge": "0x03542",
    "Desert Video Pattern Knowledge": "0x0339E",
    "Tutorial Video Pattern Knowledge": "0x03481",
    "Jungle Video Pattern Knowledge": "0x03702",
    "Theater Walkway Video Pattern Knowledge": "0x2FAF6"
}

alwaysEventHexCodes = set()

for alwaysEventItem, alwaysEventHexAndID in alwaysEventsByName.items():
    alwaysEventHexCodes.add(alwaysEventHexAndID)
    eventPanels.add(alwaysEventHexAndID)
    eventItemNames[alwaysEventHexAndID] = alwaysEventItem
    
eventItemPairs = {checksByHex[panelHex]["checkName"] + " Solved": eventItemNames[panelHex] for panelHex in eventPanels}
    
