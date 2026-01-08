class Match():
    DATA_SIZE = 4

    def __init__(self, data):
        assert(len(data) == self.DATA_SIZE)

        self.opponent = data[0]
        self.unknown = data[1]
        self.reward = data[2]
        self.reward_hidden = data[3]

    def data(self):
        data = [0x00] * self.DATA_SIZE

        data[0] = self.opponent
        data[1] = self.unknown
        data[2] = self.reward
        data[3] = self.reward_hidden

        return data
