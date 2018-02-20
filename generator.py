from allocation import Allocation
from analyzer import Analyzer

class Generator(object):
    def __init__(self, data, settings):
        self.data = data
        self.settings = settings
        self.allocation = Allocation(data, settings)

    def generate_seed(self):
        while True:
            self.shuffle()
            analyzer = Analyzer(self.data, self.allocation)
            print(analyzer.result)
            print(analyzer.error_message)
            break

    def shuffle(self):
        self.allocation.shuffle(self.data, self.settings)

    def shift_eggs_to_hard_to_reach(self):
        self.allocation.shift_eggs_to_hard_to_reach(self, data, settings)

