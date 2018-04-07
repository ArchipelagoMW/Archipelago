from allocation import Allocation
from analyzer import Analyzer
from difficultyanalysis import DifficultyAnalysis
from utility import fail
#import time
import random

class Generator(object):
    def __init__(self, data, settings):
        self.data = data
        self.settings = settings
        self.allocation = Allocation(data, settings)
        #self.start_time = time.time()

    def generate_seed(self):
        MAX_ATTEMPTS = 10000
        success = False

        for attempts in range(MAX_ATTEMPTS):
            #if attempts%10000 == 0:
                #minutes_taken = (time.time() - self.start_time)/60
                #print ('%d attempts after %d minutes' % (attempts, minutes_taken))

            self.shuffle()
            analyzer = Analyzer(self.data, self.allocation)
            if analyzer.success:
                if not self.settings.egg_goals:
                    success = True
                    break
                shift_success, goal_eggs = self.shift_eggs_to_hard_to_reach(analyzer.reachable, analyzer.hard_to_reach_items)
                if shift_success:
                    analyzer = Analyzer(self.data, self.allocation, goals=goal_eggs)
                    if analyzer.success:
                        success = True
                        break

        if not success:
            fail('Unable to generate a valid seed after %d attempts.' % MAX_ATTEMPTS)

        print('Seed generated after %d attempts' % (attempts+1))
        
        # Run difficulty analysis
        if True:
            if self.settings.egg_goals:
                goals = analyzer.goals
            else:
                goals = analyzer.hard_to_reach_items

            difficulty_analysis = DifficultyAnalysis(self.data, analyzer, goals)
            print('Difficulty: %.2f' % difficulty_analysis.difficulty_score)
            print('Breakability: %.2f' % difficulty_analysis.breakability_score)

        # Generate Visualization and Print Output:
        if False:
            Analyzer(self.data, self.allocation, visualize=True)
            self.allocation.print_important_item_locations()

        return self.allocation, analyzer

    def shuffle(self):
        self.allocation.shuffle(self.data, self.settings)

    def shift_eggs_to_hard_to_reach(self, reachable_items, hard_to_reach_items):
        return self.allocation.shift_eggs_to_hard_to_reach(self.data, self.settings, reachable_items, hard_to_reach_items)

