import pathlib
import os
pathlib.Path(__file__).parent.resolve()

overallAllItems = set()
eventPanels = set()

def getIndependentRequirementOf(check, checksDependentByHex): 
    global eventPanels
    global overallAllItems
    
    for itemSet in check["requirement"]["items"]:
        overallAllItems = overallAllItems.union(itemSet)
  
    if check["requirement"]["panels"] == frozenset({frozenset()}):
        return check["requirement"]["items"]

    allOptions = set()
   
    theseItems = check["requirement"]["items"]

    for option in check["requirement"]["panels"]:    
        for panel in option:
            if panel == "7 Lasers" or panel == "11 Lasers":
                dependentItems = frozenset({frozenset([panel])})
            else:
                dependentItems = getIndependentRequirementOf(checksDependentByHex[panel], checksDependentByHex)
               

            for itemsOption in theseItems:
                for dependentItem in dependentItems:
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
                eventPanels.add((panel, len(eventPanels)))
    
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
    independentRequirement = getIndependentRequirementOf(check, checksDependentByHex)
    
    newCheck = {"checkName": check["checkName"], "checkHex": check["checkHex"], "region": check["region"], "requirement": independentRequirement, "idOffset": check["idOffset"], "panelType": check["panelType"]}
    
    checksByHex[checkHex] = newCheck
    checksByName[newCheck["checkName"]] = newCheck
    
panelsThatHaveBeenVisited = set()  
panelsThatHaveBeenTrue = set()