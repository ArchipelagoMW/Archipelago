import json, os.path

# record solver/rando to play in the VCR tracker
class VCR(object):
    def __init__(self, name, type):
        self.baseName = os.path.basename(os.path.splitext(name)[0])
        self.outFileName = "{}.{}.vcr".format(self.baseName, type)
        self.empty()

    def empty(self):
        self.tape = []

    def addLocation(self, locName, itemName):
        self.tape.append({'type': 'location', 'loc': locName, 'item': itemName})

    def addRollback(self, count):
        self.tape.append({'type': 'rollback', 'count': count})

    def dump(self):
        with open(self.outFileName, 'w') as jsonFile:
            json.dump(self.tape, jsonFile)

    # in scavenger we have the rando solver then the scav solver, generate vcr for both
    def reinit(self, type):
        self.dump()
        self.outFileName = "{}.{}.vcr".format(self.baseName, type)
        self.empty()
