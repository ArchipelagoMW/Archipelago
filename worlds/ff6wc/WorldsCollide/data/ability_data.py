class AbilityData:
    DATA_SIZE = 14

    def __init__(self, id, data):
        self.id = id

        self.targets        = data[0]
        self.elements       = data[1]
        self.flags1         = data[2]
        self.flags2         = data[3]
        self.flags3         = data[4]
        self.mp             = data[5]
        self.power          = data[6]
        self.flags4         = data[7]
        self.accuracy       = data[8]
        self.effect         = data[9]
        self.status1        = data[10]
        self.status2        = data[11]
        self.status3        = data[12]
        self.status4        = data[13]

    def ability_data(self):
        data = [0x00] * self.DATA_SIZE

        data[0]     = self.targets
        data[1]     = self.elements
        data[2]     = self.flags1
        data[3]     = self.flags2
        data[4]     = self.flags3
        data[5]     = self.mp
        data[6]     = self.power
        data[7]     = self.flags4
        data[8]     = self.accuracy
        data[9]     = self.effect
        data[10]    = self.status1
        data[11]    = self.status2
        data[12]    = self.status3
        data[13]    = self.status4

        return data
