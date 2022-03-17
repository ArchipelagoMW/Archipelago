import pathlib
pathlib.Path(__file__).parent.resolve()

overallAllItems = set()

def getIndependentRequirementOf(check, checksDependentByHex):  
    global overallAllItems
  
    if check["requirement"]["panels"] == frozenset({frozenset()}):
        return check["requirement"]["items"]

    allOptions = set()
   
    theseItems = check["requirement"]["items"]

    for option in check["requirement"]["panels"]:    
        for panel in option:
            if panel == "7 Lasers":
                thisPanelOptions = frozenset(frozenset("7 Lasers"))
                continue
                
            if panel == "11 Lasers":
                thisPanelOptions = frozenset(frozenset("11 Lasers"))
                continue
        
            dependentItems = getIndependentRequirementOf(checksDependentByHex[panel], checksDependentByHex)

            for itemsOption in theseItems:
                for dependentItem in dependentItems:
                    #print("Dependent")
                    #print(dependentItem)
                    allOptions.add(itemsOption.union(dependentItem))
                    
                    overallAllItems = overallAllItems.union(itemsOption).union(dependentItem)
                    
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
   
    regionName = lineSplit.pop(0)
    options = set()
    
    for i in range(len(lineSplit) // 2):
        connectedRegion = lineSplit.pop(0)
        correspondingLambda = lineSplit.pop(0)
    
        options.add((connectedRegion, parseLambda(correspondingLambda)))
        
    regionObject = {"name": regionName, "connections": options};
    return regionObject


f = open("WitnessLogic.txt");

currentRegion = ""

regions = []
checksDependentByHex = dict()

for line in f.readlines():
    line = line.strip()
    
    if line == "":
        continue
        
    if line[0] != "0":
        currentRegion = defineNewRegion(line)
        regions.append(currentRegion)
        continue;
    
    
    lineSplit = line.split(" - ")
        
    checkNameFull = lineSplit.pop(0)
    
    checkHex = checkNameFull[0:7]
    checkName = checkNameFull[9:-1]    
    
    requiredPanel = lineSplit.pop(0)
    correspondingLambda = lineSplit.pop(0)
   
    requirement = {"panels": parseLambda(requiredPanel), "items": parseLambda(correspondingLambda)}
    
    checksDependentByHex[checkHex] = {"checkName": checkName, "checkHex": checkHex, "region": currentRegion, "requirement": requirement}
    

checksIndependent = []

for check in checksDependentByHex.values():

    independentRequirement = getIndependentRequirementOf(check, checksDependentByHex)
    
    checksIndependent.append({"checkName": check["checkName"], "checkHex": check["checkHex"], "region": check["region"], "requirement": independentRequirement})
    
print("\n".join([str(check) for check in checksIndependent]))

overallAllItems = list(overallAllItems)
overallAllItems.sort()
print("\n".join(overallAllItems))